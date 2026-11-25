#!/usr/bin/env python3
"""Build the batch-9 (class 1518) IF-ADOPTED increments, fail-closed.

Reads the batch-9 raw 2-pass replay rows (j001-j033: 32 LOSS + j033 WIN)
straight from the pinned batch-9 experiment raws and emits three what-if
increment caches:

  * full 33 probed rows   (increment-batch9-probed-33rows-IFADOPTED)
  * j033 WIN row only     (increment-batch9-winj033-only-IFADOPTED)
  * 32 LOSS rows only     (increment-batch9-loss32-only-IFADOPTED)

Fail-closed gates: every row must come from BOTH passes of the same key with
identical (budget,result,nodes,legal); exactly 33 keys j001..j033; exactly one
WIN row and it must be j033; verdicts are byte-taken from the raws.
Read-only what-if analysis inputs; verdicts are NOT consumed. 11x11 stays
UNKNOWN.
"""
import hashlib
import json
import sys
from pathlib import Path

BATCH = Path(__file__).resolve().parents[4] / "research/experiments/n11-centralreply-closure-class1518-batch9-20261122"
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
    ids = ["j%03d" % i for i in range(1, 34)]
    if [k["key_id"] for k in keys if k["key_id"] in ids] != ids:
        sys.exit("ABORT batch-keys.json missing j001..j033")
    legal_by_id = {k["key_id"]: k["legal"] for k in keys}
    s5_by_id = {k["key_id"]: k["s5_index"] for k in keys}

    rows = []
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
        rows.append((kid, s5_by_id[kid], r1["lo"], r1["hi"], r1["result"], r1["nodes"]))

    wins = [r for r in rows if r[4] == 1]
    losses = [r for r in rows if r[4] == 2]
    if len(wins) != 1 or wins[0][0] != "j033":
        sys.exit(f"ABORT WIN rows: {[(w[0], w[4]) for w in wins]}")
    if len(losses) != 32:
        sys.exit(f"ABORT LOSS count {len(losses)}")

    hdr_common = [
        "# n11 central-reply closure batch 9 (class 1518) IF-ADOPTED increment (2026-11-22)",
        "# 2-pass node-exact exact-S5 verdicts at budget 15M, fresh cold, pinned jsreplay.js",
        "#   sha256 845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df",
        "# Read-only what-if analysis only; verdicts are NOT consumed.",
        "#   IF-ADOPTED decomposition per Part H-bis / Part J methodology:",
        "#   WIN-only vs LOSS-only vs full packet, machine-separated.",
    ]
    tagline = {
        "full": "# 33 rows: all batch-9 probed keys j001-j033 (32 exact LOSS + j033 WIN).",
        "win": "# 1 row: the batch-9 WIN row j033 only (no LOSS rows).",
        "loss": "# 32 rows: the batch-9 LOSS rows j001-j032 only (no WIN rows).",
    }

    def write(name, tag, sel):
        p = OUT / name
        lines = hdr_common + ([tagline[tag]] if tagline[tag] else [])
        lines += [f"s5verdict,{r[2]},{r[3]},5,{r[4]},{r[5]}" for r in sorted(sel, key=lambda r: (r[2], r[3]))]
        p.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"{name}: {len(sel)} rows, sha256 {sha(p)}")

    write("increment-batch9-probed-33rows-IFADOPTED-20261122.cache", "full", rows)
    write("increment-batch9-winj033-only-IFADOPTED-20261122.cache", "win", wins)
    write("increment-batch9-loss32-only-IFADOPTED-20261122.cache", "loss", losses)
    print("OK 33 rows (32 LOSS + 1 WIN j033), all 2-pass node-exact")


if __name__ == "__main__":
    main()
