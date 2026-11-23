#!/usr/bin/env python3
"""Batch-28 FULL row-audit, drive-5 minimal derived variant (Part CN).

The published batch-28 full audit `scripts/row_audit_batch28.py` (sha
656cac31, a batch-27 Part BQ byte-clone) corroborates every key's status.log
line with a single-line search `tag in l` where tag = WIN-HALT for result-1
rows.  Batch-28 status.log records WIN rows in TWO lines
(`... aaNNN PASS 15000000,1,<nodes>` immediately followed by
`... aaNNN WIN-HALT`), so the single-line search selects the bare WIN-HALT
line, which carries no node count, and the full audit GATE-FAILs on every
WIN row with "status.log node count mismatch".  Part CB hit exactly this
family of mismatch between a pre-registered audit and the batch-28 record
format and published a minimal derived variant (row_audit_batch28_win_halt.py,
sha 96867282) with a single-gate fix; the same route is taken here for the
FULLY-COMPLETED drive-5 state:

  * the win-halt variant is INAPPLICABLE by design in the fully-completed
    state (it GATE-FAILs on "batch fully completed with no fragment/fileless
    key" - verified on this kit, output below);
  * THIS script is the published full audit 656cac31 with EXACTLY ONE gate
    change: the result-1 (WIN) status.log corroboration now requires BOTH
    the PASS line carrying `15000000,1,<nodes>` AND the WIN-HALT line
    (identical logic to the proven win-halt variant), instead of the
    single-line `tag in l` search.  Every other gate is byte-identical.

Everything else (schema fields, verdict-consumption bookkeeping, budget and
two-pass node-exactness, quads headers, legal matching) is unchanged from the
published full audit.

Interpretation guard: node counts are bookkeeping, never verdicts; the
standard 11x11 empty board, class 5343 and every key stay UNKNOWN unless the
verdict is canonical-consumed by a later adoption Part.
"""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve()
EXP = HERE.parents[1]
SCHEMA = "n11-centralreply-closure-class5343-batch28-rowaudit-full-v2"


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
        # status.log corroboration.
        # MINIMAL DERIVED CHANGE vs published full audit 656cac31: result-1
        # (WIN) rows are recorded in batch-28 status.log as TWO lines (PASS
        # with fields + bare WIN-HALT); require BOTH (this is exactly the
        # win-halt variant's proven has_pass/has_halt pair).
        if int(r1[6]) == 1:
            lines = [l for l in status if len(l.split()) > 1 and l.split()[1] == kid]
            has_pass = any(l.split()[2] == "PASS" and l.split()[3] == f"{budget},{r1[6]},{nodes}" for l in lines)
            has_halt = any("WIN-HALT" in l for l in lines)
            if not (has_pass and has_halt):
                fail(f"{kid}: status.log WIN record incomplete: {lines}")
        else:
            tag = "PASS" if int(r1[6]) == 2 else "EXHAUSTED"
            line = next((l for l in status
                         if len(l.split()) > 1 and l.split()[1] == kid and tag in l), None)
            if line is None:
                fail(f"{kid}: no {tag} line in status.log")
            if str(nodes) not in line:
                fail(f"{kid}: status.log node count mismatch")
        results[kid] = {
            "result": int(r1[6]), "nodes": nodes, "legal": int(r1[3]),
            "two_pass_exact": True,
        }
    consumed = sorted(k for k, v in results.items() if v["result"] == 2)
    wins = sorted(k for k, v in results.items() if v["result"] == 1)
    exhausted = sorted(k for k, v in results.items() if v["result"] == 0)
    audit = {
        "schema": SCHEMA,
        "class_index": 5343,
        "batch": 28,
        "keys_total": len(keys),
        "probed": len(results),
        "pass_rows": len(consumed),
        "loss_rows": consumed,
        "win_rows": wins,
        "exhausted_rows": exhausted,
        "mismatches": 0,
        "input_sha256": sha(EXP / "input/batch-keys.json"),
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
    print(f"row-audit(full-v2) PASS: {len(results)} rows, LOSS {len(consumed)}, WIN {len(wins)}, exhausted {len(exhausted)}")


if __name__ == "__main__":
    main()
