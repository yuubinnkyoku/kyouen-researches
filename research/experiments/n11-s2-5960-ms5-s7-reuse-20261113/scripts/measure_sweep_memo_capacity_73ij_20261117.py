#!/usr/bin/env python3
"""Sweep-memo capacity measurement for the v17 external sweeps (2026-11-17).

Published alongside this script:
  output/class2-lane-sweep-memo-capacity-73ij-20261117.json

Motivation.  The external depth-10 candidate sweep engine
class4_child1_runner_v17.ts (git blob c132cc6425eee3feaeef1d697dd74f968cfedb59)
allocates a per-candidate position memo with MS=1<<18 slots and 64-probe
linear probing (memoEntry silently skips storing on chain exhaustion,
memoFind then treats the entry as absent - sound, but it costs
recomputation).  The published cost-73i and cost-73j sweeps ran that
verbatim engine: 131,402,821 + 168,445,380 candidate nodes.  The extraction
lane measured the same-day that an MS=1<<23/24 extractor memo cuts
extraction cost by ~45%; this script measures the sweep engine analogously:
it re-runs both published sweeps with a one-line MS-substituted variant
(`const MS = 1 << 18` -> `const MS = 1 << N` at line 54; no other byte
differs) and verifies verdict invariance on every one of the 146 candidate
bits (loss, capped, terminalStoneRange) plus the win/refuted bit lists.

Expected results (embedded; a re-run must reproduce them):
  - fidelity control: verbatim engine on 73i batch 1 is node-exact against
    the published raw batch (9 bits + pilot_d6 = 3402 nodes).
  - pilot capacity probe: the runner's own d6 control aborts at MS=1<<24
    with nodes=3287 (vs 3402 verbatim), i.e. the verbatim MS=1<<18 memo is
    lossy even at ~1% load.
  - 73i at MS=1<<23: 58,352,152 nodes (0.4441x), 0 verdict mismatches;
    at MS=1<<24: 58,334,444 (0.4439x), 0 mismatches.
  - 73j at MS=1<<23: 57,496,088 nodes (0.3413x), 0 mismatches.
  - sensitivity (fresh single bit): 73i bit 78  6,791,073 (published ms18)
    -> 1,917,186 (ms20) -> 1,733,674 (ms21) -> 1,703,113 (ms22)
    -> 1,701,662 (ms23) -> 1,701,638 (ms24); 73i bit 101 184,771
    -> 166,807 -> 166,097 -> 166,054 -> 166,054 -> 166,054.

DETERMINISM CAVEAT (must be respected by any future lane): the published
raw batches, audits and the published independent rerun are pinned to the
verbatim engine with pilot_d6 = 3402.  MS variants change node counts and
the pilot value, so they can only serve FUTURE sweeps, after re-calibrating
the pilot constant and pinning the new engine blob.  No published record is
replaced by this measurement.

Interpretation guard: measurement only; no new WIN/LOSS verdicts; the
published verdicts (73i: 12 WIN7-D10 + 61 REFUTED-D10; 73j: 16 WIN7-D10 +
57 REFUTED-D10; 0 capped each) are unchanged and were re-confirmed
bit-by-bit.  WIN7-D10 proves a first-player win within depth 10 from the
individual 7-stone roots only; REFUTED-D10 is not a LOSS proof.  The 11x11
empty board, both two-stone roots {49,60} and {59,60}, S2 {59,60} and
classes 1/2/4 all remain UNKNOWN.

Usage:  python3 measure_sweep_memo_capacity_73ij_20261117.py
        (env: KYOEN_NODE=node KYOEN_WORKERS=2; a full re-run takes roughly
        15-20 min on 2 cores; MS=1<<24 needs a sequential worker and about
        700 MB peak; MS=1<<25 does not fit a 1 GB cgroup)
"""
import hashlib
import json
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

HERE = sys.path[0] or "."
EXP = os.path.dirname(os.path.abspath(HERE))
OUT = os.path.join(EXP, "output")
WORK = os.path.join(OUT, "sweep_memo_capacity_73ij_work")
NODE = os.environ.get("KYOEN_NODE", "node")
WORKERS = int(os.environ.get("KYOEN_WORKERS", "2"))

RUNNER = os.path.join(HERE, "class4_child1_runner_v17.ts")
ENGINE_BLOB = "c132cc6425eee3feaeef1d697dd74f968cfedb59"
VERBATIM_LINE = "  const MS = 1 << 18, MM = MS - 1;"

DEPTH = 10
CAP = 1000000000
ANDCLOSE = 1

TARGETS = {
    "73i": {
        "child": "00000000000000403800400008000000",
        "raw_prefix": "class2-lane-cost73i-raw-batch",
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
        "win7_d10_bits": [1, 9, 11, 18, 29, 38, 54, 82, 97, 100, 110, 111],
        "published_total_nodes": 131402821,
    },
    "73j": {
        "child": "00000000000000403800000408000000",
        "raw_prefix": "class2-lane-cost73j-raw-batch",
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
        "win7_d10_bits": [0, 1, 6, 29, 44, 49, 52, 69, 74, 82, 87, 91, 98, 100, 110, 118],
        "published_total_nodes": 168445380,
    },
}

