#!/usr/bin/env python3
"""Reduce unresolved reply-27 selected-frontier s5 roots to shared s6 witnesses.

Given an s5 verdict cache, regenerate the 31 selected s4 classes from geometry.
Classes with a cached WIN child are discarded; classes whose children are all
cached LOSS are already proved LOSS.  For the remaining selected classes,
collect the unresolved canonical s5 roots and build an outcome-blind greedy
cover by canonical s6 children.

This does not assert any s6 verdict.  If a chosen s6 later proves first-player
LOSS, that verdict simultaneously proves every listed parent s5 LOSS.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EDGE_DIR = ROOT / "research/experiments/n11-search-methods/scripts"
sys.path.insert(0, str(EDGE_DIR))

from dfpn_edge_classes import d4_canonical_key, legal_after  # noqa: E402

HERE = Path(__file__).resolve().parents[1]
WITNESS = HERE / "output/reply27-direct-union-cover.json"


def decode(key):
    lo, hi = key
    pts = {p for p in range(64) if (lo >> p) & 1}
    pts.update(q + 64 for q in range(64) if (hi >> q) & 1)
    return pts


def load_cache(path):
    verdict = {}
    with path.open(newline="", encoding="utf-8") as fp:
        for row in csv.reader(fp):
            if not row or row[0].startswith("#"):
                continue
            if row[0] != "s5verdict":
                continue
            key = (int(row[1]), int(row[2]))
            value = int(row[4])
            if value not in (1, 2):
                raise SystemExit(f"invalid cached verdict {value} for {key}")
            old = verdict.get(key)
            if old is not None and old != value:
                raise SystemExit(f"CONFLICT key={key} old={old} new={value}")
            verdict[key] = value
    return verdict


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--s5-cache", type=Path, required=True)
    ap.add_argument("--targets-out", type=Path)
    args = ap.parse_args()

    cache = load_cache(args.s5_cache)
    doc = json.loads(WITNESS.read_text(encoding="utf-8"))
    first, r2 = doc["root"]
    selected = [tuple(x) for x in doc["classes"]]
    base = {first, r2}

    groups = defaultdict(list)
    for a in legal_after(base):
        for b in legal_after(base | {a}):
            if b <= a:
                continue
            key = d4_canonical_key([first, r2, a, b])
            if key in selected:
                groups[key].append((a, b))
    assert set(groups) == set(selected)

    unresolved = set()
    selected_counts = {"WIN": 0, "LOSS": 0, "UNKNOWN": 0}
    unresolved_by_class = {}
    for key in selected:
        children = set()
        for a, b in groups[key]:
            occ = base | {a, b}
            for z in legal_after(occ):
                children.add(d4_canonical_key(list(occ | {z})))
        vals = [cache.get(ch, 0) for ch in children]
        if 1 in vals:
            selected_counts["WIN"] += 1
            continue
        missing = sorted(ch for ch in children if ch not in cache)
        if not missing:
            selected_counts["LOSS"] += 1
            continue
        selected_counts["UNKNOWN"] += 1
        unresolved.update(missing)
        unresolved_by_class[f"{key[0]}:{key[1]}"] = [
            [lo, hi] for lo, hi in missing
        ]

    unresolved = sorted(unresolved)
    parent_of = {key: i for i, key in enumerate(unresolved)}
    parents = defaultdict(set)
    for key in unresolved:
        occ = decode(key)
        for z in legal_after(occ):
            child = d4_canonical_key(list(occ | {z}))
            parents[child].add(parent_of[key])

    uncovered = set(range(len(unresolved)))
    chosen = []
    while uncovered:
        child = max(
            parents,
            key=lambda k: (
                len(parents[k] & uncovered),
                -k[1],
                -k[0],
            ),
        )
        hit = parents[child] & uncovered
        if not hit:
            raise SystemExit("structural s6 cover stalled")
        chosen.append((child, sorted(hit)))
        uncovered -= hit

    out = {
        "selected_s4_status_counts": selected_counts,
        "unresolved_selected_s5": len(unresolved),
        "unique_s6_children": len(parents),
        "s6_structural_cover_size": len(chosen),
        "unresolved_by_class": unresolved_by_class,
        "s6_cover": [
            {
                "key": [child[0], child[1]],
                "parent_indices": hit,
                "legal": len(legal_after(decode(child))),
            }
            for child, hit in chosen
        ],
        "claim": "outcome-blind structural cover only; no s6 verdict asserted",
    }
    print(json.dumps(out, indent=2, sort_keys=True))
    print("REPLY27_SELECTED_HARD_S5_S6_COVER_OK")

    if args.targets_out:
        args.targets_out.parent.mkdir(parents=True, exist_ok=True)
        with args.targets_out.open("w", encoding="utf-8") as fp:
            for seq, (child, hit) in enumerate(chosen):
                legal = len(legal_after(decode(child)))
                fp.write(
                    f"reply27-hard-s6,{seq},6,{child[0]},{child[1]},"
                    f"{legal},0,1,0,0,0\n"
                )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
