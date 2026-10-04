#!/usr/bin/env python3
"""Exhaust small clutters and independently audit geometric witnesses."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from twin_core import (bits, compress, grundy_occupied, grundy_residual,
                       minimal, twin_classes)

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "scripts/research"))
from kyouen_core import Board, is_forbidden_quad, square_points  # noqa: E402
from residual_core import residual_R  # noqa: E402


def antichains(m: int):
    candidates = [s for s in range(1, 1 << m) if s.bit_count() >= 2]

    def walk(remaining: list[int], chosen: list[int]):
        if not remaining:
            yield tuple(sorted(chosen))
            return
        edge, rest = remaining[0], remaining[1:]
        yield from walk(rest, chosen)
        compatible = [other for other in rest if other & edge != other
                      and other & edge != edge]
        yield from walk(compatible, chosen + [edge])

    yield from walk(candidates, [])


def audit_clutters() -> dict:
    cases = []
    total = reduced = nonisolated = 0
    for m in range(1, 6):
        count = reducible = incident = 0
        for edges in antichains(m):
            vertices = (1 << m) - 1
            smaller, reduced_edges = compress(vertices, edges)
            count += 1
            if smaller == vertices:
                continue
            reducible += 1
            nonempty_link = any(
                len(group) >= 3 and any(edge & (1 << group[0]) for edge in edges)
                for group in twin_classes(vertices, edges)
            )
            incident += nonempty_link
            original = grundy_occupied(vertices, edges)
            deleted = grundy_occupied(smaller, reduced_edges)
            baseline = grundy_residual(vertices, edges, False)
            optimized = grundy_residual(vertices, edges, True)
            assert original["grundy"] == deleted["grundy"] == baseline["grundy"] \
                == optimized["grundy"], (m, edges)
        cases.append({"vertices": m, "all_clutters": count,
                      "reducible_clutters": reducible,
                      "nonisolated_reducible_clutters": incident})
        total += count
        reduced += reducible
        nonisolated += incident
    # Parity and positivity are essential: two equal leaves cannot be reduced
    # to one, or to zero, in the star on vertices {0,1,2}.
    star = (5, 6)  # {0,2}, {1,2}
    original = grundy_occupied(7, star)["grundy"]
    one_leaf = grundy_occupied(5, (5,))["grundy"]
    no_leaf = grundy_occupied(4, ())["grundy"]
    assert original == 2 and one_leaf == no_leaf == 1
    # All vertices of a single residual triple have identical EMPTY pair
    # graph neighborhoods, but different full links. Pair-only compression
    # would replace this two-move game by a one-move game and is unsound.
    triple = grundy_occupied(7, (7,))["grundy"]
    pair_only = grundy_occupied(1, ())["grundy"]
    assert triple == 0 and pair_only == 1
    return {"cases": cases, "all_clutters": total, "reducible_clutters": reduced,
            "nonisolated_reducible_clutters": nonisolated,
            "even_class_counterexample": {"edges": [[0, 2], [1, 2]],
                "original_grundy": original, "one_leaf_grundy": one_leaf,
                "no_leaf_grundy": no_leaf},
            "pair_only_counterexample": {"edges": [[0, 1, 2]],
                "original_grundy": triple, "one_vertex_grundy": pair_only},
            "status": "VERIFIED"}


def audit_geometry(samples: dict) -> list[dict]:
    audited = []
    for case in samples["cases"]:
        witness = case["witness"]
        if witness is None:
            continue
        n = case["n"]
        occupied = witness["occupied"]
        listed_legal = witness["legal"]
        points = square_points(n)
        # Legality on the full board, checked without the C++ quad table.
        from itertools import combinations
        assert all(not is_forbidden_quad([points[v] for v in q])
                   for q in combinations(occupied, 4)), "unsafe input position"
        triples = list(combinations(occupied, 3))
        legal = [v for v in range(n * n) if v not in set(occupied)
                 and all(not is_forbidden_quad([points[p] for p in triple + (v,)])
                         for triple in triples)]
        assert legal == listed_legal, "incomplete legal list"
        # All relevant quads lie inside S union L. Reuse the Python Board and
        # minimal-residual core on this induced point set to audit the C++ R.
        kept = occupied + legal
        board = Board([points[v] for v in kept])
        occ_mask = (1 << len(occupied)) - 1
        calculated_edges = sorted(sorted(kept[i] for i in bits(edge))
                                  for edge in residual_R(board, occ_mask))
        assert calculated_edges == sorted(witness["minimal_residual_edges"])
        vertices = sum(1 << v for v in legal)
        edges = minimal(sum(1 << v for v in edge) for edge in calculated_edges)
        classes = twin_classes(vertices, edges)
        assert sorted(classes) == sorted(witness["twin_classes"])
        reduced_vertices, reduced_edges = compress(vertices, edges)
        reference = grundy_occupied(vertices, edges)
        deleted = grundy_occupied(reduced_vertices, reduced_edges)
        baseline = grundy_residual(vertices, edges, False)
        compressed = grundy_residual(vertices, edges, True)
        assert reference["grundy"] == deleted["grundy"] == baseline["grundy"] \
            == compressed["grundy"]
        audited.append({"n": n, "occupied": occupied, "legal": legal,
                        "twin_classes": classes, "removed_vertices": vertices.bit_count()
                        - reduced_vertices.bit_count(), "grundy": reference["grundy"],
                        "direct_subset_memo_states": reference["memo_states"],
                        "residual_baseline_memo_states": baseline["memo_states"],
                        "residual_compressed_memo_states": compressed["memo_states"],
                        "status": "VERIFIED"})
    return audited


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples", type=Path, default=Path(__file__).resolve().parents[1]
                        / "output/geometry-samples.json")
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parents[1]
                        / "output/verified.json")
    args = parser.parse_args()
    samples = json.loads(args.samples.read_text(encoding="utf-8"))
    assert samples["n11_empty_root_outcome"] == "UNKNOWN"
    result = {"exhaustive_small_clutters": audit_clutters(),
              "geometry_witnesses": audit_geometry(samples),
              "n11_empty_root_outcome": "UNKNOWN"}
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