EXPECTED = {
    "73i": {"ms23_total": 58352152, "ms23_ratio": 0.4441,
            "ms24_total": 58334444, "ms24_ratio": 0.4439},
    "73j": {"ms23_total": 57496088, "ms23_ratio": 0.3413},
    "pilot_ms24": 3287,
    "sensitivity": {
        78: {20: 1917186, 21: 1733674, 22: 1703113, 23: 1701662, 24: 1701638},
        101: {20: 166807, 21: 166097, 22: 166054, 23: 166054, 24: 166054},
    },
    "published_nodes": {78: 6791073, 101: 184771},
}


def git_blob_sha(path):
    data = open(path, "rb").read()
    h = hashlib.sha1()
    h.update(b"blob %d\x00" % len(data))
    h.update(data)
    return h.hexdigest()


def make_variant(ms_shift):
    """One-line MS substitution; asserts the diff is exactly that line."""
    os.makedirs(WORK, exist_ok=True)
    src = open(RUNNER, "r", encoding="utf-8").read()
    if VERBATIM_LINE not in src:
        raise SystemExit("verbatim MS line not found in runner")
    dst = os.path.join(WORK, "class4_child1_runner_v17_ms%d.ts" % ms_shift)
    with open(dst, "w", encoding="utf-8") as fh:
        fh.write(src.replace(
            VERBATIM_LINE, "  const MS = 1 << %d, MM = MS - 1;" % ms_shift))
    a = [l for l in src.splitlines() if "const MS" not in l]
    b = [l for l in open(dst, encoding="utf-8").read().splitlines()
         if "const MS" not in l]
    if a != b:
        raise SystemExit("variant ms%d differs by more than the MS line" % ms_shift)
    return dst


def run_batch(runner, child, bits, tag, nocontrol=True):
    """Run one batch; returns dict bit -> record. Resumes from disk."""
    path = os.path.join(WORK, tag + ".jsonl")
    if not (os.path.exists(path) and os.path.getsize(path) > 0):
        cmd = [NODE, "--experimental-strip-types", runner,
               "--bits", ",".join(str(b) for b in bits),
               "--depth", str(DEPTH), "--cap", str(CAP),
               "--andclose", str(ANDCLOSE)]
        if nocontrol:
            cmd.append("--nocontrol")
        cmd += ["--child", child]
        proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(proc.stdout)
    recs = {}
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        d = json.loads(line)
        if "bit" in d:
            recs[d["bit"]] = d
    return recs


def load_published(tag):
    cfg = TARGETS[tag]
    recs = {}
    checks = []
    for bno in sorted(cfg["batches"]):
        suffix = ("%d-confirmation-20261117.jsonl" % bno
                  if bno == 9 else "%d-20261117.jsonl" % bno)
        raw_path = os.path.join(OUT, cfg["raw_prefix"] + suffix)
        actual = git_blob_sha(raw_path)
        checks.append(actual == cfg["raw_blobs"][bno])
        for line in open(raw_path, encoding="utf-8"):
            line = line.strip()
            if not line:
                continue
            d = json.loads(line)
            if "bit" in d:
                recs[d["bit"]] = d
    return recs, all(checks)


def compare(tag, published, measured):
    mismatches = []
    total_pub = 0
    total_new = 0
    per_bit = []
    for b in sorted(published):
        p = published[b]
        q = measured.get(b)
        if q is None:
            mismatches.append({"bit": b, "field": "missing"})
            continue
        for field in ("loss", "capped", "terminalStoneRange"):
            if p.get(field) != q.get(field):
                mismatches.append({"bit": b, "field": field,
                                   "published": p.get(field), "rerun": q.get(field)})
        total_pub += p["nodes"]
        total_new += q["nodes"]
        per_bit.append({"bit": b, "loss": q["loss"], "capped": q["capped"],
                        "published_nodes": p["nodes"], "nodes": q["nodes"],
                        "ratio": round(q["nodes"] / p["nodes"], 4)})
    win = sorted([b for b in measured
                  if measured[b]["loss"] is True and not measured[b]["capped"]])
    return {"total_published": total_pub, "total_measured": total_new,
            "ratio": round(total_new / total_pub, 4),
            "win_bits": win, "mismatches": mismatches, "per_bit": per_bit}


