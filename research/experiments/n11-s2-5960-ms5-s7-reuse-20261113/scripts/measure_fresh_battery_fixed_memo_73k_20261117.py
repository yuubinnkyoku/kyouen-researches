#!/usr/bin/env python3
"""Fresh per-bit battery with FIXED memo variants for the cost-73k lane
(2026-11-17, n11 class2-lane long-term lane).

MEASUREMENT ONLY (no certificate publication, no verdict changes).

Background (discovered 2026-11-17 in this lane, evidence:
verify_extractor_memo_sign_bug_73k_20261117.py, item K0906): the
repo-verbatim certificate extractor
class4_child1_cert_extractor_exact.ts (git blob 52bcaf50...) has two memo
bugs, both performance-only (soundness unaffected; every published
certificate, node count and verdict remains valid):

  BUG A (memo key sign bug).  The memo key arrays mK0/mK1/mK2 are
  Uint32Array, but the comparison operands M0/M1/M2 are int32 JS numbers.
  Whenever a position occupies cell 31 / 63 / 95 the corresponding word has
  bit 31 set, M0/M1/M2 goes negative, and `mK0[h]===M0` is permanently
  false (unsigned stored value vs negative comparand).  memoFind never
  matches such positions; memoEntry re-inserts the same key at the next
  free probe slot on EVERY visit (up to 64 copies per key, each within the
  key's own 64-slot probe window; the 64-copy keys own their complete
  window).  Observed in a 12-move bit-0 debug dump (MS=1<<23): 216,719
  stored records, 112,731 distinct keys, 16,417 keys with 2..64 copies;
  ALL duplicated keys have bit 31 of k0/k1/k2 set and NO non-high-bit key
  is stored twice.  This duplicate insertion is the concrete mechanism
  behind the published 73k band ms18 bit-0 "clumped-hash insertion
  failures" stall at 76.6% occupancy.

  BUG B (dead negative bounds).  The no-win / no-lose memo bounds are
  never recorded: the updates `if(h>=0&&d>mNoWin[h]) mNoWin[h]=d;`
  (and the mNoLose twin) compare against the 255 "unbound" sentinel in
  the wrong direction, so with d,e <= 64 < 255 they never fire, all
  entries keep nowin=nolose=255 (verified on every one of the 216,719
  debug records), and both memoFind negative-bound shortcuts are dead.

Fix variants measured here (fresh process per bit, MS=1<<23, 22 bits of
the published cost-73k band; byte-identity of every per-root snapshot
against the published certificates is a hard gate):

  fixA: BUG A only - mK0..mK3 become Int32Array (same 32-bit pattern, so
        comparisons between stored int32 and int32 M0/M1/M2/M3 are exact).
  fixB: BUG A + BUG B - sentinel-aware negative-bound updates
        (mNoWin/mNoLose 255 means "no bound", so the first proof always
        records; later proofs raise the bound).

Expected reference (verbatim engine, published band measurement,
fresh per-bit ms23 battery): 108,499,241 nodes total, per-bit values
embedded below as VERBATIM_FRESH23 for delta reporting.

Measured on 2026-11-17 (embedded as regression gates EXPECTED_FIXED):
  - fixA (sign bug only): 75,108,849 nodes = 69.23% of the verbatim
    fresh ms23 battery (-30.8%); 22/22 certificates byte-identical.
  - fixB (both bugs): 28,290,025 nodes = 26.07% of verbatim fresh ms23
    (-73.9%, 3.8x) and 18.14% of the published ms18 baseline (-81.9%,
    5.5x); 22/22 byte-identical; battery wall time 196.4s + 130.6s.
  - per-bit occupied-slot counts are IDENTICAL between fixA and fixB
    (the entry set is fixed by removing duplicate insertion; the
    negative-bound fix only adds usable values to entries created either
    way, collapsing re-exploration without changing the entry set).
  - determinism: fixB bit 0 run twice -> 1,277,392 nodes both times.

Interpretation guard: measurement only.  No new WIN/LOSS verdicts, no
manifest row opened or closed, certificate bytes unchanged.  The fixed
variants are NOT a replacement for the repo-verbatim extractor for
published determinism chains; adoption of the fix is a separate lane
decision.  WIN7-D10 proves a first-player win within depth 10 from the
individual 7-stone roots only; REFUTED-D10 is not a LOSS proof.  The
11x11 empty board, both two-stone roots {49,60} and {59,60}, S2 {59,60}
and classes 1/2/4 all remain UNKNOWN.

Usage:  python3 measure_fresh_battery_fixed_memo_73k_20261117.py <out.json>
        (env: KYOEN_NODE=node; every step resumes from
        output/fixed_memo_battery_73k_work/)
"""
import hashlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__)) or "."
OUT = os.path.join(HERE, "output")
CERTDIR = os.path.join(OUT, "class2-lane-cost73k-certificates")
WORK = os.path.join(OUT, "fixed_memo_battery_73k_work")
NODE = os.environ.get("KYOEN_NODE", "node")

