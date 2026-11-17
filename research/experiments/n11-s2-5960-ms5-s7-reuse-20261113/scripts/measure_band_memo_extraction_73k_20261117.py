#!/usr/bin/env python3
"""Band-wide memo-capacity measurement for the cost-73k extraction lane (2026-11-17).

Published alongside this script:
  output/class2-lane-band-memo-extraction-measurement-73k-20261117.json
  scripts/measure_band_memo_extraction_73k.ts (driver)

Motivation.  The certificate extractor class4_child1_cert_extractor_exact.ts
(git blob 52bcaf509ea12fad4c936501d30d26b5b66c0085) uses a process-global
position memo (MS=1<<18 slots, 64-probe linear probing; memoEntry silently
skips storing when a probe chain is exhausted, memoFind then treats the entry
as absent, which is sound but costs recomputation).  The published cost-73k
band (22 WIN7-D10 certificates, manifest git blob
0892aed07d187ae2fb3b4b90a21c7adbc1002b62) was extracted with that verbatim
engine in one fresh process per bit: 155,946,109 extraction nodes total.
The same-day 73j measurement (measure_band_memo_extraction_73j_20261117.py,
commit c206a4be) showed for the 16-bit cost-73j band that memo capacity, not
band state sharing, drives the extraction cost (fresh ms24 -44.7%,
band-wide ms24 +2.24% vs fresh).  This script replicates and extends that
measurement on the larger 22-bit 73k band with:
  - a capacity ladder at fixed band-wide sharing (MS=1<<18 / 1<<22 / 1<<23,
    plus a best-effort MS=1<<24 attempt),
  - memo occupancy instrumentation (occupied slots after every bit; the
    patched variants export memoStats()),
  - a fresh per-bit attribution battery at MS=1<<23 (and best-effort 1<<24),
  - a per-root capacity-sensitivity battery (bit 117, the band's largest
    root, fresh process at MS=1<<18,20,21,22,23,24),
  - byte-identity verification of EVERY per-root certificate snapshot
    against the published certificates (split files concatenated) in every
    configuration.

The extractor variant is generated here from the repo-verbatim engine with
exactly two changes, verified line-diff-wise: the one-line MS substitution
and an inserted export block (clearRows() + memoStats()) before extractBatch.
Neither changes any search behavior; the driver only records.

Expected values measured on 2026-11-17 (embedded as regression gates):
  - band ms18 (verbatim capacity, band-wide): 205,129,712 nodes
    (+31.54% vs published; the memo saturates inside bit 0, which alone
    occupies 598,661 slots > 262,144), per-bit ratios 1.0000 (bit 0) up to
    1.7505 (bit 39); 22/22 certificates byte-identical.
  - band ms22: 142,171,197 nodes (-8.83%), final occupancy 4,067,454/4,194,304
    (96.98%, still starved - late bits degrade).
  - band ms23: 121,186,659 nodes (-22.29%), final occupancy 7,144,086/8,388,608
    (85.16%).
  - fresh per-bit ms23 battery: 108,499,241 nodes (-30.43% vs published),
    22/22 certificates byte-identical; per-bit published/fresh node ratios
    1.2750..1.7098 except bit 95 = 1.0000.
  - sharing penalty (band ms23 vs fresh ms23, same capacity): +11.69% total;
    per-bit band/fresh ratios 0.9466..1.3380, growing with bit position
    (open-addressing cluster pollution at load factor 0.68..0.85).  Only
    bits 39/41 profit from band sharing (0.9651/0.9466); bit 95 is
    memo-state-invariant (identical node count in every configuration).
  - sensitivity bit 117 fresh ms18: 10,635,766 nodes (= published value).

Interpretation guard: measurement only.  No new WIN/LOSS verdicts, no
manifest row opened or closed, certificate bytes unchanged, published sweep
verdicts unchanged.  WIN7-D10 proves a first-player win within depth 10
from the individual 7-stone roots only; REFUTED-D10 is not a LOSS proof.
The 11x11 empty board, both two-stone roots {49,60} and {59,60}, S2 {59,60}
and classes 1/2/4 all remain UNKNOWN.

Usage:  python3 measure_band_memo_extraction_73k_20261117.py <out.json>
        (env: KYOEN_NODE=node, optional KYOEN_NODE_MAX_OLD_SPACE=350;
        full re-run takes roughly 40 min single-core and needs ~750 MB peak
        for the best-effort MS=1<<24 steps; every step resumes from the
        work directory output/band_memo_measurement_73k_work/)
"""
import hashlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__)) or "."
EXP = os.path.dirname(os.path.abspath(HERE))
OUT = os.path.join(EXP, "output")
CERTDIR = os.path.join(OUT, "class2-lane-cost73k-certificates")
WORK = os.path.join(OUT, "band_memo_measurement_73k_work")
NODE = os.environ.get("KYOEN_NODE", "node")
MAX_OLD = os.environ.get("KYOEN_NODE_MAX_OLD_SPACE", "350")

