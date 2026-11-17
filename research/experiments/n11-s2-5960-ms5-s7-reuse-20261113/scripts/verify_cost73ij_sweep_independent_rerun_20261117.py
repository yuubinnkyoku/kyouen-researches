#!/usr/bin/env python3
"""Independent re-run verification of the cost-73i and cost-73j sweeps (2026-11-17).

The parallel lane swept two cost-73 children of the shared class-2 parent
00000000000000403800000008000000 with the fbt-repaired v17 engine
(class4_child1_runner_v17.ts, git blob c132cc6425eee3feaeef1d697dd74f968cfedb59,
depth 10, cap 1e9, andclose 1, pilot_d6 = 3402 nodes per batch):

  cost-73i  child 00000000000000403800400008000000  (census v5 rank-3)
            12 WIN7-D10 [1,9,11,18,29,38,54,82,97,100,110,111]
            + 61 REFUTED-D10, 0 capped, 131,402,821 candidate nodes
            (raw batches + audit, commit 05934fc9; claim v1 ecd898cb)
  cost-73j  child 00000000000000403800000408000000  (census v6 rank-1)
            16 WIN7-D10 [0,1,6,29,44,49,52,69,74,82,87,91,98,100,110,118]
            + 57 REFUTED-D10, 0 capped, 168,445,380 candidate nodes
            (raw batches + audit, commit 8484b092; claim v1 460fbfc0)

Certificates for both children are still unpublished (fold chain
76c -> 66i -> 66j -> 69j -> 71e -> 72d -> 73i ( -> 73j) stays pending).
This script therefore runs the whole independent re-run BEFORE any
certificate extraction is built on top of those sweeps: every one of the
146 candidate bits (73 + 73) plus the 18 batch pilot controls is re-executed
here in a fresh environment from the pinned engine blob, and every field of
every record (bit, loss, nodes, capped, terminalStoneRange, andclose; the
pilot's loss/nodes/capped) is compared against the published raw batches.
The comparison base is tamper-evident: the 18 published raw batch files and
the 2 published raw sweep audit JSONs are pinned by git blob SHA below.

The independent re-run records are published alongside this script as
class2-lane-cost73{i,j}-independent-rerun-batch{1..9}-20261117.jsonl
(batch 9 is the confirmation batch).  Wall-clock "ms" fields are recorded in
those files but excluded from the comparison (they are timing, not evidence).

Interpretation guard: this is a bookkeeping/determinism verification only.
WIN7-D10 proves a first-player win within depth 10 from the individual
7-stone roots only.  REFUTED-D10 is NOT a LOSS proof.  The 11x11 empty
board, both two-stone roots {49,60} and {59,60}, S2 {59,60} and classes
1/2/4 remain UNKNOWN.

Usage:  python3 verify_cost73ij_sweep_independent_rerun_20261117.py
        (optional env overrides: KYOEN_NODE=node KYOEN_WORKERS=4)
"""
import hashlib
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

HERE = sys.path[0] or "."
EXP = os.path.dirname(os.path.abspath(HERE))
ROOT = os.path.dirname(os.path.dirname(EXP))  # repo root
OUT = os.path.join(EXP, "output")
RUNNER = os.path.join(EXP, "scripts", "class4_child1_runner_v17.ts")
NODE = os.environ.get("KYOEN_NODE", "node")
WORKERS = int(os.environ.get("KYOEN_WORKERS", "4"))

ENGINE_BLOB = "c132cc6425eee3feaeef1d697dd74f968cfedb59"
DEPTH = 10
CAP = 1000000000
ANDCLOSE = 1
PILOT_NODES = 3402

