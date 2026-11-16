#!/usr/bin/env python3
"""Independent bytes-level re-verification of the 83 WIN7-D10 certificates of
the eight remaining receipts-recompute bands of the head-1452 basis
(cost-60c, 63h, 63i, 63j, 65m, 67d, 69e, 70g), against their per-record
documentation and the BigInt independent verifier.

Run from the working mirror directory of
yuubinnkyoku/kyouen-researches @ main commit b27c0b5d2efbaa3dc4d471e59ffc27807fe0015e
with the eight band certificate directories mirrored under certs/ via
commit-pinned raw URLs:

  BASE=https://raw.githubusercontent.com/yuubnnkyoku/.../<PIN>/research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output
  (each class2-lane-cost<band>-certificates/*.cert fetched to certs/)

Steps (all asserted):
 1. load the record sources:
      - receipts-recompute per-entry records (rows/md5/sub_roots_pass) for
        60c (1), 63h (1), 63i (18), 63j (29), 65m (8), 67d (1);
      - class2-lane-cost69e-win7-certificates-20261114.json (10 records,
        md5/sha256 of the published certificate bytes; bit 116 documents the
        hashes of the UNCOMPRESSED certificate, published as
        base64(gzip-9) .cert.gz.b64);
      - class2-lane-cost70g-win7-certificates-20261115.json manifest (8
        records: strategy_rows / verify.subroots_passed / repo_blob_sha) plus
        class-frontier-cost70g-receipts-recompute-20261116.json (7 records
        with rows/md5/sub_roots_pass) -> 15 records;
    total 83 records, all distinct (band, bit) and all distinct root_hex;
 2. assert each mirrored certificate file's git blob sha and size against
    the authoritative GitHub directory listing of the pinned commit
    (83/83 pin table embedded below, fields=name/sha/size);
 3. assert md5 against every record that documents one (75 records; the eight
    70g-manifest records document no md5 - their computed md5 is recorded
    here as a new independent datum); for 69e bit 116 additionally decode
    base64, gunzip, and assert the uncompressed bytes/md5/sha256 against the
    record before verification;
 4. run the BigInt independent verifier
    (verify_win7_certificate_bigint_independent.mjs, git blob
    62b5d9413daafb172f6e10249976ee6808f7b454, byte-exact local copy: BigInt
    3x3 cofactor expansion, no floating point, no solver/verdict-cache
    import) once per certificate; assert verdict, root stones 7, root_safe,
    rows sorted-unique, union missing/extra 0/0, terminal range within
    13..17, strategy_rows == record rows, subroots_passed == record
    sub_roots_pass, and root_hex == record root_hex;
 5. cross-checks:
      - cost-60c win7 manifest published_cert whole_bytes/whole_md5/
        whole_sha256/git_blob_sha and sub_roots/terminal_count;
      - cost-70g manifest loser_first_moves/verify blocks
        (terminal_range, terminal_count, visited_states,
        loser_reply_edges) for the 8 manifest bits, and the cost-70g
        receipts-recompute-20261115 rows/sub_roots_pass for the same 8 bits;
      - cost-69e 10cert python independent audit totals (strategy_rows
        411114, subroots 535) against the per-record verifier sums;
 6. write the deterministic re-verification JSON to the output path.

Determinism: no timestamps, no wall times, fixed record order; running
twice must produce byte-identical output.
11x11 empty board remains UNKNOWN; WIN7 certificates prove only
individual 7-stone roots within depth 10.
"""
import concurrent.futures, hashlib, json, os, subprocess

PIN = "b27c0b5d2efbaa3dc4d471e59ffc27807fe0015e"
EXP = "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113"
OUTD = f"{EXP}/output"
VERIFIER = f"{EXP}/scripts/verify_win7_certificate_bigint_independent.mjs"
NODE = "node"
MIRROR = os.environ.get("REVERIFY_MIRROR", OUTD)
OUT = f"{OUTD}/class2-lane-receipts-recompute-bands-certificates-bigint-independent-reverification-20261117.json"

