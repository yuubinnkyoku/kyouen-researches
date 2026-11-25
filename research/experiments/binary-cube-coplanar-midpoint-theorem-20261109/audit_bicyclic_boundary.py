#!/usr/bin/env python3
"""Check n=8,9 bicyclic kernels by direct cycles and missing-edge additions."""
from itertools import combinations
import json
from audit_bicyclic_diameters import theta, figure_eight, dumbbell, diameter
from audit_saturated_constructions import cycles


def cases(n):
    graphs = []
    for a in range(1,n+2):
        for b in range(a,n+2):
            c = n+1-a-b
            if c >= b and (a,b) != (1,1):
                graphs.append(('theta',(a,b,c),theta(a,b,c)))
    for a in range(3,n+2):
        b = n+1-a
        if b >= a: graphs.append(('figure-eight',(a,b),figure_eight(a,b)))
    for a in range(3,n+2):
        for b in range(a,n+2):
            t = n+1-a-b
            if t >= 1: graphs.append(('dumbbell',(a,b,t),dumbbell(a,b,t)))
    output = []
    all_cycles = [c for q in combinations(range(n),4) for c in cycles(q)]
    for kind,params,(num,edges) in graphs:
        assert num == n and len(edges) == n+1
        assert all(sum(v in e for e in edges)>=2 for v in range(n))
        has_c4 = any(c <= edges for c in all_cycles)
        # An unblocked nonedge stays C4-free when added to a C4-free graph.
        unblocked = [] if has_c4 else [e for e in combinations(range(n),2) if e not in edges
                                      and not any(c <= edges | {e} for c in all_cycles)]
        assert has_c4 or unblocked, (n,kind,params)
        output.append({'kind':kind,'parameters':params,'diameter':diameter(n,edges),
                       'contains_c4':has_c4,'unblocked_nonedge':unblocked[0] if unblocked else None})
    return output


def main():
    result = []
    for n, expected in ((8,12),(9,16)):
        graphs = cases(n)
        assert len(graphs) == expected
        result.append({'vertices':n,'cases':graphs})
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
