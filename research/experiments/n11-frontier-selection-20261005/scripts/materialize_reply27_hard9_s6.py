#!/usr/bin/env python3
"""Materialize the full canonical s6 boundary below nine hard reply-27 s5 roots.

The nine s5 roots are the unresolved children of the seven still-viable
selected s4 classes after the completed 15M-node reply-27 s5 replay.  This
script does not assign outcomes.  It reconstructs every legal s6 child from
board geometry, D4-canonicalizes them, and emits an exact-replay target set plus
the parent incidence map.

A parent s5 (five stones, AND node for the fixed first-player proposition) is:
- LOSS if any s6 child is exact LOSS;
- WIN if every canonical s6 child is exact WIN;
- UNKNOWN otherwise.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EDGE_DIR = ROOT / "research/experiments/n11-search-methods/scripts"
sys.path.insert(0, str(EDGE_DIR))

from dfpn_edge_classes import d4_canonical_key, legal_after  # noqa: E402

HARD_S5 = [
    (1152921504742115328, 536870912),
    (3602879701897445376, 134217728),
    (10520408729537478660, 67108864),
    (10520408729538527232, 16384),
    (10520408729541689344, 0),
    (10520408729554255872, 32768),
    (10520408730615414784, 0),
    (10520408730619609088, 0),
    (10520408746717347840, 8),
]


def decode(key):
    lo, hi = key
    pts = {p for p in range(64) if (lo >> p) & 1}
    pts.update(q + 64 for q in range(64) if (hi >> q) & 1)
    return pts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--meta-out", type=Path)
    ap.add_argument("--shards", type=int, default=1)
    ap.add_argument("--shard", type=int, default=0)
    args = ap.parse_args()
    if args.shards < 1 or not 0 <= args.shard < args.shards:
        raise SystemExit("require shards>=1 and 0<=shard<shards")

    parents = defaultdict(set)
    per_parent = []
    for i, key in enumerate(HARD_S5):
        occ = decode(key)
        children = {
            d4_canonical_key(list(occ | {z}))
            for z in legal_after(occ)
        }
        per_parent.append(len(children))
        for child in children:
            parents[child].add(i)

    assert len(parents) == 816, len(parents)
    hist = Counter(len(v) for v in parents.values())
    assert hist == Counter({1: 808, 2: 8}), hist

    children = sorted(parents)
    chosen = [
        (i, key) for i, key in enumerate(children)
        if i % args.shards == args.shard
    ]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as fp:
        for seq, key in chosen:
            legal = len(legal_after(decode(key)))
            fp.write(
                f"reply27-hard9-s6,{seq},6,{key[0]},{key[1]},"
                f"{legal},0,1,0,0,0\n"
            )

    meta = {
        "hard_s5": [list(k) for k in HARD_S5],
        "per_parent_canonical_s6": per_parent,
        "unique_canonical_s6": len(children),
        "distinct_parent_histogram": dict(sorted(hist.items())),
        "parents": {
            f"{key[0]}:{key[1]}": sorted(parents[key])
            for key in children
        },
        "claim": "structural boundary only; no outcome asserted",
    }
    if args.meta_out:
        args.meta_out.parent.mkdir(parents=True, exist_ok=True)
        args.meta_out.write_text(
            json.dumps(meta, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    print(json.dumps({
        "hard_s5": len(HARD_S5),
        "unique_s6": len(children),
        "parent_hist": dict(sorted(hist.items())),
        "per_parent": per_parent,
        "shard_rows": len(chosen),
    }, sort_keys=True))
    print("REPLY27_HARD9_S6_MATERIALIZED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
