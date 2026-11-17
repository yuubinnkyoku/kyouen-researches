#!/usr/bin/env python3
"""Independent verification of the two memo performance bugs in the
repo-verbatim certificate extractor class4_child1_cert_extractor_exact.ts
(git blob 52bcaf50...), item K0906 (2026-11-17, n11 class2-lane).

SOUNDNESS: both bugs are performance-only.  No published certificate,
node count or verdict is invalidated.  This script verifies the bugs'
existence, mechanism and measured magnitude; it publishes nothing.

BUG A (memo key sign bug).  mK0/mK1/mK2 are Uint32Array; the comparison
operands M0/M1/M2 are int32 JS numbers.  A position occupying cell
31 / 63 / 95 has bit 31 set in word 0/1/2, so M0/M1/M2 is negative;
the stored unsigned value never compares equal, memoFind never matches,
and memoEntry re-inserts the same key at the next free probe slot on
every visit (up to 64 copies per key, the key's whole 64-slot probe
window).  Evidence: bit-0 first-12-move debug dump (verbatim engine,
MS=1<<23): 834,262 nodes, 216,719 stored records, 112,731 distinct keys,
16,417 keys with 2..64 copies; ALL duplicated keys have bit 31 of
k0/k1/k2 set, NO non-high-bit key is stored twice; 7 keys own their
complete 64-slot window (64 copies); 125,293 records (57.8%) are
high-bit; every copy of every key lies within its 64-slot probe window
(window fit, NOT a contiguous run - the first verifier draft
overclaimed contiguous-run geometry and its own FAIL gate caught it).
This duplicate insertion is the concrete mechanism behind the
published 73k band ms18 bit-0 "clumped-hash insertion failures" stall.

BUG B (dead negative bounds).  `if(h>=0&&d>mNoWin[h]) mNoWin[h]=d;` and
the mNoLose twin never fire: with the 255 "unbound" sentinel stored and
depth arguments <= 64 < 255, the comparison direction is wrong.  All
216,719 records keep nowin=nolose=255 and both memoFind negative-bound
shortcuts are dead.

Checks (all must pass):
  pins (extractor/legal/manifest) 3x
  source pattern counts (key arrays line, nowin/nolose update lines,
    comparison line x2)
  node -e sign demo (Uint32Array store/compare mismatch, Int32Array OK)
  dump regeneration: nodes == 834262, KYOENSLT magic, records 216719,
    distinct 112731, dup keys 16417 (all high-bit, zero non-high-bit),
    max copies 64, 64-copy keys 7, window fit for every dup key,
    64-copy keys span exactly 63, high-bit records 125293,
    nowin=nolose=255 on every record
  determinism: dump bytes identical on a second run
  fixed battery JSON (output/fixed_memo_battery_73k_20261117.json):
    status complete, fixA total 75,108,849, fixB total 28,290,025,
    22/22 byte-identical per variant, fixB bit0 1,277,392

Interpretation guard: measurement/verification only.  WIN7-D10 proves a
first-player win within depth 10 from the individual 7-stone roots only;
REFUTED-D10 is not a LOSS proof.  The 11x11 empty board, both two-stone
roots {49,60} and {59,60}, S2 {59,60} and classes 1/2/4 all remain
UNKNOWN.

Usage: python3 verify_extractor_memo_sign_bug_73k_20261117.py [out.json]
"""
import hashlib
import json
import os
import struct
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__)) or "."
OUT = os.path.join(HERE, "output")
WORK = os.path.join(OUT, "memo_sign_bug_verify_work")
NODE = os.environ.get("KYOEN_NODE", "node")

EXTRACTOR = os.path.join(HERE, "class4_child1_cert_extractor_exact.ts")
LEGAL = os.path.join(HERE, "legal_candidates.py")
CERTDIR = os.path.join(OUT, "class2-lane-cost73k-certificates")
MANIFEST = os.path.join(
    CERTDIR, "class2-lane-cost73k-win7-certificates-20261117.json")
if not os.path.exists(MANIFEST):
    MANIFEST = os.path.join(HERE, "manifest.json")
BATTERY_JSON = os.path.join(
    OUT, "fixed_memo_battery_73k_20261117.json")

EXTRACTOR_BLOB = "52bcaf509ea12fad4c936501d30d26b5b66c0085"
LEGAL_BLOB = "8e97082c42838c7a4a4b6d2dd235276c8d43ab9a"
MANIFEST_BLOB = "0892aed07d187ae2fb3b4b90a21c7adbc1002b62"