EXTRACTOR = os.path.join(HERE, "class4_child1_cert_extractor_exact.ts")
DRIVER = os.path.join(HERE, "measure_band_memo_extraction_73k.ts")
LEGAL = os.path.join(HERE, "legal_candidates.py")
MANIFEST = os.path.join(
    CERTDIR, "class2-lane-cost73k-win7-certificates-20261117.json")

EXTRACTOR_BLOB = "52bcaf509ea12fad4c936501d30d26b5b66c0085"
MANIFEST_BLOB = "0892aed07d187ae2fb3b4b90a21c7adbc1002b62"
LEGAL_BLOB = "8e97082c42838c7a4a4b6d2dd235276c8d43ab9a"

VERBATIM_LINE = "const MS=1<<18, MM=MS-1;"
PATCH_ANCHOR = ("export function extractBatch(childHex: string, bit: number, "
                "killTable: Record<number, number>, moves: number[]) {")
PATCH_BLOCK = """// EXPERIMENT MODIFICATION (2026-11-17, band-memo capacity measurement only;
// not a replacement for the published extractor): expose a row-set reset and
// an occupancy probe so several roots can be extracted in ONE process while
// the module-level search memo and forbidden-bit cache persist across roots.
export function clearRows(): void { rows.clear(); }
export function memoStats(): { slots: number, occupied: number } {
  let c = 0; for (let i = 0; i < MS; i++) if (mOcc[i]) c++;
  return { slots: MS, occupied: c };
}
"""

DRIVER_IMPORT_TARGET = \
    "import { extractBatch, clearRows, memoStats } from './class4_child1_cert_extractor_exact_memo18.ts';"

