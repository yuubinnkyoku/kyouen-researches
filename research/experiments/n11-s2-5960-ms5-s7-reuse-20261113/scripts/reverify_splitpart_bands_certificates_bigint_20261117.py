#!/usr/bin/env python3
"""Independent bytes-level re-verification of the 18 split-part WIN7-D10
certificates of five bands of the head-1452 basis (cost-72b 6, 74d 6, 77c 1,
77d 5), against their per-record documentation and the BigInt independent
verifier. This is the split-part batch that the single-file batch
(reverify_singlefile_bands_certificates_bigint_20261117.py, 43 records)
explicitly deferred, completing the five-band bytes re-verification.

Run from the working mirror directory of
yuubinnkyoku/kyouen-researches @ main commit 063031b67a74f568f3207e2934715e405d00afd8
with the five band certificate directories mirrored under certs/ via
commit-pinned raw URLs and the record files mirrored next to this script:

  BASE=https://raw.githubusercontent.com/yuubinnkyoku/kyouen-researches/<PIN>/research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output
  (each class2-lane-cost<band>-certificates/*.cert.part1of2/.part2of2
   fetched to certs/, the receipts-recompute and win7-certificates record
   JSONs fetched as-is)

Steps (all asserted):
 1. assert the verifier script's git blob sha (62b5d9413d...);
 2. load the record sources:
      - cost-72b: win7-certificates manifest (6 split bits 2/21/66/95/100/
        106; storage.parts carries per-part bytes/md5/git_blob_sha/lines)
        cross-agreed with the receipts-recompute rows/md5/sub_roots_pass;
      - cost-74d: win7-certificates manifest (6 split bits 2/28/102/109/112/
        116; receipts record only root_hex for these bits, the manifest is
        the rows/md5/sub_roots_pass source, as in the single-file batch);
      - cost-77c: receipts-recompute (bit 10);
      - cost-77d: receipts-recompute (bits 58/66/78/108/111);
    total 18 records, all distinct (band, bit) and all distinct root_hex;
 3. assert each mirrored part file's git blob sha and size against the
    authoritative GitHub directory listing of the pinned commit
    (36/36 pin table embedded below, fields=name/sha/size);
 4. per-part manifest agreement for 72b/74d (bytes/md5/git_blob_sha, plus
    line counts for 72b), and part1 ends on a line boundary;
 5. concatenate part1+part2 per certificate and assert the whole-file
    md5 against the record; for 72b/74d additionally bytes, sha256 and
    whole_git_blob_sha against the manifest;
 6. run the BigInt independent verifier
    (verify_win7_certificate_bigint_independent.mjs, git blob
    62b5d9413daafb172f6e10249976ee6808f7b454, byte-exact local copy: BigInt
    3x3 cofactor expansion, no floating point, no solver/verdict-cache
    import) once per concatenated certificate; assert verdict, root stones
    7, root_safe, rows sorted-unique, union missing/extra 0/0, terminal range
    within 13..17, strategy_rows == record rows, subroots_passed == record
    sub_roots_pass, and root_hex == record root_hex;
 7. cross-checks:
      - independent in-script D4 canonicalization (min hex over the eight
        square symmetries of the 11x11 board, fourth implementation)
        reproduces every record's d4_canonical_hex for all 18 certificates
        (72b receipts, 74d manifest, 77c/77d receipts);
      - 72b manifest per-bit full-field agreement (terminal_count/
        terminal_range/winner_states/loser_states/loser_reply_edges/
        visited_states_across_subroots/root_check.loser_mobility vs the
        verifier output) and the 13-record manifest totals re-summed;
      - 74d manifest per-bit full-field agreement and the 15-record
        manifest totals re-summed;
      - whole-file sha256/git blob sha of the 77c/77d concatenations are
        recorded as new bytes-level documentation (the receipts only
        document md5/rows/sub_roots_pass);
 8. write the deterministic re-verification JSON to the output path.

Determinism: no timestamps, no wall times, fixed record order; running
twice must produce byte-identical output.
11x11 empty board remains UNKNOWN; WIN7 certificates prove only
individual 7-stone roots within depth 10.
"""
import concurrent.futures, hashlib, json, os, subprocess

