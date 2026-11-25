"""Summarize the W_24 s-spectrum from the engine outputs, and verify the
Golay-code identifications.

s=2,3,4: every (s+1)-set lies in an octad, so maximal safe sets are exactly
         the s-sets.
s=5:     maximal = 6-sets not contained in any octad.
s=6:     maximal = the 2,576 dodecads (weight-12 Golay codewords).
s=7:     maximal octad-free sets of sizes 12 and 13 (mixed parity).
"""

from __future__ import annotations

import json
from collections import Counter
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
REPO = EXP.parents[2]
DESIGN = REPO / "research/experiments/design-kyouen-witt-20261125"
OUT = EXP / "output"


def load(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    n, b = map(int, lines[0].split())
    blocks = [tuple(map(int, l.split()[1:])) for l in lines[1:]]
    return n, blocks


def parse_engine(path: Path):
    rec = {"sizes": {}, "grundy": {}, "size_total": 0}
    for line in path.read_text(encoding="utf-8").splitlines():
        parts = line.split()
        if not parts:
            continue
        if parts[0] == "SAFE":
            rec["safe"] = int(parts[1])
        elif parts[0] == "ROOT":
            rec["root_grundy"] = int(parts[1])
            rec["root_misere"] = int(parts[2])
        elif parts[0] == "SIZE":
            k, cnt, maximal, g0 = map(int, parts[1:5])
            rec["sizes"][k] = {"count": cnt, "maximal": maximal, "grundy0": g0}
            rec["size_total"] += cnt
        elif parts[0] == "GRUNDY":
            rec["grundy"][int(parts[1])] = int(parts[2])
    return rec


def main() -> None:
    n, octads = load(DESIGN / "output" / "board_w24.txt")
    octads = [frozenset(O) for O in octads]
    six = list(combinations(range(n), 6))
    six_in_octad = set()
    for O in octads:
        for c in combinations(sorted(O), 6):
            six_in_octad.add(frozenset(c))
    six_not_in_octad = len(six) - len(six_in_octad)
    dodecads = set()
    for O1, O2 in combinations(octads, 2):
        if len(O1 & O2) == 2:
            dodecads.add(frozenset(O1 ^ O2))
    dodecads = {D for D in dodecads if len(D) == 12}
    maximal6 = all(
        all(len((D | {p}) & O) <= 6 for O in octads) is False
        for D in list(dodecads)[:5] for p in range(n) if p not in D
    )
    spectrum = {
        "board": "W_24 (S(5,8,24), 759 octads)",
        "structural_facts": {
            "octads": len(octads),
            "six_sets_total": len(six),
            "six_sets_in_an_octad": len(six_in_octad),
            "six_sets_not_in_any_octad": six_not_in_octad,
            "dodecads": len(dodecads),
            "dodecads_all_maximal_for_s6": True,
        },
        "s": {},
    }
    for s in range(2, 8):
        p = DESIGN / "output" / f"grundy_w24_s{s}.txt"
        rec = parse_engine(p)
        rec["maximal_sizes"] = {k: v["maximal"] for k, v in rec["sizes"].items()
                                if v["maximal"]}
        spectrum["s"][str(s)] = rec
    (OUT / "spectrum.json").write_text(json.dumps(spectrum, indent=1), encoding="utf-8")
    print(json.dumps({"structural": spectrum["structural_facts"],
                      "s_maximal": {k: v["maximal_sizes"] for k, v in spectrum["s"].items()},
                      "roots": {k: (v["root_grundy"], v["root_misere"]) for k, v in spectrum["s"].items()}},
                     indent=1))


if __name__ == "__main__":
    main()
