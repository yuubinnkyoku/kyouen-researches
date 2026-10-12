#!/usr/bin/env python3
"""First-move WIN-side proof dependency analysis (no solver search).

For a fixed first move f (first player), a WIN proof needs, for EVERY legal
reply r (second player): a third move t such that every legal fourth move u
leaves an S4={f,r,t,u} that is first-player WIN.  In fixed-first-player view
(K0371): S4 (even, OR) is WIN iff at least one S5 child is WIN; S5 (odd, AND)
is WIN iff every S6 child is WIN.

With only the existing exact-S5 cache, an S4 is classified by the shared
s4_win_polarity module as:
  free: has a cached WIN child (already first-player WIN),
  dead: every legal child cached LOSS, or no legal child at all (even-layer
        terminal LOSS; proven first-player LOSS, a LOSS-side asset instead),
  open: otherwise, i.e. no cached WIN child but >= 1 unknown child
        (optimistically usable iff one unknown child later becomes WIN,
        whose own closure needs ALL of its S6 children WIN).

A third move is viable iff none of its fourths is dead.  A reply is closable
iff it has a viable third.  Per viable third a greedy witness cover picks a
small set of unknown S5s hitting every open fourth S4 (optimistic frontier,
NOT a proof).  Replies are D4-reduced under the stabiliser of f.  S4 classes
reuse the K0417 central index space with appended new classes.
"""
from __future__ import annotations

import argparse
import gzip
import json
import sys
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
NEW_EXPERIMENT = ROOT / "research/experiments/n11-proof-cost-comparison-20261012"
OLD_EXPERIMENT = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012"
OLD_SCRIPTS = OLD_EXPERIMENT / "scripts"

