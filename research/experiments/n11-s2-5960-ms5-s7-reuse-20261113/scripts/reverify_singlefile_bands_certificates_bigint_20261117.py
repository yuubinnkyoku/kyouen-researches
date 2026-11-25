#!/usr/bin/env python3
"""Independent bytes-level re-verification of the 43 single-file WIN7-D10
certificates of five bands of the head-1452 basis (cost-63g, 72b, 74d, 77c,
77d), against their per-record documentation and the BigInt independent
verifier. Follow-up to the remaining-band certificate bytes survey
(class2-lane-remaining-band-certificate-bytes-survey-20261117.json), which
proposed exactly this batch (63g 14 + 74d 8 + 77c 7 + 77d 7 + 72b 7).

Run from the working mirror directory of
yuubinnkyoku/kyouen-researches @ main commit 063031b67a74f568f3207e2934715e405d00afd8
with the five band certificate directories mirrored under certs/ via
commit-pinned raw URLs and the record files mirrored next to this script:

  BASE=https://raw.githubusercontent.com/yuubinnkyoku/kyouen-researches/<PIN>/research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output
  (each class2-lane-cost<band>-certificates/*.cert fetched to certs/,
   the receipts-recompute and win7-certificates record JSONs fetched as-is)

Steps (all asserted):
 1. assert the verifier script's git blob sha (62b5d9413d...);
 2. load the record sources:
      - class-frontier-cost63g-receipts-recompute-20261115.json (14 records,
        rows/md5/sub_roots_pass) for band 63g (all 14 single-file bits);
      - class-frontier-cost72b-receipts-recompute-20261115.json (13 records)
        filtered to the 7 single-file bits 11/30/31/36/47/85/97;
      - class2-lane-cost74d-win7-certificates-20261115.json (15 records)
        filtered to the 8 single-file bits 12/66/68/69/80/92/100/118
        (bit 91 is a documented D4 duplicate of cost72b bit 85 and has no
        own bytes; the 6 remaining bits are split-part publications deferred
        to the split-part batch);
      - class-frontier-cost77c-receipts-recompute-20261115.json (8 records)
        filtered to the 7 single-file bits 40/50/54/58/95/96/111;
      - class-frontier-cost77d-receipts-recompute-20261115.json (12 records)
        filtered to the 7 single-file bits 7/12/39/62/64/94/96;
    total 43 records, all distinct (band, bit) and all distinct root_hex;
 3. assert each mirrored certificate file's git blob sha and size against
    the authoritative GitHub directory listing of the pinned commit
    (43/43 pin table embedded below, fields=name/sha/size);
 4. assert md5 against every record (43/43 document an md5);
 5. run the BigInt independent verifier
    (verify_win7_certificate_bigint_independent.mjs, git blob
    62b5d9413daafb172f6e10249976ee6808f7b454, byte-exact local copy: BigInt
    3x3 cofactor expansion, no floating point, no solver/verdict-cache
    import) once per certificate; assert verdict, root stones 7, root_safe,
    rows sorted-unique, union missing/extra 0/0, terminal range within
    13..17, strategy_rows == record rows, subroots_passed == record
    sub_roots_pass, and root_hex == record root_hex;
 6. cross-checks:
      - cost-63g win7 manifest (certificates keyed by bit): md5/sha256/
        bytes/whole_git_blob_sha/sub_roots_total/root_check.loser_mobility/
        terminal_range per bit; manifest totals rows 419398 / sub_roots
        667 / bytes 15142573 equal the verifier sums over the 14 bits;
      - cost-72b win7 manifest: per-bit md5/sha256/bytes/whole_git_blob_sha/
        rows/sub_roots_pass/terminal_count/terminal_range/winner_states/
        loser_states/loser_reply_edges/visited_states/root_check.loser_
        mobility for the 7 single-file bits; manifest totals (13 records:
        rows 636225 / sub_roots 729 / visited 1378650 / terminal 224802 /
        edges 1241817) re-summed from the manifest itself;
      - cost-74d win7 manifest: per-bit md5/sha256/bytes/whole_git_blob_sha/
        rows/sub_roots_pass/terminal_count/terminal_range/winner_states/
        loser_states/loser_reply_edges/visited_states/root_check.loser_
        mobility for the 8 single-file bits plus receipts-recompute
        opponent_legal_replies agreement; manifest totals (15 records:
        rows 723630 / sub_roots 883) re-summed from the manifest itself;
        bit 91 recorded as a documented D4 duplicate of 72b bit 85 (own
        md5 625163e5d5b02318623bd49a3b037a8e refers to the bit-91
        extraction, not to the 72b file bytes; not re-verified here);
      - cost-77c/77d receipts d4_canonical_hex agreement with the verifier
        root_hex and the pinned certificate file names;
 7. write the deterministic re-verification JSON to the output path.

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
OUT = f"{OUTD}/class2-lane-singlefile-bands-certificates-bigint-independent-reverification-20261117.json"

# Authoritative GitHub directory listing at PIN (fields name|sha|size),
# one line per single-file certificate across the five band dirs.
PINS = """class2-lane-cost63g-certificates/bit0-root-00000000080000801202000000200001.cert|158dd5d9d838786f86b4061534ce99308677836c|1711697
class2-lane-cost63g-certificates/bit105-root-00000200080000801202000000200000.cert|1cf08f2a488de0a6b0fa5a95aea1dc7679f709f9|775472
class2-lane-cost63g-certificates/bit113-root-00020000080000801202000000200000.cert|9c80b9c2781a79d71a0dd1604c99ef1204dcb007|2424207
class2-lane-cost63g-certificates/bit12-root-00000000080000801202000000201000.cert|c8a46fc8d28523a1b103b37dfbc885e5bcf786cc|931020
class2-lane-cost63g-certificates/bit50-root-00000000080000801206000000200000.cert|626b28d7f4b6e1025ad0c0c7d07dead4e84cde82|1191992
class2-lane-cost63g-certificates/bit54-root-00000000080000801242000000200000.cert|26d5ae74296e7f0af722890a663f711af1d4ef9d|982624
class2-lane-cost63g-certificates/bit58-root-00000000080000801602000000200000.cert|d2409f6535a964fbea438962f4b50f62d15d1713|868008
class2-lane-cost63g-certificates/bit62-root-00000000080000805202000000200000.cert|14fcb303e63b909bee3cf8035690b8564edbc22a|863816
class2-lane-cost63g-certificates/bit64-root-00000000080000811202000000200000.cert|cdc18ca665d9fe4a06a64a474df4e2eca1548375|537782
class2-lane-cost63g-certificates/bit72-root-00000000080001801202000000200000.cert|1a7cdef3398a9a95ff08a2680d37982eb9d39789|820991
class2-lane-cost63g-certificates/bit9-root-00000000080000801202000000200200.cert|7a050fce51def7852b44fa7c9da80eccb76c5128|1069295
class2-lane-cost63g-certificates/bit94-root-00000000480000801202000000200000.cert|a2d0b2944dc6cb83f2b5e2f799c4391772d7d4e9|1024583
class2-lane-cost63g-certificates/bit96-root-00000001080000801202000000200000.cert|a1299f9e1817d26d1ed742dcd91513e2210b99c3|664778
class2-lane-cost63g-certificates/bit99-root-00000008080000801202000000200000.cert|d8eec8de77265918647bf683055a1e2709154b08|1276308
class2-lane-cost72b-certificates/bit11-root-00000000000000809102000002000800.cert|c5e575784cac90712e2b3b9c3ed3d1a1c361c727|1221354
class2-lane-cost72b-certificates/bit30-root-00000000000000809102000042000000.cert|ec1859142e250aa88688eba9fd2269830f9150ec|1473717
class2-lane-cost72b-certificates/bit31-root-00000000000000809102000082000000.cert|9b545349f3c73f7474cf43af056bd348654d34c2|1600847
class2-lane-cost72b-certificates/bit36-root-00000000000000809102001002000000.cert|a30ced176f33399e3b6a7db6de0839dcf7d387d3|1495829
class2-lane-cost72b-certificates/bit47-root-00000000000000809102800002000000.cert|de3b00586d983e1146e82413c111dbea4347e6f8|1761391
class2-lane-cost72b-certificates/bit85-root-00000000002000809102000002000000.cert|c99ef87964f4770e7dab365ea42ad070b8c6495d|1456837
class2-lane-cost72b-certificates/bit97-root-00000002000000809102000002000000.cert|0a3ae82c02a7070c5715a468ea5af4ec63b3b176|1132979
class2-lane-cost74d-certificates/bit100-root-00000010000000809102020000000000.cert|ac9d0c5d834559043371b909969c36dcdb47a12f|1658930
class2-lane-cost74d-certificates/bit118-root-00400000000000809102020000000000.cert|b96de16ac906721d9f7cdf82fed45bb032d57c1a|1034744
class2-lane-cost74d-certificates/bit12-root-00000000000000809102020000001000.cert|a5df9d1184b9a70a33debae0d9dde79980935f77|1683615
class2-lane-cost74d-certificates/bit66-root-00000000000000849102020000000000.cert|50ef217aa1ffc2103942b3867ceea497d8b8a1bb|1561079
class2-lane-cost74d-certificates/bit68-root-00000000000000909102020000000000.cert|8c7c29082adb75e986a1fd1fed90da0c184a49bf|1539991
class2-lane-cost74d-certificates/bit69-root-00000000000000a09102020000000000.cert|3777ec97bd29091997829b9245040a8cbb1adea1|1394865
class2-lane-cost74d-certificates/bit80-root-00000000000100809102020000000000.cert|eae53fd78aba04d89ac1db264256f9b99ff92dd4|1532978
class2-lane-cost74d-certificates/bit92-root-00000000100000809102020000000000.cert|d55481e7fb55c3fdbe4df58f7d06ad277108779c|1449869
class2-lane-cost77c-certificates/bit111-root-00008000040000801202000000200000.cert|ceb75b312ed1d8d009bdd63e86f02802c3cdefc8|1769123
class2-lane-cost77c-certificates/bit40-root-00000000040000801202010000200000.cert|50d63ea5468288063bf380a33c9168ecf8dcd2b4|1233904
class2-lane-cost77c-certificates/bit50-root-00000000040000801206000000200000.cert|438595a2d94f72d5eac9d6b124d21123e2ce65a9|1178602
class2-lane-cost77c-certificates/bit54-root-00000000040000801242000000200000.cert|56d0a383ba5e6dfcc95c4d6a9704e2134d814211|1603365
class2-lane-cost77c-certificates/bit58-root-00000000040000801602000000200000.cert|395f088338678656586db0e6e3be480989cd9b55|1457491
class2-lane-cost77c-certificates/bit95-root-00000000840000801202000000200000.cert|456f7d9a48acd4e0f9dae62818e3aa69f0f42c47|1453158
class2-lane-cost77c-certificates/bit96-root-00000001040000801202000000200000.cert|342ed87309a50ddd0e548c8f04fa134b0e8a1ef0|1834104
class2-lane-cost77d-certificates/bit12-root-00000000100000801202000000201000.cert|65bdae86e6be6b09e7f4f436ee59f17a5f0b6e12|1753793
class2-lane-cost77d-certificates/bit39-root-00000000100000801202008000200000.cert|7b9eec0565496511b564b3d77f06468f42576622|1347439
class2-lane-cost77d-certificates/bit62-root-00000000100000805202000000200000.cert|b3bf61e98d27d70b660fb4cd62c1b7ce351723a0|1013765
class2-lane-cost77d-certificates/bit64-root-00000000100000811202000000200000.cert|64db9cb4276f5ea7dc89cce673aba8cfd3bf19e2|1220093
class2-lane-cost77d-certificates/bit7-root-00000000100000801202000000200080.cert|3fd9c162b666baa7790f622cb5966fa83737f2fd|1681877
class2-lane-cost77d-certificates/bit94-root-00000000500000801202000000200000.cert|3d72b87241db9d777f5fd2cf979ef7170a2a1116|1826619
class2-lane-cost77d-certificates/bit96-root-00000001100000801202000000200000.cert|efff08cd5f7df2eca25769414161686072227738|1282169"""

REC_63G = "class-frontier-cost63g-receipts-recompute-20261115.json"
MANIFEST_63G = "class2-lane-cost63g-win7-certificates-20261115.json"
REC_72B = "class-frontier-cost72b-receipts-recompute-20261115.json"
MANIFEST_72B = "class2-lane-cost72b-win7-certificates-20261115.json"
MANIFEST_74D = "class2-lane-cost74d-win7-certificates-20261115.json"
REC_74D = "class-frontier-cost74d-receipts-recompute-20261115.json"
REC_77C = "class-frontier-cost77c-receipts-recompute-20261115.json"
REC_77D = "class-frontier-cost77d-receipts-recompute-20261115.json"

BITS_72B_SINGLE = [11, 30, 31, 36, 47, 85, 97]
BITS_74D_SINGLE = [12, 66, 68, 69, 80, 92, 100, 118]
BITS_77C_SINGLE = [40, 50, 54, 58, 95, 96, 111]
BITS_77D_SINGLE = [7, 12, 39, 62, 64, 94, 96]

EXPECTED_RECORDS = 43
BAND_ORDER = ["63g", "72b", "74d", "77c", "77d"]

# 63g manifest totals (also asserted against the receipts totals)
TOTALS_63G_ROWS = 419398
TOTALS_63G_SUBROOTS = 667
TOTALS_63G_BYTES = 15142573
# 72b manifest totals (13 records incl. 6 split-part bits)
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
    eight square symmetries. Third implementation relative to the fold/
    harvest tools; asserted against every record's d4_canonical_hex."""
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
    # 63g: all 14 receipts records
    d = json.load(open(REC_63G))
    assert d["totals"]["receipts"] == 14
    for r in d["cost63g_addition"]:
        assert r["certified"] is True
        R.append({
            "band": "63g", "bit": r["bit"], "root_hex": r["root_hex"],
            "band_dir": band_dir("63g"),
            "file": f"bit{r['bit']}-root-{r['root_hex']}.cert",
            "rows": r["rows"], "md5": r["md5"],
            "sub_roots_pass": r["sub_roots_pass"],
            "record_source": f"{OUTD}/{REC_63G}",
            "record_kind": "receipts-recompute",
        })
    # 72b: receipts records filtered to single-file bits
    d = json.load(open(REC_72B))
    by_bit = {r["bit"]: r for r in d["cost72b_addition"]}
    assert sorted(by_bit) == [2, 11, 21, 30, 31, 36, 47, 66, 85, 95, 97, 100, 106]
    for bit in BITS_72B_SINGLE:
        r = by_bit[bit]
        assert r["certified"] is True
        R.append({
            "band": "72b", "bit": r["bit"], "root_hex": r["root_hex"],
            "band_dir": band_dir("72b"),
            "file": f"bit{r['bit']}-root-{r['root_hex']}.cert",
            "rows": r["rows"], "md5": r["md5"],
            "sub_roots_pass": r["sub_roots_pass"],
            "record_source": f"{OUTD}/{REC_72B}",
            "record_kind": "receipts-recompute",
        })
    # 74d: manifest records filtered to single-file bits
    d = json.load(open(MANIFEST_74D))
    mb = {c["bit"]: c for c in d["certificates"]}
    assert len(d["certificates"]) == 15
    for bit in BITS_74D_SINGLE:
        c = mb[bit]
        assert c["storage"]["layout"] == "single file"
        R.append({
            "band": "74d", "bit": c["bit"], "root_hex": c["root_hex"],
            "band_dir": band_dir("74d"),
            "file": c["storage"]["parts"][0]["path"].split("/")[-1],
            "rows": c["rows"], "md5": c["md5"],
            "sub_roots_pass": c["sub_roots_pass"],
            "record_source": f"{OUTD}/{MANIFEST_74D}",
            "record_kind": "win7-certificates-manifest",
        })
    # 77c / 77d: receipts records filtered to single-file bits
    for band, fn, bits in (("77c", REC_77C, BITS_77C_SINGLE), ("77d", REC_77D, BITS_77D_SINGLE)):
        d = json.load(open(fn))
        by_bit = {r["bit"]: r for r in d[f"cost{band}_addition"]}
        assert len(by_bit) == (8 if band == "77c" else 12)
        for bit in bits:
            r = by_bit[bit]
            assert r["certified"] is True
            R.append({
                "band": band, "bit": r["bit"], "root_hex": r["root_hex"],
                "band_dir": band_dir(band),
                "file": f"bit{r['bit']}-root-{r['root_hex']}.cert",
                "rows": r["rows"], "md5": r["md5"],
                "sub_roots_pass": r["sub_roots_pass"],
                "record_source": f"{OUTD}/{fn}",
                "record_kind": "receipts-recompute",
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
    rel = f"{rec['band_dir']}/{rec['file']}"
    assert rel in pins, ("unpinned file", rel)
    raw = open(f"{MIRROR}/{rel}", "rb").read()
    assert git_blob_sha(raw) == pins[rel][0], ("pin sha mismatch", rel)
    assert len(raw) == pins[rel][1], ("pin size mismatch", rel)
    computed_md5 = md5(raw)
    assert computed_md5 == rec["md5"], ("record md5 mismatch", rec["band"], rec["bit"])
    tmp = f"/tmp/reverify_singlefile_{rec['band']}_{rec['bit']}.cert"
    with open(tmp, "wb") as fh:
        fh.write(raw)
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
    assert v["strategy_rows"] == rec["rows"], ("rows", rec["band"], rec["bit"], v["strategy_rows"], rec["rows"])
    assert v["subroots_passed"] == rec["sub_roots_pass"], ("subroots", rec["band"], rec["bit"])
    return {
        "band": rec["band"], "bit": rec["bit"], "root_hex": rec["root_hex"],
        "file": rel, "storage": "single .cert file",
        "record_source": rec["record_source"], "record_kind": rec["record_kind"],
        "pinned_blob_sha": pins[rel][0], "bytes_published": len(raw),
        "certificate_bytes": len(raw),
        "computed_md5": computed_md5,
        "record_md5": rec["md5"],
        "record_md5_match": True,
        "record_rows": rec["rows"],
        "record_sub_roots_pass": rec["sub_roots_pass"],
        "verifier_status": "PASS",
        "verifier_root_mobility": v["root_mobility"],
        "verifier_rows": v["strategy_rows"],
        "verifier_subroots_passed": v["subroots_passed"],
        "verifier_terminal_range": v["terminal_range"],
        "verifier_terminal_count": v["terminal_count"],
        "verifier_visited_states": v["visited_states_across_subroots"],
        "verifier_loser_reply_edges": v["loser_reply_edges"],
        "verifier_union_missing": v["union_missing"],
        "verifier_union_extra": v["union_extra"],
    }, v


def main():
    # 0. verifier integrity
    vsrc = open(VERIFIER, "rb").read()
    assert git_blob_sha(vsrc) == VERIFIER_BLOB_SHA, "verifier blob sha mismatch"

    pins = {}
    for line in PINS.strip().split("\n"):
        p, sha, size = line.split("|")
        pins[p] = (sha, int(size))
    assert len(pins) == EXPECTED_RECORDS
    records = load_records()
    entries = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
        futs = {ex.submit(verify_one, rec, pins): rec for rec in records}
        for fut in futs:
            pass
        for fut, rec in futs.items():
            e, v = fut.result()
            entries.append((rec, e, v))
    order = {b: i for i, b in enumerate(BAND_ORDER)}
    entries.sort(key=lambda t: (order[t[0]["band"]], t[0]["bit"]))
    bykey = {(e["band"], e["bit"]): (e, v) for _, e, v in entries}

    # ---- cross-checks ----
    # 63g manifest
    m = json.load(open(MANIFEST_63G))
    e63 = [(e, v) for _, e, v in entries if e["band"] == "63g"]
    assert len(e63) == 14
    for e, v in e63:
        c = m["certificates"][str(e["bit"])]
        assert c["root_hex"] == e["root_hex"]
        assert c["md5"] == e["computed_md5"], ("63g manifest md5", e["bit"])
        assert c["bytes"] == e["certificate_bytes"], ("63g manifest bytes", e["bit"])
        assert c["whole_git_blob_sha"] == e["pinned_blob_sha"], ("63g manifest blob sha", e["bit"])
        assert c["rows"] == v["strategy_rows"], ("63g manifest rows", e["bit"])
        assert c["sub_roots_total"] == v["subroots_passed"], ("63g manifest subroots", e["bit"])
        assert c["root_check"]["loser_mobility"] == v["root_mobility"], ("63g manifest mobility", e["bit"])
        assert c["root_check"]["stones"] == 7 and c["root_check"]["match"] is True
        assert list(c["terminal_range"]) == v["terminal_range"], ("63g manifest trange", e["bit"])
        assert c["verdict"] == "WIN7"
        assert sha256(open(f"{MIRROR}/{e['file']}", "rb").read()) == c["sha256"], ("63g sha256", e["bit"])
    assert sum(e["verifier_rows"] for e, _ in e63) == TOTALS_63G_ROWS
    assert sum(e["verifier_subroots_passed"] for e, _ in e63) == TOTALS_63G_SUBROOTS
    assert sum(e["certificate_bytes"] for e, _ in e63) == TOTALS_63G_BYTES
    rec63 = json.load(open(REC_63G))
    assert rec63["totals"]["certificate_rows"] == TOTALS_63G_ROWS
    assert rec63["totals"]["certificate_sub_roots"] == TOTALS_63G_SUBROOTS
    assert rec63["totals"]["certificate_bytes"] == TOTALS_63G_BYTES

    # 72b manifest
    m = json.load(open(MANIFEST_72B))
    assert len(m["certificates"]) == TOTALS_72B["certificates"]
    per_record_key = {"sub_roots": "sub_roots_pass"}
    for k, want in TOTALS_72B.items():
        if k == "certificates":
            continue
        got = sum(c[per_record_key.get(k, k)] for c in m["certificates"])
        assert got == want, ("72b manifest totals", k, got, want)
    e72 = [(e, v) for _, e, v in entries if e["band"] == "72b"]
    assert len(e72) == 7
    for e, v in e72:
        c = [x for x in m["certificates"] if x["bit"] == e["bit"]][0]
        assert c["root_hex"] == e["root_hex"]
        assert c["md5"] == e["computed_md5"], ("72b manifest md5", e["bit"])
        assert c["sha256"] == sha256(open(f"{MIRROR}/{e['file']}", "rb").read()), ("72b sha256", e["bit"])
        assert c["bytes"] == e["certificate_bytes"], ("72b manifest bytes", e["bit"])
        assert c["whole_git_blob_sha"] == e["pinned_blob_sha"], ("72b manifest blob sha", e["bit"])
        assert c["rows"] == v["strategy_rows"], ("72b manifest rows", e["bit"])
        assert c["sub_roots_pass"] == v["subroots_passed"], ("72b manifest subroots", e["bit"])
        assert c["terminal_count"] == v["terminal_count"], ("72b terminal", e["bit"])
        assert list(c["terminal_range"]) == v["terminal_range"], ("72b trange", e["bit"])
        assert c["winner_states"] == v["winner_states"], ("72b winner", e["bit"])
        assert c["loser_states"] == v["loser_states"], ("72b loser", e["bit"])
        assert c["loser_reply_edges"] == v["loser_reply_edges"], ("72b edges", e["bit"])
        assert c["visited_states_across_subroots"] == v["visited_states_across_subroots"], ("72b visited", e["bit"])
        assert c["root_check"]["loser_mobility"] == v["root_mobility"], ("72b mobility", e["bit"])
        assert c["union_missing"] == 0 and c["union_extra"] == 0

    # 74d manifest + receipts
    m = json.load(open(MANIFEST_74D))
    assert len(m["certificates"]) == 15
    assert sum(c["rows"] for c in m["certificates"]) == TOTALS_74D["rows"]
    assert sum(c["sub_roots_pass"] for c in m["certificates"]) == TOTALS_74D["sub_roots"]
    e74 = [(e, v) for _, e, v in entries if e["band"] == "74d"]
    assert len(e74) == 8
    rec74 = {r["bit"]: r for r in json.load(open(REC_74D))["cost74d_addition"]}
    for e, v in e74:
        c = [x for x in m["certificates"] if x["bit"] == e["bit"]][0]
        assert c["root_hex"] == e["root_hex"]
        assert rec74[e["bit"]]["root_hex"] == e["root_hex"], ("74d receipts root", e["bit"])
        assert c["md5"] == e["computed_md5"], ("74d manifest md5", e["bit"])
        assert c["sha256"] == sha256(open(f"{MIRROR}/{e['file']}", "rb").read()), ("74d sha256", e["bit"])
        assert c["bytes"] == e["certificate_bytes"], ("74d manifest bytes", e["bit"])
        assert c["whole_git_blob_sha"] == e["pinned_blob_sha"], ("74d manifest blob sha", e["bit"])
        assert c["rows"] == v["strategy_rows"], ("74d manifest rows", e["bit"])
        assert c["sub_roots_pass"] == v["subroots_passed"], ("74d manifest subroots", e["bit"])
        assert c["terminal_count"] == v["terminal_count"], ("74d terminal", e["bit"])
        assert list(c["terminal_range"]) == v["terminal_range"], ("74d trange", e["bit"])
        assert c["winner_states"] == v["winner_states"], ("74d winner", e["bit"])
        assert c["loser_states"] == v["loser_states"], ("74d loser", e["bit"])
        assert c["loser_reply_edges"] == v["loser_reply_edges"], ("74d edges", e["bit"])
        assert c["visited_states_across_subroots"] == v["visited_states_across_subroots"], ("74d visited", e["bit"])
        assert c["root_check"]["loser_mobility"] == v["root_mobility"], ("74d mobility", e["bit"])
        assert c["root_check"]["match"] is True
        assert c["union_missing"] == 0 and c["union_extra"] == 0
        assert rec74[e["bit"]]["opponent_legal_replies"] == v["root_mobility"], ("74d receipts mobility", e["bit"])
    # 74d bit91: documented D4 duplicate of 72b bit85, no own bytes on main
    b91 = [x for x in m["certificates"] if x["bit"] == 91][0]
    assert b91["storage"]["layout"].startswith("not pushed: D4 duplicate of cost72b bit85")
    backing = b91["storage"]["backing_certificate"]
    assert backing["git_blob_sha"] == bykey[("72b", 85)][0]["pinned_blob_sha"], ("74d bit91 backing file is not the verified 72b bit85 bytes",)
    assert backing["path"].endswith("/class2-lane-cost72b-certificates/bit85-root-00000000002000809102000002000000.cert")

    # 77c / 77d / 63g / 72b receipts + 74d manifest: independent D4 canon check
    canon_sources = {}
    for band, fn, key in (
        ("63g", REC_63G, "cost63g_addition"), ("72b", REC_72B, "cost72b_addition"),
        ("77c", REC_77C, "cost77c_addition"), ("77d", REC_77D, "cost77d_addition")):
        for r in json.load(open(fn))[key]:
            canon_sources[(band, r["bit"])] = r["d4_canonical_hex"]
    for c in json.load(open(MANIFEST_74D))["certificates"]:
        canon_sources[("74d", c["bit"])] = c["d4_canonical_hex"]
    for _, e, _ in entries:
        want = canon_sources[(e["band"], e["bit"])]
        got = d4_canon(e["root_hex"])
        assert got == want, ("independent d4 canon", e["band"], e["bit"], got, want)
    # 74d bit91 D4-duplicate claim: same canonical orbit as 72b bit85
    assert canon_sources[("74d", 91)] == canon_sources[("72b", 85)] == d4_canon(bykey[("72b", 85)][0]["root_hex"])

    total_rows = sum(e["verifier_rows"] for _, e, _ in entries)
    total_sub = sum(e["verifier_subroots_passed"] for _, e, _ in entries)
    total_bytes = sum(e["certificate_bytes"] for _, e, _ in entries)
    from collections import Counter
    per_band = Counter(e["band"] for _, e, _ in entries)

    doc = {
        "schema": "n11-class2-lane-singlefile-bands-certificates-bigint-independent-reverification-20261117-v1",
        "date": "2026-11-17",
        "pin": {
            "commit": PIN,
            "record_files": sorted(set(r["record_source"] for r in records)),
            "authoritative_blob_sha_table": "GitHub directory listing of the five band certificate dirs at the pinned commit (fields name/sha/size), embedded in the script as PINS and asserted 43/43 against the mirrored bytes",
        },
        "method": {
            "records": "43 single-file WIN7-D10 certificate records of the remaining-band survey batch (63g 14 + 74d 8 + 77c 7 + 77d 7 + 72b 7): receipts-recompute per-entry records (rows/md5/sub_roots_pass) for 63g/72b/77c/77d and the win7-certificates manifest records for 74d; the 6 72b split-part bits, 7 74d split-part bits, 77c bit 10, 77d bits 58/66/78/108/111 and the 74d bit 91 D4 duplicate are outside this batch (split parts deferred to the split-part batch; bit 91 is documented as backed by the 72b bit 85 certificate bytes verified here)",
            "bytes": "each certificate fetched from the commit-pinned raw CDN URL into the local mirror; git blob sha+size asserted against the authoritative GitHub directory listing at the pin (43/43)",
            "verifier": "verify_win7_certificate_bigint_independent.mjs (git blob 62b5d9413daafb172f6e10249976ee6808f7b454, asserted by the script): BigInt 3x3 cofactor expansion of the exact lifted determinant [x^2+y^2,x,y,1], no floating point, no solver/verdict-cache import; root stones=7 + safe check, loser mobility vs independent enumeration, per-subroot winner strategy legality walk, union missing/extra 0/0, rows sorted unique, terminal range within 13..17",
        },
        "entries": [e for _, e, _ in entries],
        "cross_checks": {
            "cost63g_manifest_14_bits": "md5/sha256/bytes/whole_git_blob_sha/rows/sub_roots_total/root_check.loser_mobility/terminal_range per bit all reproduced; verifier sums over the 14 bits equal the manifest and receipts totals (rows 419398, sub_roots 667, bytes 15142573)",
            "cost72b_manifest_7_bits_and_totals": "per-bit md5/sha256/bytes/whole_git_blob_sha/rows/sub_roots_pass/terminal_count/terminal_range/winner_states/loser_states/loser_reply_edges/visited_states/root_check.loser_mobility all reproduced; the 13-record manifest totals (rows 636225, sub_roots 729, visited 1378650, winner 889294, loser 264554, terminal 224802, edges 1241817, extraction_nodes 200029509) re-summed and asserted",
            "cost74d_manifest_8_bits_and_totals": "per-bit full-field agreement (md5/sha256/bytes/whole_git_blob_sha/rows/sub_roots_pass/terminal_count/range/winner/loser/edges/visited/mobility) plus receipts-recompute root_hex and opponent_legal_replies agreement; the 15-record manifest totals (rows 723630, sub_roots 883) re-summed and asserted; bit 91 recorded as documented D4 duplicate of 72b bit 85 (own-coordinate md5 refers to the bit-91 extraction and is not asserted against the 72b file bytes)",
            "independent_d4_canon_all_43_records": "a third, in-script D4 canonicalization implementation (min hex over the eight square symmetries of the 11x11 board) reproduces every record's d4_canonical_hex for all 43 verified certificates; the 74d bit 91 D4-duplicate claim is machine-checked as canon(74d bit91 root) == canon(72b bit85 root)",
            "cross_band_root_distinctness": "all 43 root_hex values are distinct across the five bands (asserted at record load)",
        },
        "summary": {
            "records": len(entries),
            "distinct_certificate_files": len(set(e["file"] for _, e, _ in entries)),
            "verifier_pass": len(entries),
            "verifier_fail": 0,
            "record_md5_asserted": len(entries),
            "record_md5_mismatch": 0,
            "pin_blob_sha_mismatch": 0,
            "total_rows_independently_verified": total_rows,
            "total_sub_roots_independently_verified": total_sub,
            "total_certificate_bytes_rehashed": total_bytes,
            "records_per_band": dict(sorted(per_band.items())),
        },
        "interpretation_guard": [
            "this re-verification upgrades the 43 single-file certificates of the five bands from receipt-cert/manifest documentation to bytes-level independently re-verified evidence, on top of the earlier 33 (58c) + 82 (warm/multiband) + 83 (receipts-recompute bands) sessions; it does not change any frontier number",
            "the 24 split-part certificates of bands 72c/73g/73h/83d and the 20 split-part bits of these five bands remain deferred to a later split-part batch",
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
