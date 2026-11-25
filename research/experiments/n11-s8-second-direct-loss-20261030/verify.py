#!/usr/bin/env python3
"""Independent Python terminal proof of a second N11 LOSS8 position.

No JS geometry, solver cache, proof numbers, or partial df-pn verdicts.
The selected 18 leaves suffice; --full separately replays all 423 S10 leaves.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "n11-s9-full-child-top20-loss9-20261030"))
import verify_python as g  # independent Python 3x3 determinant and terminal recursion


def read(name):
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def verify(cert, full=None):
    assert cert["schema"] == "n11-s8-second-direct-loss-18-witness-v1"
    assert cert["board"] == 11 and cert["emptyBoard"] == "UNKNOWN"
    assert cert["verdict"] == "LOSS"
    root = cert["root"]
    b = int(root, 16)
    assert len(g.points(b)) == 8 and g.canonical(b) == b
    s9 = g.children(b)
    assert len(s9) == cert["legal9"] == 35

    incidence = {}
    for parent in s9:
        assert len(g.points(int(parent, 16))) == 9
        for leaf in g.children(int(parent, 16)):
            incidence.setdefault(leaf, set()).add(parent)
    assert len(incidence) == cert["distinct10"] == 423
    assert all(len(parents) == 2 for parents in incidence.values())

    witnesses = cert["witnesses"]
    assert len(witnesses) == cert["selectedLoss10"] == 18
    covered = set()
    used = set()
    states = 0
    for row in witnesses:
        h = row["s10"]
        assert h in incidence and h not in used
        used.add(h)
        assert len(g.points(int(h, 16))) == 10 and g.canonical(int(h, 16)) == int(h, 16)
        verdict, count, moves = g.solve10(h)
        assert verdict is False, "false LOSS10 witness " + h
        assert count == row["terminalStates"] and moves == row["legalMoves"]
        states += count
        covered.update(incidence[h])
    assert covered == set(s9)
    assert states == cert["terminalStatesPerGeometry"] == 2925

    s7 = sorted({f"{g.canonical(b ^ (1 << pt)):032x}" for pt in g.points(b)})
    assert len(s7) == 8 and s7 == cert["s7Parents"]
    for parent in s7:
        assert root in g.children(int(parent, 16))

    result = {"verified": True, "s8": root, "s8Verdict": "LOSS",
              "legal9": len(s9), "selectedLoss10": len(used),
              "terminalStatesPerGeometry": states,
              "derivedS7Parents": len(s7), "emptyBoard": "UNKNOWN"}
    if full is not None:
        assert full["schema"] == "n11-s8-second-full-loss10-closure-v1"
        assert full["board"] == 11 and full["emptyBoard"] == "UNKNOWN"
        assert full["root"] == root and full["distinct10"] == len(incidence)
        losses = []
        wins = 0
        total = 0
        for h in sorted(incidence):
            verdict, count, _ = g.solve10(h)
            total += count
            if verdict:
                wins += 1
            else:
                losses.append(h)
        assert wins == full["win10"] == 326
        assert len(losses) == full["loss10"] == 97
        assert total == full["terminalStatesPerGeometry"] == 46329
        assert losses == full["loss10Keys"]
        parents = set()
        for h in losses:
            leaf = int(h, 16)
            for pt in g.points(leaf):
                parent = f"{g.canonical(leaf ^ (1 << pt)):032x}"
                assert h in g.children(int(parent, 16))
                parents.add(parent)
        assert len(parents) == 811
        assert sorted(parents) == full["loss9ParentKeys"]
        result["fullScan"] = {"win10": wins, "loss10": len(losses),
                              "loss9Parents": len(parents),
                              "terminalStatesPerGeometry": total}
    return result


def negative(cert):
    def expect_reject(mutate):
        forged = json.loads(json.dumps(cert))
        mutate(forged)
        try:
            verify(forged)
        except (AssertionError, KeyError, IndexError, ValueError):
            pass
        else:
            raise AssertionError("forged LOSS8 certificate accepted")

    expect_reject(lambda x: x["witnesses"].pop())
    expect_reject(lambda x: x["witnesses"][0].update(s10=x["witnesses"][1]["s10"]))
    expect_reject(lambda x: x["witnesses"][0].update(
        terminalStates=x["witnesses"][0]["terminalStates"] + 1))
    expect_reject(lambda x: x["witnesses"][0].update(
        legalMoves=x["witnesses"][0]["legalMoves"] + 1))
    expect_reject(lambda x: x.update(root="0" * 32))
    expect_reject(lambda x: x["s7Parents"].pop())
    expect_reject(lambda x: x.update(emptyBoard="WIN"))


if __name__ == "__main__":
    cert = read("certificate.json")
    full = read("full_loss_closure.json") if "--full" in sys.argv else None
    report = verify(cert, full)
    if "--negative" in sys.argv:
        negative(cert)
    print(json.dumps(report, indent=2))
