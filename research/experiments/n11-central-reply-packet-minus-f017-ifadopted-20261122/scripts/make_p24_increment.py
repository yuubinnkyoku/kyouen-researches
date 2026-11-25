#!/usr/bin/env python3
"""Machine-derive the P24 if-adopted increment: the published 25-row joint
unconsumed-packet increment MINUS the single f017 WIN row.

f017's (lo, hi) key is re-derived from the pinned batch raw in the kit
(2-pass node-exact checks identical to make_joint_increment.py), then the
matching row is removed from the 25-row increment. Fail-closed: exactly one
row must be removed and it must be a WIN whose lo/hi/verdict match the raw.
The result is a 24-row increment (3 WIN + 21 LOSS) for the read-only
what-if scenario "adopt the packet except f017". Verdicts are NOT consumed.
"""
import hashlib
import sys
from pathlib import Path

KIT = Path("/home/user/knowledge/kyouen-research/_19root-refresh-kit")
JOINT_EXP = Path("/home/user/work/krjoint/research/experiments/n11-central-reply-joint-4win-adoption-ifadopted-20261122")
SRC = JOINT_EXP / "output/increment-unconsumed-packet-25rows-IFADOPTED-20261122.cache"
SRC_SHA = "d49e28245dbaab43cdc815fa96d14714ff8e71d629483ddc095a3b7f5b7577db"
OUT = Path(__file__).resolve().parents[1] / "output/increment-packet-minus-f017-24rows-IFADOPTED-20261122.cache"


def sha(p: Path) -> str:
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()


def f017_key():
    got = []
    for p in (KIT / "batch12264/output/raw/f017.p1.out", KIT / "batch12264/output/raw/f017.p2.out"):
        if not p.is_file():
            sys.exit(f"ABORT missing raw {p}")
        line = [l for l in p.read_text().splitlines() if l.startswith("replay,")]
        if len(line) != 1:
            sys.exit(f"ABORT raw parse {p}: {len(line)} rows")
        # replay,<id>,<stones>,<legal>,<is_or>,<budget>,<result>,<nodes>,<wall>,<lo>,<hi>
        got.append(line[0].split(","))
    f1, f2 = got
    for i in (2, 3, 6, 7):
        if f1[i] != f2[i]:
            sys.exit(f"ABORT f017: passes differ at field {i}")
    if f1[2] != "5" or f1[4] != "0" or f1[5] != "15000000":
        sys.exit(f"ABORT f017: schema {f1[:6]}")
    if f1[6] != "1":
        sys.exit(f"ABORT f017: result {f1[6]} != WIN")
    return int(f1[9]), int(f1[10]), int(f1[7])


def main():
    if sha(SRC) != SRC_SHA:
        sys.exit(f"ABORT source increment sha mismatch: {SRC}")
    lo, hi, nodes = f017_key()
    rows, comments = [], []
    removed = []
    for line in SRC.read_text().splitlines():
        if line.startswith("#"):
            comments.append(line)
            continue
        if not line.strip():
            continue
        parts = line.split(",")
        if len(parts) != 6 or parts[0] != "s5verdict" or parts[3] != "5":
            sys.exit(f"ABORT bad row: {line}")
        r_lo, r_hi, v = int(parts[1]), int(parts[2]), int(parts[4])
        if (r_lo, r_hi) == (lo, hi):
            if v != 1 or int(parts[5]) != nodes:
                sys.exit(f"ABORT f017 row mismatch: {line} vs raw nodes {nodes}")
            removed.append(line)
            continue
        rows.append((r_lo, r_hi, v, int(parts[5])))
    if len(removed) != 1:
        sys.exit(f"ABORT removed {len(removed)} rows, expected exactly 1")
    if any(r[2] not in (1, 2) for r in rows):
        sys.exit("ABORT bad verdict in remaining rows")
    wins = [r for r in rows if r[2] == 1]
    losses = [r for r in rows if r[2] == 2]
    if len(wins) != 3 or len(losses) != 21 or len(rows) != 24:
        sys.exit(f"ABORT counts: {len(wins)} WIN / {len(losses)} LOSS / {len(rows)} rows")
    hdr = [
        "# n11 central-reply closure grind: P24 packet-minus-f017 IF-ADOPTED increment (2026-11-22)",
        "# 24 rows = published 25-row joint unconsumed-packet increment (sha256 d49e2824...)",
        "#   minus the single f017 WIN row (2-pass node-exact raw, kit batch12264).",
        "# 3 WINs (b018/d002/e002) + 21 LOSS rows; all 24 rows are corroborated verdict-level",
        "#   by the third implementation (Part G, audit 281/281 gates PASS).",
        "# This increment exists ONLY for the if-adopted what-if analysis; verdicts are NOT consumed.",
    ]
    OUT.write_text("\n".join(hdr + [f"s5verdict,{r[0]},{r[1]},5,{r[2]},{r[3]}" for r in sorted(rows)]) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: removed 1 row (f017 WIN lo={lo} hi={hi} nodes={nodes}); 3 WIN + 21 LOSS = 24 rows")
    print(f"sha256 {sha(OUT)}")


if __name__ == "__main__":
    main()