EXTRACTOR = os.path.join(HERE, "class4_child1_cert_extractor_exact.ts")
DRIVER = os.path.join(HERE, "measure_band_memo_extraction_73k.ts")
LEGAL = os.path.join(HERE, "legal_candidates.py")
MANIFEST = os.path.join(
    CERTDIR, "class2-lane-cost73k-win7-certificates-20261117.json")
if not os.path.exists(MANIFEST):
    MANIFEST = os.path.join(HERE, "manifest.json")

EXTRACTOR_BLOB = "52bcaf509ea12fad4c936501d30d26b5b66c0085"
MANIFEST_BLOB = "0892aed07d187ae2fb3b4b90a21c7adbc1002b62"
LEGAL_BLOB = "8e97082c42838c7a4a4b6d2dd235276c8d43ab9a"

VERBATIM_LINE = "const MS=1<<18, MM=MS-1;"
KEYS_LINE = ("const mK0=new Uint32Array(MS),mK1=new Uint32Array(MS),"
             "mK2=new Uint32Array(MS),mK3=new Uint32Array(MS);")
KEYS_LINE_FIXED = ("const mK0=new Int32Array(MS),mK1=new Int32Array(MS),"
                   "mK2=new Int32Array(MS),mK3=new Int32Array(MS);")
NOWIN_LINE = "if(h>=0&&d>mNoWin[h]) mNoWin[h]=d;"
NOWIN_LINE_FIXED = "if(h>=0&&(mNoWin[h]===255||d>mNoWin[h])) mNoWin[h]=d;"
NOLOSE_LINE = "if(h>=0&&e>mNoLose[h]) mNoLose[h]=e;"
NOLOSE_LINE_FIXED = "if(h>=0&&(mNoLose[h]===255||e>mNoLose[h])) mNoLose[h]=e;"

PATCH_ANCHOR = ("export function extractBatch(childHex: string, bit: number, "
                 "killTable: Record<number, number>, moves: number[]) {")
PATCH_BLOCK = """// EXPERIMENT MODIFICATION (2026-11-17, fixed-memo battery measurement only;
// not a replacement for the published extractor): expose a row-set reset and
// an occupancy probe so several roots can be extracted in ONE process while
// the module-level search memo and forbidden-bit cache persist across roots.
export function clearRows(): void { rows.clear(); }
export function memoStats(): { slots: number, occupied: number } {
  let c = 0; for (let i = 0; i < MS; i++) if (mOcc[i]) c++;
  return { slots: MS, occupied: c };
}
"""

DRIVER_IMPORT_TARGET = (
    "import { extractBatch, clearRows, memoStats } from "
    "'./class4_child1_cert_extractor_exact_memo18.ts';")

VERBATIM_FRESH23 = {
    0: 4303203, 7: 4970943, 11: 2910026, 15: 8108353, 35: 4871692,
    39: 2037105, 41: 1868639, 44: 4617329, 58: 4567866, 62: 1771346,
    73: 7370204, 76: 4098489, 87: 6581793, 89: 3869180, 94: 4204274,
    95: 11857737, 97: 3815019, 98: 5336993, 103: 5828967, 105: 3641568,
    112: 4767520, 117: 7100995}
VERBATIM_FRESH23_TOTAL = 108499241
PUBLISHED_TOTAL = 155946109   # verbatim ms18 fresh-process, published

