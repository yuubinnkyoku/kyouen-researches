#!/usr/bin/env python3
"""Independent bytes-level re-verification of the 82 certificate records in the
warm-multiband / multiband2 / cost-70c warm6 / warm-batch3 / warm-band-hygiene
record files, against their published certificate bytes in the band
certificate directories, with the BigInt 3x3-cofactor verifier.

Run from the repo root of yuubinnkyoku/kyouen-researches at main:
    python3 research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/reverify_warm_multiband_band_certificates_bigint_20261117.py

Steps (all asserted):
 1. load the five published record files (warm-multiband 35 records,
    warm-multiband2 31, cost-70c warm6 6, cost-70c warm-batch3 4,
    warm-band-hygiene 6 -> 82 records);
 2. resolve each record's storage (single file or .part1of2/.part2of2
    line-boundary split); for six records whose record storage says
    "single file" but whose repo layout holds a part1of2/part2of2 split
    (class2-lane-cost63a bits 96/97, cost64b bits 53/116, cost61d
    bits 114/116) the parts are used and the layout drift is reported;
 3. assert per-part bytes/md5 where the record documents them, then
    assemble and assert full-certificate bytes == record bytes and
    md5 == record md5 (82/82);
 4. run the BigInt independent verifier
    (scripts/verify_win7_certificate_bigint_independent.mjs, no engine,
    no floating point) once per distinct certificate (81 distinct files;
    the hygiene cost-61d bit-22 record shares the cost-71b bit-1 file);
 5. assert per record: verdict, 7 stones, root_safe, rows sorted-unique,
    union_missing 0, union_extra 0, terminal range within 13..17,
    root_hex == record root_hex, strategy rows == record rows,
    subroots_passed == record sub_roots_pass;
 6. write the deterministic re-verification JSON to the output path.

Determinism: no timestamps, no wall times, fixed record order; running
twice must produce byte-identical output.
11x11 empty board remains UNKNOWN; WIN7 certificates prove only
individual 7-stone roots within depth 10.
"""
import concurrent.futures, hashlib, json, os, subprocess

EXP = "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113"
OUTD = f"{EXP}/output"
VERIFIER = f"{EXP}/scripts/verify_win7_certificate_bigint_independent.mjs"
OUT = f"{OUTD}/class2-lane-warm-multiband-band-certificates-bigint-independent-reverification-20261117.json"
NODE = "node"

RECORD_FILES = [
    ("warm-multiband", f"{OUTD}/class2-lane-warm-multiband-certificates-20261115.json"),
    ("warm-multiband2", f"{OUTD}/class2-lane-warm-multiband2-certificates-20261115.json"),
    ("cost70c-warm6", f"{OUTD}/class2-lane-cost70c-warm6-bigint-independent-verification-20261115.json"),
    ("cost70c-warm-batch3", f"{OUTD}/class2-lane-cost70c-warm-batch3-records-20261115.json"),
    ("warm-band-hygiene", f"{OUTD}/class2-lane-warm-band-hygiene-certificates-20261115.json"),
]
EXPECTED = {
    "records": 82,
    "total_rows": 3490727,
    "total_sub_roots": 4343,
    "record_bytes_sum": 126089080,
    "distinct_certificate_files": 81,
}
TOTAL_ROW_KEYS = ("rows",)
LAYOUT_DRIFT = {
    ("class2-lane-cost63a", 96), ("class2-lane-cost63a", 97),
    ("class2-lane-cost64b", 53), ("class2-lane-cost64b", 116),
    ("class2-lane-cost61d", 114), ("class2-lane-cost61d", 116),
}


def norm(p):
    return p if p.startswith("research/") else f"{OUTD}/{p}"


