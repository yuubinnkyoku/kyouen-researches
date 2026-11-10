"""Finite projection regression and malformed maximality evidence controls."""
import argparse
from itertools import combinations
import json
from pathlib import Path
from pilot import candidate, clauses_for_pair, save, sha
from local import repair
from verify_saved import determinant, parse


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--saved', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    assert not args.output.exists()
    checks = []
    for p in (5, 7, 11):
        edges = [q for q in combinations(range(p), 4) if determinant(q, p) == 0]
        reduced = [q for q in edges if len({min(t, p-t) for t in q}) == 4]
        h = (p-1)//2
        count = 0
        for d in range(1, h+1):
            clauses = {tuple(sorted(c)) for c in clauses_for_pair(p, reduced, d)}
            assert clauses == {tuple(sorted(c)) for c in clauses_for_pair(p, edges, d)}
            for mask in range(1 << h):
                positive = {i for i in range(1, h+1) if mask & (1 << (i-1))}
                points = candidate(d, positive, p)
                assert len(points) == len(set(points)) == h+2
                satisfiable = all(any((lit > 0) == (abs(lit) in positive) for lit in c) for c in clauses)
                safe = all(determinant(q, p) != 0 for q in combinations(points, 4))
                assert satisfiable == safe, (p, d, mask)
                count += 1
        checks.append(dict(p=p, forbidden_edges=len(edges), reduced_edges=len(reduced), assignments=count))
    points = list(range(8))
    edges = [(0, 1, 2, 3), (0, 2, 4, 5), (1, 3, 6, 7)]
    fixed, removed, bad = repair(points, edges)
    assert bad == 3 and set(fixed) == set(points)-set(removed)
    assert all(not set(q) <= set(fixed) for q in edges)
    # Each deleted point is necessary for this particular repair, not optimality.
    assert all(any(set(q) <= set(fixed+[t]) for q in edges) for t in removed)
    raw = (args.saved/'candidate.txt').read_bytes()
    blockers = (args.saved/'blockers.txt').read_bytes()
    p, n, rows = parse(raw, blockers)
    def encoded(altered):
        return (f'{p} {n} {p-n}\n'+''.join(' '.join(map(str, row))+'\n' for row in altered)).encode('ascii')
    mutations = {'missing-row': rows[:-1], 'duplicate-target': [rows[0]]+rows[:-1]}
    altered = [row[:] for row in rows]; altered[0][-1] = altered[0][-2]
    mutations['duplicate-vertex'] = altered
    altered = [row[:] for row in rows]; altered[0][0] = int(raw.split()[2])
    mutations['selected-target'] = altered
    # Keep syntax and containment valid but replace one true blocker with a nonedge.
    selected = list(map(int, raw.split()))[2:]
    t = rows[0][0]
    q = next(tuple(sorted((t,)+triple)) for triple in combinations(selected, 3)
             if determinant(tuple(sorted((t,)+triple)), p) != 0)
    altered = [row[:] for row in rows]; altered[0] = [t]+list(q)
    mutations['nonzero-determinant'] = altered
    rejected = []
    for name, value in mutations.items():
        try:
            parse(raw, encoded(value))
        except AssertionError:
            rejected.append(name)
        else:
            raise AssertionError('accepted mutation '+name)
    save(args.output, dict(projection_checks=checks, total_assignments=sum(c['assignments'] for c in checks),
                          repair_control=True, rejected_blocker_controls=rejected,
                          source_sha256=sha(Path(__file__).read_bytes()),
                          scope='Small-prime exhaustive equivalence and five corrupt blocker controls; no general proof of implementation correctness.'))
    print('PASS 192 assignments, repair control, five rejected blocker mutations')


if __name__ == '__main__':
    main()
