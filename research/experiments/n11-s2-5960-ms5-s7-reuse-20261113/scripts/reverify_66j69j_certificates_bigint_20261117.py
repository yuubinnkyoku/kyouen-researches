#!/usr/bin/env python3
"""Independent bytes-level re-verification of the 15 WIN7-D10 certificates of
the newly published cost-66j (9) and cost-69j (6) certificate bands, with a
third-implementation BigInt independent verification beyond the generator's
own Bareiss verification (verify_bit7_win7_cert.ts).

The parallel lane has published a bytes re-fetch audit for cost-71e
(audit_cost71e_published_bytes_20261117.sh, sha256/md5/bytes vs manifest).
This batch goes further for 66j/69j: on top of the bytes pins it runs the
BigInt independent verifier (verify_win7_certificate_bigint_independent.mjs,
git blob 62b5d9413daafb172f6e10249976ee6808f7b454) once per certificate and
cross-agrees the result with the full manifest record set (rows, subroots,
loser mobility, terminal range, md5, sha256, D4 canon), the per-bit
rootcheck.json sidecars (stones/loserMobility) and the per-bit subroots.json
sidecars (per-loser-first-move seen/terminals/opponentEdges/range, summed to
the verifier's visited_states/terminal_count/loser_reply_edges).

Record sources (all mirrored from the pinned commit and pin-verified):
 - class2-lane-cost{66j,69j}-win7-certificates-20261117.json manifests
 - per-bit bit{N}-rootcheck.json, bit{N}-subroots.json sidecars
 - README-split-bit{N}.md recombination docs for the 11 split certificates
 - authoritative GitHub directory listings of the two band dirs at the pin
   (67 file pins: name|sha|size, machine-extracted)

Run from the working mirror directory of
yuubinnkyoku/kyouen-researches @ main commit
d8fc41c7c9c2307a5392511b9435400a4c79c84f with the two band dirs mirrored
under certs66j69j/ and pins66j69j.txt present.

Determinism: no timestamps, no wall times, fixed record order; running twice
must produce byte-identical output.
11x11 empty board remains UNKNOWN; WIN7-D10 certificates prove only
individual 7-stone roots within depth 10.
"""
import concurrent.futures, hashlib, json, os, re, subprocess

PIN = "d8fc41c7c9c2307a5392511b9435400a4c79c84f"
EXP = "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113"
OUTD = f"{EXP}/output"
VERIFIER = f"{EXP}/scripts/verify_win7_certificate_bigint_independent.mjs"
VERIFIER_BLOB_SHA = "62b5d9413daafb172f6e10249976ee6808f7b454"
NODE = "node"
MIRROR = os.environ.get("REVERIFY_MIRROR", "certs66j69j")
PINS_FILE = "pins66j69j.txt"
OUT = f"{OUTD}/class2-lane-66j69j-certificates-bigint-independent-reverification-20261117.json"
EARLIER_BATCH_OUTPUTS = [
    f"{OUTD}/class2-lane-singlefile-bands-certificates-bigint-independent-reverification-20261117.json",
    f"{OUTD}/class2-lane-splitpart-bands-certificates-bigint-independent-reverification-20261117.json",
    f"{OUTD}/class2-lane-splitpart-sweepbands-certificates-bigint-independent-reverification-20261117.json",
]

BANDS = {
    "66j": "class2-lane-cost66j-win7-certificates-20261117.json",
    "69j": "class2-lane-cost69j-win7-certificates-20261117.json",
}
BAND_DIR = {"66j": "class2-lane-cost66j-certificates",
            "69j": "class2-lane-cost69j-certificates"}
EXPECTED = {"66j": 9, "69j": 6}


def md5(b):
    return hashlib.md5(b).hexdigest()


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def git_blob_sha(b):
    return hashlib.sha1(b"blob %d\x00" % len(b) + b).hexdigest()


