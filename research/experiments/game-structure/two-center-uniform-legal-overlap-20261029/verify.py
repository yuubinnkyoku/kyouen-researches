#!/usr/bin/env python3
"""Independent rational-state recursion for two-clique-center Node Kayles.

Run: python3 verify.py
"""
from fractions import Fraction
from functools import lru_cache
from itertools import permutations
from math import factorial


def formula(m, A, B):
    a, b, t = len(A), len(B), len(A & B)
    s = a + b - t
    p0 = Fraction(s + 1, (a + 1) * (s + 2))
    p1 = Fraction(s + 1, (b + 1) * (s + 2))
    pnone = Fraction(a*b*(s+2) + t, (a+1)*(b+1)*(s+2))
    return (p0, p1, pnone)


def direct(m, A, B):
    n = m + 2
    neighbor = [0] * n
    neighbor[0] |= 1 << 1
    neighbor[1] |= 1 << 0
    for i in range(m):
        if i in A:
            neighbor[0] |= 1 << (i + 2)
            neighbor[i+2] |= 1
        if i in B:
            neighbor[1] |= 1 << (i + 2)
            neighbor[i+2] |= 2

    @lru_cache(None)
    def rec(mask):
        if mask == 0:
            return (Fraction(0), Fraction(0), Fraction(1))
        count = mask.bit_count()
        sums = [Fraction(0), Fraction(0), Fraction(0)]
        for v in range(n):
            if mask >> v & 1:
                if v == 0:
                    sums[0] += Fraction(1, count)
                elif v == 1:
                    sums[1] += Fraction(1, count)
                else:
                    out = rec(mask & ~(neighbor[v] | (1 << v)))
                    for j in range(3):
                        sums[j] += out[j] / count
        return tuple(sums)

    return rec((1 << n) - 1)


def priority_permutations(m, A, B):
    """Enumerate all priority orders; greedy accept if no selected neighbor."""
    n = m + 2
    neighbor = [0] * n
    neighbor[0] = 1 << 1
    neighbor[1] = 1 << 0
    for i in range(m):
        if i in A:
            neighbor[0] |= 1 << (i + 2)
            neighbor[i + 2] |= 1
        if i in B:
            neighbor[1] |= 1 << (i + 2)
            neighbor[i + 2] |= 2
    counts = [0, 0, 0]
    for order in permutations(range(n)):
        selected = 0
        center = 2
        for v in order:
            if not (neighbor[v] & selected):
                selected |= 1 << v
                if v < 2:
                    center = v
        counts[center] += 1
    return tuple(Fraction(c, factorial(n)) for c in counts)


def check(m, A, B):
    f = formula(m, A, B)
    d = direct(m, A, B)
    assert f == d, (m, A, B, f, d)
    assert sum(f) == 1
    if min(len(A),len(B)) > 0:
        assert f[2] > 0
    else:
        assert f[2] == 0
    return f


def main():
    labeled = 0
    for m in range(6):
        for maskA in range(1 << m):
            A = frozenset(i for i in range(m) if maskA >> i & 1)
            for maskB in range(1 << m):
                B = frozenset(i for i in range(m) if maskB >> i & 1)
                check(m, A, B)
                labeled += 1
    print(f"labeled_graphs_m_0_to_5={labeled}")
    priority_count = 0
    for m in range(5):
        for maskA in range(1 << m):
            A = frozenset(i for i in range(m) if maskA >> i & 1)
            for maskB in range(1 << m):
                B = frozenset(i for i in range(m) if maskB >> i & 1)
                assert formula(m, A, B) == priority_permutations(m, A, B)
                priority_count += 1
    print(f"priority_permutation_checks_m_0_to_4={priority_count}")

    canonical = 0
    for m in range(6, 11):
        for a in range(m+1):
            for b in range(m+1):
                for t in range(max(0,a+b-m),min(a,b)+1):
                    A = frozenset(range(a))
                    B = frozenset(range(t)) | frozenset(range(a,a+b-t))
                    check(m, A, B)
                    canonical += 1
    print(f"canonical_graphs_m_6_to_10={canonical}")
    print(f"total_independent_checks={labeled+canonical}")

    for a in range(1,9):
        for b in range(1,9):
            for m in range(max(a,b),a+b+1):
                old=None
                for t in range(max(0,a+b-m), min(a,b)+1):
                    A=frozenset(range(a))
                    B=frozenset(range(t)) | frozenset(range(a,a+b-t))
                    p=formula(m,A,B)
                    expectation=Fraction(m)+ (1-a)*p[0] +(1-b)*p[1]
                    if old is not None:
                        assert p[2]>old[0]
                        if max(a,b)>1:
                            assert expectation>old[1]
                        else:
                            assert expectation==old[1]
                    old=(p[2],expectation)
    print('overlap_monotonicity_checks=PASS')

    m=4
    for t in (0,1,2):
        A=frozenset((0,1))
        B=frozenset(range(t))|frozenset(range(2,4-t))
        print(f"m=4 a=b=2 overlap={t} p_center1,p_center2,p_none={formula(m,A,B)}")


if __name__=='__main__':
    main()
