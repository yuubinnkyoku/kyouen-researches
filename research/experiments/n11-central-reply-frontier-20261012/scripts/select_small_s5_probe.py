#!/usr/bin/env python3
"""Measure near-closed S4 classes before deciding whether a new S5 solve helps."""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXPERIMENT = ROOT / "research/experiments/n11-central-reply-frontier-20261012"
CENTRAL = EXPERIMENT / "output/central-reply-frontier.json"
OPENINGS = ROOT / "research/experiments/n11-opening-orbits-weak-solve-20261012/output/opening-analysis.json"
BOARD_SOURCE = ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=EXPERIMENT / "output/small-s5-probe-readiness.json")
    args = parser.parse_args()
    sys.path.insert(0, str(BOARD_SOURCE.parent))
    sys.path.insert(0, str(EXPERIMENT / "scripts"))
    from independent import Board
    from analyze_central_reply_frontier import (
        audit_saved_raws, load_exact_s5_cache, s4_status, sha,
    )

    board = Board(11)
    cache = load_exact_s5_cache(board)
    raw_s5, raw_audit = audit_saved_raws(board)
    central = json.loads(CENTRAL.read_text(encoding="utf-8"))
    openings = json.loads(OPENINGS.read_text(encoding="utf-8"))
    unresolved = {row["representative"] for row in openings["orbits"] if row["status"] == "UNRESOLVED"}
    orbit_representative = {point: row["representative"] for row in openings["orbits"] for point in row["members"]}
    central_rows = {
        (row["two_stone_root"][0], move["third_move"]): move["status"]
        for row in central["ranked_central_reply_roots"]
        for move in row["third_move_table"]
    }

    # Focus the pre-search readiness check on the top three central-response
    # roots; each S4 can also be shared with other unresolved central roots.
    top_roots = [row["two_stone_root"][0] for row in central["ranked_central_reply_roots"][:3]]
    source_roots: dict[int, set[tuple[int, int]]] = defaultdict(set)
    candidate_masks: set[int] = set()
    for first in top_roots:
        pair = (1 << first) | (1 << 60)
        for third in board.points(board.legal(pair)):
            s3 = pair | (1 << third)
            for fourth in board.points(board.legal(s3)):
                s4 = board.canonical(s3 | (1 << fourth))
                source_roots[s4].add((first, third))
                candidate_masks.add(s4)

    missing_histogram = Counter()
    s4_status_counts = Counter()
    candidates = []
    for s4 in candidate_masks:
        status, children = s4_status(board, s4, cache)
        s4_status_counts[status] += 1
        if status != "UNKNOWN":
            continue
        missing = [child for child in children if (child & ((1 << 64) - 1), child >> 64) not in cache]
        missing_histogram[len(missing)] += 1
        if not missing or any(cache[(child & ((1 << 64) - 1), child >> 64)]["verdict"] == 1
                            for child in children if (child & ((1 << 64) - 1), child >> 64) in cache):
            continue
        effects = set()
        points = board.points(s4)
        if 60 not in points:
            raise ValueError("central root S4 boundary lost the center stone")
        for first_cell in points:
            if first_cell == 60:
                continue
            rep = orbit_representative[first_cell]
            if rep not in unresolved:
                continue
            for mapping in board.maps:
                if (mapping[first_cell].bit_length() - 1) != rep:
                    continue
                image = sorted(mapping[p].bit_length() - 1 for p in points)
                third_cells = set(image) - {60, rep}
                for third in third_cells:
                    if central_rows.get((rep, third)) == "UNRESOLVED":
                        effects.add((rep, third))
        missing_rows = []
        for child in missing:
            lo = child & ((1 << 64) - 1)
            hi = child >> 64
            key = (lo, hi)
            legal = board.legal(child).bit_count()
            missing_rows.append({
                "key": list(key), "legal_moves": legal,
                "validated_saved_raw_present": key in raw_s5,
                "cache_entry_present": key in cache,
            })
        candidates.append({
            "s4_key": [s4 & ((1 << 64) - 1), s4 >> 64],
            "s4_s5_child_count": len(children),
            "s5_children_already_exact_loss": len(children) - len(missing),
            "missing_s5_children": missing_rows,
            "missing_s5_child_count": len(missing),
            "central_roots_with_this_boundary_in_top_three": sorted(first for first, _ in source_roots[s4]),
            "new_unresolved_root_third_pairs_if_s4_becomes_loss": [list(pair) for pair in sorted(effects)],
            "new_unresolved_root_third_pair_count": len(effects),
            "smallest_missing_s5_legal_count": min(row["legal_moves"] for row in missing_rows),
            "cost_limit": "S5 legal-move count is a prioritization feature, not a solver node/runtime guarantee.",
        })
    candidates.sort(key=lambda row: (
        -row["new_unresolved_root_third_pair_count"], row["missing_s5_child_count"],
        row["smallest_missing_s5_legal_count"], row["s4_key"],
    ))
    result = {
        "schema": "n11-central-s5-probe-readiness-v1",
        "top_central_roots_inspected": top_roots,
        "unique_s4_classes_reconstructed": len(candidate_masks),
        "s4_status_counts": dict(sorted(s4_status_counts.items())),
        "unknown_s4_missing_s5_child_count_histogram": {
            str(count): amount for count, amount in sorted(missing_histogram.items())
        },
        "unknown_s4_with_one_missing_s5_child": missing_histogram[1],
        "unknown_s4_with_at_most_three_missing_s5_children": sum(
            amount for count, amount in missing_histogram.items() if 1 <= count <= 3
        ),
        "top_30_candidate_s4_completions": candidates[:30],
        "raw_audit": {
            "unique_files_sha_verified": raw_audit["unique_raw_file_count"],
            "validated_exact_s5_raw_keys": len(raw_s5),
            "untracked_local_raw_references": raw_audit["untracked_local_raw_references"],
        },
        "source_hashes": {
            "central_reply_frontier_sha256": sha(CENTRAL),
            "opening_analysis_sha256": sha(OPENINGS),
            "current_exact_s5_cache_sha256": sha(ROOT / "research/experiments/n11-s4-boundary-direct-20261012/output/current-exact-s5.cache"),
            "independent_geometry_sha256": sha(BOARD_SOURCE),
        },
        "exact_search_launched": False,
        "decision_rule": (
            "Only launch a small exact S5 probe when one or a few missing exact children can close a previously "
            "uncovered S4 response shared by multiple unresolved roots. Otherwise retain UNKNOWN and defer search."
        ),
    }
    output = args.output if args.output.is_absolute() else ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "top_roots": top_roots,
        "s4_status_counts": result["s4_status_counts"],
        "one_missing_child": result["unknown_s4_with_one_missing_s5_child"],
        "at_most_three_missing": result["unknown_s4_with_at_most_three_missing_s5_children"],
        "top_candidates": [{
            "s4": row["s4_key"], "missing": row["missing_s5_child_count"],
            "unresolved_effects": row["new_unresolved_root_third_pair_count"],
            "min_s5_legal": row["smallest_missing_s5_legal_count"],
        } for row in candidates[:10]],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
