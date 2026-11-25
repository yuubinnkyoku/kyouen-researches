"""Search bounded exchanges with origin retained and no complete pair."""
import argparse
import gzip
import importlib.metadata
import json
from pathlib import Path
import time
from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical195
from change_pair import HERE, FROZEN, shape, old_pair, sha, save


def build(p, seed, edges, target, max_removed):
    h = (p-1)//2
    assert 3 <= target <= h+1 and 0 <= max_removed <= len(seed)-1 and 0 in seed
    clauses, base_nv, kept = shape.build(p, edges, 1, 0, h+1-target)
    point_base = base_nv-(p-1)
    assert point_base >= 4*h
    card = CardEnc.atmost([-(point_base+t) for t in seed if t], bound=max_removed,
                         top_id=base_nv, encoding=EncType.seqcounter)
    clauses.extend(card.clauses)
    return clauses, max(base_nv, card.nv), point_base, base_nv, kept


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seed', type=Path, required=True)
    ap.add_argument('--edges', type=Path, required=True)
    ap.add_argument('--target', type=int, required=True)
    ap.add_argument('--max-removed', type=int, default=4)
    ap.add_argument('--budget', type=int, default=100000)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    seed_raw = args.seed.read_bytes()
    values = list(map(int, seed_raw.split()))
    p, n = values[:2]
    seed = values[2:]
    assert p == 2539 and len(seed) == n and seed == sorted(set(seed))
    assert n < args.target and args.budget > 0
    old_pair(p, seed)
    raw = gzip.decompress(args.edges.read_bytes())
    assert raw.splitlines()[0] == b'2539 38868'
    edges = [tuple(map(int, row.split())) for row in raw.decode('ascii').splitlines()[1:]]
    assert len(edges) == 38868
    args.output.mkdir(parents=True, exist_ok=False)
    clauses, nv, point_base, base_nv, kept = build(p, seed, edges, args.target, args.max_removed)
    cnf = (f'p cnf {nv} {len(clauses)}\n'+''.join(' '.join(map(str, c))+' 0\n' for c in clauses)).encode('ascii')
    (args.output/'input.cnf.gz').write_bytes(gzip.compress(cnf, mtime=0))
    report = dict(p=p, origin=1, complete_pairs=0, target=args.target, max_removed=args.max_removed,
                  seed_path=args.seed.as_posix(), seed_sha256=sha(seed_raw), edge_input_sha256=sha(raw),
                  input_sha256=sha(cnf), variables=nv, clauses=len(clauses), point_base=point_base,
                  base_nv=base_nv, geometric_clauses=kept, conflict_budget=args.budget,
                  source_sha256=sha(Path(__file__).read_bytes()), frozen_source_sha256=sha(FROZEN.read_bytes()),
                  helper_source_sha256=sha((HERE/'change_pair.py').read_bytes()),
                  python_sat=importlib.metadata.version('python-sat'), proof_enabled=False,
                  scope='Origin fixed and no complete pair; exact target size and bounded seed deletion. Negative solver results are unaudited.')
    save(args.output/'init.json', report)
    # Point phases retain the seed where possible; they do not constrain the model.
    phases = [point_base+t if t in seed else -(point_base+t) for t in range(1, p)]
    print('READY no complete pair', 'target', args.target, 'vars', nv, 'clauses', len(clauses), flush=True)
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
        assert len(points) == args.target and all(not (i in points and p-i in points) for i in range(1, (p+1)//2))
        removed, added = sorted(set(seed)-set(points)), sorted(set(points)-set(seed))
        assert len(removed) <= args.max_removed
        save(args.output/'model.json', dict(signed_model=model))
        candidate = (f'{p} {len(points)}\n'+' '.join(map(str, points))+'\n').encode('ascii')
        (args.output/'candidate.txt').write_bytes(candidate)
        report.update(size=len(points), removed=removed, added=added, candidate_sha256=sha(candidate),
                      all_clauses_checked=True, geometry='NOT_CHECKED')
    save(args.output/'result.json', report)
    print(report['status'], 'size', report.get('size'), 'seconds', report['solve_seconds'], flush=True)


if __name__ == '__main__':
    main()
