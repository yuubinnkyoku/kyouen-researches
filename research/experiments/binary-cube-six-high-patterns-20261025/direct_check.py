#!/usr/bin/env python3
"""Independent exact rational-affine check for q=6 pattern sets, k>32."""
from fractions import Fraction
from random import Random
from itertools import combinations

Q = 6


def rank(matrix):
    a = [[Fraction(x) for x in row] for row in matrix]
    r = 0
    for j in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][j]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        inv = a[r][j]
        a[r] = [x / inv for x in a[r]]
        for i in range(r + 1, len(a)):
            t = a[i][j]
            a[i] = [x - t * y for x, y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def solve(a, b):
    n = len(a)
    mat = [[Fraction(x) for x in row] + [Fraction(rhs)]
           for row, rhs in zip(a, b)]
    for j in range(n):
        p = next(i for i in range(j, n) if mat[i][j])
        mat[j], mat[p] = mat[p], mat[j]
        inv = mat[j][j]
        mat[j] = [x / inv for x in mat[j]]
        for i in range(n):
            if i != j:
                t = mat[i][j]
                mat[i] = [x - t * y for x, y in zip(mat[i], mat[j])]
    return [row[-1] for row in mat]


def has_new_vertex(patterns):
    columns = [[1] * Q] + [[(v >> i) & 1 for i in range(Q)] for v in patterns]
    chosen = [columns[0]]
    for col in columns[1:]:
        if rank(chosen + [col]) > len(chosen):
            chosen.append(col)
        if len(chosen) == Q:
            break
    assert len(chosen) == Q
    originals = {tuple((v >> i) & 1 for v in patterns) for i in range(Q)}
    for bitmask in range(1 << (Q - 1)):
        rhs = [1] + [(bitmask >> j) & 1 for j in range(Q - 1)]
        lam = solve(chosen, rhs)
        candidate = tuple(sum(lam[i] * ((v >> i) & 1) for i in range(Q))
                          for v in patterns)
        if candidate not in originals and all(x in (0, 1) for x in candidate):
            return True
    return False


def predicted(patterns):
    used = set(patterns)
    for r in (3, 5):
        for supp in combinations(range(Q), r):
            for minus in combinations(supp, (r - 1) // 2):
                weights = [0] * Q
                for i in supp:
                    weights[i] = -1 if i in minus else 1
                if all(sum(weights[i] * ((v >> i) & 1) for i in range(Q)) in (0, 1)
                       for v in used):
                    return True
    return False


def main():
    rng = Random(20261025)
    cases = []
    for k in (33, 34, 36, 40, 48, 49, 56):
        for _ in range(6):
            cases.append(rng.sample(range(64), k))
    for r in (3, 5):
        for supp in list(combinations(range(Q), r))[:4]:
            minus = supp[:(r - 1) // 2]
            weights = [0] * Q
            for i in supp:
                weights[i] = -1 if i in minus else 1
            allowed = [v for v in range(64)
                       if sum(weights[i] * ((v >> i) & 1) for i in range(Q)) in (0, 1)]
            for k in (33, min(len(allowed), 40)):
                cases.append(rng.sample(allowed, k))
    for patterns in cases:
        assert has_new_vertex(patterns) == predicted(patterns), len(patterns)
    print('exact rational affine-extension checks:', len(cases), 'passed')


if __name__ == '__main__':
    main()
