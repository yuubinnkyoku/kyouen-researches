#!/usr/bin/env python3
"""Split the published 25-row joint unconsumed-packet increment into a
WINs-only increment (P4: the 4 WIN rows) and a LOSSes-only increment
(P21: the 21 LOSS rows). Fail-closed. Read-only what-if analysis inputs;
verdicts are NOT consumed. 11x11 stays UNKNOWN.
"""
import hashlib
import sys
from pathlib import Path

SRC = Path("/home/user/work/krjoint/research/experiments/n11-central-reply-joint-4win-adoption-ifadopted-20261122/output/increment-unconsumed-packet-25rows-IFADOPTED-20261122.cache")
SRC_SHA = "d49e28245dbaab43cdc815fa96d14714ff8e71d629483ddc095a3b7f5b7577db"
OUT4 = Path(__file__).resolve().parents[1] / "output/increment-wins-only-4rows-IFADOPTED-20261122.cache"
OUT21 = Path(__file__).resolve().parents[1] / "output/increment-losses-only-21rows-IFADOPTED-20261122.cache"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    if sha(SRC) != SRC_SHA:
        sys.exit("ABORT source increment sha mismatch")
    wins, losses = [], []
    for line in SRC.read_text().splitlines():
        if line.startswith("#") or not line.strip():
            continue
        parts = line.split(",")
        if len(parts) != 6 or parts[0] != "s5verdict" or parts[3] != "5":
            sys.exit(f"ABORT bad row: {line}")
        v = int(parts[4])
        (wins if v == 1 else losses).append((int(parts[1]), int(parts[2]), v, int(parts[5])))
    if len(wins) != 4 or len(losses) != 21:
        sys.exit(f"ABORT counts: {len(wins)} WIN / {len(losses)} LOSS")
    hdr4 = [
        "# n11 central-reply closure grind: IF-ADOPTED WINs-only increment P4 (2026-11-22)",
        "# 4 rows: the unconsumed-packet WIN rows b018/d002/e002/f017 (no LOSS rows).",
        "# Decomposition companion of the joint 25-row packet analysis (Part H).",
        "# Read-only what-if analysis only; verdicts are NOT consumed.",
    ]
    hdr21 = [
        "# n11 central-reply closure grind: IF-ADOPTED LOSSes-only increment P21 (2026-11-22)",
        "# 21 rows: the unconsumed-packet LOSS rows (no WIN rows).",
        "# Decomposition companion of the joint 25-row packet analysis (Part H).",
        "# Read-only what-if analysis only; verdicts are NOT consumed.",
    ]
    def write(out, hdr, rows):
        out.write_text("\n".join(hdr + [f"s5verdict,{r[0]},{r[1]},5,{r[2]},{r[3]}" for r in sorted(rows)]) + "\n", encoding="utf-8")
    write(OUT4, hdr4, wins)
    write(OUT21, hdr21, losses)
    wf, lf, wt, lt = sorted(wins), sorted(losses), 0, 0
    for w in wins:
        wt += w[3]
    for l in losses:
        lt += l[3]
    print(f"P4:  {len(wins)} WIN rows, sha256 {sha(OUT4)}")
    print(f"P21: {len(losses)} LOSS rows, sha256 {sha(OUT21)}")
    print(f"WIN keys (lo,hi): {[(r[0], r[1]) for r in sorted(wins)]}")


if __name__ == "__main__":
    main()
