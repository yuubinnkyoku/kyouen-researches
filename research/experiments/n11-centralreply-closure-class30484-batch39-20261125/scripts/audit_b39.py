#!/usr/bin/env python3
"""Part EH batch-39 (closure class 30484) machine audit.

Fail-closed SSOT aggregation over the published batch-39 evidence:
  - input/batch-keys-b39.json    (targets SSOT, 50 fresh keys + 2 claim-reserved)
  - output/status.log            (final drive snapshot, 54 lines)
  - output/raw/*.p1/p2.out      (100 raws, 2-pass fresh-cold exact replay @15M)
  - sources/*                    (pinned maker inputs incl. canonical cache)

Checks (any violation => exit 1, no batch-audit.json written):
  A1 layout: input/, sources/, scripts/, output/raw exist under the experiment root
     (experiment root = parent of this script's directory).
  A2 batch-keys-b39.json sha256 == 5e25b550ef42c1f56dc9d4b69d61d33304664ad839ed7f8d19f45fe50f5e63a9;
     schema n11-centralreply-closure-batch39-keys-v1; target_key_count 50;
     consumed_into_canonical_cache false; claim_reserved_excluded == {ai044, ai048}
     with probe_order {585, 586}; 50 unique key_ids aj001..aj050.
  A3 every pin in batch-keys-b39.json["pins"] matches the recomputed sha256 of
     the corresponding sources/ file (byte drift => fail).
  A4 output/raw contains exactly 100 files: 50 keys x {p1,p2}.
  A5 per raw: exactly one `replay,` line and replay_done rows=1; fields
     id=0, stones=5, is_or=0, budget=15000000; legal/lo/hi equal the batch-keys row.
  A6 p1 vs p2 node-exact: all replay fields identical except wall_s.
  A7 status.log sha256 == 08d70bb77c08e7a37b77005b3b2dca1a759f56b4146e1623eef4eb69759a3cea,
     exactly 54 lines; exactly one PASS line per key whose "budget,result,nodes"
     equals the raws; EXHAUSTED line for each result==0 key (nodes==budget);
     WIN-HALT line for each result==1 key; no unaccounted lines; no LOSS key
     carries an EXHAUSTED/WIN-HALT line.
  A8 honest verdict accounting: EXHAUSTED keys are budget-halts (result 0,
     nodes == 15000000) => honest UNKNOWN, no same-condition re-probe;
     WIN keys are unconsumed (adoption only via scrutiny-owner C++ gate
     9193f5b6...); MISMATCH == 0 required for the drive.
  A9 all 52 child pairs (50 targets + 2 claim-reserved) absent from
     sources/canonical-cache-fc3e4ac9.cache (verdicts unconsumed by construction).

Output: output/batch-audit.json (schema n11-centralreply-closure-batch39-audit-v1),
deterministic (sort_keys, indent 2, trailing newline) so independent re-runs are
byte-identical. Stdout carries one OK line with label counts and the emitted
sha256; any check failure prints "AUDIT-FAIL" and exits 1.
"""

import hashlib
import json
import os
import re
import sys

EXP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIN_BATCH_KEYS = "5e25b550ef42c1f56dc9d4b69d61d33304664ad839ed7f8d19f45fe50f5e63a9"
PIN_STATUS_LOG = "08d70bb77c08e7a37b77005b3b2dca1a759f56b4146e1623eef4eb69759a3cea"
PIN_CANONICAL_CACHE = "fc3e4ac9052447158202f09d5efe05468dba32fe95ec90beaaa0a0de9d2c020f"
BUDGET = 15000000
SCHEMA_OUT = "n11-centralreply-closure-batch39-audit-v1"
SCRUTINY_GATE = "9193f5b6 (C++ scrutiny-owner gate; batch-39 verdicts are NOT consumed)"