# Authoritative GitHub directory listing at PIN (fields name|sha|size),
# one line per certificate file under the eight band certificate dirs.
PINS = """class2-lane-cost60c-certificates/bit92-root-00000000100000003800000008008020.cert|b35128897b07f03e4baa11583423453cb378e18d|996758
class2-lane-cost63h-certificates/bit89-root-00000000020000801202000040080000.cert|083360fcf638ca594712b8fefd4714a0d15964db|941299
class2-lane-cost63i-certificates/bit105-root-00000200000000c09002000001000000.cert|13f2a871cd93ea18e9f8086e3bfb66d2e52a10f3|1428671
class2-lane-cost63i-certificates/bit107-root-00000800000000c09002000001000000.cert|d8d4550f6909477486c55a3a0eaff5793f7cfdbb|1400753
class2-lane-cost63i-certificates/bit112-root-00010000000000c09002000001000000.cert|304ebd7e917e70e8486d835ad487b3ec109ccf20|1222486
class2-lane-cost63i-certificates/bit114-root-00040000000000c09002000001000000.cert|5fddeb77d21021f7484671cec84ab16f76c505d9|1848333
class2-lane-cost63i-certificates/bit116-root-00100000000000c09002000001000000.cert|ff0237aa6db306fc6f9d525c56c5c9e99497525d|1314893
class2-lane-cost63i-certificates/bit119-root-00800000000000c09002000001000000.cert|43228479f5e982f572f67f9ea680faae859f5249|1380699
class2-lane-cost63i-certificates/bit120-root-01000000000000c09002000001000000.cert|fb7b0edbdd816cd6620508eebc6126ef35c763f5|1072823
class2-lane-cost63i-certificates/bit30-root-00000000000000c09002000041000000.cert|dc2cc776319d8aa546c622801ad74fda307567cc|785624
class2-lane-cost63i-certificates/bit32-root-00000000000000c09002000101000000.cert|50022b9709fc907b6b8225909250e7fcc36c87da|1701420
class2-lane-cost63i-certificates/bit41-root-00000000000000c09002020001000000.cert|a50c71b7bb3515e6d1041d0fd444caa5b539f54d|1184369
class2-lane-cost63i-certificates/bit45-root-00000000000000c09002200001000000.cert|82ebcbf4fe49f1f3d17fffcebc265b866cb8903a|1873301
class2-lane-cost63i-certificates/bit54-root-00000000000000c09042000001000000.cert|1394212565edec2e283c78368bb7b3d38e6aa473|1238074
class2-lane-cost63i-certificates/bit61-root-00000000000000c0b002000001000000.cert|cba40bb4d0baa952dee4aaf1a56d6c7f67152210|579820
class2-lane-cost63i-certificates/bit62-root-00000000000000c0d002000001000000.cert|339dc8dc70d58ac42cc3f3d9bb48371e011c6c8c|1147831
class2-lane-cost63i-certificates/bit66-root-00000000000000c49002000001000000.cert|d0bbeb245a4ffc888622558f8cac14d8573c7685|1312363
class2-lane-cost63i-certificates/bit77-root-00000000000020c09002000001000000.cert|63810c9206f95a97fac6cb2cda6041550099890a|1852733
class2-lane-cost63i-certificates/bit81-root-00000000000200c09002000001000000.cert|0f61971ce9c869db53a4080c4be9a48e03166e9e|679134
class2-lane-cost63i-certificates/bit99-root-00000008000000c09002000001000000.cert|70ef6d9eec4ec9fd77654304c99253495b7ee7b0|1362293
class2-lane-cost63j-certificates/bit1-root-00000000040000003800000048000002.cert|05ae68bfba1f592793cb34a6f9ed4aed5eee9a81|1071469
class2-lane-cost63j-certificates/bit102-root-00000040040000003800000048000000.cert|b7ae7afa4a46f285f7b4ca73c81ee1fd56611882|979534
class2-lane-cost63j-certificates/bit103-root-00000080040000003800000048000000.cert|3599cb1b9fd53a0803ee363801a3ee8553a0715c|1090362
class2-lane-cost63j-certificates/bit105-root-00000200040000003800000048000000.cert|7d65ef9485d21dcc81f5c27fe578156bfd5cd0cd|1422637
class2-lane-cost63j-certificates/bit107-root-00000800040000003800000048000000.cert|72c2b2cdb0f01cd520e8fe09e9f4c60a6532f3b1|771828
class2-lane-cost63j-certificates/bit11-root-00000000040000003800000048000800.cert|1f55518fd6cc59edbf5b87175f52f5275f409ab2|1577998
class2-lane-cost63j-certificates/bit113-root-00020000040000003800000048000000.cert|03578640bb2a00ce2e166361638bcae5ede736ca|1523425
class2-lane-cost63j-certificates/bit16-root-00000000040000003800000048010000.cert|06c2dbd46e2c4ca2eb83144dccd727c7e3483ec8|1853141
class2-lane-cost63j-certificates/bit17-root-00000000040000003800000048020000.cert|a028b75498700369254019799a49162e4ce0657b|812179
class2-lane-cost63j-certificates/bit18-root-00000000040000003800000048040000.cert|7af8f1d6cd6dbbd4df5afd1be121e956b7a5332a|1149373
class2-lane-cost63j-certificates/bit3-root-00000000040000003800000048000008.cert|8fecaacf03c94bea641f7003ced831a95a6b7365|978753
class2-lane-cost63j-certificates/bit34-root-00000000040000003800000448000000.cert|232b0a4fd9ce7fb8ea70f3371b6a81e4f142df0b|1311264
class2-lane-cost63j-certificates/bit35-root-00000000040000003800000848000000.cert|e57e19522c888d11d13ae28d762b9b3aa4854ec0|1057925
class2-lane-cost63j-certificates/bit4-root-00000000040000003800000048000010.cert|8e8dd34cfc9b8546b2de5940e89761185b23a1e6|1330097
class2-lane-cost63j-certificates/bit44-root-00000000040000003800100048000000.cert|07753192e16dc390a645cc1007985f53d39bb324|1689382
class2-lane-cost63j-certificates/bit45-root-00000000040000003800200048000000.cert|35b42d5675cb3fd2fa53484ef6026884183ac78d|1544465
class2-lane-cost63j-certificates/bit52-root-00000000040000003810000048000000.cert|53a2b47c5ecdd77df9e2be5e211618a500d2dfc5|1116491
class2-lane-cost63j-certificates/bit54-root-00000000040000003840000048000000.cert|bdfc71da547f34487825c9ac448f842ce7b80b13|1018950
class2-lane-cost63j-certificates/bit68-root-00000000040000103800000048000000.cert|eeadae0a4a736e99882d316b787c2fd8b3a5f5d2|937872
class2-lane-cost63j-certificates/bit7-root-00000000040000003800000048000080.cert|243997ad0cdf19b5f1c3efe3dda54b1e959ff70d|1416352
class2-lane-cost63j-certificates/bit73-root-00000000040002003800000048000000.cert|276412d7609f92ea5880817de015d8d50fdf4173|710043
class2-lane-cost63j-certificates/bit78-root-00000000040040003800000048000000.cert|c94818a7208c0563c87f2d287848d862eae343ef|1428311
class2-lane-cost63j-certificates/bit81-root-00000000040200003800000048000000.cert|cef888628053de69e1820da8852a20b14ca68717|1274585
class2-lane-cost63j-certificates/bit87-root-00000000048000003800000048000000.cert|98d22599f2ac1a18aea30cb7fea5085fb77d4732|1509157
class2-lane-cost63j-certificates/bit88-root-00000000050000003800000048000000.cert|321acae44ffb386976a9de5d4d4d24c4b2fe7d91|1686457
class2-lane-cost63j-certificates/bit9-root-00000000040000003800000048000200.cert|c39bf4383a375cf64f27abcb4c6d05413f43a8e8|1131634
class2-lane-cost63j-certificates/bit92-root-00000000140000003800000048000000.cert|e4020fc5857a71adada4a3a05e0fe48825478a3d|1697030
class2-lane-cost63j-certificates/bit93-root-00000000240000003800000048000000.cert|a49af7270c05f5679a5027682189ee6831e032a9|359605
class2-lane-cost63j-certificates/bit99-root-00000008040000003800000048000000.cert|b2c7a83f7dea7d09dfbe050603fc52dce5b85dea|1665014
class2-lane-cost65m-certificates/bit21-root-00000000000000801202000040201000.cert|a32b6ab429a2eba260bfb971aefc7d7badc054d8|1112908
class2-lane-cost65m-certificates/bit22-root-00000000000000801202000040401000.cert|054e0d21f78f17c5067099d6c013d6e21ff74ffc|1338091
class2-lane-cost65m-certificates/bit28-root-00000000000000801202000050001000.cert|b5d53418434f1b11c70bb6e4fa6f34f54f2081f1|1817561
class2-lane-cost65m-certificates/bit35-root-00000000000000801202000840001000.cert|52ff3c4042c0b8c20903b22a85a81cf4010df355|1628812
class2-lane-cost65m-certificates/bit44-root-00000000000000801202100040001000.cert|40784da7ce7a5808d450a2264913bcf1709ebb9f|1692938
class2-lane-cost65m-certificates/bit67-root-00000000000000881202000040001000.cert|6c8458b6bcdb5b2cea652ff52f394896d0e980f0|1122421
class2-lane-cost65m-certificates/bit76-root-00000000000010801202000040001000.cert|66aec3b5218d45a6a34f080a9f98854696555156|1780309
class2-lane-cost65m-certificates/bit83-root-00000000000800801202000040001000.cert|9e880b2a201589ebd6a386315ca7c193a50c8002|1414505
class2-lane-cost67d-certificates/bit97-root-00000002000000801202000040002000.cert|e723a58ee264f12caa75bf2de7306964c8f9375e|1685346
class2-lane-cost69e-certificates/bit108-root-00001000000000803202000000008000.cert|8f65b1d375f39cd8b70e5296ce531ee0eacdb163|1224805
class2-lane-cost69e-certificates/bit116-root-00100000000000803202000000008000.cert.gz.b64|233243d463e5cad1f1a94c097ecae3ab924aa260|445162
class2-lane-cost69e-certificates/bit21-root-00000000000000803202000000208000.cert|507351ff0cb58df80d1231db9ea62228a7293d20|802884
class2-lane-cost69e-certificates/bit76-root-00000000000010803202000000008000.cert|02e5456a0fc55f5090394c6300329de64b3313c6|1645600
class2-lane-cost69e-certificates/bit84-root-00000000001000803202000000008000.cert|b3261526b628915bb2c31dd9aa6f4bd6668da92b|1068973
class2-lane-cost69e-certificates/bit87-root-00000000008000803202000000008000.cert|3e22d3d2c90422ae53c8e0432e3d84d0086c0d57|1585747
class2-lane-cost69e-certificates/bit89-root-00000000020000803202000000008000.cert|4d939aeb21eba32f1cd0bdb31b0ad3abc207b347|1698203
class2-lane-cost69e-certificates/bit90-root-00000000040000803202000000008000.cert|78d7c47ea696f638a7cad1e5d98204fcfd76d0e5|1693810
class2-lane-cost69e-certificates/bit94-root-00000000400000803202000000008000.cert|d1ca7c8cc4bf361d933b4ce0ee77f50801af2e80|1532586
class2-lane-cost69e-certificates/bit99-root-00000008000000803202000000008000.cert|4fbd36bd1b83af00eeb462c08f7b83a9aa1027f4|905701
class2-lane-cost70g-certificates/bit112-root-00010000000000801202000040000001.cert|8cf370af56c7012fedad0177db03452bb2f74bd8|1656701
class2-lane-cost70g-certificates/bit119-root-00800000000100809002000000000800.cert|b5a4297977595a6f11ef21995135f4b2cbe31b78|1490548
class2-lane-cost70g-certificates/bit120-root-01000000000000801202000040000001.cert|3a9fcee118e6036d3f50aec6fff35482e2945c38|2423973
class2-lane-cost70g-certificates/bit18-root-00000000000000801202000040040001.cert|7b0c2fa2a0366536971db6e9e1aafd4c539d0021|2404026
class2-lane-cost70g-certificates/bit20-root-00000000000100809002000000100800.cert|b2a83239066c35944c281823b9b3ebb77f94815e|610855
class2-lane-cost70g-certificates/bit24-root-00000000000000801202000041000001.cert|0112f59b8ef11c2cb9c9fff337278ad1fcaaa1a9|2095775
class2-lane-cost70g-certificates/bit28-root-00000000000000801202000050000001.cert|a94fcb72886560565fcff28efbdaf0f364cfbdca|1641809
class2-lane-cost70g-certificates/bit29-root-00000000000100809002000020000800.cert|bab4338b0a17ca93425f4e846d3e0995efa71f99|1593904
class2-lane-cost70g-certificates/bit34-root-00000000000100809002000400000800.cert|e95fcaf5becc9dadacd9c382c57b1faaf395d8b6|2034038
class2-lane-cost70g-certificates/bit59-root-00000000000000801a02000040000001.cert|99f7f3faf44072cd2e28932ff6af0e7cfd93a92e|1003502
class2-lane-cost70g-certificates/bit62-root-0000000000010080d002000000000800.cert|1c023a37bebd87ca3a5a86dc39663e743d1d66fa|958852
class2-lane-cost70g-certificates/bit70-root-00000000000100c09002000000000800.cert|d522d9ebcddd30483eaa2ee60f24a1cee8e1273e|700014
class2-lane-cost70g-certificates/bit76-root-00000000000110809002000000000800.cert|63a6c8b4667ae8a96086d986607891716a021477|1657038
class2-lane-cost70g-certificates/bit89-root-00000000020000801202000040000001.cert|0cc5c701cd485cbc40629a267bfee8cda842f01a|1453371
class2-lane-cost70g-certificates/bit9-root-00000000000100809002000000000a00.cert|1877c1c6d07a458b6daa53e56338cffc941c2a5a|1860364"""

