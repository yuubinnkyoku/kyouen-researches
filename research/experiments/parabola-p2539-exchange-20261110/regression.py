"""Exhaustively check bounded-deletion semantics and reserved counter domains."""
import argparse
from itertools import combinations, product
import json
from pathlib import Path
import sys
from pysat.solvers import Cadical195
from search import HERE, build, save, sha
from audit import check_model, decode
sys.path.insert(0, str(HERE.parent/'parabola-p2539-pair-pilot-20261110'))
from verify_saved import determinant


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    assert not args.output.exists()
    rows = []
    for p in (5, 7, 17):
        h, d = (p-1)//2, 1
        edges = [q for q in combinations(range(p), 4) if determinant(q, p) == 0]
        free = list(range(2, h+1))
        seed = next(sorted([0, d, p-d]+[p-i if side else i for i, side in zip(free, sides)])
                    for sides in product((False, True), repeat=h-1)
                    if all(not set(q) <= set([0, d, p-d]+[p-i if side else i for i, side in zip(free, sides)]) for q in edges))
        for target in (3, h+1, h+2):
            for removed_cap in sorted({0, min(2, len(seed)-3)}):
                clauses, nv, top, point_vars = build(p, d, edges, seed, target, removed_cap)
                assert top >= 3*h and nv >= top
                sat_count, unsat_count = 0, 0
                with Cadical195(bootstrap_with=clauses) as solver:
                    for states in product(range(3), repeat=h-1):
                        positive = {i+h*state for i, state in zip(free, states)}
                        points = decode(p, d, positive)
                        assumptions = [v if v in positive else -v for i in free for v in (i, h+i, 2*h+i)]
                        expected = (len(points) >= target and len(set(seed)-set(points)) <= removed_cap
                                    and all(not set(q) <= set(points) for q in edges))
                        actual = solver.solve(assumptions=assumptions)
                        assert actual == expected, (p, target, removed_cap, states)
                        sat_count += actual
                        unsat_count += not actual
                rows.append(dict(p=p, target=target, max_removed=removed_cap,
                                 sat=sat_count, unsat=unsat_count, assignments=sat_count+unsat_count))
    assert any(r['sat'] for r in rows) and any(r['unsat'] for r in rows)
    rejected = []
    for name, model in [('missing', [1]), ('duplicate', [1, 1]), ('false-clause', [-1, 2])]:
        try:
            check_model(2, [[1]], model)
        except AssertionError:
            rejected.append(name)
        else:
            raise AssertionError(name)
    save(args.output, dict(rows=rows, total_assignments=sum(r['assignments'] for r in rows),
                          rejected_models=rejected, source_sha256=sha(Path(__file__).read_bytes()),
                          scope='Small-prime exhaustive bounded deletion and target semantics with real geometric edges, including trivial cardinality bounds. Not a general implementation proof.'))
    print('PASS', sum(r['assignments'] for r in rows), 'bounded exchange assignments; three rejected models', flush=True)


if __name__ == '__main__':
    main()