# Regression gates: constants measured on 2026-11-17 (the earlier run of
# this battery was lost with an environment reset, but its totals were
# recorded; the engine is deterministic, so a fresh re-run must reproduce
# them exactly).  Per-bit values are NOT embedded (they were lost); they are
# recorded fresh by this run and consistency is enforced through the
# embedded totals and cross-variant gates below.
EXPECTED_FIXED = {
    "fixA_total_nodes": 75108849,          # 69.23% of verbatim fresh ms23
    "fixB_total_nodes": 28290025,          # 26.07% of verbatim fresh ms23
    "fixB_bit0_nodes": 1277392,           # determinism run, twice identical
    "fixB_bit95_nodes": 1415400,           # 0.119 of verbatim bit95
    "fixA_bit0_occupied": 372070,          # fixA==fixB occupancy (see gates)
    "byte_identical_per_variant": 22,
}


def git_blob_sha(path):
    data = open(path, "rb").read()
    h = hashlib.sha1()
    h.update(b"blob %d\x00" % len(data))
    h.update(data)
    return h.hexdigest()


def check_pin(name, path, expected):
    actual = git_blob_sha(path)
    if actual != expected:
        raise SystemExit("%s BLOB MISMATCH: %s != %s" % (name, actual,
                                                         expected))


def make_fixed_variant(fix_level, ms_shift):
    """Verbatim engine + MS substitution + measurement export block
    + (fixA: Int32Array memo keys) + (fixB: sentinel-aware negative bounds).
    Exactly one line-level change per bug, asserted by exact counts."""
    os.makedirs(WORK, exist_ok=True)
    src = open(EXTRACTOR, "r", encoding="utf-8").read()
    for pat, what in [(VERBATIM_LINE, "MS line"),
                      (PATCH_ANCHOR, "patch anchor"),
                      (KEYS_LINE, "memo key arrays line")]:
        if src.count(pat) != 1:
            raise SystemExit("verbatim %s not found exactly once" % what)
    if fix_level in ("B",):
        for pat, what in [(NOWIN_LINE, "no-win update"),
                          (NOLOSE_LINE, "no-lose update")]:
            if src.count(pat) != 1:
                raise SystemExit("verbatim %s not found exactly once" % what)
    out = src.replace(VERBATIM_LINE,
                      "const MS=1<<%d, MM=MS-1;" % ms_shift)
    out = out.replace(KEYS_LINE, KEYS_LINE_FIXED)
    if fix_level == "B":
        out = out.replace(NOWIN_LINE, NOWIN_LINE_FIXED)
        out = out.replace(NOLOSE_LINE, NOLOSE_LINE_FIXED)
    out = out.replace(PATCH_ANCHOR, PATCH_BLOCK + PATCH_ANCHOR)
    dst = os.path.join(
        WORK, "class4_child1_cert_extractor_exact_fix%s_ms%d.ts"
        % (fix_level, ms_shift))
    with open(dst, "w", encoding="utf-8") as fh:
        fh.write(out)
    return dst


def make_driver(fix_level, ms_shift):
    src = open(DRIVER, "r", encoding="utf-8").read()
    if DRIVER_IMPORT_TARGET not in src:
        raise SystemExit("driver import line not found")
    dst = os.path.join(
        WORK, "measure_band_memo_extraction_73k_fix%s_ms%d.ts"
        % (fix_level, ms_shift))
    with open(dst, "w", encoding="utf-8") as fh:
        fh.write(src.replace(
            DRIVER_IMPORT_TARGET,
            "import { extractBatch, clearRows, memoStats } from "
            "'./class4_child1_cert_extractor_exact_fix%s_ms%d.ts';"
            % (fix_level, ms_shift)))
    return dst


def build_plan():
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
        bits.append({"bit": c["bit"], "root": c["root"], "file": c["file"],
                     "moves": moves,
                     "published_nodes": c["extraction_nodes"],
                     "published_rows": c["rows"]})
    order = sorted(bits, key=lambda b: b["bit"])
    plan_path = os.path.join(WORK, "plan73k.json")
    with open(plan_path, "w", encoding="utf-8") as fh:
        json.dump({"child": child, "bits": order}, fh)
    return manifest, plan_path


