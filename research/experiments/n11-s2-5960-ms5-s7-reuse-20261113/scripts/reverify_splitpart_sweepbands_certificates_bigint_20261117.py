#!/usr/bin/env python3
"""Independent bytes-level re-verification of the 24 split-part WIN7-D10
certificates of the four sweep bands (cost-72c 9, 73g 8, 73h 4, 83d 3),
against their per-record documentation and the BigInt independent verifier.
This is the split-part batch for the four bands that store ALL certificates
as parts, identified by the remaining-band certificate bytes survey
(class2-lane-remaining-band-certificate-bytes-survey-20261117.json); with
the single-file batch (43 records) and the five-band split-part batch
(18 records) it exhausts the 85 survey-identified remaining-band
certificate records of this experiment.

Run from the working mirror directory of
yuubinnkyoku/kyouen-researches @ main commit 8859cd17b174dbb50a5d8233ddd5a30f3dd0e24d
with the four band certificate directories mirrored under certs/ via
commit-pinned raw URLs and the record files mirrored next to this script.

Steps (all asserted):
 1. assert the verifier script's git blob sha (62b5d9413d...);
 2. load the record sources:
      - cost-72c/73g/73h: the win7-certificates manifests (per-bit
        md5/bytes/strategy_rows/part_md5s/part_bytes/part_blob_shas/
        verify.bigint full field set) cross-agreed with the
        receipts-recompute records (rows/md5/sub_roots_pass/root_hex/
        d4_canonical_hex; 73h receipts document md5 null, the manifest
        md5 is the whole-file documentation for 73h);
      - cost-83d: receipts-recompute only (83d has no README and no
        manifest; per-part pins rest on the GitHub listing, the whole
        md5 on the receipts);
    total 24 records, all distinct (band, bit) and all distinct root_hex,
    and disjoint from the 61 root_hex values of the two earlier batches;
 3. assert each mirrored part file's git blob sha and size against the
    authoritative GitHub directory listing of the pinned commit
    (48/48 pin table embedded below, fields=name/sha/size), and for
    72c/73g/73h additionally against the manifest part_blob_shas and
    part_md5s (machine-parsed, guarding the pin table transcription);
 4. per-part manifest agreement (bytes/md5), part1 ends on a line
    boundary;
 5. concatenate part1+part2 per certificate and assert the whole-file
    md5 against the record; for 72c/73g/73h additionally bytes;
 6. run the BigInt independent verifier once per concatenated
    certificate; assert verdict, root stones 7, root_safe, rows
    sorted-unique, union missing/extra 0/0, terminal range within
    13..17, strategy_rows == record rows, subroots_passed == record
    sub_roots_pass, and root_hex == record root_hex; for 72c/73g/73h
    additionally full agreement with the manifest verify.bigint field
    set (root_mobility/subroots_passed/terminal_range/terminal_count/
    visited_states_across_subroots/loser_reply_edges);
 7. cross-checks:
      - independent in-script D4 canonicalization (fifth implementation)
        reproduces every record's d4_canonical_hex for all 24
        certificates;
      - manifest totals (strategy_rows/bytes/certificates/bytes_parts)
        and receipts totals (certificate_rows/certificate_bytes/
        certificate_sub_roots) equal the verifier sums per band;
      - joined sha256 and git blob sha recorded for all 24 (new
        bytes-level documentation; the receipts only document md5);
 8. write the deterministic re-verification JSON to the output path.

Determinism: no timestamps, no wall times, fixed record order; running
twice must produce byte-identical output.
11x11 empty board remains UNKNOWN; WIN7 certificates prove only
individual 7-stone roots within depth 10.
"""
import concurrent.futures, hashlib, json, os, subprocess

