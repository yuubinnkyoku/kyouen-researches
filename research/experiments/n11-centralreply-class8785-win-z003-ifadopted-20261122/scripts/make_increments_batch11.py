#!/usr/bin/env python3
"""Build the batch-11 (class 8785) IF-ADOPTED increments, fail-closed.

Reads the batch-11 raw 2-pass replay rows of BOTH hosts (declaring-host
p1/p2 + takeover-host .p1/.p2.takeover.out, all published), and emits three
what-if increment caches:

  * full 4 probed rows    (z001/z002/z004 LOSS + the z003 WIN)
  * z003 WIN row only     (win-only scenario)
  * 3 LOSS rows only      (loss-only scenario)

Fail-closed gates: every row must come from ALL FOUR raw files (two hosts x
two passes) with identical (stones, legal, is_or, budget, result, nodes);
exactly 4 keys z001..z004 read; z003 must be the single result-1 WIN row;
z001/z002/z004 must be result-2 LOSS rows; legal and (lo,hi) must match the
published batch-keys.json for every key; the declaring-host status.log PASS
rows must agree with the declaring-host raws for every key. Verdicts are
byte-taken from the raws.
Read-only what-if analysis inputs; verdicts are NOT consumed. 11x11 stays
UNKNOWN.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

BATCH = Path(__file__).resolve().parents[4] / "research/experiments/n11-centralreply-closure-class8785-batch11-20261122"
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


def parse_status(path: Path):
    """Declare-host status PASS rows -> {key_id: (budget, result, nodes)}."""
    got = {}
    for line in path.read_text().splitlines():
        m = re.match(r"^\S+ (\S+) PASS (\d+),(\d+),(\d+)$", line)
        if m:
            kid, b, r, n = m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4))
            kid = kid.split(".")[0]  # z003.p1 -> z003
            if kid in got and got[kid] != (b, r, n):
                sys.exit(f"ABORT status disagreement for {kid}")
            got[kid] = (b, r, n)
    return got


def main() -> None:
    keys = json.loads((BATCH / "input/batch-keys.json").read_text())["keys"]
    ids = ["z001", "z002", "z003", "z004"]
    by_id = {k["key_id"]: k for k in keys}
    for kid in ids:
        if kid not in by_id:
            sys.exit(f"ABORT batch-keys.json missing {kid}")
    legal_by_id = {k: by_id[k]["legal"] for k in ids}
    s5_by_id = {k: by_id[k]["s5_index"] for k in ids}
    lohi_by_id = {k: (int(by_id[k]["lo"]), int(by_id[k]["hi"])) for k in ids}

    status = parse_status(BATCH / "output/status.log")

    rows = []
    for kid in ids:
        variants = {}
        for tag in ("p1", "p2", "p1.takeover", "p2.takeover"):
            p = BATCH / f"output/raw/{kid}.{tag}.out"
            if not p.is_file():
                sys.exit(f"ABORT missing raw {p}")
            variants[tag] = parse_replay(p)
        ref = variants["p1"]
        for tag, r in variants.items():
            if (r["stones"], r["legal"], r["is_or"], r["budget"], r["result"],
                    r["nodes"], r["lo"], r["hi"]) != (
                    ref["stones"], ref["legal"], ref["is_or"], ref["budget"],
                    ref["result"], ref["nodes"], ref["lo"], ref["hi"]):
                sys.exit(f"ABORT {kid}: host/pass mismatch {tag} {r} vs p1 {ref}")
        if ref["budget"] != 15000000 or ref["stones"] != 5 or ref["is_or"] != 0:
            sys.exit(f"ABORT {kid}: wrong budget/depth {ref}")
        if ref["legal"] != legal_by_id[kid]:
            sys.exit(f"ABORT {kid}: legal mismatch raw={ref['legal']} batch-keys={legal_by_id[kid]}")
        if (ref["lo"], ref["hi"]) != lohi_by_id[kid]:
            sys.exit(f"ABORT {kid}: key mismatch raw=({ref['lo']},{ref['hi']}) batch-keys={lohi_by_id[kid]}")
        if status.get(kid) != (ref["budget"], ref["result"], ref["nodes"]):
            sys.exit(f"ABORT {kid}: status.log disagreement {status.get(kid)} vs {(ref['budget'], ref['result'], ref['nodes'])}")
        if ref["result"] == 0:
            sys.exit(f"ABORT {kid}: exhaustion row in a resolved batch (no UNKNOWN rows expected)")
        rows.append((kid, s5_by_id[kid], ref["lo"], ref["hi"], ref["result"], ref["nodes"]))

    wins = [r for r in rows if r[4] == 1]
    losses = [r for r in rows if r[4] == 2]
    if len(wins) != 1 or wins[0][0] != "z003":
        sys.exit(f"ABORT WIN rows: {[(w[0], w[4]) for w in wins]}")
    if len(losses) != 3 or sorted(l[0] for l in losses) != ["z001", "z002", "z004"]:
        sys.exit(f"ABORT LOSS rows: {[l[0] for l in losses]}")

    hdr_common = [
        "# n11 central-reply closure batch 11 (class 8785) IF-ADOPTED increment (2026-11-22)",
        "# 2-pass node-exact exact-S5 verdicts at budget 15M, fresh cold, pinned jsreplay.js",
        "#   sha256 845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df",
        "# BOTH hosts agree 4-way (declaring p1/p2 + takeover p1/p2) on every row;",
        "#   declaring-host status.log PASS rows agree on (budget,result,nodes).",
        "# Read-only what-if analysis only; verdicts are NOT consumed.",
        "#   IF-ADOPTED decomposition per Part H-bis / Part J / Part R / Part V methodology:",
        "#   WIN-only vs LOSS-only vs full packet, machine-separated.",
        "# batch 11 probed 4/51 (first wave only); z005-z051 remain untouched.",
    ]
    tagline = {
        "full": "# 4 rows: all batch-11 probed keys (z001/z002/z004 LOSS + z003 WIN).",
        "win": "# 1 row: the batch-11 WIN row z003 only (s5 198530).",
        "loss": "# 3 rows: the batch-11 LOSS rows only (z001/z002/z004; no WIN rows).",
    }

    def write(name, tag, sel):
        p = OUT / name
        lines = hdr_common + ([tagline[tag]] if tagline[tag] else [])
        lines += [f"s5verdict,{r[2]},{r[3]},5,{r[4]},{r[5]}" for r in sorted(sel, key=lambda r: (r[2], r[3]))]
        p.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"{name}: {len(sel)} rows, sha256 {sha(p)}")

    write("increment-batch11-probed-4rows-IFADOPTED-20261122.cache", "full", rows)
    write("increment-batch11-winz003-only-IFADOPTED-20261122.cache", "win", wins)
    write("increment-batch11-loss3-only-IFADOPTED-20261122.cache", "loss", losses)
    print("OK 4 resolved rows (3 LOSS + 1 WIN z003), all 4-way host/pass node-exact")


if __name__ == "__main__":
    main()
