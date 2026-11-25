#!/usr/bin/env python3
"""Independent integer determinant audit for q+1 planar points."""
from itertools import combinations, permutations
from collections import Counter

def det4(rows):
    total = 0
    for p in permutations(range(4)):
        inv = sum(p[i] > p[j] for i in range(4) for j in range(i+1, 4))
        term = 1
        for i, j in enumerate(p):
            term *= rows[i][j]
        total += (-1 if inv & 1 else 1) * term
    return total

def forbidden(points):
    # q>=4: all 4-subsets concyclic or collinear iff q-set is.
    return all(det4([(x*x+y*y, x, y, 1) for x, y in four]) == 0
               for four in combinations(points, 4))

def count_f(points):
    n = len(points)
    return sum(forbidden([points[i] for i in range(n) if i != k])
               for k in range(n))

def grid_audit(width, q, expected):
    grid = [(x,y) for x in range(width) for y in range(width)]
    distribution = Counter()
    for pts in combinations(grid, q+1):
        f = count_f(pts)
        assert f in (0, 1, q+1), (q, pts, f)
        distribution[f] += 1
    assert dict(distribution) == expected, (q, distribution)
    print(f"grid={width} q={q}: {sum(distribution.values())} sets; {dict(sorted(distribution.items()))}")

def witness_audit():
    for q in range(4, 11):
        examples = {
            0: [(i,i*i) for i in range(1,q+2)],
            1: [(i,0) for i in range(q)] + [(0,1)],
            q+1: [(i,0) for i in range(q+1)],
        }
        for expected, points in examples.items():
            assert count_f(points) == expected, (q, expected)
    print("q=4..10: all three integer witness types verified")

if __name__ == "__main__":
    grid_audit(4, 4, {0:2360, 1:1928, 5:80})
    grid_audit(4, 5, {0:7288, 1:688, 6:32})
    witness_audit()
