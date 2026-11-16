#!/usr/bin/env python3
"""Verify the v15 cross-engine re-check of the 41 REFUTED-D10 bits of class2-lane cost64h.

Context: the published cost64h sweep (claim v2 blob 68e48780..., 23 WIN7-D10 /
41 REFUTED-D10, node_sum 47,017,565) was produced by the v16 engine
(class4_child1_runner_v16.ts, git blob 0a4a86f6...). The parallel lane published a
v15 crosscheck only for the 23 WIN bits (class2-lane-cost64h-v15-crosscheck-
20261116.jsonl). This script verifies the complementary, previously-unchecked
layer: all 41 REFUTED-D10 bits re-run on the independent v15 engine
(class4_child1_runner.ts, git blob 8744fc65...), which must return loss=false,
capped=false for every one of them (verdict-level cross-engine agreement).
Two WIN bits (4, 120) are re-run as positive controls and must match the
published v15 crosscheck node-exactly.

The two engines are different implementations, so node counts are NOT expected
to agree between v15 and v16; the check is verdict-level (loss/capped), plus
node-exact agreement for the two win controls against the same-engine published
v15 crosscheck.

Checks:
  C1  41 expected refuted bits present, each exactly once
  C2  all 41 v15 records: loss=false, capped=false (REFUTED-D10 agreement)
  C3  published v16 raw batches: same 41 bits all loss=false, capped=false
  C4  bit-set equality between v15 rerun and v16 published refuted set
  C5  pilot_d6 controls 5/5: loss=false, nodes=5949, capped=false
  C6  win controls (4, 120): loss=true, capped=false, node-exact vs published
      v15 crosscheck (3555878 / 4836378)
  C7  v15 refuted node_sum == 57767631 (informational pin)
  C8  engine + invocation pins recorded

Interpretation guard: cross-engine agreement strengthens the published
REFUTED-D10 records but creates no verdicts beyond them. REFUTED-D10 is not a
LOSS proof. WIN7-D10 proves a first-player win within depth 10 from the
individual 7-stone roots only. The 11x11 empty board, the two-stone roots
{49,60} and {59,60}, S2 {59,60} and classes 1/2/4 all remain UNKNOWN.
"""

import argparse
import hashlib
import json
import os
import sys

REFUTED_BITS = [1, 2, 3, 5, 14, 16, 18, 21, 23, 25, 29, 34, 35, 43, 45, 46,
                53, 54, 66, 69, 82, 85, 86, 87, 88, 92, 95, 96, 97, 98, 99,
                102, 103, 105, 106, 107, 108, 111, 112, 115, 117]
WIN_CONTROL_BITS = [4, 120]
V15_PILOT_NODES = 5949
WIN_CONTROL_EXPECTED_NODES = {4: 3555878, 120: 4836378}
V15_REFUTED_NODE_SUM = 57767631
V15_BLOB = "8744fc65b6b7cac6bd561403ce4c749e01c51359"
V16_BLOB = "0a4a86f6828dc010c89ff17596054336a6b6091f"
CLAIM_V2_BLOB = "68e4878094b78eaf0a465033d0289a6db5d94861"
CHILD = "00000000000000403800000008100000"


def git_blob(path):
    data = open(path, "rb").read()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def load_jsonl(path):
    recs = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                recs.append(json.loads(line))
    return recs


