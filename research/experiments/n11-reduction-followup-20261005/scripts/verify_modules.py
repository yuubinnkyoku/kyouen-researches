#!/usr/bin/env python3
"""Independent occupied-subset audits of exchangeable-module reductions."""
from __future__ import annotations

import argparse
from itertools import combinations, permutations
import json
from pathlib import Path
import sys
from time import perf_counter
from functools import lru_cache

from module_core import (ROOT, bits, class_kernel, compress, exchangeable_classes,
                         components, grundy)
from module_core import misere_auxiliary
from twin_core import grundy_occupied, grundy_residual  # noqa: E402
from verify_twins import antichains  # noqa: E402

sys.path.insert(0, str(ROOT / "scripts/research"))
from kyouen_core import Board, is_forbidden_quad, square_points  # noqa: E402
from residual_core import residual_R  # noqa: E402


def invariant_orbit_clutters(k: int, w: int, rank: int):
    """ALL invariant clutters, encoded by (X intersection count, W mask).

    Orbit (s,B) is contained in an edge of orbit (t,A) exactly when
    s<=t and B subset A. This is independent of the vertex-pair detector.
    """
    candidates = [(t, a) for t in range(k + 1) for a in range(1 << w)
                  if 2 <= t + a.bit_count() <= rank]

    def comparable(p, q):
        return p[0] <= q[0] and p[1] & q[1] == p[1]

    def walk(remaining, chosen):
        if not remaining:
            yield chosen
            return
        p, rest = remaining[0], remaining[1:]
        yield from walk(rest, chosen)
        rest = [q for q in rest if not comparable(p, q) and not comparable(q, p)]
        yield from walk(rest, chosen + [p])

    for orbit_list in walk(candidates, []):
        edges = []
        for t, a in orbit_list:
            for x_subset in combinations(range(k), t):
                edges.append(sum(1 << v for v in x_subset) | (a << k))
        yield tuple(sorted(edges))


def check_case(vertices, edges, verify_permutations=False):
    smaller, reduced_edges = compress(vertices, edges)
    reference = grundy_occupied(vertices, edges)
    deleted = grundy_occupied(smaller, reduced_edges)
    module = grundy(vertices, edges, "modules")
    split = grundy(vertices, edges, "modules-components")
    fast = grundy(vertices, edges, "fast-modules-components")
    assert reference["grundy"] == deleted["grundy"] == module["grundy"] \
        == split["grundy"] == fast["grundy"], (vertices, edges)
    misere = misere_occupied(vertices, edges)
    assert misere == misere_occupied(smaller, reduced_edges) \
        == misere_auxiliary(vertices, edges, False) \
        == misere_auxiliary(vertices, edges, True), (vertices, edges)
    groups = exchangeable_classes(vertices, edges)
    if verify_permutations:
        edge_set = set(edges)
        for group in groups:
            for image in permutations(group):
                mapping = dict(zip(group, image))
                transformed = {sum(1 << mapping.get(v, v) for v in bits(edge))
                               for edge in edges}
                assert transformed == edge_set
    return {"removed": vertices.bit_count() - smaller.bit_count(),
            "has_capacity_reduction": any(class_kernel(g, edges)["kind"] == "capacity"
                and class_kernel(g, edges)["keep"] < len(g) for g in groups),
            "has_depth_above_one_reduction": any(
                class_kernel(g, edges)["kind"] == "mixed-depth-parity"
                and class_kernel(g, edges)["depth"] > 1
                and class_kernel(g, edges)["keep"] < len(g) for g in groups)}


def misere_occupied(vertices, edges):
    """Independent occupied-subset auxiliary mex, terminal value one."""
    @lru_cache(None)
    def evaluate(occupied):
        values = set()
        for v in bits(vertices & ~occupied):
            child = occupied | (1 << v)
            if not any(child & edge == edge for edge in edges):
                values.add(evaluate(child))
        if not values:
            return 1
        answer = 0
        while answer in values:
            answer += 1
        return answer
    return evaluate(0)


