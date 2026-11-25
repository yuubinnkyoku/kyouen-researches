#!/usr/bin/env python3
"""One bounded, cache-free S9 terminal probe chosen by the fixed14 frontier.

Only the minimum-residual S8 parent's cheapest S9 child is examined. A
completed terminal proof is printed; a timeout is never a verdict.
"""
import hashlib
import json
from pathlib import Path
import verify_python as geometry
from verify_full_incidence import historical_claims, new_claims

HERE = Path(__file__).resolve().parent


def run():
    plan = json.loads((HERE / "post_top20_frontier.json").read_text())
    cert = json.loads((HERE / "certificate.json").read_text())
    assert plan["emptyBoard"] == "UNKNOWN"
    assert plan["unknown9After"] == 750 and plan["unknownEdgesAfter"] == 760
    chosen = plan["targetS9ChildrenBySmallestS10Boundary"][0]
    s9 = chosen["s9"]
    old_wins, old_losses = historical_claims()
    assert s9 not in old_wins and s9 not in old_losses
    assert s9 not in new_claims(cert)
    children = geometry.children(int(s9, 16))
    assert len(children) == chosen["legal10"]
    tested = []
    for i, child in enumerate(children):
        verdict, states, legal = geometry.solve10(child)
        tested.append({"index": i, "s10": child, "s10Win": verdict,
                       "terminalStates": states, "s10LegalMoves": legal})
        if not verdict:
            leaf = int(child, 16)
            closure = sorted({f"{geometry.canonical(leaf ^ (1 << p)):032x}"
                              for p in geometry.points(leaf)})
            result = {
                "schema": "n11-fixed14-post-top20-one-s9-terminal-v1",
                "emptyBoard": "UNKNOWN",
                "s9": s9,
                "s9Verdict": "LOSS",
                "s10Children": len(children),
                "testedS10": tested,
                "loss10WitnessIndex": i,
                "loss9ParentClosure": len(closure),
                "loss9ParentSha256": hashlib.sha256(
                    ("\n".join(closure) + "\n").encode()).hexdigest(),
                "twoStoneRootClosed": False,
            }
            print(json.dumps(result, indent=2))
            return result
    result = {
        "schema": "n11-fixed14-post-top20-one-s9-terminal-v1",
        "emptyBoard": "UNKNOWN",
        "s9": s9,
        "s9Verdict": "WIN",
        "s10Children": len(children),
        "testedS10": tested,
        "twoStoneRootClosed": False,
    }
    print(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    run()