PIN = "8859cd17b174dbb50a5d8233ddd5a30f3dd0e24d"
EXP = "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113"
OUTD = f"{EXP}/output"
VERIFIER = f"{EXP}/scripts/verify_win7_certificate_bigint_independent.mjs"
VERIFIER_BLOB_SHA = "62b5d9413daafb172f6e10249976ee6808f7b454"
NODE = "node"
MIRROR = os.environ.get("REVERIFY_MIRROR", "certs")
OUT = f"{OUTD}/class2-lane-splitpart-sweepbands-certificates-bigint-independent-reverification-20261117.json"
EARLIER_SINGLEFILE = f"{OUTD}/class2-lane-singlefile-bands-certificates-bigint-independent-reverification-20261117.json"
EARLIER_SPLITPART = f"{OUTD}/class2-lane-splitpart-bands-certificates-bigint-independent-reverification-20261117.json"

# Authoritative GitHub directory listing at PIN (fields name|sha|size),
# one line per split part file across the four band dirs (48 lines).
PINS = """
class2-lane-cost72c-certificates/bit1-root-00000000000000801202000000220002.cert.part1of2|5baca28650dd7cee907c8a236f676249737720e2|991259
class2-lane-cost72c-certificates/bit1-root-00000000000000801202000000220002.cert.part2of2|b084d29730db26ddd95cd2c3b25a6f7275d9860d|991292
class2-lane-cost72c-certificates/bit24-root-00000000000000801202000001220000.cert.part1of2|70b501172e6376a4ed22a831d43bf866b572a943|800933
class2-lane-cost72c-certificates/bit24-root-00000000000000801202000001220000.cert.part2of2|d7806c7fab887fd86921b590aaa4401a1c24003f|800435
class2-lane-cost72c-certificates/bit39-root-00000000000000801202008000220000.cert.part1of2|4aa82b14bb479719525a762d35ff04612e34c315|593821
class2-lane-cost72c-certificates/bit39-root-00000000000000801202008000220000.cert.part2of2|d34e86699b9adbd8dd2d90624ba3e2b89594475d|593569
class2-lane-cost72c-certificates/bit59-root-00000000000000801a02000000220000.cert.part1of2|8641585c7b3fd5e5515daa10321a4a633a1f28f1|570846
class2-lane-cost72c-certificates/bit59-root-00000000000000801a02000000220000.cert.part2of2|dab799a961ed1dfc5bef6132fcded5539238e0c4|570012
class2-lane-cost72c-certificates/bit64-root-00000000000000811202000000220000.cert.part1of2|9aab862ed20177f920a1aa4d01a4320f70987a06|674315
class2-lane-cost72c-certificates/bit64-root-00000000000000811202000000220000.cert.part2of2|285face8493ef23553ce0ce59907c4b1f6ee2627|673360
class2-lane-cost72c-certificates/bit67-root-00000000000000881202000000220000.cert.part1of2|8e1dd2f5f2c994625e05143b1f3c05cfb9752897|505555
class2-lane-cost72c-certificates/bit67-root-00000000000000881202000000220000.cert.part2of2|e0b583e84c94602f95601ac4407dd3ec5d8e8bc9|504767
class2-lane-cost72c-certificates/bit7-root-00000000000000801202000000220080.cert.part1of2|ee4ff12194b72f2abde7d91aaa7d51f2f403d6bb|591133
class2-lane-cost72c-certificates/bit7-root-00000000000000801202000000220080.cert.part2of2|79d201c6b88b8ebe6536ba48a5a88491f759635a|590747
class2-lane-cost72c-certificates/bit72-root-00000000000001801202000000220000.cert.part1of2|1ffb5c4ef2d0efdbbeed0c63781b7bf328c5df81|376900
class2-lane-cost72c-certificates/bit72-root-00000000000001801202000000220000.cert.part2of2|779378be117c44b54b19048f8068a29a2e32a1e5|376494
class2-lane-cost72c-certificates/bit96-root-00000001000000801202000000220000.cert.part1of2|a2f333daed70fc8500a864b411720208bd99a7ad|699648
class2-lane-cost72c-certificates/bit96-root-00000001000000801202000000220000.cert.part2of2|f0dd28b26c651738601f0432bb755f0ea05f0602|699092
class2-lane-cost73g-certificates/bit113-root-00020000000000849002000000000800.cert.part1of2|86043ff50c9ca7d1ee99a8a8d87cd504ca20fb60|560539
class2-lane-cost73g-certificates/bit113-root-00020000000000849002000000000800.cert.part2of2|8b666bdfbc98b0ad2caf8205fea4bf81b2f5f6ce|560550
class2-lane-cost73g-certificates/bit31-root-00000000000000849002000080000800.cert.part1of2|e6df769953abf0bede854855f703a8325f24f400|796484
class2-lane-cost73g-certificates/bit31-root-00000000000000849002000080000800.cert.part2of2|fe72dace55a9f4be9bbdc73833e43098df076a07|796508
class2-lane-cost73g-certificates/bit54-root-00000000000000849042000000000800.cert.part1of2|e45d586c5127a15a3492a9c1a21f6730692145c8|1021164
class2-lane-cost73g-certificates/bit54-root-00000000000000849042000000000800.cert.part2of2|4ed0a546d3bfb2f73207f3276d67bff70c51c318|1021185
class2-lane-cost73g-certificates/bit56-root-00000000000000849102000000000800.cert.part1of2|57db778b38c6e1e4a4baca11b3c84d371668a859|527206
class2-lane-cost73g-certificates/bit56-root-00000000000000849102000000000800.cert.part2of2|5582a8749e1f9ecd76e9869d2b305a4b41d44054|527214
class2-lane-cost73g-certificates/bit62-root-0000000000000084d002000000000800.cert.part1of2|59fed86945fad1c383e0293f248359bca627e7d5|724323
class2-lane-cost73g-certificates/bit62-root-0000000000000084d002000000000800.cert.part2of2|2e66cf74ef48d756b26fb058491be71007e2af55|724356
class2-lane-cost73g-certificates/bit69-root-00000000000000a49002000000000800.cert.part1of2|59437a1d732557628c228437905a6df9b90d95b5|829756
class2-lane-cost73g-certificates/bit69-root-00000000000000a49002000000000800.cert.part2of2|6d5c9d59bac7c8bd74f19902f7bf79d44e420502|829818
class2-lane-cost73g-certificates/bit81-root-00000000000200849002000000000800.cert.part1of2|01ae2e668694a08b8483d287ddc910fc8edcedb8|599310
class2-lane-cost73g-certificates/bit81-root-00000000000200849002000000000800.cert.part2of2|3ad8405f22429ec042d2d8629d242d48aff97400|599373
class2-lane-cost73g-certificates/bit89-root-00000000020000849002000000000800.cert.part1of2|671a8ec8f6d21bcc628c9013c787c11de1c93a09|1137503
class2-lane-cost73g-certificates/bit89-root-00000000020000849002000000000800.cert.part2of2|df9ae207249cd83654d165ddb596987409cb20a5|1137508
class2-lane-cost73h-certificates/bit45-root-00000000200000083800200000000200.cert.part1of2|1d0f6a4bbf21cb4d6d842dad0838f6ee747d5d7a|815509
class2-lane-cost73h-certificates/bit45-root-00000000200000083800200000000200.cert.part2of2|0fe43fec9d9164ab924a844936e9fc41eff78445|814405
class2-lane-cost73h-certificates/bit48-root-00000000200000083801000000000200.cert.part1of2|fa53dbabad90f693183cce1679616a62ad4aada1|633532
class2-lane-cost73h-certificates/bit48-root-00000000200000083801000000000200.cert.part2of2|e4e3b066288831b730a117f141e3c3a51d7baa25|631244
class2-lane-cost73h-certificates/bit82-root-00000000200400083800000000000200.cert.part1of2|cca89b12bfff1fa911793619954c889f6d0b7694|812049
class2-lane-cost73h-certificates/bit82-root-00000000200400083800000000000200.cert.part2of2|d21bf57579258a35769e7c43a234fff552f0af81|807665
class2-lane-cost73h-certificates/bit96-root-00000001200000083800000000000200.cert.part1of2|274fbfda2dd2fc400d73d3b308c5f3416e7130a8|936786
class2-lane-cost73h-certificates/bit96-root-00000001200000083800000000000200.cert.part2of2|3d9e7372737df25cda6c4aba4f9bfb50285cb6e5|933225
class2-lane-cost83d-certificates/bit16-root-00000000200000003800100000010200.cert.part1of2|44176845d520a7feb3d1d18d3b1912a388c13623|1226499
class2-lane-cost83d-certificates/bit16-root-00000000200000003800100000010200.cert.part2of2|adb6daf529884d729731d45afa6c72b3dc7d2016|1226472
class2-lane-cost83d-certificates/bit51-root-00000000200000003808100000000200.cert.part1of2|6a00807a4b47372df118b4dc4d6f80cf10d4be3b|1049949
class2-lane-cost83d-certificates/bit51-root-00000000200000003808100000000200.cert.part2of2|08378253032b6cb56d7ba914c9c6036aeaf2a96b|1049928
class2-lane-cost83d-certificates/bit82-root-00000000200400003800100000000200.cert.part1of2|14559e5787772a4bd65f982181e8b05770d2d24b|1638728
class2-lane-cost83d-certificates/bit82-root-00000000200400003800100000000200.cert.part2of2|126b0a5f56c3ae7ed6ff94f6049225c9f30355cc|1638684
"""

