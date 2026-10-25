#!/usr/bin/env python3
"""Exact arithmetic checks of K0567, independent of the rooted rank verifier."""

C3 = {8: 1, 6: -3, 4: 3, 2: -1}
C4 = {16: 1, 12: -12, 10: 30, 8: -35, 6: 27, 4: -16, 2: 5}
C5 = {32: 1, 24: -30, 20: 140, 18: 135, 16: -1215,
      14: 2205, 12: -1977, 10: 780, 8: 250,
      6: -495, 4: 255, 2: -49}


def exact(coefficients, denominator, d):
    numerator = sum(coefficient * base**d
                    for base, coefficient in coefficients.items())
    assert numerator % denominator == 0
    return numerator // denominator


def v2(x):
    assert x > 0
    return (x & -x).bit_length() - 1



def rank_mod_101(rows, dimension):
    """Row rank over F_101; exact for 0/1 cube differences in d<=5."""
    matrix = [[x % 101 for x in row] for row in rows]
    rank = 0
    for column in range(dimension):
        pivot = next((i for i in range(rank, len(matrix))
                      if matrix[i][column] != 0), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inv = pow(matrix[rank][column], -1, 101)
        for j in range(column, dimension):
            matrix[rank][j] = matrix[rank][j] * inv % 101
        for i in range(rank + 1, len(matrix)):
            factor = matrix[i][column]
            if factor:
                for j in range(column, dimension):
                    matrix[i][j] = (matrix[i][j] - factor * matrix[rank][j]) % 101
        rank += 1
        if rank == len(matrix):
            break
    return rank


def count_four_sections_direct(d):
    """Exhaustive geometric test, independent of the E4 closed formula."""
    from itertools import combinations

    vertices = [tuple((i >> j) & 1 for j in range(d))
                for i in range(1 << d)]
    count = 0
    for indices in combinations(range(1 << d), 4):
        origin = vertices[indices[0]]
        directions = [
            tuple(vertices[x][j] - origin[j] for j in range(d))
            for x in indices[1:]
        ]
        rank = rank_mod_101(directions, d)
        if rank == d:
            continue
        if all(rank_mod_101(
            directions + [tuple(vertices[x][j] - origin[j]
                                for j in range(d))], d) > rank
               for x in range(1 << d) if x not in indices):
            count += 1
    return count


def main():
    for d in range(3, 65):
        value = exact(C3, 6, d)
        assert v2(value) == d + (d % 2 == 0)
    for d in range(3, 65):
        value = exact(C4, 24, d)
        assert v2(value) == d - (1 if d % 2 else 2)
        assert v2(exact({4: 1, 2: -1}, 2, d)) == d - 1
    for d in range(3, 6):
        assert count_four_sections_direct(d) == exact(C4, 24, d)
    for d in range(5, 65):
        value = exact(C5, 120, d)
        assert value % (1 << d) == 0
        assert (value // (1 << d)) % 2 == (d % 4 in (1, 2))
    assert exact(C3, 6, 3) == 8
    assert exact(C3, 6, 4) == 160
    assert exact(C5, 120, 5) == 2592
    assert exact(C5, 120, 6) == 256704
    # Existing exact finite counts, illustrating the even-q orbit bound.
    for d, q, count in [(4, 6, 40), (5, 6, 1200), (4, 8, 20)]:
        assert count % (1 << max(0, d - v2(q))) == 0
    print("K0567: all exact arithmetic checks passed (d<=64)")


if __name__ == "__main__":
    main()
