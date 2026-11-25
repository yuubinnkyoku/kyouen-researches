#!/usr/bin/env python3
"""Exhaustively check the leaf bound for n<=6 and the constructions to n=20."""
from itertools import combinations
import json
from audit_saturated_constructions import audit, construct, cycles


def exhaustive(n):
    edges = list(combinations(range(n),2))
    index = {e:i for i,e in enumerate(edges)}
    forbidden = [sum(1 << index[e] for e in c)
                 for q in combinations(range(n),4) for c in cycles(q)]
    all_edges = (1 << len(edges))-1
    counts = {'c4_free':0, 'saturated':0, 'saturated_with_leaf':0}
    for mask in range(1 << len(edges)):
        if any(mask & c == c for c in forbidden):
            continue
        counts['c4_free'] += 1
        missing = all_edges & ~mask
        blocked = 0
        for c in forbidden:
            if (mask & c).bit_count() == 3:
                blocked |= c & ~mask
        if missing & ~blocked:
            continue
        counts['saturated'] += 1
        degrees = [sum(bool(mask & (1 << i)) for i,e in enumerate(edges) if v in e)
                   for v in range(n)]
        if 1 in degrees:
            counts['saturated_with_leaf'] += 1
            assert mask.bit_count() >= (3*n-5)//2, (n,mask)
    return {'vertices':n, **counts}


def main():
    small = [exhaustive(n) for n in (4,5,6)]
    constructions = []
    for n in range(5,21):
        result = audit(n)
        edges = construct(n)
        leaves = sum(sum(v in e for e in edges)==1 for v in range(n))
        assert leaves in (2,3) and len(edges) == (3*n-5)//2
        constructions.append({'vertices':n, 'edges':len(edges), 'leaves':leaves,
                              'missing_edges_checked':result['missing_edges_checked']})
    print(json.dumps({'exhaustive':small,'constructions':constructions},indent=2))


if __name__ == '__main__':
    main()
