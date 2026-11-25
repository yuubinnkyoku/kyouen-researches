#!/usr/bin/env python3
"""Independent bytes-level re-verification of the 11 WIN7-D10 certificates of
the published cost-78c certificate band (child
00000000000000403800000008000008, s6_s7_edge_cost 78, published by the
parallel class2-lane certificate-extraction session as per-bit commits
b359756fef..97650e276e with the band dir
output/class2-lane-cost78c-certificates/), with a third-implementation BigInt
independent verification beyond the extractor's own Bareiss verification
(verify_bit7_win7_cert.ts run per verify_cost78c_one.sh).

This implements the optional follow-up named by the cost-78c claim itself:
claim v4 (git blob 5cd0591a0676494965a02460dff7246c1d3aa885, published at
3ed406e339 with the in-band manifest) ends its next_action with "optional
follow-up: BigInt independent third-implementation re-verification of the 11
certificates"; the current-main claim v5 (git blob
1850832186ba9c8715624094f05d67aa4eb10f0b, a provenance-only correction over
v4 whose certificates block is asserted byte-equal here) carries the same
next_action.

This follows the reverify_cost73j / reverify_cost73k / reverify_cost73l BigInt
batches: on top of the bytes pins it runs the BigInt independent verifier
(verify_win7_certificate_bigint_independent.mjs, git blob
62b5d9413daafb172f6e10249976ee6808f7b454) once per certificate and
cross-agrees the result with
 - the in-band manifest class2-lane-cost78c-win7-certificates-20261117.json
   (git blob b7fe519e923c6170e836f71e3f084f73219d5, published at 3ed406e339):
   per-record root/verdict WIN7/depth 10/rows/extraction_nodes/fbt_drops 0/
   subroots==subroots_pass==loser_mobility/union 0/0/terminal_stone_range/
   md5/sha256/d4_canon_root/raw_is_canon/storage, plus the manifest totals
   (11 certificates / 614,003 rows / 77,967,826 extraction nodes /
   22,223,603 published bytes / 0 fbt_drops_total / 0 capped_per_move_total);
 - stats.json (git blob 70813ca75d3216d1836e408183c5d0db883e6cbc, published at
   eb157af2be): per-bit root/rows/nodes/moves/md5/sha256/size/fbt_drops;
 - det-reextraction.json (git blob 07e150ede079deb7d70a734d41ea5d1a49b00fea):
   the fresh-process determinism re-extraction md5s of bits [69, 116] equal
   the joined md5s recomputed here from the pinned certificate bytes;
 - the per-bit rootcheck.json sidecars (stones/loserMobility; two JSON lines)
   and the per-bit subroots.jsonl sidecars (batched per-loser-first-move
   seen/terminals/opponentEdges/range, summed to the verifier's
   visited_states/terminal_count/loser_reply_edges);
 - the sweep claim v5 (schema
   n11-class2-lane-cost78c-inflight-20261118-v5: win7_d10_bits, s6_child,
   certificates COMPLETE/manifest_blob_sha/totals equal to the manifest's,
   and its 12 confirmation root_canons).

Cost-78c specifics handled here:
 - the authoritative pin table is the GitHub API contents listing of the
   band dir at the pin commit 1687397338a89a489263c12f41780e1182f18b9c
   (59 files, name|git blob sha|size), embedded verbatim in PINS_TABLE below;
   the claim v5 blob is the 60th pin and the superseded claim v4 blob
   (provenance diff asserted against v5) the 61st;
 - bit 116 is a THREE-part split (part1of3/part2of3/part3of3, README-split
   names two split boundary bytes); the other ten bits are two-part splits;
 - every root is child | (1 << bit) (asserted against the claim s6_child,
   the manifest record root, the certificate file name, the README root line
   and the verifier's root_hex);
 - cross-batch disjointness covers the 183 earlier BigInt-verified roots:
   the 151 of the eight earlier batches plus the 32 roots of the cost-73l
   BigInt batch output (git blob
   547fe617abc179ff47f3607079d3ca8c1de4359b), all fetched from the published
   repo, blob-pinned inline as in the 73j/73k/73l batches.

Run from this directory with the mirror fetched from the commit-pinned raw
CDN URLs (see MIRROR notes in main()).

Determinism: no timestamps, no wall times, fixed record order; running twice
must produce byte-identical output.
11x11 empty board remains UNKNOWN; WIN7-D10 certificates prove only
individual 7-stone roots within depth 10.
"""
import concurrent.futures, hashlib, json, os, re, subprocess

PIN = "1687397338a89a489263c12f41780e1182f18b9c"
ROOT = os.path.dirname(os.path.abspath(__file__))
VERIFIER = os.path.join(ROOT, "verify_win7_certificate_bigint_independent.mjs")
VERIFIER_BLOB_SHA = "62b5d9413daafb172f6e10249976ee6808f7b454"
NODE = "node"
MIRROR = os.path.join(ROOT, "certs78c")
CLAIM_DIR = os.path.join(ROOT, "claim78c")
CLAIM_FILE = "class2-lane-cost78c-inflight-20261117.json"
CLAIM_BLOB_SHA = "1850832186ba9c8715624094f05d67aa4eb10f0b"
CLAIM_SCHEMA = "n11-class2-lane-cost78c-inflight-20261118-v5"
CLAIM_V4_FILE = CLAIM_FILE + ".v4"
CLAIM_V4_BLOB_SHA = "5cd0591a0676494965a02460dff7246c1d3aa885"
CLAIM_V3_BLOB_SHA = "d3105b3a6c6cac68c35d84f2ebca8b10e7b72228"
FOLLOWUP_SENTENCE = ("optional follow-up: BigInt independent third-implementation"
                     " re-verification of the 11 certificates")
