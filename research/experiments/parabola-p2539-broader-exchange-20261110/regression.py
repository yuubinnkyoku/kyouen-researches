"""Check changed/absent complete-pair bounded selection against small integer geometry."""
import argparse
from itertools import combinations, product
from pathlib import Path
import sys
from pysat.solvers import Cadical195
from change_pair import HERE, build as changed_build, save, sha
from no_pair import build as absent_build
sys.path.insert(0, str(HERE.parent/'parabola-p2539-pair-pilot-20261110'))
from verify_saved import determinant


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    assert not args.output.exists()
    rows = []
    for p in (5, 7, 17):
        h = (p-1)//2
        edges = [q for q in combinations(range(p), 4) if determinant(q, p) == 0]
        free = list(range(2, h+1))
        seed = next(sorted([0, 1, p-1]+[p-i if side else i for i, side in zip(free, sides)])
                    for sides in product((False, True), repeat=h-1)
                    if all(not set(q) <= set([0, 1, p-1]+[p-i if side else i for i, side in zip(free, sides)]) for q in edges))
        for mode, builder in [('changed-pair', changed_build), ('no-pair', absent_build)]:
            targets = (h+1, h+2) if mode == 'changed-pair' else sorted({max(3, h), h+1})
            assignments = []
            pair_choices = sorted({2, h}) if mode == 'changed-pair' else [None]
            for both in pair_choices:
                variable_pairs = [i for i in range(1, h+1) if i != both]
                for states in product((1, 2, 3), repeat=len(variable_pairs)):
                    choice = dict(zip(variable_pairs, states))
                    if both is not None:
                        choice[both] = 0
                    points = [0]
                    positives = set()
                    for i in range(1, h+1):
                        state = choice[i]
                        positives.add(4*i-3+state)
                        if state in (0, 2):
                            points.append(i)
                        if state in (0, 3):
                            points.append(p-i)
                    safe = all(not set(q) <= set(points) for q in edges)
                    assignments.append((positives, points, safe))
            for target in targets:
                for cap in (0, 1, min(3, len(seed)-1)):
                    clauses, nv, base, prior, _ = builder(p, seed, edges, target, cap)
                    assert base >= 4*h and prior >= base+p-1 and nv >= prior
                    accepted, rejected = 0, 0
                    with Cadical195(bootstrap_with=clauses) as solver:
                        for positives, points, safe in assignments:
                            assumptions = [v if v in positives else -v for v in range(1, 4*h+1)]
                            expected = safe and len(points) == target and len(set(seed)-set(points)) <= cap
                            actual = solver.solve(assumptions=assumptions)
                            assert actual == expected, (mode, p, target, cap, points)
                            accepted += actual
                            rejected += not actual
                    rows.append(dict(mode=mode, p=p, target=target, max_removed=cap,
                                     assignments=len(assignments), accepted=accepted, rejected=rejected))
    assert any(r['accepted'] for r in rows) and any(r['rejected'] for r in rows)
    save(args.output, dict(rows=rows, total_assignments=sum(r['assignments'] for r in rows),
         changed_source_sha256=sha((HERE/'change_pair.py').read_bytes()),
         absent_source_sha256=sha((HERE/'no_pair.py').read_bytes()),
         regression_source_sha256=sha(Path(__file__).read_bytes()),
         scope='Exhaustive small geometry and bounded deletion checks for sampled complete-pair identities and all no-pair states; not a general encoding proof.'))
    print('PASS', sum(r['assignments'] for r in rows), 'changed/no-pair bounded assignments', flush=True)


if __name__ == '__main__':
    main()
