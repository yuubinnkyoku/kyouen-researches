#!/usr/bin/env python3
"""Audit the odd/even constructions by directly enumerating four-cycles."""
from itertools import combinations
import json


def construct(n):
    if n < 5:
        raise ValueError('n must be at least 5')
    k = (n - 3) // 2 if n % 2 else (n - 4) // 2
    edges = set()
    for i in range(k):
        a, b = 2*i+1, 2*i+2
        edges.update(((0,a), (0,b), (a,b)))
    if n % 2:
        edges.update(((1,2*k+1), (0,2*k+2)))
    else:
        edges.update(((0,2*k+1), (1,2*k+2), (2,2*k+3)))
    return edges


def cycles(vertices):
    a, b, c, d = vertices
    for v in ((a,b,c,d), (a,b,d,c), (a,c,b,d)):
        yield {tuple(sorted((v[i], v[(i+1)%4]))) for i in range(4)}


def audit(n):
    edges = construct(n)
    assert len(edges) == (3*n-5)//2
    all_edges = set(combinations(range(n),2))
    assert edges <= all_edges
    quadruples = list(combinations(range(n),4))
    assert all(not cycle <= edges for q in quadruples for cycle in cycles(q))
    missing = sorted(all_edges - edges)
    for edge in missing:
        # Any new cycle must contain both endpoints of the added edge.
        others = [v for v in range(n) if v not in edge]
        found = any(cycle <= edges | {edge}
                    for pair in combinations(others,2)
                    for cycle in cycles(tuple(sorted(edge + pair))))
        assert found, (n, edge)
    return {'dimension':n, 'edges':len(edges), 'missing_edges_checked':len(missing),
            'quadruples_checked_for_safety':len(quadruples), 'status':'PASS'}


if __name__ == '__main__':
    print(json.dumps([audit(n) for n in range(5,21)], indent=2))