sys.path.insert(0, str(NEW_EXPERIMENT / "scripts"))
sys.path.insert(0, str(OLD_SCRIPTS))
sys.path.insert(0, str(ROOT / "research/experiments/n11-central-reply-frontier-20261012/scripts"))
sys.path.insert(0, str(ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts"))
from independent import Board  # noqa: E402
from analyze_central_reply_frontier import (  # noqa: E402
    load_exact_s5_cache, sha, CACHE as CACHE_PATH)
from build_dependency_graph import key_of  # noqa: E402
from s4_win_polarity import classify_s4, verdict_of, FREE, OPEN, DEAD  # noqa: E402


def mask_of(pair: list[int]) -> int:
    return pair[0] | (pair[1] << 64)


def greedy_witness_cover(needs: list[set[int]]) -> set[int]:
    """Hit every non-empty need-set with few elements (optimistic frontier)."""
    uncovered = [s for s in needs if s]
    chosen: set[int] = set()
    while uncovered:
        freq: Counter[int] = Counter()
        for s in uncovered:
            for e in s:
                freq[e] += 1
        best = max(freq, key=lambda e: (freq[e], e))
        chosen.add(best)
        uncovered = [s for s in uncovered if best not in s]
    return chosen


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--graph", type=Path,
                        default=OLD_EXPERIMENT / "output/dependency-graph.json.gz")
    parser.add_argument("--firsts", type=int, nargs="+", default=[49])
    parser.add_argument("--output", type=Path,
                        default=NEW_EXPERIMENT / "output/win-side-analysis.json")
    args = parser.parse_args()
    started = time.time()

    graph_path = args.graph if args.graph.is_absolute() else ROOT / args.graph
    with gzip.open(graph_path, "rt", encoding="utf-8") as stream:
        central = json.load(stream)

    board = Board(11)
    cache = load_exact_s5_cache(board)
    s5_masks = [mask_of(pair) for pair in central["s5_masks"]]
    s4_masks = [mask_of(pair) for pair in central["s4_masks"]]
    s5_index = {m: i for i, m in enumerate(s5_masks)}
    s4_index = {m: i for i, m in enumerate(s4_masks)}
    base_s4, base_s5 = len(s4_masks), len(s5_masks)
    s4_kind: dict[int, str] = {}
    s4_unknown: dict[int, list[int]] = {}

    def classify(index: int) -> str:
        hit = s4_kind.get(index)
        if hit is not None:
            return hit
        children = board.children(s4_masks[index])
        verdicts = [verdict_of(cache, key_of(c)) for c in children]
        kind = classify_s4(verdicts)
        unknown = []
        if kind == OPEN:
            for c, v in zip(children, verdicts):
                if v != 0:
                    continue
                k = s5_index.get(c)
                if k is None:
                    k = len(s5_masks)
                    s5_index[c] = k
                    s5_masks.append(c)
                unknown.append(k)
        s4_kind[index] = kind
        s4_unknown[index] = unknown
        return kind

    analyses = []
    for first in args.firsts:
        t_first = time.time()
        stab = [m for m in board.maps if m[first] == (1 << first)]
        seen: set[tuple] = set()
        orbit_reps: list[int] = []
        for r in range(121):
            if r == first:
                continue
            orb = tuple(sorted(m[r] for m in stab))
            if orb in seen:
                continue
            seen.add(orb)
            orbit_reps.append(r)
        reply_rows = []
        witness_union: set[int] = set()
        and_width = 0
        for pos, r in enumerate(orbit_reps):
            pair = (1 << first) | (1 << r)
            thirds = board.points(board.legal(pair))
            assert len(thirds) == 119, f"pair {{{first},{r}}}: {len(thirds)} thirds"
            best: dict | None = None
            n_viable = 0
            n_all_free = 0
            for t in thirds:
                s3 = pair | (1 << t)
                fourths = board.points(board.legal(s3))
                s4s = []
                for u in fourths:
                    m = board.canonical(s3 | (1 << u))
                    i = s4_index.get(m)
                    if i is None:
                        i = len(s4_masks)
                        s4_index[m] = i
                        s4_masks.append(m)
                    s4s.append(i)
                kinds = [classify(i) for i in s4s]
                if DEAD in kinds:
                    continue
                n_viable += 1
                needs = [set(s4_unknown[i]) for i, k in zip(s4s, kinds) if k == OPEN]
                if not needs:
                    n_all_free += 1
                    cand = {"third": t, "fourths": len(fourths), "witnesses": []}
                else:
                    wit = sorted(greedy_witness_cover(needs))
                    cand = {"third": t, "fourths": len(fourths), "witnesses": wit}
                if best is None or len(cand["witnesses"]) < len(best["witnesses"]):
                    best = cand
            if best is None:
                reply_rows.append({"reply": r, "closable": False})
            else:
                witness_union |= set(best["witnesses"])
                and_width += best["fourths"]
                reply_rows.append({"reply": r, "closable": True,
                                    "all_free": n_all_free > 0,
                                    "viable_thirds": n_viable,
                                    "chosen_third": best["third"],
                                    "chosen_fourths": best["fourths"],
                                    "witnesses": best["witnesses"],
                                    "witness_masks": sorted(
                                        [s5_masks[e] & ((1 << 64) - 1),
                                         s5_masks[e] >> 64]
                                        for e in best["witnesses"])})
            print(f"  first {first}: reply {pos + 1}/{len(orbit_reps)} "
                  f"(r={r}) closable={best is not None} "
                  f"s4_touched={len(s4_kind)}", flush=True)
        n_close = sum(1 for x in reply_rows if x["closable"])
        n_free = sum(1 for x in reply_rows if x.get("all_free"))
        analyses.append({
            "first": first,
            "stabiliser_order": len(stab),
            "reply_orbits": len(orbit_reps),
            "closable_replies": n_close,
            "unclosable_replies": [x["reply"] for x in reply_rows if not x["closable"]],
            "free_closable_replies": n_free,
            "witness_replies": n_close - n_free,
            "and_width_fourths": and_width,
            "optimistic_witness_s5": len(witness_union),
            "replies": reply_rows,
            "seconds": round(time.time() - t_first, 1),
        })
        print(json.dumps({k: analyses[-1][k] for k in
                          ("first", "reply_orbits", "closable_replies",
                           "free_closable_replies", "witness_replies",
                           "and_width_fourths", "optimistic_witness_s5",
                           "seconds")}, ensure_ascii=False), flush=True)

    new_s4 = len(s4_masks) - base_s4
    new_s5 = len(s5_masks) - base_s5
    kind_counts = Counter(s4_kind.values())
    result = {
        "schema": "n11-win-side-analysis-v2",
        "polarity": ("K0371 fixed-first-player: S4 WIN iff >= 1 cached S5 WIN "
                     "child; S4 LOSS (dead) iff all legal children cached LOSS "
                     "or no legal child; open iff no cached WIN but >= 1 "
                     "unknown child. Shared module s4_win_polarity."),
        "central_graph_sha256": sha(graph_path),
        "cache_sha256": sha(CACHE_PATH),
        "polarity_module_sha256": sha(NEW_EXPERIMENT / "scripts" / "s4_win_polarity.py"),
        "cache_rows": len(cache),
        "s4_classes_touched": len(s4_kind),
        "s4_kind_counts": dict(kind_counts),
        "s4_dead_loss_side_assets": kind_counts.get(DEAD, 0),
        "new_s4_classes": new_s4,
        "new_s5_masks": new_s5,
        "note": ("witness counts are optimistic frontiers: every witness S5 "
                 "still needs its own all-sixths WIN closure (S5 AND layer), "
                 "which is NOT costed here. Dead S4s (all children cached "
                 "LOSS, or terminal) are proven first-player-LOSS positions "
                 "reusable by the LOSS side."),
        "firsts": analyses,
        "seconds": round(time.time() - started, 1),
    }
    output = args.output if args.output.is_absolute() else ROOT / args.output
    with output.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
