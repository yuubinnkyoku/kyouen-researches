#!/usr/bin/env python3
"""Batch-22 PARTIAL row-audit after the pre-registered WIN-HALT (Part BL).

The declared batch-22 protocol (note amendment, declaration commit
8b27515b) pre-registered the stop rule: a WIN (replay result 1, two-pass
node-exact) halts the batch immediately with rc=45 and an honest WIN
label (verdict NOT consumed; adoption scrutiny owner unchanged).  The
batch halted at k002: 1 of 53 keys carries a completed two-pass row
(k002 WIN); k001 was mid-flight on the other worker when the drive
timeout killed it (its p1 is a complete pass, its p2 is a truncated
fragment without `# replay_done`) and therefore does NOT count as a
probed row; the remaining 52 keys are UNPROBED.

This audit machine-verifies exactly what the halted batch produced:

* every COMPLETED key (both pass files with terminal `# replay_done`)
  is two-pass node-exact (all compared fields identical, wall_s
  excluded) and within the declared budget;
* raw key / legal / nodes match the published input packet;
* forbidden quadruples header is 95670 in every counted raw file;
* per-key PASS/WIN-HALT lines in output/status.log match the raw result
  and node count;
* k001's fragment pair is verified to be: p1 complete (bookkeeping
  single pass, recorded, NOT evidence, key stays UNPROBED) and p2
  truncated (no `# replay_done`, not evidence, fresh-cold re-run by the
  published completeness guard in a future continuation);
* verdict consumption bookkeeping: result 2 rows are LOSS (adoption
  candidates, consumed only by a later declared adoption Part), the
  result 1 row is an honest WIN label (never adopted here), the 52
  unprobed keys stay UNKNOWN. No closure, coverage, secured or root
  claim is made.

Interpretation guard: node counts are bookkeeping, never verdicts; the
standard 11x11 empty board, all 19 central-reply roots, class 25835 and
every key stay UNKNOWN at this point.
"""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve()
EXP = HERE.parents[1]
SCHEMA = "n11-centralreply-closure-class25835-batch22-rowaudit-winhalt-v1"

COMPLETED = ["k002"]
FRAGMENT_KEY = "k001"
KEYS_TOTAL = 53


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
    return {"done": done, "row": row, "quads": quads}