VERBATIM_LINE = "const MS=1<<18, MM=MS-1;"
KEYS_LINE = ("const mK0=new Uint32Array(MS),mK1=new Uint32Array(MS),"
             "mK2=new Uint32Array(MS),mK3=new Uint32Array(MS);")
NOWIN_LINE = "if(h>=0&&d>mNoWin[h]) mNoWin[h]=d;"
NOLOSE_LINE = "if(h>=0&&e>mNoLose[h]) mNoLose[h]=e;"
CMP_LINE = ("if(mK0[h]===M0&&mK1[h]===M1&&mK2[h]===M2&&mK3[h]===M3)"
            "return h;")
ANCHOR = ("export function extractBatch(childHex: string, bit: number, "
          "killTable: Record<number, number>, moves: number[]) {")

DUMP_BLOCK = """// VERIFICATION MODIFICATION (2026-11-17, dump-only; NO search-behavior
// change, NO bug fix): export the whole memo table (occupied slots, with
// slot index) in the KYOENSLT debug format:
//   16-byte header: 'KYOENSLT' ascii + MS uint32LE + count uint32LE
//   24-byte record: k0..k3 uint32LE + win,lose,nowin,nolose uint8 +
//                   slot uint32LE
export function dumpMemo(path: string): { slots: number, occupied: number } {
  let c = 0; for (let i = 0; i < MS; i++) if (mOcc[i]) c++;
  const b = Buffer.alloc(16 + 24 * c);
  b.write('KYOENSLT', 0, 'ascii');
  b.writeUInt32LE(MS, 8); b.writeUInt32LE(c, 12);
  let o = 16;
  for (let i = 0; i < MS; i++) if (mOcc[i]) {
    b.writeUInt32LE(mK0[i] >>> 0, o); b.writeUInt32LE(mK1[i] >>> 0, o + 4);
    b.writeUInt32LE(mK2[i] >>> 0, o + 8); b.writeUInt32LE(mK3[i] >>> 0, o + 12);
    b.writeUInt8(mWin[i], o + 16); b.writeUInt8(mLose[i], o + 17);
    b.writeUInt8(mNoWin[i], o + 18); b.writeUInt8(mNoLose[i], o + 19);
    b.writeUInt32LE(i, o + 20); o += 24;
  }
  fs.writeFileSync(path, b);
  return { slots: MS, occupied: c };
}
"""

DRIVER_SRC = """import { extractBatch, dumpMemo } from './class4_child1_cert_extractor_exact_dump_ms23.ts';
import fs from 'fs';
const plan = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const b = plan.bits[0];
const res: any = extractBatch(plan.child, b.bit, {}, b.moves);
if (res.fatal !== undefined && res.fatal !== null) { process.stderr.write('INVALID fatal=' + res.fatal); process.exit(1); }
if (res.fbt_drops !== 0) { process.stderr.write('INVALID fbt_drops=' + res.fbt_drops); process.exit(1); }
const st = dumpMemo(process.argv[3]);
fs.writeFileSync(process.argv[4], JSON.stringify({ nodes: res.sum, rows: res.rows.length, occupied: st.occupied, slots: st.slots }));
process.stderr.write('nodes ' + res.sum + ' rows ' + res.rows.length + ' occupied ' + st.occupied + String.fromCharCode(10));
"""

# Expected (measured 2026-11-17, deterministic engine; regression gates):
EXP_NODES_12MOVES = 834262
EXP_RECORDS = 216719
EXP_DISTINCT = 112731
EXP_DUP_KEYS = 16417
EXP_MAX_COPIES = 64
EXP_KEYS_64 = 7
EXP_HIGHBIT_RECORDS = 125293
EXP_FIXA_TOTAL = 75108849
EXP_FIXB_TOTAL = 28290025
EXP_FIXB_BIT0 = 1277392

checks = []


def check(name, ok, detail):
    checks.append({"check": name, "ok": bool(ok), "detail": detail})
    if not ok:
        print("FAIL:", name, "-", detail)
    return ok


def git_blob_sha(path):
    data = open(path, "rb").read()
    h = hashlib.sha1()
    h.update(b"blob %d\x00" % len(data))
    h.update(data)
    return h.hexdigest()


