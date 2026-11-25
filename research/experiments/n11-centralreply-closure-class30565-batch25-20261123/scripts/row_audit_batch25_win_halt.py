#!/usr/bin/env python3
"""Batch-24 PARTIAL row-audit after the pre-registered WIN-HALT (Part BO).

Unlike the batch-22 win-halt audit (written post-hoc with the halted
key ids transcribed), THIS variant is PRE-REGISTERED in the batch-25
scaffold before any execution: nothing about which key halts the batch
is hardcoded.  Every quantity is derived from the published experiment
directory itself:

* completed keys: exactly those whose output/raw/{kid}.p1.out AND p2.out
  both carry the terminal `# replay_done` line;
* fragment keys: keys with at least one pass file that are NOT completed
  (a mid-flight worker killed by the drive timeout leaves truncated or
  half-written files; a truncated pass never produced a verdict and is
  not evidence; any complete single pass is bookkeeping only);
* fileless keys: no pass file at all, UNPROBED.

The declared batch-25 protocol (Part BO note amendment) pre-registered
the stop rule: a WIN (replay result 1, two-pass node-exact) halts the
batch immediately with runner rc=45 and an honest WIN label (verdict NOT
consumed; adoption scrutiny owner unchanged).  This audit machine-
verifies exactly what the halted batch produced:

* every COMPLETED key is two-pass node-exact (all compared fields
  identical, wall_s excluded) and within the declared budget; raw key /
  legal / nodes match the published input packet; forbidden quadruples
  header is 95670 in both counted raw files; per-key PASS/WIN-HALT/
  EXHAUSTED lines in output/status.log match the raw result and node
  count (when the raw pass pair exists);
* the audit is only valid under a WIN-HALT invocation: there must be at
  least one completed WIN row (result 1); if the batch completed without
  any WIN row, this variant GATE-FAILS by design and the full audit
  (row_audit_batch25.py) applies instead;
* verdict consumption bookkeeping: result 2 rows are LOSS (adoption
  candidates, consumed only by a later declared adoption Part), result
  1 rows are honest WIN labels (never adopted here), result 0 rows are
  honest UNKNOWN exhaustion bookkeeping (no same-condition re-probe);
  every non-completed key stays UNKNOWN / UNPROBED.  No closure,
  coverage, secured or root claim is made.

Interpretation guard: node counts are bookkeeping, never verdicts; the
standard 11x11 empty board, all 19 central-reply roots, class 30565 and every key stay UNKNOWN at this point.
"""
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve()
EXP = HERE.parents[1]
SCHEMA = "n11-centralreply-closure-class30565-batch25-rowaudit-winhalt-v1"
KEYS_TOTAL = 53
VERDICT_TAGS = ("PASS", "WIN-HALT", "MISMATCH", "EXHAUSTED")


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


def status_verdict_keys(status):
    out = set()
    for l in status:
        parts = l.split()
        for i, p in enumerate(parts):
            if p in VERDICT_TAGS and i >= 1:
                out.add(parts[i - 1])
    return out