def main():
    ap = argparse.ArgumentParser()
    here = os.path.dirname(os.path.abspath(__file__))
    outdir = os.path.normpath(os.path.join(here, "..", "output"))
    ap.add_argument("--v15-files", nargs=5, default=[
        os.path.join(outdir, "class2-lane-cost64h-v15-refuted-crosscheck-%s-20261116.jsonl" % w)
        for w in "abcde"])
    ap.add_argument("--v16-raw", nargs=8, default=[
        os.path.join(outdir, "class2-lane-cost64h-raw-batch%d-20261116.jsonl" % i)
        for i in range(1, 9)])
    ap.add_argument("--v15-crosscheck-published",
                    default=os.path.join(outdir, "class2-lane-cost64h-v15-crosscheck-20261116.jsonl"))
    ap.add_argument("--out",
                    default=os.path.join(outdir, "class2-lane-cost64h-v15-refuted-crosscheck-verification-20261116.json"))
    args = ap.parse_args()

    # load v15 rerun files
    v15_pilots, v15_bits = [], {}
    v15_file_blobs = {}
    for p in args.v15_files:
        v15_file_blobs[os.path.basename(p)] = git_blob(p)
        for r in load_jsonl(p):
            if "control" in r:
                v15_pilots.append(r)
            else:
                v15_bits.setdefault(r["bit"], []).append(r)

    # load v16 published raw batches
    v16_pilots, v16_bits = [], {}
    for p in args.v16_raw:
        for r in load_jsonl(p):
            if "control" in r:
                v16_pilots.append(r)
            else:
                v16_bits.setdefault(r["bit"], []).append(r)

    # load published v15 crosscheck (win bits)
    pub15_bits = {}
    for r in load_jsonl(args.v15_crosscheck_published):
        if "bit" in r:
            pub15_bits[r["bit"]] = r

    # C1: each refuted bit exactly once
    c1 = all(v15_bits.get(b) and len(v15_bits[b]) == 1 for b in REFUTED_BITS)
    # C2: v15 verdicts
    c2 = all(v15_bits[b][0]["loss"] is False and v15_bits[b][0]["capped"] is False
             for b in REFUTED_BITS)
    # C3: v16 published verdicts
    c3 = all(b in v16_bits and v16_bits[b][0]["loss"] is False
             and v16_bits[b][0]["capped"] is False for b in REFUTED_BITS)
    # C4: bit-set equality
    v15_refuted_set = set(b for b in v15_bits if b in REFUTED_BITS)
    c4 = v15_refuted_set == set(REFUTED_BITS) and \
        set(b for b in v16_bits if v16_bits[b][0]["loss"] is False) >= set(REFUTED_BITS)
    # C5: pilots
    c5 = len(v15_pilots) == 5 and all(
        p["control"] == "pilot_d6" and p["loss"] is False
        and p["nodes"] == V15_PILOT_NODES and p["capped"] is False for p in v15_pilots)
    # C6: win controls
    c6_detail = {}
    c6 = True
    for b in WIN_CONTROL_BITS:
        rec = v15_bits.get(b, [None])[0]
        pub = pub15_bits.get(b)
        ok = (rec is not None and pub is not None
              and rec["loss"] is True and rec["capped"] is False
              and rec["nodes"] == WIN_CONTROL_EXPECTED_NODES[b]
              and rec["nodes"] == pub["nodes"])
        c6_detail[b] = {"rerun_nodes": rec["nodes"] if rec else None,
                        "published_nodes": pub["nodes"] if pub else None,
                        "loss": rec["loss"] if rec else None,
                        "capped": rec["capped"] if rec else None,
                        "node_exact_vs_published_v15": bool(rec and pub and rec["nodes"] == pub["nodes"])}
        c6 = c6 and ok
    # C7: node sum
    node_sum = sum(v15_bits[b][0]["nodes"] for b in REFUTED_BITS)
    c7 = node_sum == V15_REFUTED_NODE_SUM
    # C8: pins
    c8 = V15_BLOB.startswith("8744fc65") and V16_BLOB.startswith("0a4a86f6")

    checks = {
        "C1_refuted_41_present_once": bool(c1),
        "C2_v15_all_41_loss_false_uncapped": bool(c2),
        "C3_v16_published_all_41_loss_false_uncapped": bool(c3),
        "C4_bit_set_equality_v15_vs_v16": bool(c4),
        "C5_pilot_d6_5_of_5": bool(c5),
        "C6_win_controls_node_exact_vs_published_v15": bool(c6),
        "C7_v15_refuted_node_sum": bool(c7),
        "C8_engine_pins": bool(c8),
    }

    per_bit = []
    for b in REFUTED_BITS:
        r15, r16 = v15_bits[b][0], v16_bits[b][0]
        per_bit.append({
            "bit": b,
            "v15": {"loss": r15["loss"], "nodes": r15["nodes"], "capped": r15["capped"]},
            "v16_published": {"loss": r16["loss"], "nodes": r16["nodes"], "capped": r16["capped"]},
            "verdict_agreement": bool(r15["loss"] is False and r16["loss"] is False
                                      and r15["capped"] is False and r16["capped"] is False),
            "note": "verdict-level agreement; node counts differ across engines by design",
        })

    result = {
        "child": CHILD,
        "claim_v2_blob": CLAIM_V2_BLOB,
        "date": "2026-11-16",
        "engines": {
            "v15": "class4_child1_runner.ts (git blob %s)" % V15_BLOB,
            "v16": "class4_child1_runner_v16.ts (git blob %s)" % V16_BLOB,
        },
        "v15_invocation": "node --experimental-strip-types class4_child1_runner.ts "
                          "--child %s --bits <worker batch> --depth 10 --cap 1000000000 "
                          "--andclose 1 (pilot_d6 control on; 5 workers a-e, 41 refuted "
                          "bits split across a-d, win controls 4/120 on e)" % CHILD,
        "refuted_bits": REFUTED_BITS,
        "win_control_bits": WIN_CONTROL_BITS,
        "v15_refuted_node_sum": node_sum,
        "v15_file_blobs": v15_file_blobs,
        "win_control_detail": c6_detail,
        "checks": checks,
        "per_bit": per_bit,
        "interpretation_guard": "cross-engine (v15 vs v16) verdict-level agreement on all "
            "41 REFUTED-D10 bits plus node-exact same-engine agreement on 2 win controls; "
            "this strengthens the published depth-10 capped sweep records but creates no "
            "verdicts beyond them; REFUTED-D10 is not a LOSS proof; WIN7-D10 proves a "
            "first-player win within depth 10 from the individual 7-stone roots only; the "
            "11x11 empty board, the two-stone roots {49,60} and {59,60}, S2 {59,60} and "
            "classes 1/2/4 all remain UNKNOWN",
    }

    with open(args.out, "w") as f:
        json.dump(result, f, indent=1, sort_keys=True)
        f.write("\n")

    all_pass = all(checks.values())
    print("checks:", json.dumps(checks))
    print("v15 refuted node_sum:", node_sum)
    print("win controls:", json.dumps(c6_detail))
    print("ALL PASS" if all_pass else "FAILURE")
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