MANIFEST_FILE = "class2-lane-cost78c-win7-certificates-20261117.json"
MANIFEST_BLOB_SHA = "b7fe519e923c6170e836f71e3f084f73219319d5"
MANIFEST_SCHEMA = "n11-class2-lane-cost78c-win7-certificates-20261117-v1"
STATS_FILE = "stats.json"
STATS_BLOB_SHA = "70813ca75d3216d1836e408183c5d0db883e6cbc"
DET_FILE = "det-reextraction.json"
DET_BLOB_SHA = "07e150ede079deb7d70a734d41ea5d1a49b00fea"
EARLIER_DIR = os.path.join(ROOT, "earlier")
BAND_DIR = "class2-lane-cost78c-certificates"
CHILD = "00000000000000403800000008000008"
EXPECTED = 11
EXPECTED_BITS = [1, 4, 9, 30, 49, 69, 75, 79, 100, 114, 116]
THREEPART_BIT = 116
OUT = os.path.join(ROOT, "class2-lane-cost78c-certificates-bigint-"
                    "independent-reverification-20261117.json")


EARLIER_BATCHES = [
    ("class2-lane-singlefile-bands-certificates-bigint-independent-reverification-20261117.json",
     "ceb79e97f530de7f2dcdb984a9b0be928bbf592a", 43),
    ("class2-lane-splitpart-bands-certificates-bigint-independent-reverification-20261117.json",
     "5b91667255406175be32c0c47ccd48592a547607", 18),
    ("class2-lane-splitpart-sweepbands-certificates-bigint-independent-reverification-20261117.json",
     "91e9f53923655be007c05e27ca471bc211a71345", 24),
    ("class2-lane-66j69j-certificates-bigint-independent-reverification-20261117.json",
     "c24224eaa3f48b0e5d1fbe90f4daccf284e6c968", 15),
    ("class2-lane-cost63cd-certificates-regeneration-verification-20261117.json",
     "0978ed784439b05f36b0893faa0a97824f6c3a77", 2),
    ("class2-lane-cost72d-certificates-bigint-independent-reverification-20261117.json",
     "1fa6d465f6f87413f11ca113cdf6925a52859adf", 11),
    ("class2-lane-cost73j-certificates-bigint-independent-reverification-20261117.json",
     "34dd4504b889655e4e43f7b9a6f7b55391bdd562", 16),
    ("class2-lane-cost73k-certificates-bigint-independent-reverification-20261117.json",
     "6a07426a52be3f059c750dbccc20277c9c5839ca", 22),
    ("class2-lane-cost73l-certificates-bigint-independent-reverification-20261117.json",
     "547fe617abc179ff47f3607079d3ca8c1de4359b", 32),
]