def audit_small():
    cases = []
    for m in range(1, 6):
        counts = {"vertices": m, "all_clutters": 0, "reducible": 0,
                  "capacity_reducible": 0, "higher_depth_reducible": 0}
        for edges in antichains(m):
            result = check_case((1 << m) - 1, edges, True)
            counts["all_clutters"] += 1
            counts["reducible"] += result["removed"] > 0
            counts["capacity_reducible"] += result["has_capacity_reduction"]
            counts["higher_depth_reducible"] += result["has_depth_above_one_reduction"]
        cases.append(counts)
    orbit_cases = []
    for k, w, rank in [(6, 2, 4), (6, 3, 4)]:
        counts = {"class_size": k, "outside_vertices": w, "rank": rank,
                  "all_invariant_clutters": 0, "higher_depth_reducible": 0}
        for edges in invariant_orbit_clutters(k, w, rank):
            result = check_case((1 << (k + w)) - 1, edges)
            counts["all_invariant_clutters"] += 1
            counts["higher_depth_reducible"] += result["has_depth_above_one_reduction"]
        orbit_cases.append(counts)
    # Pair-only true twins fail when a higher edge distinguishes the pair.
    edges = (3, 13)  # {0,1}, {0,2,3}; pair graph alone says 0~1.
    original = grundy_occupied(15, edges)["grundy"]
    malformed = grundy_occupied(14, ())["grundy"]
    assert original != malformed
    assert not any(0 in g and 1 in g for g in exchangeable_classes(15, edges))
    # Same automorphism orbit is weaker than every transposition being an
    # automorphism: cycle C4 has one orbit but no four-point module.
    cycle = (3, 6, 12, 9)
    assert max(map(len, exchangeable_classes(15, cycle))) == 2
    assert grundy_occupied(15, cycle)["grundy"] == 0
    assert grundy_occupied(1, ())["grundy"] == 1
    # A rank-four class genuinely needs all four representatives. Outside
    # a,b,c are fixed. Edges: each X triple + b; each X pair + a,c; b,c.
    sharpness = []
    for k in range(9):
        edges = [sum(1 << v for v in subset) | (1 << (k + 1))
                 for subset in combinations(range(k), 3)]
        edges += [sum(1 << v for v in subset) | (1 << k) | (1 << (k + 2))
                  for subset in combinations(range(k), 2)]
        edges += [(1 << (k + 1)) | (1 << (k + 2))]
        g = grundy_occupied((1 << (k + 3)) - 1, tuple(edges))["grundy"]
        sharpness.append({"class_size": k, "grundy": g})
    assert [case["grundy"] for case in sharpness] == [0, 1, 2, 2, 3, 2, 3, 2, 3]
    return {"all_small_clutters": cases, "complete_invariant_clutters": orbit_cases,
            "pair_only_counterexample": {"edges": [[0, 1], [0, 2, 3]],
                "original_grundy": original, "delete_vertex_zero_grundy": malformed},
            "rank_four_bound_sharpness": sharpness,
            "misere_auxiliary_mex_checked": True,
            "status": "VERIFIED"}


def independent_geometry(witness):
    n = 11
    points = square_points(n)
    occupied = witness["occupied"]
    assert all(not is_forbidden_quad([points[v] for v in q])
               for q in combinations(occupied, 4))
    occupied_set = set(occupied)
    triples = list(combinations(occupied, 3))
    legal = [v for v in range(n * n) if v not in occupied_set
             and all(not is_forbidden_quad([points[p] for p in triple + (v,)])
                     for triple in triples)]
    assert legal == witness["legal"]
    kept = occupied + legal
    board = Board([points[v] for v in kept])
    generated = sorted(sorted(kept[v] for v in bits(edge))
                       for edge in residual_R(board, (1 << len(occupied)) - 1))
    assert generated == sorted(witness["minimal_residual_edges"])
    return {"occupied": occupied, "legal": legal, "minimal_residual_edges": generated,
            "status": "GEOMETRY_VERIFIED"}


