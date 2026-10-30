#!/usr/bin/env python3
"""Independent 4x4-integer-geometry audit of fixed14 first-LOSS S7 -> S6 edges.

The 13 S7 roots are terminal-certificate-backed by the existing fixed37
verification pipeline. This audit independently checks their reverse
incidence and legal S6->S7 boundary. The frozen 2232 S7 LOSS entries are a
HISTORICAL comparison set, not 2232 newly verified terminal certificates.
A missing child in this limited union is not a proved UNKNOWN verdict.
"""
if not __debug__:
    raise SystemExit("Refusing python -O")

import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OLD = HERE.parent / "n11-targeted-terminal-lift-20261015" / "data" / "all_s7_loss_2232.txt"
LIFT = HERE / "lift_result.json"
FROZEN_WIN7 = HERE.parent / "n11-targeted-terminal-lift-20261015" / "data" / "all_s7_win_17.txt"
OLD_BLOB = "e2b8fc243422751ce048302a3ed65df1ef7e5211"
LIFT_BLOB = "f8e335cd8fafec9d98745e89cb207d4e31c220be"
FROZEN_WIN7_BLOB = "677e962f3f70be73abcd77037df8822880927b22"
PRIOR_FIRST_WIN7 = "00000000000100001000000042401008"
MIXED_S6 = "00000000000000821080200000000020"
FIRST_WIN7 = "00020000000000821080200000000020"

def require(ok, reason):
    if not ok:
        raise ValueError(reason)

def pinned(path, expected):
    raw = path.read_bytes()
    header = ("blob " + str(len(raw)) + "\0").encode("ascii")
    require(hashlib.sha1(header + raw).hexdigest() == expected,
            "source Git blob identity changed: " + str(path))
    return raw

def points(h):
    n = int(h, 16)
    require(n >> 121 == 0, "outside 11x11")
    return tuple(i for i in range(121) if n & (1 << i))

MAPS = []
for mode in range(8):
    mapping = []
    for i in range(121):
        x, y = i % 11, i // 11
        a, b = ((x,y), (10-y,x), (10-x,10-y), (y,10-x),
                (10-x,y), (10-y,10-x), (x,10-y), (y,x))[mode]
        mapping.append(11*b+a)
    MAPS.append(mapping)

def canonical(ps):
    return f"{min(sum(1 << m[p] for p in ps) for m in MAPS):032x}"