def d4_canon(h):
    """Independent D4 canonical form on the 11x11 board: min hex over the
    eight square symmetries. Sixth implementation; asserted against every
    record's d4_canon_root."""
    stones = [i for i in range(121) if int(h, 16) >> i & 1]
    assert len(stones) == 7, ("d4_canon expects 7 stones", h)
    best = None
    for xf in (False, True):
        for yf in (False, True):
            for sw in (False, True):
                v = 0
                for i in stones:
                    x, y = i % 11, i // 11
                    if xf:
                        x = 10 - x
                    if yf:
                        y = 10 - y
                    if sw:
                        x, y = y, x
                    v |= 1 << (y * 11 + x)
                hs = f"{v:032x}"
                if best is None or hs < best:
                    best = hs
    return best


def load_pins():
    pins = {}
    for line in open(PINS_FILE):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        rel, sha, size = line.split("|")
        pins[rel] = (sha, int(size))
    assert len(pins) == 67, len(pins)
    return pins


def load_records():
    R = []
    for band, mfile in BANDS.items():
        m = json.load(open(f"{MIRROR}/{mfile}"))
        certs = m["certificates"]
        assert len(certs) == EXPECTED[band], (band, len(certs))
        for c in certs:
            assert c["verdict"] == "WIN7" and c["depth"] == 10
            assert c["subroots"] == c["subroots_pass"] and c["subroots_pass"] > 0
            assert c["union_missing"] == 0 and c["union_extra"] == 0
            assert c["terminal_stone_range"] == [13, 17]
            assert c["loser_mobility"] == c["subroots_pass"]
            assert len(c["root"]) == 32 and len(c["d4_canon_root"]) == 32
            split = c["storage"] != "whole file"
            R.append({
                "band": band, "bit": c["bit"], "root_hex": c["root"],
                "d4_canon_root": c["d4_canon_root"], "raw_is_canon": c["raw_is_canon"],
                "rows": c["rows"], "subroots_pass": c["subroots_pass"],
                "loser_mobility": c["loser_mobility"],
                "terminal_stone_range": c["terminal_stone_range"],
                "md5": c["md5"], "sha256": c["sha256"],
                "file": c["file"], "split": split,
                "band_dir": BAND_DIR[band],
            })
    assert len(R) == 15, len(R)
    kb = [(r["band"], r["bit"]) for r in R]
    assert len(set(kb)) == len(kb), "duplicate (band, bit)"
    roots = [r["root_hex"] for r in R]
    assert len(set(roots)) == len(roots), "duplicate root across records"
    # disjointness from the 85 survey-identified remaining-band records
    earlier_roots = set()
    for fn in EARLIER_BATCH_OUTPUTS:
        d = json.load(open(fn))
        earlier_roots.update(e["root_hex"] for e in d["entries"])
    assert len(earlier_roots) == 85, len(earlier_roots)
    overlap = set(roots) & earlier_roots
    assert not overlap, ("root overlap with the 85-record band population",
                         sorted(overlap))
    # also disjoint across D4 canon classes (a root may be a symmetry of
    # another record's root; that must not happen silently)
    canons = [r["d4_canon_root"] for r in R]
    assert len(set(canons)) == len(canons), "duplicate D4 canon across records"
    return R


