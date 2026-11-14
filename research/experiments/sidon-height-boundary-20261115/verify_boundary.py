#!/usr/bin/env python3
"""Exact small-instance audit for the q=2|B| fiber-reduction boundary."""
from fractions import Fraction as F
from itertools import combinations
import json


def solve_linear(A, b):
    M = [[F(x) for x in row] + [F(y)] for row, y in zip(A, b)]
    if not M:
        return []
    m, n = len(M), len(M[0]) - 1
    pivots, row = [], 0
    for col in range(n):
        pivot = next((i for i in range(row, m) if M[i][col]), None)
        if pivot is None:
            continue
        M[row], M[pivot] = M[pivot], M[row]
        z = M[row][col]
        M[row] = [v / z for v in M[row]]
        for i in range(m):
            if i != row and M[i][col]:
                z = M[i][col]
                M[i] = [x - z*y for x, y in zip(M[i], M[row])]
        pivots.append(col)
        row += 1
        if row == m:
            break
    for rr in M:
        if all(v == 0 for v in rr[:n]) and rr[n] != 0:
            return None
    solution = [F(0)] * n
    for i, col in enumerate(pivots):
        solution[col] = M[i][n]
    return solution


def rank(vectors):
    if not vectors:
        return 0
    M = [[F(x) for x in row] for row in vectors]
    m, n, row = len(M), len(M[0]), 0
    for col in range(n):
        pivot = next((i for i in range(row, m) if M[i][col]), None)
        if pivot is None:
            continue
        M[row], M[pivot] = M[pivot], M[row]
        z = M[row][col]
        M[row] = [v / z for v in M[row]]
        for i in range(row + 1, m):
            if M[i][col]:
                z = M[i][col]
                M[i] = [x - z*y for x, y in zip(M[i], M[row])]
        row += 1
        if row == m:
            break
    return row


def affine_rank(points):
    if len(points) <= 1:
        return 0
    p0 = points[0]
    return rank([[x-y for x, y in zip(p, p0)] for p in points[1:]])


def cospherical(points):
    if len(points) < 2:
        return False
    dim = len(points[0])
    A, rhs = [], []
    for p in points:
        A.append([2*F(x) for x in p] + [F(1)])
        rhs.append(sum(F(x)*F(x) for x in p))
    solution = solve_linear(A, rhs)
    if solution is None:
        return False
    center, k = solution[:dim], solution[dim]
    return sum(x*x for x in center) + k > 0


def pair_sums_unique(heights):
    sums = [a+b for a, b in combinations(heights, 2)]
    return len(sums) == len(set(sums))


def audit_base(B, heights):
    r, w = len(B[0]), len(B)
    q, ambient_dim = 2*w, r+1
    assert len(heights) >= 2 and pair_sums_unique(heights)
    board = [tuple(b) + (z,) for b in B for z in heights]
    predicted_failure = affine_rank(B) == r and cospherical(B)
    checked = mismatches = 0
    for Q in combinations(board, q):
        checked += 1
        occupied = [tuple(b) for b in B
                    if any(tuple(p[:r]) == tuple(b) for p in Q)]
        vertical_bad = affine_rank(occupied) < r
        geometric_bad = (affine_rank(list(Q)) < ambient_dim
                         or cospherical(list(Q)))
        if geometric_bad != vertical_bad:
            assert geometric_bad and not vertical_bad and predicted_failure
            pairs = []
            for b in B:
                pair = tuple(sorted(p[-1] for p in Q
                                    if tuple(p[:r]) == tuple(b)))
                assert len(pair) == 2
                pairs.append(pair)
            assert len(set(pairs)) == 1
            mismatches += 1
    expected = len(list(combinations(heights, 2))) if predicted_failure else 0
    assert mismatches == expected
    return {
        "base_points": [list(b) for b in B],
        "height_set": list(heights),
        "q": q,
        "base_full_dimensional": affine_rank(B) == r,
        "base_cospherical": cospherical(B),
        "q_subsets_checked": checked,
        "false_safe_q_subsets": mismatches,
    }


def main():
    consecutive_cases = [
        ([(0,)], [[0, 1], [0, 1, 2]]),
        ([(0,), (1,)], [[0, 1], [0, 1, 2]]),
        ([(0,), (1,), (2,)], [[0, 1], [0, 1, 2]]),
        ([(0, 0), (1, 0), (2, 0)], [[0, 1], [0, 1, 2]]),
        ([(0, 0), (1, 0), (0, 1)], [[0, 1], [0, 1, 2]]),
        ([(0, 0), (2, 0), (0, 2), (2, 2)], [[0, 1], [0, 1, 2]]),
        ([(0, 0), (2, 0), (0, 2), (2, 3)], [[0, 1], [0, 1, 2]]),
        ([(0, 0), (2, 0), (0, 2), (2, 2), (1, 4)], [[0, 1], [0, 1, 2]]),
    ]
    consecutive = [audit_base(B, A) for B, sets in consecutive_cases for A in sets]

    sidon_heights = [0, 1, 3, 7]
    sidon_bases = [
        [(0,), (1,)],
        [(0,), (1,), (3,)],
        [(0, 0), (1, 0), (0, 1)],
        [(0, 0), (2, 0), (0, 2), (2, 2)],
        [(0, 0), (2, 0), (0, 2), (2, 3)],
    ]
    sidon = [audit_base(B, sidon_heights) for B in sidon_bases]

    B = [(2, 2), (-2, 2), (2, -2), (1, 3)]
    heights = [0, 1, 2, 3]
    Q = [
        (2, 2, 0), (2, 2, 3), (-2, 2, 0), (-2, 2, 3),
        (2, -2, 0), (2, -2, 3), (1, 3, 1), (1, 3, 2),
    ]
    assert not pair_sums_unique(heights)
    assert affine_rank(B) == 2 and not cospherical(B)
    assert len(Q) == 8 and affine_rank(Q) == 3 and cospherical(Q)
    non_sidon = {
        "base_points": [list(b) for b in B],
        "height_set": heights,
        "q": 8,
        "base_full_dimensional": True,
        "base_cospherical": False,
        "sphere_center": [0, 0, "3/2"],
        "sphere_radius_squared": "41/4",
        "false_safe_q_subset": [list(p) for p in Q],
    }
    result = {
        "consecutive_height_audits": {
            "cases": len(consecutive),
            "q_subsets_checked": sum(x["q_subsets_checked"] for x in consecutive),
            "false_safe_q_subsets": sum(x["false_safe_q_subsets"] for x in consecutive),
            "full_dimensional_cosphere_cases": sum(
                x["base_full_dimensional"] and x["base_cospherical"] for x in consecutive),
        },
        "sidon_height_audits": {
            "height_set": sidon_heights,
            "cases": len(sidon),
            "q_subsets_checked": sum(x["q_subsets_checked"] for x in sidon),
            "false_safe_q_subsets": sum(x["false_safe_q_subsets"] for x in sidon),
            "full_dimensional_cosphere_cases": sum(
                x["base_full_dimensional"] and x["base_cospherical"] for x in sidon),
        },
        "non_sidon_counterexample": non_sidon,
        "all_assertions": "PASS",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
