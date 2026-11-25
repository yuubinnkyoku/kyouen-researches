#!/usr/bin/env python3
"""Build dependency-graph roots for non-central replies, sharing index space.

For first moves 49/38/16 the top non-central replies (27, 93) from the cached
reply ranking are enumerated with the same independent Board + exact-cache
procedure as K0417.  S4/S5 index maps are pre-seeded from the central graph so
class indices coincide wherever geometry repeats; genuinely new classes are
appended with global indices.  This makes S4/S5 reuse across central and
alternative roots directly measurable.  No solver search is involved.
"""
from __future__ import annotations

import argparse
import gzip
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
NEW_EXPERIMENT = ROOT / "research/experiments/n11-proof-cost-comparison-20261012"
OLD_EXPERIMENT = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012"
OLD_SCRIPTS = OLD_EXPERIMENT / "scripts"

sys.path.insert(0, str(OLD_SCRIPTS))
sys.path.insert(0, str(ROOT / "research/experiments/n11-central-reply-frontier-20261012/scripts"))
sys.path.insert(0, str(ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts"))
from independent import Board  # noqa: E402
from analyze_central_reply_frontier import load_exact_s5_cache, sha  # noqa: E402
from build_dependency_graph import build_root, canonical_pair, key_of  # noqa: E402

TARGETS = {49: [27, 93], 38: [27, 93], 16: [27, 93]}


def mask_of(pair: list[int]) -> int:
    return pair[0] | (pair[1] << 64)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--graph", type=Path,
                        default=OLD_EXPERIMENT / "output/dependency-graph.json.gz")
    parser.add_argument("--output", type=Path,
                        default=NEW_EXPERIMENT / "output/alt-roots.json.gz")
    parser.add_argument("--summary", type=Path,
                        default=NEW_EXPERIMENT / "output/alt-roots-summary.json")
    args = parser.parse_args()
    started = time.time()

    graph_path = args.graph if args.graph.is_absolute() else ROOT / args.graph
    with gzip.open(graph_path, "rt", encoding="utf-8") as stream:
        central = json.load(stream)

    board = Board(11)
    cache = load_exact_s5_cache(board)

    s5_masks = [mask_of(pair) for pair in central["s5_masks"]]
    s4_masks = [mask_of(pair) for pair in central["s4_masks"]]
    s4_status = list(central["s4_status"])
    s4_cost = [list(row) for row in central["s4_cost"]]
    s5_index = {mask: i for i, mask in enumerate(s5_masks)}
    s4_index = {mask: i for i, mask in enumerate(s4_masks)}
    base_s4 = len(s4_masks)
    base_s5 = len(s5_masks)

    seen_pair = {mask_of(root["pair_mask"]) for root in central["roots"]}
    roots = []
    skipped = []
    for first, replies in TARGETS.items():
        for reply in replies:
            pair, c_first, c_reply = canonical_pair(board, first, reply)
            if pair in seen_pair:
                skipped.append({"first": first, "reply": reply,
                                "reason": "canonical pair already in central graph"})
                continue
            seen_pair.add(pair)
            n_s4_before, n_s5_before = len(s4_masks), len(s5_masks)
            row = build_root(
                board,
                {"first": c_first, "reply": c_reply,
                 "origin_first": first, "origin_reply": reply,
                 "role": "alternative"},
                cache, s5_index, s5_masks, s4_index, s4_masks,
                s4_status, s4_cost)
            row["new_s4_classes"] = len(s4_masks) - n_s4_before
            row["new_s5_universe"] = len(s5_masks) - n_s5_before
            roots.append(row)

    new_s4 = {str(i): {"mask": [m & ((1 << 64) - 1), m >> 64],
                       "status": s4_status[i], "cost": s4_cost[i]}
              for i, m in enumerate(s4_masks[base_s4:], start=base_s4)}
    new_s5 = {str(i): [m & ((1 << 64) - 1), m >> 64]
              for i, m in enumerate(s5_masks[base_s5:], start=base_s5)}

    payload = {
        "schema": "n11-alt-roots-v1",
        "central_graph": str(graph_path.relative_to(ROOT)),
        "central_graph_sha256": sha(graph_path),
        "base_s4_classes": base_s4,
        "base_s5_universe": base_s5,
        "total_s4_classes": len(s4_masks),
        "total_s5_universe": len(s5_masks),
        "targets": {str(k): v for k, v in TARGETS.items()},
        "skipped": skipped,
        "roots": roots,
        "new_s4_classes": new_s4,
        "new_s5_masks": new_s5,
        "seconds": round(time.time() - started, 1),
    }
    output = args.output if args.output.is_absolute() else ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(output, "wt", encoding="utf-8", newline="\n") as stream:
        json.dump(payload, stream, separators=(",", ":"))
    summary = {
        "schema": "n11-alt-roots-summary-v1",
        "roots": [
            {"origin_first": r["origin_first"], "origin_reply": r["origin_reply"],
             "canonical_first": r["canonical_first"],
             "canonical_reply": r["canonical_reply"],
             "reachable_s4_classes": r["reachable_s4_classes"],
             "s4_option_slots": r["s4_option_slots"],
             "thirds_with_free_loss_s4": r["thirds_with_free_loss_s4"],
             "s4_option_status_counts": r["s4_option_status_counts"],
             "new_s4_classes": r["new_s4_classes"],
             "new_s5_universe": r["new_s5_universe"]}
            for r in roots],
        "skipped": skipped,
        "seconds": payload["seconds"],
    }
    summary_path = args.summary if args.summary.is_absolute() else ROOT / args.summary
    with summary_path.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
