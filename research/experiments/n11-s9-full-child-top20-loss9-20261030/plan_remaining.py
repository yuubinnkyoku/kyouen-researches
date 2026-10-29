#!/usr/bin/env python3
"""Proof-only N11 post-top20 S8->S9 frontier audit and targeted next worklist.

Rebuilds all 19 historical certificate batches and the independently verified
top20 LOSS10 leaves. A residual S9 is UNKNOWN, never implicitly WIN or LOSS.
The shared-edge bound is combinatorial, not a game-theoretic verdict.
"""
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

import verify_python as geometry
from verify_full_incidence import historical_claims, new_claims, incidence_delta

HERE = Path(__file__).resolve().parent
EXPERIMENTS = HERE.parent


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run():
    audit_path = EXPERIMENTS / "n11-s8-complete-child-audit-20261030" / "incidence.json"
    cert_path = HERE / "certificate.json"
    result_path = HERE / "result.json"
    audit, cert, prior = map(load, (audit_path, cert_path, result_path))

    # Re-solve all 20 new terminal LOSS10 witnesses before trusting propagation.
    states, verified_parents = geometry.verify_certificate(cert)
    assert states == prior["terminalStatesPerGeometry"] == 2602
    old_wins, old_losses = historical_claims()
    new_losses = new_claims(cert)
    assert new_losses == verified_parents
    incidence_delta(audit, cert, prior, old_wins, old_losses, new_losses)
    assert not old_wins.intersection(old_losses | new_losses)

    fresh = new_losses - old_losses
    all_losses = old_losses | new_losses
    rows = []
    parents = defaultdict(list)
    old_edges = new_edges = raw_new_edges = total_edges = 0
    for row in audit["s8Rows"]:
        kids = set(geometry.children(int(row["h"], 16)))
        assert len(kids) == row["legal9"]
        assert not kids.intersection(old_wins)
        known_old = kids & old_losses
        added = kids & fresh
        raw_new = kids & new_losses
        unknown = sorted(kids - all_losses)
        assert len(known_old) == row["certifiedLoss9"]
        assert len(unknown) == row["unknown9"] - len(added)
        old_edges += len(known_old)
        new_edges += len(added)
        raw_new_edges += len(raw_new)
        total_edges += len(kids)
        for child in unknown:
            parents[child].append(row["h"])
        rows.append({
            "s8": row["h"],
            "unknownBefore": row["unknown9"],
            "newCertifiedLossEdges": len(added),
            "unknownAfter": len(unknown),
        })

    assert len(rows) == 37
    assert total_edges == 1088 and old_edges == 259
    assert new_edges == 69 and raw_new_edges == 74
    assert sum(r["unknownAfter"] for r in rows) == 760
    assert len(parents) == 750
    assert sum(r["unknownBefore"] for r in rows) == 829
    assert len(new_losses) == 192 and len(fresh) == 184

    # For any selection S of remaining distinct S9 positions, the number of
    # S8->S9 edges it covers is at most |S| + 10. This does NOT prove that
    # any candidate is WIN9 or LOSS9; it bounds only sharing opportunities.
    excess_before = 829 - 799
    excess_after = sum(len(v) - 1 for v in parents.values())
    assert excess_before == 30 and excess_after == 10
    degree_histogram = dict(sorted(Counter(map(len, parents.values())).items()))
    target = min(rows, key=lambda r: (r["unknownAfter"], r["s8"]))
    target_children = sorted(
        ({"s9": h, "legal10": len(geometry.children(int(h, 16))),
          "otherUnprovedS8Parents": len(parents[h]) - 1}
         for h, ps in parents.items() if target["s8"] in ps),
        key=lambda r: (r["legal10"], -r["otherUnprovedS8Parents"], r["s9"]),
    )
    assert len(target_children) == target["unknownAfter"]
    assert target["unknownAfter"] == min(r["unknownAfter"] for r in rows) == 11

    report = {
        "schema": "n11-fixed14-post-top20-frontier-v1",
        "emptyBoard": "UNKNOWN",
        "sourceSha256": {
            "incidence": digest(audit_path),
            "top20Certificate": digest(cert_path),
            "top20Result": digest(result_path),
        },
        "historicalWin9": len(old_wins),
        "historicalLoss9": len(old_losses),
        "newLoss9ParentClosure": len(new_losses),
        "newDistinctLoss9": len(fresh),
        "unprovedS8": len(rows),
        "unknown9Before": 799,
        "unknown9After": len(parents),
        "unknownEdgesBefore": 829,
        "unknownEdgesAfter": sum(r["unknownAfter"] for r in rows),
        "sharedEdgeExcessBefore": excess_before,
        "sharedEdgeExcessAfter": excess_after,
        "sharedEdgeExcessRemoved": excess_before - excess_after,
        "maximumAdditionalEdgesBeyondDistinctS9Certificates": excess_after,
        "remainingS9ParentDegreeHistogram": degree_histogram,
        "newLoss9EdgesOnS8Rows": new_edges,
        "rawNewLoss9EdgesIncludingPreviouslyKnown": raw_new_edges,
        "previouslyKnownOverlapEdges": raw_new_edges - new_edges,
        "minUnknownChildrenPerS8": target["unknownAfter"],
        "maxUnknownChildrenPerS8": max(r["unknownAfter"] for r in rows),
        "bestS8ByFewestUnprovedChildren": target,
        "targetS9ChildrenBySmallestS10Boundary": target_children,
        "allS8Rows": sorted(rows, key=lambda r: (r["unknownAfter"], r["s8"])),
        "newTwoStoneClosures": 0,
        "winLossConflicts": 0,
    }
    frozen = HERE / "post_top20_frontier.json"
    if frozen.exists():
        assert report == load(frozen), "frozen residual frontier mismatch"
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return report


if __name__ == "__main__":
    run()
