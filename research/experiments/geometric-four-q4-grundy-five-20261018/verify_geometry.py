#!/usr/bin/env python3
"""Independent exact circle/line audit and 5x5 finite lower bound.

No geometry or game code is imported from the repository.  The geometric
predicate solves the circle through three points using integer coefficients;
collinear triples are handled as lines.  The 5x5 audit enumerates every
11-point subset, pruning only after a fifth forbidden quadruple is formed.
"""
from collections import Counter
from functools import lru_cache
from itertools import combinations
import json

WITNESS = (
    (0, 0), (0, 4), (1, 1), (1, 3), (3, 1), (3, 2),
    (3, 4), (4, 1), (4, 5), (5, 0), (5, 2),
)


def forbidden(pts):
    a, b, c, d = pts
    u = (b[0] - a[0], b[1] - a[1])
    v = (c[0] - a[0], c[1] - a[1])
    w = (d[0] - a[0], d[1] - a[1])
    delta = u[0] * v[1] - u[1] * v[0]
    if delta == 0:
        return u[0] * w[1] - u[1] * w[0] == 0
    q = lambda p: p[0] * p[0] + p[1] * p[1]
    qb, qc, qd = q(b) - q(a), q(c) - q(a), q(d) - q(a)
    A = -qb * v[1] + qc * u[1]
    B = -u[0] * qc + v[0] * qb
    return delta * qd + A * w[0] + B * w[1] == 0


def edge_census(points):
    return [tuple(e) for e in combinations(range(len(points)), 4)
            if forbidden([points[i] for i in e])]


def witness_audit():
    edges = edge_census(WITNESS)
    expected = [
        (0, 1, 2, 3), (0, 2, 7, 9),
        (4, 6, 7, 10), (5, 6, 7, 8),
    ]
    assert edges == expected, (edges, expected)
    edge_masks = [sum(1 << i for i in edge) for edge in edges]

    @lru_cache(None)
    def grundy(mask):
        options = set()
        for i in range(len(WITNESS)):
            if mask & (1 << i):
                continue
            child = mask | (1 << i)
            if any(child & e == e for e in edge_masks):
                continue
            options.add(grundy(child))
        g = 0
        while g in options:
            g += 1
        return g

    root = grundy(0)
    hist = Counter(grundy(mask) for mask in range(1 << len(WITNESS))
                   if all(mask & e != e for e in edge_masks))
    assert root == 5
    assert sum(hist.values()) == 1635
    assert dict(hist) == {0: 585, 1: 586, 2: 224, 3: 230, 4: 9, 5: 1}
    return {'points': [list(p) for p in WITNESS],
            'forbidden_sets': [[list(WITNESS[i]) for i in e] for e in edges],
            'forbidden_count': len(edges), 'safe_states': sum(hist.values()),
            'root_grundy': root, 'histogram': dict(sorted(hist.items()))}


def five_by_five_audit():
    points = [(x, y) for x in range(5) for y in range(5)]
    edges_by_last = [[] for _ in points]
    for e in edge_census(points):
        edges_by_last[e[-1]].append(sum(1 << i for i in e[:-1]))
    assert sum(map(len, edges_by_last)) == 826
    visited = [0] * 12
    solutions = []

    def rec(next_index, chosen, mask, forbidden_count):
        visited[chosen] += 1
        if chosen == 11:
            solutions.append(mask)
            return
        for i in range(next_index, 25 - (11 - chosen) + 1):
            newly_forbidden = 0
            for triple in edges_by_last[i]:
                if mask & triple == triple:
                    newly_forbidden += 1
                    if forbidden_count + newly_forbidden >= 5:
                        break
            if forbidden_count + newly_forbidden < 5:
                rec(i + 1, chosen + 1, mask | (1 << i),
                    forbidden_count + newly_forbidden)

    rec(0, 0, 0, 0)
    assert not solutions
    assert visited == [1, 15, 120, 680, 3060, 11480, 36620,
                       99646, 175657, 85034, 2568, 0]
    return {'grid': '5x5', 'total_11_subsets': 4457400,
            'forbidden_quadruples_in_grid': 826,
            '11_subsets_with_at_most_4_forbidden_quadruples': len(solutions),
            'visited_nodes_by_depth': visited}


def main():
    print(json.dumps({'witness': witness_audit(),
                      'five_by_five': five_by_five_audit()},
                     ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
