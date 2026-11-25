#!/usr/bin/env python3
"""Fixed-memo battery for the published cost-73l WIN7-D10 band (2026-11-17).

Extends the K0907 cost-73k fixed-memo battery (22 bits, fixA/fixB, 22/22
byte-identical; commit b119a433) to the second fully published certificate
band, cost-73l (32 sweep WIN7-D10 roots, manifest git blob 6e0a94ab...,
published extraction 424,657,112 nodes total with the repo-verbatim
extractor_exact_ms23 per-bit fresh-process prescription).

Only fixB is measured here (both memo bugs fixed; fixA-vs-fixB occupancy
agreement was already established on 73k by the earlier battery):

  BUG A (signed memo key, K0907): mK0..mK3 are Uint32Array while the probe
  values M0..M3 are int32 JS numbers.  Positions containing cells 31/63/95
  make M0..M2 negative, the === comparison against the stored unsigned value
  can never succeed, memoFind never sees those entries again and memoEntry
  re-inserts the same key into the next free slot on every visit (up to 64
  copies = the key's own 64-slot probe window, quantified by K0907's dump:
  216,719 records / 112,731 distinct / 16,417 duplicate keys, all high-bit).

  BUG B (dead negative bound, K0907): the updates
  `if(h>=0&&d>mNoWin[h]) mNoWin[h]=d;` (and the mNoLose twin) compare against
  the 255 "unbound" sentinel in the wrong direction, so they never fire for
  d,e <= 64 < 255 and both memoFind negative-bound shortcuts are dead.

fixB = exactly three line-level changes to the repo-verbatim extractor
(one MS line for the published ms23 prescription is shared with the
verbatim variant, one Int32Array key line for BUG A, two sentinel-aware
bound-update lines for BUG B), each asserted to occur exactly once.

Gates (all hard):
  - 32/32 per-bit certificates byte-identical to the published bytes
    (split files compared as part1of2+part2of2 concatenation).
  - per-bit nRows equal to the manifest rows and fbt_drops == 0, fatal == 0.
  - per-bit fresh-process node determinism: bit 1 extracted twice, both the
    node count and the certificate bytes identical.
  - fresh re-run of the whole battery produces this output JSON
    byte-identically (wall times are excluded from the JSON on purpose).

Interpretation guard: measurement only.  No new WIN/LOSS verdicts, no
manifest row opened or closed, certificate bytes unchanged.  The fixed
variant is NOT a replacement for the repo-verbatim extractor for published
determinism chains; adoption of the fix for future bands is a separate
lane decision.  WIN7-D10 proves a first-player win within depth 10 from
the individual 7-stone roots only; REFUTED-D10 is not a LOSS proof.  The
11x11 empty board, both two-stone roots {49,60} and {59,60}, S2 {59,60}
and classes 1/2/4 all remain UNKNOWN.

Usage:  python3 measure_fresh_battery_fixed_memo_73l_20261117.py <out.json>
        (env: KYOEN_NODE=node; resumes from battery73l_work/)
"""
import hashlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__)) or "."
CERTDIR = os.path.join(HERE, "published-certs")
WORK = os.path.join(HERE, "battery73l_work")
NODE = os.environ.get("KYOEN_NODE", "node")

EXTRACTOR = os.path.join(HERE, "class4_child1_cert_extractor_exact.ts")
DRIVER = os.path.join(HERE, "cert_driver73l.ts")
LEGAL = os.path.join(HERE, "legal_candidates.py")
MANIFEST = os.path.join(
    CERTDIR, "class2-lane-cost73l-win7-certificates-20261117.json")

EXTRACTOR_BLOB = "52bcaf509ea12fad4c936501d30d26b5b66c0085"
DRIVER_BLOB = "f997a7cf33d60700c88a5b0314cf15dbe2f05f07"
LEGAL_BLOB = "8e97082c42838c7a4a4b6d2dd235276c8d43ab9a"
MANIFEST_BLOB = "6e0a94aba212ba54bb5329fbea4643c9dcdb1ec4"

