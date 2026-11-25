#!/usr/bin/env python3
"""Independent exact audit of S7/S8 overlap under one n11 class-2 S5 parent.

Run with:
    python audit.py > output/audit.json

Standard library only. The audit is geometric/bookkeeping evidence, not a game
solver. It cross-checks a lifted 3x3 determinant against a separate full 4x4
Bareiss determinant, and uses separate D4 coordinate implementations.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter

S5_HEX = "00000000000000801202000040000000"
S6_HEXES = {
    "cost64a": "00000000000000801282000040000000",
    "cost71d": "00000000000000801202000040000400",
    "cost75e": "00000000040000809002000000000002",
    "cost76c": "00000000010000809002000001000000",
    "cost76d": "00000000040000003800080008000000",
    "cost77e": "00000000040000809002000000004000",
}
EXPECTED_COSTS = {
    "cost64a": 64,
    "cost71d": 71,
    "cost75e": 75,
    "cost76c": 76,
    "cost76d": 76,
    "cost77e": 77,
}
MAIN_HEAD = "1dde798765b4b63c9e225cfd7599c68322b4c595"
RUNNER_PATH = (
    "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/"
    "scripts/class4_child1_runner_v16.ts"
)
RUNNER_BLOB_SHA1 = "0a4a86f6828dc010c89ff17596054336a6b6091f"


def occupied(mask: int) -> list[int]:
    return [i for i in range(121) if (mask >> i) & 1]


def lifted_row(i: int) -> tuple[int, int, int]:
    x, y = i % 11, i // 11
    return x * x + y * y, x, y


def det_lifted(ids: tuple[int, int, int, int]) -> int:
    """3x3 determinant after subtracting the first lifted row."""
    a, b, c, d = (lifted_row(i) for i in ids)
    u = tuple(b[j] - a[j] for j in range(3))
    v = tuple(c[j] - a[j] for j in range(3))
    w = tuple(d[j] - a[j] for j in range(3))
    return (
        u[0] * (v[1] * w[2] - v[2] * w[1])
        - u[1] * (v[0] * w[2] - v[2] * w[0])
        + u[2] * (v[0] * w[1] - v[1] * w[0])
    )


def bareiss_det(matrix: list[list[int]]) -> int:
    """Fraction-free exact determinant, with row pivoting."""
    a = [list(map(int, row)) for row in matrix]
    n = len(a)
    sign = 1
    previous_pivot = 1
    for k in range(n - 1):
        if a[k][k] == 0:
            pivot_row = next((r for r in range(k + 1, n) if a[r][k] != 0), None)
            if pivot_row is None:
                return 0
            a[k], a[pivot_row] = a[pivot_row], a[k]
            sign = -sign
        pivot = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = a[i][j] * pivot - a[i][k] * a[k][j]
                assert numerator % previous_pivot == 0
                a[i][j] = numerator // previous_pivot
        for i in range(k + 1, n):
            a[i][k] = 0
        previous_pivot = pivot
    return sign * a[n - 1][n - 1]


def det_bareiss(ids: tuple[int, int, int, int]) -> int:
    rows = []
    for i in ids:
        x, y = i % 11, i // 11
        rows.append([x * x + y * y, x, y, 1])
    return bareiss_det(rows)


def is_safe(mask: int, determinant) -> bool:
    ps = occupied(mask)
    return all(determinant(q) != 0 for q in itertools.combinations(ps, 4))


def legal_moves(mask: int, determinant) -> list[int]:
    ps = occupied(mask)
    used = set(ps)
    out = []
    for move in range(121):
        if move in used:
            continue
        if all(determinant((*triple, move)) != 0
               for triple in itertools.combinations(ps, 3)):
            out.append(move)
    return out


# D4 implementation A: reflect first, then rotate.
def transform_index_lifted(i: int, g: int) -> int:
    x, y = i % 11, i // 11
    if g >= 4:
        x = 10 - x
    r = g % 4
    if r == 0:
        X, Y = x, y
    elif r == 1:
        X, Y = 10 - y, x
    elif r == 2:
        X, Y = 10 - x, 10 - y
    else:
        X, Y = y, 10 - x
    return 11 * Y + X


def transform_mask_lifted(mask: int, g: int) -> int:
    result = 0
    for i in occupied(mask):
        result |= 1 << transform_index_lifted(i, g)
    return result


# D4 implementation B: use (rotation, reflection) parameters directly.
def transform_mask_bareiss(mask: int, g: int) -> int:
    rotation, reflect = g % 4, g // 4
    result = 0
    for i in occupied(mask):
        x, y = i % 11, i // 11
        if reflect:
            x = 10 - x
        if rotation == 0:
            u, v = x, y
        elif rotation == 1:
            u, v = 10 - y, x
        elif rotation == 2:
            u, v = 10 - x, 10 - y
        else:
            u, v = y, 10 - x
        result |= 1 << (11 * v + u)
    return result


def align_to_parent(child: int, parent: int, transform_mask) -> tuple[int, int, int]:
    matches = []
    for deleted in occupied(child):
        candidate_parent = child ^ (1 << deleted)
        for g in range(8):
            if transform_mask(candidate_parent, g) == parent:
                matches.append((deleted, g, transform_mask(child, g)))
    if len(matches) != 1:
        raise AssertionError(f"expected one parent alignment, got {matches}")
    return matches[0]


def run_audit(method: str, determinant, transform_mask) -> dict:
    parent = int(S5_HEX, 16)
    stabilizer = [g for g in range(8) if transform_mask(parent, g) == parent]
    assert stabilizer == [0]

    aligned: dict[str, int] = {}
    alignments = {}
    for name, hx in S6_HEXES.items():
        child = int(hx, 16)
        assert child.bit_count() == 6 and is_safe(child, determinant)
        deleted, transform, aligned_child = align_to_parent(child, parent, transform_mask)
        assert (aligned_child & parent) == parent and aligned_child.bit_count() == 6
        moves = legal_moves(aligned_child, determinant)
        assert len(moves) == EXPECTED_COSTS[name], (name, len(moves))
        aligned[name] = aligned_child
        alignments[name] = {
            "deleted_bit_in_source": deleted,
            "d4_transform": transform,
            "added_bit_over_common_s5": (aligned_child ^ parent).bit_length() - 1,
            "legal_moves": len(moves),
        }

    # Candidate roots and first replies are collected during the per-group pass,
    # so each of the 439 candidate roots is enumerated only once.
    root_occurrences: dict[int, list[dict]] = {}
    root_replies: dict[int, set[int]] = {}
    per_group = {}
    group_states = {}
    total_four_checks = 0
    safe_pair_checks = 0
    directed_edges_before_dedup = 0
    for name, child in aligned.items():
        first_moves = legal_moves(child, determinant)
        after_first = {p: set(legal_moves(child | (1 << p), determinant)) for p in first_moves}
        directed_edges = sum(len(v) for v in after_first.values())
        directed_edges_before_dedup += directed_edges
        safe_pairs = []
        states = set()
        for p in first_moves:
            root = child | (1 << p)
            root_occurrences.setdefault(root, []).append({"s6_group": name, "candidate_bit": p})
            replies = after_first[p]
            if root in root_replies:
                assert root_replies[root] == replies
            else:
                root_replies[root] = replies
        for p, q in itertools.combinations(first_moves, 2):
            state = child | (1 << p) | (1 << q)
            assert state.bit_count() == 8
            state_safe = True
            for four in itertools.combinations(occupied(state), 4):
                total_four_checks += 1
                if determinant(four) == 0:
                    state_safe = False
                    break
            if state_safe:
                assert q in after_first[p] and p in after_first[q]
                safe_pairs.append([p, q])
                states.add(state)
                safe_pair_checks += 70
        assert len(states) == len(safe_pairs)
        assert directed_edges == 2 * len(safe_pairs)
        assert all((state & parent) == parent for state in states)
        per_group[name] = {
            "legal_first_moves": len(first_moves),
            "all_unordered_second_move_pairs": len(first_moves) * (len(first_moves) - 1) // 2,
            "safe_unordered_pairs": len(safe_pairs),
            "directed_first_reply_edges_reenumerated": directed_edges,
            "distinct_raw_8stone_states": len(states),
        }
        group_states[name] = states

    assert sum(EXPECTED_COSTS.values()) == 439
    assert len(root_occurrences) == 424
    duplicate_roots = []
    for root, incidences in sorted(root_occurrences.items()):
        assert len(incidences) in (1, 2)
        if len(incidences) == 2:
            duplicate_roots.append({
                "root_hex": f"{root:032x}",
                "occurrences": incidences,
                "legal_first_replies": len(root_replies[root]),
            })
    assert len(duplicate_roots) == 15

    edges_before_dedup = sum(len(root_replies[root]) * len(incidences)
                             for root, incidences in root_occurrences.items())
    edges_after_dedup = sum(len(replies) for replies in root_replies.values())
    removed_edges = edges_before_dedup - edges_after_dedup
    assert edges_before_dedup == directed_edges_before_dedup

    unique_root_child_multiplicity = Counter()
    for root, replies in root_replies.items():
        for q in replies:
            unique_root_child_multiplicity[root | (1 << q)] += 1

    union = set().union(*group_states.values())
    group_frequency = Counter(sum(state in group for group in group_states.values()) for state in union)
    pairwise = {
        f"{a}__{b}": len(group_states[a] & group_states[b])
        for a, b in itertools.combinations(group_states, 2)
    }
    unique_root_duplicate_visits = edges_after_dedup - len(union)
    duplicate_visits_before_dedup = edges_before_dedup - len(union)
    unique_root_frequency = Counter(unique_root_child_multiplicity.values())
    d4_s7_orbits = {min(transform_mask(root, g) for g in range(8)) for root in root_occurrences}
    d4_s8_orbits = {min(transform_mask(state, g) for g in range(8)) for state in union}

    totals = {
        "candidate_s7_root_occurrences": sum(EXPECTED_COSTS.values()),
        "unique_raw_s7_roots": len(root_occurrences),
        "duplicate_raw_s7_root_masks": len(duplicate_roots),
        "unique_d4_s7_root_orbits": len(d4_s7_orbits),
        "safe_unordered_move_pairs": sum(v["safe_unordered_pairs"] for v in per_group.values()),
        "directed_first_reply_edges_before_root_dedup": edges_before_dedup,
        "directed_first_reply_edges_after_root_dedup": edges_after_dedup,
        "first_reply_edges_removed_by_root_dedup": removed_edges,
        "distinct_raw_8stone_states": len(union),
        "distinct_d4_8stone_orbits": len(d4_s8_orbits),
        "distinct_states_reached_from_multiple_s6_groups": sum(v for k, v in group_frequency.items() if k >= 2),
        "potential_duplicate_first_reply_visits_before_root_dedup": duplicate_visits_before_dedup,
        "potential_duplicate_first_reply_fraction_before_root_dedup": duplicate_visits_before_dedup / edges_before_dedup,
        "potential_duplicate_first_reply_visits_after_root_dedup": unique_root_duplicate_visits,
        "potential_duplicate_first_reply_fraction_after_root_dedup": unique_root_duplicate_visits / edges_after_dedup,
        "states_reached_from_exactly_two_s6_groups": group_frequency.get(2, 0),
        "states_reached_from_exactly_three_s6_groups": group_frequency.get(3, 0),
        "explicit_four_point_checks_all_candidate_pairs_early_exit": total_four_checks,
        "explicit_four_point_checks_safe_pair_visits": safe_pair_checks,
        "explicit_four_point_checks_distinct_safe_states": len(union) * 70,
    }
    assert totals["candidate_s7_root_occurrences"] == 439
    assert totals["unique_raw_s7_roots"] == 424
    assert totals["duplicate_raw_s7_root_masks"] == 15
    assert totals["directed_first_reply_edges_before_root_dedup"] == 26812
    assert totals["directed_first_reply_edges_after_root_dedup"] == 25834
    assert totals["first_reply_edges_removed_by_root_dedup"] == 978
    assert totals["distinct_raw_8stone_states"] == 12448
    assert totals["potential_duplicate_first_reply_visits_before_root_dedup"] == 14364
    assert totals["potential_duplicate_first_reply_visits_after_root_dedup"] == 13386
    assert totals["distinct_states_reached_from_multiple_s6_groups"] == 938
    assert totals["explicit_four_point_checks_safe_pair_visits"] == 938420
    assert totals["explicit_four_point_checks_distinct_safe_states"] == 871360
    assert totals["explicit_four_point_checks_all_candidate_pairs_early_exit"] >= 871360
    assert len(d4_s7_orbits) == 424
    assert len(d4_s8_orbits) == 12448
    assert group_frequency == Counter({1: 11510, 2: 918, 3: 20})
    assert unique_root_frequency == Counter({2: 11510, 3: 938})

    return {
        "method": method,
        "parent_stabilizer": stabilizer,
        "alignments": alignments,
        "per_group": per_group,
        "totals": totals,
        "pairwise_raw_intersections": pairwise,
        "duplicate_s7_roots": duplicate_roots,
        "s6_group_multiplicity_histogram": {str(k): v for k, v in sorted(group_frequency.items())},
        "candidate_root_visit_multiplicity_histogram_before_root_dedup": {
            str(2 * k): v for k, v in sorted(group_frequency.items())
        },
        "unique_s7_root_visit_multiplicity_histogram_after_root_dedup": {
            str(k): v for k, v in sorted(unique_root_frequency.items())
        },
    }


def compare(a: dict, b: dict) -> None:
    for key in (
        "parent_stabilizer", "alignments", "per_group", "totals",
        "pairwise_raw_intersections", "duplicate_s7_roots",
        "s6_group_multiplicity_histogram",
        "candidate_root_visit_multiplicity_histogram_before_root_dedup",
        "unique_s7_root_visit_multiplicity_histogram_after_root_dedup",
    ):
        assert a[key] == b[key], key


def main() -> None:
    lifted = run_audit("lifted 3x3 determinant", det_lifted, transform_mask_lifted)
    bareiss = run_audit("full 4x4 Bareiss determinant", det_bareiss, transform_mask_bareiss)
    compare(lifted, bareiss)
    result = {
        "schema": "n11-class2-shared-s6-overlap-independent-audit-v1",
        "agreement": "PASS",
        "baseline": {
            "main_head": MAIN_HEAD,
            "canonical_class2_head": "1405/6443/509457/4713/373180",
            "s5_hex": S5_HEX,
            "runner_path": RUNNER_PATH,
            "runner_blob_sha1": RUNNER_BLOB_SHA1,
            "runner_memo_entries": 1 << 18,
            "runner_memo_probe_limit": 64,
            "runner_forbidden_triple_entries": 1 << 17,
            "runner_forbidden_triple_probe_limit": 48,
            "runner_cache_lifetime": "freshEngine() per candidate; no cross-candidate memo/forbidden-triple cache reuse",
            "runner_memo_key": "raw four-word occupancy; no D4 canonicalization",
        },
        "methods": [lifted["method"], bareiss["method"]],
        "independent_verification": {
            "method": bareiss["method"],
            "agreement": "PASS",
            "compared": [
                "all six D4 alignments and legal-move counts",
                "all per-group safe-pair and directed-edge counts",
                "all 15 pairwise raw intersections",
                "all 15 duplicate S7 root masks and source incidences",
                "all multiplicity histograms and aggregate totals",
            ],
        },
        "audit": lifted,
        "interpretation": (
            "15 duplicate raw S7 roots can be removed before search. After that, "
            "13,386 first-reply visits are combinatorially redundant across the 424 "
            "unique roots if every legal reply is reached. This is only a structural "
            "upper bound, not measured TT hits or node savings. Early cutoffs, table "
            "saturation and search order can reduce actual reuse. No game verdict is inferred."
        ),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