def main():
    keys = json.loads((EXP / "input/batch-keys.json").read_text(encoding="utf-8"))["keys"]
    budget = int(json.loads((EXP / "input/batch-keys.json").read_text(encoding="utf-8"))["budget"])
    by_id = {k["key_id"]: k for k in keys}
    if len(keys) != KEYS_TOTAL:
        fail(f"packet key count {len(keys)} != {KEYS_TOTAL}")
    for kid in COMPLETED:
        if kid not in by_id:
            fail(f"completed key {kid} not in the published packet")
    status = (EXP / "output/status.log").read_text(encoding="utf-8").splitlines()
    results = {}
    for kid in COMPLETED:
        k = by_id[kid]
        p1 = parse_raw(EXP / f"output/raw/{kid}.p1.out")
        p2 = parse_raw(EXP / f"output/raw/{kid}.p2.out")
        if not p1["done"] or not p2["done"]:
            fail(f"{kid}: missing # replay_done")
        if p1["row"] is None or p2["row"] is None:
            fail(f"{kid}: missing replay row")
        r1, r2 = p1["row"], p2["row"]
        if r1[:8] + r1[9:] != r2[:8] + r2[9:]:
            fail(f"{kid}: p1/p2 row mismatch {r1} vs {r2}")
        if int(r1[2]) != 5 or int(r1[5]) != budget:
            fail(f"{kid}: stones/budget mismatch: {r1}")
        if int(r1[9]) != int(k["lo"]) or int(r1[10]) != int(k["hi"]):
            fail(f"{kid}: raw key does not match the published input row")
        if int(r1[6]) not in (0, 1, 2):
            fail(f"{kid}: invalid result {r1[6]}")
        nodes = int(r1[7])
        if int(r1[6]) != 0 and nodes > budget:
            fail(f"{kid}: nodes exceed budget")
        if int(r1[3]) != int(k["legal"]):
            fail(f"{kid}: raw legal mismatch vs published packet")
        if p1["quads"] != 95670 or p2["quads"] != 95670:
            fail(f"{kid}: forbidden quadruples header mismatch")
        tag = "PASS" if int(r1[6]) == 2 else ("WIN-HALT" if int(r1[6]) == 1 else "EXHAUSTED")
        if int(r1[6]) == 1:
            # the PASS determinant line is emitted first, then the WIN-HALT line
            lines = [l for l in status if len(l.split()) > 1 and l.split()[1] == kid]
            has_pass = any(l.split()[2] == "PASS" and l.split()[3] == f"{budget},{r1[6]},{nodes}" for l in lines)
            has_halt = any("WIN-HALT" in l for l in lines)
            if not (has_pass and has_halt):
                fail(f"{kid}: status.log WIN-HALT record incomplete: {lines}")
            line = next(l for l in lines if "WIN-HALT" in l)
        else:
            line = next((l for l in status
                         if len(l.split()) > 1 and l.split()[1] == kid and tag in l), None)
            if line is None:
                fail(f"{kid}: no {tag} line in status.log")
        if str(nodes) not in "".join(lines) if int(r1[6]) == 1 else str(nodes) not in line:
            fail(f"{kid}: status.log node count mismatch")
        results[kid] = {
            "result": int(r1[6]), "nodes": nodes, "legal": int(r1[3]),
            "two_pass_exact": True,
        }

    # fragment-key verification: a006 must be exactly what the guard expects
    f1 = parse_raw(EXP / f"output/raw/{FRAGMENT_KEY}.p1.out")
    f2 = parse_raw(EXP / f"output/raw/{FRAGMENT_KEY}.p2.out")
    if not f1["done"]:
        fail(f"{FRAGMENT_KEY}.p1 unexpectedly truncated")
    if f1["row"] is None:
        fail(f"{FRAGMENT_KEY}.p1 missing replay row")
    if f2["done"]:
        fail(f"{FRAGMENT_KEY}.p2 unexpectedly complete")
    if f1["quads"] != 95670:
        fail(f"{FRAGMENT_KEY}.p1 forbidden quadruples header mismatch")
    k6 = by_id[FRAGMENT_KEY]
    if int(f1["row"][9]) != int(k6["lo"]) or int(f1["row"][10]) != int(k6["hi"]):
        fail(f"{FRAGMENT_KEY}: p1 raw key does not match the published input row")
    frag_note = {
        "key_id": FRAGMENT_KEY,
        "p1_complete_single_pass": True,
        "p1_result_bookkeeping": int(f1["row"][6]),
        "p1_nodes_bookkeeping": int(f1["row"][7]),
        "p2_truncated_no_replay_done": True,
        "evidence": False,
        "probed": False,
    }
    if FRAGMENT_KEY in results:
        fail("fragment key must not be in the completed results")

    consumed = sorted(k for k, v in results.items() if v["result"] == 2)
    wins = sorted(k for k, v in results.items() if v["result"] == 1)
    exhausted = sorted(k for k, v in results.items() if v["result"] == 0)
    probed_ids = [k["key_id"] for k in keys if k["key_id"] in results]
    unprobed = [k["key_id"] for k in keys if k["key_id"] not in results]
    if len(probed_ids) + len(unprobed) != KEYS_TOTAL:
        fail("probed/unprobed partition mismatch")
    if FRAGMENT_KEY not in unprobed:
        fail("fragment key must be counted unprobed")
    # halt-order sanity: the WIN row is k002; nothing after the halt was completed
    if wins != ["k002"]:
        fail(f"unexpected win set {wins}")
    # status.log honesty: no PASS/WIN-HALT/EXHAUSTED line for any unprobed key
    for l in status:
        parts = l.split()
        for i, p in enumerate(parts):
            if p in ("PASS", "WIN-HALT", "MISMATCH", "EXHAUSTED") and parts[i - 1] in unprobed:
                fail(f"status.log carries a verdict-ish line for unprobed key {parts[i-1]}")

    audit = {
        "schema": SCHEMA,
        "class_index": 25835,
        "batch": 22,
        "keys_total": KEYS_TOTAL,
        "probed": len(results),
        "pass_rows": len(consumed),
        "loss_rows": consumed,
        "win_rows": wins,
        "exhausted_rows": exhausted,
        "mismatches": 0,
        "fragment_key": frag_note,
        "unprobed_count": len(unprobed),
        "stop_rule": ("pre-registered WIN-HALT rc=45 at k002 (replay result 1, "
                      "two-pass node-exact); verdict not consumed; batch halted"),
        "input_sha256": sha(EXP / "input/batch-keys.json"),
        "note": ("two-pass node-exact rows only; the WIN row is an honest label (never "
                 "adopted in this batch, scrutiny owner C++ second-implementation gate "
                 "9193f5b6 unchanged); LOSS rows are adoption candidates only (consumption "
                 "via a separate declared adoption Part with the pinned fail-closed "
                 "merger); the fragment key k001 is UNPROBED (its complete p1 is a "
                 "bookkeeping single pass, not evidence; its truncated p2 carries no "
                 "# replay_done and is re-run fresh-cold by the published completeness "
                 "guard in any future continuation); the remaining 52 keys are UNPROBED; "
                 "the standard 11x11 empty board and every key stay UNKNOWN at this point"),
    }
    with (EXP / "output/row-audit-winhalt.json").open("w", encoding="utf-8") as fh:
        json.dump(audit, fh, indent=1)
        fh.write("\n")
    print(f"row-audit(winhalt) PASS: {len(results)} completed rows "
          f"(LOSS {len(consumed)}, WIN {len(wins)}, exhausted {len(exhausted)}), "
          f"fragment {FRAGMENT_KEY} unprobed, {len(unprobed)} keys unprobed")


if __name__ == "__main__":
    main()