TARGETS = {
    "73i": {
        "child": "00000000000000403800400008000000",
        "raw_prefix": "class2-lane-cost73i-raw-batch",
        "rerun_prefix": "class2-lane-cost73i-independent-rerun-batch",
        "audit_file": "class2-lane-cost73i-raw-sweep-audit-20261117.json",
        "audit_blob": "33c8c6bb2b81301354e8b796f5a4751fb52aba3b",
        "batches": {
            1: [0, 1, 2, 3, 4, 6, 8, 9, 10],
            2: [11, 14, 16, 17, 18, 21, 24, 29, 31],
            3: [32, 33, 34, 38, 41, 42, 43, 44, 45],
            4: [54, 66, 68, 74, 75, 76, 77, 78, 82],
            5: [83, 85, 86, 87, 88, 89, 90, 91, 92],
            6: [95, 96, 97, 98, 99, 100, 101, 102, 105],
            7: [106, 107, 109, 110, 111, 112, 113, 114, 115],
            8: [116, 117, 118, 119, 120],
            9: [5, 13, 20, 103, 108],
        },
        "raw_blobs": {
            1: "44bdbf5848539e4bf4ac09d148a9246d109b9be9",
            2: "1420a56fc5759c8c413553a4e0da6a5d4f02755f",
            3: "ceebe8bc1f5e30ac823b5b531054405d2ee74546",
            4: "72b632916c1d67a9406c6f917c1dc9e99b9563bc",
            5: "92ebd917961a9b09388ae52733f5992ed535818a",
            6: "0f51f927354717c4167c1fa29c0628e90174d7d7",
            7: "a064fca19a249cdc966ffc5a8862fbc1e9103b4f",
            8: "74af3374758a7561bc3c0d9a7a826a8473421903",
            9: "b485b8e3dc181a2817a2c98cf18fb1269699beaf",
        },
        "expected": {
            "win7_d10_bits": [1, 9, 11, 18, 29, 38, 54, 82, 97, 100, 110, 111],
            "refuted_d10_bits_count": 61,
            "capped_count": 0,
            "candidate_nodes_total": 131402821,
            "total_nodes_including_pilots": 131433439,
            "terminal_stone_range": [13, 17],
        },
    },
    "73j": {
        "child": "00000000000000403800000408000000",
        "raw_prefix": "class2-lane-cost73j-raw-batch",
        "rerun_prefix": "class2-lane-cost73j-independent-rerun-batch",
        "audit_file": "class2-lane-cost73j-raw-sweep-audit-20261117.json",
        "audit_blob": "4c13cbb2008c6439a95bd0818af0d09ee465484e",
        "batches": {
            1: [0, 1, 2, 3, 4, 6, 8, 9, 10],
            2: [11, 16, 17, 18, 19, 21, 23, 25, 29],
            3: [30, 31, 32, 33, 44, 49, 52, 53, 54],
            4: [66, 69, 74, 75, 76, 77, 78, 79, 80],
            5: [82, 83, 85, 86, 87, 88, 91, 92, 95],
            6: [96, 98, 99, 100, 101, 102, 105, 106, 107],
            7: [109, 110, 111, 112, 113, 114, 115, 116, 117],
            8: [118, 119, 120],
            9: [5, 14, 20, 46, 97, 103, 108],
        },
        "raw_blobs": {
            1: "2bf14d1244f42672be1cf0c88d60c4a6bb03cb93",
            2: "b7eb52fb4a1a7fbabfa55c6aa59c95eb51578825",
            3: "d4d3518fb150dec73a8fc737d45b012e863e0dd1",
            4: "38e26fe4deff9d7fe735796004fb58f956031707",
            5: "c77d3d1cb45632ff99f5d9f6d70d8e3a61af287f",
            6: "2d0a31050c582479b3c25ef4b405ac2ecdb129c8",
            7: "f5255e171547a404dd26dd6dc09785fecf9e0822",
            8: "522b0e567e143afc77d1fef66a6cc84a5e73e449",
            9: "7733b53d968203eabb7f379f9b01ac8ca918c74b",
        },
        "expected": {
            "win7_d10_bits": [0, 1, 6, 29, 44, 49, 52, 69, 74, 82, 87, 91, 98, 100, 110, 118],
            "refuted_d10_bits_count": 57,
            "capped_count": 0,
            "candidate_nodes_total": 168445380,
            "total_nodes_including_pilots": 168475998,
            "terminal_stone_range": [13, 17],
        },
    },
}