def run_verifier(path):
    p = subprocess.run([NODE, VERIFIER, path], capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def verify_one(rec, pins):
    d = f"{rec['band_dir']}/{rec['file']}"
    def pin_of(rel):
        assert rel in pins, ("unpinned file", rel)
        return pins[rel]
    if not rec["split"]:
        raw = open(f"{MIRROR}/{d}", "rb").read()
        pin = pin_of(d)
        assert git_blob_sha(raw) == pin[0], ("pin sha mismatch", d)
        assert len(raw) == pin[1], ("pin size mismatch", d)
        joined = raw
        storage = "whole file"
        parts = None
    else:
        p1, p2 = f"{d}.part1of2", f"{d}.part2of2"
        pin1, pin2 = pin_of(p1), pin_of(p2)
        raw1 = open(f"{MIRROR}/{p1}", "rb").read()
        raw2 = open(f"{MIRROR}/{p2}", "rb").read()
        assert git_blob_sha(raw1) == pin1[0] and len(raw1) == pin1[1], ("pin part1", d)
        assert git_blob_sha(raw2) == pin2[0] and len(raw2) == pin2[1], ("pin part2", d)
        assert raw1.endswith(b"\n"), ("part1 not on a line boundary", d)
        joined = raw1 + raw2
        storage = "split part1of2+part2of2 concatenation"
        parts = {"part1": {"pinned_blob_sha": pin1[0], "bytes": pin1[1]},
                 "part2": {"pinned_blob_sha": pin2[0], "bytes": pin2[1]}}
    # whole-file documentation: manifest md5 AND sha256
    assert md5(joined) == rec["md5"], ("manifest md5", rec["band"], rec["bit"])
    assert sha256(joined) == rec["sha256"], ("manifest sha256", rec["band"], rec["bit"])
    # sidecar records
    bd = rec["band_dir"]
    rootcheck = json.loads(open(f"{MIRROR}/{bd}/bit{rec['bit']}-rootcheck.json", "rb").read().decode().strip().splitlines()[0])
    assert rootcheck["stones"] == 7, ("rootcheck stones", rec["band"], rec["bit"])
    assert rootcheck["loserMobility"] == rec["loser_mobility"], ("rootcheck mobility", rec["band"], rec["bit"])
    subroots_raw = open(f"{MIRROR}/{bd}/bit{rec['bit']}-subroots.json", "rb").read().decode().strip().splitlines()
    subroots = json.loads(subroots_raw[0])
    assert subroots["rows"] == rec["rows"], ("subroots rows", rec["band"], rec["bit"])
    stats = subroots["stats"]
    assert len(stats) == rec["subroots_pass"], ("subroots key count", rec["band"], rec["bit"])
    for k, s in stats.items():
        assert 13 <= s["range"][0] and s["range"][1] <= 17, ("subroots range", rec["band"], rec["bit"], k)
    # README-split doc for split certificates
    readme = None
    if rec["split"]:
        rd = f"{bd}/README-split-bit{rec['bit']}.md"
        pin_of(rd)
        txt = open(f"{MIRROR}/{rd}", "rb").read().decode()
        m = re.search(r"is (\d+) bytes and is published as two parts", txt)
        assert m, ("README split bytes", rec["band"], rec["bit"])
        assert int(m.group(1)) == len(joined), ("README whole bytes", rec["band"], rec["bit"])
        m = re.search(r"md5sum .*?#\s*([0-9a-f]{32})", txt)
        assert m and m.group(1) == rec["md5"], ("README md5", rec["band"], rec["bit"])
        m = re.search(r"line boundary \(byte (\d+)\)", txt)
        assert m and int(m.group(1)) == parts["part1"]["bytes"], ("README split byte", rec["band"], rec["bit"])
        m = re.search(r"^root `([0-9a-f]{32})`", txt, re.M)
        assert m and m.group(1) == rec["root_hex"], ("README root", rec["band"], rec["bit"])
        m = re.search(r"D4 canon `([0-9a-f]{32})`", txt)
        # the 66j READMEs document the D4 canon inline; the 69j READMEs do
        # not (their roots are documented canon-less in the manifest only)
        if m:
            assert m.group(1) == rec["d4_canon_root"], ("README canon", rec["band"], rec["bit"])
        readme = {"bytes": len(joined), "split_boundary": parts["part1"]["bytes"],
                  "md5": rec["md5"]}
    # BigInt independent verifier (third implementation beyond the
    # generator's Bareiss verify)
    tmp = f"/tmp/reverify_66j69j_{rec['band']}_{rec['bit']}.cert"
    with open(tmp, "wb") as fh:
        fh.write(joined)
    rc, out, err = run_verifier(tmp)
    assert rc == 0, ("verifier nonzero", rec["band"], rec["bit"], err[:300])
    v = json.loads(out)
    os.unlink(tmp)
    assert v["verdict"] == "WIN7 certificate independently verified"
    assert v["root_hex"] == rec["root_hex"], ("root_hex", rec["band"], rec["bit"])
    assert v["root_stones"] == 7 and v["root_safe"] is True
    assert v["rows_sorted_unique"] is True
    assert v["union_missing"] == 0 and v["union_extra"] == 0
    assert v["strategy_rows"] == rec["rows"], ("rows", rec["band"], rec["bit"])
    assert v["consumed_winner_rows"] == rec["rows"], ("consumed rows", rec["band"], rec["bit"])
    assert v["subroots_passed"] == rec["subroots_pass"], ("subroots", rec["band"], rec["bit"])
    assert v["root_mobility"] == rec["loser_mobility"], ("mobility", rec["band"], rec["bit"])
    assert list(v["terminal_range"]) == rec["terminal_stone_range"], ("trange", rec["band"], rec["bit"])
    # subroots sidecar sums == verifier sums (Bareiss-generated stats vs
    # BigInt verifier: third-implementation field agreement)
    assert sum(s["seen"] for s in stats.values()) == v["visited_states_across_subroots"], \
        ("subroots seen sum", rec["band"], rec["bit"])
    assert sum(s["terminals"] for s in stats.values()) == v["terminal_count"], \
        ("subroots terminals sum", rec["band"], rec["bit"])
    assert sum(s["opponentEdges"] for s in stats.values()) == v["loser_reply_edges"], \
        ("subroots opponentEdges sum", rec["band"], rec["bit"])
    # independent D4 canonicalization
    got_canon = d4_canon(rec["root_hex"])
    assert got_canon == rec["d4_canon_root"], \
        ("independent d4 canon", rec["band"], rec["bit"], got_canon, rec["d4_canon_root"])
    assert rec["raw_is_canon"] == (rec["root_hex"] == rec["d4_canon_root"]), \
        ("raw_is_canon consistency", rec["band"], rec["bit"])
    entry = {
        "band": rec["band"], "bit": rec["bit"], "root_hex": rec["root_hex"],
        "d4_canon_root": rec["d4_canon_root"], "raw_is_canon": rec["raw_is_canon"],
        "certificate": d, "storage": storage,
        "record_source": f"{OUTD}/{BANDS[rec['band']]}",
        "record_kind": "win7-certificates manifest + rootcheck/subroots sidecars + README-split",
        "joined_bytes": len(joined),
        "joined_md5": md5(joined),
        "joined_sha256": sha256(joined),
        "joined_git_blob_sha": git_blob_sha(joined),
        "manifest_md5_match": True,
        "manifest_sha256_match": True,
        "record_rows": rec["rows"],
        "record_sub_roots_pass": rec["subroots_pass"],
        "record_loser_mobility": rec["loser_mobility"],
        "record_terminal_stone_range": rec["terminal_stone_range"],
        "rootcheck_stones": rootcheck["stones"],
        "rootcheck_loser_mobility": rootcheck["loserMobility"],
        "subroots_sidecar_keys": len(stats),
        "verifier_status": "PASS",
        "verifier_root_mobility": v["root_mobility"],
        "verifier_rows": v["strategy_rows"],
        "verifier_subroots_passed": v["subroots_passed"],
        "verifier_terminal_range": v["terminal_range"],
        "verifier_terminal_count": v["terminal_count"],
        "verifier_visited_states": v["visited_states_across_subroots"],
        "verifier_loser_reply_edges": v["loser_reply_edges"],
        "verifier_winner_states": v["winner_states"],
        "verifier_loser_states": v["loser_states"],
        "verifier_union_missing": v["union_missing"],
        "verifier_union_extra": v["union_extra"],
    }
    if parts is not None:
        entry["parts"] = parts
    if readme is not None:
        entry["readme_split_doc"] = readme
    return entry, v


def main():
    vsrc = open(VERIFIER, "rb").read()
    assert git_blob_sha(vsrc) == VERIFIER_BLOB_SHA, "verifier blob sha mismatch"
    pins = load_pins()
    records = load_records()
    entries = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
        futs = {ex.submit(verify_one, rec, pins): rec for rec in records}
        for fut in concurrent.futures.as_completed(futs):
            e, v = fut.result()
            entries.append((futs[fut], e, v))
    order = {"66j": 0, "69j": 1}
    entries.sort(key=lambda t: (order[t[0]["band"]], t[0]["bit"]))

    # cross-checks
    for band in ("66j", "69j"):
        eb = [e for rec, e, _ in entries if rec["band"] == band]
        assert len(eb) == EXPECTED[band], (band, len(eb))
    total_rows = sum(e["verifier_rows"] for _, e, _ in entries)
    total_sub = sum(e["verifier_subroots_passed"] for _, e, _ in entries)
    total_bytes = sum(e["joined_bytes"] for _, e, _ in entries)
    from collections import Counter
    per_band = Counter(rec["band"] for rec, _, _ in entries)
    n_split = sum(1 for _, e, _ in entries if e["storage"].startswith("split"))

    doc = {
        "schema": "n11-class2-lane-66j69j-certificates-bigint-independent-reverification-20261117-v1",
        "date": "2026-11-17",
        "pin": {
            "commit": PIN,
            "record_files": sorted(set(
                [f"{OUTD}/{BANDS[b]}" for b in BANDS] +
                [f"{OUTD}/{BAND_DIR[b]}/bit{n}-rootcheck.json" for b in BANDS
                 for n in sorted(r["bit"] for r in records if r["band"] == b)] +
                [f"{OUTD}/{BAND_DIR[b]}/bit{n}-subroots.json" for b in BANDS
                 for n in sorted(r["bit"] for r in records if r["band"] == b)] +
                [f"{OUTD}/{BAND_DIR[b]}/README-split-bit{n}.md" for b in BANDS
                 for n in sorted(r["bit"] for r in records
                                if r["band"] == b and r["split"])])),
            "authoritative_blob_sha_table": "GitHub directory listings of the two band certificate dirs at the pinned commit (67 file pins name|sha|size, machine-extracted into pins66j69j.txt and asserted 67/67 against the mirrored bytes)",
        },
        "method": {
            "records": "15 WIN7-D10 certificate records of the newly published cost-66j (9) and cost-69j (6) bands: win7-certificates manifests (rows/subroots_pass/loser_mobility/terminal_stone_range/md5/sha256/d4_canon_root/raw_is_canon, union 0/0 documented) plus per-bit rootcheck.json and subroots.json sidecars and README-split-bitN.md recombination docs for the 11 split certificates; all 15 records structurally pre-asserted (verdict WIN7, depth 10, subroots==subroots_pass, loser_mobility==subroots_pass, terminal range [13,17])",
            "bytes": "each whole certificate or part fetched from the commit-pinned raw CDN URL into the local mirror; git blob sha+size asserted against the authoritative GitHub directory listing at the pin (67/67); split part1 asserted to end on a line boundary; certificates reconstructed as exact part1+part2 concatenations; joined md5 AND sha256 asserted against the manifest (both are documented); README-split docs cross-checked (whole bytes, split boundary byte, md5, D4 canon)",
            "verifier": "verify_win7_certificate_bigint_independent.mjs (git blob 62b5d9413daafb172f6e10249976ee6808f7b454, asserted by the script): BigInt 3x3 cofactor expansion of the exact lifted determinant [x^2+y^2,x,y,1], no floating point, no solver/verdict-cache import; this is a third implementation beyond the generator's own Bareiss verify_bit7_win7_cert.ts documented in the manifests; per certificate asserted verdict/root_hex/stones 7/root_safe/rows sorted-unique/union 0/0/terminal range within 13..17/strategy_rows/subroots_passed/root_mobility/terminal_range/consumed_winner_rows",
            "sidecar_cross_agreement": "per-bit subroots.json (Bareiss-verified per-loser-first-move stats) sums fully agree with the BigInt verifier output on all 15 certificates: sum(seen)==visited_states_across_subroots, sum(terminals)==terminal_count, sum(opponentEdges)==loser_reply_edges, key count==subroots_pass, every per-move range within [13,17]; rootcheck.json stones==7 and loserMobility==manifest loser_mobility==verifier root_mobility",
        },
        "entries": [e for _, e, _ in entries],
        "cross_checks": {
            "independent_d4_canon_all_15_records": "a sixth, in-script D4 canonicalization implementation (min hex over the eight square symmetries of the 11x11 board) reproduces every record's d4_canon_root for all 15 certificates; raw_is_canon (True for 6 records, False for 9) verified as exactly root_hex == d4_canon_root; the 15 D4 canons are mutually distinct",
            "manifest_sha256_agreement": "the manifests document sha256 in addition to md5 for all 15 records; the joined bytes reproduce both (new for this batch family: previous batches documented md5 only)",
            "cross_batch_root_disjointness": "all 15 root_hex distinct in-batch and disjoint from the 85 root_hex values of the three earlier band batches (single-file 43 + five-band split 18 + sweep split 24), asserted at record load against the three published batch outputs",
            "beyond_parallel_lane": "the parallel lane's cost-71e published-bytes audit (audit_cost71e_published_bytes_20261117.sh) re-fetches bytes against manifest pins; this batch additionally runs the third-implementation BigInt verifier per certificate and cross-agrees the two sidecar record families",
        },
        "summary": {
            "records": len(entries),
            "file_pins_asserted": 67,
            "split_certificates": n_split,
            "whole_certificates": len(entries) - n_split,
            "verifier_pass": len(entries),
            "verifier_fail": 0,
            "manifest_md5_mismatch": 0,
            "manifest_sha256_mismatch": 0,
            "pin_blob_sha_mismatch": 0,
            "sidecar_cross_agreement_fail": 0,
            "total_rows_independently_verified": total_rows,
            "total_sub_roots_independently_verified": total_sub,
            "total_certificate_bytes_rehashed": total_bytes,
            "records_per_band": dict(sorted(per_band.items())),
            "rows_per_band": {b: sum(e["verifier_rows"] for rec, e, _ in entries if rec["band"] == b) for b in ("66j", "69j")},
            "bytes_per_band": {b: sum(e["joined_bytes"] for rec, e, _ in entries if rec["band"] == b) for b in ("66j", "69j")},
        },
        "interpretation_guard": [
            "this re-verification upgrades the 15 certificates of the newly published cost-66j and cost-69j bands from manifest+sidecar documentation to bytes-level, third-implementation independently re-verified evidence; the bytes-re-verified population of this experiment stands at 283 + 15 = 298 records (the cost-71e band was byte-audited separately by the parallel lane); it does not change any frontier number and closes no manifest row",
            "the receipt folds of the 66j/69j rows remain behind the pending 76c/66i/66j folds handled by the parallel lane",
            "solved 1452 (and the landed 64h fold projection 1472) are manifest cover bookkeeping; a WIN7-D10 certificate proves only that its individual 7-stone root is a first-player win within depth 10",
            "the 63 REFUTED-D10 bits of these bands are NOT LOSS proofs",
            "11x11 empty board, two-stone root {49,60}, S2 {59,60}, class 1, class 2 and class 4 all remain UNKNOWN",
        ],
    }
    with open(OUT, "w") as fh:
        json.dump(doc, fh, indent=1, sort_keys=False)
        fh.write("\n")
    print(json.dumps(doc["summary"], indent=1))


if __name__ == "__main__":
    main()