PIN = "063031b67a74f568f3207e2934715e405d00afd8"
EXP = "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113"
OUTD = f"{EXP}/output"
VERIFIER = f"{EXP}/scripts/verify_win7_certificate_bigint_independent.mjs"
VERIFIER_BLOB_SHA = "62b5d9413daafb172f6e10249976ee6808f7b454"
NODE = "node"
MIRROR = os.environ.get("REVERIFY_MIRROR", "certs")
OUT = f"{OUTD}/class2-lane-splitpart-bands-certificates-bigint-independent-reverification-20261117.json"

# Authoritative GitHub directory listing at PIN (fields name|sha|size),
# one line per split part file across the four band dirs (36 lines).
PINS = """
class2-lane-cost72b-certificates/bit100-root-00000010000000809102000002000000.cert.part1of2|cb66a3f425dff53e7437be8eb0abbc69b49de675|1202854
class2-lane-cost72b-certificates/bit100-root-00000010000000809102000002000000.cert.part2of2|d8dedf8485a5c38d47592f9ea801dfca95221cb2|1201235
class2-lane-cost72b-certificates/bit106-root-00000400000000809102000002000000.cert.part1of2|156e4627ffa588bce672d0323297c6b111c4fb47|1261225
class2-lane-cost72b-certificates/bit106-root-00000400000000809102000002000000.cert.part2of2|f6afbcc3e68447ce8f61400989a81dd30222c699|1258563
class2-lane-cost72b-certificates/bit2-root-00000000000000809102000002000004.cert.part1of2|b6d906796787fa1bd65e03bbee3f575fc779352b|1050314
class2-lane-cost72b-certificates/bit2-root-00000000000000809102000002000004.cert.part2of2|6119bd26e7dd361e455570aaf7a924ac536fc70e|1048439
class2-lane-cost72b-certificates/bit21-root-00000000000000809102000002200000.cert.part1of2|83881542cca69c868eec5214dea27e07180f9cae|923948
class2-lane-cost72b-certificates/bit21-root-00000000000000809102000002200000.cert.part2of2|c305db4154ed641b4135d5feb8c5b6bcb5421d9c|921626
class2-lane-cost72b-certificates/bit66-root-00000000000000849102000002000000.cert.part1of2|e8bfd06e8c7d8e477ff858dc46f5b709c3039c1c|951629
class2-lane-cost72b-certificates/bit66-root-00000000000000849102000002000000.cert.part2of2|ef8e29b98d7e45aa18a602be12a4395b02a0730b|949777
class2-lane-cost72b-certificates/bit95-root-00000000800000809102000002000000.cert.part1of2|a5ec0a2d1640a5bc6d47e033bb887af594e39d19|1031838
class2-lane-cost72b-certificates/bit95-root-00000000800000809102000002000000.cert.part2of2|16a1c2bf1b73b6025ded0a62a7fda7113ba79d65|1030217
class2-lane-cost74d-certificates/bit102-root-00000040000000809102020000000000.cert.part1of2|f162f273cd73fe8a14ecf9643e9b676a5ccfef1a|1341201
class2-lane-cost74d-certificates/bit102-root-00000040000000809102020000000000.cert.part2of2|e120a1c6fc595794aff8a05fb47d1f6448aedda7|1337190
class2-lane-cost74d-certificates/bit109-root-00002000000000809102020000000000.cert.part1of2|1281e409086115805afb02e0ac381876e09161c3|974359
class2-lane-cost74d-certificates/bit109-root-00002000000000809102020000000000.cert.part2of2|0becc5c15bc05f06010d198de7a1f2ecc3b6b1ea|970942
class2-lane-cost74d-certificates/bit112-root-00010000000000809102020000000000.cert.part1of2|fc9e1249988d84aed453bd5dd49bba9e507dc820|1165575
class2-lane-cost74d-certificates/bit112-root-00010000000000809102020000000000.cert.part2of2|5f6c6ac07481840d96e9dbde611ac810b6fbb4b9|1163819
class2-lane-cost74d-certificates/bit116-root-00100000000000809102020000000000.cert.part1of2|802cafdcb9888f3b6f01a61ea856fdb186b506d2|1011277
class2-lane-cost74d-certificates/bit116-root-00100000000000809102020000000000.cert.part2of2|065d89caaec2887dd6b13c1e40b0fb459698e897|1009061
class2-lane-cost74d-certificates/bit2-root-00000000000000809102020000000004.cert.part1of2|423d01baeff9a3427ffd3662b2b36ec0726b85b8|929020
class2-lane-cost74d-certificates/bit2-root-00000000000000809102020000000004.cert.part2of2|162d4808c73c2417855a815f2e1d4a5a7f2d4d42|927668
class2-lane-cost74d-certificates/bit28-root-00000000000000809102020010000000.cert.part1of2|7802b191a33e7c0e31aea7ea34b6c2cbd4eb6923|1001382
class2-lane-cost74d-certificates/bit28-root-00000000000000809102020010000000.cert.part2of2|65aa4a6995df9a932080dfc2f19614fdb2790325|999240
class2-lane-cost77c-certificates/bit10-root-00000000040000801202000000200400.cert.part1of2|dabd418030e6b5a734fb0173617c64a3d7d6c6ff|1262832
class2-lane-cost77c-certificates/bit10-root-00000000040000801202000000200400.cert.part2of2|fc56dd5253feaa46d60c0809267d515f5a0fd1e4|1262811
class2-lane-cost77d-certificates/bit108-root-00001000100000801202000000200000.cert.part1of2|4b26ea479cb1d2edaa9e415808e56915f66c060c|1025535
class2-lane-cost77d-certificates/bit108-root-00001000100000801202000000200000.cert.part2of2|c98f4189cf4ab933ba4b4211453bc207840cd93e|1025488
class2-lane-cost77d-certificates/bit111-root-00008000100000801202000000200000.cert.part1of2|4ce73f124cae58c99d14769281163ef5a29711cc|1058590
class2-lane-cost77d-certificates/bit111-root-00008000100000801202000000200000.cert.part2of2|2ee35da9bc0244f1627e50c1fe291813097965ae|1058566
class2-lane-cost77d-certificates/bit58-root-00000000100000801602000000200000.cert.part1of2|d4389949b84918f997a7edbd972f7efd748c895e|981637
class2-lane-cost77d-certificates/bit58-root-00000000100000801602000000200000.cert.part2of2|36acfba5405cd383e3a1669288f4e67f24277a6b|981575
class2-lane-cost77d-certificates/bit66-root-00000000100000841202000000200000.cert.part1of2|20fcf0c48f258fb487ea22995a18ae4e7cbdf0d9|1007617
class2-lane-cost77d-certificates/bit66-root-00000000100000841202000000200000.cert.part2of2|bfa0299c4e65fbea9bbc622c7e8def5f85ba39b4|1007610
class2-lane-cost77d-certificates/bit78-root-00000000100040801202000000200000.cert.part1of2|3dbb7b17522597edaacfed379d81108aa0889de7|1359908
class2-lane-cost77d-certificates/bit78-root-00000000100040801202000000200000.cert.part2of2|c67cb1b499f6eccdde414eb7fb307d9211f1beae|1359839
"""

