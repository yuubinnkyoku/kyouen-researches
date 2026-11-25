"""Nontrivial exhaustive projection controls beyond the two-complete-pair cases."""
import argparse
from itertools import combinations
from pathlib import Path
from pilot import candidate, clauses_for_pair, save, sha
from verify_saved import determinant


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    assert not args.output.exists()
    checks = []
    for p in (17, 19):
        edges = [q for q in combinations(range(p), 4) if determinant(q, p) == 0]
        reduced = [q for q in edges if len({min(t, p-t) for t in q}) == 4]
        assert reduced  # p<=13 has none and alone cannot exercise projection signs.
        h, safe_count, unsafe_count = (p-1)//2, 0, 0
        for d in range(1, h+1):
            clauses = {tuple(sorted(c)) for c in clauses_for_pair(p, reduced, d)}
            assert clauses and clauses == {tuple(sorted(c)) for c in clauses_for_pair(p, edges, d)}
            for mask in range(1 << h):
                positive = {i for i in range(1, h+1) if mask & (1 << (i-1))}
                points = candidate(d, positive, p)
                assert len(points) == len(set(points)) == h+2
                selected = set(points)
                # edges were obtained by direct determinant over EVERY ambient quadruple.
                safe = all(not set(q) <= selected for q in edges)
                sat = all(any((lit > 0) == (abs(lit) in positive) for lit in c) for c in clauses)
                assert sat == safe, (p, d, mask)
                safe_count += safe
                unsafe_count += not safe
        assert safe_count and unsafe_count
        checks.append(dict(p=p, full_edges=len(edges), nontrivial_edges=len(reduced),
                           safe_assignments=safe_count, unsafe_assignments=unsafe_count,
                           assignments=safe_count+unsafe_count))
    save(args.output, dict(checks=checks, total_assignments=sum(r['assignments'] for r in checks),
                          source_sha256=sha(Path(__file__).read_bytes()),
                          scope='Exhaustive p17,p19 assignments exercise nonempty signed clauses and both safe and unsafe templates.'))
    print('PASS', sum(r['assignments'] for r in checks), 'nontrivial projection assignments')


if __name__ == '__main__':
    main()
