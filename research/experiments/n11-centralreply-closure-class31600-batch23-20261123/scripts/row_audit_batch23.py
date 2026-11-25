#!/usr/bin/env python3
"""Batch-23 row-audit: machine re-verification of every raw row (Part BN).

Fail-closed audit over the published batch-23 experiment directory:

* every key in input/batch-keys.json has both pass files, each carrying
  the terminal `# replay_done` line (no truncated fragment counts);
* the `replay,` rows of p1 and p2 are node-exact (all compared fields
  identical, wall_s excluded) and within the declared budget;
* per-key PASS/EXHAUSTED/WIN-HALT lines in output/status.log match the
  raw result and node count;
* verdict consumption bookkeeping: result 2 rows are LOSS (adoption
  candidates, consumed only by a later adoption Part), result 1 rows
  are honest WIN labels (never adopted here), result 0 rows are honest
  exhaustion bookkeeping (UNKNOWN, never re-probed at 15M);
* schema fields carry the batch snapshot sha256s for row-level
  provenance.

Interpretation guard: node counts are bookkeeping, never verdicts; the
standard 11x11 empty board and every key stay UNKNOWN unless the verdict
is canonical-consumed by a later adoption Part.
"""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve()
EXP = HERE.parents[1]
SCHEMA = "n11-centralreply-closure-class31600-batch23-rowaudit-v1"


def fail(msg):
    print("GATE FAILED: " + msg)
    raise SystemExit(1)


def sha(p):
    d = hashlib.sha256()
    with Path(p).open("rb") as s:
        for b in iter(lambda: s.read(1024 * 1024), b""):
            d.update(b)
    return d.hexdigest()


def parse_raw(path):
    lines = Path(path).read_text(encoding="utf-8", errors="strict").splitlines()
    done = False
    row = None
    quads = None
    for ln in lines:
        if ln.startswith("# replay_done"):
            done = True
        elif ln.startswith("replay,"):
            row = ln.split(",")
        elif ln.startswith("# forbidden quadruples:"):
            quads = int(ln.split(":")[1].strip())
    if not done:
        fail(f"{path.name}: missing # replay_done (truncated fragment)")
    if row is None:
        fail(f"{path.name}: missing replay row")
    return {"row": row, "quads": quads}


def main():
    keys = json.loads((EXP / "input/batch-keys.json").read_text(encoding="utf-8"))["keys"]
    budget = int(json.loads((EXP / "input/batch-keys.json").read_text(encoding="utf-8"))["budget"])
    status = (EXP / "output/status.log").read_text(encoding="utf-8").splitlines()
    results = {}
    for k in keys:
        kid = k["key_id"]
        p1 = parse_raw(EXP / f"output/raw/{kid}.p1.out")
        p2 = parse_raw(EXP / f"output/raw/{kid}.p2.out")
        r1, r2 = p1["row"], p2["row"]
        # node-exact determinism: all fields identical EXCEPT wall_s (field 8),
        # which is wall-clock bookkeeping and never part of the verdict
        if r1[:8] + r1[9:] != r2[:8] + r2[9:]:
            fail(f"{kid}: p1/p2 row mismatch {r1} vs {r2}")
        # replay format: row[1]=id, row[2]=stones, row[3]=legal, row[4]=is_or,
        #                row[5]=budget, row[6]=result, row[7]=nodes, row[8]=wall_s,
        #                row[9]=key_lo, row[10]=key_hi
        if int(r1[2]) != 5 or int(r1[5]) != budget:
            fail(f"{kid}: stones/budget mismatch: {r1}")
        if int(r1[9]) != int(k["lo"]) or int(r1[10]) != int(k["hi"]):
            fail(f"{kid}: raw key does not match the published input row")
        if int(r1[6]) not in (0, 1, 2):
            fail(f"{kid}: invalid result {r1[6]}")
        nodes = int(r1[7])
        if int(r1[6]) == 0 and nodes != budget:
            fail(f"{kid}: exhausted without full budget nodes")
        if int(r1[6]) != 0 and nodes > budget:
            fail(f"{kid}: nodes exceed budget")
        if int(r1[3]) != int(k["legal"]):
            fail(f"{kid}: raw legal mismatch vs published packet")
        if p1["quads"] != 95670 or p2["quads"] != 95670:
            fail(f"{kid}: forbidden quadruples header mismatch")
        # status.log corroboration
        tag = "PASS" if int(r1[6]) == 2 else ("WIN-HALT" if int(r1[6]) == 1 else "EXHAUSTED")
        line = next((l for l in status
                     if len(l.split()) > 1 and l.split()[1] == kid and tag in l), None)
        if line is None:
            fail(f"{kid}: no {tag} line in status.log")
        if str(nodes) not in line:
            fail(f"{kid}: status.log node count mismatch")
        results[kid] = {
            "result": int(r1[6]), "nodes": nodes, "legal": int(r1[3]),
            "two_pass_exact": True, "status_line": line,
        }
    consumed = sorted(k for k, v in results.items() if v["result"] == 2)
    wins = sorted(k for k, v in results.items() if v["result"] == 1)
    exhausted = sorted(k for k, v in results.items() if v["result"] == 0)
    audit = {
        "schema": SCHEMA,
        "class_index": 31600,
        "batch": 23,
        "keys_total": len(keys),
        "probed": len(results),
        "pass_rows": len(consumed),
        "win_rows": wins,
        "exhausted_rows": exhausted,
        "mismatches": 0,
        "input_sha256": sha(EXP / "input/batch-keys.json"),
        "raws_dir_sha256": None,  # per-file sha, too bulky; row-level gates above
        "note": ("all rows two-pass node-exact; LOSS rows are adoption candidates only "
                 "(consumption via a separate declared adoption Part with the pinned "
                 "fail-closed merger); WIN rows are honest labels (never adopted in this "
                 "batch, scrutiny owner waits); exhausted rows are honest UNKNOWN "
                 "(no same-condition re-probe); the standard 11x11 empty board and every "
                 "key stay UNKNOWN at this point"),
    }
    with (EXP / "output/row-audit.json").open("w", encoding="utf-8") as fh:
        json.dump(audit, fh, indent=1)
        fh.write("\n")
    print(f"row-audit PASS: {len(results)} rows, LOSS {len(consumed)}, WIN {len(wins)}, exhausted {len(exhausted)}")


if __name__ == "__main__":
    main()
