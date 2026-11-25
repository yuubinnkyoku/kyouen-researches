#!/usr/bin/env python3
"""Independent D4 / integer-geometry check of the fixed14 LOSS7 -> WIN6 lift.

The S7 verdict itself is established by lift.js and the terminal S8 certificates.
Its S7 LOSS is for the player to move (second player at odd ply), hence
original-first WIN. Only this fixed-first WIN7 yields seven WIN6 witnesses.
This script only checks the exact legal geometry and reverse incidence.
"""
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXPECTED_LOSS7 = "00020000000000821080200000000020"
EXPECTED_PARENTS = [
    "00000000000000003080080000008020",
    "000000000000000a1082000000000008",
    "00000000000000821080200000000020",
    "00000080008000003080000000000020",
    "00020000000000021080200000000020",
    "00020000000000820080200000000020",
    "00020000000000821080000000000020",
]


def points(key):
    mask = int(key, 16)
    assert mask >> 121 == 0
    return tuple(i for i in range(121) if (mask >> i) & 1)


def canonical(indices):
    variants = []
    for mode in range(8):
        mask = 0
        for i in indices:
            x, y = i % 11, i // 11
            a = ((x, y), (10 - y, x), (10 - x, 10 - y),
                 (y, 10 - x), (10 - x, y), (10 - y, 10 - x),
                 (x, 10 - y), (y, x))[mode]
            mask |= 1 << (11 * a[1] + a[0])
        variants.append(mask)
    return f"{min(variants):032x}"


def forbidden(quad):
    xy = [(i % 11, i // 11) for i in quad]
    dx, dy = xy[3]
    rows = [(x - dx, y - dy, x*x + y*y - dx*dx - dy*dy)
            for x, y in xy[:3]]
    a, b, c = rows
    return (a[0]*(b[1]*c[2] - b[2]*c[1])
            - a[1]*(b[0]*c[2] - b[2]*c[0])
            + a[2]*(b[0]*c[1] - b[1]*c[0])) == 0


def safe(indices):
    return not any(forbidden(q) for q in itertools.combinations(indices, 4))


def main():
    result = json.loads((ROOT / "lift_result.json").read_text())
    assert result["schema"] == "n11-fixed14-direct37-s7-lift-v1"
    assert (result["win7"], result["loss7"], result["unknown7"]) == (13, 1, 0)
    assert result["winLossConflicts"] == 0
    assert result["emptyBoard"] == "UNKNOWN"
    assert len(result["rows"]) == 14
    losing = [r for r in result["rows"] if r["verdict"] == "LOSS"]
    assert len(losing) == 1
    row = losing[0]
    assert row["s7"] == EXPECTED_LOSS7
    assert row["knownLoss8Children"] == row["unproved8Children"] == 0
    seven = points(row["s7"])
    assert len(seven) == 7 and safe(seven) and canonical(seven) == row["s7"]

    legal_eight = {
        canonical(seven + (i,))
        for i in range(121)
        if i not in seven and safe(seven + (i,))
    }
    assert len(legal_eight) == row["legal8"] == 35

    parents = set()
    for removed in seven:
        six = tuple(i for i in seven if i != removed)
        assert len(six) == 6 and safe(six)
        key = canonical(six)
        parents.add(key)
        assert canonical(six + (removed,)) == EXPECTED_LOSS7
    assert sorted(parents) == EXPECTED_PARENTS
    print(json.dumps({
        "verified": True, "s7Loss": EXPECTED_LOSS7,
        "legalS8": len(legal_eight), "derivedS6Win": len(parents),
        "s6WinKeys": sorted(parents), "emptyBoard": "UNKNOWN",
        "existingS6OverlapChecked": False
    }, indent=2))


if __name__ == "__main__":
    main()
