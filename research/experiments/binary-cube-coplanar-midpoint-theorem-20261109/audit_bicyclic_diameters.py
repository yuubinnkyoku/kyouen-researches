#!/usr/bin/env python3
"""Audit bicyclic diameter cases with Floyd-Warshall, independently of BFS."""
from itertools import combinations
import json


def add_path(edges, start, end, length, next_vertex):
    for _ in range(length - 1):
        edges.add(tuple(sorted((start, next_vertex))))
        start, next_vertex = next_vertex, next_vertex + 1
    edges.add(tuple(sorted((start, end))))
    return next_vertex


def theta(a,b,c):
    edges, nxt = set(), 2
    for length in (a,b,c):
        nxt = add_path(edges, 0, 1, length, nxt)
    return nxt, edges


def figure_eight(a,b):
    edges, nxt = set(), 1
    for length in (a,b):
        nxt = add_path(edges, 0, 0, length, nxt)
    return nxt, edges


def dumbbell(a,b,t):
    edges, nxt = set(), 2
    nxt = add_path(edges, 0, 0, a, nxt)
    nxt = add_path(edges, 1, 1, b, nxt)
    nxt = add_path(edges, 0, 1, t, nxt)
    return nxt, edges


def diameter(n, edges):
    d = [[0 if i==j else n+1 for j in range(n)] for i in range(n)]
    for u,v in edges: d[u][v] = d[v][u] = 1
    for k in range(n):
        for i in range(n):
            for j in range(n): d[i][j] = min(d[i][j], d[i][k] + d[k][j])
    assert all(d[u][v] <= n for u,v in combinations(range(n),2))
    return max(max(row) for row in d)


def cases(n):
    result = []
    for a in range(1,n+2):
        for b in range(a,n+2):
            c = n+1-a-b
            if c >= b and (a,b) != (1,1):
                result.append(('theta',(a,b,c),theta(a,b,c)))
    for a in range(3,n+2):
        b = n+1-a
        if b >= a: result.append(('figure-eight',(a,b),figure_eight(a,b)))
    for a in range(3,n+2):
        for b in range(a,n+2):
            t = n+1-a-b
            if t >= 1: result.append(('dumbbell',(a,b,t),dumbbell(a,b,t)))
    out = []
    for kind, parameters, (count,edges) in result:
        assert count == n and len(edges) == n+1
        degrees = [sum(v in e for e in edges) for v in range(n)]
        assert min(degrees) >= 2
        diam = diameter(n, edges)
        assert diam >= 4, (n,kind,parameters,diam)
        out.append({'kind':kind, 'parameters':parameters, 'diameter':diam})
    return out


def main():
    base = cases(10)
    assert {kind:sum(r['kind']==kind for r in base) for kind in ('theta','figure-eight','dumbbell')} == {
        'theta':9,'figure-eight':3,'dumbbell':9}
    extended = [{'vertices':n, 'cases':len(cases(n))} for n in range(11,21)]
    print(json.dumps({'vertices':10,'base_cases':base,'larger_sanity_checks':extended},indent=2))


if __name__ == '__main__':
    main()
