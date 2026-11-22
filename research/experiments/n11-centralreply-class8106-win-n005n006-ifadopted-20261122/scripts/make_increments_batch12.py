#!/usr/bin/env python3
"""Build the batch-12 (class 8106) IF-ADOPTED increments, fail-closed.

Reads the batch-12 raw 2-pass replay rows of the declaring host
(p1/p2 pairs, all published: chunk 1 eca35f3c for n001-n004, chunk 2
ace92d84 for n005-n008 + status.log), and emits three what-if increment
caches:

  * full 8 probed rows    (n001-n004/n007/n008 LOSS + n005/n006 WIN)
  * n005/n006 WIN rows only (win-only scenario; first multi-WIN increment)
  * 6 LOSS rows only      (loss-only scenario)

Fail-closed gates: every row must come from BOTH raw passes with identical
(stones, legal, is_or, budget, result, nodes); exactly 8 keys n001..n008
read; n005/n006 must be exactly the two result-1 WIN rows;
n001-n004/n007/n008 must be result-2 LOSS rows; legal and (lo,hi) must match
the published batch-keys.json for every key; the declaring-host status.log
PASS rows must agree with the declaring-host raws for every key.  Batch-12
was executed entirely on the declaring host (no takeover-host passes exist),
so the cross-check is 3-way (p1/p2/status) instead of batch-11's 4-way
cross-host. Verdicts are byte-taken from the raws.
Read-only what-if analysis inputs; verdicts are NOT consumed. 11x11 stays
UNKNOWN.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

BATCH = Path(__file__).resolve().parents[4] / "research/experiments/n11-centralreply-closure-class8106-batch12-20261122"
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
            kid = kid.split(".")[0]  # n005.p1 -> n005
            if kid in got and got[kid] != (b, r, n):
                sys.exit(f"ABORT status disagreement for {kid}")
            got[kid] = (b, r, n)
    return got


def main() -> None:
    keys = json.loads((BATCH / "input/batch-keys.json").read_text())["keys"]
    ids = ["n001", "n002", "n003", "n004", "n005", "n006", "n007", "n008"]
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
        for tag in ("p1", "p2"):
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
                sys.exit(f"ABORT {kid}: pass mismatch {tag} {r} vs p1 {ref}")
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
    if len(wins) != 2 or sorted(w[0] for w in wins) != ["n005", "n006"]:
        sys.exit(f"ABORT WIN rows: {[(w[0], w[4]) for w in wins]}")
    if len(losses) != 6 or sorted(l[0] for l in losses) != ["n001", "n002", "n003", "n004", "n007", "n008"]:
        sys.exit(f"ABORT LOSS rows: {[l[0] for l in losses]}")

    hdr_common = [
        "# n11 central-reply closure batch 12 (class 8106) IF-ADOPTED increment (2026-11-22)",
        "# 2-pass node-exact exact-S5 verdicts at budget 15M, fresh cold, pinned jsreplay.js",
        "#   sha256 845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df",
        "# BOTH declaring-host passes agree (p1/p2) on every row; declaring-host",
        "#   status.log PASS rows agree on (budget,result,nodes). Batch-12 was",
        "#   executed entirely on the declaring host: 3-way fail-closed (p1/p2/status),",
        "#   no takeover-host passes exist for this batch (unlike batch-11's 4-way).",
        "# Read-only what-if analysis only; verdicts are NOT consumed.",
        "#   IF-ADOPTED decomposition per Part H-bis / Part J / Part R / Part V / Part AB methodology:",
        "#   WIN-only vs LOSS-only vs full packet, machine-separated.",
        "# batch 12 probed 8/52 (two waves); n009-n052 remain untouched.",
    ]
    tagline = {
        "full": "# 8 rows: all batch-12 probed keys (n001-n004/n007/n008 LOSS + n005/n006 WIN).",
        "win": "# 2 rows: the batch-12 WIN rows n005/n006 only (s5 188395 and s5 219608) - first multi-WIN increment.",
        "loss": "# 6 rows: the batch-12 LOSS rows only (n001-n004/n007/n008; no WIN rows).",
    }

    def write(name, tag, sel):
        p = OUT / name
        lines = hdr_common + ([tagline[tag]] if tagline[tag] else [])
        lines += [f"s5verdict,{r[2]},{r[3]},5,{r[4]},{r[5]}" for r in sorted(sel, key=lambda r: (r[2], r[3]))]
        p.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"{name}: {len(sel)} rows, sha256 {sha(p)}")

    write("increment-batch12-probed-8rows-IFADOPTED-20261122.cache", "full", rows)
    write("increment-batch12-winn005n006-only-IFADOPTED-20261122.cache", "win", wins)
    write("increment-batch12-loss6-only-IFADOPTED-20261122.cache", "loss", losses)
    print("OK 8 resolved rows (6 LOSS + 2 WIN n005/n006), all 3-way (p1/p2/status) node-exact")


if __name__ == "__main__":
    main()
