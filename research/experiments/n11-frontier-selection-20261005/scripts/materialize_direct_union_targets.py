#!/usr/bin/env python3
"""Materialize the direct-union n=11 proof frontier as exact-replay targets.

The 31-class witness is structural: if every selected class is eventually
proved LOSS, the fixed reply {60,0} is refuted.  This script expands those
classes into the DISTINCT canonical s5 positions that are not already covered
by the two independently verified LOSS classes.

Output rows use the existing --exact-replay record schema:
    tag,seq,stones,key_lo,key_hi,legal,depth,is_or,retries,nodes,result

No verdict is asserted for a target row; result=0 means "to solve".
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EDGE_DIR = ROOT / "research/experiments/n11-search-methods/scripts"
sys.path.insert(0, str(EDGE_DIR))

from dfpn_edge_classes import FIRST, R2, d4_canonical_key, legal_after  # noqa: E402

HERE = Path(__file__).resolve().parents[1]
DEFAULT_WITNESS = HERE / "output/direct-union-cover.json"


def build_classes():
    base = {FIRST, R2}
    verts = legal_after(base)
    groups = defaultdict(list)
    for a in verts:
        for b in legal_after(base | {a}):
            if b <= a:
                continue
            key = d4_canonical_key([FIRST, R2, a, b])
            groups[key].append((a, b))
    assert len(groups) == 3396
    return groups


def class_children(key, groups):
    out = set()
    base = {FIRST, R2}
    for a, b in groups[key]:
        occ = base | {a, b}
        for z in legal_after(occ):
            out.add(d4_canonical_key([FIRST, R2, a, b, z]))
    return out


def occupied_from_key(key):
    lo, hi = key
    out = set()
    for p in range(64):
        if (lo >> p) & 1:
            out.add(p)
    for q in range(64):
        if (hi >> q) & 1:
            out.add(q + 64)
    assert len(out) == 5
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--witness", type=Path, default=DEFAULT_WITNESS)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--shards", type=int, default=1)
    ap.add_argument("--shard", type=int, default=0)
    args = ap.parse_args()
    if args.shards < 1 or not (0 <= args.shard < args.shards):
        raise SystemExit("require shards>=1 and 0<=shard<shards")

    doc = json.loads(args.witness.read_text(encoding="utf-8"))
    selected = [tuple(row["key"]) for row in doc["selected"]]
    forced = [tuple(row) for row in doc["forced_known_loss_keys"]]

    groups = build_classes()
    children = {}
    for key in set(selected) | set(forced):
        if key not in groups:
            raise SystemExit(f"witness class missing from regenerated geometry: {key}")
        children[key] = class_children(key, groups)

    known = set().union(*(children[key] for key in forced))
    needed = set().union(*(children[key] for key in selected)) - known
    targets = sorted(needed)
    if len(known) != 209 or len(targets) != 2319:
        raise SystemExit(
            f"unexpected frontier size: known={len(known)} targets={len(targets)}"
        )

    chosen = [(i, key) for i, key in enumerate(targets) if i % args.shards == args.shard]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as fh:
        fh.write(
            "# direct-union n11 s5 targets; empty verdicts only; "
            f"global=2319 shards={args.shards} shard={args.shard}\n"
        )
        for global_i, key in chosen:
            legal = len(legal_after(occupied_from_key(key)))
            fh.write(
                f"direct-union-{global_i},{global_i},5,{key[0]},{key[1]},"
                f"{legal},0,0,0,0,0\n"
            )
        fh.write(f"# target_done rows={len(chosen)} global=2319 known_loss=209\n")

    print(
        f"TARGETS_OK global=2319 shard={args.shard}/{args.shards} "
        f"rows={len(chosen)} out={args.out}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
