#!/usr/bin/env python3
"""Independent exact enumeration of high-density cube sections for k <= 4.

This tests affine spans of vertex subsets, not normal-vector coefficients.
Modulo 101 rank is exact for the {-1,0,1} minors of order <= 4:
Hadamard's bound is 4^(4/2)=16 < 101.
"""
from itertools import combinations

PRIME = 101


def rank(rows):
    basis = {}
    for row in rows:
        v = [x % PRIME for x in row]
        for j in sorted(basis):
            if v[j]:
                c = v[j]
                v = [(x - c * y) % PRIME for x, y in zip(v, basis[j])]
        j = next((j for j, x in enumerate(v) if x), None)
        if j is not None:
            c = pow(v[j], -1, PRIME)
            basis[j] = [(c * x) % PRIME for x in v]
    return len(basis)


def exact_support_counts(k):
    vertices = [tuple((v >> i) & 1 for i in range(k)) for v in range(1 << k)]
    n = len(vertices)
    result = {}
    for size in range((n + 3) // 4, n // 2 + 1):
        for indices in combinations(range(n), size):
            base = vertices[indices[0]]
            directions = [
                tuple(vertices[v][i] - base[i] for i in range(k))
                for v in indices[1:]
            ]
            r = rank(directions)
            if r >= k:
                continue
            chosen = set(indices)
            # Affine hull must contain no unselected cube vertex.
            if any(
                rank(directions + [
                    tuple(vertices[v][i] - base[i] for i in range(k))
                ]) == r
                for v in range(n) if v not in chosen
            ):
                continue
            # No coordinate axis may lie in the direction space.
            if any(
                rank(directions + [tuple(int(i == j) for i in range(k))]) == r
                for j in range(k)
            ):
                continue
            result[size] = result.get(size, 0) + 1
    return result


def main():
    expected = {
        1: {1: 2},
        2: {1: 4, 2: 2},
        3: {2: 16, 3: 8},
        4: {4: 92, 6: 8},
    }
    for k in range(1, 5):
        found = exact_support_counts(k)
        assert found == expected[k], (k, found, expected[k])
        print(f"k={k}: {found}; coefficient={sum(found.values())}")
    print("PASS: c_1..c_4 = 2,6,24,100")


if __name__ == "__main__":
    main()
