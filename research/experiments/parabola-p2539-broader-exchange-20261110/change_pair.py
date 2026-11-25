"""Keep the origin, change the complete pair, and bound deletions of seed points."""
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
spec = importlib.util.spec_from_file_location('changed_pair_frozen_shape', FROZEN)
shape = importlib.util.module_from_spec(spec)
spec.loader.exec_module(shape)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def save(path, obj):
    with path.open('x', encoding='utf-8', newline='\n') as f:
        f.write(json.dumps(obj, indent=2)+'\n')


def old_pair(p, seed):
    pairs = [i for i in range(1, (p+1)//2) if i in seed and p-i in seed]
    assert len(pairs) == 1 and 0 in seed
    return pairs[0]


def build(p, seed, edges, target, max_removed):
    h = (p-1)//2
    d = old_pair(p, seed)
    assert 3 <= target <= h+2 and 0 <= max_removed <= len(seed)-1
    clauses, base_nv, kept = shape.build(p, edges, 1, 1, h+2-target)
    # The frozen builder places all point variables at the end of its domain.
    point_base = base_nv-(p-1)
    assert point_base >= 4*h
    clauses.append([-(4*d-3)])  # BOTH of the old complete pair is forbidden.
    inputs = [-(point_base+t) for t in seed if t]
    card = CardEnc.atmost(inputs, bound=max_removed, top_id=base_nv, encoding=EncType.seqcounter)
    clauses.extend(card.clauses)
    nv = max(base_nv, card.nv)
    return clauses, nv, point_base, base_nv, kept


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seed', type=Path, required=True)
    ap.add_argument('--edges', type=Path, required=True)
    ap.add_argument('--target', type=int, required=True)
    ap.add_argument('--max-removed', type=int, default=3)
    ap.add_argument('--budget', type=int, default=100000)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    seed_raw = args.seed.read_bytes()
    values = list(map(int, seed_raw.split()))
    p, n = values[:2]
    seed = values[2:]
    assert p == 2539 and len(seed) == n and seed == sorted(set(seed))
    assert len(seed) < args.target and args.budget > 0
    d = old_pair(p, seed)
    raw = gzip.decompress(args.edges.read_bytes())
    assert raw.splitlines()[0] == b'2539 38868'
    edges = [tuple(map(int, row.split())) for row in raw.decode('ascii').splitlines()[1:]]
    assert len(edges) == 38868
    args.output.mkdir(parents=True, exist_ok=False)
    clauses, nv, point_base, base_nv, kept = build(p, seed, edges, args.target, args.max_removed)
    cnf = (f'p cnf {nv} {len(clauses)}\n'+''.join(' '.join(map(str, c))+' 0\n' for c in clauses)).encode('ascii')
    (args.output/'input.cnf.gz').write_bytes(gzip.compress(cnf, mtime=0))
    report = dict(p=p, origin=1, complete_pairs=1, excluded_complete_pair=d, target=args.target,
                  max_removed=args.max_removed, seed_path=args.seed.as_posix(), seed_sha256=sha(seed_raw),
                  edge_input_sha256=sha(raw), input_sha256=sha(cnf), variables=nv, clauses=len(clauses),
                  point_base=point_base, base_nv=base_nv, geometric_clauses=kept, conflict_budget=args.budget,
                  source_sha256=sha(Path(__file__).read_bytes()), frozen_source_sha256=sha(FROZEN.read_bytes()),
                  python_sat=importlib.metadata.version('python-sat'), proof_enabled=False,
                  scope='Origin fixed; exactly one complete pair different from the seed pair. Exact target size, bounded seed deletion. Negative results are solver-only.')
    save(args.output/'init.json', report)
    phases = []
    for i in range(1, (p+1)//2):
        low, high = i in seed, p-i in seed
        states = (low and high, not low and not high, low and not high, high and not low)
        phases.extend((4*i-3+j) if state else -(4*i-3+j) for j, state in enumerate(states))
    print('READY changed pair', 'target', args.target, 'vars', nv, 'clauses', len(clauses), flush=True)
    started = time.monotonic()
    with Cadical195(bootstrap_with=clauses) as solver:
        solver.set_phases(phases)
        solver.conf_budget(args.budget)
        answer = solver.solve_limited()
        model = solver.get_model() if answer is True else None
        statistics = solver.accum_stats()
    report.update(status='SAT' if answer is True else 'SOLVER_UNSAT' if answer is False else 'UNKNOWN',
                  solve_seconds=time.monotonic()-started, statistics=statistics)
    if model is not None:
        assert len(model) == nv and {abs(v) for v in model} == set(range(1, nv+1))
        positive = {v for v in model if v > 0}
        assert all(any((v > 0) == (abs(v) in positive) for v in c) for c in clauses)
        points = [0]+[t for t in range(1, p) if point_base+t in positive]
        assert len(points) == args.target and old_pair(p, points) != d
        removed, added = sorted(set(seed)-set(points)), sorted(set(points)-set(seed))
        assert len(removed) <= args.max_removed
        save(args.output/'model.json', dict(signed_model=model))
        candidate = (f'{p} {len(points)}\n'+' '.join(map(str, points))+'\n').encode('ascii')
        (args.output/'candidate.txt').write_bytes(candidate)
        report.update(size=len(points), removed=removed, added=added, complete_pair=old_pair(p, points),
                      candidate_sha256=sha(candidate), all_clauses_checked=True, geometry='NOT_CHECKED')
    save(args.output/'result.json', report)
    print(report['status'], 'size', report.get('size'), 'pair', report.get('complete_pair'), 'seconds', report['solve_seconds'], flush=True)


if __name__ == '__main__':
    main()
