#!/usr/bin/env python3
"""Independently check the cover's upper and lower certificates with integers.

No shared geometry, generator, MILP, floating point, or solver verdict is
used. Reconstruct every safe s4 class using a translated 3x3 determinant.
This checks finite certificates; the report proves the unbounded theorem.
"""
from __future__ import annotations

import argparse
import copy
import json
from collections import defaultdict
from itertools import combinations
from pathlib import Path

if not __debug__:
    raise SystemExit("verification requires assertions; do not use python -O")


def forbidden(n: int, vertices: tuple[int, ...]) -> bool:
    # Translate the first point to the origin. Expanding the lifted 4x4
    # determinant along its origin row leaves this 3x3 determinant.
    x0, y0 = vertices[0] % n, vertices[0] // n
    rows = []
    for v in vertices[1:]:
        x, y = v % n - x0, v // n - y0
        rows.append((x * x + y * y, x, y))
    a, b, c = rows
    value = (a[0] * (b[1] * c[2] - b[2] * c[1])
             - a[1] * (b[0] * c[2] - b[2] * c[0])
             + a[2] * (b[0] * c[1] - b[1] * c[0]))
    return value == 0


def images(n: int, q: tuple[int, ...]) -> list[tuple[int, ...]]:
    coords = [(v % n, v // n) for v in q]
    m = n - 1
    transforms = (
        lambda x, y: (x, y), lambda x, y: (m - x, y),
        lambda x, y: (x, m - y), lambda x, y: (m - x, m - y),
        lambda x, y: (y, x), lambda x, y: (m - y, x),
        lambda x, y: (y, m - x), lambda x, y: (m - y, m - x),
    )
    return [tuple(sorted(yy * n + xx for xx, yy in (t(x, y) for x, y in coords)))
            for t in transforms]


def universe(n: int) -> tuple[set[int], dict[tuple[int, ...], set[int]], int]:
    base = {0, n * n // 2}
    vertices = set(range(n * n)) - base
    classes: dict[tuple[int, ...], set[int]] = defaultdict(set)
    safe_edges = 0
    for a, b in combinations(sorted(vertices), 2):
        q = tuple(sorted(base | {a, b}))
        if not forbidden(n, q):
            safe_edges += 1
            classes[min(images(n, q))].update((a, b))
    return vertices, classes, safe_edges


def verify_case(case: dict) -> dict:
    n = case["n"]
    assert n >= 3 and n % 2, "unsupported board"
    vertices, classes, safe_edges = universe(n)
    assert case["root"] == [0, n * n // 2], "wrong root"
    assert case["n_vertices"] == len(vertices), "wrong vertex count"
    assert case["n_safe_edges"] == safe_edges, "wrong safe edge count"
    assert case["n_all_classes"] == len(classes), "wrong class count"
    positive = case["dual_positive_vertices"]
    assert len(set(positive)) == len(positive), "duplicate dual weights"
    assert set(positive) <= vertices, "weights outside universe"
    assert case["dual_denominator"] == 2, "unsupported denominator"
    assert case["dual_numerator"] == len(positive), "wrong dual sum"
    weight_set = set(positive)
    maximum_load = max(len(weight_set & coverage) for coverage in classes.values())
    assert maximum_load <= 2, "infeasible lower-bound dual"
    assert case["max_dual_class_numerator"] == maximum_load, "wrong dual maximum"
    lower = (len(positive) + 1) // 2
    if n == 3:
        # This necessary exceptional case has a weaker orbit dual. Full
        # enumeration proves no single class covers seven vertices.
        maximum_size = max(map(len, classes.values()))
        lower = max(lower, (len(vertices) + maximum_size - 1) // maximum_size)
    witness_keys = [tuple(row["key"]) for row in case["classes"]]
    assert len(set(witness_keys)) == len(witness_keys), "duplicate witness classes"
    covered: set[int] = set()
    for row, key in zip(case["classes"], witness_keys):
        assert key in classes, "unsafe or noncanonical witness class"
        assert row["coverage"] == sorted(classes[key]), "incorrect class coverage"
        covered.update(classes[key])
    assert covered == vertices, "incomplete upper-bound cover"
    upper = len(witness_keys)
    assert lower == upper == case["optimal_class_count"], "bounds do not coincide"
    expected = 2 if n == 3 else (n * n + n - 8 + 3) // 4
    assert upper == expected, "does not match theorem"
    expected_reuse = n >= 9
    assert case["reuses_center_corner_1_2"] == expected_reuse, "wrong reuse claim"
    if expected_reuse:
        known = min(images(n, (0, 1, 2, n * n // 2)))
        assert known in witness_keys, "known class was not reused"
    return {"n": n, "safe_edges": safe_edges, "all_classes": len(classes),
            "dual_total": f"{len(positive)}/2", "max_dual_load": f"{maximum_load}/2",
            "lower_bound": lower, "upper_bound": upper,
            "independent_status": "VERIFIED"}


def mutation_checks(case: dict) -> list[str]:
    # The lower bound and upper bound are checked separately. In particular,
    # a solver's claimed optimal objective is never trusted.
    mutations = []
    removed = copy.deepcopy(case)
    removed["classes"] = removed["classes"][:-1]
    mutations.append(("removed_class", removed))
    changed = copy.deepcopy(case)
    changed["classes"][0]["coverage"] = []
    mutations.append(("false_coverage", changed))
    inflated = copy.deepcopy(case)
    inflated["dual_positive_vertices"] = sorted(set(range(case["n"] ** 2))
                                                  - set(case["root"]))
    inflated["dual_numerator"] = len(inflated["dual_positive_vertices"])
    mutations.append(("infeasible_dual", inflated))
    duplicate = copy.deepcopy(case)
    duplicate["classes"].append(copy.deepcopy(duplicate["classes"][0]))
    mutations.append(("duplicate_class", duplicate))
    passed = []
    for label, bad in mutations:
        try:
            verify_case(bad)
        except AssertionError:
            passed.append(label)
        else:
            raise AssertionError(f"invalid certificate accepted: {label}")
    return passed


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--mutation-checks", action="store_true")
    args = parser.parse_args()
    data = json.loads(args.certificate.read_text(encoding="utf-8"))
    assert data["n11_empty_root_outcome"] == "UNKNOWN", "unproved root verdict"
    result = {"cases": [verify_case(case) for case in data["cases"]],
              "n11_empty_root_outcome": "UNKNOWN"}
    if args.mutation_checks:
        case = next(case for case in data["cases"] if case["n"] == 11)
        result["rejected_mutations"] = mutation_checks(case)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
