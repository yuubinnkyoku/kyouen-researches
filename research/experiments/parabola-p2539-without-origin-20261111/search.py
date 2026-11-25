"""Exclude the origin and bound the TOTAL number of removed seed points."""
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
spec = importlib.util.spec_from_file_location('without_origin_fixed_shape', FROZEN)
shape = importlib.util.module_from_spec(spec); spec.loader.exec_module(shape)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def save(path, obj):
    with path.open('x', encoding='utf-8', newline='\n') as f:
        f.write(json.dumps(obj, indent=2)+'\n')


def build(p, seed, target, complete_pairs, max_removed, edges):
    h = (p-1)//2
    origin_cost = int(0 in seed)
    assert complete_pairs in (0, 1) and 1 <= target <= h+complete_pairs
    cap = max_removed-origin_cost
    nonzero = [t for t in seed if t]
    assert 0 <= cap <= len(nonzero)
    clauses, base_nv, kept = shape.build(p, edges, 0, complete_pairs, h+complete_pairs-target)
    point_base = base_nv-(p-1)
    assert point_base >= 4*h
    card = CardEnc.atmost([-(point_base+t) for t in nonzero], bound=cap,
                         top_id=base_nv, encoding=EncType.seqcounter)
    clauses.extend(card.clauses)
    return clauses, max(base_nv, card.nv), point_base, base_nv, kept, cap


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seed', type=Path, required=True)
    ap.add_argument('--edges', type=Path, required=True)
    ap.add_argument('--target', type=int, required=True)
    ap.add_argument('--complete-pairs', type=int, choices=(0, 1), required=True)
    ap.add_argument('--max-removed', type=int, default=4)
    ap.add_argument('--budget', type=int, default=100000)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    seed_raw = args.seed.read_bytes(); tokens = list(map(int, seed_raw.split()))
    p, n, seed = tokens[0], tokens[1], tokens[2:]
    assert p == 2539 and len(seed) == n and seed == sorted(set(seed)) and all(0 <= t < p for t in seed)
    assert n < args.target and args.budget > 0
    edge_raw = gzip.decompress(args.edges.read_bytes())
    assert sha(edge_raw) == '30e5d500f658a7a245fdff3e5c7830dc62b376632f2a6c1e75dea08552671dff'
    edges = [tuple(map(int, row.split())) for row in edge_raw.decode('ascii').splitlines()[1:]]
    args.output.mkdir(parents=True, exist_ok=False)
    clauses, nv, base, prior, kept, cap = build(p, seed, args.target, args.complete_pairs, args.max_removed, edges)
    cnf = (f'p cnf {nv} {len(clauses)}\n'+''.join(' '.join(map(str, c))+' 0\n' for c in clauses)).encode('ascii')
    (args.output/'input.cnf.gz').write_bytes(gzip.compress(cnf, mtime=0))
    report = dict(p=p, origin=0, complete_pairs=args.complete_pairs, target=args.target,
                  max_removed=args.max_removed, origin_removal_cost=int(0 in seed), nonzero_removal_bound=cap,
                  seed_path=args.seed.as_posix(), seed_sha256=sha(seed_raw), edge_input_sha256=sha(edge_raw),
                  input_sha256=sha(cnf), variables=nv, clauses=len(clauses), point_base=base, base_nv=prior,
                  geometric_clauses=kept, conflict_budget=args.budget, source_sha256=sha(Path(__file__).read_bytes()),
                  frozen_source_sha256=sha(FROZEN.read_bytes()), python_sat=importlib.metadata.version('python-sat'),
                  scope='No origin, exact target size, zero/one complete pair, TOTAL seed deletions including the absent origin. Solver claims require independent audit.')
    save(args.output/'init.json', report)
    phases = [base+t if t in seed else -(base+t) for t in range(1, p)]
    print('READY no-origin', 'B', args.complete_pairs, 'target', args.target, 'total removed', args.max_removed,
          'nonzero cap', cap, 'vars', nv, 'clauses', len(clauses), flush=True)
    started = time.monotonic()
    with Cadical195(bootstrap_with=clauses, with_proof=True) as solver:
        solver.set_phases(phases); solver.conf_budget(args.budget)
        answer = solver.solve_limited()
        model = solver.get_model() if answer is True else None
        proof = solver.get_proof() if answer is not True else None
        stats = solver.accum_stats()
    report.update(status='SAT' if answer is True else 'SOLVER_UNSAT' if answer is False else 'UNKNOWN',
                  solve_seconds=time.monotonic()-started, statistics=stats)
    if model is not None:
        assert len(model) == nv and {abs(v) for v in model} == set(range(1, nv+1))
        positive = {v for v in model if v > 0}
        assert all(any((v > 0) == (abs(v) in positive) for v in c) for c in clauses)
        points = [t for t in range(1, p) if base+t in positive]
        assert len(points) == args.target
        assert len([i for i in range(1, (p+1)//2) if i in points and p-i in points]) == args.complete_pairs
        removed, added = sorted(set(seed)-set(points)), sorted(set(points)-set(seed))
        assert len(removed) <= args.max_removed
        save(args.output/'model.json', dict(signed_model=model))
        raw = (f'{p} {len(points)}\n'+' '.join(map(str, points))+'\n').encode('ascii')
        (args.output/'candidate.txt').write_bytes(raw)
        report.update(size=len(points), removed=removed, added=added, candidate_sha256=sha(raw), geometry='NOT_CHECKED')
    if proof:
        raw = ('\n'.join(proof)+'\n').encode('ascii')
        (args.output/'proof.drat.gz').write_bytes(gzip.compress(raw, mtime=0))
        report.update(proof_sha256=sha(raw), proof_lines=len(proof), proof_complete=answer is False,
                      independent_proof_audit='NOT_RUN')
    save(args.output/'result.json', report)
    print(report['status'], 'size', report.get('size'), 'proof lines', report.get('proof_lines'),
          'seconds', report['solve_seconds'], flush=True)


if __name__ == '__main__':
    main()