def make_dump_variant():
    os.makedirs(WORK, exist_ok=True)
    src = open(EXTRACTOR, "r", encoding="utf-8").read()
    if src.count(VERBATIM_LINE) != 1 or src.count(ANCHOR) != 1:
        raise SystemExit("verbatim patch anchors not found exactly once")
    out = src.replace(VERBATIM_LINE, "const MS=1<<23, MM=MS-1;")
    out = out.replace(ANCHOR, DUMP_BLOCK + ANCHOR)
    dst = os.path.join(WORK, "class4_child1_cert_extractor_exact_dump_ms23.ts")
    with open(dst, "w", encoding="utf-8") as fh:
        fh.write(out)
    return dst


def run_dump(tag):
    variant = make_dump_variant()
    driver = os.path.join(WORK, "dump_driver_%s.ts" % tag)
    with open(driver, "w", encoding="utf-8") as fh:
        fh.write(DRIVER_SRC)
    manifest = json.load(open(MANIFEST, encoding="utf-8"))
    c0 = [x for x in manifest["certificates"] if x["bit"] == 0][0]
    proc = subprocess.run([sys.executable, LEGAL, c0["root"]],
                          capture_output=True, text=True, check=True)
    lines = [l for l in proc.stdout.splitlines() if l.strip()]
    moves = [int(x) for x in lines[1].split(",")]
    if len(moves) != c0["loser_mobility"]:
        raise SystemExit("mobility mismatch")
    plan = {"child": manifest["s6_child_hex"],
            "bits": [{"bit": 0, "root": c0["root"], "moves": moves[:12]}]}
    plan_path = os.path.join(WORK, "dump_plan_%s.json" % tag)
    with open(plan_path, "w", encoding="utf-8") as fh:
        json.dump(plan, fh)
    dump_path = os.path.join(WORK, "memo_dump_%s.bin" % tag)
    meta_path = os.path.join(WORK, "dump_meta_%s.json" % tag)
    subprocess.run([NODE, "--experimental-strip-types",
                    "--max-old-space-size=350", driver, plan_path,
                    dump_path, meta_path], check=True)
    return json.load(open(meta_path, encoding="utf-8")), dump_path


def parse_dump(path):
    data = open(path, "rb").read()
    if data[:8] != b"KYOENSLT":
        raise SystemExit("bad magic")
    ms, count = struct.unpack_from("<II", data, 8)
    recs = []
    for i in range(count):
        k0, k1, k2, k3 = struct.unpack_from("<IIII", data, 16 + 24 * i)
        win, lose, nowin, nolose = struct.unpack_from(
            "<BBBB", data, 16 + 24 * i + 16)
        slot, = struct.unpack_from("<I", data, 16 + 24 * i + 20)
        recs.append((k0, k1, k2, k3, win, lose, nowin, nolose, slot))
    return ms, count, recs


def window_fit(slots, ms):
    """True iff all copies fit within some 64-slot cyclic window
    (memoEntry probes at most 64 slots from the hash slot)."""
    s = sorted(slots)
    gaps = [s[i + 1] - s[i] for i in range(len(s) - 1)]
    gaps.append(s[0] + ms - s[-1])   # wrap-around gap
    span = s[-1] - s[0] if len(s) > 1 else 0
    # removing the largest cyclic gap leaves the window span
    return span - max(gaps) <= 63


def analyze(ms, recs):
    from collections import Counter
    keys = Counter()
    slots_by_key = {}
    nowin_all_255 = True
    nolose_all_255 = True
    highbit_records = 0
    for (k0, k1, k2, k3, win, lose, nowin, nolose, slot) in recs:
        key = (k0, k1, k2, k3)
        keys[key] += 1
        slots_by_key.setdefault(key, []).append(slot)
        if nowin != 255:
            nowin_all_255 = False
        if nolose != 255:
            nolose_all_255 = False
        if (k0 | k1 | k2) & 0x80000000:
            highbit_records += 1
    distinct = len(keys)
    dups = {k: c for k, c in keys.items() if c > 1}
    dup_high = sum(1 for k in dups if (k[0] | k[1] | k[2]) & 0x80000000)
    dup_nonhigh = len(dups) - dup_high
    max_copies = max(keys.values())
    keys_64 = sum(1 for c in dups.values() if c == 64)
    fit_all = all(window_fit(v, ms) for v in slots_by_key.values()
                  if len(v) > 1)
    span63_64copy = all((max(v) - min(v)) == 63
                        for v in slots_by_key.values() if len(v) == 64)
    return {
        "records": len(recs), "distinct": distinct, "dup_keys": len(dups),
        "dup_keys_highbit": dup_high, "dup_keys_nonhighbit": dup_nonhigh,
        "max_copies": max_copies, "keys_with_64_copies": keys_64,
        "all_dup_keys_window_fit": fit_all,
        "keys_64_span_exactly_63": span63_64copy,
        "highbit_records": highbit_records,
        "highbit_record_ratio": round(highbit_records / len(recs), 4),
        "nowin_all_255": nowin_all_255, "nolose_all_255": nolose_all_255,
    }


