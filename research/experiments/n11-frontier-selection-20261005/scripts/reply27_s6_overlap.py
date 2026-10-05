#!/usr/bin/env python3
"""Measure exact s6 sharing below the reply-27 direct-union s5 frontier."""
from __future__ import annotations

import itertools
import json
import sys
from collections import Counter, defaultdict
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

    # Expand exactly the selected 31 classes.
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
    assert len(s5) == doc["selected_unique_s5"] == 2262

    # Cache, for every triple that actually occurs, the points that would
    # complete a forbidden quadruple with it.  This preserves exact geometry
    # while avoiding a fresh 4-subset scan for every target/candidate.
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

    multiplicity = Counter()
    legal_counts = []
    total = 0
    for key in s5:
        occ = decode(key)
        assert len(occ) == 5
        bad = set()
        for tri in itertools.combinations(sorted(occ), 3):
            bad.update(bans(tri))
        legal = [z for z in range(V) if z not in occ and z not in bad]
        legal_counts.append(len(legal))
        total += len(legal)
        for z in legal:
            child = d4_canonical_key(list(occ | {z}))
            multiplicity[child] += 1

    unique = len(multiplicity)
    hist = Counter(multiplicity.values())
    assert total == 206536
    assert unique == 81999
    assert hist == Counter({2: 42021, 3: 37562, 4: 2344, 6: 72})
    assert min(legal_counts) == 70
    assert max(legal_counts) == 105

    out = {
        "s5_targets": len(s5),
        "s6_incidence": total,
        "unique_s6": unique,
        "duplicate_incidence": total - unique,
        "unique_fraction": unique / total,
        "duplicate_fraction": 1.0 - unique / total,
        "s5_legal_min": min(legal_counts),
        "s5_legal_max": max(legal_counts),
        "s5_legal_mean": sum(legal_counts) / len(legal_counts),
        "s6_parent_multiplicity_histogram": dict(sorted(hist.items())),
        "s6_with_multiple_target_parents": sum(n for m, n in hist.items() if m > 1),
    }
    print(json.dumps(out, indent=2, sort_keys=True))
    print("REPLY27_S6_OVERLAP_VERIFIED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
