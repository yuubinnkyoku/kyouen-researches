#!/usr/bin/env python3
"""Triangle anti-parallel concurrency scan (AG(2,q)).

C = l1 u l2 u l3 u {R}: triangle + common point of the three anti-parallel
lines D_i = (line through vertex v_i parallel to the opposite side l_i).
Enumerates ALL triangles, reports how many have concurrent D_i, with
definition-level verification of the resulting set.
Companion lemma (canonical coordinates l1: y=0, l2: x=0, l3: x+y=1):
D1^D2 = (1,1), which lies on D3: x+y=0 iff 2=0 in the field,
and all triangles are AGL(2,q)-conjugate (single orbit, stabilizer order 6),
so concurrency happens for ALL triangles iff char 2.
"""
import json, sys, os
from itertools import combinations
sys.path.insert(0, os.path.dirname(__file__))
from boards import affine_plane

def run(q):
    pts, lines = affine_plane(q)
    lines = [frozenset(l) for l in lines]
    tri_count = 0
    found = 0
    witness = None
    warn = 0
    for (i, j, k3) in combinations(range(len(lines)), 3):
        l1, l2, l3 = lines[i], lines[j], lines[k3]
        if not (len(l1 & l2) == 1 and len(l1 & l3) == 1 and len(l2 & l3) == 1):
            continue
        v1, v2, v3 = list(l2 & l3), list(l1 & l3), list(l1 & l2)
        if v1 == v2 or v2 == v3 or v1 == v3:
            continue
        tri_count += 1
        def find_D(v, li):
            for L in lines:
                if v[0] in L and not (L & li) and L != li:
                    return L
            return None
        D1, D2, D3 = find_D(v1, l1), find_D(v2, l2), find_D(v3, l3)
        if D1 is None or D2 is None or D3 is None:
            continue
        common = D1 & D2 & D3
        if not common:
            continue
        R = list(common)[0]
        C = l1 | l2 | l3 | {R}
        cnts = [len(C & L) for L in lines]
        if min(cnts) >= 2 and len(C) == 3 * q - 2:
            found += 1
            if witness is None:
                witness = {'q': q, 'size': len(C),
                           'lines': [sorted(l1), sorted(l2), sorted(l3)],
                           'R': R, 'C': sorted(C)}
        else:
            warn += 1
    print(json.dumps({'q': q, 'triangles': tri_count,
                      'concurrent_D_triangles': found,
                      'failed_verify': warn, 'witness': witness}))

if __name__ == '__main__':
    for q in [int(x) for x in sys.argv[1:]]:
        run(q)
