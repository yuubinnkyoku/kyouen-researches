#!/usr/bin/env python3
"""Build the batch-8 (class 2634) IF-ADOPTED increments, fail-closed.

Reads the batch-8 raw 2-pass replay rows (h001-h045: 43 LOSS + h045 WIN;
h002 is an honest budget-exhaustion UNKNOWN row and is EXCLUDED from every
what-if increment - only 2-pass resolved rows may enter) straight from the
pinned batch-8 experiment raws and emits three what-if increment caches:

  * full 44 probed rows   (43 loss + the h045 WIN)
  * h045 WIN row only     (win-only scenario)
  * 43 LOSS rows only     (loss-only scenario)

Fail-closed gates: every row must come from BOTH passes of the same key with
identical (budget,result,nodes,legal); exactly 45 keys h001..h045 read; h002
must be a result-0 exhaustion and is dropped from all increments; exactly one
WIN row and it must be h045; verdicts are byte-taken from the raws.
Read-only what-if analysis inputs; verdicts are NOT consumed. 11x11 stays
UNKNOWN.
"""
import hashlib
import json
import sys
from pathlib import Path

BATCH = Path(__file__).resolve().parents[4] / "research/experiments/n11-centralreply-closure-class2634-batch8-20261122"
OUT = Path(__file__).resolve().parents[1] / "output"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def parse_replay(path: Path):
    row = None
    for line in path.read_text().splitlines():
        if line.startswith("replay,"):
            parts = line.split(",")
            if row is not None:
                sys.exit(f"ABORT multiple replay rows in {path}")
            row = {
                "stones": int(parts[2]), "legal": int(parts[3]),
                "is_or": int(parts[4]),
                "budget": int(parts[5]), "result": int(parts[6]),
                "nodes": int(parts[7]),
                "lo": int(parts[9]), "hi": int(parts[10]),
            }
    if row is None:
        sys.exit(f"ABORT no replay row in {path}")
    return row


def main():
    keys = json.loads((BATCH / "input/batch-keys.json").read_text())["keys"]
    ids = ["h%03d" % i for i in range(1, 46)]
    if [k["key_id"] for k in keys if k["key_id"] in ids] != ids:
        sys.exit("ABORT batch-keys.json missing h001..h045")
    legal_by_id = {k["key_id"]: k["legal"] for k in keys}
    s5_by_id = {k["key_id"]: k["s5_index"] for k in keys}

    rows = []
    exhaustions = []
    for kid in ids:
        p1 = BATCH / f"output/raw/{kid}.p1.out"
        p2 = BATCH / f"output/raw/{kid}.p2.out"
        r1, r2 = parse_replay(p1), parse_replay(p2)
        if (r1["budget"], r1["result"], r1["nodes"], r1["legal"]) != (r2["budget"], r2["result"], r2["nodes"], r2["legal"]):
            sys.exit(f"ABORT {kid}: pass mismatch {r1} vs {r2}")
        if r1["budget"] != 15000000 or r1["stones"] != 5 or r1["is_or"] != 0:
            sys.exit(f"ABORT {kid}: wrong budget/depth {r1}")
        if r1["legal"] != legal_by_id[kid]:
            sys.exit(f"ABORT {kid}: legal mismatch raw={r1['legal']} worklist={legal_by_id[kid]}")
        if r1["result"] == 0:
            exhaustions.append((kid, s5_by_id[kid], r1["lo"], r1["hi"], r1["nodes"]))
            continue
        rows.append((kid, s5_by_id[kid], r1["lo"], r1["hi"], r1["result"], r1["nodes"]))

    wins = [r for r in rows if r[4] == 1]
    losses = [r for r in rows if r[4] == 2]
    if len(wins) != 1 or wins[0][0] != "h045":
        sys.exit(f"ABORT WIN rows: {[(w[0], w[4]) for w in wins]}")
    if len(losses) != 43:
        sys.exit(f"ABORT LOSS count {len(losses)}")
    if [(e[0], e[4]) for e in exhaustions] != [("h002", 15000000)]:
        sys.exit(f"ABORT exhaustion rows: {exhaustions}")

    hdr_common = [
        "# n11 central-reply closure batch 8 (class 2634) IF-ADOPTED increment (2026-11-22)",
        "# 2-pass node-exact exact-S5 verdicts at budget 15M, fresh cold, pinned jsreplay.js",
        "#   sha256 845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df",
        "# Read-only what-if analysis only; verdicts are NOT consumed.",
        "#   IF-ADOPTED decomposition per Part H-bis / Part J / Part R methodology:",
        "#   WIN-only vs LOSS-only vs full packet, machine-separated.",
        "# h002 (s5 11390, budget exhaustion result 0, UNKNOWN) is excluded from",
        "#   every increment; it is not a resolved verdict and not re-searched here.",
    ]
    tagline = {
        "full": "# 44 rows: all batch-8 probed resolved keys h001-h045 minus h002 (43 LOSS + h045 WIN).",
        "win": "# 1 row: the batch-8 WIN row h045 only (no LOSS rows).",
        "loss": "# 43 rows: the batch-8 LOSS rows only (no WIN rows).",
    }

    def write(name, tag, sel):
        p = OUT / name
        lines = hdr_common + ([tagline[tag]] if tagline[tag] else [])
        lines += [f"s5verdict,{r[2]},{r[3]},5,{r[4]},{r[5]}" for r in sorted(sel, key=lambda r: (r[2], r[3]))]
        p.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"{name}: {len(sel)} rows, sha256 {sha(p)}")

    write("increment-batch8-probed-44rows-IFADOPTED-20261122.cache", "full", rows)
    write("increment-batch8-winh045-only-IFADOPTED-20261122.cache", "win", wins)
    write("increment-batch8-loss43-only-IFADOPTED-20261122.cache", "loss", losses)
    print("OK 44 resolved rows (43 LOSS + 1 WIN h045; h002 exhaustion excluded), all 2-pass node-exact")


if __name__ == "__main__":
    main()