# name|git blob sha|size -- the GitHub API contents listing of
# research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost78c-certificates/
# at the pin commit (59 files: 56 certificate-band files + manifest
# class2-lane-cost78c-win7-certificates-20261117.json + stats.json +
# det-reextraction.json).
PINS_TABLE = """
README-split-bit1.md|b3ba0569d85e9f7ac3137c6ee377c5838d017b9f|533
README-split-bit100.md|b6a426bb68c632fe8ec3995bc2842f510ed64dfa|534
README-split-bit114.md|c741b4b8a4023588088c0461a804e22c4a14dfc7|535
README-split-bit116.md|2ce13d9cd75940543bd7b620156c72a7b59d11f4|680
README-split-bit30.md|840d159c186c656824942a6a7ab8af826f483437|533
README-split-bit4.md|ed4972c71e2ae3ca8cd4462d705cc82c7c5473dd|533
README-split-bit49.md|2fdf461b0d367e32c894e7b1ce0ca5b5aa6b00fc|533
README-split-bit69.md|a54b79c65a17ca980bcb7b4318913e65fc883dd1|533
README-split-bit75.md|63f7f9314c5821a672db1775fae93a342b62a291|533
README-split-bit79.md|8f640c14906a76cefa108f09ac868d5bfc6f6dd3|533
README-split-bit9.md|eb43f2d9e960e630aa6733633c34e4217fa68abb|533
bit1-rootcheck.json|ac164cb503e9f8dcbfa5cdbf12fdd7d12ad2ba2d|58
bit1-subroots.jsonl|a51a6a1b55515cc4cbc9dc74b5d05dbc1bc35c7e|4587
bit100-rootcheck.json|039ae62b7e4ab8179f69ca2d323f7083775cd4ac|58
bit100-subroots.jsonl|56cc03816642c6659bc2e9c5fc791a682e2c7f50|4572
bit114-rootcheck.json|e8eb880f9d521832a92563a5a90d7b4b94b04f6d|58
bit114-subroots.jsonl|dd48acb33e86a677b8eac6af75d9581413072b94|5038
bit116-rootcheck.json|55ab4bca7cbf3173339ed13118f6ec56e0044126|58
bit116-subroots.jsonl|6a1cd2223467f9fdb57528bf165d3617f863e4b9|5039
bit30-rootcheck.json|44d50cb61b6bf903c6b61bd8bedfcd3d525a0afc|58
bit30-subroots.jsonl|dc3d9666dce817a3db0741a1ae82161af3877db1|4102
bit4-rootcheck.json|fc3d73ad8c3b39eebe0e2d03d067df4d92433c40|58
bit4-subroots.jsonl|d7fdbb9e6091fa0cbad1abc809e517ff99e96794|4449
bit49-rootcheck.json|9a1286b108e1a457644c93de11c8cd5460193c9b|58
bit49-subroots.jsonl|9bdcd3e729bd80dd7bc9d7896ec2c0e4c74ad84e|4355
bit69-rootcheck.json|4b5788183b2e906a6c81e408441d82a01d000f1c|58
bit69-subroots.jsonl|22d9364ba923a013b0a93bf38e8eb62fd81672b5|4009
bit75-rootcheck.json|557e1003111550d526e367eebb9793d13b07870e|58
bit75-subroots.jsonl|bfbfd1691b2e6c0a121a4064cda2da385167635a|3942
bit79-rootcheck.json|4ee4ec7ec69589a26cd4add28c36767989f0bba5|58
bit79-subroots.jsonl|ed0d20e9c1ceab12a9926b0f63a102aaa6ef97cc|4766
bit9-rootcheck.json|67c2501c2eb524f99df0c84d12690b1bc8d6a791|58
bit9-subroots.jsonl|e3cc31b41f1d64ae40fac6b0717e207cd7e605aa|4875
class2-lane-cost78c-win7-certificates-20261117.json|b7fe519e923c6170e836f71e3f084f73219319d5|13545
det-reextraction.json|07e150ede079deb7d70a734d41ea5d1a49b00fea|180
n11_s7_0000000000000040380000000800000a.cert.part1of2|0c48d349d1afd89a684ec3b09ad4f45485cfd643|1178560
n11_s7_0000000000000040380000000800000a.cert.part2of2|4c241950e62f9605966e92bba74837d80b54c9ec|1178546
n11_s7_00000000000000403800000008000018.cert.part1of2|ccf4abca6a5cefb5be5134d1eb89d0d992246759|1192602
n11_s7_00000000000000403800000008000018.cert.part2of2|8fbd7b649e534f84496d3ebd283ab5e7f135752d|1192574
n11_s7_00000000000000403800000008000208.cert.part1of2|f0039318c23b3c6dce2c42aad7c8214fd36abfcf|1288082
n11_s7_00000000000000403800000008000208.cert.part2of2|4e00e0362a667ac0b0bb9eec2437a70df9611637|1288069
n11_s7_00000000000000403800000048000008.cert.part1of2|7b959b7289046742699fa6f048f372d862716298|885603
n11_s7_00000000000000403800000048000008.cert.part2of2|56c4b66c2a718537e90663448ba7c1cab2b3f30f|885532
n11_s7_00000000000000403802000008000008.cert.part1of2|fcd2c54a591a356bdb59a101ab252b3856e03df5|781285
n11_s7_00000000000000403802000008000008.cert.part2of2|65e344a1876d0a1aeda330c5d4cec6ada9787813|781262
n11_s7_00000000000000603800000008000008.cert.part1of2|6a18ea2db546bb4e4c8088ea151754c39a0bc398|620331
n11_s7_00000000000000603800000008000008.cert.part2of2|e0fc39f62f2664fc71957ce7a66b4d5acbb69a67|620312
n11_s7_00000000000008403800000008000008.cert.part1of2|5d4e8e013aa4074ce2ab6647fba63fa2f8c19c73|657085
n11_s7_00000000000008403800000008000008.cert.part2of2|933facdf8943420dfc2320802b047513afeb7e93|657034
n11_s7_00000000000080403800000008000008.cert.part1of2|0f0ad5e5ce2e594c534f127caa0adf61d82dbb16|883293
n11_s7_00000000000080403800000008000008.cert.part2of2|3467dcc2764570e42811130dc5b57a5dbec58dce|883263
n11_s7_00000010000000403800000008000008.cert.part1of2|4819c069deb821e5e707684e44866fd2d1404e47|983733
n11_s7_00000010000000403800000008000008.cert.part2of2|9c8d76689547a6f2c86dd6e2d1e177bb387ac60e|983681
n11_s7_00040000000000403800000008000008.cert.part1of2|5e701a594051edecb871abe777f352ba5beae492|1221325
n11_s7_00040000000000403800000008000008.cert.part2of2|3c7493b92ee9da667510a6e19b23df0ad7fa39eb|1221324
n11_s7_00100000000000403800000008000008.cert.part1of3|8ae9ee8651eef766e63a02263f7f02999089e18e|946728
n11_s7_00100000000000403800000008000008.cert.part2of3|e7327a6241edbcbb6cf5683c85dee4d72369bc3b|946688
n11_s7_00100000000000403800000008000008.cert.part3of3|397bfac28b2ea2f08d53e67c0a5ca80f1dbfe38b|946691
stats.json|70813ca75d3216d1836e408183c5d0db883e6cbc|3195
"""


def md5(b):
    return hashlib.md5(b).hexdigest()


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def git_blob_sha(b):
    return hashlib.sha1(b"blob %d\x00" % len(b) + b).hexdigest()


def d4_canon(h):
    """Independent D4 canonical form on the 11x11 board: min hex over the
    eight square symmetries. Asserted to be mutually distinct for the 11
    winner roots and disjoint from the claim's 12 confirmation root canons."""
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
    for line in PINS_TABLE.strip().splitlines():
        rel, sha, size = line.split("|")
        pins[rel] = (sha, int(size))
    assert len(pins) == 59, len(pins)
    return pins


def root_of_bit(bit):
    return f"{int(CHILD, 16) | (1 << bit):032x}"


def load_manifest():
    mb = open(os.path.join(MIRROR, MANIFEST_FILE), "rb").read()
    assert git_blob_sha(mb) == MANIFEST_BLOB_SHA, "manifest blob sha mismatch"
    m = json.loads(mb)
    assert m["schema"] == MANIFEST_SCHEMA, m["schema"]
    assert m["date"] == "2026-11-17"
    assert m["s5_parent_hex"] == "00000000000000403800000008000000"
    assert m["s6_child_hex"] == CHILD, m["s6_child_hex"]
    assert m["s6_s7_edge_cost"] == 78
    assert CLAIM_V3_BLOB_SHA in m["basis"], "manifest basis claim v3 blob"
    assert "UNKNOWN" in m["unknown_status"]
    recs = m["certificates"]
    assert [r["bit"] for r in recs] == EXPECTED_BITS, \
        [r["bit"] for r in recs]
    for r in recs:
        assert r["verdict"] == "WIN7" and r["depth"] == 10
        assert r["fbt_drops"] == 0 and r["fatal"] is None
        assert r["subroots"] == r["subroots_pass"] == r["loser_mobility"]
        assert r["union_missing"] == 0 and r["union_extra"] == 0
        assert r["terminal_stone_range"] == [13, 17], r["terminal_stone_range"]
        assert r["root"] == root_of_bit(r["bit"]), r["root"]
        assert r["file"] == f"n11_s7_{r['root']}.cert", r["file"]
        assert r["rows"] > 0 and r["extraction_nodes"] > 0
    t = m["totals"]
    assert t["certificates"] == len(recs) == EXPECTED
    assert t["rows"] == sum(r["rows"] for r in recs), t["rows"]
    assert t["extraction_nodes"] == sum(r["extraction_nodes"] for r in recs)
    assert t["fbt_drops_total"] == 0 and t["capped_per_move_total"] == 0
    return m, {r["bit"]: r for r in recs}, t


