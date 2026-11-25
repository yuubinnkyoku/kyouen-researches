#!/usr/bin/env python3
"""Part EF batch-38 (closure class 30345) machine audit - takeover lane.

Fail-closed SSOT aggregation over the published batch-38 evidence
(b39 pattern of Part EH audit_b39.py, adapted to batch-38):
  - input/batch-keys-b38.json    (targets SSOT, 49 fresh keys ai001..ai049)
  - output/status.log            (final drive snapshot, 81 lines)
  - output/raw/*.p1/p2.out       (98 raws, 2-pass fresh-cold exact replay @15M)
  - output/raw/*.truncated.*.out (7 historical P2 truncation artifacts,
                                  none carries a replay_done marker, none is
                                  evidence; published for the incident record)
  - sources/*                    (pinned maker inputs incl. canonical cache)

Differences from the b39 machine forced by the batch-38 records:
  - A4 expects exactly 105 files: 98 replay passes + 7 named truncated
    artifacts (pinned set); a truncated artifact must NOT carry replay_done.
  - A7 accepts a 4th status line class "P2-TRUNCATED-RETRY" (exactly 7 lines,
    one per truncated artifact, timestamp-consistent with the artifact name),
    and the final status.log carries 81 lines (49 PASS + 6 EXHAUSTED
    + 19 WIN-HALT + 7 P2-TRUNCATED-RETRY).
  - A2 targets 49 keys ai001..ai049 with probe_order {132..139, 141..181}
    (140 = prior batch-1 dual-class key b018, excluded from this batch as a
    prior probe-level unconsumed WIN), prior_packeted_excluded == {b018}.
  - A9 checks 50 pairs absent from the canonical cache: 49 targets + b018
    (the class-30345 unknown at selection was exactly these 50 children).

All other checks (any violation => exit 1, no batch-audit.json written):
integer semantics use Python ints; the batch-keys lo values are exact
(never JS-double rounded).
"""

import hashlib
import json
import os
import re
import sys