RECEIPTS_BANDS = [
    ("60c", "class-frontier-cost60c-receipts-recompute-20261116.json", "cost60c_addition_on_cost75e_1407", "class2-lane-cost60c-certificates"),
    ("63h", "class-frontier-cost63h-receipts-recompute-20261115.json", "cost63h_addition", "class2-lane-cost63h-certificates"),
    ("63i", "class-frontier-cost63i-receipts-recompute-20261116.json", "cost63i_addition", "class2-lane-cost63i-certificates"),
    ("63j", "class-frontier-cost63j-receipts-recompute-20261116.json", "cost63j_addition", "class2-lane-cost63j-certificates"),
    ("65m", "class-frontier-cost65m-receipts-recompute-20261116.json", "cost65m_addition", "class2-lane-cost65m-certificates"),
    ("67d", "class-frontier-cost67d-receipts-recompute-20261116.json", "cost67d_addition", "class2-lane-cost67d-certificates"),
]
REC_69E = "class2-lane-cost69e-win7-certificates-20261114.json"
MANIFEST_70G = "class2-lane-cost70g-win7-certificates-20261115.json"
REC_70G_B = "class-frontier-cost70g-receipts-recompute-20261116.json"
REC_70G_A = "class-frontier-cost70g-receipts-recompute-20261115.json"
REC_60C_MANIFEST = "class2-lane-cost60c-win7-certificates-20261116.json"
AUDIT_69E = "class2-lane-cost69e-10cert-python-independent-audit-20261115.json"