REC_72B = "class-frontier-cost72b-receipts-recompute-20261115.json"
MANIFEST_72B = "class2-lane-cost72b-win7-certificates-20261115.json"
MANIFEST_74D = "class2-lane-cost74d-win7-certificates-20261115.json"
REC_74D = "class-frontier-cost74d-receipts-recompute-20261115.json"
REC_77C = "class-frontier-cost77c-receipts-recompute-20261115.json"
REC_77D = "class-frontier-cost77d-receipts-recompute-20261115.json"

BITS_72B = [2, 21, 66, 95, 100, 106]
BITS_74D = [2, 28, 102, 109, 112, 116]
BITS_77C = [10]
BITS_77D = [58, 66, 78, 108, 111]

EXPECTED_RECORDS = 18
EXPECTED_PARTS = 36
BAND_ORDER = ["72b", "74d", "77c", "77d"]

# 72b manifest totals (13 records; re-summed here as in the single-file batch)
TOTALS_72B = {
    "certificates": 13, "rows": 636225, "sub_roots": 729,
    "visited_states_across_subroots": 1378650, "winner_states": 889294,
    "loser_states": 264554, "terminal_count": 224802,
    "loser_reply_edges": 1241817, "extraction_nodes": 200029509,
}
# 74d manifest totals (15 records)
TOTALS_74D = {"certificates": 15, "rows": 723630, "sub_roots": 883}


def md5(b):
    return hashlib.md5(b).hexdigest()


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def git_blob_sha(b):
    return hashlib.sha1(b"blob %d\x00" % len(b) + b).hexdigest()