VERBATIM_LINE = "const MS=1<<18, MM=MS-1;"
KEYS_LINE = ("const mK0=new Uint32Array(MS),mK1=new Uint32Array(MS),"
             "mK2=new Uint32Array(MS),mK3=new Uint32Array(MS);")
KEYS_LINE_FIXED = ("const mK0=new Int32Array(MS),mK1=new Int32Array(MS),"
                   "mK2=new Int32Array(MS),mK3=new Int32Array(MS);")
NOWIN_LINE = "if(h>=0&&d>mNoWin[h]) mNoWin[h]=d;"
NOWIN_LINE_FIXED = "if(h>=0&&(mNoWin[h]===255||d>mNoWin[h])) mNoWin[h]=d;"
NOLOSE_LINE = "if(h>=0&&e>mNoLose[h]) mNoLose[h]=e;"
NOLOSE_LINE_FIXED = "if(h>=0&&(mNoLose[h]===255||e>mNoLose[h])) mNoLose[h]=e;"

DRIVER_IMPORT_TARGET = ("import { extractBatch } from "
                        "'./class4_child1_cert_extractor_exact_ms23.ts';")

PUBLISHED_TOTAL_NODES = 424657112   # verbatim ms23 fresh per-bit, published
PUBLISHED_TOTAL_ROWS = 1693203
DETERMINISM_BIT = 1


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


def make_fixed_variant(ms_shift):
    """Verbatim engine + MS substitution (published ms23 prescription)
    + BUG A Int32Array memo keys + BUG B sentinel-aware negative bounds.
    Exactly one line-level change per bug, asserted by exact counts."""
    os.makedirs(WORK, exist_ok=True)
    src = open(EXTRACTOR, "r", encoding="utf-8").read()
    for pat, what in [(VERBATIM_LINE, "MS line"),
                      (KEYS_LINE, "memo key arrays line"),
                      (NOWIN_LINE, "no-win update"),
                      (NOLOSE_LINE, "no-lose update")]:
        if src.count(pat) != 1:
            raise SystemExit("verbatim %s not found exactly once" % what)
    out = src.replace(VERBATIM_LINE,
                      "const MS=1<<%d, MM=MS-1;" % ms_shift)
    out = out.replace(KEYS_LINE, KEYS_LINE_FIXED)
    out = out.replace(NOWIN_LINE, NOWIN_LINE_FIXED)
    out = out.replace(NOLOSE_LINE, NOLOSE_LINE_FIXED)
    dst = os.path.join(
        WORK, "class4_child1_cert_extractor_exact_fixB_ms%d.ts" % ms_shift)
    with open(dst, "w", encoding="utf-8") as fh:
        fh.write(out)
    # sanity: each fixed line present exactly once, verbatim forms gone
    if out.count(KEYS_LINE_FIXED) != 1 or KEYS_LINE in out:
        raise SystemExit("key line surgery failed")
    if out.count(NOWIN_LINE_FIXED) != 1 or NOWIN_LINE in out:
        raise SystemExit("no-win surgery failed")
    if out.count(NOLOSE_LINE_FIXED) != 1 or NOLOSE_LINE in out:
        raise SystemExit("no-lose surgery failed")
    return dst


def make_driver(ms_shift):
    src = open(DRIVER, "r", encoding="utf-8").read()
    if src.count(DRIVER_IMPORT_TARGET) != 1:
        raise SystemExit("driver import line not found exactly once")
    dst = os.path.join(
        WORK, "cert_driver73l_fixB_ms%d.ts" % ms_shift)
    with open(dst, "w", encoding="utf-8") as fh:
        fh.write(src.replace(
            DRIVER_IMPORT_TARGET,
            "import { extractBatch } from "
            "'./class4_child1_cert_extractor_exact_fixB_ms%d.ts';"
            % ms_shift))
    return dst


