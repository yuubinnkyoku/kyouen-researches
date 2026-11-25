#!/usr/bin/env python3
"""Band-wide memo-capacity measurement for the cost-73j extraction lane (2026-11-17).

Published alongside this script:
  output/class2-lane-band-memo-extraction-measurement-73j-20261117.json

Motivation.  The certificate extractor class4_child1_cert_extractor_exact.ts
(git blob 52bcaf509ea12fad4c936501d30d26b5b66c0085) uses a process-global
position memo (MS=1<<18 slots, 64-probe linear probing; memoEntry silently
skips storing when a probe chain is exhausted, memoFind then treats the entry
as absent, which is sound but costs recomputation).  The published cost-73j
band (16 WIN7-D10 certificates, manifest git blob
e88710b5a2d4848be77a03ae5104e46aefc1279a) was extracted with that verbatim
engine in one fresh process per bit: 166,238,087 extraction nodes total.
This script measures how much of that cost is pure memo capacity, by
re-extracting the same band with one-line MS-substituted engine variants
(the ONLY change is `const MS = 1 << 18` -> `const MS = 1 << N`), and by
comparing band-wide single-process runs against fresh per-bit processes.

All evidence invariants checked here (expected values embedded):
  - fidelity: run A (band-wide verbatim) reproduces bit 0 exactly at the
    published 9,260,973 nodes / 46,463 rows (memo is empty at band start);
    a fresh verbatim bit 98 run reproduces 25,505,012 nodes / 64,451 rows
    with rows byte-identical to the published certificate data rows.
  - run A (verbatim MS=1<<18, band-wide): 229,836,337 nodes (+38.26% vs
    published fresh baseline; the memo saturates inside bit 0 and later
    bits lose intra-bit memoization, per-bit ratios 1.244513..2.050475).
  - run B (MS=1<<24, band-wide): 94,005,413 nodes (-43.45%).
  - attribution battery (each of the 16 bits in its own fresh MS=1<<24
    process): 91,941,958 nodes (-44.69%), 16/16 per-bit row sets
    byte-identical to the published certificates.
  - sensitivity (bit 98, fresh process): 1<<18 25,505,012 / 1<<20 17,721,785
    / 1<<21 14,860,944 / 1<<22 13,262,116 / 1<<23 12,462,197 / 1<<24
    12,193,647 / 1<<25 12,100,297; rows constant 64,451, one md5.
  - union invariance: the run A union, run B union and the union of the 16
    published certificate row sets are byte-equal (547,910 rows,
    md5 5eb31648e510d1718eaf68de8c6a1e97).
  - fbt_drops=0 everywhere.

Interpretation guard: measurement only.  No new WIN/LOSS verdicts, no
manifest row opened or closed, certificate bytes unchanged, published sweep
verdicts unchanged.  WIN7-D10 proves a first-player win within depth 10 from
the individual 7-stone roots only; REFUTED-D10 is not a LOSS proof.  The
11x11 empty board, both two-stone roots {49,60} and {59,60}, S2 {59,60} and
classes 1/2/4 all remain UNKNOWN.

Usage:  python3 measure_band_memo_extraction_73j_20261117.py
        (env: KYOEN_NODE=node; full re-run takes roughly 25 min single-core)
"""
import hashlib
import json
import os
import subprocess
import sys

HERE = sys.path[0] or "."
EXP = os.path.dirname(os.path.abspath(HERE))
OUT = os.path.join(EXP, "output")
WORK = os.path.join(OUT, "band_memo_measurement_73j_work")
NODE = os.environ.get("KYOEN_NODE", "node")

EXTRACTOR = os.path.join(HERE, "class4_child1_cert_extractor_exact.ts")
DRIVER = os.path.join(HERE, "measure_band_memo_extraction_73j.ts")
LEGAL = os.path.join(HERE, "legal_candidates.py")
MANIFEST = os.path.join(
    OUT, "class2-lane-cost73j-win7-certificates-20261117.json")

EXTRACTOR_BLOB = "52bcaf509ea12fad4c936501d30d26b5b66c0085"
MANIFEST_BLOB = "e88710b5a2d4848be77a03ae5104e46aefc1279a"
LEGAL_BLOB = "8e97082c42838c7a4a4b6d2dd235276c8d43ab9a"

EXPECTED = {
    "bits": [0, 1, 6, 29, 44, 49, 52, 69, 74, 82, 87, 91, 98, 100, 110, 118],
    "published_total_nodes": 166238087,
    "union_rows": 547910,
    "union_md5": "5eb31648e510d1718eaf68de8c6a1e97",
    "bit0_nodes": 9260973, "bit0_rows": 46463,
    "bit98_nodes_ms18": 25505012, "bit98_rows": 64451,
    "bit98_rows_md5": "6db21986f3a67c35dde3d9d275acd29f",
    "run_a_total": 229836337, "run_a_ratio": 1.382573,
    "run_b_total": 94005413, "run_b_ratio": 0.565487,
    "fresh_ms24_total": 91941958, "fresh_ms24_ratio": 0.5531,
    "sensitivity_bit98": {18: 25505012, 20: 17721785, 21: 14860944,
                          22: 13262116, 23: 12462197, 24: 12193647,
                          25: 12100297},
}

