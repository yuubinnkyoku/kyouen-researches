#!/usr/bin/env python3
"""Independent exact 11x11 LOSS8 certificate: 18 LOSS10 leaves cover 36 S9 moves."""
import hashlib
import json
from collections import defaultdict
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'n11-s9-full-child-top20-loss9-20261030'))
import verify_python as g

HERE = Path(__file__).resolve().parent

def verify(c):
    assert c["schema"] == "n11-s8-loss-perfect-matching-v1"
    assert c["board"] == 11 and c["emptyBoard"] == "UNKNOWN"
    assert c["s8Verdict"] == "LOSS"
    root = int(c["s8"], 16)
    assert len(g.points(root)) == 8 and g.canonical(root) == root
    s9 = g.children(root)
    assert len(s9) == c["s9LegalCount"] == 36
    incidence = defaultdict(set)
    for i, h in enumerate(s9):
        for child in g.children(int(h, 16)):
            incidence[child].add(i)
    assert len(incidence) == c["s10BoundaryDistinct"] == 480
    assert all(len(v) == c["s10ParentDegree"] == 2 for v in incidence.values())
    selected = c["s10Witnesses"]
    assert len(selected) == c["selectedLossLeaves"] == 18
    assert len({x["s10"] for x in selected}) == len(selected)
    covered = set()
    total_states = 0
    for row in selected:
        h = row["s10"]
        assert h in incidence
        assert not (covered & incidence[h]), "overlapping matching edges"
        verdict, states, legal = g.solve10(h)
        assert not verdict, "false LOSS10 terminal witness: " + h
        assert states == row["terminalStates"] and legal == row["legalMoves"]
        covered.update(incidence[h])
        total_states += states
    assert covered == set(range(len(s9))), "incomplete universal S9 boundary"
    assert total_states == c["selectedTerminalStates"] == 5240
    parents = sorted({f"{g.canonical(root ^ (1 << p)):032x}" for p in g.points(root)})
    assert len(parents) == c["s7ParentCount"] == 8
    for h in parents:
        assert c["s8"] in g.children(int(h, 16))
    digest = hashlib.sha256((chr(10).join(parents) + chr(10)).encode()).hexdigest()
    assert digest == c["s7ParentSha256"]
    return {"verified": True, "language": "Python", "s8": c["s8"],
            "s8Verdict": "LOSS", "s9AllChildren": len(s9),
            "loss10Witnesses": len(selected), "terminalStates": total_states,
            "derivedS7LossParents": len(parents), "emptyBoard": "UNKNOWN"}

def negative(c):
    def reject(label, change):
        forged = json.loads(json.dumps(c))
        change(forged)
        try:
            verify(forged)
        except (AssertionError, KeyError, ValueError, IndexError):
            return
        raise AssertionError("forged proof accepted: " + label)
    reject("wrong terminal", lambda x: x["s10Witnesses"][0].update(
        s10=x["s10Witnesses"][1]["s10"]))
    reject("wrong state count", lambda x: x["s10Witnesses"][0].update(
        terminalStates=0))
    reject("wrong legal count", lambda x: x["s10Witnesses"][0].update(
        legalMoves=0))
    reject("missing edge", lambda x: x["s10Witnesses"].pop())
    reject("wrong root", lambda x: x.update(s8="0" * 32))
    reject("wrong parent digest", lambda x: x.update(s7ParentSha256="0" * 64))

if __name__ == "__main__":
    import sys
    cert = json.loads((HERE / "certificate.json").read_text())
    result = verify(cert)
    if "--negative" in sys.argv:
        negative(cert)
    print(json.dumps(result, indent=2))