# Local mirrors carry a rec- prefix to distinguish them from the same-name
# class-frontier files of other bands; the repo paths (record_source) have
# no prefix. Mirror == repo bytes verified by cmp at the pinned commit.
REC = {
    "72c": "rec-class-frontier-cost72c-receipts-recompute-20261115.json",
    "73g": "rec-class-frontier-cost73g-receipts-recompute-20261115.json",
    "73h": "rec-class-frontier-cost73h-receipts-recompute-20261115.json",
    "83d": "rec-class-frontier-cost83d-receipts-recompute-20261115.json",
}
REC_REPO = {
    "72c": "class-frontier-cost72c-receipts-recompute-20261115.json",
    "73g": "class-frontier-cost73g-receipts-recompute-20261115.json",
    "73h": "class-frontier-cost73h-receipts-recompute-20261115.json",
    "83d": "class-frontier-cost83d-receipts-recompute-20261115.json",
}
MANIFEST = {
    "72c": "class2-lane-cost72c-win7-certificates-20261115.json",
    "73g": "class2-lane-cost73g-win7-certificates-20261115.json",
    "73h": "class2-lane-cost73h-win7-certificates-20261115.json",
}

BAND_ORDER = ["72c", "73g", "73h", "83d"]
BITS = {
    "72c": [1, 7, 24, 39, 59, 64, 67, 72, 96],
    "73g": [31, 54, 56, 62, 69, 81, 89, 113],
    "73h": [45, 48, 82, 96],
    "83d": [16, 51, 82],
}
EXPECTED_RECORDS = 24
EXPECTED_PARTS = 48