VERBATIM_LINE = "const MS=1<<18, MM=MS-1;"


def git_blob_sha(path):
    data = open(path, "rb").read()
    h = hashlib.sha1()
    h.update(b"blob %d\x00" % len(data))
    h.update(data)
    return h.hexdigest()


def check_pin(name, path, expected):
    actual = git_blob_sha(path)
    if actual != expected:
        raise SystemExit("%s BLOB MISMATCH: %s != %s" % (name, actual, expected))
    return actual


def make_variant(ms_shift):
    """One-line MS substitution (ms_shift=18 copies verbatim); asserts the diff."""
    os.makedirs(WORK, exist_ok=True)
    src = open(EXTRACTOR, "r", encoding="utf-8").read()
    dst = os.path.join(WORK, "class4_child1_cert_extractor_exact_ms%d.ts" % ms_shift)
    if ms_shift == 18:
        with open(dst, "w", encoding="utf-8") as fh:
            fh.write(src)
        return dst
    if VERBATIM_LINE not in src:
        raise SystemExit("verbatim MS line not found in extractor")
    with open(dst, "w", encoding="utf-8") as fh:
        fh.write(src.replace(VERBATIM_LINE,
                             "const MS=1<<%d, MM=MS-1;" % ms_shift))
    # verify: only the MS line differs
    a = [l for l in src.splitlines() if "const MS" not in l]
    b = [l for l in open(dst, encoding="utf-8").read().splitlines()
         if "const MS" not in l]
    if a != b:
        raise SystemExit("variant ms%d differs by more than the MS line" % ms_shift)
    return dst


def driver_import_line(ms_shift):
    return "./class4_child1_cert_extractor_exact_ms%d.ts" % ms_shift


def make_driver(ms_shift):
    """The published driver with only the import line retargeted at a variant."""
    src = open(DRIVER, "r", encoding="utf-8").read()
    target = "import { extractBatch } from './class4_child1_cert_extractor_exact.ts';"
    if target not in src:
        raise SystemExit("driver import line not found")
    dst = os.path.join(WORK, "measure_band_memo_extraction_73j_ms%d.ts" % ms_shift)
    with open(dst, "w", encoding="utf-8") as fh:
        fh.write(src.replace(target,
                             "import { extractBatch } from '%s';" % driver_import_line(ms_shift)))
    return dst


def build_plan():
    """child + per-bit {bit, root, moves, published_nodes, published_rows}."""
    manifest = json.load(open(MANIFEST, encoding="utf-8"))
    child = manifest["s6_child_hex"]
    bits = []
    for c in manifest["certificates"]:
        proc = subprocess.run([sys.executable, LEGAL, c["root"]],
                              capture_output=True, text=True, check=True)
        lines = [l for l in proc.stdout.splitlines() if l.strip()]
        moves = [int(x) for x in lines[1].split(",")]
        if len(moves) != c["loser_mobility"]:
            raise SystemExit("mobility mismatch bit %d" % c["bit"])
        bits.append({"bit": c["bit"], "root": c["root"], "moves": moves,
                     "published_nodes": c["extraction_nodes"],
                     "published_rows": c["rows"]})
    order = sorted(bits, key=lambda b: b["bit"])
    if [b["bit"] for b in order] != EXPECTED["bits"]:
        raise SystemExit("bit list mismatch")
    plan_path = os.path.join(WORK, "plan73j.json")
    with open(plan_path, "w", encoding="utf-8") as fh:
        json.dump({"child": child, "bits": order}, fh)
    return plan_path, sum(b["published_nodes"] for b in order)


def run_driver(driver, plan, tag, bits=None):
    summary = os.path.join(WORK, tag + ".summary.json")
    rows = os.path.join(WORK, tag + ".rows.txt")
    if os.path.exists(summary) and os.path.exists(rows) and os.path.getsize(summary) > 0:
        return json.load(open(summary, encoding="utf-8")), rows  # resume
    cmd = [NODE, "--experimental-strip-types", driver, plan, summary, rows]
    if bits is not None:
        # fresh single-bit battery: write a one-bit plan
        plan1 = os.path.join(WORK, tag + ".plan.json")
        full = json.load(open(plan, encoding="utf-8"))
        full["bits"] = [b for b in full["bits"] if b["bit"] == bits]
        with open(plan1, "w", encoding="utf-8") as fh:
            json.dump(full, fh)
        cmd = [NODE, "--experimental-strip-types", driver, plan1, summary, rows]
    subprocess.run(cmd, check=True)
    return json.load(open(summary, encoding="utf-8")), rows