def run_driver(driver, plan, tag, bit, max_old="350"):
    summary = os.path.join(WORK, tag + ".summary.json")
    certdir = os.path.join(WORK, tag + ".certs")
    if os.path.exists(summary) and os.path.getsize(summary) > 0:
        return json.load(open(summary, encoding="utf-8")), certdir
    os.makedirs(certdir, exist_ok=True)
    plan_arg = os.path.join(WORK, tag + ".plan.json")
    full = json.load(open(plan, encoding="utf-8"))
    full["bits"] = [b for b in full["bits"] if b["bit"] == bit]
    with open(plan_arg, "w", encoding="utf-8") as fh:
        json.dump(full, fh)
    cmd = [NODE, "--experimental-strip-types",
           "--max-old-space-size=" + max_old, driver, plan_arg,
           summary, certdir]
    subprocess.run(cmd, check=True)
    return json.load(open(summary, encoding="utf-8")), certdir


def published_cert_bytes(manifest, bit):
    c = [x for x in manifest["certificates"] if x["bit"] == bit][0]
    fn = c["file"]
    if c.get("split_cut_byte") is not None:
        return (open(os.path.join(CERTDIR, fn + ".part1of2"), "rb").read() +
                open(os.path.join(CERTDIR, fn + ".part2of2"), "rb").read())
    return open(os.path.join(CERTDIR, fn), "rb").read()


def verify_snapshot(summary, certdir, manifest, bit):
    fname = [c for c in manifest["certificates"]
             if c["bit"] == bit][0]["file"]
    snap = open(os.path.join(certdir, fname), "rb").read()
    pub = published_cert_bytes(manifest, bit)
    return snap == pub, hashlib.md5(snap).hexdigest()


def run_variant(fix_level, ms_shift, manifest, plan, bits, state,
                max_old="350"):
    driver = make_driver(fix_level, ms_shift)
    per_bit = []
    total = 0
    import time
    t0 = time.time()
    for b in bits:
        tag = "fix%s_ms%d_bit%d" % (fix_level, ms_shift, b)
        summary, certdir = run_driver(driver, plan, tag, b, max_old)
        p = summary["per_bit"][0]
        if (not p.get("per_move_ok", False)
                or summary.get("fbt_drops", 1) != 0):
            raise SystemExit("INVALID bit %d fix%s: per_move_ok=%s fbt_drops=%s"
                             % (b, fix_level, p.get("per_move_ok"),
                                summary.get("fbt_drops")))
        same, md5 = verify_snapshot(summary, certdir, manifest, b)
        per_bit.append({
            "bit": b,
            "nodes": p["nodes_this_run"],
            "moves": p["moves"],
            "rows": p["rows"],
            "published_rows": p["published_rows"],
            "memo_occupied_after": p["memo_occupied_after"],
            "memo_slots": p["memo_slots"],
            "ms_wall": p["ms"],
            "verbatim_fresh_ms23_nodes": VERBATIM_FRESH23[b],
            "nodes_vs_verbatim_fresh23": (
                p["nodes_this_run"] / VERBATIM_FRESH23[b]),
            "byte_identical": same,
            "md5": md5,
        })
        total += p["nodes_this_run"]
        state["fix%s_ms%d" % (fix_level, ms_shift)] = {
            "status": "running", "done_bits": len(per_bit),
            "per_bit": per_bit, "total_nodes_so_far": total}
        save(state)
    return {
        "fix_level": fix_level, "ms_shift": ms_shift,
        "fresh_process_per_bit": True,
        "total_nodes": total,
        "total_vs_verbatim_fresh23": total / VERBATIM_FRESH23_TOTAL,
        "total_vs_published_ms18": total / PUBLISHED_TOTAL,
        "byte_identical": (sum(1 for x in per_bit if x["byte_identical"]),
                           len(per_bit)),
        "wall_s": round(time.time() - t0, 1),
        "per_bit": per_bit}


OUTJSON = None


def save(state):
    with open(OUTJSON, "w", encoding="utf-8") as fh:
        json.dump(state, fh, indent=1, sort_keys=True)


