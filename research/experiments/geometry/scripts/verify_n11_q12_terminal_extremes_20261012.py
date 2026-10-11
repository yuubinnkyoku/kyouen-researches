#!/usr/bin/env python3
"""11x11 q=12 maximal-safe size bounds: exact integer and finite certificates.

The two circle enumerations are independent: 441 half-integral centers vs
287980 unordered triples with primitive determinant equations.
No third-party packages or solver are needed.
"""
from collections import Counter, defaultdict
from functools import reduce
from itertools import combinations
from math import gcd

N = 11
POINTS = [(x, y) for y in range(N) for x in range(N)]


def center_census():
    result = {}
    for cx2 in range(2 * N - 1):
        for cy2 in range(2 * N - 1):
            groups = defaultdict(set)
            for i, (x, y) in enumerate(POINTS):
                groups[(2*x-cx2)**2 + (2*y-cy2)**2].add(i)
            for r2four, ids in groups.items():
                if len(ids) >= 12:
                    result[(cx2, cy2, r2four)] = frozenset(ids)
    return result


def triple_census():
    groups = defaultdict(int)
    for i, j, k in combinations(range(len(POINTS)), 3):
        ax, ay = POINTS[i]
        bx, by = POINTS[j]
        cx, cy = POINTS[k]
        ux, uy, vx, vy = bx-ax, by-ay, cx-ax, cy-ay
        determinant = ux*vy - vx*uy
        if determinant == 0:
            continue
        p = bx*bx + by*by - ax*ax - ay*ay
        q = cx*cx + cy*cy - ax*ax - ay*ay
        b = uy*q - p*vy
        c = vx*p - ux*q
        d = -determinant*(ax*ax + ay*ay) - b*ax - c*ay
        coeffs = (determinant, b, c, d)
        g = reduce(gcd, (abs(v) for v in coeffs))
        coeffs = tuple(v//g for v in coeffs)
        if coeffs[0] < 0:
            coeffs = tuple(-v for v in coeffs)
        groups[coeffs] |= (1 << i) | (1 << j) | (1 << k)
    return {frozenset(i for i in range(N*N) if mask >> i & 1)
            for mask in groups.values() if mask.bit_count() >= 12}


CIRCLES = center_census()
assert len(CIRCLES) == 21
assert all(len(edge) == 12 for edge in CIRCLES.values())
assert set(CIRCLES.values()) == triple_census()
assert Counter(r for _, _, r in CIRCLES) == {50: 16, 130: 4, 100: 1}
EDGES = list(CIRCLES.values())
assert len(set(EDGES)) == 21

deg = Counter(p for e in EDGES for p in e)
assert Counter(deg.get(p, 0) for p in range(121)) == {0: 9, 1: 24, 2: 36, 3: 52}
assert Counter(len(a & b) for a, b in combinations(EDGES, 2)) == {0: 114, 2: 96}

# Witnesses are omitted-point sets; safe sets are their complements.
MIN_COVER = {(1,1),(2,1),(6,2),(8,6),(7,7),(6,8),(6,10)}
MAX_MINIMAL_COVER = {
    (1,0),(2,0),(0,2),(2,2),(3,2),(10,2),(1,3),(9,3),
    (4,4),(6,4),(0,5),(3,5),(4,6),(6,6),(2,8),(3,8),(3,9),(7,9),
}


def verify_minimal_cover(coords):
    chosen = {N*y+x for x, y in coords}
    hits = [e & chosen for e in EDGES]
    assert all(hits), 'not a transversal'
    assert all(any(h == {p} for h in hits) for p in chosen), 'not minimal'


assert len(MIN_COVER) == 7
assert len(MAX_MINIMAL_COVER) == 18
verify_minimal_cover(MIN_COVER)
verify_minimal_cover(MAX_MINIMAL_COVER)

# At least ceil(21/3)=7 omitted points are required: maximum degree is 3.
assert max(deg.values()) == 3

# If a minimal cover contained >=19 points, pick 19 of its points and
# distinct private circles (one per point). Each picked circle would have
# an exclusive point relative to these 19 circles. Refute all C(21,19)=210
# candidate sets of 19 circles by omitting each pair.
missing = Counter()
for omitted in combinations(range(21), 2):
    chosen = [i for i in range(21) if i not in omitted]
    counts = Counter(p for i in chosen for p in EDGES[i])
    with_exclusive = sum(any(counts[p] == 1 for p in EDGES[i]) for i in chosen)
    missing[19 - with_exclusive] += 1
    assert with_exclusive < 19
assert sum(missing.values()) == 210

print('11x11 q=12: 21 forbidden circles (16 radius^2=25/2, 4 radius^2=65/2, 1 radius^2=25)')
print('two independent circle enumerations agree; no circle contains 13 points')
print('circle intersection histogram:', dict(sorted(Counter(len(a & b) for a,b in combinations(EDGES,2)).items())))
print('point incidence degrees:', dict(sorted(Counter(deg.get(p,0) for p in range(121)).items())))
print('19-subsets rejected:', sum(missing.values()), 'missing-exclusive histogram:', dict(sorted(missing.items())))
print('minimum transversal=7; maximum inclusion-minimal transversal=18')
print('maximum maximal safe size=114; minimum maximal safe size=103')
print('witness for 7 omitted points:', sorted(MIN_COVER))
print('witness for 18 omitted points:', sorted(MAX_MINIMAL_COVER))