def resolve_storage(r):
    st = r.get("storage") or {}
    if "part1" in st:
        return "part1of2+part2of2", [(norm(st["part1"]["path"]), st["part1"].get("bytes"), st["part1"].get("md5")),
                                     (norm(st["part2"]["path"]), st["part2"].get("bytes"), st["part2"].get("md5"))]
    f = r.get("file") or st.get("file") or st.get("path")
    assert f, (r.get("band"), r.get("bit"), "no storage reference")
    if isinstance(f, list):
        f = f[0]
    f = str(f)
    if "part1of2" in f and "+ .part2of2" in f:
        base = norm(f.split(" + ")[0])
        return "part1of2+part2of2", [(base, None, None), (base.replace("part1of2", "part2of2"), None, None)]
    base = norm(f)
    if os.path.exists(base):
        return "single", [(base, None, None)]
    p1, p2 = base + ".part1of2", base + ".part2of2"
    assert os.path.exists(p1) and os.path.exists(p2), (r.get("band"), r.get("bit"), base)
    return "single-declared-parts-found", [(p1, None, None), (p2, None, None)]


def read(p):
    with open(p, "rb") as fh:
        return fh.read()


def md5(b):
    return hashlib.md5(b).hexdigest()


def run_verifier(path):
    p = subprocess.run([NODE, VERIFIER, path], capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def main():
    entries = []
    ver_by_file = {}
    total_rows = 0
    total_sub = 0
    bytes_sum = 0
    for src_name, path in RECORD_FILES:
        d = json.load(open(path))
        for r in d["records"]:
            layout, parts = resolve_storage(r)
            part_reports = []
            blob = b""
            for (pp, pbytes, pmd5) in parts:
                raw = read(pp)
                if pbytes is not None:
                    assert len(raw) == pbytes, (r["band"], r["bit"], pp, len(raw), pbytes)
                if pmd5 is not None:
                    assert md5(raw) == pmd5, (r["band"], r["bit"], pp)
                part_reports.append({"path": pp, "bytes": len(raw), "md5": md5(raw),
                                     "record_part_bytes_match": pbytes is None or len(raw) == pbytes,
                                     "record_part_md5_match": pmd5 is None or md5(raw) == pmd5})
                blob += raw
            assert len(blob) == r["bytes"], (r["band"], r["bit"], len(blob), r["bytes"])
            assert md5(blob) == r["md5"], (r["band"], r["bit"], "full md5 mismatch")
            key = tuple(p[0] for p in parts)
            if key not in ver_by_file:
                tmp = f"/tmp/warm_reverify_{len(ver_by_file)}.cert"
                with open(tmp, "wb") as fh:
                    fh.write(blob)
                rc, out, err = run_verifier(tmp)
                assert rc == 0, (r["band"], r["bit"], err[:300])
                ver_by_file[key] = (json.loads(out), tmp)
                os.unlink(tmp)
            v, tmp = ver_by_file[key]
            assert v["verdict"] == "WIN7 certificate independently verified"
            assert v["root_stones"] == 7 and v["root_safe"] is True
            assert v["rows_sorted_unique"] is True
            assert v["union_missing"] == 0 and v["union_extra"] == 0
            assert 13 <= v["terminal_range"][0] and v["terminal_range"][1] <= 17
            assert v["root_hex"] == r["root_hex"], (r["band"], r["bit"], v["root_hex"], r["root_hex"])
            assert v["strategy_rows"] == r["rows"], (r["band"], r["bit"], "rows")
            assert v["subroots_passed"] == r["sub_roots_pass"], (r["band"], r["bit"], "subroots")
            entries.append({
                "source_record_file": path.split("/")[-1],
                "record_source": src_name,
                "band": r["band"],
                "bit": r["bit"],
                "root_hex": r["root_hex"],
                "resolved_layout": layout,
                "layout_drift_single_declared_parts_found": (r["band"], r["bit"]) in LAYOUT_DRIFT,
                "bytes": r["bytes"],
                "md5_full_certificate": r["md5"],
                "parts": part_reports,
                "shared_file_with_other_record": None,
                "verifier_status": "PASS",
                "verifier_rows": v["strategy_rows"],
                "verifier_subroots_passed": v["subroots_passed"],
                "verifier_root_mobility": v["root_mobility"],
                "verifier_terminal_range": v["terminal_range"],
                "verifier_union_missing": v["union_missing"],
                "verifier_union_extra": v["union_extra"],
                "record_rows": r["rows"],
                "record_sub_roots_pass": r["sub_roots_pass"],
                "rows_match": True,
                "sub_roots_match": True,
            })
            total_rows += v["strategy_rows"]
            total_sub += v["subroots_passed"]
            bytes_sum += r["bytes"]

    # duplicate-file annotation (hygiene cost-61d bit 22 shares the cost-71b bit-1 file)
    by_key = {}
    for e in entries:
        by_key.setdefault(tuple(p["path"] for p in e["parts"]), []).append(e)
    for key, group in by_key.items():
        if len(group) > 1:
            for e in group:
                e["shared_file_with_other_record"] = sorted(
                    f"{g['band']} bit {g['bit']}" for g in group if g is not e)

    assert len(entries) == EXPECTED["records"]
    assert total_rows == EXPECTED["total_rows"]
    assert total_sub == EXPECTED["total_sub_roots"]
    assert bytes_sum == EXPECTED["record_bytes_sum"]
    assert len(by_key) == EXPECTED["distinct_certificate_files"]
    assert all(e["verifier_status"] == "PASS" and e["rows_match"] and e["sub_roots_match"]
               for e in entries)
    drift = [e for e in entries if e["layout_drift_single_declared_parts_found"]]
    assert len(drift) == 6

    from collections import Counter
    per_source = Counter(e["record_source"] for e in entries)
    doc = {
        "schema": "n11-class2-lane-warm-multiband-band-certificates-bigint-independent-reverification-20261117-v1",
        "date": "2026-11-17",
        "method": ("all 82 certificate records of the warm-multiband (35), warm-multiband2 (31), "
                   "cost-70c warm6 (6), cost-70c warm-batch3 (4) and warm-band-hygiene (6) record "
                   "files resolved to their published certificate bytes (single files or "
                   ".part1of2/.part2of2 line-boundary splits in the band certificate directories), "
                   "byte-checked against the per-record bytes/md5 (and per-part bytes/md5 where "
                   "documented), then independently verified with the published BigInt 3x3-cofactor "
                   "verifier (verify_win7_certificate_bigint_independent.mjs, no engine, no "
                   "floating point) with per-record row / sub_roots_pass / root_hex / union / "
                   "terminal-range equality asserted"),
        "summary": {
            "records": 82,
            "distinct_certificate_files": 81,
            "verifier_pass": 82,
            "verifier_fail": 0,
            "record_mismatch": 0,
            "records_with_layout_drift": 6,
            "total_rows_independently_verified": total_rows,
            "total_sub_roots_independently_verified": total_sub,
            "total_certificate_bytes_rehashed": bytes_sum,
            "records_per_source": dict(per_source),
        },
        "layout_drift_note": ("six records declare 'single file' storage while the repo holds a "
                              "part1of2/part2of2 split (cost63a bits 96/97, cost64b bits 53/116, "
                              "cost61d bits 114/116); the concatenated parts match the record "
                              "bytes and full-certificate md5 exactly, so the drift is "
                              "presentational, not substantive"),
        "duplicate_file_note": ("the warm-band-hygiene cost-61d bit-22 record and cost-71b bit-1 "
                                "record reference the same certificate file (same root "
                                "00000000000000803202000000400002); the verifier ran once for it"),
        "entries": entries,
        "interpretation_guard": ("bookkeeping over published certificates; solved counts measure "
                                 "manifest coverage, not the game-theoretic value of any position; "
                                 "WIN7 certificates prove only individual 7-stone roots within depth 10"),
        "unknown_status": "11x11 empty board: UNKNOWN",
    }
    with open(OUT, "w") as f:
        json.dump(doc, f, indent=1)
        f.write("\n")
    print(f"wrote {OUT}: pass=82/82 mismatch=0 rows={total_rows} sub_roots={total_sub} "
          f"distinct_files=81 layout_drift=6")


if __name__ == "__main__":
    main()
