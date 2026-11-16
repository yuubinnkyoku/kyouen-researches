#!/usr/bin/env python3
"""Third independent exact reproduction of the shared S6/S7/S8 audit.

This script deliberately uses a direct lifted-coordinate determinant and its own
D4 transform implementation. It emits a deduplicated 7-stone root worklist
with all S6-parent incidences, plus exact first-reply overlap totals.

Run:
    python audit_post_cost75e.py | gzip -n -9 > output/shared-s7-worklist-post-cost75e.json.gz

This is geometry/worklist evidence only, not a game-outcome solver.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, defaultdict

SOURCE_MAIN = "f0c9a005d797a6f496772ff8edb8a19782cf837b"
PARENT_HEX = "00000000000000801202000040000000"
SOURCE_CHILDREN = {
    "cost64a": "00000000000000801282000040000000",
    "cost71d": "00000000000000801202000040000400",
    "cost76c": "00000000010000809002000001000000",
    "cost76d": "00000000040000003800080008000000",
    "cost77e": "00000000040000809002000000004000",
}
EXPECTED = {
    "cost64a": (55, 0, 55, 64),
    "cost71d": (10, 0, 10, 71),
    "cost76c": (88, 4, 98, 76),
    "cost76d": (43, 7, 113, 76),
    "cost77e": (14, 2, 106, 77),
}


def bits(mask: int) -> list[int]:
    return [i for i in range(121) if (mask >> i) & 1]


def transform_index(i: int, g: int) -> int:
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


def transform_mask(mask: int, g: int) -> int:
    out = 0
    for i in bits(mask):
        out |= 1 << transform_index(i, g)
    return out


def align(child: int, parent: int) -> tuple[int, int, int]:
    matches = []
    for deleted in bits(child):
        reduced = child ^ (1 << deleted)
        for g in range(8):
            if transform_mask(reduced, g) == parent:
                matches.append((deleted, g, transform_mask(child, g)))
    if len(matches) != 1:
        raise AssertionError(f"non-unique parent alignment: {matches}")
    return matches[0]


def lifted(i: int) -> tuple[int, int, int]:
    x, y = i % 11, i // 11
    return x * x + y * y, x, y


def circle_det(ids: tuple[int, int, int, int]) -> int:
    a, b, c, d = (lifted(i) for i in ids)
    u = tuple(b[k] - a[k] for k in range(3))
    v = tuple(c[k] - a[k] for k in range(3))
    w = tuple(d[k] - a[k] for k in range(3))
    return (
        u[0] * (v[1] * w[2] - v[2] * w[1])
        - u[1] * (v[0] * w[2] - v[2] * w[0])
        + u[2] * (v[0] * w[1] - v[1] * w[0])
    )


def safe(mask: int) -> bool:
    p = bits(mask)
    return all(circle_det(q) != 0 for q in itertools.combinations(p, 4))


def legal_moves(mask: int) -> list[int]:
    p = bits(mask)
    used = set(p)
    triples = list(itertools.combinations(p, 3))
    return [
        move for move in range(121)
        if move not in used
        and all(circle_det((*triple, move)) != 0 for triple in triples)
    ]


def run() -> dict:
    parent = int(PARENT_HEX, 16)
    stabilizer = [g for g in range(8) if transform_mask(parent, g) == parent]
    assert stabilizer == [0]

    aligned: dict[str, int] = {}
    alignments = {}
    for name, hx in SOURCE_CHILDREN.items():
        source = int(hx, 16)
        assert source.bit_count() == 6 and safe(source)
        deleted, transform, child = align(source, parent)
        exp_deleted, exp_transform, exp_added, exp_moves = EXPECTED[name]
        assert (deleted, transform) == (exp_deleted, exp_transform)
        assert child.bit_count() == 6 and (child & parent) == parent
        added = (child ^ parent).bit_length() - 1
        assert added == exp_added
        moves = legal_moves(child)
        assert len(moves) == exp_moves
        aligned[name] = child
        alignments[name] = {
            "deleted_source_bit": deleted,
            "d4_transform": transform,
            "added_bit_over_parent": added,
            "legal_moves": len(moves),
        }

    root_sources: dict[int, list[dict]] = defaultdict(list)
    root_replies: dict[int, set[int]] = {}
    group_states: dict[str, set[int]] = {}
    per_group = {}
    directed_before = 0

    for name, child in aligned.items():
        first = legal_moves(child)
        after_first = {p: set(legal_moves(child | (1 << p))) for p in first}
        directed = sum(len(replies) for replies in after_first.values())
        directed_before += directed
        states = set()

        for p in first:
            root = child | (1 << p)
            assert safe(root)
            root_sources[root].append({"s6_group": name, "candidate_bit": p})
            replies = after_first[p]
            if root in root_replies:
                assert root_replies[root] == replies
            else:
                root_replies[root] = replies
            for q in replies:
                states.add(root | (1 << q))

        per_group[name] = {
            "legal_first_moves": len(first),
            "directed_first_reply_edges": directed,
            "distinct_raw_8stone_states": len(states),
        }
        group_states[name] = states

    assert sum(EXPECTED[name][3] for name in EXPECTED) == 364
    assert len(root_sources) == 354
    assert all(len(v) in (1, 2) for v in root_sources.values())

    duplicates = []
    for root, sources in root_sources.items():
        if len(sources) == 2:
            duplicates.append({
                "root_hex": f"{root:032x}",
                "sources": sorted(sources, key=lambda x: (x["s6_group"], x["candidate_bit"])),
                "legal_first_replies": len(root_replies[root]),
            })
    duplicates.sort(key=lambda x: (-x["legal_first_replies"], x["root_hex"]))
    assert len(duplicates) == 10

    edges_before = sum(len(root_replies[r]) * len(src) for r, src in root_sources.items())
    edges_after = sum(len(root_replies[r]) for r in root_sources)
    union = set().union(*group_states.values())
    frequency = Counter(sum(state in group for group in group_states.values()) for state in union)
    pairwise = {
        f"{a}__{b}": len(group_states[a] & group_states[b])
        for a, b in itertools.combinations(group_states, 2)
    }
    root_child_multiplicity = Counter()
    for root, replies in root_replies.items():
        for q in replies:
            root_child_multiplicity[root | (1 << q)] += 1
    root_child_frequency = Counter(root_child_multiplicity.values())
    d4_s7_orbits = {min(transform_mask(root, g) for g in range(8)) for root in root_sources}
    d4_s8_orbits = {min(transform_mask(state, g) for g in range(8)) for state in union}
    four_point_checks = 0
    for state in union:
        ps = bits(state)
        for quad in itertools.combinations(ps, 4):
            four_point_checks += 1
            assert circle_det(quad) != 0

    assert edges_before == directed_before == 22174
    assert edges_after == 21526
    assert edges_before - edges_after == 648
    assert len(union) == 10449
    assert edges_after - len(union) == 11077
    assert frequency == Counter({1: 9821, 2: 618, 3: 10})
    assert sum(pairwise.values()) == 648
    assert root_child_frequency == Counter({2: 9821, 3: 628})
    assert len(d4_s7_orbits) == 354
    assert len(d4_s8_orbits) == 10449
    assert four_point_checks == 731430

    worklist = []
    for root in sorted(root_sources):
        worklist.append({
            "root_hex": f"{root:032x}",
            "sources": sorted(root_sources[root], key=lambda x: (x["s6_group"], x["candidate_bit"])),
            "legal_first_replies": len(root_replies[root]),
        })

    return {
        "schema": "kyouen.n11.shared_s7_worklist.v2",
        "source_main": SOURCE_MAIN,
        "parent_s5_hex": PARENT_HEX,
        "current_open_s6_rows": 5,
        "current_remaining_s7_edge_cost": 364,
        "parent_d4_stabilizer": stabilizer,
        "independent_reproduction": "PASS",
        "alignments": alignments,
        "per_group": per_group,
        "totals": {
            "candidate_s7_occurrences": sum(EXPECTED[name][3] for name in EXPECTED),
            "unique_raw_s7_roots": len(root_sources),
            "duplicate_s7_roots": len(duplicates),
            "directed_first_reply_edges_before_root_dedup": edges_before,
            "directed_first_reply_edges_after_root_dedup": edges_after,
            "first_reply_edges_removed_by_root_dedup": edges_before - edges_after,
            "distinct_raw_8stone_states": len(union),
            "potential_duplicate_first_reply_visits_after_root_dedup": edges_after - len(union),
            "potential_duplicate_first_reply_visits_before_root_dedup": edges_before - len(union),
            "states_reached_from_exactly_two_s6_groups": frequency[2],
            "states_reached_from_exactly_three_s6_groups": frequency[3],
            "states_reached_from_exactly_two_unique_s7_roots": root_child_frequency[2],
            "states_reached_from_exactly_three_unique_s7_roots": root_child_frequency[3],
            "unique_d4_s7_orbits": len(d4_s7_orbits),
            "unique_d4_s8_orbits": len(d4_s8_orbits),
            "explicit_four_point_checks_on_distinct_s8_states": four_point_checks,
            "safe_unordered_move_pairs": sum(v["directed_first_reply_edges"] for v in per_group.values()) // 2,
        },
        "pairwise_s6_group_intersections": pairwise,
        "duplicate_s7_roots_ranked_by_reply_count": duplicates,
        "unique_s7_root_worklist": worklist,
        "interpretation": {
            "deduplication": "The remaining S6-child occurrences are deduplicated into distinct raw S7 roots; each duplicate root is listed once with all parent incidences.",
            "reuse_upper_bound": "potential_duplicate_first_reply_visits_after_root_dedup is an upper bound from full legal first-reply enumeration, not a measured TT hit or node reduction.",
            "game_outcomes": "No WIN/LOSS verdict is inferred. REFUTED-D10 and incomplete search are not LOSS proofs.",
        },
    }


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, sort_keys=True, indent=2))