def load_stats():
    sb = open(os.path.join(MIRROR, STATS_FILE), "rb").read()
    assert git_blob_sha(sb) == STATS_BLOB_SHA, "stats blob sha mismatch"
    st = json.loads(sb)
    assert sorted(int(k) for k in st) == sorted(EXPECTED_BITS), sorted(st)
    return {int(k): v for k, v in st.items()}


def load_det():
    db = open(os.path.join(MIRROR, DET_FILE), "rb").read()
    assert git_blob_sha(db) == DET_BLOB_SHA, "det blob sha mismatch"
    d = json.loads(db)
    assert d["bits"] == [69, 116], d["bits"]
    return d


def load_claim():
    cb = open(os.path.join(CLAIM_DIR, CLAIM_FILE), "rb").read()
    assert git_blob_sha(cb) == CLAIM_BLOB_SHA, "claim v5 blob sha mismatch"
    claim = json.loads(cb)
    assert claim["schema"] == CLAIM_SCHEMA, claim["schema"]
    assert claim["s6_child"] == CHILD
    assert claim["s6_s7_edge_cost"] == 78
    assert claim["candidate_count"] == 78
    ae = claim["actual_execution"]
    win_bits = ae["win7_d10_bits"]
    assert sorted(win_bits) == sorted(EXPECTED_BITS), win_bits
    assert ae["certificate_extraction"].startswith("COMPLETE: 11/11"), \
        ae["certificate_extraction"][:40]
    assert ae["certificate_verification"].startswith(
        "COMPLETE: engine-free verification PASS on all 11"), \
        ae["certificate_verification"][:40]
    certs = claim["certificates"]
    assert certs["status"].startswith("complete: 11 WIN7-D10")
    assert certs["manifest"] == MANIFEST_FILE, certs["manifest"]
    assert certs["manifest_blob_sha"] == MANIFEST_BLOB_SHA, \
        certs["manifest_blob_sha"]
    assert certs["determinism_sample_bits"] == [69, 116]
    assert FOLLOWUP_SENTENCE in claim["next_action"], claim["next_action"][-120:]
    conf = claim["transfers"]
    assert sorted(int(k) for k in conf) == [5, 13, 14, 20, 34, 46, 97, 103,
                                            108, 110, 115, 118]
    conf_canons = {v["root_canon"] for v in conf.values()}
    assert len(conf_canons) == 12
    # claim v4 superseded by v5: provenance-only diff, certificates block
    # byte-identical (the v4 blob is pinned and cross-compared here)
    v4b = open(os.path.join(CLAIM_DIR, CLAIM_V4_FILE), "rb").read()
    assert git_blob_sha(v4b) == CLAIM_V4_BLOB_SHA, "claim v4 blob sha mismatch"
    v4 = json.loads(v4b)
    assert v4["schema"] == "n11-class2-lane-cost78c-inflight-20261118-v4"
    assert v4["certificates"] == certs, "v4/v5 certificates block differs"
    assert v4["actual_execution"]["win7_d10_bits"] == win_bits
    assert FOLLOWUP_SENTENCE in v4["next_action"]
    return claim, conf_canons, certs["totals"]