EXPECTED = {
    "bits": [0, 7, 11, 15, 35, 39, 41, 44, 58, 62, 73, 76,
             87, 89, 94, 95, 97, 98, 103, 105, 112, 117],
    "published_total_nodes": 155946109,
    "band18_total": 205129712,
    "band18_bit0_nodes": 6442831,       # band start = fresh process
    "band18_bit95_nodes": 11857737,     # memo-state-invariant root
    "band22_total": 142171197,
    "band22_final_occupied": 4067454,
    "band23_total": 121186659,
    "band23_final_occupied": 7144086,
    "fresh23_total": 108499241,
    "fresh23_per_bit": {
        0: 4303203, 7: 4970943, 11: 2910026, 15: 8108353, 35: 4871692,
        39: 2037105, 41: 1868639, 44: 4617329, 58: 4567866, 62: 1771346,
        73: 7370204, 76: 4098489, 87: 6581793, 89: 3869180, 94: 4204274,
        95: 11857737, 97: 3815019, 98: 5336993, 103: 5828967, 105: 3641568,
        112: 4767520, 117: 7100995},
    "sensitivity_bit117_ms18": 10635766,   # == published extraction_nodes
    "bit117_published_rows": 59587,
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
        raise SystemExit("%s BLOB MISMATCH: %s != %s" % (name, actual, expected))


def make_variant(ms_shift):
    """Verbatim engine + MS substitution + clearRows/memoStats export block.

    The ONLY code changes vs the repo-verbatim engine are the `const MS=...`
    line and the inserted export block; asserted by exact string surgery.
    Neither changes search behavior (clearRows/memoStats are only called by
    the measurement driver between extractBatch calls).
    """
    os.makedirs(WORK, exist_ok=True)
    src = open(EXTRACTOR, "r", encoding="utf-8").read()
    if src.count(VERBATIM_LINE) != 1:
        raise SystemExit("verbatim MS line not found exactly once")
    if src.count(PATCH_ANCHOR) != 1:
        raise SystemExit("patch anchor not found exactly once")
    dst = os.path.join(
        WORK, "class4_child1_cert_extractor_exact_memo%d.ts" % ms_shift)
    out = src.replace(VERBATIM_LINE,
                     "const MS=1<<%d, MM=MS-1;" % ms_shift)
    out = out.replace(PATCH_ANCHOR, PATCH_BLOCK + PATCH_ANCHOR)
    # verify: removing the patch block from the variant must reproduce the
    # verbatim engine with exactly the MS line substituted
    stripped = out.replace(PATCH_BLOCK, "")
    if stripped != src.replace(VERBATIM_LINE,
                               "const MS=1<<%d, MM=MS-1;" % ms_shift):
        raise SystemExit("variant ms%d differs by more than MS + patch block"
                         % ms_shift)
    with open(dst, "w", encoding="utf-8") as fh:
        fh.write(out)
    return dst


def make_driver(ms_shift):
    """The published driver with only the import line retargeted at a variant."""
    src = open(DRIVER, "r", encoding="utf-8").read()
    if DRIVER_IMPORT_TARGET not in src:
        raise SystemExit("driver import line not found")
    dst = os.path.join(
        WORK, "measure_band_memo_extraction_73k_ms%d.ts" % ms_shift)
    with open(dst, "w", encoding="utf-8") as fh:
        fh.write(src.replace(
            DRIVER_IMPORT_TARGET,
            "import { extractBatch, clearRows, memoStats } from "
            "'./class4_child1_cert_extractor_exact_memo%d.ts';" % ms_shift))
    return dst


def build_plan():
    """child + per-bit {bit, root, file, moves, published_nodes, published_rows}."""
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
    if [b["bit"] for b in order] != EXPECTED["bits"]:
        raise SystemExit("bit list mismatch")
    plan_path = os.path.join(WORK, "plan73k.json")
    with open(plan_path, "w", encoding="utf-8") as fh:
        json.dump({"child": child, "bits": order}, fh)
    return plan_path, sum(b["published_nodes"] for b in order)


def run_driver(driver, plan, tag, bits=None, max_old=None):
    """Run one driver invocation with resume; returns (summary, certDir)."""
    summary = os.path.join(WORK, tag + ".summary.json")
    certdir = os.path.join(WORK, tag + ".certs")
    if os.path.exists(summary) and os.path.getsize(summary) > 0:
        return json.load(open(summary, encoding="utf-8")), certdir  # resume
    os.makedirs(certdir, exist_ok=True)
    plan_arg = plan
    if bits is not None:
        # fresh single-bit battery: write a one-bit plan
        plan_arg = os.path.join(WORK, tag + ".plan.json")
        full = json.load(open(plan, encoding="utf-8"))
        full["bits"] = [b for b in full["bits"] if b["bit"] == bits]
        with open(plan_arg, "w", encoding="utf-8") as fh:
            json.dump(full, fh)
    cmd = [NODE, "--experimental-strip-types", driver, plan_arg,
           summary, certdir]
    if max_old:
        cmd[1:1] = ["--max-old-space-size=" + max_old]
    subprocess.run(cmd, check=True)
    return json.load(open(summary, encoding="utf-8")), certdir


def published_cert_bytes(manifest, bit):
    c = [x for x in manifest["certificates"] if x["bit"] == bit][0]
    fn = c["file"]
    if c.get("split_cut_byte") is not None:
        return (open(os.path.join(CERTDIR, fn + ".part1of2"), "rb").read() +
                open(os.path.join(CERTDIR, fn + ".part2of2"), "rb").read())
    return open(os.path.join(CERTDIR, fn), "rb").read()


def verify_snapshots(summary, certdir, manifest):
    """Every per-root snapshot must be byte-identical to the published cert."""
    results = []
    ok = 0
    for p in summary["per_bit"]:
        fname = [c for c in manifest["certificates"]
                 if c["bit"] == p["bit"]][0]["file"]
        snap = open(os.path.join(certdir, fname), "rb").read()
        pub = published_cert_bytes(manifest, p["bit"])
        same = snap == pub
        ok += 1 if same else 0
        results.append({"bit": p["bit"], "byte_identical": same,
                        "rows": p["rows"],
                        "md5": hashlib.md5(snap).hexdigest()})
    return ok, results


def main():
    os.makedirs(WORK, exist_ok=True)
    check_pin("extractor", EXTRACTOR, EXTRACTOR_BLOB)
    check_pin("manifest", MANIFEST, MANIFEST_BLOB)
    check_pin("legal_candidates", LEGAL, LEGAL_BLOB)
    manifest = json.load(open(MANIFEST, encoding="utf-8"))

    plan_path, pub_total = build_plan()
    if pub_total != EXPECTED["published_total_nodes"]:
        raise SystemExit("published node total mismatch: %d" % pub_total)

    failures = []
    def expect(name, got, want):
        if got != want:
            failures.append({"check": name, "expected": want, "got": got})

    record = {
        "schema": ("n11-class2-lane-band-memo-extraction-"
                   "measurement-73k-20261117-v1"),
        "date": "2026-11-17",
        "lane": "n11 class2-lane long-term lane (cost-73k band)",
        "purpose": ("measurement of the extraction-memo (position-keyed "
                    "win/loss table) capacity effect and of band-wide "
                    "cross-root memo sharing on certificate extraction cost "
                    "for the published cost-73k WIN7-D10 band; no new "
                    "verdicts, no certificate bytes changed"),
        "inputs": {
            "extractor_engine": {
                "path": "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/class4_child1_cert_extractor_exact.ts",
                "git_blob_sha": EXTRACTOR_BLOB,
                "memo_spec": ("MS=1<<18 slots, 64-probe linear probing, "
                              "memoEntry silently skips on chain exhaustion"),
            },
            "manifest": {
                "path": "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost73k-certificates/class2-lane-cost73k-win7-certificates-20261117.json",
                "git_blob_sha": MANIFEST_BLOB,
            },
            "candidate_enumerator": {
                "path": "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/legal_candidates.py",
                "git_blob_sha": LEGAL_BLOB,
            },
            "driver": {
                "path": "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/measure_band_memo_extraction_73k.ts",
            },
            "precedent_73j": {
                "path": "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/measure_band_memo_extraction_73j_20261117.py",
                "commit": "c206a4be",
                "note": ("same-day 73j band capacity measurement: fresh ms24 "
                         "-44.7%, band-wide ms24 +2.24% vs fresh (sharing "
                         "non-contributory); this 73k entry replicates the "
                         "capacity effect on the 22-bit band and adds memo "
                         "occupancy instrumentation, the ms22 intermediate "
                         "point, and a per-root sharing penalty table"),
            },
        },
        "published_baseline": {
            "child_hex": manifest["s6_child_hex"],
            "bits": EXPECTED["bits"],
            "per_bit_fresh_process_extraction_nodes_total": pub_total,
        },
    }

    def save():
        with open(sys.argv[1], "w", encoding="utf-8") as fh:
            json.dump(record, fh, indent=1, sort_keys=False)
            fh.write("\n")

    # ---- band-wide runs (memo carried across the 22 bits, ascending order) ----
    band_runs = {}
    for ms, tag, total, occ in (
            (18, "band_memo_ms18", EXPECTED["band18_total"], None),
            (22, "band_memo_ms22", EXPECTED["band22_total"],
             EXPECTED["band22_final_occupied"]),
            (23, "band_memo_ms23", EXPECTED["band23_total"],
             EXPECTED["band23_final_occupied"])):
        make_variant(ms)
        summary, certdir = run_driver(make_driver(ms), plan_path, tag)
        n_ok, snaps = verify_snapshots(summary, certdir, manifest)
        expect(tag + "_total", summary["total_nodes_single_process_with_band_memo"], total)
        expect(tag + "_fbt_drops", summary["fbt_drops"], 0)
        expect(tag + "_byte_identical", n_ok, 22)
        if occ is not None:
            expect(tag + "_final_occupied",
                   summary["per_bit"][-1]["memo_occupied_after"], occ)
        band_runs[ms] = {
            "memo_slots": 1 << ms,
            "total_nodes": summary["total_nodes_single_process_with_band_memo"],
            "vs_published": round(summary["total_nodes_single_process_with_band_memo"] / pub_total, 6),
            "byte_identical": n_ok,
            "final_occupied": summary["per_bit"][-1]["memo_occupied_after"],
            "per_bit": summary["per_bit"],
            "snapshots": snaps,
        }
        record["band_wide_runs"] = band_runs
        save()

    expect("band18_bit0_nodes", band_runs[18]["per_bit"][0]["nodes_this_run"],
           EXPECTED["band18_bit0_nodes"])
    expect("band18_bit95_memo_invariance",
           [p for p in band_runs[18]["per_bit"] if p["bit"] == 95][0]["nodes_this_run"],
           EXPECTED["band18_bit95_nodes"])

    # ---- fresh per-bit attribution battery (ms23): sharing decomposition ----
    make_variant(23)
    fresh23 = []
    for b in EXPECTED["bits"]:
        summary, certdir = run_driver(make_driver(23), plan_path,
                                      "fresh_ms23_bit%d" % b, bits=b)
        n_ok, _ = verify_snapshots(summary, certdir, manifest)
        got = summary["total_nodes_single_process_with_band_memo"]
        expect("fresh23_bit%d_nodes" % b, got, EXPECTED["fresh23_per_bit"][b])
        expect("fresh23_bit%d_byte_identical" % b, n_ok, 1)
        expect("fresh23_bit%d_fbt_drops" % b, summary["fbt_drops"], 0)
        fresh23.append({"bit": b, "fresh_ms23_nodes": got,
                        "byte_identical": n_ok == 1})
    fresh23_total = sum(f["fresh_ms23_nodes"] for f in fresh23)
    expect("fresh23_total", fresh23_total, EXPECTED["fresh23_total"])

    band23 = band_runs[23]
    per_bit_sharing = []
    for f in fresh23:
        b23 = [p for p in band23["per_bit"] if p["bit"] == f["bit"]][0]
        pub_nodes = [c for c in manifest["certificates"]
                     if c["bit"] == f["bit"]][0]["extraction_nodes"]
        per_bit_sharing.append({
            "bit": f["bit"],
            "published_ms18_fresh_nodes": pub_nodes,
            "fresh_ms23_nodes": f["fresh_ms23_nodes"],
            "band_ms23_nodes": b23["nodes_this_run"],
            "capacity_gain_fresh23_vs_published":
                round(f["fresh_ms23_nodes"] / pub_nodes, 6),
            "sharing_penalty_band23_vs_fresh23":
                round(b23["nodes_this_run"] / f["fresh_ms23_nodes"], 6),
        })
    record["attribution"] = {
        "fresh_per_bit_ms23": {
            "total_nodes": fresh23_total,
            "vs_published": round(fresh23_total / pub_total, 6),
            "byte_identical_22_of_22":
                all(f["byte_identical"] for f in fresh23),
            "per_bit": fresh23,
        },
        "sharing_decomposition_same_capacity_ms23": {
            "band_wide_total": band23["total_nodes"],
            "fresh_total": fresh23_total,
            "band_wide_penalty_vs_fresh":
                round(band23["total_nodes"] / fresh23_total, 6),
            "note": ("band-wide sharing at MS=1<<23 (final load factor 0.8516) "
                     "is HARMFUL: +11.69% vs fresh per-bit at the same "
                     "capacity.  Per-bit penalties grow with bit position "
                     "(open-addressing cluster pollution); only bits 39/41 "
                     "profit (0.9651/0.9466); bit 95 is memo-state-invariant "
                     "(1.0000 in every configuration)"),
            "per_bit": per_bit_sharing,
        },
    }
    save()

    # ---- sensitivity: bit 117 (largest root) fresh at every capacity ----
    sens = []
    for ms in (18, 20, 21, 22, 23, 24):
        make_variant(ms)
        try:
            summary, certdir = run_driver(
                make_driver(ms), plan_path, "bit117_ms%d" % ms, bits=117,
                max_old=("400" if ms >= 24 else None))
            n_ok, _ = verify_snapshots(summary, certdir, manifest)
            got = summary["total_nodes_single_process_with_band_memo"]
            entry = {"ms_shift": ms, "memo_slots": 1 << ms, "nodes": got,
                     "byte_identical": n_ok == 1}
            if ms == 18:
                expect("sensitivity_bit117_ms18", got,
                       EXPECTED["sensitivity_bit117_ms18"])
                expect("sensitivity_bit117_rows",
                       summary["per_bit"][0]["rows"],
                       EXPECTED["bit117_published_rows"])
        except subprocess.CalledProcessError as e:
            entry = {"ms_shift": ms, "memo_slots": 1 << ms,
                     "status": "run-failed", "detail": str(e)[:200]}
        sens.append(entry)
    record["sensitivity_bit117_fresh"] = sens
    save()

    # ---- best-effort extras: fresh ms24 battery and band-wide ms24 ----
    make_variant(24)
    fresh24 = []
    for b in EXPECTED["bits"]:
        try:
            summary, certdir = run_driver(
                make_driver(24), plan_path, "fresh_ms24_bit%d" % b, bits=b,
                max_old="400")
            n_ok, _ = verify_snapshots(summary, certdir, manifest)
            fresh24.append({"bit": b,
                            "fresh_ms24_nodes":
                                summary["total_nodes_single_process_with_band_memo"],
                            "byte_identical": n_ok == 1})
        except subprocess.CalledProcessError as e:
            fresh24.append({"bit": b, "status": "run-failed",
                            "detail": str(e)[:200]})
            break
    record["attribution"]["fresh_per_bit_ms24"] = {
        "status": ("complete" if len(fresh24) == 22 and
                   all("fresh_ms24_nodes" in f for f in fresh24)
                   else "partial"),
        "per_bit": fresh24,
    }
    if all("fresh_ms24_nodes" in f for f in fresh24) and len(fresh24) == 22:
        record["attribution"]["fresh_per_bit_ms24"]["total_nodes"] = \
            sum(f["fresh_ms24_nodes"] for f in fresh24)
        record["attribution"]["fresh_per_bit_ms24"]["vs_published"] = round(
            sum(f["fresh_ms24_nodes"] for f in fresh24) / pub_total, 6)
    save()

    try:
        summary, certdir = run_driver(
            make_driver(24), plan_path, "band_memo_ms24", max_old="400")
        n_ok, snaps = verify_snapshots(summary, certdir, manifest)
        record["band_wide_runs"][24] = {
            "memo_slots": 1 << 24,
            "total_nodes": summary["total_nodes_single_process_with_band_memo"],
            "vs_published": round(
                summary["total_nodes_single_process_with_band_memo"] / pub_total, 6),
            "byte_identical": n_ok,
            "final_occupied": summary["per_bit"][-1]["memo_occupied_after"],
            "per_bit": summary["per_bit"],
            "snapshots": snaps,
        }
    except subprocess.CalledProcessError as e:
        record["band_wide_runs"][24] = {
            "memo_slots": 1 << 24,
            "status": "run-failed",
            "detail": str(e)[:200],
            "note": ("best-effort attempt recorded as an experiment fact "
                     "(memory ceiling ~1 GB on the measurement host)"),
        }
    save()

    # ---- gates summary ----
    record["gates"] = {
        "failures": failures,
        "all_expected_values_reproduced": not failures,
    }
    record["interpretation_guard"] = {
        "new_verdicts": "none",
        "manifest_rows_opened_or_closed": "none",
        "certificate_bytes": "unchanged (22/22 byte-identical in every completed configuration)",
        "win7_d10_scope": ("WIN7-D10 proves a first-player win within depth 10 "
                           "from the individual 7-stone roots only; "
                           "REFUTED-D10 is not a LOSS proof"),
        "unknown_status": {
            "11x11_empty_board": "UNKNOWN",
            "two_stone_roots": {"49,60": "UNKNOWN", "59,60": "UNKNOWN"},
            "s2_59_60": "UNKNOWN",
            "class1": "UNKNOWN", "class2": "UNKNOWN", "class4": "UNKNOWN",
        },
    }
    save()

    print("FAILURES: %d" % len(failures))
    for f in failures:
        print("  " + json.dumps(f))
    print("band18 %d band22 %d band23 %d fresh23 %d (baseline %d)" %
          (band_runs[18]["total_nodes"], band_runs[22]["total_nodes"],
           band_runs[23]["total_nodes"], fresh23_total, pub_total))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
