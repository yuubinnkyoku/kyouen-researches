"""Search only the unexcluded layer of exactly five missing seed points."""
import argparse
import gzip
import hashlib
import importlib.metadata
import importlib.util
import json
from pathlib import Path
import time
from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical195

HERE = Path(__file__).resolve().parent
FROZEN = HERE.parent/'parabola-size1323-drat-20261109/encoding_fixed.py'
spec = importlib.util.spec_from_file_location('exact_five_fixed_shape', FROZEN)
shape = importlib.util.module_from_spec(spec)
spec.loader.exec_module(shape)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def save(path, obj):
    with path.open('x', encoding='utf-8', newline='\n') as f:
        f.write(json.dumps(obj, indent=2)+'\n')


def build(p, seed, target, origin, complete_pairs, removed, edges):
    h = (p-1)//2
    assert origin in (0, 1) and complete_pairs in (0, 1)
    empty = h+origin+complete_pairs-target
    assert 0 <= empty <= h-complete_pairs
    origin_cost = int(0 in seed and not origin)
    nonzero = [t for t in seed if t]
    loss = removed-origin_cost
    assert 0 <= loss <= len(nonzero)
    clauses, base_nv, kept = shape.build(p, edges, origin, complete_pairs, empty)
    base = base_nv-(p-1)
    assert base >= 4*h
    card = CardEnc.equals([-(base+t) for t in nonzero], bound=loss, top_id=base_nv, encoding=EncType.seqcounter)
    clauses.extend(card.clauses)
    return clauses, max(base_nv, card.nv), base, base_nv, kept, loss


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seed', type=Path, required=True)
    ap.add_argument('--edges', type=Path, required=True)
    ap.add_argument('--target', type=int, default=1259)
    ap.add_argument('--origin', type=int, choices=(0, 1), required=True)
    ap.add_argument('--complete-pairs', type=int, choices=(0, 1), required=True)
    ap.add_argument('--removed', type=int, default=5)
    ap.add_argument('--budget', type=int, default=100000)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    seed_raw = args.seed.read_bytes(); tokens = list(map(int, seed_raw.split()))
    p, n, seed = tokens[0], tokens[1], tokens[2:]
    assert p == 2539 and n == len(seed) and seed == sorted(set(seed)) and all(0 <= t < p for t in seed)
    assert n < args.target and args.budget > 0
    edge_raw = gzip.decompress(args.edges.read_bytes())
    assert sha(edge_raw) == '30e5d500f658a7a245fdff3e5c7830dc62b376632f2a6c1e75dea08552671dff'
    edges = [tuple(map(int, row.split())) for row in edge_raw.decode('ascii').splitlines()[1:]]
    args.output.mkdir(parents=True, exist_ok=False)
    clauses, nv, base, prior, kept, loss = build(p, seed, args.target, args.origin, args.complete_pairs, args.removed, edges)
    raw = (f'p cnf {nv} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses)).encode('ascii')
    (args.output/'input.cnf.gz').write_bytes(gzip.compress(raw, mtime=0))
    report = dict(p=p, origin=args.origin, complete_pairs=args.complete_pairs, target=args.target,
        removed_exactly=args.removed, nonzero_removed_exactly=loss, origin_removal_cost=int(0 in seed and not args.origin),
        seed_path=args.seed.as_posix(), seed_size=n, seed_sha256=sha(seed_raw), edge_input_sha256=sha(edge_raw),
        input_sha256=sha(raw), variables=nv, clauses=len(clauses), point_base=base, base_nv=prior,
        geometric_clauses=kept, conflict_budget=args.budget, source_sha256=sha(Path(__file__).read_bytes()),
        frozen_source_sha256=sha(FROZEN.read_bytes()), python_sat=importlib.metadata.version('python-sat'), proof_enabled=False,
        scope='Exact target and EXACT seed deletions; proven four-deletion region is excluded by a lower cardinality bound. Solver statuses alone are not independent geometric conclusions.')
    save(args.output/'init.json', report)
    phases = []
    for i in range(1, (p+1)//2):
        a, b = i in seed, p-i in seed
        phases.extend(4*i-3+j if v else -(4*i-3+j) for j,v in enumerate((a and b, not a and not b, a and not b, b and not a)))
    phases.extend(base+t if t in seed else -(base+t) for t in range(1,p))
    print('READY exact', args.removed, 'origin', args.origin, 'B', args.complete_pairs, 'vars', nv, 'clauses', len(clauses), flush=True)
    started = time.monotonic()
    with Cadical195(bootstrap_with=clauses) as solver:
        solver.set_phases(phases); solver.conf_budget(args.budget)
        answer = solver.solve_limited()
        model = solver.get_model() if answer is True else None
        stats = solver.accum_stats()
    report.update(status='SAT' if answer is True else 'SOLVER_UNSAT' if answer is False else 'UNKNOWN', solve_seconds=time.monotonic()-started, statistics=stats)
    if model is not None:
        assert len(model) == nv and {abs(v) for v in model} == set(range(1,nv+1))
        positive = {v for v in model if v > 0}
        assert all(any((v > 0) == (abs(v) in positive) for v in c) for c in clauses)
        points = ([0] if args.origin else [])+[t for t in range(1,p) if base+t in positive]
        assert len(points) == args.target and len(set(points)) == len(points)
        assert len([i for i in range(1,(p+1)//2) if i in points and p-i in points]) == args.complete_pairs
        removed, added = sorted(set(seed)-set(points)), sorted(set(points)-set(seed))
        assert len(removed) == args.removed
        save(args.output/'model.json', dict(signed_model=model))
        candidate = (f'{p} {len(points)}\n'+' '.join(map(str,points))+'\n').encode('ascii')
        (args.output/'candidate.txt').write_bytes(candidate)
        report.update(size=len(points), removed=removed, added=added, candidate_sha256=sha(candidate), geometry='NOT_CHECKED')
    save(args.output/'result.json', report)
    print(report['status'], report.get('size'), 'seconds', report['solve_seconds'], flush=True)


if __name__ == '__main__':
    main()
