#!/usr/bin/env python3
"""Reproduce the exploratory full S10 boundary classification (not needed by proof)."""
import json
from collections import Counter
from pathlib import Path
from verify import g, verify

HERE = Path(__file__).resolve().parent

def run():
    cert = json.loads((HERE / "certificate.json").read_text())
    proof = verify(cert)
    s9 = g.children(int(cert["s8"], 16))
    incidence = Counter(k for h in s9 for k in g.children(int(h, 16)))
    assert len(incidence) == 480 and sum(incidence.values()) == 960
    assert set(incidence.values()) == {2}
    losses = wins = 0
    for h in sorted(incidence):
        result, _, _ = g.solve10(h)
        wins += result
        losses += not result
    report = {"schema": "n11-s8-loss-full-s10-scan-v1",
              "s8": cert["s8"], "s8Verdict": proof["s8Verdict"],
              "legal9": len(s9), "legal10Edges": sum(incidence.values()),
              "distinct10": len(incidence), "win10": wins, "loss10": losses,
              "selectedLoss10": len(cert["s10Witnesses"]),
              "selectedTerminalStates": proof["terminalStates"],
              "emptyBoard": "UNKNOWN"}
    frozen = json.loads((HERE / "full_boundary_scan.json").read_text())
    assert report == frozen, "full boundary scan changed"
    print(json.dumps(report, indent=2))
    return report

if __name__ == "__main__":
    run()
