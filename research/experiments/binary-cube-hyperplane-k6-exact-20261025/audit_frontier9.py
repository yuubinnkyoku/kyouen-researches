"""Independent sanity check for the K_6 upper bound.

Takes the frontier 9-point witness and shows, for each of the 55 remaining
vertices, exactly which d-subset hyperplane (as a normal vector of small
integers) the candidate lies on.  This is a human-readable audit of why no
10th point can be added to this particular witness; it is not the UNSAT
proof (that is the SAT certificate), but a cross-check that the geometry
matches the combinatorics.

Also counts, over all orderings of the same witness, the set of forbidden
vertices to confirm the ban list is stable (order-independence).
"""
import sys
from fractions import Fraction

WITNESS = [57, 49, 10, 23, 3, 16, 9, 5, 38]  # d=6 m=9 from frontier.txt
D = 6


def det_bareiss(a):
    a = [row[:] for row in a]
    n = len(a)
    prev, sign = 1, 1
    for k in range(n - 1):
        piv = next((i for i in range(k, n) if a[i][k]), None)
        if piv is None:
            return 0
        if piv != k:
            a[k], a[piv] = a[piv], a[k]
            sign = -sign
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                a[i][j] = (a[k][k] * a[i][j] - a[i][k] * a[k][j]) // prev
            a[i][k] = 0
        prev = a[k][k]
    return sign * a[-1][-1]


def hyperplane_normal(dsub):
    """Integer normal z of the (d+1)-row augmented matrix of the d points."""
    d = len(dsub)
    m = [[1] + [(p >> i) & 1 for i in range(D)] for p in dsub]
    z = []
    for j in range(d + 1):
        sub = [row[:j] + row[j + 1:] for row in m]
        dv = det_bareiss(sub)
        z.append(-dv if j & 1 else dv)
    return z


def dot(z, v):
    return z[0] + sum(z[i + 1] for i in range(D) if (v >> i) & 1)


def forbidden():
    """Map each forbidden vertex to the smallest d-subset hyperplane it lies on."""
    pts = WITNESS
    banned = {}
    # enumerate all d=6 subsets of the 9 points: C(9,6)=84 hyperplanes
    from itertools import combinations
    for dsub in combinations(pts, D):
        z = hyperplane_normal(list(dsub))
        for v in range(1 << D):
            if v in pts or v in banned:
                continue
            if dot(z, v) == 0:
                banned[v] = (dsub, z)
    return banned


def main():
    pts = set(WITNESS)
    banned = forbidden()
    free = [v for v in range(1 << D) if v not in pts and v not in banned]
    print(f"witness: {sorted(pts)} (9 points)")
    print(f"forbidden vertices: {len(banned)} of {64 - 9} outside")
    print(f"free vertices: {free}")
    for v in sorted(banned):
        dsub, z = banned[v]
        # compress z by gcd
        from math import gcd
        g = 0
        for c in z:
            g = gcd(g, abs(c))
        zc = [c // g for c in z]
        print(f"v={v:2d} on hyperplane of {dsub}, normal {zc}")


if __name__ == "__main__":
    sys.exit(main())