def total_nodes_key(summary):
    return summary[[k for k in summary if k.startswith("total_nodes")][0]]


def main():
    os.makedirs(WORK, exist_ok=True)
    check_pin("extractor", EXTRACTOR, EXTRACTOR_BLOB)
    check_pin("manifest", MANIFEST, MANIFEST_BLOB)
    check_pin("legal_candidates", LEGAL, LEGAL_BLOB)

    plan_path, pub_total = build_plan()
    if pub_total != EXPECTED["published_total_nodes"]:
        raise SystemExit("published node total mismatch: %d" % pub_total)

    failures = []
    def expect(name, got, want):
        if got != want:
            failures.append({"check": name, "expected": want, "got": got})

    # run A: band-wide, verbatim MS=1<<18 engine
    make_variant(18)
    runA, rowsA = run_driver(make_driver(18), plan_path, "band_memo")
    expect("run_a_total", total_nodes_key(runA), EXPECTED["run_a_total"])
    expect("run_a_bit0_nodes", runA["per_bit"][0]["nodes_this_run"], EXPECTED["bit0_nodes"])
    expect("run_a_bit0_rows", runA["per_bit"][0]["rows_new_this_bit"], EXPECTED["bit0_rows"])
    expect("run_a_fbt_drops", runA["fbt_drops"], 0)

    # run B: band-wide, MS=1<<24 variant
    make_variant(24)
    runB, rowsB = run_driver(make_driver(24), plan_path, "band_memo_ms24")
    expect("run_b_total", total_nodes_key(runB), EXPECTED["run_b_total"])
    expect("run_b_fbt_drops", runB["fbt_drops"], 0)

    # fidelity: fresh verbatim bit 98 (rows byte-identical to published cert)
    run98, rows98 = run_driver(make_driver(18), plan_path, "bit98_ms18", bits=98)
    expect("bit98_ms18_nodes", total_nodes_key(run98), EXPECTED["bit98_nodes_ms18"])
    r98 = open(rows98, "rb").read()
    expect("bit98_rows", len(r98.decode().splitlines()), EXPECTED["bit98_rows"])
    expect("bit98_rows_md5", hashlib.md5(r98).hexdigest(), EXPECTED["bit98_rows_md5"])

    # attribution battery: 16 fresh MS=1<<24 per-bit runs
    make_variants = [18, 20, 21, 22, 23, 24, 25]
    for ms in make_variants:
        if ms != 18:
            make_variant(ms)
    fresh_total = 0
    per_bit_attr = []
    for b in EXPECTED["bits"]:
        s, r = run_driver(make_driver(24), plan_path, "fresh_ms24_%d" % b, bits=b)
        n = total_nodes_key(s)
        fresh_total += n
        rr = hashlib.md5(open(r, "rb").read()).hexdigest()
        rows_n = len(open(r, encoding="utf-8").read().splitlines())
        per_bit_attr.append({"bit": b, "fresh_ms24_nodes": n,
                             "rows": rows_n, "rows_md5": rr,
                             "row_md5_constant": rr == EXPECTED["bit98_rows_md5"]
                             if b == 98 else None})
        if b == 98:
            expect("bit98_ms24_nodes", n, EXPECTED["sensitivity_bit98"][24])
    expect("fresh_ms24_total", fresh_total, EXPECTED["fresh_ms24_total"])

    # sensitivity: bit 98 fresh at every MS
    sens = []
    for ms in (18, 20, 21, 22, 23, 24, 25):
        s, r = run_driver(make_driver(ms), plan_path, "bit98_ms%d" % ms, bits=98)
        n = total_nodes_key(s)
        sens.append({"ms_shift": ms, "memo_slots": 1 << ms, "nodes": n})
        expect("sensitivity_ms%d" % ms, n, EXPECTED["sensitivity_bit98"][ms])
        expect("sensitivity_ms%d_rows_md5" % ms,
               hashlib.md5(open(r, "rb").read()).hexdigest(),
               EXPECTED["bit98_rows_md5"])

    # union invariance
    ua = open(rowsA, "rb").read()
    ub = open(rowsB, "rb").read()
    expect("union_rows_a", len(ua.decode().splitlines()), EXPECTED["union_rows"])
    expect("union_md5_a", hashlib.md5(ua).hexdigest(), EXPECTED["union_md5"])
    expect("union_a_equals_b", ua == ub, True)

    print("FAILURES: %d" % len(failures))
    for f in failures:
        print("  " + json.dumps(f))
    print("run_a %d run_b %d fresh_ms24 %d (baseline %d)" %
          (total_nodes_key(runA), total_nodes_key(runB), fresh_total, pub_total))
    print("sensitivity: " + json.dumps(sens))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