# receipts totals (certificate_rows / certificate_bytes / certificate_sub_roots)
TOTALS_REC = {
    "72c": {"rows": 321781, "bytes": 11604178, "sub_roots": 474, "receipts": 9},
    "73g": {"rows": 343092, "bytes": 12392797, "sub_roots": 450, "receipts": 8},
    "73h": {"rows": 176451, "bytes": 6384415, "sub_roots": 234, "receipts": 4},
    "83d": {"rows": 216638, "bytes": 7830260, "sub_roots": 188, "receipts": 3},
}


def md5(b):
    return hashlib.md5(b).hexdigest()


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def git_blob_sha(b):
    return hashlib.sha1(b"blob %d\x00" % len(b) + b).hexdigest()


def d4_canon(h):
    """Independent D4 canonical form on the 11x11 board: min hex over the
    eight square symmetries. Fifth implementation relative to the fold/
    harvest tools and the two earlier batch scripts; asserted against every
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
    for band in BAND_ORDER:
        rec_by_bit = {r["bit"]: r for r in json.load(open(REC[band]))[f"cost{band}_addition"]}
        assert len(rec_by_bit) == TOTALS_REC[band]["receipts"], (band, len(rec_by_bit))
        man_by_bit = None
        if band in MANIFEST:
            m = json.load(open(MANIFEST[band]))
            man_by_bit = {c["bit"]: c for c in m["certificates"]}
            assert len(man_by_bit) == TOTALS_REC[band]["receipts"], (band, "manifest count")
        for bit in BITS[band]:
            r = rec_by_bit[bit]
            assert r["certified"] is True
            c = man_by_bit[bit] if man_by_bit else None
            if c is not None:
                assert c["root_hex"] == r["root_hex"], (band, bit, "root")
                assert c["strategy_rows"] == r["rows"], (band, bit, "rows man/rec")
                assert c["verify"]["bigint"]["subroots_passed"] == r["sub_roots_pass"], (band, bit, "subs man/rec")
                if r.get("md5"):
                    assert c["md5"] == r["md5"], (band, bit, "md5 man/rec")
                assert c["join_md5_equals_whole"] is True
            R.append({
                "band": band, "bit": bit, "root_hex": r["root_hex"],
                "d4_canonical_hex": r["d4_canonical_hex"],
                "band_dir": band_dir(band),
                "base": f"bit{bit}-root-{r['root_hex']}.cert",
                "rows": r["rows"],
                "md5": (c["md5"] if c is not None else r["md5"]),
                "receipts_md5": r.get("md5"),
                "sub_roots_pass": r["sub_roots_pass"],
                "record_source": (f"{OUTD}/{MANIFEST[band]}" if band in MANIFEST
                                  else f"{OUTD}/{REC_REPO[band]}"),
                "record_kind": ("win7-certificates-manifest+receipts-recompute"
                                if c is not None else "receipts-recompute"),
                "manifest": c,
            })
    assert len(R) == EXPECTED_RECORDS, len(R)
    kb = [(r["band"], r["bit"]) for r in R]
    assert len(set(kb)) == len(kb), "duplicate (band, bit)"
    roots = [r["root_hex"] for r in R]
    assert len(set(roots)) == len(roots), "duplicate root_hex across records"
    # disjointness from the two earlier batches (both outputs mirrored locally)
    earlier_roots = set()
    for fn in (EARLIER_SINGLEFILE, EARLIER_SPLITPART):
        d = json.load(open(fn))
        earlier_roots.update(e["root_hex"] for e in d["entries"])
    assert len(earlier_roots) == 61, len(earlier_roots)
    overlap = set(roots) & earlier_roots
    assert not overlap, ("root overlap with earlier batches", sorted(overlap))
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
    if rec["manifest"] is not None:
        c = rec["manifest"]
        for desc_sha, desc_md5, desc_bytes, rel, raw in zip(
                c["part_blob_shas"], c["part_md5s"], c["part_bytes"],
                (p1, p2), (raw1, raw2)):
            assert desc_sha == pins[rel][0], ("manifest part blob sha vs pin", rel)
            assert desc_sha == git_blob_sha(raw), ("manifest part blob sha", rel)
            assert desc_md5 == md5(raw), ("manifest part md5", rel)
            assert desc_bytes == len(raw), ("manifest part bytes", rel)
        assert c["repo_paths"] == [p1, p2], ("manifest repo_paths", base)
    whole = raw1 + raw2
    computed_md5 = md5(whole)
    assert rec["md5"] and computed_md5 == rec["md5"], \
        ("record md5 mismatch", rec["band"], rec["bit"], computed_md5, rec["md5"])
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
        assert git_blob_sha(whole) == c["repo_blob_sha"], \
            ("manifest joined repo_blob_sha", rec["band"], rec["bit"])
    tmp = f"/tmp/reverify_sweepbands_{rec['band']}_{rec['bit']}.cert"
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
        vb = rec["manifest"]["verify"]["bigint"]
        assert vb["root_stones"] == 7 and vb["root_safe"] is True
        assert vb["root_mobility"] == v["root_mobility"], ("mobility", rec["band"], rec["bit"])
        assert vb["subroots_passed"] == v["subroots_passed"], ("subs", rec["band"], rec["bit"])
        assert list(vb["terminal_range"]) == v["terminal_range"], ("trange", rec["band"], rec["bit"])
        assert vb["terminal_count"] == v["terminal_count"], ("terminal", rec["band"], rec["bit"])
        assert vb["visited_states_across_subroots"] == v["visited_states_across_subroots"], \
            ("visited", rec["band"], rec["bit"])
        assert vb["loser_reply_edges"] == v["loser_reply_edges"], ("edges", rec["band"], rec["bit"])
        assert vb["union_missing"] == 0 and vb["union_extra"] == 0
        assert vb["rows_sorted_unique"] is True
        assert rec["manifest"]["loser_first_moves"] == v["root_mobility"], \
            ("loser_first_moves vs mobility", rec["band"], rec["bit"])
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
    entries = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
        futs = {ex.submit(verify_one, rec, pins): rec for rec in records}
        for fut in concurrent.futures.as_completed(futs):
            e, v = fut.result()
            entries.append((futs[fut], e, v))
    order = {b: i for i, b in enumerate(BAND_ORDER)}
    entries.sort(key=lambda t: (order[t[0]["band"]], t[0]["bit"]))

    # ---- cross-checks ----
    # independent D4 canonicalization: all 24 records
    for rec, e, _ in entries:
        got = d4_canon(rec["root_hex"])
        assert got == rec["d4_canonical_hex"], \
            ("independent d4 canon", rec["band"], rec["bit"], got, rec["d4_canonical_hex"])

    # per-band totals: manifest totals (72c/73g/73h) and receipts totals (all)
    for band in BAND_ORDER:
        eb = [e for rec, e, _ in entries if rec["band"] == band]
        t = TOTALS_REC[band]
        assert len(eb) == t["receipts"], (band, len(eb))
        assert sum(e["verifier_rows"] for e in eb) == t["rows"], (band, "rows total")
        assert sum(e["joined_bytes"] for e in eb) == t["bytes"], (band, "bytes total")
        assert sum(e["verifier_subroots_passed"] for e in eb) == t["sub_roots"], (band, "subs total")
        rt = json.load(open(REC[band]))["totals"]
        assert rt["certificate_rows"] == t["rows"] and rt["certificate_bytes"] == t["bytes"] \
            and rt["certificate_sub_roots"] == t["sub_roots"], (band, "receipts totals")
        if band in MANIFEST:
            mt = json.load(open(MANIFEST[band]))["totals"]
            assert mt["certificates"] == t["receipts"], (band, "manifest certificates")
            assert mt["strategy_rows"] == t["rows"], (band, "manifest rows total")
            assert mt["bytes"] == t["bytes"] and mt["bytes_parts"] == t["bytes"], \
                (band, "manifest bytes total")

    total_rows = sum(e["verifier_rows"] for _, e, _ in entries)
    total_sub = sum(e["verifier_subroots_passed"] for _, e, _ in entries)
    total_bytes = sum(e["joined_bytes"] for _, e, _ in entries)
    from collections import Counter
    per_band = Counter(rec["band"] for rec, _, _ in entries)

    doc = {
        "schema": "n11-class2-lane-splitpart-sweepbands-certificates-bigint-independent-reverification-20261117-v1",
        "date": "2026-11-17",
        "pin": {
            "commit": PIN,
            "record_files": sorted(set(r["record_source"] for r in records)),
            "authoritative_blob_sha_table": "GitHub directory listing of the four band certificate dirs at the pinned commit (fields name/sha/size), embedded in the script as PINS, asserted 48/48 against the mirrored part bytes and 42/42 against the manifest part_blob_shas (machine-parsed)",
        },
        "method": {
            "records": "24 split-part WIN7-D10 certificate records of the four sweep bands that store all certificates as parts (72c 9 + 73g 8 + 73h 4 + 83d 3): win7-certificates manifest records cross-agreed with receipts-recompute for 72c/73g/73h (the 73h receipts document md5 null; the manifest md5 is the whole-file documentation), receipts-recompute records for 83d (no README, no manifest; per-part pins rest on the listing, whole md5 on the receipts); with the single-file batch (43) and the five-band split-part batch (18) this exhausts the 85 survey-identified remaining-band certificate records",
            "bytes": "each part fetched from the commit-pinned raw CDN URL into the local mirror; git blob sha+size asserted against the authoritative GitHub directory listing at the pin (48/48) and against the manifest part metadata for 72c/73g/73h (part_blob_shas/part_md5s/part_bytes, machine-parsed); part1 asserted to end on a line boundary; certificates reconstructed as exact part1+part2 concatenations",
            "verifier": "verify_win7_certificate_bigint_independent.mjs (git blob 62b5d9413daafb172f6e10249976ee6808f7b454, asserted by the script): BigInt 3x3 cofactor expansion of the exact lifted determinant [x^2+y^2,x,y,1], no floating point, no solver/verdict-cache import; root stones=7 + safe check, loser mobility vs independent enumeration, per-subroot winner strategy legality walk, union missing/extra 0/0, rows sorted unique, terminal range within 13..17",
        },
        "entries": [e for _, e, _ in entries],
        "cross_checks": {
            "independent_d4_canon_all_24_records": "a fifth, in-script D4 canonicalization implementation (min hex over the eight square symmetries of the 11x11 board) reproduces every record's d4_canonical_hex for all 24 certificates (receipts-recompute)",
            "manifest_verify_bigint_field_agreement_21_records": "for 72c/73g/73h the verifier output fully reproduces the manifest verify.bigint field set (root_mobility/subroots_passed/terminal_range/terminal_count/visited_states_across_subroots/loser_reply_edges) plus manifest loser_first_moves == root_mobility; manifest part metadata (blob sha/md5/bytes per part) reproduced against the mirrored bytes and against the pin table",
            "band_totals": "per band the verifier sums equal the receipts totals (72c 321,781 rows / 474 sub_roots / 11,604,178 bytes; 73g 343,092 / 450 / 12,392,797; 73h 176,451 / 234 / 6,384,415; 83d 216,638 / 188 / 7,830,260) and, for 72c/73g/73h, the manifest totals (strategy_rows/bytes/bytes_parts/certificates)",
            "cross_batch_root_disjointness": "all 24 root_hex distinct in-batch and disjoint from the 61 root_hex values of the single-file batch (43) and the five-band split-part batch (18), asserted at record load against the two published batch outputs",
            "joined_hash_documentation": "joined sha256 and git blob sha recorded for all 24 as new bytes-level documentation; 83d whole-file documentation beyond the receipts md5 is new here (83d has no README/manifest)",
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
            "this re-verification upgrades the 24 split-part certificates of the four sweep bands from manifest/receipt documentation to bytes-level independently re-verified evidence; with the single-file batch (43 records) and the five-band split-part batch (18 records), the bytes-re-verified population stands at 259 + 24 = 283 records and the survey-identified remaining-band certificate population of this experiment is exhausted; it does not change any frontier number",
            "the newly published 66j/69j/71e certificate bands and the 63c/63d extractor regeneration remain as later candidates",
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