def main():
    os.makedirs(WORK, exist_ok=True)
    engine_blob = git_blob_sha(RUNNER)
    if engine_blob != ENGINE_BLOB:
        raise SystemExit("ENGINE BLOB MISMATCH: %s" % engine_blob)

    failures = []
    def expect(name, got, want):
        if got != want:
            failures.append({"check": name, "expected": want, "got": got})

    # 1) fidelity control: verbatim engine, 73i batch 1, default pilot control ON
    ctrl = run_batch(RUNNER, TARGETS["73i"]["child"], TARGETS["73i"]["batches"][1],
                     "control_73i_b1_verbatim", nocontrol=False)
    pub73i, pins_i = load_published("73i")
    pub73j, pins_j = load_published("73j")
    expect("raw_pins_73i", pins_i, True)
    expect("raw_pins_73j", pins_j, True)
    for b in TARGETS["73i"]["batches"][1]:
        for field in ("loss", "nodes", "capped", "terminalStoneRange"):
            expect("control_b1_bit%d_%s" % (b, field),
                   ctrl[b].get(field), pub73i[b].get(field))
    expect("control_bits", len(pub73i), 73)
    expect("control_bits_73j", len(pub73j), 73)

    # 2) pilot capacity probe at MS=1<<24 (runner aborts its own control)
    v24 = make_variant(24)
    probe = subprocess.run(
        [NODE, "--experimental-strip-types", v24,
         "--bits", "0", "--depth", str(DEPTH), "--cap", str(CAP),
         "--andclose", str(ANDCLOSE), "--child", TARGETS["73i"]["child"]],
        capture_output=True, text=True)
    m = re.search(r"got loss=(\w+) nodes=(\d+)", probe.stderr)
    expect("pilot_probe_ms24_nodes", int(m.group(2)) if m else None,
           EXPECTED["pilot_ms24"])

    # 3) full sweeps at MS=1<<23 (both children) and MS=1<<24 (73i)
    v23 = make_variant(23)
    results = {}
    jobs = []
    for tag, cfg in TARGETS.items():
        for bno, bits in cfg["batches"].items():
            jobs.append((tag, bno, cfg["child"], bits, v23, "ms23_%s_b%d" % (tag, bno)))
    for bno, bits in TARGETS["73i"]["batches"].items():
        jobs.append(("73i", bno, TARGETS["73i"]["child"], bits, v24,
                     "ms24_73i_b%d" % bno))
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futs = {tagj: pool.submit(run_batch, runner, child, bits, tagj)
                for (tag, bno, child, bits, runner, tagj) in jobs}
        for tagj, fut in futs.items():
            results[tagj] = fut.result()

    def merged(prefix, tag):
        recs = {}
        for bno in TARGETS[tag]["batches"]:
            recs.update(results["%s_%s_b%d" % (prefix, tag, bno)])
        return recs

    comp = {}
    comp["73i_ms23"] = compare("73i", pub73i, merged("ms23", "73i"))
    comp["73i_ms24"] = compare("73i", pub73i, merged("ms24", "73i"))
    comp["73j_ms23"] = compare("73j", pub73j, merged("ms23", "73j"))

    expect("73i_ms23_total", comp["73i_ms23"]["total_measured"],
           EXPECTED["73i"]["ms23_total"])
    expect("73i_ms23_mismatches", len(comp["73i_ms23"]["mismatches"]), 0)
    expect("73i_ms23_win", comp["73i_ms23"]["win_bits"], TARGETS["73i"]["win7_d10_bits"])
    expect("73i_ms24_total", comp["73i_ms24"]["total_measured"],
           EXPECTED["73i"]["ms24_total"])
    expect("73i_ms24_mismatches", len(comp["73i_ms24"]["mismatches"]), 0)
    expect("73j_ms23_total", comp["73j_ms23"]["total_measured"],
           EXPECTED["73j"]["ms23_total"])
    expect("73j_ms23_mismatches", len(comp["73j_ms23"]["mismatches"]), 0)
    expect("73j_ms23_win", comp["73j_ms23"]["win_bits"], TARGETS["73j"]["win7_d10_bits"])

    # 4) sensitivity: fresh single bits at ms20/21/22 (23/24 come from the sweeps)
    sens = {}
    for bit in (78, 101):
        curve = {"18": EXPECTED["published_nodes"][bit]}
        for ms in (20, 21, 22):
            v = make_variant(ms)
            recs = run_batch(v, TARGETS["73i"]["child"], [bit],
                             "sens_73i_bit%d_ms%d" % (bit, ms))
            curve[str(ms)] = recs[bit]["nodes"]
            expect("sens_bit%d_ms%d" % (bit, ms), recs[bit]["nodes"],
                   EXPECTED["sensitivity"][bit][ms])
        r23 = merged("ms23", "73i")[bit]
        r24 = merged("ms24", "73i")[bit]
        curve["23"] = r23["nodes"]
        curve["24"] = r24["nodes"]
        expect("sens_bit%d_ms23" % bit, r23["nodes"], EXPECTED["sensitivity"][bit][23])
        expect("sens_bit%d_ms24" % bit, r24["nodes"], EXPECTED["sensitivity"][bit][24])
        sens[bit] = curve

    print("FAILURES: %d" % len(failures))
    for f in failures:
        print("  " + json.dumps(f))
    for k, v in comp.items():
        print("%s: %d -> %d (x%.4f), mismatches %d, win %s" %
              (k, v["total_published"], v["total_measured"], v["ratio"],
               len(v["mismatches"]), v["win_bits"] == TARGETS[k.split("_")[0]]["win7_d10_bits"]))
    print("sensitivity: " + json.dumps(sens))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
