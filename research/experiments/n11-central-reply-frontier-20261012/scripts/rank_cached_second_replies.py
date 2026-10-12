#!/usr/bin/env python3
"""Find second-move roots helped most by globally reusable exact LOSS-S4 evidence."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import defaultdict
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXPERIMENT = ROOT / "research/experiments/n11-central-reply-frontier-20261012"
OPENINGS = ROOT / "research/experiments/n11-opening-orbits-weak-solve-20261012/output/opening-analysis.json"
ROOT_PROOF = ROOT / "research/experiments/n11-s4-boundary-direct-20261012/output/root-60-27-loss-proof.json"
CENTRAL = EXPERIMENT / "output/central-reply-frontier.json"
BOARD_SOURCE = ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py"


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def key(mask: int) -> tuple[int, int]:
    return mask & ((1 << 64) - 1), mask >> 64


def point_image(mapping: list[int], point: int) -> int:
    return mapping[point].bit_length() - 1


def response_orbits(board, first: int) -> list[dict]:
    stabilizer = [mapping for mapping in board.maps if point_image(mapping, first) == first]
    unseen = set(board.points(board.legal(1 << first)))
    result = []
    while unseen:
        seed = min(unseen)
        members = sorted({point_image(mapping, seed) for mapping in stabilizer})
        if not set(members) <= set(board.points(board.legal(1 << first))):
            raise ValueError("first-move stabilizer moved a legal reply outside the legal set")
        unseen.difference_update(members)
        result.append({"representative": min(members), "members": members, "weight": len(members)})
    return sorted(result, key=lambda row: row["representative"])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=EXPERIMENT / "output/cached-second-reply-ranking.json")
    args = parser.parse_args()
    sys.path.insert(0, str(BOARD_SOURCE.parent))
    from independent import Board

    board = Board(11)
    sys.path.insert(0, str(EXPERIMENT / "scripts"))
    from analyze_central_reply_frontier import audit_saved_raws, load_exact_s5_cache

    cache_path = ROOT / "research/experiments/n11-s4-boundary-direct-20261012/output/current-exact-s5.cache"
    cache = load_exact_s5_cache(board)
    raw_s5, _raw_audit = audit_saved_raws(board)
    raw_key_set = set(raw_s5)
    openings = json.loads(OPENINGS.read_text(encoding="utf-8"))
    central = json.loads(CENTRAL.read_text(encoding="utf-8"))
    root_proof = json.loads(ROOT_PROOF.read_text(encoding="utf-8"))

    standalone_s4_caches = []
    cache_files = list((ROOT / "research/experiments").rglob("*.cache"))
    for path in cache_files:
        with path.open(encoding="utf-8-sig", errors="replace") as stream:
            first = next((line.strip() for line in stream
                          if line.strip() and not line.lstrip().startswith("#")), "")
        if first.startswith("s4verdict,"):
            standalone_s4_caches.append(str(path.relative_to(ROOT)))

    # Any cache-derived S4 LOSS must be a predecessor of a cached S5 child.
    parent_candidates = set()
    for lo, hi in cache:
        parent_candidates.update(board.predecessors(lo | (hi << 64)))
    loss_s4 = set()
    for parent in parent_candidates:
        if parent.bit_count() != 4 or board.canonical(parent) != parent:
            raise ValueError(f"invalid S4 predecessor {parent}")
        children = board.children(parent)
        if children and all(cache.get(key(child), {}).get("verdict") == 2 for child in children):
            loss_s4.add(parent)

    # A known losing S4 contains the two-stone root plus a third/fourth pair.
    # Both orders of those last two safe additions yield the same S4 position.
    coverage: dict[tuple[int, int], set[int]] = defaultdict(set)
    loss_classes: dict[tuple[int, int], set[int]] = defaultdict(set)
    for state in loss_s4:
        # Expand the canonical class before assigning physical first/reply
        # coordinates; the canonical representative need not contain the
        # same numbered cells as a root in its D4 orbit.
        images = {sum(mapping[p] for p in board.points(state)) for mapping in board.maps}
        for image in images:
            points = board.points(image)
            for pair in combinations(points, 2):
                pair_key = tuple(sorted(pair))
                last_two = sorted(set(points) - set(pair))
                for third in last_two:
                    coverage[pair_key].add(third)
                loss_classes[pair_key].add(state)

    proof_loss_s4 = {tuple(row["key"]) for row in root_proof["used_s4_loss_classes"]}
    global_loss_keys = {key(state) for state in loss_s4}
    if global_loss_keys != proof_loss_s4:
        raise ValueError(
            "global exact-cache LOSS-S4 reverse index differs from K0414's independent 32-class witness set"
        )

    unresolved = [row for row in openings["orbits"] if row["status"] == "UNRESOLVED"]
    per_first = []
    all_reply_orbits = []
    for orbit in unresolved:
        first = orbit["representative"]
        replies = response_orbits(board, first)
        if sum(row["weight"] for row in replies) != 120:
            raise ValueError(f"first move {first} has an unexpected number of legal replies")
        rows = []
        for response in replies:
            reply = response["representative"]
            pair = tuple(sorted((first, reply)))
            covered = sorted(coverage.get(pair, set()))
            class_set = loss_classes.get(pair, set())
            candidate = {
                "first_move": first,
                "second_move_representative": reply,
                "second_move_orbit_members_under_first_stabilizer": response["members"],
                "second_move_orbit_weight": response["weight"],
                "two_stone_root": list(pair),
                "known_loss_s4_classes": len(class_set),
                "third_moves_with_known_loss_s4_response": len(covered),
                "third_moves_without_known_loss_s4_response": 119 - len(covered),
                "covered_third_move_ids": covered,
                "s5_cache_hits_below_known_loss_s4_classes": 0,
                "validated_saved_s5_raw_hits_below_known_loss_s4_classes": 0,
            }
            if class_set:
                s5_children = set().union(*(board.children(s4) for s4 in class_set))
                candidate["s5_cache_hits_below_known_loss_s4_classes"] = len(s5_children)
                candidate["validated_saved_s5_raw_hits_below_known_loss_s4_classes"] = sum(
                    key(child) in raw_key_set and raw_s5[key(child)] == cache[key(child)]["verdict"]
                    for child in s5_children
                )
            rows.append(candidate)
            all_reply_orbits.append(candidate)
        rows.sort(key=lambda row: (
            -row["third_moves_with_known_loss_s4_response"],
            -row["known_loss_s4_classes"], row["second_move_representative"],
        ))
        best_noncentral = next(row for row in rows if row["second_move_representative"] != 60)
        per_first.append({
            "first_move": first,
            "initial_orbit": orbit["orbit"],
            "initial_orbit_size": orbit["size"],
            "second_move_reply_orbits": len(replies),
            "central_reply_60": next(row for row in rows if row["second_move_representative"] == 60),
            "best_noncentral_reply": best_noncentral,
            "top_five_replies_by_existing_loss_s4_coverage": rows[:5],
        })

    all_reply_orbits.sort(key=lambda row: (
        -row["third_moves_with_known_loss_s4_response"],
        -row["known_loss_s4_classes"],
        -row["validated_saved_s5_raw_hits_below_known_loss_s4_classes"],
        -row["s5_cache_hits_below_known_loss_s4_classes"],
        row["first_move"], row["second_move_representative"],
    ))
    best_noncentral_global = next(row for row in all_reply_orbits
                                  if row["second_move_representative"] != 60)
    if sum(row["third_moves_with_known_loss_s4_response"] == 119 for row in all_reply_orbits):
        raise ValueError("a full existing-evidence pair LOSS needs the full boundary/response-table audit")

    central_counts = {row["two_stone_root"][0]: row["third_moves_with_known_s4_loss_response"]
                      for row in central["ranked_central_reply_roots"]}
    for first in central_counts:
        row = next(row for row in all_reply_orbits if row["first_move"] == first and row["second_move_representative"] == 60)
        if row["third_moves_with_known_loss_s4_response"] != central_counts[first]:
            raise ValueError(f"global S4 inverse and central-root boundary disagree for {first}")

    result = {
        "schema": "n11-cached-second-reply-loss-s4-ranking-v1",
        "opening_orbit_count": 21,
        "unresolved_opening_orbit_count": 19,
        "current_exact_s5_cache_rows": len(cache),
        "current_exact_s5_cache_sha256": sha(cache_path),
        "independent_geometry_sha256": sha(BOARD_SOURCE),
        "globally_reconstructed_cache_derived_s4_loss_classes": len(loss_s4),
        "global_s4_loss_set_matches_k0414_witness_classes": True,
        "tracked_research_cache_files_inspected": len(cache_files),
        "standalone_s4_exact_cache_files": standalone_s4_caches,
        "method": (
            "Enumerate every canonical S4 predecessor of a current exact S5 cache row; retain an S4 only if all "
            "independently regenerated legal S5 children are exact LOSS. Each retained four-stone set supplies "
            "both possible third/fourth move orders for each of its six two-stone subsets."
        ),
        "scope_limit": (
            "This reverse index covers cache-derived S4 LOSS only. Terminal S4 positions with no legal fifth move "
            "are outside the predecessor index; no candidate is promoted without full pair-boundary validation."
        ),
        "per_first_move": per_first,
        "top_40_second_move_orbits_global": all_reply_orbits[:40],
        "best_noncentral_reply_orbit_global": best_noncentral_global,
        "any_root_proven_loss_from_existing_cache_alone": False,
        "exact_search_launched": False,
        "ranking_limit": "S4 coverage and cache hit counts are finite-boundary metrics, not solver node/runtime guarantees.",
    }
    output = args.output if args.output.is_absolute() else ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "known_loss_s4_classes": len(loss_s4),
        "top_20": [{
            "first": row["first_move"], "second": row["second_move_representative"],
            "weight": row["second_move_orbit_weight"],
            "covered_third_moves": row["third_moves_with_known_loss_s4_response"],
            "loss_s4_classes": row["known_loss_s4_classes"],
        } for row in all_reply_orbits[:20]],
        "central_match": True,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