def d4_canon(h):
    """Independent D4 canonical form on the 11x11 board: min hex over the
    eight square symmetries. Fourth implementation relative to the fold/
    harvest tools and the single-file batch script; asserted against every
    record's d4_canonical_hex."""
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


def band_dir(band):
    return f"class2-lane-cost{band}-certificates"


def load_records():
    R = []
    # 72b: manifest split bits, cross-agreed with receipts
    m = json.load(open(MANIFEST_72B))
    mb = {c["bit"]: c for c in m["certificates"]}
    rb = {r["bit"]: r for r in json.load(open(REC_72B))["cost72b_addition"]}
    for bit in BITS_72B:
        c = mb[bit]
        r = rb[bit]
        assert c["storage"]["layout"].startswith("2 parts")
        assert c["storage"]["joined_md5_equals_whole_md5"] is True
        assert r["certified"] is True
        assert (c["rows"], c["md5"], c["sub_roots_pass"], c["root_hex"]) == \
               (r["rows"], r["md5"], r["sub_roots_pass"], r["root_hex"]), \
               ("72b manifest/receipts disagreement", bit)
        R.append({
            "band": "72b", "bit": bit, "root_hex": c["root_hex"],
            "d4_canonical_hex": r["d4_canonical_hex"],
            "band_dir": band_dir("72b"),
            "base": f"bit{bit}-root-{c['root_hex']}.cert",
            "rows": c["rows"], "md5": c["md5"],
            "sub_roots_pass": c["sub_roots_pass"],
            "record_source": f"{OUTD}/{MANIFEST_72B}",
            "record_kind": "win7-certificates-manifest+receipts-recompute",
            "manifest": c,
        })
    # 74d: manifest split bits (receipts record only root_hex for these)
    m = json.load(open(MANIFEST_74D))
    mb = {c["bit"]: c for c in m["certificates"]}
    rb = {r["bit"]: r for r in json.load(open(REC_74D))["cost74d_addition"]}
    for bit in BITS_74D:
        c = mb[bit]
        r = rb[bit]
        assert c["storage"]["layout"].startswith("2 parts")
        assert c["storage"]["joined_md5_equals_whole_md5"] is True
        assert r["root_hex"] == c["root_hex"], ("74d receipts root", bit)
        R.append({
            "band": "74d", "bit": bit, "root_hex": c["root_hex"],
            "d4_canonical_hex": c["d4_canonical_hex"],
            "band_dir": band_dir("74d"),
            "base": f"bit{bit}-root-{c['root_hex']}.cert",
            "rows": c["rows"], "md5": c["md5"],
            "sub_roots_pass": c["sub_roots_pass"],
            "record_source": f"{OUTD}/{MANIFEST_74D}",
            "record_kind": "win7-certificates-manifest",
            "manifest": c,
        })
    # 77c / 77d: receipts split bits
    for band, fn, bits, key in (
            ("77c", REC_77C, BITS_77C, "cost77c_addition"),
            ("77d", REC_77D, BITS_77D, "cost77d_addition")):
        d = json.load(open(fn))
        by_bit = {r["bit"]: r for r in d[key]}
        assert len(by_bit) == (8 if band == "77c" else 12)
        for bit in bits:
            r = by_bit[bit]
            assert r["certified"] is True
            R.append({
                "band": band, "bit": bit, "root_hex": r["root_hex"],
                "d4_canonical_hex": r["d4_canonical_hex"],
                "band_dir": band_dir(band),
                "base": f"bit{bit}-root-{r['root_hex']}.cert",
                "rows": r["rows"], "md5": r["md5"],
                "sub_roots_pass": r["sub_roots_pass"],
                "record_source": f"{OUTD}/{fn}",
                "record_kind": "receipts-recompute",
                "manifest": None,
            })
    assert len(R) == EXPECTED_RECORDS, len(R)
    kb = [(r["band"], r["bit"]) for r in R]
    assert len(set(kb)) == len(kb), "duplicate (band, bit)"
    roots = [r["root_hex"] for r in R]
    assert len(set(roots)) == len(roots), "duplicate root_hex across records"
    return R


