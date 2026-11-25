#!/usr/bin/env python3
"""Compare leafless SAT encoding with direct checks on all small graphs."""
from itertools import combinations
import json
from pysat.solvers import Cadical195
from audit_saturation_sat import direct
import leafless_saturation_sat


def audit(n):
    edges = list(combinations(range(n),2))
    solvers = {k:Cadical195(bootstrap_with=leafless_saturation_sat.encode(n,k)[1])
               for k in range(1,len(edges))}
    checked = saturated = 0
    try:
        for mask in range(1,(1 << len(edges))-1,2):
            chosen = {e for i,e in enumerate(edges) if mask & (1 << i)}
            assumptions = [i+1 if mask & (1 << i) else -i-1 for i in range(len(edges))]
            expected = all(sum(v in edge for edge in chosen)>=2 for v in range(n)) and direct(n,edges,chosen)
            actual = solvers[len(chosen)].solve(assumptions=assumptions)
            assert actual == expected, (n,mask,actual,expected)
            checked += 1
            saturated += expected
    finally:
        for solver in solvers.values(): solver.delete()
    return {'vertices':n,'graphs_checked':checked,'leafless_saturated':saturated}


if __name__ == '__main__':
    print(json.dumps([audit(n) for n in (4,5,6)],indent=2))
