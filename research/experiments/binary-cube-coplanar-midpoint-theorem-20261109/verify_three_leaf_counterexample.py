#!/usr/bin/env python3
"""Verify the explicit 8-vertex counterexample to the three-leaf lemma."""
from itertools import combinations
import json
from audit_saturated_constructions import construct, cycles


def main():
    n = 8
    expected = {(0,1),(0,2),(1,2),(0,3),(0,4),(3,4),(0,5),(1,6),(2,7)}
    edges = construct(n)
    assert edges == expected
    degrees = [sum(v in edge for edge in edges) for v in range(n)]
    leaves = [v for v,degree in enumerate(degrees) if degree == 1]
    assert leaves == [5,6,7]
    quadruples = list(combinations(range(n),4))
    assert all(not cycle <= edges for q in quadruples for cycle in cycles(q))
    missing = [edge for edge in combinations(range(n),2) if edge not in edges]
    for edge in missing:
        assert any(cycle <= edges | {edge} for q in quadruples for cycle in cycles(q)), edge
    print(json.dumps({'vertices':n,'edges':len(edges),'leaves':leaves,
                      'quadruples_checked':len(quadruples),'missing_edges_checked':len(missing),
                      'status':'PASS'},indent=2))


if __name__ == '__main__':
    main()