def main():
    out_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        OUT, "extractor-memo-sign-bug-verify-73k-20261117.json")
    os.makedirs(WORK, exist_ok=True)

    # --- pins ---
    check("pin_extractor", git_blob_sha(EXTRACTOR) == EXTRACTOR_BLOB,
          git_blob_sha(EXTRACTOR))
    check("pin_legal_candidates", git_blob_sha(LEGAL) == LEGAL_BLOB,
          git_blob_sha(LEGAL))
    check("pin_manifest", git_blob_sha(MANIFEST) == MANIFEST_BLOB,
          git_blob_sha(MANIFEST))

    # --- source pattern counts ---
    src = open(EXTRACTOR, "r", encoding="utf-8").read()
    check("src_uint32_memo_keys", src.count(KEYS_LINE) == 1,
          "mK0..mK3 declared as Uint32Array exactly once")
    check("src_dead_nowin_update", src.count(NOWIN_LINE) == 1,
          "verbatim `d>mNoWin[h]` (sentinel-dead) update exactly once")
    check("src_dead_nolose_update", src.count(NOLOSE_LINE) == 1,
          "verbatim `e>mNoLose[h]` (sentinel-dead) update exactly once")
    check("src_cmp_line_twice", src.count(CMP_LINE) == 2,
          "unsigned-stored vs int32-comparand key compare in memoFind and "
          "memoEntry")
    # bit31 cells: word w = c>>>5, bit = 1<<(c&31); cells 31/63/95 set
    # bit 31 of words 0/1/2 -> negative int32 comparand.
    check("src_cells_31_63_95_map_to_bit31",
          all(((c >> 5) in (0, 1, 2)) and ((c & 31) == 31)
              for c in (31, 63, 95)),
          "cells 31/63/95 occupy bit31 of words 0/1/2")

    # --- node -e sign demo ---
    demo = subprocess.run(
        [NODE, "-e",
         "const u=new Uint32Array(1),i=new Int32Array(1);"
         "const M=(0x80000000|0);u[0]=M;i[0]=M;"
         "console.log(u[0]===M, i[0]===M, u[0], i[0]);"],
        capture_output=True, text=True, check=True)
    parts = demo.stdout.split()
    check("node_uint32_store_compare_mismatch", parts[0] == "false",
          "Uint32Array store of int32 -2^31 reads back 2^31 unsigned; "
          "=== against the int32 value is false: " + demo.stdout.strip())
    check("node_int32_store_compare_exact", parts[1] == "true",
          "Int32Array store/compare is exact: " + demo.stdout.strip())

    # --- dump regeneration (verbatim engine, bit0 first 12 moves) ---
    meta1, dump1 = run_dump("run1")
    check("dump_nodes_834262", meta1["nodes"] == EXP_NODES_12MOVES,
          "12-move bit0 extraction nodes=%s" % meta1["nodes"])
    ms, count, recs = parse_dump(dump1)
    check("dump_magic_ms", ms == (1 << 23) and count == len(recs),
          "KYOENSLT header ms=%d count=%d records=%d" % (ms, count, len(recs)))
    a = analyze(ms, recs)
    check("dump_records_216719", a["records"] == EXP_RECORDS, str(a["records"]))
    check("dump_distinct_112731", a["distinct"] == EXP_DISTINCT,
          str(a["distinct"]))
    check("dump_dup_keys_16417", a["dup_keys"] == EXP_DUP_KEYS,
          str(a["dup_keys"]))
    check("dump_all_dup_keys_highbit", a["dup_keys_highbit"] == a["dup_keys"]
          and a["dup_keys_nonhighbit"] == 0,
          "duplicated keys high-bit=%d non-high-bit=%d (bug A signature: "
          "only bit31 keys can be re-inserted)"
          % (a["dup_keys_highbit"], a["dup_keys_nonhighbit"]))
    check("dump_max_copies_64", a["max_copies"] == EXP_MAX_COPIES,
          str(a["max_copies"]))
    check("dump_keys_64_copies_7", a["keys_with_64_copies"] == EXP_KEYS_64,
          str(a["keys_with_64_copies"]))
    check("dump_all_dups_within_64_window",
          a["all_dup_keys_window_fit"],
          "every key's copies fit its 64-slot probe window (window fit, "
          "not contiguity)")
    check("dump_64copy_keys_private_window",
          a["keys_64_span_exactly_63"],
          "64-copy keys own their complete 64-slot window (span 63)")
    check("dump_highbit_records_125293",
          a["highbit_records"] == EXP_HIGHBIT_RECORDS,
          "%d (%.1f%%)" % (a["highbit_records"],
                           100 * a["highbit_record_ratio"]))
    check("dump_nowin_nolose_all_255",
          a["nowin_all_255"] and a["nolose_all_255"],
          "no-win/no-lose bounds never recorded (bug B: sentinel compare "
          "direction dead)")

    # --- determinism: second run, byte-identical dump ---
    meta2, dump2 = run_dump("run2")
    same_bytes = (open(dump1, "rb").read() == open(dump2, "rb").read())
    check("dump_deterministic_bytes",
          meta2["nodes"] == meta1["nodes"] and same_bytes,
          "run2 nodes=%s bytes_identical=%s" % (meta2["nodes"], same_bytes))

    # --- fixed battery JSON gates ---
    if os.path.exists(BATTERY_JSON):
        bat = json.load(open(BATTERY_JSON, encoding="utf-8"))
        okb = (bat.get("status") == "complete"
               and bat["fixA_ms23"]["total_nodes"] == EXP_FIXA_TOTAL
               and bat["fixB_ms23"]["total_nodes"] == EXP_FIXB_TOTAL
               and bat["fixA_ms23"]["byte_identical"] == [22, 22]
               and bat["fixB_ms23"]["byte_identical"] == [22, 22]
               and bat["determinism_gate"]["fixB_bit0_nodes_run1"]
               == EXP_FIXB_BIT0)
        detail = ("status=%s fixA=%s fixB=%s byteA=%s byteB=%s det=%s"
                  % (bat.get("status"),
                     bat.get("fixA_ms23", {}).get("total_nodes"),
                     bat.get("fixB_ms23", {}).get("total_nodes"),
                     bat.get("fixA_ms23", {}).get("byte_identical"),
                     bat.get("fixB_ms23", {}).get("byte_identical"),
                     bat.get("determinism_gate",
                             {}).get("fixB_bit0_nodes_run1")))
    else:
        okb, detail = False, "battery JSON missing: %s" % BATTERY_JSON
    check("fixed_battery_json_gates", okb, detail)

    result = {
        "schema": "n11-class2-lane-extractor-memo-sign-bug-verify-73k"
                  "-20261117-v1",
        "date": "2026-11-17",
        "status": "pass" if all(c["ok"] for c in checks) else "FAIL",
        "extractor_blob": EXTRACTOR_BLOB,
        "bug_a": {
            "kind": "memo key sign bug (Uint32Array store vs int32 compare)",
            "soundness_impact": "none (memo is optimization-only)",
            "mechanism": ("positions on cells 31/63/95 make M0/M1/M2 "
                          "negative; memoFind never matches; memoEntry "
                          "re-inserts on every visit, up to 64 copies = "
                          "the key's whole 64-slot probe window"),
            "evidence_dump": a,
            "extraction_nodes_12moves": meta1["nodes"],
        },
        "bug_b": {
            "kind": "dead negative bounds (sentinel 255 compare direction)",
            "soundness_impact": "none",
            "evidence": "nowin=nolose=255 on all %d records" % a["records"],
        },
        "interpretation_guard": (
            "Verification only; no verdict change.  WIN7-D10 proves a win "
            "within depth 10 from individual 7-stone roots; REFUTED-D10 "
            "is not a LOSS proof.  11x11 empty board, two-stone roots "
            "{49,60}/{59,60}, S2 {59,60} and classes 1/2/4 remain UNKNOWN."),
        "checks": checks,
        "n_checks": len(checks),
        "n_pass": sum(1 for c in checks if c["ok"]),
    }
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=1, sort_keys=True)
    print("%d/%d checks pass -> %s" % (result["n_pass"],
                                       result["n_checks"], result["status"]))
    if result["status"] != "pass":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
