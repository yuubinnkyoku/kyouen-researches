#!/usr/bin/env python3
"""Exact finite subspace-lattice certificate for five-point 3-flat sections.

No floating point or external packages. The enumerated lattice depends only
on dimensions 3 and 4; the resulting exponential polynomial holds for all d.
"""
from collections import Counter
from fractions import Fraction
from itertools import combinations


def rref(rows, n):
    a = [[Fraction(x) for x in row] for row in rows]
    pivot = 0
    for col in range(n):
        i = next((i for i in range(pivot, len(a)) if a[i][col]), None)
        if i is None:
            continue
        a[pivot], a[i] = a[i], a[pivot]
        v = a[pivot][col]
        a[pivot] = [x / v for x in a[pivot]]
        for i in range(len(a)):
            if i != pivot:
                v = a[i][col]
                if v:
                    a[i] = [a[i][j] - v * a[pivot][j] for j in range(n)]
        pivot += 1
        if pivot == len(a):
            break
    return tuple(tuple(row) for row in a[:pivot])


def polynomial_for_rank(n, wanted):
    """Count n-bit column sequences of length d whose Q-rank is wanted.

    Return coefficients c_b of sum_b c_b * b**d. Rational subspaces are
    represented by their unique exact RREF basis.
    """
    nonzero = [tuple((v >> j) & 1 for j in range(n))
               for v in range(1, 1 << n)]
    spaces = {(): 0}
    for rank in range(1, wanted + 1):
        for vectors in combinations(nonzero, rank):
            basis = rref(vectors, n)
            if len(basis) == rank:
                spaces[basis] = rank
    ordered = sorted(spaces, key=lambda s: spaces[s])
    if n == 4 and wanted == 3:
        upper = [s for s in ordered if spaces[s] == 3]
        incidence = Counter()
        for basis in ordered:
            if spaces[basis] == 2:
                size = 1 + sum(len(rref((*basis, v), n)) == 2 for v in nonzero)
                superspaces = sum(len(rref((*basis, *u), n)) == 3 for u in upper)
                incidence[(size, superspaces)] += 1
        assert incidence == {(3, 5): 30, (4, 4): 15, (4, 3): 10}
        print('rank-2 subspace incidences (binary points, rank-3 superspaces):',
              sorted(incidence.items()))
    exact = {}
    histogram = Counter()
    for basis in ordered:
        rank = spaces[basis]
        contained = 1 + sum(len(rref((*basis, v), n)) == rank for v in nonzero)
        histogram[(rank, contained)] += 1
        polynomial = Counter({contained: 1})
        for smaller in ordered:
            if spaces[smaller] >= rank:
                break
            if len(rref((*basis, *smaller), n)) == rank:
                polynomial.subtract(exact[smaller])
        exact[basis] = polynomial
    total = Counter()
    for basis in ordered:
        if spaces[basis] == wanted:
            total.update(exact[basis])
    return {b: c for b, c in total.items() if c}, histogram


def evaluate(poly, d):
    return sum(coefficient * base ** d for base, coefficient in poly.items())


def stirling(n, k):
    row = [1] + [0] * k
    for i in range(1, n + 1):
        nxt = [0] * (k + 1)
        for j in range(1, min(i, k) + 1):
            nxt[j] = j * row[j] + row[j - 1]
        row = nxt
    return row[k]


def main():
    r43, lattice4 = polynomial_for_rank(4, 3)
    r33, lattice3 = polynomial_for_rank(3, 3)
    assert r43 == {8: 10, 6: 15, 4: -70, 3: -150, 2: 365, 1: -170}
    assert r33 == {8: 1, 4: -6, 3: -3, 2: 17, 1: -9}
    assert sum(v for (rank, _), v in lattice4.items() if rank == 3) == 45
    assert lattice4[(3, 4)] == 20 and lattice4[(3, 6)] == 15
    assert lattice4[(3, 8)] == 10
    print('Q^4 subspaces by (rank, binary points):', sorted(lattice4.items()))
    print('R_4,3(d) coefficients:', sorted(r43.items(), reverse=True))
    print('R_3,3(d) coefficients:', sorted(r33.items(), reverse=True))
    for d in range(3, 9):
        five_subsets = (1 << d) * (evaluate(r43, d) - 10 * evaluate(r33, d)) // 120
        h8 = (1 << (d - 3)) * stirling(d + 1, 4)
        h6_numer = 5 * (10 ** d - 4 * 8 ** d + 6 * 6 ** d
                         - 4 * 4 ** d + 2 ** d)
        assert h6_numer % 48 == 0
        h6 = h6_numer // 48
        h5 = five_subsets - 6 * h6 - 56 * h8
        expected = 15 * (1 << d) * stirling(d + 1, 6)
        assert h5 == expected
        print(f'd={d}: H5={h5}, H6={h6}, H8={h8}, rank3_five_subsets={five_subsets}')
    assert [15 * (1 << d) * stirling(d + 1, 6) for d in (4, 5, 6, 7, 8)] == [0, 480, 20160, 510720, 10160640]
    print('All exact symbolic coefficients and integer checks passed.')


if __name__ == '__main__':
    main()
