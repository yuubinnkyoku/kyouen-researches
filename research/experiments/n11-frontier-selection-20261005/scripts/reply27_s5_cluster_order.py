#!/usr/bin/env python3
"""Order reply-27 s5 jobs to expose s6 sharing early.

Builds the exact 2262-target s5 frontier and its 81999 canonical s6 children,
then greedily schedules the next s5 with the largest number of s6 children
already present in the accumulated cache.  This is a structural scheduler:
no game verdict or runtime-cost claim is made.

It is intended for A/B against canonical-key order with --exact-share-layer=6.
"""
from __future__ import annotations

import argparse
import heapq
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


def build_s5():
    doc = json.loads(WITNESS.read_text(encoding="utf-8"))
    first, r2 = doc["root"]
    selected = {tuple(x) for x in doc["classes"]}
    base = {first, r2}
    groups = defaultdict(list)
    for a in legal_after(base):
        for b in legal_after(base | {a}):
            if b <= a:
                continue
            key = d4_canonical_key([first, r2, a, b])
            if key in selected:
                groups[key].append((a, b))
    assert set(groups) == selected
    s5 = set()
    for key in selected:
        for a, b in groups[key]:
            occ = base | {a, b}
            for z in legal_after(occ):
                s5.add(d4_canonical_key(list(occ | {z})))
    assert len(s5) == 2262
    return sorted(s5)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, help="write exact-replay CSV in clustered order")
    ap.add_argument("--prefix", type=int, default=16)
    args = ap.parse_args()

    s5 = build_s5()
    index = {key: i for i, key in enumerate(s5)}
    children = [set() for _ in s5]
    parents = defaultdict(set)
    for i, key in enumerate(s5):
        occ = decode(key)
        for z in legal_after(occ):
            child = d4_canonical_key(list(occ | {z}))
            children[i].add(child)
            parents[child].add(i)
    assert len(parents) == 81999

    # Weighted sharing degree: number of pairwise shared s6 incidences.
    wdeg = [0] * len(s5)
    for ps in parents.values():
        q = list(ps)
        for a in range(len(q)):
            for b in range(a + 1, len(q)):
                wdeg[q[a]] += 1
                wdeg[q[b]] += 1

    # Seed with the most sharing-central target, then maximize overlap with
    # the accumulated s6 cache. Ties prefer fewer new children, then larger
    # global sharing degree, then canonical index.
    start = max(range(len(s5)), key=lambda i: (wdeg[i], -len(children[i]), -i))
    chosen = [False] * len(s5)
    overlap = [0] * len(s5)
    order = [start]
    chosen[start] = True
    cached = set(children[start])

    for ch in children[start]:
        for j in parents[ch]:
            if not chosen[j]:
                overlap[j] += 1

    heap = []
    def push(j):
        heapq.heappush(
            heap,
            (-overlap[j], len(children[j]) - overlap[j], -wdeg[j], j),
        )
    for j in range(len(s5)):
        if not chosen[j]:
            push(j)

    while len(order) < len(s5):
        while True:
            neg, new_count, neg_deg, j = heapq.heappop(heap)
            if chosen[j]:
                continue
            if (
                -neg != overlap[j]
                or new_count != len(children[j]) - overlap[j]
                or -neg_deg != wdeg[j]
            ):
                push(j)
                continue
            break
        chosen[j] = True
        order.append(j)
        for ch in children[j]:
            if ch in cached:
                continue
            cached.add(ch)
            for q in parents[ch]:
                if not chosen[q]:
                    overlap[q] += 1
                    push(q)

    def prefix_stats(seq, n):
        cache = set()
        hits = 0
        rows = []
        for pos, i in enumerate(seq[:n]):
            h = len(children[i] & cache)
            rows.append((pos, i, h, len(children[i])))
            hits += h
            cache.update(children[i])
        return hits, len(cache), rows

    p = min(args.prefix, len(s5))
    sorted_hits, sorted_unique, _ = prefix_stats(list(range(len(s5))), p)
    cluster_hits, cluster_unique, rows = prefix_stats(order, p)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        with args.out.open("w", encoding="utf-8") as fp:
            for seq, i in enumerate(order):
                lo, hi = s5[i]
                legal = len(legal_after(decode(s5[i])))
                fp.write(f"reply27-cluster,{seq},5,{lo},{hi},{legal},0,0,0,0,0\n")

    out = {
        "targets": len(s5),
        "unique_s6": len(parents),
        "prefix": p,
        "canonical_order_prior_s6_hits": sorted_hits,
        "clustered_order_prior_s6_hits": cluster_hits,
        "hit_increase": cluster_hits - sorted_hits,
        "hit_increase_fraction":
            (cluster_hits / sorted_hits - 1.0) if sorted_hits else None,
        "canonical_order_unique_s6_after_prefix": sorted_unique,
        "clustered_order_unique_s6_after_prefix": cluster_unique,
        "first_clustered_rows": [
            {
                "position": pos,
                "canonical_index": i,
                "prior_s6_hits": h,
                "s6_children": nchild,
            }
            for pos, i, h, nchild in rows
        ],
        "claim": "structural job-ordering result only; no runtime or verdict claim",
    }
    print(json.dumps(out, indent=2, sort_keys=True))
    print("REPLY27_S5_CLUSTER_ORDER_VERIFIED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