EXPECTED_RECORDS = 83
AUDIT_69E_ROWS = 411114
AUDIT_69E_SUBROOTS = 535


def md5(b):
    return hashlib.md5(b).hexdigest()


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def git_blob_sha(b):
    return hashlib.sha1(b"blob %d\x00" % len(b) + b).hexdigest()


def load_records():
    R = []
    for band, fn, key, band_dir in RECEIPTS_BANDS:
        d = json.load(open(fn))
        for r in d[key]:
            R.append({
                "band": band, "bit": r["bit"], "root_hex": r["root_hex"],
                "band_dir": band_dir,
                "file": f"bit{r['bit']}-root-{r['root_hex']}.cert",
                "rows": r["rows"], "md5": r["md5"], "sha256": None,
                "sub_roots_pass": r["sub_roots_pass"],
                "record_source": f"{OUTD}/{fn}", "record_kind": "receipts-recompute",
            })
    d = json.load(open(REC_69E))
    for r in d["certificates"]:
        R.append({
            "band": "69e", "bit": r["bit"], "root_hex": r["root_hex"],
            "band_dir": "class2-lane-cost69e-certificates",
            "file": r["file"].split("/")[-1],
            "rows": r["rows"], "md5": r["md5"], "sha256": r.get("sha256"),
            "sub_roots_pass": r["sub_roots_pass"],
            "record_source": f"{OUTD}/{REC_69E}", "record_kind": "win7-certificates-records",
        })
    d = json.load(open(MANIFEST_70G))
    for r in d["certificates"]:
        R.append({
            "band": "70g", "bit": r["bit"], "root_hex": r["root_hex"],
            "band_dir": "class2-lane-cost70g-certificates",
            "file": r["repo_path"].split("/")[-1],
            "rows": r["strategy_rows"], "md5": None, "sha256": None,
            "sub_roots_pass": r["verify"]["subroots_passed"],
            "record_source": f"{OUTD}/{MANIFEST_70G}", "record_kind": "win7-manifest",
            "manifest": r,
        })
    d = json.load(open(REC_70G_B))
    for r in d["cost70g_addition"]:
        R.append({
            "band": "70g", "bit": r["bit"], "root_hex": r["root_hex"],
            "band_dir": "class2-lane-cost70g-certificates",
            "file": f"bit{r['bit']}-root-{r['root_hex']}.cert",
            "rows": r["rows"], "md5": r["md5"], "sha256": None,
            "sub_roots_pass": r["sub_roots_pass"],
            "record_source": f"{OUTD}/{REC_70G_B}", "record_kind": "receipts-recompute",
        })
    # uniqueness
    assert len(R) == EXPECTED_RECORDS, len(R)
    kb = [(r["band"], r["bit"]) for r in R]
    assert len(set(kb)) == len(kb), "duplicate (band, bit)"
    roots = [r["root_hex"] for r in R]
    assert len(set(roots)) == len(roots), "duplicate root_hex across records"
    return R


