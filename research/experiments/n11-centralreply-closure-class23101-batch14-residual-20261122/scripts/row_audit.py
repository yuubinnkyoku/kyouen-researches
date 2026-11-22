#!/usr/bin/env python3
"""Row-audit for Part AW (class 23101 batch-14 residual q043..q052), fail-closed.

Re-verifies every published-destined row mechanically from the raw pass files:
  * both passes carry the terminal '# replay_done' line (completeness guard)
  * p1 == p2 on (stones, legal, is_or, budget, result, nodes, lo, hi) --
    2-pass fresh-cold determinism, node-exact
  * budget == 15,000,000 and nodes <= budget
  * result == 2 (LOSS) for every row (this batch found zero WIN, zero
    exhaustion - asserted, not assumed)
  * the input CSV (lo,hi,legal) agrees with the row's raw header and with
    input/batch-keys.json for the key id
  * the status.log PASS row agrees with the raws on (budget, result, nodes)
  * the status.log resolved set is exactly the 10 residual keys

Emits output/row-audit.json (schema
n11-centralreply-closure-class23101-batch14residual-rowaudit-v1).  Verdicts
are NOT consumed here.  11x11 stays UNKNOWN; nodes are bookkeeping, never
verdicts.
"""
import hashlib
import json
import sys
from pathlib import Path

EXP = Path(__file__).resolve().parents[1]
RAW = EXP / "output/raw"
INPUT = EXP / "input"

RESIDUAL_IDS = [f"q{i:03d}" for i in range(43, 53)]
BUDGET = 15000000
FIELDS = ("stones", "legal", "is_or", "budget", "result", "nodes", "lo", "hi")


def die(msg):
    sys.exit(f"ABORT {msg}")


def parse_replay(path: Path):
    row = None
    done = False
    for line in path.read_text().splitlines():
        if line.startswith("replay,"):
            if row is not None:
                die(f"multiple replay rows in {path}")
            p = line.split(",")
            row = {"stones": int(p[2]), "legal": int(p[3]), "is_or": int(p[4]),
                   "budget": int(p[5]), "result": int(p[6]), "nodes": int(p[7]),
                   "lo": int(p[9]), "hi": int(p[10])}
        if line.startswith("# replay_done"):
            done = True
    if row is None:
        die(f"no replay row in {path}")
    if not done:
        die(f"incomplete pass (no '# replay_done') in {path}")
    return row


def main():
    keys = {k["key_id"]: k for k in json.loads((INPUT / "batch-keys.json").read_text())["keys"]}
    if set(keys) != set(RESIDUAL_IDS):
        die("batch-keys ids != residual ids")

    status = {}
    for line in (EXP / "output/status.log").read_text().splitlines():
        parts = line.split()
        if len(parts) >= 4 and parts[2] == "PASS":
            kid, b, r, n = parts[1], int(parts[3].split(",")[0]), int(parts[3].split(",")[1]), int(parts[3].split(",")[2])
            status[kid] = (b, r, n)
    if set(status) != set(RESIDUAL_IDS):
        die(f"status resolved set != residual set: {sorted(set(status) ^ set(RESIDUAL_IDS))}")

    rows = []
    total_nodes = 0
    for kid in RESIDUAL_IDS:
        p1 = parse_replay(RAW / f"{kid}.p1.out")
        p2 = parse_replay(RAW / f"{kid}.p2.out")
        if tuple(p1[f] for f in FIELDS) != tuple(p2[f] for f in FIELDS):
            die(f"{kid}: p1/p2 mismatch {p1} vs {p2}")
        for r in (p1, p2):
            if r["budget"] != BUDGET or r["nodes"] > BUDGET or r["stones"] != 5 or r["is_or"] != 0:
                die(f"{kid}: budget/depth fields wrong {r}")
            if r["result"] != 2:
                die(f"{kid}: expected result 2 (LOSS), got {r['result']}")
        k = keys[kid]
        for r in (p1, p2):
            if (r["lo"], r["hi"]) != (int(k["lo"]), int(k["hi"])) or r["legal"] != int(k["legal"]):
                die(f"{kid}: raw key/legal disagree with batch-keys {r} vs {k}")
        csv_fields = (INPUT / f"{kid}.input.csv").read_text().strip().split(",")
        if (csv_fields[3], csv_fields[4], csv_fields[5]) != (k["lo"], k["hi"], str(k["legal"])):
            die(f"{kid}: input csv disagrees with batch-keys")
        if status[kid] != (p1["budget"], p1["result"], p1["nodes"]):
            die(f"{kid}: status.log disagreement {status[kid]} vs raw")
        total_nodes += p1["nodes"]
        rows.append({"key_id": kid, "s5_index": int(k["s5_index"]),
                     "lo": p1["lo"], "hi": p1["hi"], "legal": p1["legal"],
                     "result": p1["result"], "nodes": p1["nodes"], "budget": p1["budget"]})

    results = {r["result"] for r in rows}
    if results != {2} or len(rows) != 10:
        die(f"row results {results} / count {len(rows)}")

    audit = {
        "schema": "n11-centralreply-closure-class23101-batch14residual-rowaudit-v1",
        "part": "Part AW (solver, batch-14 residual q043..q052)",
        "class_index": 23101,
        "budget": BUDGET,
        "probed_rows": len(rows),
        "probed_ids": RESIDUAL_IDS,
        "wins": [],
        "win_continues": [],
        "exhausted_result0": [],
        "mismatch": 0,
        "replay_done_complete_all_passes": True,
        "all_result2_2pass_node_exact": True,
        "status_pass_rows_cross_checked": True,
        "total_nodes_per_pass": total_nodes,
        "nodes_range": [min(r["nodes"] for r in rows), max(r["nodes"] for r in rows)],
        "verdict_consumption": 0,
        "interpretation_guard": ("row audit only: the 10 LOSS rows are NOT consumed here; "
                                 "canonical adoption is a separately declared Part on the "
                                 "post-AV 6,172-row base; class 23101 still holds the "
                                 "unconsumed q042 WIN (scrutiny owner gate 9193f5b6...); "
                                 "standard 11x11 empty board / 19 central-reply roots / "
                                 "class 23101 and all 10 keys remain UNKNOWN; nodes are "
                                 "bookkeeping, never verdicts"),
        "rows": rows,
    }
    out = EXP / "output/row-audit.json"
    out.write_text(json.dumps(audit, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"row-audit PASS: 10/10 rows result 2, 2-pass node-exact, total nodes/pass {total_nodes}")
    print(f"sha256 {hashlib.sha256(out.read_bytes()).hexdigest()}")


if __name__ == "__main__":
    main()