EXP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIN_BATCH_KEYS = "298071046bfba8473c5b3d6e0b6a30108697eb0899aed7c70fcb4c5343f7cb8d"
PIN_STATUS_LOG = "8ca390768e317b5fdf810767dbd6e7bc31790d58762701e71759b4883fd8e14f"
PIN_CANONICAL_CACHE = "fc3e4ac9052447158202f09d5efe05468dba32fe95ec90beaaa0a0de9d2c020f"
BUDGET = 15000000
SCHEMA_OUT = "n11-centralreply-closure-batch38-audit-v1"
SCRUTINY_GATE = "9193f5b6 (C++ scrutiny-owner gate; batch-38 verdicts are NOT consumed)"
TRUNCATED_ARTIFACTS = {
    "ai014.p2.truncated.073413.out",
    "ai024.p2.truncated.080131.out",
    "ai029.p2.truncated.081247.out",
    "ai030.p2.truncated.081247.out",
    "ai038.p2.truncated.082814.out",
    "ai040.p2.truncated.083709.out",
    "ai041.p2.truncated.083709.out",
}
STATUS_LINES = 81


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
    keys_path = os.path.join(inp, "batch-keys-b38.json")
    status_path = os.path.join(EXP, "output", "status.log")
    for p in (keys_path, status_path):
        if not os.path.isfile(p):
            fail("A1 missing file " + p)

    # A2 batch keys SSOT
    if sha256_file(keys_path) != PIN_BATCH_KEYS:
        fail("A2 batch-keys-b38.json sha256 drift")
    packet = json.loads(read_text(keys_path))
    if packet.get("schema") != "n11-centralreply-closure-batch38-keys-v1":
        fail("A2 schema drift: %r" % packet.get("schema"))
    if packet.get("target_key_count") != 49 or len(packet.get("keys", [])) != 49:
        fail("A2 target_key_count/keys mismatch")
    if packet.get("consumed_into_canonical_cache") is not False:
        fail("A2 consumed_into_canonical_cache must be false")
    prior = packet.get("prior_packeted_excluded", [])
    if len(prior) != 1 or prior[0].get("key_id") != "b018" \
            or prior[0].get("probe_order") != 140 \
            or prior[0].get("lo") != 1153204079095189504 \
            or prior[0].get("hi") != 65536 \
            or prior[0].get("budget_result_nodes") != "15000000,1,3549602":
        fail("A2 prior_packeted_excluded drift")
    keys = packet["keys"]
    ids = [k["key_id"] for k in keys]
    if len(set(ids)) != 49 or sorted(ids) != ["ai%03d" % i for i in range(1, 50)]:
        fail("A2 key_id set drift")
    if sorted(k["probe_order"] for k in keys) != \
            list(range(132, 140)) + list(range(141, 182)):
        fail("A2 probe_order set drift (expected 132..139 + 141..181)")

    # A3 pinned bytes recomputed (sources/ + the pinned scripts)
    pins = packet.get("pins", {})
    expected_pin_keys = {
        "batch1_batch_keys", "batch1_status", "canonical_cache",
        "closure_classes", "freshness_ranks1to12", "jsreplay",
        "prior_probe_universe", "quarantine", "refresh_summary",
        "runbatch", "worklist_class30345_extract",
    }
    if set(pins) != expected_pin_keys:
        fail("A3 pin key set drift: %r" % sorted(pins))
    pin2file = {
        "batch1_batch_keys": (src, "batch1-packet/batch-keys.json"),
        "batch1_status": (src, "batch1-packet/status.log"),
        "canonical_cache": (src, "canonical-cache-fc3e4ac9.cache"),
        "closure_classes": (src, "closure-classes.csv"),
        "freshness_ranks1to12": (src, "freshness-ranks1to12.csv"),
        "jsreplay": (os.path.join(EXP, "scripts"), "jsreplay.js"),
        "prior_probe_universe": (src, "prior-probe-universe.csv"),
        "quarantine": (src, "quarantine.json"),
        "refresh_summary": (src, "refresh-summary.json"),
        "worklist_class30345_extract": (src, "worklist-class30345-extract.csv"),
        "runbatch": (os.path.join(EXP, "scripts"), "runbatch.sh"),
    }
    for pk, (pdir, fname) in pin2file.items():
        p = os.path.join(pdir, fname)
        if not os.path.isfile(p):
            fail("A3 missing pinned file " + fname)
        if sha256_file(p) != pins[pk]:
            fail("A3 pin drift for %s (%s)" % (fname, pk))
    if pins["jsreplay"] != "845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df":
        fail("A3 jsreplay pin unexpected")
    if sha256_file(os.path.join(EXP, "scripts", "jsreplay.js")) != pins["jsreplay"]:
        fail("A3 jsreplay bytes drift")
    if pins["canonical_cache"] != PIN_CANONICAL_CACHE:
        fail("A3 canonical cache pin unexpected")

    # A4 raw set: 98 passes + exactly the named truncated artifacts
    raws = sorted(os.listdir(raw_dir))
    expect = sorted(list("%s.%s.out" % (i, p) for i in ids for p in ("p1", "p2"))
                    + list(TRUNCATED_ARTIFACTS))
    if raws != expect:
        fail("A4 output/raw file set drift (%d files)" % len(raws))
    for t in TRUNCATED_ARTIFACTS:
        txt = read_text(os.path.join(raw_dir, t))
        if "# replay_done" in txt:
            fail("A4 truncated artifact carries replay_done: " + t)

    # A7 status log structure
    if sha256_file(status_path) != PIN_STATUS_LOG:
        fail("A7 status.log sha256 drift")
    status_text = read_text(status_path)
    status_lines = [l for l in status_text.splitlines() if l.strip()]
    if len(status_lines) != STATUS_LINES:
        fail("A7 status.log must have %d lines, got %d" % (STATUS_LINES, len(status_lines)))
    pat_pass = re.compile(r"^(\S+) (ai\d{3}) PASS (%d),(\d),(\d+)$" % BUDGET)
    pat_exh = re.compile(r"^\S+ (ai\d{3}) EXHAUSTED %d,0,%d$" % (BUDGET, BUDGET))
    pat_win = re.compile(r"^\S+ (ai\d{3}) WIN-HALT$")
    pat_trunc = re.compile(r"^(\S+) (ai\d{3}) P2-TRUNCATED-RETRY$")
    seen_pass, seen_exh, seen_win, seen_trunc = {}, set(), set(), {}
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
        m = pat_trunc.match(l)
        if m:
            kid = m.group(2)
            if kid in seen_trunc:
                fail("A7 duplicate P2-TRUNCATED-RETRY line " + kid)
            seen_trunc[kid] = m.group(1)
            continue
        fail("A7 unaccounted status.log line: %r" % l)
    if len(seen_pass) != 49:
        fail("A7 PASS lines %d != 49" % len(seen_pass))
    if len(seen_trunc) != 7:
        fail("A7 P2-TRUNCATED-RETRY lines %d != 7" % len(seen_trunc))
    for kid, ts in seen_trunc.items():
        hhmmss = ts.split("T")[1].replace(":", "").split(".")[0][:6]
        cand = [t for t in TRUNCATED_ARTIFACTS
                if t.startswith(kid + ".p2.truncated." + hhmmss)]
        if not cand:
            fail("A7 truncated artifact not found for %s at %s" % (kid, hhmmss))

    # A5/A6/A8 per-key raw checks
    per_key = []
    counts = {"LOSS": 0, "EXHAUSTED": 0, "WIN": 0}
    total_nodes = 0
    exhausted_keys, win_keys, loss_keys = [], [], []
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
            parts[p] = [int(x) if i not in (0,) else x for i, x in enumerate(f)]
        r1, r2 = parts["p1"], parts["p2"]
        if [x for i, x in enumerate(r1) if i != 7] != [x for i, x in enumerate(r2) if i != 7]:
            fail("A6 %s p1/p2 not node-exact: %r vs %r" % (kid, r1, r2))
        if not (r1[0] == "0" and r1[1] == 5 and r1[3] == 0 and r1[4] == BUDGET):
            fail("A5 %s unexpected replay header fields %r" % (kid, r1))
        if r1[2] != k["legal"] or r1[8] != k["lo"] or r1[9] != k["hi"]:
            fail("A5 %s legal/lo/hi drift vs batch-keys" % kid)
        result, nodes = r1[5], r1[6]
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
        if result == 2:
            loss_keys.append(kid)
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
    if counts["EXHAUSTED"] != 6 or counts["WIN"] != 19 or counts["LOSS"] != 24:
        fail("A8 honest label counts drift: %r" % counts)

    # A9a closure-classes rank-12 anchor for class 30345 (SSOT tie)
    cc_lines = [l for l in read_text(os.path.join(src, "closure-classes.csv")).splitlines()
                if l.strip()]
    if cc_lines[0].split(",") != ["class_rank", "class_index", "class_lo", "class_hi",
                                 "unknown_now", "first_group_first", "first_group_third",
                                 "groups_served_count"]:
        fail("A9a closure-classes.csv header drift")
    rank12 = [l.split(",") for l in cc_lines[1:] if l.split(",")[0] == "12"]
    if len(rank12) != 1 or rank12[0][:5] != ["12", "30345", "1152922604118478848",
                                            "65536", "50"]:
        fail("A9a closure-classes rank-12 row drift: %r" % rank12)
    if any(k["class_mask"] != [1152922604118478848, 65536] for k in keys):
        fail("A9a key class_mask drift")
    if any(int(k.get("class_unknown_now_at_selection", -1)) != 50 for k in keys):
        fail("A9a key class_unknown_now_at_selection drift")

    # A9 canonical-cache absence (50 pairs: 49 targets + b018; maker G4 port)
    all_children = [(k["lo"], k["hi"]) for k in keys] + [
        (prior[0]["lo"], prior[0]["hi"])]
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
        fail("A9 canonical cache contains batch-38 pair(s): %r" % sorted(present))
    if n_cache_rows != packet["canonical_cache_s5verdict_rows"]:
        fail("A9 canonical cache row count drift %d != %r"
             % (n_cache_rows, packet["canonical_cache_s5verdict_rows"]))

    audit = {
        "batch": "batch-38",
        "batch_keys_b38_sha256": PIN_BATCH_KEYS,
        "claims": ("no closure, no coverage, no secured-coverage, no root outcome claimed; "
                   "standard 11x11 empty board and all 19 central-reply roots stay UNKNOWN; "
                   "nodes are bookkeeping"),
        "class_index": 30345,
        "class_mask": [1152922604118478848, 65536],
        "drive": ("2-pass fresh-cold exact replay, budget 15000000, order 0, "
                  "1 solver row / key / pass, drive step = 2 keys x 2 workers (2-core host), "
                  "WIN-CONTINUE single-drive design to 49/49 keys"),
        "part": "Part EF (takeover lane completed ai044..ai049)",
        "per_key": per_key,
        "pins": dict(pins),
        "reported_truncation_artifacts": sorted(TRUNCATED_ARTIFACTS),
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
            "class_30484_dual_class_children": {
                "ai044": "LOSS 5677449 (unconsumed honest label; future loss-only adoption candidate)",
                "ai048": "WIN 2232854 (unconsumed; scrutiny-owner C++ gate exclusive)",
                "note": ("the two class-30484 claim-reserved batch-38 children measured here "
                         "for the first time; both verdicts remain unconsumed"),
            },
        },
        "schema": SCHEMA_OUT,
        "selection": ("closure-classes 27e00b0d rank 12, class 30345 unknown_now 50 = "
                      "49 clean fresh targets ai001..ai049 (probe_order 132..139, 141..181) + "
                      "prior batch-1 dual-class key b018 (probe_order 140, probe-level "
                      "unconsumed WIN, excluded, same-condition re-probe prohibited); "
                      "ranks 1..11 machine-verified fresh-0 "
                      "(freshness-ranks1to12.csv e5f51717)"),
        "status_log_sha256": PIN_STATUS_LOG,
        "target_key_count": 49,
        "truncation_retries_status_lines": 7,
        "verdicts_consumed_into_canonical_cache": False,
    }
    out_path = os.path.join(EXP, "output", "batch-audit.json")
    blob = json.dumps(audit, sort_keys=True, indent=2) + "\n"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(blob)
    print("AUDIT-OK batch-38 class 30345: 49 keys, LOSS %d / EXHAUSTED %d / WIN %d, MISMATCH 0, "
          "truncation artifacts 7, total_nodes_single_pass %d, batch-audit.json sha256 %s"
          % (counts["LOSS"], counts["EXHAUSTED"], counts["WIN"], total_nodes,
             hashlib.sha256(blob.encode("utf-8")).hexdigest()))


if __name__ == "__main__":
    main()
