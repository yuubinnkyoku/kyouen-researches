#!/usr/bin/env python3
"""Build the S3/S4/S5 proof dependency graph used by the joint S5 planner.

For every candidate two-stone root the script enumerates the 119 legal third
moves, regenerates the canonical S4 response classes with the independent
integer-geometry Board, and records for each S4 class

* its exact-cache derived status (LOSS / WIN / UNKNOWN),
* the unknown exact-S5 children that would have to become LOSS.

S5 children that already carry an exact cache verdict never enter the cost
universe, and any S4 with a cache WIN child is dropped from the LOSS option
list. Nothing here asserts a future verdict: the graph only states which
unknown S5 verdicts a LOSS proof would consume.
"""
from __future__ import annotations

import argparse
import gzip
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXPERIMENT = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012"
OPENINGS = ROOT / "research/experiments/n11-opening-orbits-weak-solve-20261012/output/opening-analysis.json"
RANKING = ROOT / "research/experiments/n11-central-reply-frontier-20261012/output/cached-second-reply-ranking.json"
CACHE = ROOT / "research/experiments/n11-s4-boundary-direct-20261012/output/current-exact-s5.cache"
BOARD_SOURCE = ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py"
FRONTIER = ROOT / "research/experiments/n11-central-reply-frontier-20261012/output/central-reply-frontier.json"

sys.path.insert(0, str(BOARD_SOURCE.parent))
sys.path.insert(0, str(ROOT / "research/experiments/n11-central-reply-frontier-20261012/scripts"))
from independent import Board  # noqa: E402
from analyze_central_reply_frontier import load_exact_s5_cache, sha  # noqa: E402

STATUS_LOSS = 0
STATUS_UNKNOWN = 1


def key_of(mask: int) -> tuple[int, int]:
    return mask & ((1 << 64) - 1), mask >> 64


def selected_roots(extra_replies: int) -> list[dict]:
    openings = json.loads(OPENINGS.read_text(encoding="utf-8"))
    unresolved = [row for row in openings["orbits"] if row["status"] == "UNRESOLVED"]
    ranking = json.loads(RANKING.read_text(encoding="utf-8"))
    by_first = {row["first_move"]: row for row in ranking["per_first_move"]}
    roots = [{"first": 27, "reply": 60, "role": "known-loss-baseline"}]
    for row in unresolved:
        first = row["representative"]
        entry = by_first[first]
        ordered: list[int] = []
        for candidate in entry["top_five_replies_by_existing_loss_s4_coverage"]:
            reply = candidate["second_move_representative"]
            if reply != 60 and reply not in ordered:
                ordered.append(reply)
        for reply in [60, *ordered[:extra_replies]]:
            roots.append({"first": first, "reply": reply,
                          "role": "central" if reply == 60 else "alternative"})
    return roots


def canonical_pair(board: Board, first: int, reply: int) -> tuple[int, int, int]:
    """Return the canonical two-stone mask plus its (first, reply) point labels."""
    pair = (1 << first) | (1 << reply)
    canonical = board.canonical(pair)
    if canonical == pair:
        return canonical, first, reply
    for mapping in board.maps:
        image = sum(mapping[point] for point in (first, reply))
        if image == canonical:
            a = mapping[first].bit_length() - 1
            b = mapping[reply].bit_length() - 1
            return canonical, a, b
    raise ValueError("D4 image of pair root not found")