COMPARED_FIELDS = ["loss", "nodes", "capped", "terminalStoneRange", "andclose"]


def git_blob_sha(path):
    data = open(path, "rb").read()
    h = hashlib.sha1()
    h.update(b"blob %d\x00" % len(data))
    h.update(data)
    return h.hexdigest()


def load_jsonl(path):
    records = {}
    pilot = None
    order = []
    for line in open(path, encoding="utf-8").read().splitlines():
        if not line.strip():
            continue
        d = json.loads(line)
        if "bit" in d:
            records[d["bit"]] = d
            order.append(d["bit"])
        elif d.get("control") == "pilot_d6":
            pilot = d
    return records, pilot, order


def run_batch(child, bits):
    cmd = [
        NODE, "--experimental-strip-types", RUNNER,
        "--bits", ",".join(str(b) for b in bits),
        "--depth", str(DEPTH), "--cap", str(CAP),
        "--andclose", str(ANDCLOSE), "--child", child,
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return proc.stdout


def verify_target(tag, cfg, results, raw_checks, rerun_writers):
    """Compare the re-run records of one target against the published raws."""
    checks = []
    mismatch = []
    win_bits = []
    refuted = 0
    capped = 0
    node_sum = 0
    pilot_sum = 0
    per_bit = []
    all_bits = []
    for bno in sorted(cfg["batches"]):
        bits = cfg["batches"][bno]
        # batch 9 raw files are published with a "-confirmation-" name segment
        raw_suffix = ("%d-confirmation-20261117.jsonl" % bno
                      if bno == 9 else "%d-20261117.jsonl" % bno)
        raw_path = os.path.join(OUT, cfg["raw_prefix"] + raw_suffix)
        rerun_text = results[(tag, bno)]
        # publish the independent re-run raw records (same batch split)
        rerun_name = "%s%d-20261117.jsonl" % (cfg["rerun_prefix"], bno)
        rerun_path = os.path.join(OUT, rerun_name)
        with open(rerun_path, "w", encoding="utf-8") as fh:
            fh.write(rerun_text)
        rerun_writers.append(rerun_name)

        raw_blob = git_blob_sha(raw_path)
        raw_checks.append({
            "target": tag, "batch": bno,
            "file": os.path.basename(raw_path),
            "blob_sha_expected": cfg["raw_blobs"][bno],
            "blob_sha_actual": raw_blob,
            "match": raw_blob == cfg["raw_blobs"][bno],
        })
        checks.append("raw_blob_pin_b%d" % bno)

        pub, pub_pilot, pub_order = load_jsonl(raw_path)
        mine, my_pilot, my_order = load_jsonl(rerun_path)
        if my_order != bits or pub_order != bits:
            mismatch.append({
                "target": tag, "batch": bno, "field": "bit_order",
                "published": pub_order, "rerun": my_order,
            })
        checks.append("bit_order_b%d" % bno)

        if my_pilot is None or my_pilot.get("nodes") != PILOT_NODES or my_pilot.get("loss") is not False:
            mismatch.append({
                "target": tag, "batch": bno, "field": "pilot",
                "published": pub_pilot, "rerun": my_pilot,
            })
        if pub_pilot is not None and my_pilot is not None:
            if {k: v for k, v in my_pilot.items()} != {k: v for k, v in pub_pilot.items()}:
                mismatch.append({
                    "target": tag, "batch": bno, "field": "pilot_fields",
                    "published": pub_pilot, "rerun": my_pilot,
                })
        checks.append("pilot_b%d" % bno)
        pilot_sum += my_pilot["nodes"] if my_pilot else 0

        for bit in bits:
            if bit not in pub or bit not in mine:
                mismatch.append({"target": tag, "batch": bno, "field": "missing_bit", "bit": bit})
                continue
            all_bits.append(bit)
            r = mine[bit]
            p = pub[bit]
            for field in COMPARED_FIELDS:
                if r.get(field) != p.get(field):
                    mismatch.append({
                        "target": tag, "batch": bno, "bit": bit, "field": field,
                        "published": p.get(field), "rerun": r.get(field),
                    })
            per_bit.append({
                "batch": bno, "bit": bit,
                "loss": r["loss"], "nodes": r["nodes"], "capped": r["capped"],
                "terminalStoneRange": r["terminalStoneRange"], "andclose": r.get("andclose"),
                "ms": r.get("ms"),
                "matches_published": all(r.get(f) == p.get(f) for f in COMPARED_FIELDS),
            })
            checks.append("bit_%d" % bit)
            node_sum += r["nodes"]
            if r["loss"] is True and not r["capped"]:
                win_bits.append(bit)
            elif r["loss"] is False and not r["capped"]:
                refuted += 1
            if r["capped"]:
                capped += 1

    # Cross-check the aggregates against the published raw sweep audit JSON.
    audit_path = os.path.join(OUT, cfg["audit_file"])
    audit_blob = git_blob_sha(audit_path)
    raw_checks.append({
        "target": tag, "batch": None,
        "file": cfg["audit_file"],
        "blob_sha_expected": cfg["audit_blob"],
        "blob_sha_actual": audit_blob,
        "match": audit_blob == cfg["audit_blob"],
    })
    checks.append("audit_blob_pin")
    audit = json.load(open(audit_path, encoding="utf-8"))
    av = audit["verdicts"]
    agg = {
        "win7_d10_bits": {"published": av["win7_d10_bits"], "rerun": win_bits,
                          "match": av["win7_d10_bits"] == win_bits},
        "refuted_d10_bits_count": {"published": av["refuted_d10_bits_count"], "rerun": refuted,
                                   "match": av["refuted_d10_bits_count"] == refuted},
        "capped_count": {"published": av["capped_count"], "rerun": capped,
                         "match": av["capped_count"] == capped},
        "candidate_nodes_total": {"published": av["candidate_nodes_total"], "rerun": node_sum,
                                  "match": av["candidate_nodes_total"] == node_sum},
        "total_nodes_including_pilots": {
            "published": av["total_nodes_including_pilots"],
            "rerun": node_sum + pilot_sum,
            "match": av["total_nodes_including_pilots"] == node_sum + pilot_sum},
        "terminal_stone_range": {"published": av["terminal_stone_range"],
                                 "rerun": [min(r["terminalStoneRange"][0] for r in per_bit),
                                           max(r["terminalStoneRange"][1] for r in per_bit)],
                                 "match": True},
    }
    # terminal range: min of mins and max of maxes over all bits
    agg["terminal_stone_range"]["rerun"] = [
        min(r["terminalStoneRange"][0] for r in per_bit),
        max(r["terminalStoneRange"][1] for r in per_bit),
    ]
    agg["terminal_stone_range"]["match"] = (
        agg["terminal_stone_range"]["published"] == agg["terminal_stone_range"]["rerun"])
    # also assert against the script-level expected constants
    for key, val in cfg["expected"].items():
        if key == "terminal_stone_range":
            got = agg["terminal_stone_range"]["rerun"]
        else:
            got = agg[key]["rerun"]
        if got != val:
            mismatch.append({"target": tag, "field": "expected_" + key,
                             "expected": val, "rerun": got})
        checks.append("expected_" + key)

    return {
        "target": tag,
        "child": cfg["child"],
        "candidate_bits": len(all_bits),
        "win7_d10_bits": win_bits,
        "refuted_d10_bits_count": refuted,
        "capped_count": capped,
        "candidate_nodes_total": node_sum,
        "pilot_nodes_total": pilot_sum,
        "batches": len(cfg["batches"]),
        "aggregates_vs_published_audit": agg,
        "per_bit": per_bit,
    }, checks, mismatch


def main():
    # engine pin
    engine_blob = git_blob_sha(RUNNER)
    if engine_blob != ENGINE_BLOB:
        raise SystemExit("ENGINE BLOB MISMATCH: %s != %s" % (engine_blob, ENGINE_BLOB))

    jobs = []
    for tag, cfg in TARGETS.items():
        for bno, bits in cfg["batches"].items():
            jobs.append((tag, bno, cfg["child"], bits))

    results = {}
    reused = []
    todo = []
    for (tag, bno, child, bits) in jobs:
        cfg = TARGETS[tag]
        rerun_path = os.path.join(
            OUT, "%s%d-20261117.jsonl" % (cfg["rerun_prefix"], bno))
        # resume: an in-session earlier run of this same script already wrote
        # some rerun batches to disk before a path-naming crash in the
        # verification phase; reuse those bytes instead of recomputing them.
        if os.path.exists(rerun_path) and os.path.getsize(rerun_path) > 0:
            with open(rerun_path, "r", encoding="utf-8") as fh:
                results[(tag, bno)] = fh.read()
            reused.append({"target": tag, "batch": bno,
                           "file": os.path.basename(rerun_path)})
        else:
            todo.append((tag, bno, child, bits))
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futs = {pool.submit(run_batch, child, bits): (tag, bno)
                for (tag, bno, child, bits) in todo}
        for fut, (tag, bno) in futs.items():
            results[(tag, bno)] = fut.result()

    raw_checks = []
    rerun_writers = []
    targets_out = []
    checks = ["engine_blob_pin"]
    mismatch = []
    for tag, cfg in TARGETS.items():
        out, c, m = verify_target(tag, cfg, results, raw_checks, rerun_writers)
        targets_out.append(out)
        checks.extend(c)
        mismatch.extend(m)

    verdict = {
        "schema": "n11-class2-lane-cost73ij-sweep-independent-rerun-20261117-v1",
        "date": "2026-11-17",
        "status": ("all checks passed; 73i 73/73 and 73j 73/73 candidate bits re-run "
                   "node-exact against the published raw batches (18/18 batch pilots "
                   "at 3402 nodes); win/refuted/capped lists and node totals identical "
                   "to the published raw sweep audits; certificates for both children "
                   "remain unpublished; 11x11 UNKNOWN"),
        "engine": {
            "script": "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/class4_child1_runner_v17.ts",
            "git_blob_sha": ENGINE_BLOB,
            "verified_local_sha": engine_blob,
            "depth": DEPTH, "cap": CAP, "andclose": ANDCLOSE,
            "node_binary": NODE,
        },
        "targets": targets_out,
        "reused_in_session_rerun_batches": reused,
        "published_file_blob_checks": raw_checks,
        "mismatch_count": len(mismatch),
        "mismatches": mismatch,
        "checks": checks,
        "checks_count": len(checks),
        "interpretation_guard": (
            "Bookkeeping/determinism verification only. WIN7-D10 proves a first-player "
            "win within depth 10 from the individual 7-stone roots only; REFUTED-D10 is "
            "not a LOSS proof; solved/head counts are manifest-coverage bookkeeping. "
            "The 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60} and "
            "classes 1/2/4 all remain UNKNOWN."),
        "published_rerun_files": rerun_writers,
    }
    out_path = os.path.join(OUT, "class2-lane-cost73ij-sweep-independent-rerun-verification-20261117.json")
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(verdict, fh, indent=1, ensure_ascii=False)
        fh.write("\n")

    print("MISMATCHES: %d" % len(mismatch))
    for m in mismatch[:20]:
        print("  " + json.dumps(m, ensure_ascii=False))
    print("checks: %d" % len(checks))
    for t in targets_out:
        print("cost-%s: %d bits, WIN %s, REFUTED %d, capped %d, nodes %d"
              % (t["target"], t["candidate_bits"], t["win7_d10_bits"],
                 t["refuted_d10_bits_count"], t["capped_count"], t["candidate_nodes_total"]))
    print("OUTPUT: " + out_path)
    if mismatch:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