def main():
    keys = json.loads((EXP / "input/batch-keys.json").read_text(encoding="utf-8"))["keys"]
    budget = int(json.loads((EXP / "input/batch-keys.json").read_text(encoding="utf-8"))["budget"])
    by_id = {k["key_id"]: k for k in keys}
    if len(keys) != KEYS_TOTAL:
        fail(f"packet key count {len(keys)} != {KEYS_TOTAL}")
    for kid in by_id:
        if len(kid) != 4 or kid[0] != "i" or not re.fullmatch(r"i\d{3}", kid):
            fail(f"unexpected key id form {kid} (batch-25 expects i###)")
    status = (EXP / "output/status.log").read_text(encoding="utf-8").splitlines()

    completed = {}
    fragments = {}
    fileless = []
    for kid in by_id:
        p1p = EXP / f"output/raw/{kid}.p1.out"
        p2p = EXP / f"output/raw/{kid}.p2.out"
        if not p1p.exists() and not p2p.exists():
            fileless.append(kid)
            continue
        f1 = parse_raw(p1p) if p1p.exists() else {"done": False, "row": None, "quads": None}
        f2 = parse_raw(p2p) if p2p.exists() else {"done": False, "row": None, "quads": None}
        if f1["done"] and f2["done"]:
            completed[kid] = (f1, f2)
        else:
            fragments[kid] = (f1, f2)
    if len(completed) + len(fragments) + len(fileless) != KEYS_TOTAL:
        fail("completed/fragment/fileless partition mismatch")
    if not fragments and not fileless:
        fail("batch fully completed with no fragment/fileless key: the FULL audit "
             "(row_audit_batch25.py) applies, not this win-halt variant")

    # completed-key gates (identical to the full audit)
    results = {}
    for kid, (p1, p2) in sorted(completed.items()):
        k = by_id[kid]
        r1, r2 = p1["row"], p2["row"]
        if r1 is None or r2 is None:
            fail(f"{kid}: missing replay row")
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
        tag = "PASS" if int(r1[6]) == 2 else ("WIN-HALT" if int(r1[6]) == 1 else "EXHAUSTED")
        if int(r1[6]) == 1:
            lines = [l for l in status if len(l.split()) > 1 and l.split()[1] == kid]
            has_pass = any(l.split()[2] == "PASS" and l.split()[3] == f"{budget},{r1[6]},{nodes}" for l in lines)
            has_halt = any("WIN-HALT" in l for l in lines)
            if not (has_pass and has_halt):
                fail(f"{kid}: status.log WIN-HALT record incomplete: {lines}")
        else:
            line = next((l for l in status
                         if len(l.split()) > 1 and l.split()[1] == kid and tag in l), None)
            if line is None:
                fail(f"{kid}: no {tag} line in status.log")
            if str(nodes) not in line:
                fail(f"{kid}: status.log node count mismatch")
        results[kid] = {"result": int(r1[6]), "nodes": nodes, "legal": int(r1[3]),
                        "two_pass_exact": True}

    wins = sorted(k for k, v in results.items() if v["result"] == 1)
    if not wins:
        fail("no completed WIN row found: not a WIN-HALT state; "
             "the FULL audit (row_audit_batch25.py) applies, not this variant")

    # fragment-key gates: never evidence; any complete single pass is
    # bookkeeping only; the key stays UNPROBED (fresh-cold re-run by the
    # published completeness guard in any future continuation)
    frag_notes = {}
    for kid, (f1, f2) in sorted(fragments.items()):
        k = by_id[kid]
        for tag, f in (("p1", f1), ("p2", f2)):
            if f["done"] and f["row"] is not None:
                if int(f["row"][9]) != int(k["lo"]) or int(f["row"][10]) != int(k["hi"]):
                    fail(f"{kid}: {tag} complete-pass raw key mismatch vs published input row")
        frag_notes[kid] = {
            "p1_complete_single_pass": f1["done"],
            "p1_result_bookkeeping": int(f1["row"][6]) if f1["done"] and f1["row"] else None,
            "p2_complete_single_pass": f2["done"],
            "pass_pair_complete": False,
            "evidence": False,
            "probed": False,
        }

    # status.log honesty: no verdict-ish line for any non-completed key
    verdict_keys = status_verdict_keys(status)
    noncompleted = set(fragments) | set(fileless)
    bad = sorted(verdict_keys & noncompleted)
    if bad:
        fail(f"status.log carries verdict-ish lines for non-completed keys {bad}")
    missing = sorted(set(completed) - verdict_keys)
    if missing:
        fail(f"status.log lacks verdict lines for completed keys {missing}")

    consumed = sorted(k for k, v in results.items() if v["result"] == 2)
    exhausted = sorted(k for k, v in results.items() if v["result"] == 0)
    audit = {
        "schema": SCHEMA,
        "class_index": 30565,
        "batch": 25,
        "keys_total": KEYS_TOTAL,
        "probed": len(results),
        "pass_rows": len(consumed),
        "loss_rows": consumed,
        "win_rows": wins,
        "exhausted_rows": exhausted,
        "mismatches": 0,
        "fragment_keys": frag_notes,
        "fileless_unprobed": sorted(fileless),
        "unprobed_count": len(fragments) + len(fileless),
        "derived_state": True,
        "stop_rule": ("pre-registered WIN-HALT (runner rc=45 at the first WIN row, "
                      "replay result 1, two-pass node-exact); verdict not consumed; "
                      "batch halted; fragment/fileless keys UNPROBED"),
        "input_sha256": sha(EXP / "input/batch-keys.json"),
        "note": ("two-pass node-exact rows only; WIN rows are honest labels (never "
                 "adopted in this batch, scrutiny owner C++ second-implementation gate "
                 "9193f5b6 unchanged); LOSS rows are adoption candidates only (consumption "
                 "via a separate declared adoption Part with the pinned fail-closed "
                 "merger); fragment keys are UNPROBED (a complete single pass is "
                 "bookkeeping, not evidence; truncated passes carry no # replay_done and "
                 "are re-run fresh-cold by the published completeness guard in any future "
                 "continuation); fileless keys are UNPROBED; the standard 11x11 empty "
                 "board and every key stay UNKNOWN at this point"),
    }
    with (EXP / "output/row-audit-winhalt.json").open("w", encoding="utf-8") as fh:
        json.dump(audit, fh, indent=1)
        fh.write("\n")
    print(f"row-audit(winhalt) PASS: {len(results)} completed rows "
          f"(LOSS {len(consumed)}, WIN {len(wins)}, exhausted {len(exhausted)}), "
          f"fragments {sorted(fragments)}, fileless {len(fileless)}, "
          f"unprobed {len(fragments) + len(fileless)}")


if __name__ == "__main__":
    main()