def decode_69e_116(raw):
    import base64, gzip
    return gzip.decompress(base64.b64decode(raw))


def run_verifier(path):
    p = subprocess.run([NODE, VERIFIER, path], capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def verify_one(rec, pins):
    rel = f"{rec['band_dir']}/{rec['file']}"
    assert rel in pins, ("unpinned file", rel)
    raw = open(f"{MIRROR}/{rel}", "rb").read()
    assert git_blob_sha(raw) == pins[rel][0], ("pin sha mismatch", rel)
    assert len(raw) == pins[rel][1], ("pin size mismatch", rel)
    plain = raw
    storage = "single .cert file"
    if rel.endswith(".gz.b64"):
        plain = decode_69e_116(raw)
        storage = "base64(gzip-9) .cert.gz.b64 -> decompressed for verification"
        assert len(plain) == 2670116, ("bit116 uncompressed bytes", len(plain))
        assert md5(plain) == rec["md5"], ("bit116 uncompressed md5",)
        assert sha256(plain) == rec["sha256"], ("bit116 uncompressed sha256",)
    computed_md5 = md5(plain)
    if rec["md5"] is not None:
        assert computed_md5 == rec["md5"], ("record md5 mismatch", rec["band"], rec["bit"])
    tmp = f"/tmp/reverify_bands_{rec['band']}_{rec['bit']}.cert"
    with open(tmp, "wb") as fh:
        fh.write(plain)
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
        "file": rel, "storage": storage,
        "record_source": rec["record_source"], "record_kind": rec["record_kind"],
        "pinned_blob_sha": pins[rel][0], "bytes_published": len(raw),
        "certificate_bytes": len(plain),
        "computed_md5": computed_md5,
        "record_md5": rec["md5"],
        "record_md5_match": rec["md5"] is None or computed_md5 == rec["md5"],
        "record_sha256": rec["sha256"],
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
    # keep deterministic order: by band, then bit
    order = {b: i for i, b in enumerate(["60c", "63h", "63i", "63j", "65m", "67d", "69e", "70g"])}
    entries.sort(key=lambda t: (order[t[0]["band"]], t[0]["bit"]))

    # ---- cross-checks ----
    # 60c manifest
    m = json.load(open(REC_60C_MANIFEST))
    c = m["certificates"][0]
    pc = c["published_cert"]
    e60 = [e for _, e, _ in entries if e["band"] == "60c"][0]
    assert e60["computed_md5"] == pc["whole_md5"]
    assert e60["certificate_bytes"] == pc["whole_bytes"]
    assert e60["pinned_blob_sha"] == pc["git_blob_sha"]
    assert e60["verifier_rows"] == c["rows"] and e60["record_sub_roots_pass"] == c["sub_roots"]
    assert e60["verifier_terminal_count"] == c["terminal_count"]
    assert e60["verifier_terminal_range"] == list(c["terminal_range"])
    sha2 = sha256(open(f"{MIRROR}/class2-lane-cost60c-certificates/bit92-root-00000000100000003800000008008020.cert", "rb").read())
    assert sha2 == pc["whole_sha256"], ("60c whole_sha256",)
    # 70g manifest cross-checks (8 bits)
    mg = json.load(open(MANIFEST_70G))
    bykey = {(e["band"], e["bit"]): (e, v) for _, e, v in entries}
    for r in mg["certificates"]:
        e, v = bykey[("70g", r["bit"])]
        assert e["pinned_blob_sha"] == r["repo_blob_sha"], ("70g blob sha", r["bit"])
        assert e["verifier_rows"] == r["strategy_rows"]
        assert v["root_mobility"] == r["loser_first_moves"], ("70g mobility", r["bit"])
        assert v["terminal_range"] == r["verify"]["terminal_range"], ("70g trange", r["bit"])
        assert v["terminal_count"] == r["verify"]["terminal_count"], ("70g tcount", r["bit"])
        assert v["visited_states_across_subroots"] == r["verify"]["visited_states_across_subroots"], ("70g visited", r["bit"])
        assert v["loser_reply_edges"] == r["verify"]["loser_reply_edges"], ("70g edges", r["bit"])
        assert r["verify"]["union_missing"] == 0 and r["verify"]["union_extra"] == 0
    # 70g-a receipts-recompute (8 bits) rows/sub_roots agreement
    ra = json.load(open(REC_70G_A))
    for r in ra["cost70g_addition"]:
        e, _ = bykey[("70g", r["bit"])]
        assert e["verifier_rows"] == r["rows"], ("70g-a rows", r["bit"])
        assert e["record_sub_roots_pass"] == r["sub_roots_pass"], ("70g-a subroots", r["bit"])
    # 69e python audit totals
    e69 = [e for _, e, _ in entries if e["band"] == "69e"]
    assert len(e69) == 10
    assert sum(e["verifier_rows"] for e in e69) == AUDIT_69E_ROWS
    assert sum(e["verifier_subroots_passed"] for e in e69) == AUDIT_69E_SUBROOTS

    total_rows = sum(e["verifier_rows"] for _, e, _ in entries)
    total_sub = sum(e["verifier_subroots_passed"] for _, e, _ in entries)
    total_bytes = sum(e["certificate_bytes"] for _, e, _ in entries)
    n_md5_record = sum(1 for _, e, _ in entries if e["record_md5"] is not None)
    from collections import Counter
    per_band = Counter(e["band"] for _, e, _ in entries)

    doc = {
        "schema": "n11-class2-lane-receipts-recompute-bands-certificates-bigint-independent-reverification-20261117-v1",
        "date": "2026-11-17",
        "pin": {
            "commit": PIN,
            "record_files": sorted(set(r["record_source"] for r in records)),
            "authoritative_blob_sha_table": "GitHub directory listing of the eight band certificate dirs at the pinned commit (fields name/sha/size), embedded in the script as PINS and asserted 83/83 against the mirrored bytes",
        },
        "method": {
            "records": "83 WIN7-D10 certificate records: receipts-recompute per-entry records (rows/md5/sub_roots_pass) for bands 60c(1)/63h(1)/63i(18)/63j(29)/65m(8)/67d(1); cost-69e win7-certificates records (10, with sha256; bit 116 documents hashes of the UNCOMPRESSED certificate published as base64(gzip-9)); cost-70g = win7 manifest (8, strategy_rows/subroots_passed/repo_blob_sha, no md5 documented) + receipts-recompute-20261116 (7, with md5)",
            "bytes": "each certificate fetched from the commit-pinned raw CDN URL into the local mirror; git blob sha+size asserted against the authoritative GitHub directory listing at the pin (83/83)",
            "verifier": "verify_win7_certificate_bigint_independent.mjs (git blob 62b5d9413daafb172f6e10249976ee6808f7b454): BigInt 3x3 cofactor expansion of the exact lifted determinant [x^2+y^2,x,y,1], no floating point, no solver/verdict-cache import; root stones=7 + safe check, loser mobility vs independent enumeration, per-subroot winner strategy legality walk, union missing/extra 0/0, rows sorted unique, terminal range within 13..17",
        },
        "entries": [e for _, e, _ in entries],
        "cross_checks": {
            "cost60c_manifest": "published_cert whole_bytes/whole_md5/whole_sha256/git_blob_sha, rows/sub_roots/terminal_count/terminal_range all reproduced",
            "cost70g_manifest_8_bits": "repo_blob_sha, loser_first_moves, verify terminal_range/terminal_count/visited_states/loser_reply_edges all reproduced",
            "cost70g_receipts_recompute_20261115_8_bits": "rows/sub_roots_pass all reproduced",
            "cost69e_python_audit_totals": f"strategy_rows sum == {AUDIT_69E_ROWS}, subroots sum == {AUDIT_69E_SUBROOTS}",
        },
        "summary": {
            "records": len(entries),
            "distinct_certificate_files": len(set(e["file"] for _, e, _ in entries)),
            "verifier_pass": len(entries),
            "verifier_fail": 0,
            "record_md5_asserted": n_md5_record,
            "record_md5_mismatch": 0,
            "pin_blob_sha_mismatch": 0,
            "total_rows_independently_verified": total_rows,
            "total_sub_roots_independently_verified": total_sub,
            "total_certificate_bytes_rehashed": total_bytes,
            "records_per_band": dict(sorted(per_band.items())),
        },
        "interpretation_guard": [
            "this re-verification strengthens the head-1452 census tier-R population: the 83 certificates of these eight bands move from receipt-cert documentation to bytes-level independently re-verified evidence; it does not change any frontier number",
            "solved 1452 is manifest cover bookkeeping of the head-1452 frontier",
            "a WIN7-D10 certificate proves only that its individual 7-stone root is a first-player win within depth 10",
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