def det4(ps):
    # Independent homogeneous 4x4 circle/line test, fraction-free Bareiss.
    m = [[(p%11)**2 + (p//11)**2, p%11, p//11, 1] for p in ps]
    prev, sign = 1, 1
    for k in range(3):
        if not m[k][k]:
            swap = next((i for i in range(k+1, 4) if m[i][k]), None)
            if swap is None:
                return 0
            m[k], m[swap] = m[swap], m[k]
            sign = -sign
        pivot = m[k][k]
        for i in range(k+1, 4):
            for j in range(k+1, 4):
                numerator = m[i][j]*pivot - m[i][k]*m[k][j]
                require(numerator % prev == 0, "Bareiss nonexact division")
                m[i][j] = numerator // prev
            m[i][k] = 0
        prev = pivot
    return sign * m[3][3]

def safe(ps):
    return all(det4(q) != 0 for q in itertools.combinations(ps, 4))

def children(six):
    ps = points(six)
    require(len(ps) == 6 and safe(ps) and canonical(ps) == six,
            "invalid canonical six-stone parent " + six)
    triples = list(itertools.combinations(ps, 3))
    occupied = set(ps)
    out = set()
    for p in range(121):
        if p in occupied:
            continue
        if all(det4((*t, p)) != 0 for t in triples):
            out.add(canonical((*ps, p)))
    return out

def audit(old, lift, frozen_win):
    require(len(old) == 2232 and old == sorted(set(old)),
            "historical S7 LOSS inventory changed")
    require(all(len(points(h)) == 7 and canonical(points(h)) == h and
                safe(points(h)) for h in old),
            "historical S7 LOSS inventory contains invalid board")
    require(lift["schema"] == "n11-fixed14-direct37-s7-lift-v1" and
            lift["emptyBoard"] == "UNKNOWN" and
            lift["winLossConflicts"] == 0 and
            (lift["win7"], lift["loss7"], lift["unknown7"]) == (13, 1, 0),
            "frozen S7 lift status changed")
    rows = lift["rows"]
    require(len(rows) == 14 and len({r["s7"] for r in rows}) == 14,
            "fixed14 root list malformed")
    first_loss = sorted(r["s7"] for r in rows if r["verdict"] == "WIN")
    first_win = [r["s7"] for r in rows if r["verdict"] == "LOSS"]
    require(len(first_loss) == 13 and first_win == [FIRST_WIN7] and
            all(r["knownLoss8Children"] > 0 and
                r["unproved8Children"] == 0 and r["witness"] is not None
                for r in rows if r["verdict"] == "WIN"),
            "S7 fixed-first polarity/witness regression")
    require(all(len(points(h)) == 7 and safe(points(h)) and
                canonical(points(h)) == h for h in first_loss),
            "new first-LOSS S7 board invalid")
    require(len(frozen_win) == 17 and frozen_win == sorted(set(frozen_win)) and
            all(len(points(h)) == 7 and safe(points(h)) and
                canonical(points(h)) == h for h in frozen_win),
            "frozen WIN7 comparison list invalid")
    historical = set(old)
    require(not historical.intersection(first_loss),
            "historical and new S7 LOSS overlap changed")
    edges = set()
    for h in first_loss:
        ps = points(h)
        for p in ps:
            parent = canonical(tuple(x for x in ps if x != p))
            edges.add((parent, h))
    parents = sorted({p for p, _ in edges})
    require(len(parents) == 91 and len(edges) == 91,
            "new S6 reverse-incidence sharing changed")
    # One S6 parent has both a newly certified fixed-first LOSS7 child and
    # the independently terminal-backed fixed-first WIN7 child. Its S6
    # verdict is WIN (OR), not LOSS; a single LOSS7 is never enough.
    win7 = frozen_win + [FIRST_WIN7, PRIOR_FIRST_WIN7]
    win6 = {canonical(tuple(x for x in points(h) if x != p))
            for h in win7 for p in points(h)}
    require(len(win6) == 117, "historical + two new WIN7 witness union changed")
    already_win6 = sorted(set(parents) & win6)
    first_win_parents = {canonical(tuple(x for x in points(FIRST_WIN7) if x != p))
                         for p in points(FIRST_WIN7)}
    require(already_win6 == [MIXED_S6] and MIXED_S6 in first_win_parents,
            "mixed WIN7/LOSS7 child polarity regression")
    new_set = set(first_loss)
    rows6 = []
    for parent in parents:
        kids = children(parent)
        new = kids & new_set
        old_hit = kids & historical
        require(len(new) == 1 and not (new & old_hit) and
                (parent, next(iter(new))) in edges,
                "new S6->S7 witness edge missing or duplicated")
        rows6.append({
            "s6": parent, "legal7": len(kids),
            "historicalLoss7": len(old_hit),
            "newCertifiedLoss7": len(new),
            "notCoveredByTheseSources": len(kids - historical - new_set),
        })
    rows6.sort(key=lambda r: (r["notCoveredByTheseSources"],
                              -r["historicalLoss7"], r["s6"]))
    totals = {
        "s6ParentClasses": len(rows6),
        "newCertifiedS6ToS7Edges": len(edges),
        "s6AlreadyWINByIndependentWIN7Witness": len(already_win6),
        "remainingS6CandidatesAfterWINExclusion": len(rows6)-len(already_win6),
        "historicalS6ToS7EdgesWithinTheseParents":
            sum(r["historicalLoss7"] for r in rows6),
        "allLegalS6ToS7EdgesWithinTheseParents":
            sum(r["legal7"] for r in rows6),
        "remainingEdgesRelativeToTheseSources":
            sum(r["notCoveredByTheseSources"] for r in rows6),
        "minimumRemaining": rows6[0]["notCoveredByTheseSources"],
        "maximumRemaining": rows6[-1]["notCoveredByTheseSources"],
        "parentsAtMinimum": sum(
            r["notCoveredByTheseSources"] == rows6[0]["notCoveredByTheseSources"]
            for r in rows6),
    }
    require(totals == {
        "s6ParentClasses": 91,
        "newCertifiedS6ToS7Edges": 91,
        "s6AlreadyWINByIndependentWIN7Witness": 1,
        "remainingS6CandidatesAfterWINExclusion": 90,
        "historicalS6ToS7EdgesWithinTheseParents": 76,
        "allLegalS6ToS7EdgesWithinTheseParents": 6056,
        "remainingEdgesRelativeToTheseSources": 5889,
        "minimumRemaining": 46,
        "maximumRemaining": 86,
        "parentsAtMinimum": 5,
    }, "S6 frontier totals changed")
    require(all(r["notCoveredByTheseSources"] > 0 for r in rows6),
            "S6 closure claimed from incomplete inventory")
    return {
        "schema": "n11-fixed14-loss7-to-s6-independent-4x4-audit-v1",
        "perspective": "original-first-player",
        "historicalLoss7": len(old),
        "newTerminalBackedLoss7": len(first_loss),
        "overlapWithHistoricalLoss7": 0,
        **totals,
        "closestFiveS6": rows6[:5],
        "mixedPolarityS6AlreadyWIN": already_win6,
        "newS6LossProofs": 0,
        "twoStoneRootClosed": False,
        "emptyBoard": "UNKNOWN",
        "limitations": ("Historical 2232 LOSS7 are a comparison baseline; "
                        "this audit does not independently verify them or "
                        "the terminal S8 leaves. Uncovered is relative to "
                        "these two sources, not a true UNKNOWN verdict."),
    }

def main():
    require(det4((0, 1, 11, 12)) == 0, "circle fixture")
    require(det4((0, 1, 11, 24)) != 0, "noncircle fixture")
    old = pinned(OLD, OLD_BLOB).decode("ascii").splitlines()
    lift = json.loads(pinned(LIFT, LIFT_BLOB))
    frozen_win = pinned(FROZEN_WIN7, FROZEN_WIN7_BLOB).decode("ascii").splitlines()
    result = audit(old, lift, frozen_win)
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
