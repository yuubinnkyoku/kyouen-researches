#!/usr/bin/env python3
"""Independent Python replay of one post-top20 S9 terminal certificate and S8 lift."""
import hashlib
import json
from collections import defaultdict
from pathlib import Path

import verify_python as g
from verify_full_incidence import historical_claims, new_claims

HERE = Path(__file__).resolve().parent
EXP = HERE.parent


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def verify_terminal(cert, plan):
    assert cert["schema"] == "n11-fixed14-post-top20-one-s9-terminal-v1"
    assert cert["emptyBoard"] == "UNKNOWN" and cert["s9Verdict"] == "LOSS"
    assert cert["twoStoneRootClosed"] is False
    target = plan["targetS9ChildrenBySmallestS10Boundary"][0]
    assert target["s9"] == cert["s9"]
    children = g.children(int(cert["s9"], 16))
    assert len(children) == target["legal10"] == cert["s10Children"]
    assert len(cert["testedS10"]) == cert["loss10WitnessIndex"] + 1
    for i, row in enumerate(cert["testedS10"]):
        assert row["index"] == i and row["s10"] == children[i]
        outcome, states, legal = g.solve10(row["s10"])
        assert outcome == row["s10Win"] == (i < cert["loss10WitnessIndex"])
        assert states == row["terminalStates"]
        assert legal == row["s10LegalMoves"]
    leaf = int(children[cert["loss10WitnessIndex"]], 16)
    closure = {f"{g.canonical(leaf ^ (1 << pt)):032x}"
               for pt in g.points(leaf)}
    assert cert["s9"] in closure
    assert len(closure) == cert["loss9ParentClosure"]
    assert hashlib.sha256(("\n".join(sorted(closure)) + "\n").encode()).hexdigest() == cert["loss9ParentSha256"]
    return closure


def run():
    cert = load(HERE / "single_s9_certificate.json")
    plan = load(HERE / "post_top20_frontier.json")
    old_audit = load(EXP / "n11-s8-complete-child-audit-20261030" / "incidence.json")
    top20 = load(HERE / "certificate.json")
    assert plan["unknown9After"] == 750 and plan["unknownEdgesAfter"] == 760
    closure = verify_terminal(cert, plan)
    old_wins, old_losses = historical_claims()
    top20_losses = new_claims(top20)
    assert not closure.intersection(old_wins)
    known = old_losses | top20_losses
    fresh = closure - known
    rows = []
    newly_closed = []
    old_unknowns, new_unknowns = set(), set()
    new_edges = 0
    for old_row in old_audit["s8Rows"]:
        kids = set(g.children(int(old_row["h"], 16)))
        assert len(kids) == old_row["legal9"]
        unknown_before = kids - known
        unknown_after = unknown_before - fresh
        assert not kids.intersection(old_wins)
        old_unknowns.update(unknown_before)
        new_unknowns.update(unknown_after)
        added = len(unknown_before) - len(unknown_after)
        new_edges += added
        if not unknown_after:
            newly_closed.append(old_row["h"])
        rows.append((old_row["h"], len(unknown_before), len(unknown_after), added))
    assert len(old_unknowns) == 750 and sum(x[1] for x in rows) == 760
    assert len(rows) == 37
    assert not newly_closed or all(x[2] == 0 for x in rows if x[0] in newly_closed)
    result = {
        "schema": "n11-fixed14-post-top20-one-s9-proof-lift-v1",
        "emptyBoard": "UNKNOWN",
        "s9Verdict": "LOSS",
        "s9": cert["s9"],
        "loss9ParentClosure": len(closure),
        "newDistinctLoss9": len(fresh),
        "newCertifiedLoss9Edges": new_edges,
        "unknown9Before": len(old_unknowns),
        "unknown9After": len(new_unknowns),
        "unknownEdgesBefore": 760,
        "unknownEdgesAfter": sum(x[2] for x in rows),
        "newlyClosedLoss8": len(newly_closed),
        "newlyClosedLoss8Keys": newly_closed,
        "winLossConflicts": 0,
        "newTwoStoneClosures": 0,
    }
    fixed = HERE / "single_s9_result.json"
    if fixed.exists():
        assert result == load(fixed), "frozen single S9 proof delta mismatch"
    print(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    import sys
    if "--negative" in sys.argv:
        original = load(HERE / "single_s9_certificate.json")
        plan = load(HERE / "post_top20_frontier.json")
        for mutation in (
            lambda c: c["testedS10"][-1].update(s10Win=True),
            lambda c: c["testedS10"][-1].update(terminalStates=0),
            lambda c: c.update(loss10WitnessIndex=255),
            lambda c: c.update(loss9ParentSha256="0" * 64),
            lambda c: c.update(s9="0" * 32),
        ):
            forged = json.loads(json.dumps(original))
            mutation(forged)
            try:
                verify_terminal(forged, plan)
            except (AssertionError, IndexError, KeyError, ValueError):
                continue
            raise AssertionError("forged terminal certificate accepted")
    run()