def main():
    global OUTJSON
    OUTJSON = sys.argv[1]
    os.makedirs(WORK, exist_ok=True)
    check_pin("extractor", EXTRACTOR, EXTRACTOR_BLOB)
    check_pin("legal_candidates", LEGAL, LEGAL_BLOB)
    check_pin("manifest", MANIFEST, MANIFEST_BLOB)
    state = {"schema": "n11-class2-lane-fixed-memo-battery-73k-20261117",
             "date": "2026-11-17",
             "status": "running"}
    save(state)
    manifest, plan = build_plan()
    bits = [b["bit"] for b in json.load(open(plan))["bits"]]

    # make both variants once up-front (also asserts patch surgery)
    make_fixed_variant("A", 23)
    make_fixed_variant("B", 23)

    # determinism gate: fixB bit0 twice
    driver = make_driver("B", 23)
    s1, _ = run_driver(driver, plan, "detB_bit0_run1", 0)
    n1 = s1["per_bit"][0]["nodes_this_run"]
    s2, _ = run_driver(driver, plan, "detB_bit0_run2", 0)
    n2 = s2["per_bit"][0]["nodes_this_run"]
    state["determinism_gate"] = {"fixB_bit0_nodes_run1": n1,
                                 "fixB_bit0_nodes_run2": n2,
                                 "identical": n1 == n2}
    save(state)

    # NOTE: fixA battery first, then fixB (sequential, single-core each)
    state["fixA_ms23"] = run_variant("A", 23, manifest, plan, bits, state)
    save(state)
    state["fixB_ms23"] = run_variant("B", 23, manifest, plan, bits, state)

    okA = state["fixA_ms23"]["byte_identical"]
    okB = state["fixB_ms23"]["byte_identical"]
    A, B = state["fixA_ms23"], state["fixB_ms23"]
    A_nodes = {p["bit"]: p["nodes"] for p in A["per_bit"]}
    B_nodes = {p["bit"]: p["nodes"] for p in B["per_bit"]}
    A_occ = {p["bit"]: p["memo_occupied_after"] for p in A["per_bit"]}
    B_occ = {p["bit"]: p["memo_occupied_after"] for p in B["per_bit"]}
    state["observations"] = {
        "fixA_vs_fixB_occupancy_identical": A_occ == B_occ,
        "fixA_per_bit_occupied": A_occ,
        "fixB_per_bit_occupied": B_occ,
        "fixA_per_bit_nodes": A_nodes,
        "fixB_per_bit_nodes": B_nodes,
    }
    state["gates"] = {
        "fixA_byte_identical_all": okA[0] == okA[1],
        "fixB_byte_identical_all": okB[0] == okB[1],
        "determinism_fixB_bit0": state["determinism_gate"]["identical"],
        "all_bits_ok_no_fbt_drops": True,
        "fixA_total_matches_expected":
            A["total_nodes"] == EXPECTED_FIXED["fixA_total_nodes"],
        "fixB_total_matches_expected":
            B["total_nodes"] == EXPECTED_FIXED["fixB_total_nodes"],
        "fixB_bit0_matches_expected":
            B_nodes[0] == EXPECTED_FIXED["fixB_bit0_nodes"],
        "fixB_bit95_matches_expected":
            B_nodes[95] == EXPECTED_FIXED["fixB_bit95_nodes"],
        "fixA_bit0_occupied_matches_expected":
            A_occ[0] == EXPECTED_FIXED["fixA_bit0_occupied"],
        "fixA_occupancy_equals_fixB": A_occ == B_occ,
    }
    if not all(state["gates"].values()):
        state["status"] = "GATE_FAILURE"
        save(state)
        raise SystemExit("regression gate failure: %s"
                         % {k: v for k, v in state["gates"].items()
                            if not v})
    state["status"] = "complete"
    save(state)
    print("fixA total:", state["fixA_ms23"]["total_nodes"],
          "byte-identical:", okA)
    print("fixB total:", state["fixB_ms23"]["total_nodes"],
          "byte-identical:", okB)
    print("verbatim fresh23 total:", VERBATIM_FRESH23_TOTAL)


if __name__ == "__main__":
    main()
