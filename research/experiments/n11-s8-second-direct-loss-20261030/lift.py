#!/usr/bin/env python3
"""Reconstruct fixed14 frontier from sealed historical proofs and both full S10 closures.

This is a proof-only audit, not an assertion that the remaining S8/S2 roots are solved.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
sys.path.insert(0, str(EXP / "n11-s9-full-child-top20-loss9-20261030"))
sys.path.insert(0, str(EXP / "n11-s8-direct-loss-perfect-matching-20261030"))
from verify_full_incidence import historical_claims, new_claims
from verify_single import verify_terminal
from audit_full_loss_closure import verify_manifest
import verify_python as g
sys.path.insert(0, str(HERE))
from verify import verify as verify_new


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def run():
    top = EXP / "n11-s9-full-child-top20-loss9-20261030"
    previous = EXP / "n11-s8-direct-loss-perfect-matching-20261030"
    old_wins, old_losses = historical_claims()
    top20 = new_claims(read(top / "certificate.json"))
    single = verify_terminal(read(top / "single_s9_certificate.json"),
                             read(top / "post_top20_frontier.json"))
    first81, old_states = verify_manifest(read(previous / "full_loss_closure.json"))
    assert old_states == 20997 and len(first81) == 684
    known = old_losses | top20 | single | first81
    assert not old_wins.intersection(known)
    assert len(old_wins) == 56

    new_cert = read(HERE / "certificate.json")
    new_full = read(HERE / "full_loss_closure.json")
    new_proof = verify_new(new_cert, new_full)
    assert new_proof["s8Verdict"] == "LOSS"
    assert new_proof["fullScan"]["loss9Parents"] == 811
    fresh = set(new_full["loss9ParentKeys"]) - known
    assert not old_wins.intersection(fresh), "WIN9/LOSS9 conflict"

    audit = read(EXP / "n11-s8-complete-child-audit-20261030" / "incidence.json")
    before, after = set(), set()
    before_edges = after_edges = 0
    closed_before, closed_after, changed = [], [], []
    for row in audit["s8Rows"]:
        children = set(g.children(int(row["h"], 16)))
        assert len(children) == row["legal9"]
        assert not children.intersection(old_wins)
        unknown_before = children - known
        unknown_after = unknown_before - fresh
        before.update(unknown_before)
        after.update(unknown_after)
        before_edges += len(unknown_before)
        after_edges += len(unknown_after)
        if not unknown_before:
            closed_before.append(row["h"])
        if not unknown_after:
            closed_after.append(row["h"])
        if len(unknown_after) != len(unknown_before):
            changed.append({"s8": row["h"], "unknownBefore": len(unknown_before),
                            "newLoss9Edges": len(unknown_before) - len(unknown_after),
                            "unknownAfter": len(unknown_after)})
    assert len(before) == 728 and before_edges == 736, "prior frontier changed"
    assert closed_before == ["00012010000000821080000000000020"]
    assert new_cert["root"] in closed_after and len(closed_after) >= 2
    assert before_edges - after_edges == sum(x["newLoss9Edges"] for x in changed)
    report = {
        "schema": "n11-second-loss8-full97-fixed14-frontier-v1",
        "emptyBoard": "UNKNOWN",
        "historicalWin9": len(old_wins),
        "priorKnownLoss9": len(known),
        "newLoss10": 97,
        "newLoss9ParentClosure": 811,
        "newLoss9BeyondPriorProofSets": len(fresh),
        "unknown9Before": len(before),
        "unknown9After": len(after),
        "unknownEdgesBefore": before_edges,
        "unknownEdgesAfter": after_edges,
        "newlyCertifiedLossEdges": before_edges - after_edges,
        "closedS8Before": closed_before,
        "closedS8After": closed_after,
        "remainingUnprovedS8Of37": 37 - len(closed_after),
        "winLossConflicts": 0,
        "twoStoneRootClosureChecked": False,
        "changedRows": changed,
    }
    frozen = HERE / "frontier_result.json"
    if frozen.exists():
        assert report == read(frozen), "fixed frontier report mismatch"
    print(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    run()
