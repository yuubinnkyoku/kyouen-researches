#!/usr/bin/env python3
"""Independent small state-space DP and exact rational circle audit.
Run: python research/experiments/three-by-four-q6-row-spacings-20261018/verify.py
"""
import itertools
import json
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache


def det(a):
    if len(a) == 1:
        return a[0][0]
    return sum((-1)**j * a[0][j] * det([row[:j] + row[j+1:] for row in a[1:]]) for j in range(len(a)))


def circle_or_line(points):
    # For six points, first find a noncollinear triple. No floating point.
    triple = None
    for a, b, c in itertools.combinations(points, 3):
        if det([[a[0], a[1], 1], [b[0], b[1], 1], [c[0], c[1], 1]]) != 0:
            triple = (a, b, c)
            break
    if triple is None:
        return True
    a, b, c = triple
    return all(det([[p[0]*p[0]+p[1]*p[1], p[0], p[1], 1] for p in (a, b, c, d)]) == 0 for d in points)


def geometry_edges(a, b):
    pts = [(F(x), F(y)) for y in (F(0), a, a+b) for x in range(4)]
    return sorted(sum(1 << i for i in idxs) for idxs in itertools.combinations(range(12), 6)
                  if circle_or_line([pts[i] for i in idxs]))


def solve_bitmasks(edges):
    @lru_cache(None)
    def grundy(mask):
        successors = set()
        for j in range(12):
            if (mask >> j) & 1:
                continue
            new = mask | (1 << j)
            if any(new & edge == edge for edge in edges):
                continue
            successors.add(grundy(new))
        return next(k for k in range(13) if k not in successors)
    safe = [m for m in range(1 << 12) if all(m & e != e for e in edges)]
    terminals = [m for m in safe if all((m >> j) & 1 or
                any((m | (1 << j)) & e == e for e in edges) for j in range(12))]
    return {
        'forbidden_count': len(edges),
        'safe_count': len(safe),
        'terminal_sizes': dict(sorted(Counter(m.bit_count() for m in terminals).items())),
        'grundy_histogram': dict(sorted(Counter(grundy(m) for m in safe).items())),
        'root_grundy': grundy(0),
        'first_child_grundy': sorted(set(grundy(1 << j) for j in range(12))),
    }


def solve_quotient():
    # E1=I union A, E2=I union B; O are free points.
    @lru_cache(None)
    def g(i, a, b, o):
        options = set()
        for j, (v, cap) in enumerate(zip((i, a, b, o), (2, 4, 4, 2))):
            if v == cap:
                continue
            nxt = [i, a, b, o]
            nxt[j] += 1
            if nxt[0] == 2 and (nxt[1] == 4 or nxt[2] == 4):
                continue
            options.add(g(*nxt))
        return next(k for k in range(13) if k not in options)
    # Counts DP includes states with different label multiplicities, and is
    # genuinely independent of the 4096-bitmask recursion.
    # Full 75-type finite certificate, printed in proof.md (X = unsafe).
    expected = [
        [[0,1,2,0,1],[1,0,3,1,0],[2,3,2,0,1],[0,1,0,1,0],[1,0,1,0,1]],
        [[1,0,1,3,0],[0,1,0,2,1],[1,0,1,3,0],[3,2,3,2,1],[0,1,0,1,0]],
        [[0,1,0,1,None],[1,0,1,0,None],[0,1,0,1,None],[1,0,1,0,None],[None,None,None,None,None]],
    ]
    checked = 0
    for i in range(3):
        for a in range(5):
            for b in range(5):
                if expected[i][a][b] is None:
                    continue
                assert g(i,a,b,0) == expected[i][a][b], (i,a,b)
                checked += 1
    assert checked == 66
    assert g(0, 0, 0, 0) == 0
    assert {g(1,0,0,0),g(0,1,0,0),g(0,0,1,0),g(0,0,0,1)} == {1}
    return {'root_grundy': g(0,0,0,0), 'first_child_grundy': [1], 'safe_quotient_types': checked, 'cache_states':g.cache_info().currsize}


def main():
    examples = {
        'none': (F(1), F(3)),
        'ab': (F(1), F(2)),
        'a_times_total': (F(1,2), F(7,2)),
        'b_times_total': (F(7,2), F(1,2)),
        'double': (F(1), F(1)),
    }
    results = {}
    for label, (a,b) in examples.items():
        edges = geometry_edges(a,b)
        prediction = int(a*b == 2) + int(a*(a+b) == 2) + int(b*(a+b) == 2)
        assert len(edges) == prediction, (label, edges)
        if len(edges) == 2:
            assert (edges[0] & edges[1]).bit_count() == 2
        results[label] = {'a':str(a), 'b':str(b), 'edges':edges, **solve_bitmasks(edges)}
    assert [results[k]['root_grundy'] for k in examples] == [0,1,1,1,0]
    assert results['double']['safe_count'] == 3972
    assert results['double']['terminal_sizes'] == {10:16, 11:2}
    assert results['double']['grundy_histogram'] == {0:1378,1:1378,2:608,3:608}
    assert solve_quotient()['root_grundy'] == results['double']['root_grundy']
    results['independent_quotient'] = solve_quotient()
    print(json.dumps(results, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
