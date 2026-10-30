#!/usr/bin/env python3
"""Audit the fixed14 S7 verdict perspective and newly secured S6 witnesses.

The frozen lift_result.json labels S7 WIN/LOSS for the player *to move*.
At odd ply S7, that player is the second player, so these labels are the
opposite of the fixed-original-first convention used by older S7 proofs.
This is an incidence/polarity audit, NOT an independent S8 terminal solver.
"""
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASELINE = HERE.parent / "n11-targeted-terminal-lift-20261015" / "data" / "all_s7_win_17.txt"
BASELINE_SHA256 = "17282f84fd65ad20ac58ef794449a52bcc796d8129a1a3a58d726a305fbeb21e"
KNOWN_S6_LOSS = "00000000040004001004000004010000"
EXPECTED_FIRST_WIN7 = "00020000000000821080200000000020"


def require(ok, why):
    if not ok:
        raise ValueError(why)


def points(key):
    mask = int(key, 16)
    require(mask >> 121 == 0, "mask exceeds 11x11")
    return tuple(i for i in range(121) if (mask >> i) & 1)


def canonical(indices):
    variants = []
    for mode in range(8):
        mask = 0
        for i in indices:
            x, y = i % 11, i // 11
            a, b = ((x, y), (10-y, x), (10-x, 10-y), (y, 10-x),
                    (10-x, y), (10-y, 10-x), (x, 10-y), (y, x))[mode]
            mask |= 1 << (11*b + a)
        variants.append(mask)
    return f"{min(variants):032x}"


def forbidden(q):
    xy = [(i % 11, i // 11) for i in q]
    x, y = xy[3]
    a, b, c = [(u-x, v-y, u*u+v*v-x*x-y*y) for u, v in xy[:3]]
    return (a[0]*(b[1]*c[2]-b[2]*c[1])
            - a[1]*(b[0]*c[2]-b[2]*c[0])
            + a[2]*(b[0]*c[1]-b[1]*c[0])) == 0


def safe(indices):
    return not any(forbidden(q) for q in itertools.combinations(indices, 4))


def children(indices):
    require(safe(indices), "unsafe parent")
    return {canonical((*indices, i))
            for i in range(121) if i not in indices and safe((*indices, i))}


def parents(keys):
    return {canonical(tuple(p for p in points(h) if p != removed))
            for h in keys for removed in points(h)}


def audit(data, frozen):
    require(data["schema"] == "n11-fixed14-direct37-s7-lift-v1",
            "unexpected lift schema")
    require(data["emptyBoard"] == "UNKNOWN" and
            data["winLossConflicts"] == 0, "lift status/conflict")
    rows = data["rows"]
    require(len(rows) == 14 and len({r["s7"] for r in rows}) == 14,
            "not fourteen distinct S7 roots")
    first_win, first_loss = [], []
    for r in rows:
        key = r["s7"]
        pp = points(key)
        require(len(pp) == 7 and canonical(pp) == key and safe(pp),
                "invalid S7 board " + key)
        kids = children(pp)
        require(len(kids) == r["legal8"], "wrong legal S8 count " + key)
        losing = r["knownLoss8Children"]
        missing = r["unproved8Children"]
        require(isinstance(losing, int) and isinstance(missing, int) and
                losing >= 0 and missing == 0 and losing <= len(kids),
                "incomplete or invalid S8 coverage " + key)
        if losing:
            # S7: second player moves. One S8 first-player LOSS means
            # S7 second-player WIN, equivalently original-first LOSS.
            require(r["verdict"] == "WIN" and r["witness"] in kids,
                    "S7 side-to-move WIN witness mismatch " + key)
            first_loss.append(key)
        else:
            # Every S8 first-player WIN: second player cannot avoid losing.
            require(r["verdict"] == "LOSS" and r["witness"] is None,
                    "S7 side-to-move LOSS mismatch " + key)
            first_win.append(key)
    require((len(first_win), len(first_loss)) == (1, 13) and
            first_win == [EXPECTED_FIRST_WIN7] and
            (data["win7"], data["loss7"], data["unknown7"]) == (13, 1, 0),
            "S7 polarity regression")
    require(len(frozen) == 17 and frozen == sorted(set(frozen)),
            "historical S7 baseline malformed")
    for key in frozen:
        pp = points(key)
        require(len(pp) == 7 and canonical(pp) == key and safe(pp),
                "invalid frozen S7 root " + key)
    old6, new6 = parents(frozen), parents(first_win)
    require(len(old6) == 103 and len(new6) == 7 and not (old6 & new6),
            "S6 baseline/new witness overlap changed")
    require(KNOWN_S6_LOSS not in new6, "known S6 LOSS conflict")
    for six in new6:
        require(EXPECTED_FIRST_WIN7 in children(points(six)),
                "S6 witness is not a legal S7 child " + six)
    old5, new5 = parents(old6), parents(new6)
    require(len(old5) == 277 and len(new5) == 21 and
            len(old5 & new5) == 1, "S5 reverse incidence changed")
    edges = {(five, six) for six in new6
             for five in parents([six])}
    require(len(edges) == 42, "S5->S6 witness edge count changed")
    return {
        "schema": "n11-fixed14-s7-polarity-s6-baseline-audit-v1",
        "source": "frozen S8 terminal certificate lift; not a new terminal proof",
        "s7VerdictPerspectiveInLift": "side-to-move (second player)",
        "s7SideToMove": {"WIN": 13, "LOSS": 1},
        "s7OriginalFirst": {"WIN": 1, "LOSS": 13},
        "originalFirstWin7": first_win,
        "oldS6WinWitnessClasses": len(old6),
        "additionalS6WinWitnessClasses": len(new6),
        "overlapS6": len(old6 & new6),
        "combinedS6WinWitnessClasses": len(old6 | new6),
        "newS6Keys": sorted(new6),
        "oldS5IncidentClasses": len(old5),
        "newS5IncidentClasses": len(new5),
        "overlapS5": len(old5 & new5),
        "newS5ClassesBeyondBaseline": len(new5 - old5),
        "combinedS5IncidentClasses": len(old5 | new5),
        "newS5ToS6WitnessEdges": len(edges),
        "newS5FullWinProofs": 0,
        "twoStoneRootClosed": False,
        "emptyBoard": "UNKNOWN",
    }


def main():
    raw = BASELINE.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == BASELINE_SHA256,
            "historical baseline SHA-256 mismatch")
    frozen = raw.decode("ascii").splitlines()
    data = json.loads((HERE / "lift_result.json").read_text())
    result = audit(data, frozen)
    # Negative controls must actually exercise the audit.
    import copy
    for field, value in (("verdict", "LOSS"),
                         ("legal8", data["rows"][0]["legal8"] + 1),
                         ("witness", "0"*32)):
        altered = copy.deepcopy(data)
        altered["rows"][0][field] = value
        try:
            audit(altered, frozen)
        except ValueError:
            pass
        else:
            raise AssertionError("mutated S7 " + field + " was accepted")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
