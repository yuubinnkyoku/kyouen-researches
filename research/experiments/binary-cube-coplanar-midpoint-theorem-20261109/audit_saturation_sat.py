#!/usr/bin/env python3
"""Compare SAT encoding with direct four-cycle checks on all small graphs."""
from itertools import combinations
import json
from pysat.solvers import Cadical195
import saturation_sat


def direct(n, edges, chosen):
    cycles = []
    for a,b,c,d in combinations(range(n),4):
        for q in ((a,b,c,d), (a,b,d,c), (a,c,b,d)):
            cycles.append({tuple(sorted((q[i],q[(i+1)%4]))) for i in range(4)})
    return (all(not c <= chosen for c in cycles)
            and all(any(c <= chosen | {e} for c in cycles) for e in edges if e not in chosen))


def audit(n):
    edges = list(combinations(range(n),2))
    # Cardinality size 0 and the complete graph are outside the encoder's scope.
    solvers = {size: Cadical195(bootstrap_with=saturation_sat.encode(n,size)[1])
               for size in range(1,len(edges))}
    checked = saturated = 0
    try:
        for mask in range(1, (1 << len(edges)) - 1, 2):
            chosen = {e for i,e in enumerate(edges) if mask & (1 << i)}
            assumptions = [i+1 if mask & (1 << i) else -i-1 for i in range(len(edges))]
            expected = direct(n, edges, chosen)
            actual = solvers[len(chosen)].solve(assumptions=assumptions)
            assert actual == expected, (n,mask,actual,expected)
            checked += 1
            saturated += expected
    finally:
        for solver in solvers.values(): solver.delete()
    return {'vertices':n, 'graphs_checked':checked, 'saturated':saturated}


if __name__ == '__main__':
    print(json.dumps([audit(n) for n in (4,5,6)],indent=2))