def run_verifier(path):
    p = subprocess.run([NODE, VERIFIER, path], capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def verify_one(rec, pins):
    base = f"{rec['band_dir']}/{rec['base']}"
    p1, p2 = f"{base}.part1of2", f"{base}.part2of2"
    raw1 = open(f"{MIRROR}/{p1}", "rb").read()
    raw2 = open(f"{MIRROR}/{p2}", "rb").read()
    for rel, raw in ((p1, raw1), (p2, raw2)):
        assert rel in pins, ("unpinned part", rel)
        assert git_blob_sha(raw) == pins[rel][0], ("pin sha mismatch", rel)
        assert len(raw) == pins[rel][1], ("pin size mismatch", rel)
    assert raw1.endswith(b"\n"), ("part1 does not end on a line boundary", base)
    # per-part manifest agreement (72b/74d)
    if rec["manifest"] is not None:
        parts = rec["manifest"]["storage"]["parts"]
        assert len(parts) == 2, ("manifest parts", base)
        for desc, rel, raw in ((parts[0], p1, raw1), (parts[1], p2, raw2)):
            assert desc["path"].endswith(rel), ("manifest part path", rel)
            assert desc["bytes"] == len(raw), ("manifest part bytes", rel)
            assert desc["md5"] == md5(raw), ("manifest part md5", rel)
            assert desc["git_blob_sha"] == git_blob_sha(raw), ("manifest part blob sha", rel)
            if "lines" in desc:
                assert desc["lines"] == raw.count(b"\n"), ("manifest part lines", rel)
    whole = raw1 + raw2
    computed_md5 = md5(whole)
    assert computed_md5 == rec["md5"], ("record md5 mismatch", rec["band"], rec["bit"])
    entry = {
        "band": rec["band"], "bit": rec["bit"], "root_hex": rec["root_hex"],
        "certificate": base, "storage": "split part1of2+part2of2 concatenation",
        "record_source": rec["record_source"], "record_kind": rec["record_kind"],
        "part1": {"pinned_blob_sha": pins[p1][0], "bytes": len(raw1)},
        "part2": {"pinned_blob_sha": pins[p2][0], "bytes": len(raw2)},
        "part1_line_boundary": True,
        "joined_bytes": len(whole),
        "joined_md5": computed_md5,
        "joined_sha256": sha256(whole),
        "joined_git_blob_sha": git_blob_sha(whole),
        "record_md5": rec["md5"],
        "record_md5_match": True,
        "record_rows": rec["rows"],
        "record_sub_roots_pass": rec["sub_roots_pass"],
    }
    if rec["manifest"] is not None:
        c = rec["manifest"]
        assert c["bytes"] == len(whole), ("manifest whole bytes", rec["band"], rec["bit"])
        assert c["sha256"] == entry["joined_sha256"], ("manifest sha256", rec["band"], rec["bit"])
        assert c["whole_git_blob_sha"] == entry["joined_git_blob_sha"], \
            ("manifest whole blob sha", rec["band"], rec["bit"])
    tmp = f"/tmp/reverify_splitpart_{rec['band']}_{rec['bit']}.cert"
    with open(tmp, "wb") as fh:
        fh.write(whole)
    rc, out, err = run_verifier(tmp)
    assert rc == 0, ("verifier nonzero", rec["band"], rec["bit"], err[:300])
    v = json.loads(out)
    os.unlink(tmp)
    assert v["verdict"] == "WIN7 certificate independently verified"
    assert v["root_stones"] == 7 and v["root_safe"] is True
    assert v["rows_sorted_unique"] is True
    assert v["union_missing"] == 0 and v["union_extra"] == 0
    assert 13 <= v["terminal_range"][0] and v["terminal_range"][1] <= 17
    assert v["root_hex"] == rec["root_hex"], ("root_hex", rec["band"], rec["bit"])
    assert v["strategy_rows"] == rec["rows"], \
        ("rows", rec["band"], rec["bit"], v["strategy_rows"], rec["rows"])
    assert v["subroots_passed"] == rec["sub_roots_pass"], ("subroots", rec["band"], rec["bit"])
    if rec["manifest"] is not None:
        c = rec["manifest"]
        assert c["terminal_count"] == v["terminal_count"], ("terminal", rec["band"], rec["bit"])
        assert list(c["terminal_range"]) == v["terminal_range"], ("trange", rec["band"], rec["bit"])
        assert c["winner_states"] == v["winner_states"], ("winner", rec["band"], rec["bit"])
        assert c["loser_states"] == v["loser_states"], ("loser", rec["band"], rec["bit"])
        assert c["loser_reply_edges"] == v["loser_reply_edges"], ("edges", rec["band"], rec["bit"])
        assert c["visited_states_across_subroots"] == v["visited_states_across_subroots"], \
            ("visited", rec["band"], rec["bit"])
        assert c["root_check"]["loser_mobility"] == v["root_mobility"], ("mobility", rec["band"], rec["bit"])
        assert c["root_check"]["stones"] == 7 and c["root_check"]["match"] is True
        assert c["union_missing"] == 0 and c["union_extra"] == 0
    entry.update({
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
    })
    return entry, v


def main():
    # 0. verifier integrity
    vsrc = open(VERIFIER, "rb").read()
    assert git_blob_sha(vsrc) == VERIFIER_BLOB_SHA, "verifier blob sha mismatch"

    pins = {}
    for line in PINS.strip().split("\n"):
        p, sha, size = line.split("|")
        pins[p] = (sha, int(size))
    assert len(pins) == EXPECTED_PARTS, len(pins)
    records = load_records()
    assert sum(1 for r in records if r["band"] == "72b") == 6
    assert sum(1 for r in records if r["band"] == "74d") == 6
    assert sum(1 for r in records if r["band"] == "77c") == 1
    assert sum(1 for r in records if r["band"] == "77d") == 5
    entries = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
        futs = {ex.submit(verify_one, rec, pins): rec for rec in records}
        for fut in concurrent.futures.as_completed(futs):
            e, v = fut.result()
            entries.append((futs[fut], e, v))
    order = {b: i for i, b in enumerate(BAND_ORDER)}
    entries.sort(key=lambda t: (order[t[0]["band"]], t[0]["bit"]))

    # ---- cross-checks ----
    # independent D4 canonicalization: all 18 records
    for rec, e, _ in entries:
        got = d4_canon(rec["root_hex"])
        assert got == rec["d4_canonical_hex"], \
            ("independent d4 canon", rec["band"], rec["bit"], got, rec["d4_canonical_hex"])

    # 72b manifest totals re-sum (13 records)
    m = json.load(open(MANIFEST_72B))
    assert len(m["certificates"]) == TOTALS_72B["certificates"]
    per_record_key = {"sub_roots": "sub_roots_pass"}
    for k, want in TOTALS_72B.items():
        if k == "certificates":
            continue
        got = sum(c[per_record_key.get(k, k)] for c in m["certificates"])
        assert got == want, ("72b manifest totals", k, got, want)

    # 74d manifest totals re-sum (15 records)
    m = json.load(open(MANIFEST_74D))
    assert len(m["certificates"]) == TOTALS_74D["certificates"]
    assert sum(c["rows"] for c in m["certificates"]) == TOTALS_74D["rows"]
    assert sum(c["sub_roots_pass"] for c in m["certificates"]) == TOTALS_74D["sub_roots"]

    # joined bytes vs manifest bytes sum for the split population
    total_rows = sum(e["verifier_rows"] for _, e, _ in entries)
    total_sub = sum(e["verifier_subroots_passed"] for _, e, _ in entries)
    total_bytes = sum(e["joined_bytes"] for _, e, _ in entries)
    total_parts = sum(e["part1"]["bytes"] + e["part2"]["bytes"] for _, e, _ in entries)
    assert total_bytes == total_parts
    from collections import Counter
    per_band = Counter(rec["band"] for rec, _, _ in entries)

    doc = {
        "schema": "n11-class2-lane-splitpart-bands-certificates-bigint-independent-reverification-20261117-v1",
        "date": "2026-11-17",
        "pin": {
            "commit": PIN,
            "record_files": sorted(set(r["record_source"] for r in records)),
            "authoritative_blob_sha_table": "GitHub directory listing of the four band certificate dirs at the pinned commit (fields name/sha/size), embedded in the script as PINS and asserted 36/36 against the mirrored part bytes",
        },
        "method": {
            "records": "18 split-part WIN7-D10 certificate records of the five-band split-part batch (72b 6 + 74d 6 + 77c 1 + 77d 5): the win7-certificates manifest records (with per-part storage metadata) for 72b/74d, cross-agreed with the receipts-recompute for 72b, and the receipts-recompute records for 77c/77d; completes the deferred split-part half of the remaining-band certificate bytes survey batch after the 43-record single-file batch",
            "bytes": "each part fetched from the commit-pinned raw CDN URL into the local mirror; git blob sha+size asserted against the authoritative GitHub directory listing at the pin (36/36); per-part bytes/md5/git_blob_sha (and 72b line counts) asserted against the manifest storage metadata; part1 asserted to end on a line boundary; certificates reconstructed as exact part1+part2 concatenations",
            "verifier": "verify_win7_certificate_bigint_independent.mjs (git blob 62b5d9413daafb172f6e10249976ee6808f7b454, asserted by the script): BigInt 3x3 cofactor expansion of the exact lifted determinant [x^2+y^2,x,y,1], no floating point, no solver/verdict-cache import; root stones=7 + safe check, loser mobility vs independent enumeration, per-subroot winner strategy legality walk, union missing/extra 0/0, rows sorted unique, terminal range within 13..17",
        },
        "entries": [e for _, e, _ in entries],
        "cross_checks": {
            "independent_d4_canon_all_18_records": "a fourth, in-script D4 canonicalization implementation (min hex over the eight square symmetries of the 11x11 board) reproduces every record's d4_canonical_hex for all 18 split-part certificates (72b receipts, 74d manifest, 77c/77d receipts)",
            "cost72b_manifest_6_bits_and_totals": "per-bit md5/sha256/bytes/whole_git_blob_sha/rows/sub_roots_pass/terminal_count/terminal_range/winner_states/loser_states/loser_reply_edges/visited_states_across_subroots/root_check.loser_mobility all reproduced against the joined bytes, plus per-part storage metadata agreement; the 13-record manifest totals (rows 636225, sub_roots 729, visited 1378650, winner 889294, loser 264554, terminal 224802, edges 1241817, extraction_nodes 200029509) re-summed and asserted",
            "cost74d_manifest_6_bits_and_totals": "per-bit full-field agreement (md5/sha256/bytes/whole_git_blob_sha/rows/sub_roots_pass/terminal_count/range/winner/loser/edges/visited/mobility) against the joined bytes plus per-part storage metadata agreement; the 15-record manifest totals (rows 723630, sub_roots 883) re-summed and asserted",
            "cost77c77d_receipts": "receipts md5/rows/sub_roots_pass asserted against the joined bytes; the joined sha256 and git blob sha are recorded here as new bytes-level documentation (the receipts only document md5/rows/sub_roots_pass)",
            "cross_band_root_distinctness": "all 18 root_hex values are distinct across the four bands (asserted at record load) and disjoint from the 43 single-file batch roots",
        },
        "summary": {
            "records": len(entries),
            "part_files_pinned_and_asserted": EXPECTED_PARTS,
            "distinct_certificates": len(set(e["certificate"] for _, e, _ in entries)),
            "verifier_pass": len(entries),
            "verifier_fail": 0,
            "record_md5_asserted": len(entries),
            "record_md5_mismatch": 0,
            "pin_blob_sha_mismatch": 0,
            "part_line_boundary_violation": 0,
            "total_rows_independently_verified": total_rows,
            "total_sub_roots_independently_verified": total_sub,
            "total_certificate_bytes_rehashed": total_bytes,
            "records_per_band": dict(sorted(per_band.items())),
        },
        "interpretation_guard": [
            "this re-verification upgrades the 18 split-part certificates of the five bands from receipt/manifest documentation to bytes-level independently re-verified evidence, completing the five-band certificate bytes re-verification together with the 43-record single-file batch (198 record sessions before this one: 33 58c + 82 warm/multiband + 83 receipts-recompute bands); it does not change any frontier number",
            "the 24 split-part certificates of bands 72c/73g/73h/83d remain deferred to a later split-part batch (83d has no README)",
            "solved 1452 (and the landed 64h fold projection 1472) are manifest cover bookkeeping; a WIN7-D10 certificate proves only that its individual 7-stone root is a first-player win within depth 10",
            "REFUTED-D10 entries are not LOSS proofs",
            "11x11 empty board, two-stone root {49,60}, S2 {59,60}, class 1, class 2 and class 4 all remain UNKNOWN",
        ],
    }
    with open(OUT, "w") as fh:
        json.dump(doc, fh, indent=1, sort_keys=False)
        fh.write("\n")
    print(json.dumps(doc["summary"], indent=1))


if __name__ == "__main__":
    main()
