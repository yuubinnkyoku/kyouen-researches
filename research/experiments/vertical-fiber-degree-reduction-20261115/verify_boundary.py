#!/usr/bin/env python3
"""Exact boundary witnesses for the q > t|B| fiber-intersection theorem.

This verifier checks finite sharpness examples, not the universal root bound.
It tests simplex bases in dimensions 1..8, fiber degrees 1..8, and explicit
irreducible integer examples in degrees 1, 2, and 3.
"""
from itertools import combinations
from math import prod


def simplex_base(r: int):
    zero = (0,) * r
    basis = []
    for i in range(r):
        v = [0] * r
        v[i] = 1
        basis.append(tuple(v))
    return [zero, *basis]


def eval_product_polynomial(z: int, roots: tuple[int, ...]) -> int:
    return prod(z - a for a in roots)


def check_reducible_boundary(r: int, t: int) -> None:
    B = simplex_base(r)
    w = len(B)
    q = t * w
    heights = tuple(range(1, t + 1))

    # F(z)=prod_{j=1}^t(z-j) is monic of degree t and vanishes
    # at every selected height in every fiber.
    points = [(b, z) for b in B for z in heights]
    assert len(points) == q
    assert all(eval_product_polynomial(z, heights) == 0 for _, z in points)

    # Every affine hyperplane meets the r-dimensional simplex vertices
    # in at most r points. Check the capacity inequality for all subsets
    # of the corresponding maximum possible trace size.
    for k in range(r + 1):
        for T in combinations(B, k):
            occupancy_sum = t * len(T)
            assert occupancy_sum <= q - 1, (r, t, T, occupancy_sum, q - 1)

    assert t * r <= q - 1


def check_irreducible_integer_examples(r: int) -> None:
    B = simplex_base(r)
    # x_1 is 0 on the zero vertex and e_2,...,e_r, and 1 on e_1.
    x1_values = [b[0] for b in B]

    # t=1: F=z-x_1.
    roots_by_x1 = {0: (0,), 1: (1,)}
    assert all(z - x1 == 0 for x1, roots in roots_by_x1.items() for z in roots)
    assert sum(len(roots_by_x1[x]) for x in x1_values) == len(B)
    assert len(set(roots_by_x1[0] + roots_by_x1[1])) == 2

    # t=2: F=z(z-3)+2*x_1.
    roots_by_x1 = {0: (0, 3), 1: (1, 2)}
    for x1, roots in roots_by_x1.items():
        assert all(z * (z - 3) + 2 * x1 == 0 for z in roots)
        assert len(set(roots)) == 2
    assert sum(len(roots_by_x1[x]) for x in x1_values) == 2 * len(B)
    assert len(set(roots_by_x1[0] + roots_by_x1[1])) == 4

    # t=3: F=z(z-4)(z-5)-12*x_1.
    roots_by_x1 = {0: (0, 4, 5), 1: (1, 2, 6)}
    for x1, roots in roots_by_x1.items():
        assert all(z * (z - 4) * (z - 5) - 12 * x1 == 0 for z in roots)
        assert len(set(roots)) == 3
    assert sum(len(roots_by_x1[x]) for x in x1_values) == 3 * len(B)
    assert len(set(roots_by_x1[0] + roots_by_x1[1])) == 6

    # Every base-hyperplane trace is proper, so c_b=t passes at q=t|B|.
    for t in (1, 2, 3):
        q = t * len(B)
        assert t * (len(B) - 1) <= q - 1


def main() -> None:
    cases = 0
    for r in range(1, 9):
        for t in range(1, 9):
            check_reducible_boundary(r, t)
            cases += 1
        check_irreducible_integer_examples(r)
    print({
        "status": "PASS",
        "simplex_dimensions": 8,
        "fiber_degrees": 8,
        "reducible_boundary_cases": cases,
        "irreducible_integer_degrees": [1, 2, 3],
        "claim": "finite sharpness witnesses only; universal q>t*w theorem is proved separately",
    })


if __name__ == "__main__":
    main()