def fail(msg):
    print("AUDIT-FAIL " + msg)
    sys.exit(1)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def read_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def main():
    # A1 layout
    inp = os.path.join(EXP, "input")
    src = os.path.join(EXP, "sources")
    raw_dir = os.path.join(EXP, "output", "raw")
    for d in (inp, src, raw_dir):
        if not os.path.isdir(d):
            fail("A1 missing directory " + d)
    keys_path = os.path.join(inp, "batch-keys-b39.json")
    status_path = os.path.join(EXP, "output", "status.log")
    for p in (keys_path, status_path):
        if not os.path.isfile(p):
            fail("A1 missing file " + p)

    # A2 batch keys SSOT
    if sha256_file(keys_path) != PIN_BATCH_KEYS:
        fail("A2 batch-keys-b39.json sha256 drift")
    packet = json.loads(read_text(keys_path))
    if packet.get("schema") != "n11-centralreply-closure-batch39-keys-v1":
        fail("A2 schema drift: %r" % packet.get("schema"))
    if packet.get("target_key_count") != 50 or len(packet.get("keys", [])) != 50:
        fail("A2 target_key_count/keys mismatch")
    if packet.get("consumed_into_canonical_cache") is not False:
        fail("A2 consumed_into_canonical_cache must be false")
    reserved = packet.get("claim_reserved_excluded", [])
    if sorted(r.get("key_id") for r in reserved) != ["ai044", "ai048"]:
        fail("A2 claim-reserved set drift: %r" % [r.get("key_id") for r in reserved])
    if sorted(r.get("probe_order") for r in reserved) != [585, 586]:
        fail("A2 claim-reserved probe_order drift")
    keys = packet["keys"]
    ids = [k["key_id"] for k in keys]
    if len(set(ids)) != 50 or sorted(ids) != ["aj%03d" % i for i in range(1, 51)]:
        fail("A2 key_id set drift")
    if sorted(k["probe_order"] for k in keys) != \
            list(range(540, 585)) + list(range(587, 592)):
        fail("A2 probe_order set drift (expected 540..584 + 587..591)")

    # A3 pinned bytes recomputed (sources/ + the pinned drive scripts)
    pins = packet.get("pins", {})
    expected_pin_keys = {
        "batch38_batch_keys", "canonical_cache", "closure_classes",
        "freshness_ranks13to20", "jsreplay", "prior_probe_universe",
        "quarantine", "refresh_summary", "runbatch",
        "worklist_class30484_extract",
    }
    if set(pins) != expected_pin_keys:
        fail("A3 pin key set drift: %r" % sorted(pins))
    pin2file = {
        "batch38_batch_keys": (src, "batch-keys-b38.json"),
        "canonical_cache": (src, "canonical-cache-fc3e4ac9.cache"),
        "closure_classes": (src, "closure-classes.csv"),
        "freshness_ranks13to20": (src, "freshness-ranks13to20.csv"),
        "jsreplay": (os.path.join(EXP, "scripts"), "jsreplay.js"),
        "prior_probe_universe": (src, "prior-probe-universe.csv"),
        "quarantine": (src, "quarantine.json"),
        "refresh_summary": (src, "refresh-summary.json"),
        "runbatch": (os.path.join(EXP, "scripts"), "runbatch.sh"),
        "worklist_class30484_extract": (src, "worklist-class30484-extract.csv"),
    }
    for pk, (pdir, fname) in pin2file.items():
        p = os.path.join(pdir, fname)
        if not os.path.isfile(p):
            fail("A3 missing pinned file " + fname)
        if sha256_file(p) != pins[pk]:
            fail("A3 pin drift for %s (%s)" % (fname, pk))
    if pins["canonical_cache"] != PIN_CANONICAL_CACHE:
        fail("A3 canonical cache pin unexpected")

    # A4 raw set
    raws = sorted(os.listdir(raw_dir))
    expect = sorted("%s.%s.out" % (i, p) for i in ids for p in ("p1", "p2"))
    if raws != expect:
        fail("A4 output/raw file set drift (%d files)" % len(raws))

    status_text = read_text(status_path)

    # Status log structural pass (A7)
    if sha256_file(status_path) != PIN_STATUS_LOG:
        fail("A7 status.log sha256 drift")
    status_lines = [l for l in status_text.splitlines() if l.strip()]
    if len(status_lines) != 54:
        fail("A7 status.log must have 54 lines, got %d" % len(status_lines))
    pat_pass = re.compile(r"^(\S+) (aj\d{3}) PASS (%d),(\d),(\d+)$" % BUDGET)
    pat_exh = re.compile(r"^\S+ (aj\d{3}) EXHAUSTED %d,0,%d$" % (BUDGET, BUDGET))
    pat_win = re.compile(r"^\S+ (aj\d{3}) WIN-HALT$")
    seen_pass, seen_exh, seen_win = {}, set(), set()
    for l in status_lines:
        m = pat_pass.match(l)
        if m:
            kid = m.group(2)
            if kid in seen_pass:
                fail("A7 duplicate PASS line " + kid)
            seen_pass[kid] = (m.group(1), int(m.group(4)), int(m.group(5)))
            continue
        m = pat_exh.match(l)
        if m:
            seen_exh.add(m.group(1))
            continue
        m = pat_win.match(l)
        if m:
            seen_win.add(m.group(1))
            continue
        fail("A7 unaccounted status.log line: %r" % l)
    if len(seen_pass) != 50:
        fail("A7 PASS lines %d != 50" % len(seen_pass))

    # A5/A6/A8 per-key raw checks
    per_key = []
    counts = {"LOSS": 0, "EXHAUSTED": 0, "WIN": 0}
    total_nodes = 0
    exhausted_keys, win_keys = [], []
    for k in sorted(keys, key=lambda x: x["probe_order"]):
        kid = k["key_id"]
        parts = {}
        for p in ("p1", "p2"):
            txt = read_text(os.path.join(raw_dir, "%s.%s.out" % (kid, p)))
            reps = re.findall(r"^replay,(.*)$", txt, re.M)
            if len(reps) != 1 or "# replay_done rows=1" not in txt:
                fail("A5 %s.%s replay rows != 1" % (kid, p))
            f = reps[0].split(",")
            if len(f) != 10:
                fail("A5 %s.%s field count %d != 10" % (kid, p, len(f)))
            parts[p] = f
        r1, r2 = parts["p1"], parts["p2"]
        if [x for i, x in enumerate(r1) if i != 7] != [x for i, x in enumerate(r2) if i != 7]:
            fail("A6 %s p1/p2 not node-exact: %r vs %r" % (kid, r1, r2))
        if not (r1[0] == "0" and r1[1] == "5" and r1[3] == "0" and int(r1[4]) == BUDGET):
            fail("A5 %s unexpected replay header fields %r" % (kid, r1))
        if int(r1[2]) != k["legal"] or int(r1[8]) != k["lo"] or int(r1[9]) != k["hi"]:
            fail("A5 %s legal/lo/hi drift vs batch-keys" % kid)
        result, nodes = int(r1[5]), int(r1[6])
        label = {0: "EXHAUSTED", 1: "WIN", 2: "LOSS"}.get(result, None)
        if label is None:
            fail("A8 %s result not in {0,1,2}: %s" % (kid, r1[5]))
        if kid not in seen_pass:
            fail("A7 missing PASS line for " + kid)
        ts, st_res, st_nodes = seen_pass[kid]
        if (st_res, st_nodes) != (result, nodes):
            fail("A7 %s PASS line drift: (%d,%d) vs raw (%d,%d)"
                 % (kid, st_res, st_nodes, result, nodes))
        if result == 0:
            if nodes != BUDGET:
                fail("A8 %s EXHAUSTED with nodes %d != budget" % (kid, nodes))
            if kid not in seen_exh:
                fail("A7 missing EXHAUSTED line for " + kid)
            exhausted_keys.append(kid)
        elif kid in seen_exh:
            fail("A7 EXHAUSTED line on non-exhausted key " + kid)
        if result == 1:
            if kid not in seen_win:
                fail("A7 missing WIN-HALT line for " + kid)
            win_keys.append(kid)
        elif kid in seen_win:
            fail("A7 WIN-HALT line on non-WIN key " + kid)
        counts[label] += 1
        total_nodes += nodes
        per_key.append({
            "budget": BUDGET,
            "key_id": kid,
            "nodes": nodes,
            "probe_order": k["probe_order"],
            "result": result,
            "result_label": label,
            "ts": ts,
        })
    leftover_exh = seen_exh - set(exhausted_keys)
    leftover_win = seen_win - set(win_keys)
    if leftover_exh or leftover_win:
        fail("A7 unaccounted EXHAUSTED/WIN-HALT lines: %r %r"
             % (sorted(leftover_exh), sorted(leftover_win)))
    if counts["EXHAUSTED"] != 2 or counts["WIN"] != 2 or counts["LOSS"] != 46:
        fail("A8 honest label counts drift: %r" % counts)

    # A9a closure-classes rank-20 anchor for class 30484 (SSOT tie)
    cc_lines = [l for l in read_text(os.path.join(src, "closure-classes.csv")).splitlines()
                if l.strip()]
    if cc_lines[0].split(",") != ["class_rank", "class_index", "class_lo", "class_hi",
                                 "unknown_now", "first_group_first", "first_group_third",
                                 "groups_served_count"]:
        fail("A9a closure-classes.csv header drift")
    rank20 = [l.split(",") for l in cc_lines[1:] if l.split(",")[0] == "20"]
    if len(rank20) != 1 or rank20[0][:5] != ["20", "30484", "1152922604135251968",
                                             "65536", "52"]:
        fail("A9a closure-classes rank-20 row drift: %r" % rank20)
    if any(k["class_mask"] != [1152922604135251968, 65536] for k in keys):
        fail("A9a key class_mask drift")
    if any(int(k.get("class_unknown_now_at_selection", -1)) != 52 for k in keys):
        fail("A9a key class_unknown_now_at_selection drift")

    # A9 canonical-cache absence (52 pairs, port of maker G4)
    all_children = [(k["lo"], k["hi"]) for k in keys] + [
        (r["lo"], r["hi"]) for r in reserved
    ]
    wanted = set(all_children)
    n_cache_rows = 0
    present = set()
    with open(os.path.join(src, "canonical-cache-fc3e4ac9.cache"), "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("s5verdict,"):
                n_cache_rows += 1
                q = line.rstrip("\n").split(",")
                if (int(q[1]), int(q[2])) in wanted:
                    present.add((int(q[1]), int(q[2])))
    if present:
        fail("A9 canonical cache contains batch-39 pair(s): %r" % sorted(present))
    if n_cache_rows != packet["canonical_cache_s5verdict_rows"]:
        fail("A9 canonical cache row count drift %d != %r"
             % (n_cache_rows, packet["canonical_cache_s5verdict_rows"]))

    audit = {
        "batch": "batch-39",
        "batch_keys_b39_sha256": PIN_BATCH_KEYS,
        "claims": ("no closure, no coverage, no secured-coverage, no root outcome claimed; "
                   "standard 11x11 empty board and all 19 central-reply roots stay UNKNOWN; "
                   "nodes are bookkeeping"),
        "class_index": 30484,
        "class_mask": [1152922604135251968, 65536],
        "drive": ("2-pass fresh-cold exact replay, budget 15000000, "
                  "1 solver row / key / pass, single drive39 invocation = 2 keys x 2 workers (2-core host)"),
        "part": "Part EH",
        "per_key": per_key,
        "pins": dict(pins),
        "results": {
            "EXHAUSTED": counts["EXHAUSTED"],
            "LOSS": counts["LOSS"],
            "MISMATCH": 0,
            "WIN": counts["WIN"],
            "exhausted_keys_honest_unknown": exhausted_keys,
            "exhausted_note": ("result==0 at 15000000-node budget on both passes; honest UNKNOWN, "
                               "no same-condition re-probe permitted"),
            "total_nodes_all_keys_single_pass": total_nodes,
            "win_keys_unconsumed": win_keys,
            "win_note": ("WIN verdicts NOT consumed anywhere; adoption only via scrutiny-owner "
                         "C++ gate " + SCRUTINY_GATE),
        },
        "schema": SCHEMA_OUT,
        "selection": ("closure-classes 27e00b0d rank 20, class 30484 unknown_now 52 = "
                      "2 dual-class children claim-reserved for in-flight Part EF (batch-38 ai044/ai048, "
                      "probe_order 585/586, same-condition re-probe prohibited) + 50 clean fresh targets "
                      "aj001..aj050 (probe_order 540..589); ranks 13..19 machine-verified fresh-0 "
                      "(freshness-ranks13to20.csv deea05b8)"),
        "status_log_sha256": PIN_STATUS_LOG,
        "target_key_count": 50,
        "verdicts_consumed_into_canonical_cache": False,
    }
    out_path = os.path.join(EXP, "output", "batch-audit.json")
    blob = json.dumps(audit, sort_keys=True, indent=2) + "\n"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(blob)
    print("AUDIT-OK batch-39 class 30484: 50 keys, LOSS %d / EXHAUSTED %d / WIN %d, MISMATCH 0, "
          "total_nodes_single_pass %d, batch-audit.json sha256 %s"
          % (counts["LOSS"], counts["EXHAUSTED"], counts["WIN"], total_nodes,
             hashlib.sha256(blob.encode("utf-8")).hexdigest()))


if __name__ == "__main__":
    main()