def run_verifier(path, mobility):
    p = subprocess.run([NODE, VERIFIER, path, str(mobility)],
                       capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def verify_one(bit, pins, rec, st):
    root_hex = root_of_bit(bit)
    assert rec["root"] == root_hex, ("manifest root", bit)
    assert rec["bit"] == bit
    base = f"n11_s7_{root_hex}.cert"
    three = bit == THREEPART_BIT
    suffixes = (["part1of3", "part2of3", "part3of3"] if three
                else ["part1of2", "part2of2"])
    parts = []
    joined = b""
    for suf in suffixes:
        rel = f"{base}.{suf}"
        pin = pins[rel]
        raw = open(os.path.join(MIRROR, rel), "rb").read()
        assert git_blob_sha(raw) == pin[0], ("pin sha mismatch", rel)
        assert len(raw) == pin[1], ("pin size mismatch", rel)
        assert raw.endswith(b"\n"), ("split part not on a line boundary", rel)
        joined += raw
        parts.append({"suffix": suf, "pinned_blob_sha": pin[0],
                      "bytes": pin[1]})
    storage = ("split part1of3+part2of3+part3of3 concatenation" if three
               else "split part1of2+part2of2 concatenation")
    # manifest storage kind cross-agreement
    exp_storage = (("split part1of3/part2of3/part3of3 + README-split-bit%d.md"
                    % bit) if three else
                   ("split part1of2/part2of2 + README-split-bit%d.md" % bit))
    assert rec["storage"] == exp_storage, ("manifest storage", bit,
                                          rec["storage"])
    assert rec["file"] == base, ("manifest file", bit)
    # README-split recombination doc
    rd = f"README-split-bit{bit}.md"
    assert rd in pins
    txt = open(os.path.join(MIRROR, rd), "rb").read().decode()
    mm = re.search(r"is (\d+) bytes and is published as "
                   + ("three parts" if three else "two parts"), txt)
    assert mm, ("README split bytes", bit)
    assert int(mm.group(1)) == len(joined), ("README whole bytes", bit)
    mm = re.search(r"md5sum .*?#\s*([0-9a-f]{32})", txt)
    assert mm and mm.group(1) == md5(joined), ("README md5", bit)
    if three:
        mm = re.search(r"line boundaries \(bytes (\d+) and (\d+)\)", txt)
        assert mm, ("README split boundaries", bit)
        b1, b2 = int(mm.group(1)), int(mm.group(2))
        assert b1 == parts[0]["bytes"], ("README boundary1", bit)
        assert b2 == parts[0]["bytes"] + parts[1]["bytes"], \
            ("README boundary2", bit)
    else:
        mm = re.search(r"line boundary \(byte (\d+)\)", txt)
        assert mm and int(mm.group(1)) == parts[0]["bytes"], \
            ("README split boundary", bit)
    mm = re.search(r"^root `([0-9a-f]{32})`", txt, re.M)
    assert mm and mm.group(1) == root_hex, ("README root", bit)
    # header + data-row accounting
    lines = joined.decode().splitlines()
    assert lines[0] == ("n11-terminal-strategy-v1 original_first_WIN7 "
                       "second_to_move_LOSS"), ("header", bit)
    assert lines[1] == f"root {root_hex}", ("root line", bit)
    n_rows = len(lines) - 2
    # manifest record cross-agreement (rows/md5/sha256/d4 canon/etc.)
    assert rec["verdict"] == "WIN7" and rec["depth"] == 10
    assert rec["rows"] == n_rows, ("manifest rows", bit)
    assert rec["md5"] == md5(joined), ("manifest md5", bit)
    assert rec["sha256"] == sha256(joined), ("manifest sha256", bit)
    assert rec["fbt_drops"] == 0 and rec["fatal"] is None
    assert rec["union_missing"] == 0 and rec["union_extra"] == 0
    assert rec["subroots"] == rec["subroots_pass"] == rec["loser_mobility"]
    assert rec["terminal_stone_range"] == [13, 17]
    got_canon = d4_canon(root_hex)
    assert rec["d4_canon_root"] == got_canon, ("manifest d4 canon", bit)
    assert rec["raw_is_canon"] == (root_hex == got_canon), \
        ("manifest raw_is_canon", bit)
    # stats.json per-bit cross-agreement
    assert st["root"] == root_hex, ("stats root", bit)
    assert st["rows"] == n_rows, ("stats rows", bit)
    assert st["nodes"] == rec["extraction_nodes"], ("stats nodes", bit)
    assert st["md5"] == md5(joined), ("stats md5", bit)
    assert st["sha256"] == sha256(joined), ("stats sha256", bit)
    assert st["size"] == len(joined), ("stats size", bit)
    assert st["fbt_drops"] == 0, ("stats fbt_drops", bit)
    # sidecar: rootcheck.json is a two-line JSONL
    rc_rel = f"bit{bit}-rootcheck.json"
    rc_lines = [json.loads(l) for l in
                open(os.path.join(MIRROR, rc_rel), "rb").read()
                .decode().strip().splitlines()]
    assert len(rc_lines) == 2, ("rootcheck lines", bit)
    assert rc_lines[0]["stones"] == 7, ("rootcheck stones", bit)
    mobility = rc_lines[0]["loserMobility"]
    assert rc_lines[1]["rows"] == n_rows, ("rootcheck rows", bit)
    assert mobility == rec["loser_mobility"] == st["moves"], \
        ("mobility vs manifest/stats", bit)
    # sidecar: subroots.jsonl is BATCHED
    sr_rel = f"bit{bit}-subroots.jsonl"
    sr_lines = [json.loads(l) for l in
                open(os.path.join(MIRROR, sr_rel), "rb").read()
                .decode().strip().splitlines()]
    stats = {}
    for l in sr_lines:
        assert l["rows"] == n_rows, ("subroots line rows", bit)
        for k, s in l["stats"].items():
            assert k not in stats, ("duplicate subroot key", bit, k)
            stats[k] = s
    assert len(stats) == mobility, ("subroots key count", bit)
    for k, s in stats.items():
        assert 13 <= s["range"][0] and s["range"][1] <= 17, \
            ("subroots range", bit, k)
    # BigInt independent verifier (third implementation beyond the
    # extractor's Bareiss verify)
    tmp = os.path.join(ROOT, f"scratch_reverify_cost78c_{bit}.cert")
    with open(tmp, "wb") as fh:
        fh.write(joined)
    rc, out, err = run_verifier(tmp, mobility)
    os.unlink(tmp)
    assert rc == 0, ("verifier nonzero", bit, err[:300])
    v = json.loads(out)
    assert v["verdict"] == "WIN7 certificate independently verified"
    assert v["root_hex"] == root_hex, ("root_hex", bit)
    assert v["root_stones"] == 7 and v["root_safe"] is True
    assert v["rows_sorted_unique"] is True
    assert v["union_missing"] == 0 and v["union_extra"] == 0
    assert v["strategy_rows"] == n_rows, ("rows", bit)
    assert v["consumed_winner_rows"] == n_rows, ("consumed rows", bit)
    assert v["subroots_passed"] == mobility, ("subroots", bit)
    assert v["root_mobility"] == mobility, ("mobility", bit)
    assert 13 <= v["terminal_range"][0] and v["terminal_range"][1] <= 17, \
        ("terminal range", bit)
    # sidecar sums == verifier sums (Bareiss-generated stats vs BigInt
    # verifier: third-implementation field agreement)
    assert sum(s["seen"] for s in stats.values()) == \
        v["visited_states_across_subroots"], ("subroots seen sum", bit)
    assert sum(s["terminals"] for s in stats.values()) == \
        v["terminal_count"], ("subroots terminals sum", bit)
    assert sum(s["opponentEdges"] for s in stats.values()) == \
        v["loser_reply_edges"], ("subroots opponentEdges sum", bit)
    entry = {
        "bit": bit, "root_hex": root_hex, "d4_canon_root": got_canon,
        "raw_is_canon": root_hex == got_canon,
        "certificate": base, "storage": storage,
        "record_source": ("research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/"
                          + BAND_DIR + "/ (in-band manifest "
                          + MANIFEST_FILE + " + per-bit sidecars: README-split-bitN.md + "
                          "bitN-rootcheck.json + bitN-subroots.jsonl + certificate parts)"),
        "record_kind": ("win7-certificates in-band manifest record + per-bit sidecars "
                        "+ sweep claim v5 (win7_d10_bits/s6_child/certificates COMPLETE)"),
        "joined_bytes": len(joined),
        "joined_md5": md5(joined),
        "joined_sha256": sha256(joined),
        "joined_git_blob_sha": git_blob_sha(joined),
        "readme_split_md5_match": True,
        "manifest_record_agreement": True,
        "manifest_record": {
            "bit": rec["bit"], "root": rec["root"], "verdict": rec["verdict"],
            "depth": rec["depth"], "rows": rec["rows"],
            "extraction_nodes": rec["extraction_nodes"],
            "subroots": rec["subroots"], "loser_mobility": rec["loser_mobility"],
            "d4_canon_root": rec["d4_canon_root"],
            "raw_is_canon": rec["raw_is_canon"],
            "md5": rec["md5"], "sha256": rec["sha256"],
            "file": rec["file"], "storage": rec["storage"],
        },
        "stats_record_agreement": True,
        "record_rows": n_rows,
        "record_extraction_nodes": rec["extraction_nodes"],
        "rootcheck_stones": rc_lines[0]["stones"],
        "rootcheck_loser_mobility": mobility,
        "subroots_sidecar_lines": len(sr_lines),
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
        "parts": parts,
        "readme_split_doc": {
            "bytes": len(joined),
            "split_boundaries": ([parts[0]["bytes"], parts[0]["bytes"] + parts[1]["bytes"]]
                                 if three else [parts[0]["bytes"]]),
            "md5": md5(joined),
        },
    }
    return entry, v


def main():
    vsrc = open(VERIFIER, "rb").read()
    assert git_blob_sha(vsrc) == VERIFIER_BLOB_SHA, "verifier blob sha mismatch"
    pins = load_pins()
    manifest, rec_by_bit, mtotals = load_manifest()
    stats = load_stats()
    det = load_det()
    claim, conf_canons, ctotals = load_claim()
    assert ctotals == mtotals, ("claim v5 certificates totals != manifest",
                               ctotals, mtotals)
    # every root = child | (1 << bit)
    for bit in EXPECTED_BITS:
        assert root_of_bit(bit) in "".join(
            open(os.path.join(MIRROR, "README-split-bit%d.md" % bit),
                 "rb").read().decode()), ("root not in README", bit)
    roots = [root_of_bit(b) for b in EXPECTED_BITS]
    assert len(set(roots)) == len(roots), "duplicate root across bits"
    entries = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
        futs = {ex.submit(verify_one, b, pins, rec_by_bit[b], stats[b]): b
                for b in EXPECTED_BITS}
        for fut in concurrent.futures.as_completed(futs):
            e, _ = fut.result()
            entries.append((futs[fut], e))
    entries.sort(key=lambda t: t[0])

    assert len(entries) == EXPECTED
    total_rows = sum(e["verifier_rows"] for _, e in entries)
    total_sub = sum(e["verifier_subroots_passed"] for _, e in entries)
    total_bytes = sum(e["joined_bytes"] for _, e in entries)
    n_three = sum(1 for _, e in entries
                  if e["storage"].startswith("split part1of3"))
    # manifest totals cross-agreement with the bytes recomputed here
    assert total_rows == mtotals["rows"], (total_rows, mtotals["rows"])
    assert total_bytes == mtotals["published_bytes"], \
        (total_bytes, mtotals["published_bytes"])
    assert sum(e["record_extraction_nodes"] for _, e in entries) == \
        mtotals["extraction_nodes"]
    # stats.json totals cross-agreement
    assert sum(s["rows"] for s in stats.values()) == mtotals["rows"]
    assert sum(s["nodes"] for s in stats.values()) == \
        mtotals["extraction_nodes"]
    assert sum(s["size"] for s in stats.values()) == \
        mtotals["published_bytes"]
    # det-reextraction.json cross-agreement: the published fresh-process
    # determinism md5s equal the joined md5s recomputed from the pinned bytes
    e_by = dict(entries)
    for dbit in det["bits"]:
        assert f"bit {dbit}: {e_by[dbit]['joined_md5']}" in det["result"], \
            ("det md5 mismatch", dbit)

    # cross-batch disjointness against the 183 earlier BigInt-verified roots
    earlier_roots, earlier_canons = set(), set()
    for fn, blob, n in EARLIER_BATCHES:
        b = open(os.path.join(EARLIER_DIR, fn), "rb").read()
        assert git_blob_sha(b) == blob, ("earlier batch pin", fn)
        d = json.loads(b)
        es = d["entries"]
        assert len(es) == n, (fn, len(es))
        for e in es:
            earlier_roots.add(e["root_hex"])
            earlier_canons.add(d4_canon(e["root_hex"]))
    assert len(earlier_roots) == 183, len(earlier_roots)
    ov = set(roots) & earlier_roots
    assert not ov, ("root overlap with the 183 earlier records", sorted(ov))
    canons = [e["d4_canon_root"] for _, e in entries]
    assert len(set(canons)) == len(canons), "duplicate D4 canon in-batch"
    ovc = set(canons) & earlier_canons
    assert not ovc, ("D4 canon overlap with the 183 earlier records",
                     sorted(ovc))
    # winner canons disjoint from the claim's 12 confirmation root canons
    ovcf = set(canons) & conf_canons
    assert not ovcf, ("D4 canon overlap with confirmation canons", sorted(ovcf))
    doc = {
        "schema": ("n11-class2-lane-cost78c-certificates-bigint-"
                   "independent-reverification-20261117-v1"),
        "date": "2026-11-17",
        "pin": {
            "commit": PIN,
            "band_commits": ("b359756fef..97650e276e (per-bit certificate commits: "
                             "bit69 at b359756fef, bit75 at 7230700071, bit49 at "
                             "2b41affd71/651fe837f7, bit30 at 178af8c5db/a531922c0b, "
                             "bit79 at 49afd359fe/d30ef26c1f, bit100 at "
                             "8a08d83afb/bfa60c76ba, bit9 at 76d66ffbf6/0152df7fb9, "
                             "bit114 at 2a00d54c66/7fd24f62df, bit1 at "
                             "45579b5830/2684abe21d, bit4 at 9ebba114d1/81457db870, "
                             "bit116 at 59447c2d37/628b6d8c0d/97650e276e)"),
            "manifest_lane_commits": ("3ed406e339ef82e8fdb7aadcb2e8da0ddd26189a "
                                      "(in-band manifest + claim v4) / "
                                      "eb157af2be0f35f58446ab1f5923c1c712dc1043 "
                                      "(stats.json + det-reextraction.json) / "
                                      "1687397338a89a489263c12f41780e1182f18b9c "
                                      "(claim v5 pin-provenance correction; the "
                                      "listing pin commit)"),
            "record_files": ("research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/"
                             + BAND_DIR + "/ (59 files: 11x README-split-bitN.md, 11x "
                             "bitN-rootcheck.json, 11x bitN-subroots.jsonl, 23 certificate "
                             "parts: ten part1of2/part2of2 pairs + one part1of3/part2of3/"
                             "part3of3 triple, the in-band manifest "
                             + MANIFEST_FILE + ", stats.json, det-reextraction.json) + "
                             "the sweep claim v5 " + CLAIM_FILE
                             + " (and the superseded claim v4, provenance-compared)"),
            "authoritative_blob_sha_table": ("the GitHub API contents listing of the band dir "
                                             "at the pin commit " + PIN + " (59 files, "
                                             "name|git blob sha|size, embedded verbatim as "
                                             "PINS_TABLE and asserted 59/59 against the "
                                             "mirrored bytes) + the claim v5 pin (60th) + "
                                             "the claim v4 pin (61st); the nine earlier "
                                             "batch outputs used for disjointness are "
                                             "blob-pinned inline (183 earlier roots)"),
        },
        "method": {
            "records": ("11 WIN7-D10 certificate records of the published cost-78c band "
                        "(child " + CHILD + ", edge cost 78, sweep claim v5 blob "
                        + CLAIM_BLOB_SHA + " over the provenance-superseded v4 blob "
                        + CLAIM_V4_BLOB_SHA + " whose certificates block is asserted "
                        "identical): the record set is the in-band manifest "
                        + MANIFEST_FILE + " (blob " + MANIFEST_BLOB_SHA + ", schema "
                        + MANIFEST_SCHEMA + ", basis pinned to the sweep claim v3 blob "
                        + CLAIM_V3_BLOB_SHA + ") cross-agreed per record with the "
                        "per-bit sidecar family (README-split-bitN.md recombination doc: "
                        "whole-file byte size, split boundary byte(s), whole-file md5, "
                        "root; bitN-rootcheck.json two-line JSONL: stones/loserMobility/"
                        "rows; bitN-subroots.jsonl batched per-loser-first-move Bareiss "
                        "stats) and with stats.json (per-bit root/rows/nodes/moves/md5/"
                        "sha256/size/fbt_drops); the sweep claim v5 "
                        "(win7_d10_bits == [1,4,9,30,49,69,75,79,100,114,116], s6_child, "
                        "candidate_count 78, certificates COMPLETE with manifest_blob_sha "
                        "and totals equal to the manifest's) is cross-agreed at load; "
                        "every root asserted == child | (1<<bit)"),
            "bytes": ("each certificate part mirrored from the commit-pinned raw CDN URLs "
                      "(pin " + PIN + "), git blob sha+size asserted 59/59 against the "
                      "embedded GitHub-listing pin table; split parts asserted to end on "
                      "line boundaries and the boundary byte(s) to equal the README-split "
                      "stated values; certificates reconstructed as exact concatenations; "
                      "joined md5+sha256 asserted against both the README-split md5 and "
                      "the manifest record md5/sha256; 2-line header asserted and data "
                      "rows == rootcheck rows == manifest rows == stats rows"),
            "verifier": ("verify_win7_certificate_bigint_independent.mjs (git blob "
                         + VERIFIER_BLOB_SHA + ", asserted by the script; run with the "
                         "rootcheck loserMobility as argv[3]): BigInt 3x3 cofactor expansion "
                         "of the exact lifted determinant [x^2+y^2,x,y,1], no floating "
                         "point, no solver/verdict-cache import; third implementation beyond "
                         "the extractor's own Bareiss verify_bit7_win7_cert.ts run per "
                         "verify_cost78c_one.sh; per certificate asserted "
                         "verdict/root_hex/stones 7/root_safe/rows sorted-unique/union 0/0/"
                         "terminal range within 13..17/strategy_rows/subroots_passed=="
                         "root_mobility/consumed_winner_rows"),
            "sidecar_cross_agreement": ("per-bit subroots.jsonl (Bareiss-verified per-"
                                        "loser-first-move stats, batched 8 per line) sums "
                                        "fully agree with the BigInt verifier output on all "
                                        "11 certificates: sum(seen)==visited_states_across_"
                                        "subroots, sum(terminals)==terminal_count, "
                                        "sum(opponentEdges)==loser_reply_edges, m-key count=="
                                        "subroots_pass==loser_mobility==manifest loser_mobility=="
                                        "stats moves, every per-move range within [13,17]; "
                                        "rootcheck.json line 1 stones==7 and loserMobility=="
                                        "verifier root_mobility, line 2 rows==data rows"),
            "det_reextraction_agreement": ("det-reextraction.json (blob " + DET_BLOB_SHA
                                           + "): the published fresh-process re-extraction "
                                           "determinism md5s of bits [69, 116] equal the "
                                           "joined md5s recomputed here from the pinned "
                                           "certificate bytes"),
        },
        "entries": [e for _, e in entries],
        "cross_checks": {
            "independent_d4_canon_all_11_records": ("an in-script D4 canonicalization "
                                                    "implementation (min hex over the eight "
                                                    "square symmetries of the 11x11 board) "
                                                    "computes every record's d4_canon_root; "
                                                    "all 11 equal the manifest record "
                                                    "d4_canon_root fields; the 11 D4 canons "
                                                    "are mutually distinct and disjoint "
                                                    "from the claim v5's 12 confirmation "
                                                    "root_canons (the claim's "
                                                    "winner_canons_distinct_from_confirmation_"
                                                    "canons statement re-derived "
                                                    "independently for the 11 winner roots)"),
            "cross_batch_root_disjointness": ("all 11 root_hex distinct in-batch and disjoint "
                                              "from the 183 root_hex values of the nine "
                                              "earlier independently re-verified batches "
                                              "(single-file 43 + split-part bands 18 + "
                                              "split-part sweepbands 24 + 66j/69j 15 + 63cd 2 "
                                              "+ 72d 11 + 73j 16 + 73k 22 + 73l 32), asserted "
                                              "at load against the blob-pinned published batch "
                                              "outputs; D4-canon disjoint against the computed "
                                              "canons of all 183 earlier roots"),
            "manifest_totals_cross_agreement": ("the manifest totals (11 certificates / "
                                                "614,003 rows / 77,967,826 extraction nodes / "
                                                "22,223,603 published bytes / 0 fbt_drops_total / "
                                                "0 capped_per_move_total) equal the sums "
                                                "recomputed here from the pinned bytes and the "
                                                "BigInt verifier outputs, and equal the claim "
                                                "v5 certificates.totals block"),
            "stats_and_det_cross_agreement": ("stats.json per-bit root/rows/nodes/moves/md5/"
                                               "sha256/size/fbt_drops agree with both the "
                                               "manifest records and the bytes recomputed "
                                               "here; det-reextraction.json's bits [69,116] "
                                               "md5s equal the recomputed joined md5s"),
            "claim_v4_v5_provenance_diff": ("claim v5 (blob " + CLAIM_BLOB_SHA + ") supersedes "
                                            "v4 (blob " + CLAIM_V4_BLOB_SHA + ") by a "
                                            "pin-provenance-only correction (the parallel "
                                            "batches-1-6 audit republication); both blobs "
                                            "pinned here and the certificates block asserted "
                                            "identical between them; both next_action fields "
                                            "name this batch's work as the optional follow-up"),
            "beyond_publication_lane": ("the 78c publication's own verification "
                                        "(verify_bit7_win7_cert.ts, engine-free Bareiss, via "
                                        "verify_cost78c_one.sh) is documented in the per-bit "
                                        "commits, the in-band manifest, stats.json and "
                                        "det-reextraction.json; this batch adds the "
                                        "third-implementation BigInt verifier per certificate, "
                                        "the 61-file pin assertion from the GitHub listing "
                                        "(59 band files + claim v5 + claim v4), and the "
                                        "manifest/stats/det/claim cross-agreement; it "
                                        "implements the optional follow-up named in the "
                                        "claim v4/v5 next_action"),
        },
        "summary": {
            "records": len(entries),
            "file_pins_asserted": 61,
            "three_part_split_certificates": n_three,
            "two_part_split_certificates": len(entries) - n_three,
            "whole_certificates": 0,
            "verifier_pass": len(entries),
            "verifier_fail": 0,
            "readme_md5_mismatch": 0,
            "pin_blob_sha_mismatch": 0,
            "sidecar_cross_agreement_fail": 0,
            "manifest_cross_agreement": "11/11",
            "stats_cross_agreement": "11/11",
            "det_reextraction_cross_agreement": True,
            "total_rows_independently_verified": total_rows,
            "total_sub_roots_independently_verified": total_sub,
            "total_certificate_bytes_rehashed": total_bytes,
            "total_extraction_nodes_manifest_agreed": mtotals["extraction_nodes"],
            "earlier_bigint_verified_records_covered": 183,
            "bytes_reverified_population_after_this_batch": 392,
            "per_bit_loser_mobility": {str(b): e["rootcheck_loser_mobility"]
                                       for b, e in entries},
        },
        "interpretation_guard": [
            ("this re-verification upgrades the 11 certificates of the published cost-78c "
             "band to bytes-level, third-implementation independently re-verified evidence "
             "with full in-band manifest/stats/determinism-record/claim cross-agreement; the "
             "bytes-re-verified population of this experiment stands at 381 + 11 = 392 "
             "records (counting per the 72d/73k batch bookkeeping); it does not change any "
             "frontier number and closes no manifest row"),
            ("the cost-78c receipt fold stays pending behind the 66i/66j/69j/71e/72d/73i/73j/"
             "73k/73l folds managed by their own lanes; no manifest row is closed by this "
             "re-verification"),
            ("a WIN7-D10 certificate proves only that its individual 7-stone root is a "
             "first-player win within depth 10"),
            ("the 67 REFUTED-D10 bits of the cost-78c sweep are NOT LOSS proofs of those roots"),
            ("11x11 empty board, two-stone roots {49,60} and {59,60}, S2 {59,60}, class 1, "
             "class 2 and class 4 all remain UNKNOWN"),
        ],
    }
    with open(OUT, "w") as fh:
        json.dump(doc, fh, indent=1, sort_keys=False)
        fh.write("\n")
    print(json.dumps(doc["summary"], indent=1))


if __name__ == "__main__":
    main()