def build_root(board: Board, root: dict, cache, s5_index: dict[int, int],
               s5_masks: list[int], s4_index: dict[int, int], s4_masks: list[int],
               s4_status: list[int], s4_cost: list[list[int]]) -> dict:
    pair = (1 << root["first"]) | (1 << root["reply"])
    if board.canonical(pair) != pair:
        raise ValueError(f"non-canonical pair root {root['first']},{root['reply']}")
    thirds = board.points(board.legal(pair))
    if len(thirds) != 119:
        raise ValueError(f"expected 119 third moves at {root['first']},{root['reply']}")

    third_rows = []
    status_counter = Counter()
    for third in thirds:
        s3 = pair | (1 << third)
        classes = {board.canonical(s3 | (1 << fourth))
                   for fourth in board.points(board.legal(s3))}
        options = []
        for mask in sorted(classes):
            index = s4_index.get(mask)
            if index is None:
                children = board.children(mask)
                if not children:
                    status, cost = STATUS_LOSS, []
                else:
                    verdicts = [cache.get(key_of(child), {}).get("verdict", 0)
                                for child in children]
                    if 1 in verdicts:
                        status, cost = -1, []
                    elif all(value == 2 for value in verdicts):
                        status, cost = STATUS_LOSS, []
                    else:
                        status = STATUS_UNKNOWN
                        cost = []
                        for child in children:
                            if key_of(child) in cache:
                                continue
                            s5_key = s5_index.get(child)
                            if s5_key is None:
                                s5_key = len(s5_masks)
                                s5_index[child] = s5_key
                                s5_masks.append(child)
                            cost.append(s5_key)
                index = len(s4_masks)
                s4_index[mask] = index
                s4_masks.append(mask)
                s4_status.append(status)
                s4_cost.append(sorted(cost))
            status_counter[s4_status[index]] += 1
            if s4_status[index] != -1:
                options.append(index)
        if not options:
            raise ValueError(f"third {third} of {root['first']},{root['reply']} has no LOSS-capable S4")
        third_rows.append({"third": third, "options": options})

    return {
        "origin_first": root["origin_first"],
        "origin_reply": root["origin_reply"],
        "canonical_first": root["first"],
        "canonical_reply": root["reply"],
        "role": root["role"],
        "pair_mask": [pair & ((1 << 64) - 1), pair >> 64],
        "thirds": third_rows,
        "reachable_s4_classes": len({index for row in third_rows for index in row["options"]}),
        "s4_option_slots": status_counter[STATUS_LOSS] + status_counter[STATUS_UNKNOWN],
        "thirds_with_free_loss_s4": sum(
            1 for row in third_rows
            if any(s4_status[index] == STATUS_LOSS for index in row["options"])),
        "s4_option_status_counts": {"LOSS": status_counter[STATUS_LOSS],
                                    "UNKNOWN": status_counter[STATUS_UNKNOWN],
                                    "WIN_EXCLUDED": status_counter[-1]},
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--extra-replies", type=int, default=0,
                        help="additional non-central replies per unresolved first move")
    parser.add_argument("--output", type=Path, default=EXPERIMENT / "output/dependency-graph.json.gz")
    parser.add_argument("--summary", type=Path, default=EXPERIMENT / "output/dependency-summary.json")
    args = parser.parse_args()

    board = Board(11)
    cache = load_exact_s5_cache(board)

    s5_index: dict[int, int] = {}
    s5_masks: list[int] = []
    s4_index: dict[int, int] = {}
    s4_masks: list[int] = []
    s4_status: list[int] = []
    s4_cost: list[list[int]] = []

    roots = []
    seen_pair: set[int] = set()
    for spec in selected_roots(args.extra_replies):
        pair, first, reply = canonical_pair(board, spec["first"], spec["reply"])
        if pair in seen_pair:
            continue
        seen_pair.add(pair)
        roots.append(build_root(
            board,
            spec | {"first": first, "reply": reply,
                    "origin_first": spec["first"], "origin_reply": spec["reply"]},
            cache, s5_index, s5_masks, s4_index, s4_masks, s4_status, s4_cost))
    unresolved_firsts = {row["origin_first"] for row in roots if row["role"] != "known-loss-baseline"}
    if len(unresolved_firsts) != 19:
        raise ValueError(f"expected 19 unresolved first moves, found {len(unresolved_firsts)}")

    loss_classes = sum(1 for status in s4_status if status == STATUS_LOSS)
    unknown_classes = sum(1 for status in s4_status if status == STATUS_UNKNOWN)
    win_classes = sum(1 for status in s4_status if status == -1)

    graph = {
        "schema": "n11-joint-s5-dependency-graph-v1",
        "trust_boundary": (
            "S3/S4/S5 geometry comes from the independent integer-geometry Board. "
            "S4 LOSS/UNKNOWN/WIN labels use only the current solver-trusted exact S5 cache. "
            "UNKNOWN children are the only cost items; no unknown verdict is asserted."
        ),
        "source_hashes": {
            "opening_analysis_sha256": sha(OPENINGS),
            "cached_second_reply_ranking_sha256": sha(RANKING),
            "central_reply_frontier_sha256": sha(FRONTIER),
            "current_exact_s5_cache_sha256": sha(CACHE),
            "independent_geometry_sha256": sha(BOARD_SOURCE),
        },
        "parameters": {"extra_replies_per_first": args.extra_replies},
        "counts": {
            "roots": len(roots),
            "s4_classes_total": len(s4_masks),
            "s4_classes_loss": loss_classes,
            "s4_classes_unknown": unknown_classes,
            "s4_classes_win_excluded": win_classes,
            "s5_cost_universe": len(s5_masks),
            "exact_s5_cache_rows": len(cache),
        },
        "roots": roots,
        "s4_masks": [[mask & ((1 << 64) - 1), mask >> 64] for mask in s4_masks],
        "s4_status": s4_status,
        "s4_cost": s4_cost,
        "s5_masks": [[mask & ((1 << 64) - 1), mask >> 64] for mask in s5_masks],
    }

    output = args.output if args.output.is_absolute() else ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(output, "wt", encoding="utf-8", newline="\n") as stream:
        json.dump(graph, stream, separators=(",", ":"))

    summary = {
        "schema": "n11-joint-s5-dependency-summary-v1",
        "source_hashes": graph["source_hashes"],
        "parameters": graph["parameters"],
        "counts": graph["counts"],
        "graph_bytes_gzip": output.stat().st_size,
        "roots": [
            {key: value for key, value in row.items() if key not in ("thirds", "pair_mask")}
            | {"pair_mask": row["pair_mask"],
               "third_count": len(row["thirds"]),
               "options_per_third_min": min(len(item["options"]) for item in row["thirds"]),
               "options_per_third_max": max(len(item["options"]) for item in row["thirds"]),
               "options_per_third_mean": round(
                   sum(len(item["options"]) for item in row["thirds"]) / len(row["thirds"]), 3)}
            for row in roots
        ],
    }
    summary_path = args.summary if args.summary.is_absolute() else ROOT / args.summary
    with summary_path.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"output": str(output), "summary": str(summary_path),
                      "counts": graph["counts"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