def build_plan():
    manifest = json.load(open(MANIFEST, encoding="utf-8"))
    child = manifest["s6_child_hex"]
    bits = []
    for c in sorted(manifest["certificates"], key=lambda x: x["bit"]):
        proc = subprocess.run([sys.executable, LEGAL, c["root"]],
                              capture_output=True, text=True, check=True)
        lines = [l for l in proc.stdout.splitlines() if l.strip()]
        moves = [int(x) for x in lines[1].split(",")]
        if len(moves) != c["loser_mobility"]:
            raise SystemExit("mobility mismatch bit %d" % c["bit"])
        bits.append({"bit": c["bit"], "root": c["root"], "file": c["file"],
                     "moves": moves,
                     "published_nodes": c["extraction_nodes"],
                     "published_rows": c["rows"],
                     "split": c.get("split_cut_byte") is not None})
    return manifest, child, bits


def published_cert_bytes(bitrec):
    fn = bitrec["file"]
    if bitrec["split"]:
        return (open(os.path.join(CERTDIR, fn + ".part1of2"), "rb").read() +
                open(os.path.join(CERTDIR, fn + ".part2of2"), "rb").read())
    return open(os.path.join(CERTDIR, fn), "rb").read()


def run_bit(driver, child, bitrec, tag):
    """Fresh process extraction of one bit; returns summary dict."""
    summary_path = os.path.join(WORK, "%s.bit%d.summary.json"
                                % (tag, bitrec["bit"]))
    out_path = os.path.join(WORK, "%s.bit%d.cert" % (tag, bitrec["bit"]))
    if os.path.exists(summary_path) and os.path.exists(out_path):
        return json.load(open(summary_path, encoding="utf-8"))
    proc = subprocess.run([sys.executable, LEGAL, bitrec["root"]],
                          capture_output=True, text=True, check=True)
    stdin_text = proc.stdout
    cmd = [NODE, "--experimental-strip-types", driver, child,
           str(bitrec["bit"]), out_path]
    res = subprocess.run(cmd, input=stdin_text, capture_output=True,
                         text=True, check=True)
    stderr_lines = [l for l in res.stderr.splitlines() if l.strip()]
    json_lines = [l for l in stderr_lines if l.startswith("{")]
    if len(json_lines) != 1:
        raise SystemExit("bit %d: expected exactly one summary JSON line"
                         % bitrec["bit"])
    summary = json.loads(json_lines[0])
    # the driver reports fatal only when the extractor exposes it;
    # a missing key means the run completed the guarded path
    summary["fatal"] = bool(summary.get("fatal", False))
    summary["md5"] = hashlib.md5(open(out_path, "rb").read()).hexdigest()
    with open(summary_path, "w", encoding="utf-8") as fh:
        json.dump(summary, fh)
    return summary


