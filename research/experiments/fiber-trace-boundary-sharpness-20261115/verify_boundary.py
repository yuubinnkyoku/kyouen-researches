#!/usr/bin/env python3
"""Exact boundary counterexample for the q > 2|B| hypothesis in K0824.

For every r >= 1, B={0,e_1,...,e_r}, m=2 and q=2(r+1).
The trace-capacity model accepts the full occupancy vector, but all board
points lie on one sphere. Only the Python standard library is required.
"""
from argparse import ArgumentParser
from fractions import Fraction


def exact_rank(matrix):
    a = [[Fraction(x) for x in row] for row in matrix]
    if not a:
        return 0
    rows, cols = len(a), len(a[0])
    rank = 0
    for col in range(cols):
        pivot = next((i for i in range(rank, rows) if a[i][col]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        scale = a[rank][col]
        a[rank] = [x / scale for x in a[rank]]
        for i in range(rows):
            if i != rank and a[i][col]:
                factor = a[i][col]
                a[i] = [a[i][j] - factor * a[rank][j]
                        for j in range(cols)]
        rank += 1
        if rank == rows:
            break
    return rank


def verify_dimension(r):
    if r < 1:
        raise ValueError("r must be at least 1")

    base = [(0,) * r]
    for i in range(r):
        base.append(tuple(int(j == i) for j in range(r)))

    w = r + 1
    q = 2 * w
    m = 2

    # The r+1 base points are affinely independent. Thus no affine
    # hyperplane can contain all of them, so every trace has size <= r.
    augmented = [tuple(point) + (1,) for point in base]
    base_rank = exact_rank(augmented)
    assert base_rank == r + 1

    max_trace = r
    max_trace_occupancy = m * max_trace
    assert max_trace_occupancy == 2 * r
    assert max_trace_occupancy <= q - 1
    assert max_trace_occupancy == q - 2

    points = [tuple(point) + (z,) for point in base for z in (0, 1)]
    assert len(points) == q
    assert len(set(points)) == q

    # Multiply the sphere equation by 4 to avoid fractions:
    # sum_j (2*x_j-1)^2 + (2*z-1)^2 = r+1.
    sphere_values = {
        sum((2 * coordinate - 1) ** 2 for coordinate in point)
        for point in points
    }
    assert sphere_values == {r + 1}

    return {
        "d": r + 1,
        "r": r,
        "w": w,
        "m": m,
        "q": q,
        "affine_rank": base_rank,
        "max_trace_size": max_trace,
        "max_trace_occupancy": max_trace_occupancy,
        "q_minus_1": q - 1,
        "sphere_points": len(points),
        "sphere_rhs_times_4": r + 1,
    }


def main():
    parser = ArgumentParser()
    parser.add_argument("--max-r", type=int, default=12)
    args = parser.parse_args()
    if args.max_r < 1:
        parser.error("--max-r must be at least 1")

    for r in range(1, args.max_r + 1):
        result = verify_dimension(r)
        print(
            f"PASS d={result['d']} w={result['w']} q={result['q']} "
            f"rank={result['affine_rank']} "
            f"trace_max={result['max_trace_size']} "
            f"capacity_max={result['max_trace_occupancy']} "
            f"sphere_points={result['sphere_points']}"
        )
    print(f"ALL PASS: r=1..{args.max_r}")


if __name__ == "__main__":
    main()
