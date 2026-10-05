#!/usr/bin/env python3
"""Audit the C++ coordinator's initial greedy r2=0 cover against direct-union.

Rebuilds all geometry from the board rule.  It does not trust stored class
coverage or s5 counts.  The verdict state is deliberately the K0329 frontier
used by direct-union-cover.json: two proved LOSS classes, one proved WIN class,
everything else UNKNOWN.
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EDGE_DIR = ROOT / "research/experiments/n11-search-methods/scripts"
sys.path.insert(0, str(EDGE_DIR))

from dfpn_edge_classes import d4_canonical_key, legal_after  # noqa: E402

HERE = Path(__file__).resolve().parents[1]
DIRECT = HERE / "output/direct-union-cover.json"


def build(first=60, r2=0):
    base = {first, r2}
    verts = legal_after(base)
    groups = defaultdict(list)
    for a in verts:
        for b in legal_after(base | {a}):
            if b <= a:
                continue
            groups[d4_canonical_key([first, r2, a, b])].append((a, b))
    coverage = {
        key: {x for edge in edges for x in edge}
        for key, edges in groups.items()
    }
    return base, verts, groups, coverage


def child_keys(base, edges):
    out = set()
    for a, b in edges:
        occ = base | {a, b}
        for z in legal_after(occ):
            out.add(d4_canonical_key(list(occ | {z})))
    return out


def cpp_greedy(keys, coverage, verdict):
    """Exact reproduction of DfPn::coordinate's selection/tie behavior."""
    covered = set()
    used = set()
    members = []
    while True:
        best = None
        best_cost = 99
        best_fresh = 0
        for i, key in enumerate(keys):
            if i in used or verdict.get(key) == "WIN":
                continue
            cost = 0 if verdict.get(key) == "LOSS" else 1
            fresh = len(coverage[key] - covered)
            if not fresh:
                continue
            if fresh > best_fresh or (fresh == best_fresh and cost < best_cost):
                best = i
                best_cost = cost
                best_fresh = fresh
        if best is None:
            break
        used.add(best)
        key = keys[best]
        members.append(key)
        covered.update(coverage[key])
    return members, covered


def main():
    doc = json.loads(DIRECT.read_text(encoding="utf-8"))
    base, verts, groups, coverage = build()
    assert len(verts) == 119
    assert len(groups) == 3396

    loss = {tuple(x) for x in doc["forced_known_loss_keys"]}
    win = tuple(doc["forbidden_known_win_key"])
    verdict = {key: "LOSS" for key in loss}
    verdict[win] = "WIN"

    keys = sorted(groups)  # std::map iteration order in the C++ coordinator
    greedy, got = cpp_greedy(keys, coverage, verdict)
    assert got == set(verts)

    direct = [tuple(row["key"]) for row in doc["selected"]]
    assert len(direct) == 31
    assert set().union(*(coverage[k] for k in direct)) == set(verts)

    needed = set(greedy) | set(direct) | loss
    children = {k: child_keys(base, groups[k]) for k in needed}
    known = set().union(*(children[k] for k in loss))
    greedy_union = set().union(*(children[k] for k in greedy))
    direct_union = set().union(*(children[k] for k in direct))

    out = {
        "all_classes": len(groups),
        "vertices": len(verts),
        "known_loss_s5": len(known),
        "cpp_greedy_classes": len(greedy),
        "cpp_greedy_unique_s5": len(greedy_union),
        "cpp_greedy_unknown_unique_s5": len(greedy_union - known),
        "direct_union_classes": len(direct),
        "direct_union_unique_s5": len(direct_union),
        "direct_union_unknown_unique_s5": len(direct_union - known),
        "extra_unknown_s5_in_cpp_greedy":
            len(greedy_union - known) - len(direct_union - known),
        "cpp_greedy_over_direct_fraction":
            (len(greedy_union - known) / len(direct_union - known) - 1.0),
        "claim":
            "initial-skeleton audit only; no game verdict is inferred",
    }

    assert out["known_loss_s5"] == 209
    assert out["cpp_greedy_classes"] == 35
    assert out["cpp_greedy_unique_s5"] == 3806
    assert out["cpp_greedy_unknown_unique_s5"] == 3597
    assert out["direct_union_unique_s5"] == 2528
    assert out["direct_union_unknown_unique_s5"] == 2319
    assert out["extra_unknown_s5_in_cpp_greedy"] == 1278

    print(json.dumps(out, indent=2, sort_keys=True))
    print("COORDINATOR_FRONTIER_AUDIT_VERIFIED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
