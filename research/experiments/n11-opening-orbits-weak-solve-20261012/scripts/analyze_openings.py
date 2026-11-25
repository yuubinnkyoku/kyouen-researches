#!/usr/bin/env python3
"""Enumerate 11x11 first-move D4 orbits and bounded central-reply geometry."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = ROOT / "research/experiments/n11-s4-boundary-direct-20261012"
HELPER = ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts"
ROOT_PROOF = EXP / "output/root-60-27-loss-proof.json"
CACHE = EXP / "output/current-exact-s5.cache"


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def point_from_map(mapping: list[int], point: int) -> int:
    return mapping[point].bit_length() - 1


def d4_orbits(board) -> list[dict]:
    unseen = set(range(board.size))
    result = []
    while unseen:
        seed = min(unseen)
        members = sorted({point_from_map(mapping, seed) for mapping in board.maps})
        unseen.difference_update(members)
        x, y = seed % 11, seed // 11
        dx, dy = abs(x - 5), abs(y - 5)
        label = [min(dx, dy), max(dx, dy)]
        result.append({"orbit": label, "representative": min(members),
                       "members": members, "size": len(members)})
    result.sort(key=lambda row: tuple(row["orbit"]))
    return result


def response_orbit_count(board, first_move: int) -> tuple[int, int]:
    stabilizer = [mapping for mapping in board.maps if point_from_map(mapping, first_move) == first_move]
    unseen = set(range(board.size)) - {first_move}
    count = 0
    while unseen:
        seed = min(unseen)
        orbit = {point_from_map(mapping, seed) for mapping in stabilizer}
        if first_move in orbit:
            raise ValueError("point stabilizer moved a response onto the occupied first move")
        unseen.difference_update(orbit)
        count += 1
    return board.size - 1, count


def response_orbit_representatives(board, first_move: int) -> list[dict]:
    stabilizer = [mapping for mapping in board.maps if point_from_map(mapping, first_move) == first_move]
    unseen = set(range(board.size)) - {first_move}
    result = []
    while unseen:
        seed = min(unseen)
        members = sorted({point_from_map(mapping, seed) for mapping in stabilizer})
        unseen.difference_update(members)
        result.append({"representative": min(members), "members": members, "weight": len(members)})
    return result


def load_cache(path: Path) -> dict[tuple[int, int], dict]:
    rows = {}
    with path.open(encoding="utf-8-sig", newline="") as stream:
        for row in csv.reader(stream):
            if not row or row[0].lstrip().startswith("#"):
                continue
            if len(row) != 6 or row[0] != "s5verdict":
                raise ValueError(f"invalid S5 cache row: {row}")
            lo, hi, stones, verdict, nodes = map(int, row[1:])
            key = (lo, hi)
            if stones != 5 or verdict not in (1, 2) or nodes < 0 or key in rows:
                raise ValueError(f"invalid/duplicate S5 exact cache key: {key}")
            rows[key] = {"verdict": verdict, "nodes": nodes}
    return rows


def central_response_boundary(board, first_move: int, reply: int, cache: dict) -> dict:
    root = (1 << first_move) | (1 << reply)
    if first_move == reply or board.canonical(root) != root:
        raise ValueError("sample two-stone root is invalid or noncanonical")
    third_moves = board.points(board.legal(root))
    s4_coverage: dict[int, set[int]] = {}
    s4_masks: dict[int, int] = {}
    fourth_edges = 0
    for third in third_moves:
        s3 = root | (1 << third)
        for fourth in board.points(board.legal(s3)):
            s4 = board.canonical(s3 | (1 << fourth))
            s4_coverage.setdefault(s4, set()).add(third)
            s4_masks[s4] = s4
            fourth_edges += 1

    s5_children_by_s4 = {s4: board.children(mask) for s4, mask in s4_masks.items()}
    s5_union = set().union(*s5_children_by_s4.values()) if s5_children_by_s4 else set()
    cache_hits = {key for key in s5_union
                  if (key & ((1 << 64) - 1), key >> 64) in cache}
    cache_values = Counter(cache[(key & ((1 << 64) - 1), key >> 64)]["verdict"] for key in cache_hits)
    direct_hits = sum(cache[(key & ((1 << 64) - 1), key >> 64)]["nodes"] > 0 for key in cache_hits)
    return {
        "two_stone_root": [first_move, reply],
        "root_is_canonical": True,
        "legal_third_moves": len(third_moves),
        "fourth_response_edges": fourth_edges,
        "canonical_s4_response_classes": len(s4_masks),
        "s4_classes_per_third_move_min": min(Counter().values(), default=0) if not third_moves else min(
            sum(third in coverage for coverage in s4_coverage.values()) for third in third_moves),
        "s4_classes_per_third_move_max": max(
            sum(third in coverage for coverage in s4_coverage.values()) for third in third_moves),
        "canonical_s5_boundary_edges": sum(len(children) for children in s5_children_by_s4.values()),
        "unique_canonical_s5_children": len(s5_union),
        "current_exact_s5_cache_hits": len(cache_hits),
        "current_exact_s5_cache_hit_verdicts": {
            "WIN": cache_values[1], "LOSS": cache_values[2]},
        "current_exact_s5_cache_hits_with_nonzero_solver_nodes": direct_hits,
        "current_exact_s5_cache_hits_with_zero_nodes": len(cache_hits) - direct_hits,
        "s3_moves_all_have_at_least_one_fourth_reply": len(s4_coverage) > 0 and all(
            any(third in coverage for coverage in s4_coverage.values()) for third in third_moves),
    }


def opening_reply_probe(board, first_move: int, cache: dict, winning_s4_parents: set[int]) -> dict:
    """Bound a solver-trusted winning-opening proof without starting a search.

    After a second-player reply, a first-player third move is a candidate only if
    every legal fourth reply reaches an S4 position with a cached exact S5 WIN
    child. This is the finite boundary obligation for that candidate line.
    """
    representatives = response_orbit_representatives(board, first_move)
    covered_actual_replies = 0
    witnessed_orbits = 0
    total_third_moves = 0
    total_fourth_edges = 0
    total_s4_classes = 0
    total_s4_classes_with_cached_s5_win = 0
    total_min_candidate_s4_classes = 0
    witness_examples = []
    for response_orbit in representatives:
        reply = response_orbit["representative"]
        pair = (1 << first_move) | (1 << reply)
        if not (board.legal(1 << first_move) & (1 << reply)):
            raise ValueError(f"invalid reply representative after first move {first_move}: {reply}")
        by_third: dict[int, set[int]] = {}
        all_s4: set[int] = set()
        fourth_edges = 0
        for third in board.points(board.legal(pair)):
            s3 = pair | (1 << third)
            fourth_moves = board.points(board.legal(s3))
            children = {board.canonical(s3 | (1 << fourth)) for fourth in fourth_moves}
            if not children:
                raise ValueError(f"third move {third} has no legal fourth response")
            by_third[third] = children
            all_s4.update(children)
            fourth_edges += len(fourth_moves)
        good = [third for third, s4s in by_third.items()
                if all(s4 in winning_s4_parents for s4 in s4s)]
        total_third_moves += len(by_third)
        total_fourth_edges += fourth_edges
        total_s4_classes += len(all_s4)
        total_s4_classes_with_cached_s5_win += sum(s4 in winning_s4_parents for s4 in all_s4)
        total_min_candidate_s4_classes += min(map(len, by_third.values()))
        if good:
            witnessed_orbits += 1
            covered_actual_replies += response_orbit["weight"]
            witness_examples.append({"reply_representative": reply,
                                     "reply_orbit_weight": response_orbit["weight"],
                                     "third_move_witnesses": good[:8],
                                     "s4_classes_for_first_witness": len(by_third[good[0]])})
    return {
        "first_move": first_move,
        "second_player_legal_replies": board.size - 1,
        "reply_orbits_under_first_move_stabilizer": len(representatives),
        "reply_orbits_covered_by_existing_exact_s5_win_cache": witnessed_orbits,
        "actual_replies_covered_by_existing_exact_s5_win_cache": covered_actual_replies,
        "third_move_candidates_checked_per_reply_orbit": total_third_moves,
        "fourth_response_edges_checked_per_reply_orbit": total_fourth_edges,
        "unique_canonical_s4_classes_per_reply_orbit_sum": total_s4_classes,
        "s4_classes_with_at_least_one_existing_exact_s5_win_child": total_s4_classes_with_cached_s5_win,
        "minimum_s4_classes_for_a_candidate_third_move_per_reply_orbit_sum": total_min_candidate_s4_classes,
        "cached_win_coverage_is_only_a_solver_trusted_witness_probe": True,
        "witness_examples": witness_examples[:12],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path,
                        default=ROOT / "research/experiments/n11-opening-orbits-weak-solve-20261012/output/opening-analysis.json")
    args = parser.parse_args()
    sys.path.insert(0, str(HELPER))
    from independent import Board
    board = Board(11)

    proof = json.loads(ROOT_PROOF.read_text(encoding="utf-8"))
    if proof["root_outcome"] != "LOSS" or proof["legal_root_moves"] != 119:
        raise ValueError("the reply27 root proof does not assert a complete 119-move LOSS")
    if len(proof["third_move_witnesses"]) != 119 or len({x["root_move"] for x in proof["third_move_witnesses"]}) != 119:
        raise ValueError("root response table is not a one-to-one 119-move cover")

    orbits = d4_orbits(board)
    if len(orbits) != 21 or sum(row["size"] for row in orbits) != 121:
        raise ValueError("11x11 D4 orbit partition must contain 21 orbits covering 121 cells")
    proven_cells = {60, 27, 57, 63, 93}
    for orbit in orbits:
        intersection = proven_cells.intersection(orbit["members"])
        if intersection and intersection != set(orbit["members"]):
            raise ValueError(f"proven first moves do not form a union of complete D4 orbits: {orbit}")
        orbit["status"] = "LOSS_PROVEN" if intersection else "UNRESOLVED"
        orbit["first_move_loss_derivation"] = None
        if orbit["status"] == "LOSS_PROVEN":
            orbit["first_move_loss_derivation"] = (
                "root {60,27} LOSS plus move-order invariance and D4 symmetry"
            )
    if sum(row["status"] == "LOSS_PROVEN" for row in orbits) != 2:
        raise ValueError("expected exactly the center and cardinal-distance-three orbits proven LOSS")

    anchor = (1 << 60) | (1 << 27)
    images = {sum(mapping[p] for p in (60, 27)) for mapping in board.maps}
    if any(board.canonical(mask) != board.canonical(anchor) for mask in images):
        raise ValueError("D4 image of the certified pair differs from its canonical position")

    cache = load_cache(CACHE)
    winning_s5_masks = [lo | (hi << 64) for (lo, hi), row in cache.items() if row["verdict"] == 1]
    winning_s4_parents: set[int] = set()
    for child in winning_s5_masks:
        for point in board.points(child):
            parent = child & ~(1 << point)
            if parent.bit_count() == 4:
                winning_s4_parents.add(board.canonical(parent))

    central_reply_legal_moves = [move for move in range(board.size)
                                 if move != 60 and (board.legal(1 << move) & (1 << 60))]
    if len(central_reply_legal_moves) != 120:
        raise ValueError(f"center 60 is not a legal reply after all 120 noncentral first moves: {len(central_reply_legal_moves)}")
    sample_specs = [
        {"opening_first_move": 60, "opponent_reply": 27, "role": "proved-loss witness"},
        {"opening_first_move": 27, "opponent_reply": 60, "role": "proved-loss witness; central reply"},
        {"opening_first_move": 49, "opponent_reply": 60, "role": "unresolved central-reply probe"},
        {"opening_first_move": 48, "opponent_reply": 60, "role": "unresolved central-reply probe"},
        {"opening_first_move": 25, "opponent_reply": 60, "role": "unresolved central-reply probe"},
        {"opening_first_move": 0, "opponent_reply": 60, "role": "unresolved central-reply probe"},
    ]
    samples = []
    for spec in sample_specs:
        first, reply = spec["opening_first_move"], spec["opponent_reply"]
        move_count, response_orbits = response_orbit_count(board, first)
        central_legal = first != 60 and bool(board.legal(1 << first) & (1 << 60))
        boundary = central_response_boundary(board, first, reply, cache)
        samples.append({
            **spec,
            "second_player_legal_responses": move_count,
            "response_orbits_under_first_move_stabilizer": response_orbits,
            "cell_60_legal_as_reply": central_legal,
            "exact_pair_root_outcome_known_from_current_record": [first, reply] in ([60, 27], [27, 60]),
            "boundary": boundary,
        })

    proof_probe_first_moves = [60, 49, 48, 25, 0]
    opening_reply_probes = [opening_reply_probe(board, first, cache, winning_s4_parents)
                            for first in proof_probe_first_moves]

    output = args.output if args.output.is_absolute() else ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    doc = {
        "schema": "n11-opening-orbits-and-central-reply-boundaries-v1",
        "board_size": "11x11",
        "indexing": "cell = 11*y+x; center=60",
        "root_pair_move_order_invariant": True,
        "d4_orbit_count": len(orbits),
        "cell_count": sum(row["size"] for row in orbits),
        "proven_loss_orbit_count": 2,
        "proven_loss_cell_count": len(proven_cells),
        "unresolved_orbit_count": 19,
        "unresolved_cell_count": 116,
        "orbits": orbits,
        "central_reply_facts": {
            "cell_60_is_legal_after_every_noncentral_first_move": len(central_reply_legal_moves) == 120,
            "cell_60_legal_reply_count_independent_geometry": len(central_reply_legal_moves),
            "known_losing_opening_orbits_using_reply_60": [[0, 3]],
            "unknown_central_reply_is_not_assumed_winning": True,
        },
        "bounded_response_samples": samples,
        "opening_win_certificate_probe": {
            "first_moves_are_representatives_of_distinct_d4_orbits": proof_probe_first_moves,
            "existing_exact_s5_win_rows": len(winning_s5_masks),
            "unique_canonical_s4_positions_with_existing_exact_s5_win_child": len(winning_s4_parents),
            "probes": opening_reply_probes,
            "obligation": "For every second-player reply, a first-player third move must make every legal fourth response reach an S4 with at least one exact S5 WIN child. The probe checks this cached witness condition only; missing coverage is unresolved.",
        },
        "source_hashes": {
            "reply27_root_proof_sha256": sha(ROOT_PROOF),
            "current_exact_s5_cache_sha256": sha(CACHE),
            "independent_geometry_sha256": sha(HELPER / "independent.py"),
        },
        "trust": "D4 partition and response boundaries are finite independent geometry calculations. Only the two named first-move orbits have exact LOSS classification; no new solver search was run.",
    }
    output.write_text(json.dumps(doc, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in doc.items() if k not in ("orbits", "bounded_response_samples")},
                     ensure_ascii=False, indent=2))
    print(json.dumps({"samples": [{"first": row["opening_first_move"],
                                  "reply": row["opponent_reply"],
                                  **row["boundary"]} for row in samples]},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
