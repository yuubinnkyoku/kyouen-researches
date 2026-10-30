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
PRIOR_INDEPENDENT_FIRST_WIN7 = "00000000000100001000000042401008"
K0423_PROVEN_LOSS5 = "00000000000101001001010000000000"
SOLVER_TRUSTED_LOSS5_EXCLUSIONS = {
    "00000000000000001204001000100000",
    "00000000000100009000010000001000",
    "00000000000100009001000000001000",
    "00000000100000009001000000001000",
}


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


def certified_new_s8(cert, data):
    """Bind the S7 witness labels to the independently checked S8 certificate.

    This is a provenance check, not a substitute for verify.py/verify.js
    recomputing the terminal S10 leaves.
    """
    require(cert["schema"] == data["sourceFixed37"] ==
            "n11-fixed14-37-s8-direct-terminal-v1" and
            cert["board"] == 11 and cert["emptyBoard"] == "UNKNOWN",
            "unexpected S8 certificate provenance")
    require(len(cert["rows"]) == 37, "wrong certified S8 root count")
    seen, losses, wins = set(), set(), set()
    for key, verdict, _ in cert["rows"]:
        pp = points(key)
        require(key not in seen and len(pp) == 8 and
                canonical(pp) == key and safe(pp),
                "duplicate, unsafe, or noncanonical certified S8 root")
        require(verdict in ("W", "L"), "invalid certified S8 verdict")
        seen.add(key)
        (wins if verdict == "W" else losses).add(key)
    require(len(wins) == data["newWin8"] == 8 and
            len(losses) == data["newLoss8"] == 29 and
            not (wins & losses), "certified S8 WIN/LOSS inventory mismatch")
    return losses, wins


def audit(data, frozen, cert):
    require(data["schema"] == "n11-fixed14-direct37-s7-lift-v1",
            "unexpected lift schema")
    require(data["emptyBoard"] == "UNKNOWN" and
            data["winLossConflicts"] == 0, "lift status/conflict")
    loss8, win8 = certified_new_s8(cert, data)
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
        certified_loss_children = kids & loss8
        require(len(certified_loss_children) <= r["knownLoss8Children"],
                "certified LOSS8 exceeds claimed S7 count " + key)
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
            require(r["witness"] in certified_loss_children and
                    r["witness"] not in win8,
                    "S7 witness has no certified LOSS8 provenance " + key)
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
    prior = points(PRIOR_INDEPENDENT_FIRST_WIN7)
    require(len(prior) == 7 and safe(prior) and
            canonical(prior) == PRIOR_INDEPENDENT_FIRST_WIN7,
            "invalid 2026-10-26 independently proven first-WIN S7 root")
    prior6 = parents([PRIOR_INDEPENDENT_FIRST_WIN7])
    require(len(prior6) == 7 and not (prior6 & (old6 | new6)),
            "2026-10-26 S6 witness overlap changed")
    combined6 = old6 | new6 | prior6
    combined5 = parents(combined6)
    require(len(combined6) == 117 and len(combined5) == 318,
            "combined S6/S5 inventory changed")
    records = []
    for five in combined5:
        legal6 = children(points(five))
        covered = legal6 & combined6
        records.append((len(legal6) - len(covered), five,
                        len(legal6), len(covered), legal6 - covered))
    records.sort()
    require(len(records) == 318 and records[0][:4] ==
            (14, K0423_PROVEN_LOSS5, 17, 3),
            "unfiltered S5 boundary changed")
    filtered = [r for r in records if r[1] != K0423_PROVEN_LOSS5 and
                r[1] not in SOLVER_TRUSTED_LOSS5_EXCLUSIONS]
    require(len(filtered) == 313 and filtered[0][:4] ==
            (25, "00000000000000821080000000000020", 32, 7),
            "S5 evidence-aware shortlist changed")
    def summarize(rows):
        distinct = set().union(*(r[4] for r in rows))
        return (len(rows), sum(r[2] for r in rows),
                sum(r[3] for r in rows), sum(r[0] for r in rows),
                len(distinct))
    require(summarize(records) == (318, 28278, 696, 27582, 26994) and
            summarize(filtered) == (313, 27919, 685, 27234, 26654),
            "S5 incidence totals changed")
    require(all(r[0] > 0 for r in filtered),
            "partial S6 coverage misreported as S5 WIN proof")
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
        "additional20261026IndependentS6WinClasses": len(prior6),
        "threeSourceS6WinClasses": len(combined6),
        "threeSourceS5IncidentClasses": len(combined5),
        "threeSourceS5LegalEdges": 28278,
        "threeSourceS5SecuredEdges": 696,
        "threeSourceS5UncoveredEdges": 27582,
        "K0423ProvenLossS5Excluded": 1,
        "solverTrustedLossS5ExcludedForScheduling": 4,
        "filteredS5CandidateClasses": len(filtered),
        "filteredS5LegalEdges": 27919,
        "filteredS5SecuredEdges": 685,
        "filteredS5UncoveredEdges": 27234,
        "filteredS5DistinctUncoveredS6": 26654,
        "filteredMinimumUncoveredS6Children": filtered[0][0],
        "closestUnexcludedS5": {"key": filtered[0][1],
                                "legalS6": filtered[0][2],
                                "coveredS6": filtered[0][3],
                                "uncoveredS6": filtered[0][0]},
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
    cert = json.loads((HERE / "certificate.json").read_text())
    result = audit(data, frozen, cert)
    # Negative controls must actually exercise the audit.
    import copy
    # A *legal* S8 child with an independently certified WIN8 verdict
    # used to pass the old audit as a false LOSS8 witness.
    legal_but_wrong = "00000000000000821080000001040120"
    require(legal_but_wrong in certified_new_s8(cert, data)[1] and
            legal_but_wrong in children(points(data["rows"][0]["s7"])),
            "false-green fixture is no longer a legal WIN8 child")
    for field, value in (("verdict", "LOSS"),
                         ("legal8", data["rows"][0]["legal8"] + 1),
                         ("witness", "0"*32),
                         ("witness", legal_but_wrong)):
        altered = copy.deepcopy(data)
        altered["rows"][0][field] = value
        try:
            audit(altered, frozen, cert)
        except ValueError:
            pass
        else:
            raise AssertionError("mutated S7 " + field + " was accepted")
    altered_cert = copy.deepcopy(cert)
    altered_cert["rows"][0][1] = "L"
    try:
        audit(data, frozen, altered_cert)
    except ValueError:
        pass
    else:
        raise AssertionError("mutated S8 certificate verdict was accepted")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
