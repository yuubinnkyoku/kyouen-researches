#!/usr/bin/env python3
"""Independent checks for the unbounded-arm q=4 spider theorem.

Four-state transfer, binary-word enumeration, and independent graph deletion.
Standard library only; all counts and comparisons use exact integers.
"""
from collections import Counter
from fractions import Fraction
from itertools import product


def transfer_counts(length, center):
    states = {(center, 0): 1, (center, 1): 1}
    for _ in range(2, length + 1):
        nxt = Counter()
        for (a, b), count in states.items():
            for c in (0, 1):
                if a == b == c == 0:
                    continue
                nxt[b, c] += count
        states = nxt
    return sum(count for (a, b), count in states.items() if a or b)


def branch_poly(length, center, first=None):
    out = Counter()
    for word in product((0, 1), repeat=length):
        if first is not None and word[0] != first:
            continue
        chain = (center,) + word + (0,)
        if any(chain[i] == 0 and chain[i-1] == 0 and chain[i+1] == 0
               for i in range(1, length + 1)):
            continue
        e = sum(chain[i] * chain[i+1] for i in range(length))
        degree = length - word.count(0) - e - (1-center)
        out[degree] += 1
    return +out


def convolution(a, b):
    out = Counter()
    for i, x in a.items():
        for j, y in b.items():
            out[i+j] += x*y
    return +out


def predicted(lengths):
    s = 2 + sum(lengths)
    d = len(lengths)
    A, B, C = (Counter({0: 1}) for _ in range(3))
    for ell in lengths:
        A = convolution(A, branch_poly(ell, 1))
        B = convolution(B, branch_poly(ell, 0))
        C = convolution(C, branch_poly(ell, 0, first=0))
    out = Counter()
    for i, v in A.items():
        out[s+i] += v
    for i, v in B.items():
        out[s+d-1+i] += v
    for i, v in C.items():
        out[s+d-1+i] -= v
    out[s+sum(lengths)-1] += 1
    return +out


def direct_graph(lengths):
    edges = []
    n = 1
    for ell in lengths:
        prev = 0
        for _ in range(ell):
            edges.append((prev, n))
            prev = n
            n += 1
    neighbor = [0] * n
    for a, b in edges:
        neighbor[a] |= 1 << b
        neighbor[b] |= 1 << a
    total_points = 1+n+len(edges)
    out = Counter({total_points-1: 1})
    full = (1 << n)-1
    for removed in range(1 << n):
        kept = full ^ removed
        if any(removed & (1 << i) and not (neighbor[i] & kept)
               for i in range(n)):
            continue
        e = sum(bool(kept & (1 << a)) and bool(kept & (1 << b))
                for a, b in edges)
        out[total_points-removed.bit_count()-e] += 1
    return +out


def main():
    A = [1] + [transfer_counts(ell, 1) for ell in range(1, 151)]
    B = [1] + [transfer_counts(ell, 0) for ell in range(1, 151)]
    assert A[:9] == [1, 2, 3, 6, 11, 20, 37, 68, 125]
    assert B[1:9] == [1, 3, 5, 9, 17, 31, 57, 105]
    for ell in range(1, 151):
        if ell >= 4:
            assert A[ell] == sum(A[ell-j] for j in (1, 2, 3))
            assert B[ell] == sum(B[ell-j] for j in (1, 2, 3))
        if ell >= 3:
            assert A[ell]-B[ell] == A[ell-3]
            assert Fraction(B[ell], A[ell]) <= Fraction(17, 20)
        assert 2*B[ell] >= A[ell]
    for ell in range(1, 16):
        assert sum(branch_poly(ell, 1).values()) == A[ell]
        assert sum(branch_poly(ell, 0).values()) == B[ell]
    cases, subsets = 0, 0
    for count in range(1, 5):
        for lengths in product(range(1, 6), repeat=count):
            if sum(lengths) > 11:
                continue
            assert predicted(lengths) == direct_graph(lengths), lengths
            cases += 1
            subsets += 1 << (1+sum(lengths))
    assert cases == 405 and subsets == 685204
    print(f"PASS: 150 lengths, 15 word checks, {cases} graph cases / {subsets:,} subsets")
    print("Sharp ratio: B_5/A_5 = 17/20.")


if __name__ == "__main__":
    main()
