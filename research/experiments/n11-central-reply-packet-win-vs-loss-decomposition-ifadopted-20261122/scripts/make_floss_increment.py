#!/usr/bin/env python3
"""P17: the 17 batch12264 LOSS rows only (f001-f016, f018 - no WINs).

Keys are re-derived fail-closed from the pinned kit batch12264 raws
(2-pass agreement + schema + expected-verdict gates, as in
make_joint_increment.py), then the matching LOSS rows are selected from the
published 25-row packet increment. Read-only what-if analysis input;
verdicts are NOT consumed. 11x11 stays UNKNOWN.
"""
import hashlib
import sys
from pathlib import Path

KIT = Path("/home/user/knowledge/kyouen-research/_19root-refresh-kit")
SRC = Path("/home/user/work/krjoint/research/experiments/n11-central-reply-joint-4win-adoption-ifadopted-20261122/output/increment-unconsumed-packet-25rows-IFADOPTED-20261122.cache")
SRC_SHA = "d49e28245dbaab43cdc815fa96d14714ff8e71d629483ddc095a3b7f5b7577db"
OUT = Path(__file__).resolve().parents[1] / "output/increment-fbatch-losses-only-17rows-IFADOPTED-20261122.cache"
FKEYS = ["f%03d" % i for i in range(1, 17)] + ["f018"]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def raw_key(name):
    got = []
    for p in (KIT / f"batch12264/output/raw/{name}.p1.out", KIT / f"batch12264/output/raw/{name}.p2.out"):
        line = [l for l in p.read_text().splitlines() if l.startswith("replay,")]
        if len(line) != 1:
            sys.exit(f"ABORT raw parse {p}")
        got.append(line[0].split(","))
    f1, f2 = got
    for i in (2, 3, 6, 7):
        if f1[i] != f2[i]:
            sys.exit(f"ABORT {name}: passes differ at field {i}")
    if f1[2] != "5" or f1[4] != "0" or f1[5] != "15000000":
        sys.exit(f"ABORT {name}: schema {f1[:6]}")
    if f1[6] != "2":
        sys.exit(f"ABORT {name}: result {f1[6]} != expected LOSS")
    return int(f1[9]), int(f1[10])


def main():
    if sha(SRC) != SRC_SHA:
        sys.exit("ABORT source increment sha mismatch")
    fkeys = {raw_key(n) for n in FKEYS}
    if len(fkeys) != 17:
        sys.exit(f"ABORT f keys {len(fkeys)} != 17")
    rows = []
    for line in SRC.read_text().splitlines():
        if line.startswith("#") or not line.strip():
            continue
        parts = line.split(",")
        if len(parts) != 6 or parts[0] != "s5verdict" or parts[3] != "5":
            sys.exit(f"ABORT bad row: {line}")
        k = (int(parts[1]), int(parts[2]))
        if k in fkeys:
            if int(parts[4]) != 2:
                sys.exit(f"ABORT f row not LOSS: {line}")
            rows.append((k[0], k[1], 2, int(parts[5])))
    if len(rows) != 17:
        sys.exit(f"ABORT selected {len(rows)} != 17 f-LOSS rows")
    hdr = [
        "# n11 central-reply closure grind: IF-ADOPTED batch12264-LOSS-only increment P17 (2026-11-22)",
        "# 17 rows: f001-f016, f018 (batch12264 LOSS keys, re-derived from the pinned raws).",
        "# Decomposition companion of the joint 25-row packet analysis (Part H).",
        "# Read-only what-if analysis only; verdicts are NOT consumed.",
    ]
    OUT.write_text("\n".join(hdr + [f"s5verdict,{r[0]},{r[1]},5,{r[2]},{r[3]}" for r in sorted(rows)]) + "\n", encoding="utf-8")
    print(f"P17: 17 f-LOSS rows, sha256 {sha(OUT)}")


if __name__ == "__main__":
    main()
