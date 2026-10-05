#!/usr/bin/env python3
"""Materialize the reply-27 31-class witness into exact-replay s5 shards."""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EDGE_DIR = ROOT / "research/experiments/n11-search-methods/scripts"
sys.path.insert(0, str(EDGE_DIR))

from dfpn_edge_classes import d4_canonical_key, legal_after  # noqa: E402

HERE = Path(__file__).resolve().parents[1]
DEFAULT_WITNESS = HERE / "output/reply27-direct-union-cover.json"


def occupied_from_key(key):
    lo, hi = key
    pts = {p for p in range(64) if (lo >> p) & 1}
    pts.update(q + 64 for q in range(64) if (hi >> q) & 1)
    assert len(pts) == 5
    return pts


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
    first, r2 = doc["root"]
    selected = [tuple(x) for x in doc["classes"]]

    base = {first, r2}
    verts = legal_after(base)
    groups = defaultdict(list)
    for a in verts:
        for b in legal_after(base | {a}):
            if b <= a:
                continue
            key = d4_canonical_key([first, r2, a, b])
            if key in selected:
                groups[key].append((a, b))

    missing = set(selected) - set(groups)
    if missing:
        raise SystemExit(f"selected classes missing from geometry: {sorted(missing)}")

    targets = set()
    for key in selected:
        for a, b in groups[key]:
            occ = base | {a, b}
            for z in legal_after(occ):
                targets.add(d4_canonical_key([first, r2, a, b, z]))
    targets = sorted(targets)
    if len(targets) != doc["selected_unique_s5"] != 2262:
        raise SystemExit(f"unexpected target count {len(targets)}")
    if len(targets) != 2262:
        raise SystemExit(f"expected 2262 targets, got {len(targets)}")

    chosen = [(i, key) for i, key in enumerate(targets) if i % args.shards == args.shard]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as fh:
        fh.write(
            "# reply27 direct-union n11 s5 targets; no verdict asserted; "
            f"global=2262 shards={args.shards} shard={args.shard}\n"
        )
        for i, key in chosen:
            legal = len(legal_after(occupied_from_key(key)))
            fh.write(
                f"reply27-{i},{i},5,{key[0]},{key[1]},{legal},0,0,0,0,0\n"
            )
        fh.write(f"# target_done rows={len(chosen)} global=2262\n")

    print(
        f"REPLY27_TARGETS_OK global=2262 shard={args.shard}/{args.shards} "
        f"rows={len(chosen)} out={args.out}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
