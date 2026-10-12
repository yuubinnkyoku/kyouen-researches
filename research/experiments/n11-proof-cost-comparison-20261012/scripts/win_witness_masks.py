#!/usr/bin/env python3
"""Verify the WIN-side witness covers against recomputed geometry (K0371).

For every closable reply of the stored WIN-side analysis, this script
re-enumerates the chosen third's fourths from the independent Board, rebuilds
each S4's child verdicts from the exact cache, and checks with the shared
s4_win_polarity module that

* no fourth S4 is dead (otherwise the reply is not closable),
* every open fourth S4 contains at least one stored witness mask,
* every stored witness mask is a canonical, cache-unknown S5 key
  (a proper optimistic WIN witness: cached keys cannot become WIN, and
  non-canonical keys are unstable aliases),
* the distinct-witness total matches the analysis header.

It then saves the verified witness mask set for overlap measurement against
the LOSS-side joint plan.  No solver search is involved.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
NEW_EXPERIMENT = ROOT / "research/experiments/n11-proof-cost-comparison-20261012"

sys.path.insert(0, str(NEW_EXPERIMENT / "scripts"))
sys.path.insert(0, str(ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts"))
sys.path.insert(0, str(ROOT / "research/experiments/n11-central-reply-frontier-20261012/scripts"))
from independent import Board  # noqa: E402
from analyze_central_reply_frontier import load_exact_s5_cache, sha  # noqa: E402
from s4_win_polarity import classify_s4, verdict_of, FREE, OPEN, DEAD  # noqa: E402


def key_of(mask: int) -> tuple[int, int]:
    return mask & ((1 << 64) - 1), mask >> 64


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--analysis", type=Path,
                        default=NEW_EXPERIMENT / "output/win-side-analysis.json")
    parser.add_argument("--output", type=Path,
                        default=NEW_EXPERIMENT / "output/win-witness-masks.json")
    args = parser.parse_args()
    started = time.time()

    analysis = json.loads(args.analysis.read_text(encoding="utf-8"))
    assert analysis["schema"] == "n11-win-side-analysis-v2", \
        "verifier requires the corrected-polarity analysis"
    first_row = next(a for a in analysis["firsts"] if a["first"] == 49)
    board = Board(11)
    cache = load_exact_s5_cache(board)

    failures: list[str] = []
    masks: set[int] = set()
    for rep in first_row["replies"]:
        if not rep["closable"]:
            continue
        stored = {lo | (hi << 64) for lo, hi in rep["witness_masks"]}
        for m in stored:
            if board.canonical(m) != m:
                failures.append(f"reply {rep['reply']}: stored witness is "
                                f"non-canonical {key_of(m)}")
            if key_of(m) in cache:
                failures.append(f"reply {rep['reply']}: stored witness "
                                f"{key_of(m)} is already cached")
        masks |= stored
        pair = (1 << 49) | (1 << rep["reply"])
        s3 = pair | (1 << rep["chosen_third"])
        fourths = board.points(board.legal(s3))
        if len(fourths) != rep["chosen_fourths"]:
            failures.append(f"reply {rep['reply']}: fourth count drift")
            continue
        for u in fourths:
            m = board.canonical(s3 | (1 << u))
            children = board.children(m)
            verdicts = [verdict_of(cache, key_of(c)) for c in children]
            kind = classify_s4(verdicts)
            if kind == DEAD:
                failures.append(f"reply {rep['reply']}: dead S4 in stored "
                                f"viable third")
            elif kind == OPEN:
                unknown = {c for c, v in zip(children, verdicts) if v == 0}
                if not (unknown & stored):
                    failures.append(f"reply {rep['reply']}: open S4 left "
                                    f"unwitnessed by stored cover")
            elif kind != FREE:
                failures.append(f"reply {rep['reply']}: unknown kind {kind}")

    if len(masks) != first_row["optimistic_witness_s5"]:
        failures.append(f"distinct total {len(masks)} != header "
                        f"{first_row['optimistic_witness_s5']}")

    result = {
        "schema": "n11-win-witness-masks-v2",
        "analysis_sha256": sha(args.analysis),
        "cache_sha256": sha(ROOT / "research/experiments/n11-s4-boundary-direct-20261012/output/current-exact-s5.cache"),
        "polarity_module_sha256": sha(NEW_EXPERIMENT / "scripts" / "s4_win_polarity.py"),
        "first": 49,
        "verified_witness_s5": len(masks),
        "failures": failures,
        "passed": not failures,
        "witness_masks": sorted([[m & ((1 << 64) - 1), m >> 64] for m in masks]),
        "seconds": round(time.time() - started, 1),
    }
    with args.output.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(result, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(json.dumps({k: result[k] for k in ("verified_witness_s5", "passed",
                                            "failures", "seconds")},
                     ensure_ascii=False, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