def audit_snapshots(samples, legal_limit):
    assert samples["n11_empty_root_outcome"] == "UNKNOWN"
    summary = {"snapshots": len(samples["snapshots"]), "benchmark_legal_limit": legal_limit,
               "reducible_snapshots": 0, "capacity_reducible_snapshots": 0,
               "higher_depth_reducible_snapshots": 0, "benchmark_snapshots": 0,
               "max_initial_removed": 0}
    totals = {mode: {"memo_states": 0, "wall_seconds": 0.0}
              for mode in ["baseline", "twins", "modules", "modules-components",
                           "fast-modules", "fast-modules-components"]}
    benchmark = []
    best = None
    best_ratio = 0
    best_connected = None
    best_connected_ratio = 0
    for index, witness in enumerate(samples["snapshots"]):
        vertices = sum(1 << v for v in witness["legal"])
        edges = tuple(sorted(sum(1 << v for v in edge)
                             for edge in witness["minimal_residual_edges"]))
        groups = exchangeable_classes(vertices, edges)
        capacities = [g for g in groups if class_kernel(g, edges)["kind"] == "capacity"
                      and class_kernel(g, edges)["keep"] < len(g)]
        higher = [g for g in groups if class_kernel(g, edges)["kind"] == "mixed-depth-parity"
                  and class_kernel(g, edges)["depth"] > 1
                  and class_kernel(g, edges)["keep"] < len(g)]
        smaller, _ = compress(vertices, edges)
        removed = vertices.bit_count() - smaller.bit_count()
        summary["reducible_snapshots"] += removed > 0
        summary["capacity_reducible_snapshots"] += bool(capacities)
        summary["higher_depth_reducible_snapshots"] += bool(higher)
        summary["max_initial_removed"] = max(summary["max_initial_removed"], removed)
        if vertices.bit_count() > legal_limit:
            continue
        summary["benchmark_snapshots"] += 1
        row = {"snapshot_index": index, "legal_vertices": vertices.bit_count(),
               "initial_removed": removed, "modes": {}}
        reference = grundy_occupied(vertices, edges)
        assert misere_occupied(vertices, edges) == misere_auxiliary(vertices, edges, True)
        for mode in totals:
            start = perf_counter()
            if mode == "twins":
                result = grundy_residual(vertices, edges, True)
            else:
                result = grundy(vertices, edges, mode)
            elapsed = perf_counter() - start
            assert result["grundy"] == reference["grundy"]
            result["wall_seconds"] = elapsed
            row["modes"][mode] = result
            totals[mode]["memo_states"] += result["memo_states"]
            totals[mode]["wall_seconds"] += elapsed
        benchmark.append(row)
        ratio = row["modes"]["baseline"]["memo_states"] / max(
            1, row["modes"]["modules-components"]["memo_states"])
        if capacities and ratio > best_ratio:
            best, best_ratio = (witness, row, groups), ratio
        if capacities and len(components(vertices, edges)) == 1 \
                and any(edge.bit_count() >= 3 for edge in edges) \
                and ratio > best_connected_ratio:
            best_connected, best_connected_ratio = (witness, row, groups), ratio
    audited = None
    if best is not None:
        witness, row, groups = best
        audited = independent_geometry(witness)
        audited["exchangeable_classes"] = groups
        audited["benchmark"] = row
    audited_connected = None
    if best_connected is not None:
        witness, row, groups = best_connected
        audited_connected = independent_geometry(witness)
        audited_connected["exchangeable_classes"] = groups
        audited_connected["benchmark"] = row
    return {"summary": summary, "totals": totals, "best_capacity_witness": audited,
            "connected_higher_edge_capacity_witness": audited_connected,
            "benchmark": benchmark, "misere_auxiliary_mex_checked": True,
            "status": "VERIFIED"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples", type=Path)
    parser.add_argument("--legal-limit", type=int, default=14)
    parser.add_argument("--skip-small", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = {"n11_empty_root_outcome": "UNKNOWN"}
    if not args.skip_small:
        result["small_clutter_audit"] = audit_small()
    if args.samples:
        result["n11_snapshots"] = audit_snapshots(
            json.loads(args.samples.read_text()), args.legal_limit)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    for key, value in result.items():
        if isinstance(value, dict):
            print(key, json.dumps({k: v for k, v in value.items() if k != "benchmark"},
                                 ensure_ascii=False)[:5000])
        else:
            print(key, value)


if __name__ == "__main__":
    main()
