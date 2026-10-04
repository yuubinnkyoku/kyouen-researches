#!/usr/bin/env python3
"""Construct center/corner s4 covers without an optimization package.

Uses the shared exact geometry and D4 implementation. These are potential
certificate skeletons: no position WIN/LOSS label is inferred or stored.
The companion verifier reconstructs every safe class independently.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

if not __debug__:
    raise SystemExit("generation requires assertions; do not use python -O")

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "scripts/research"))
from kyouen_core import is_forbidden_quad, square_points  # noqa: E402
from residual_core import d4_perms  # noqa: E402


def orbit_representative(n: int, v: int) -> int:
    x, y = v % n, v // n
    return n * min(x, y) + max(x, y)


def construct(n: int) -> dict:
    if n < 3 or not n % 2:
        raise ValueError("an odd side length at least 3 is required")
    points = square_points(n)
    center = n * n // 2
    base = {0, center}
    corners = {0, n - 1, n * (n - 1), n * n - 1}
    vertices = sorted(set(range(n * n)) - base)
    permutations = d4_perms(n)

    def safe(q: list[int]) -> bool:
        return len(set(q)) == 4 and not is_forbidden_quad([points[v] for v in q])

    def canonical(q) -> tuple[int, ...]:
        return min(tuple(sorted(p[v] for v in q)) for p in permutations)

    def coverage(q) -> set[int]:
        out: set[int] = set()
        for permutation in permutations:
            image = {permutation[v] for v in q}
            if base <= image:
                out.update(image - base)
        return out

    # Full finite class universe, for the stored lower-bound audit.
    classes: dict[tuple[int, ...], set[int]] = defaultdict(set)
    safe_edges = 0
    for a, b in combinations(vertices, 2):
        q = [0, center, a, b]
        if safe(q):
            safe_edges += 1
            classes[canonical(q)].update((a, b))

    if n == 3:
        selected = [[0, center, 1, 2], [0, center, 1, n * n - 1]]
        adjacency = {}
        unmatched: set[int] = set()
    else:
        reuse = n >= 9
        selected = [
            [0, center, n - 1, 3 if reuse else 1],
            [0, center, n * n - 1, 4 if reuse else 2],
        ]
        if reuse:
            # Exactly the existing {center, corner, 1, 2} proof class.
            selected.append([0, center, 1, 2])
        already = set().union(*(coverage(q) for q in selected))
        representatives = sorted(
            {orbit_representative(n, v) for v in vertices if v not in corners}
            - {orbit_representative(n, v) for v in already}
        )
        adjacency = {
            a: {b for b in representatives if b != a and safe([0, center, a, b])}
            for a in representatives
        }
        # Greedy matching followed by length-three augmentations. Under the
        # proved degree bound this must leave at most one unmatched vertex.
        remaining = set(representatives)
        matched: list[tuple[int, int]] = []
        while remaining:
            a = min(remaining)
            choices = adjacency[a] & remaining
            remaining.remove(a)
            if choices:
                b = min(choices)
                remaining.remove(b)
                matched.append((a, b))
        unmatched = set(representatives) - {v for pair in matched for v in pair}
        while len(unmatched) >= 2:
            augment = None
            for a, b in combinations(sorted(unmatched), 2):
                for i, (u, v) in enumerate(matched):
                    if u in adjacency[a] and v in adjacency[b]:
                        augment = (a, b, i, u, v)
                        break
                    if v in adjacency[a] and u in adjacency[b]:
                        augment = (a, b, i, v, u)
                        break
                if augment:
                    break
            if augment is None:
                raise RuntimeError("matching failed; no cover claimed")
            a, b, i, u, v = augment
            matched[i] = (a, u)
            matched.append((b, v))
            unmatched.difference_update((a, b))
        if unmatched:
            a = next(iter(unmatched))
            if not adjacency[a]:
                raise RuntimeError("isolated leftover; no cover claimed")
            matched.append((a, min(adjacency[a])))
            unmatched.clear()
        selected.extend([0, center, a, b] for a, b in matched)

    selected_keys = [canonical(q) for q in selected]
    assert len(set(selected_keys)) == len(selected_keys)
    assert all(safe(q) for q in selected)
    assert set().union(*(classes[key] for key in selected_keys)) == set(vertices)
    positive = sorted(
        {orbit_representative(n, v) for v in vertices if v not in corners}
    )
    max_load = max(len(set(positive) & c) for c in classes.values())
    assert max_load <= 2
    claimed = 2 if n == 3 else (n * n + n - 8 + 3) // 4
    assert len(selected) == claimed
    return {
        "n": n,
        "root": sorted(base),
        "n_vertices": len(vertices),
        "n_safe_edges": safe_edges,
        "n_all_classes": len(classes),
        "max_class_coverage": max(map(len, classes.values())),
        "dual_denominator": 2,
        "dual_positive_vertices": positive,
        "dual_numerator": len(positive),
        "max_dual_class_numerator": max_load,
        "optimal_class_count": claimed,
        "reuses_center_corner_1_2": n >= 9,
        "matching_vertices": len(adjacency),
        "matching_min_degree": min(map(len, adjacency.values()), default=None),
        "selected_coverage_histogram": dict(sorted(Counter(
            len(classes[key]) for key in selected_keys
        ).items())),
        "classes": [
            {"key": list(key), "coverage": sorted(classes[key])}
            for key in selected_keys
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--boards", type=int, nargs="+", default=[3, 5, 7, 9, 11, 13, 15])
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parents[1]
                        / "output/center-corner-cover.json")
    args = parser.parse_args()
    result = {
        "scope": "all safe s4 D4 classes for root {center, corner}; no WIN/LOSS labels",
        "key_encoding": "lexicographically smallest sorted point-id tuple in the D4 orbit",
        "n11_empty_root_outcome": "UNKNOWN",
        "cases": [construct(n) for n in args.boards],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    for case in result["cases"]:
        print(f"n={case['n']} classes={case['optimal_class_count']} "
              f"universe={case['n_all_classes']} dual={case['dual_numerator']}/2")


if __name__ == "__main__":
    main()
