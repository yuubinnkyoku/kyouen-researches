#!/usr/bin/env python3
"""Construct a small structural s6 witness cover below the reply-27 s5 frontier.

This is outcome-blind.  It proves only that 847 canonical s6 positions can be
chosen so every one of the 2262 target s5 roots has at least one selected s6
child.  If those selected s6 positions were all exact LOSS for the fixed first
player, they would witness LOSS for every target s5.  No such verdict claim is
made here.
"""
from __future__ import annotations

import heapq
import itertools
import json
import random
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EDGE_DIR = ROOT / "research/experiments/n11-search-methods/scripts"
sys.path.insert(0, str(EDGE_DIR))

from dfpn_edge_classes import V, d4_canonical_key, forbidden, legal_after  # noqa: E402

HERE = Path(__file__).resolve().parents[1]
WITNESS = HERE / "output/reply27-direct-union-cover.json"


def decode(key):
    lo, hi = key
    pts = {p for p in range(64) if (lo >> p) & 1}
    pts.update(q + 64 for q in range(64) if (hi >> q) & 1)
    return pts


def main():
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
                s5.add(d4_canonical_key([first, r2, a, b, z]))
    s5 = sorted(s5)
    assert len(s5) == 2262
    s5_index = {key: i for i, key in enumerate(s5)}

    triple_bans = {}

    def bans(tri):
        tri = tuple(sorted(tri))
        got = triple_bans.get(tri)
        if got is None:
            got = {
                z for z in range(V)
                if z not in tri and forbidden(tri[0], tri[1], tri[2], z)
            }
            triple_bans[tri] = got
        return got

    parents = defaultdict(set)
    for key in s5:
        occ = decode(key)
        bad = set()
        for tri in itertools.combinations(sorted(occ), 3):
            bad.update(bans(tri))
        for z in range(V):
            if z in occ or z in bad:
                continue
            child = d4_canonical_key(list(occ | {z}))
            parents[child].add(s5_index[key])

    assert len(parents) == 81999
    assert min(map(len, parents.values())) == 2
    assert max(map(len, parents.values())) == 5

    children = sorted(parents)
    sets = [parents[ch] for ch in children]
    inv = [[] for _ in s5]
    degree = [0] * len(s5)
    for j, ss in enumerate(sets):
        for i in ss:
            inv[i].append(j)
            degree[i] += 1

    # Seeded tie-breaking makes the constructive upper bound reproducible.
    # Primary objective is ordinary greedy set cover gain.  On equal gain,
    # prioritize a set containing the currently lowest-degree parent, then a
    # fixed pseudo-random priority.  This is heuristic: 847 is not claimed
    # globally minimal.
    rng = random.Random(52)
    priority = [rng.random() for _ in children]
    uncovered = [True] * len(s5)
    remaining = len(s5)
    version = [0] * len(children)

    def heap_key(j):
        live = [i for i in sets[j] if uncovered[i]]
        gain = len(live)
        min_degree = min((degree[i] for i in live), default=10**9)
        lo, hi = children[j]
        return (-gain, min_degree, priority[j], lo, hi, j)

    heap = []
    for j in range(len(children)):
        heapq.heappush(heap, (*heap_key(j), 0))

    chosen = []
    while remaining:
        *stored, seen_version = heapq.heappop(heap)
        j = stored[-1]
        if seen_version != version[j]:
            continue
        current = heap_key(j)
        if tuple(stored) != current:
            version[j] += 1
            heapq.heappush(heap, (*current, version[j]))
            continue
        gain = -current[0]
        assert gain > 0
        chosen.append(j)
        for i in sets[j]:
            if not uncovered[i]:
                continue
            uncovered[i] = False
            remaining -= 1
            for q in inv[i]:
                version[q] += 1
                heapq.heappush(heap, (*heap_key(q), version[q]))

    assert len(chosen) == 847
    covered = set()
    size_hist = defaultdict(int)
    for j in chosen:
        covered.update(sets[j])
        size_hist[len(sets[j])] += 1
    assert len(covered) == len(s5) == 2262
    assert dict(size_hist) == {5: 72, 4: 15, 3: 425, 2: 335}

    out = {
        "s5_targets": len(s5),
        "unique_s6": len(children),
        "max_distinct_parents_per_s6": 5,
        "structural_cover_size": len(chosen),
        "trivial_capacity_lower_bound": (len(s5) + 4) // 5,
        "selected_parent_size_histogram": dict(sorted(size_hist.items())),
        "selected_total_parent_incidence": sum(len(sets[j]) for j in chosen),
        "seed": 52,
        "claim": "outcome-blind constructive s6 child cover; no s6 verdict claim",
    }
    print(json.dumps(out, indent=2, sort_keys=True))
    print("REPLY27_S6_STRUCTURAL_COVER_VERIFIED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
