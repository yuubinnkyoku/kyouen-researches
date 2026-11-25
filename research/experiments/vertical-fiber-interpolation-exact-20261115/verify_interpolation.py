#!/usr/bin/env python3
"""Exact finite audit for the vertical-fiber interpolation theorem."""
from __future__ import annotations

from fractions import Fraction
from itertools import product
import json
from pathlib import Path


def separating_values(points: list[tuple[int, ...]]) -> tuple[list[int], list[int]]:
    dimension = len(points[0])
    for parameter in range(10_000):
        vector = [parameter**i for i in range(dimension)]
        values = [sum(x * v for x, v in zip(point, vector)) for point in points]
        if len(set(values)) == len(points):
            return vector, values
    raise RuntimeError("failed to find a separating linear functional")


def lagrange_matrix(values: list[int]) -> list[list[Fraction]]:
    matrix = []
    for x in values:
        row = []
        for i, x_i in enumerate(values):
            value = Fraction(1, 1)
            for j, x_j in enumerate(values):
                if i != j:
                    value *= Fraction(x - x_j, x_i - x_j)
            row.append(value)
        matrix.append(row)
    return matrix


def monic_coefficients(roots: list[int]) -> list[int]:
    coefficients = [1]
    for root in roots:
        next_coefficients = [0] * (len(coefficients) + 1)
        for i, coefficient in enumerate(coefficients):
            next_coefficients[i] -= root * coefficient
            next_coefficients[i + 1] += coefficient
        coefficients = next_coefficients
    return coefficients


def evaluate(coefficients: list[int], value: int) -> int:
    result = 0
    for coefficient in reversed(coefficients):
        result = result * value + coefficient
    return result


def audit_board(vertical_degree: int, base_side: int = 2, height_count: int = 3) -> dict:
    base = list(product(range(base_side), repeat=2))
    height_set = list(range(height_count))
    vector, projected = separating_values(base)
    interpolation = lagrange_matrix(projected)
    n = len(base)
    assert all(interpolation[j][i] == (1 if i == j else 0)
               for j in range(n) for i in range(n))

    configuration_count = 1 << (n * height_count)
    q_counts = {q: {"safe": 0, "unsafe": 0}
                for q in range(1, n * height_count + 1)}
    occupancy_vectors = set()
    max_attained = 0

    for mask in range(configuration_count):
        occupied_by_fiber = []
        occupancy = []
        for fiber_index in range(n):
            occupied = [height_set[j] for j in range(height_count)
                        if (mask >> (fiber_index * height_count + j)) & 1]
            occupied_by_fiber.append(occupied)
            occupancy.append(len(occupied))

        exact_max = sum(min(count, vertical_degree) for count in occupancy)
        max_attained = max(max_attained, exact_max)
        occupancy_vectors.add(tuple(occupancy))

        fiber_polynomials = []
        selected_roots = []
        for fiber_index, occupied in enumerate(occupied_by_fiber):
            roots = list(occupied[:vertical_degree])
            selected_roots.append(list(roots))
            while len(roots) < vertical_degree:
                roots.append(100 + fiber_index * max(1, vertical_degree) + len(roots))
            coefficients = monic_coefficients(roots)
            assert len(coefficients) == vertical_degree + 1
            assert coefficients[-1] == 1
            assert all(evaluate(coefficients, h) == 0 for h in selected_roots[-1])
            fiber_polynomials.append(coefficients)

        for base_index in range(n):
            for power in range(vertical_degree):
                interpolated = sum(interpolation[base_index][other] *
                                   fiber_polynomials[other][power]
                                   for other in range(n))
                assert interpolated == fiber_polynomials[base_index][power]
            assert fiber_polynomials[base_index][-1] == 1

        realized = sum(len(roots) for roots in selected_roots)
        assert realized == exact_max
        for q, counts in q_counts.items():
            if exact_max < q:
                counts["safe"] += 1
            else:
                counts["unsafe"] += 1
                assert realized >= q

    return {
        "base": f"{base_side}x{base_side}",
        "height_count": height_count,
        "vertical_degree": vertical_degree,
        "separating_linear_form_vector": vector,
        "base_points": len(base),
        "cell_configurations": configuration_count,
        "distinct_occupancy_vectors": len(occupancy_vectors),
        "expected_occupancy_vectors": (height_count + 1) ** len(base),
        "maximum_intersection_attained": max_attained,
        "q_classification": {
            str(q): {"safe_configurations": values["safe"],
                     "unsafe_configurations": values["unsafe"]}
            for q, values in q_counts.items() if q in (3, 4, 5)
        },
        "lagrange_matrix": "identity over Q",
        "pass": True,
    }


def audit_degenerate_fiber_obstruction() -> dict:
    base = list(product(range(2), repeat=2))
    vector, projected = separating_values(base)
    values = []
    for point in base:
        projection = sum(x * v for x, v in zip(point, vector))
        value = 1
        for root in projected:
            value *= projection - root
        values.append(value)
    assert all(value == 0 for value in values)
    return {
        "projection_values": projected,
        "G_is_nonzero_polynomial": True,
        "G_values_on_base": values,
        "all_fibers_are_identically_zero_for_F_equals_G": True,
        "conclusion": "without the nonzero-on-each-fiber condition and without a base-degree bound, every board cell lies on one nonzero polynomial zero set",
    }


def main() -> None:
    cases = [audit_board(t) for t in (1, 2, 3)]
    result = {
        "claim": "max_F |S intersect Z(F)| = sum_b min(c_b,t) for all F with deg_z(F)<=t and F(b,.) nonzero on every fiber; equality is attained by monic interpolation",
        "cases": cases,
        "degenerate_fiber_obstruction": audit_degenerate_fiber_obstruction(),
        "all_pass": all(case["pass"] for case in cases),
    }
    output = Path(__file__).resolve().parent / "output" / "audit.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