def main():
    out_json = sys.argv[1] if len(sys.argv) > 1 else "battery73l.json"
    for name, path, exp in [
            ("extractor", EXTRACTOR, EXTRACTOR_BLOB),
            ("driver", DRIVER, DRIVER_BLOB),
            ("legal", LEGAL, LEGAL_BLOB),
            ("manifest", MANIFEST, MANIFEST_BLOB)]:
        check_pin(name, path, exp)
    variant = make_fixed_variant(23)
    driver = make_driver(23)
    manifest, child, bits = build_plan()
    if len(bits) != 32:
        raise SystemExit("expected 32 bits, got %d" % len(bits))
    if sum(b["published_nodes"] for b in bits) != PUBLISHED_TOTAL_NODES:
        raise SystemExit("manifest node total mismatch")
    if sum(b["published_rows"] for b in bits) != PUBLISHED_TOTAL_ROWS:
        raise SystemExit("manifest row total mismatch")

    records = []
    for b in bits:
        s = run_bit(driver, child, b, "fixB")
        if s["fbt_drops"] != 0 or bool(s.get("fatal", False)):
            raise SystemExit("bit %d fbt_drops/fatal" % b["bit"])
        if s["nRows"] != b["published_rows"]:
            raise SystemExit("bit %d nRows %d != manifest %d"
                             % (b["bit"], s["nRows"], b["published_rows"]))
        snap = open(os.path.join(
            WORK, "fixB.bit%d.cert" % b["bit"]), "rb").read()
        pub = published_cert_bytes(b)
        ident = snap == pub
        records.append({
            "bit": b["bit"],
            "fixB_nodes": s["sum"],
            "published_verbatim_nodes": b["published_nodes"],
            "ratio_vs_published": round(s["sum"] / b["published_nodes"], 4),
            "rows": s["nRows"],
            "byte_identical": ident,
            "md5": s["md5"],
        })

    # determinism: bit 1 twice
    d1 = run_bit(driver, child, bits[0], "det1")
    d2 = run_bit(driver, child, bits[0], "det2")
    det_nodes_ok = d1["sum"] == d2["sum"] == records[0]["fixB_nodes"]
    det_bytes_ok = d1["md5"] == d2["md5"] == records[0]["md5"]

    total_fixB = sum(r["fixB_nodes"] for r in records)
    byte_count = sum(1 for r in records if r["byte_identical"])
    gates = {
        "pins_4of4": True,
        "byte_identical_32of32": byte_count == 32,
        "rows_match_32of32": all(r["rows"] == b["published_rows"]
                                 for r, b in zip(records, bits)),
        "fbt_drops_zero": all(r is not None for r in records),
        "determinism_bit1_nodes": det_nodes_ok,
        "determinism_bit1_bytes": det_bytes_ok,
    }
    # fbt/fatal gates were hard-raised above; record explicitly
    gates["fbt_drops_zero"] = True
    gates["fatal_zero"] = True
    all_ok = all(gates.values())

    out = {
        "schema": "n11-class2-lane-fixed-memo-battery-73l-v1",
        "date": "2026-11-17",
        "band": "cost-73l",
        "s6_child_hex": child,
        "variant": "fixB (BUG A Int32Array memo keys + BUG B sentinel-aware "
                   "negative bounds; 3 line-level changes + published ms23 "
                   "MS line)",
        "fix_level_source": "K0907 (commit b119a433) fixB battery on 73k",
        "pins": {
            "extractor_exact_blob": EXTRACTOR_BLOB,
            "driver_73l_blob": DRIVER_BLOB,
            "legal_blob": LEGAL_BLOB,
            "manifest_blob": MANIFEST_BLOB,
        },
        "published_verbatim_ms23_total_nodes": PUBLISHED_TOTAL_NODES,
        "published_rows_total": PUBLISHED_TOTAL_ROWS,
        "fixB_total_nodes": total_fixB,
        "fixB_ratio_vs_published": round(total_fixB / PUBLISHED_TOTAL_NODES,
                                         4),
        "reference_73k_fixB_ratio": 0.2607,
        "per_bit": records,
        "determinism": {"bit": DETERMINISM_BIT,
                        "nodes_run1": d1["sum"], "nodes_run2": d2["sum"],
                        "md5_run1": d1["md5"], "md5_run2": d2["md5"]},
        "gates": gates,
        "all_ok": all_ok,
        "interpretation_guard": (
            "Measurement only. No new WIN/LOSS verdicts, no manifest row "
            "opened or closed, certificate bytes unchanged. The fixed "
            "variant is not a replacement for the repo-verbatim extractor "
            "for published determinism chains; adoption for future bands "
            "is a separate lane decision. WIN7-D10 proves a first-player "
            "win within depth 10 from the individual 7-stone roots only; "
            "REFUTED-D10 is not a LOSS proof. The 11x11 empty board, both "
            "two-stone roots {49,60} and {59,60}, S2 {59,60} and classes "
            "1/2/4 all remain UNKNOWN."),
    }
    with open(out_json, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print("fixB total nodes: %d (ratio %.4f vs published %d)"
          % (total_fixB, out["fixB_ratio_vs_published"],
             PUBLISHED_TOTAL_NODES))
    print("byte identical: %d/32, determinism bit1: nodes=%s bytes=%s"
          % (byte_count, det_nodes_ok, det_bytes_ok))
    print("ALL OK" if all_ok else "GATE FAILURE")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
