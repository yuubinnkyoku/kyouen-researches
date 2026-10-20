#!/usr/bin/env python3
"""Exact pair-sum enumeration for three horizontal rows and five common x coordinates."""
from collections import defaultdict, Counter
from itertools import combinations


def circle_patterns(xs, a, b):
    assert len(xs) == 5 and len(set(xs)) == 5 and a > 0 and b > 0
    pairs = defaultdict(list)
    for u, v in combinations(xs, 2):
        pairs[u + v].append((u, v, u * v))
    out = []
    for s, group in pairs.items():
        if len(group) < 2:
            continue
        assert len(group) == 2
        lo, hi = sorted(group, key=lambda p: p[2])
        d = hi[2] - lo[2]
        assert d > 0
        if d == a * (a + b):
            out.append((s, (hi[:2], lo[:2], lo[:2])))
        if d == b * (a + b):
            out.append((s, (lo[:2], lo[:2], hi[:2])))
        if d == a * b:
            out.append((s, (hi[:2], lo[:2], hi[:2])))
    return out


def is_arithmetic(xs):
    x = sorted(xs)
    return all(x[i] - x[i-1] == x[1] - x[0] for i in range(2, 5))


def test():
    max_count = 0
    hist = Counter()
    total = 0
    fours = []
    threes = []
    for xs in combinations(range(11), 5):
        for a in range(1, 8):
            for b in range(1, 8):
                cs = circle_patterns(xs, a, b)
                n = len(cs)
                total += 1
                hist[n] += 1
                max_count = max(max_count, n)
                assert n <= 4
                if n == 4:
                    assert is_arithmetic(xs) and a == b == xs[1]-xs[0]
                    fours.append((xs, a, b))
                if n == 3 and len(threes) < 8:
                    threes.append((xs, a, b))
    assert len(circle_patterns((0,1,2,3,4), 1, 1)) == 4
    assert len(circle_patterns((0,1,2,3,4), 1, 2)) == 3
    print({'configurations': total, 'max_circles': max_count, 'histogram': dict(sorted(hist.items())),
           'four_circle_examples': fours[:8], 'three_circle_examples': threes})

if __name__ == '__main__':
    test()
