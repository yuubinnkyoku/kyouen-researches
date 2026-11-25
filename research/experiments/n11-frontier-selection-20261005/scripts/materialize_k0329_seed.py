#!/usr/bin/env python3
"""Materialize the independently verified 209-row n=11 s5 LOSS seed.

The seed consists exactly of the canonical s5 children of the two K0329
LOSS s4 classes under root {60,0}.  Verdicts are not inferred from geometry:
the two universal LOSS class proofs were independently cold-replayed in K0329.
Geometry here is used only to regenerate their canonical child keys.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EDGE_DIR = ROOT / "research/experiments/n11-search-methods/scripts"
sys.path.insert(0, str(EDGE_DIR))

from dfpn_edge_classes import d4_canonical_key, legal_after  # noqa: E402

FIRST, R2 = 60, 0
LOSS_CLASSES = {
    (1152921504606846983, 0): 103,
    (1152921504606848001, 4): 106,
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    base = {FIRST, R2}
    groups = {}
    for a in legal_after(base):
        for b in legal_after(base | {a}):
            if b <= a:
                continue
            k = d4_canonical_key([FIRST, R2, a, b])
            if k in LOSS_CLASSES:
                groups.setdefault(k, []).append((a, b))
    assert set(groups) == set(LOSS_CLASSES)

    all_children = set()
    for key, expected in LOSS_CLASSES.items():
        # D4-equivalent raw edges have the same canonical s5 child set.
        a, b = groups[key][0]
        occ = base | {a, b}
        children = {
            d4_canonical_key(list(occ | {z}))
            for z in legal_after(occ)
        }
        assert len(children) == expected, (key, len(children), expected)
        all_children.update(children)

    assert len(all_children) == 209
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as fp:
        fp.write("# s5 verdict cache: n=11 schema=1 (canonical key -> WIN/LOSS, UNKNOWN never stored)\n")
        for lo, hi in sorted(all_children):
            # nodes=0 marks proof-derived materialization; the verifier never
            # trusts this metadata and K0329 cold-replayed every verdict.
            fp.write(f"s5verdict,{lo},{hi},5,2,0\n")
    print(f"K0329_SEED_OK rows={len(all_children)} out={args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
