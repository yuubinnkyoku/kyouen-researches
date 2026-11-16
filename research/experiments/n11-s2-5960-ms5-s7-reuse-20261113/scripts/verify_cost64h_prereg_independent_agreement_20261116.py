#!/usr/bin/env python3
"""Independent agreement verification of the published cost-64h fold
PRE-REGISTRATION (class2-lane-cost64h-fold-preregistration-independent-
20261116.json, git blob 5074a8a0cbb75fcc91b5b999a3135fac06d42400, commit
c64579b4b879, 2026-11-16T13:43:18Z) against a fully independent
re-derivation in this fresh environment.

Second-implementation protocol (this lane did not run the cost-64h sweep,
did not extract the certificates and did not write the pre-registration;
it verifies them):

  1. blob-verify every published input artifact it consumes: the basis
     chain (133 blob-pinned basis JSONs + 3 gz + 6 MS5 manifest parts via
     the published head-1450 fold-projection tool), the published cost-66c
     and cost-76d/77e fold JSONs, the head-1452 presweep census, the
     cost-64h claim v2, the raw sweep audit, the 8 raw batches, the v15
     crosscheck, the independent full re-run verification record, the
     third certificate verification record and all 87 files of the
     published certificate directory (pins recorded below);
  2. reproduce the canonical head 1452 (basis 1450 + the four cost-76d/77e
     receipts) and re-derive the cost-64h sweep aggregates from the 8 raw
     batches (23 WIN7-D10 bits, 41 REFUTED-D10, 0 capped, node sum
     47,017,565, 8/8 pilot controls at 3402 nodes) plus the v15
     cross-engine agreement;
  3. byte-verify all 23 published WIN7 certificates against the published
     directory pins, recompute md5/sha256, re-derive root mobility with
     the independent exact-integer Bareiss enumerator (legal_candidates.py)
     and check header / root line / sorted-unique strategy rows / row
     counts against the published summaries, BigInt records and Bareiss
     records; record that bits 116 and 120 have no published BigInt/Bareiss
     records on main at check time and verify them locally with the
     published independent BigInt verifier;
  4. run the conflict census: the 64 candidate D4 orbits of the child
     00000000000000403800000008100000 against the 760 folded roots at head
     1452 (zero overlaps), the 23 WIN roots pairwise distinct and disjoint;
  5. independently project the 23-receipt fold (ascending bit order) onto
     head 1452 with the verbatim frontier semantics and compare
     field-by-field with the published pre-registration.

Bookkeeping verification only; no engine search was run, no verdict was
created and no row was closed by this script. Solved counts measure
manifest coverage, not the game-theoretic value of any position; WIN7
certificates prove a first-player win within depth 10 from the individual
7-stone roots only; REFUTED-D10 is not a LOSS proof; the 11x11 empty board,
two-stone roots {49,60}/{59,60}, S2 {59,60} and classes 1/2/4 remain
UNKNOWN.
"""
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
SCRIPTS = HERE / "scripts"
OUT = HERE / "output"
sys.path.insert(0, str(SCRIPTS))

from fold_projection_head1450_tool_20261116 import (  # noqa: E402
    canon, covers, popcount, reconstruct, git_blob_sha)
import preregister_cost76d_77e_fold_20261116 as pre  # noqa: E402
from legal_candidates import legal_candidates  # noqa: E402

CHILD = "00000000000000403800000008100000"
PARENT_A = "00000000000000403800000008000000"
PARENT_B = "00000000000000003800000008001000"
WIN_BITS = [4, 6, 8, 33, 38, 42, 44, 49, 68, 74, 76, 77, 78, 79, 83, 89,
            91, 101, 109, 113, 114, 116, 120]
HEAD_1452 = (1452, 174, 6396, 506144, 4669, 370058)
HEAD_1450 = (1450, 174, 6398, 506297, 4671, 370211)
FOLD76D77E_JSON = "class-frontier-cost76d77e-receipts-recompute-20261116.json"
FOLD66C_JSON = "class-frontier-cost66c-receipts-recompute-20261116.json"
FOLD66C_BLOB = "8783993e5c73cc9697c3ca48aef981725f422be8"
PREREG_JSON = "class2-lane-cost64h-fold-preregistration-independent-20261116.json"
PREREG_BLOB = "5074a8a0cbb75fcc91b5b999a3135fac06d42400"
PREREG_COMMIT = "c64579b4b8798a74f5da909ad7c2d50b555ecdb1"
CENSUS_JSON = "class2-lane-next-target-presweep-1452-20261116.json"
CENSUS_BLOB = "0d9a94a272de9fe45708757f17bfea60239a3c9b"
CLAIM_JSON = "class2-lane-cost64h-inflight-20261116.json"
CLAIM_BLOB = "68e4878094b78eaf0a465033d0289a6db5d94861"
AUDIT_JSON = "class2-lane-cost64h-sweep-audit-20261116.json"
AUDIT_BLOB = "98f55cdaf7810f89ab32b726ea810d4b31ca6c88"
RERUN_JSON = "class2-lane-cost64h-independent-rerun-verification-20261116.json"
RERUN_BLOB = "17ab4b4bf963a9e16c9ed40d559fc7b5bc3c7684"
THIRD_JSON = "class2-lane-cost64h-certificate-third-verification-20261116.json"
THIRD_BLOB = "caba78da65592b521b3cc0644fac6eae01612762"
V15_JSONL = "class2-lane-cost64h-v15-crosscheck-20261116.jsonl"
V15_BLOB = "0d32c2a0f5411d455f5b1503bc37c95c58f0b155"
CERTDIR = "class2-lane-cost64h-certificates"
BIGINT_VERIFIER = "verify_win7_certificate_bigint_independent.mjs"

# published git blob shas of every file in the certificate directory,
# taken from the GitHub directory listing of main at check time
# (commit 0fc0b9e2c7); bits 116 and 120 have no BigInt/Bareiss records on
# main at check time (recorded here as a publication-coverage gap, not an
# error: the certificates themselves are published and byte-pinned)
CERT_PINS = {
    "bit101-bareiss-verify.json":
        "97a75dc3e63c21f4f3c578d024ed4997b2d0d21e",
    "bit101-root-00000020000000403800000008100000.bigint.json":
        "bd51a46c426364edfe196aeec0acbac5fd239615",
    "bit101-root-00000020000000403800000008100000.cert":
        "68c7235d49bb7dc45b63e9d2e190054b2409bb60",
    "bit101-root-00000020000000403800000008100000.cert.part1of1.summary.json":
        "644b74763d486ae9b139c7ba2f5663b808d6dc30",
    "bit109-bareiss-verify.json":
        "796ebd5118beb451c57068cafd608fbe816976c8",
    "bit109-root-00002000000000403800000008100000.bigint.json":
        "2226453d9dfc53f2f0b38a59c928382d19a5d161",
    "bit109-root-00002000000000403800000008100000.cert":
        "4f8398876e36c861d1b97dbb8f91614acddade3e",
    "bit109-root-00002000000000403800000008100000.cert.part1of1.summary.json":
        "b3e993d0346d9438418c45b0212293fcf52c8438",
    "bit113-bareiss-verify.json":
        "4400819a89fdccf28f99cb3bc8e46a1f24c7e052",
    "bit113-root-00020000000000403800000008100000.bigint.json":
        "a712e28214e2926e61bb58eeca2da481da708c65",
    "bit113-root-00020000000000403800000008100000.cert":
        "fb4b02dcd336a474384ae045f533dd0368b81052",
    "bit113-root-00020000000000403800000008100000.cert.part1of1.summary.json":
        "54cb691e1935c3e532785b9f8f74b0ab22729944",
    "bit114-bareiss-verify.json":
        "164a3dbfb8c54be320968b56d20811784925d324",
    "bit114-root-00040000000000403800000008100000.bigint.json":
        "a64d6f63bd03688e568efeab9d40c0dea0b53f6c",
    "bit114-root-00040000000000403800000008100000.cert":
        "1880bc8a9428052d7e8cfb941a20b444f633cd45",
    "bit114-root-00040000000000403800000008100000.cert.part1of1.summary.json":
        "f3f8e0cb65782151bc5b2490c19d9c6c997a9b85",
    "bit116-root-00100000000000403800000008100000.cert":
        "fbc3836be608c963f0a5dea8a2dd32ef52956ec5",
    "bit116-root-00100000000000403800000008100000.cert.part1of1.summary.json":
        "fb233862ba6b7825c35800f9548ec408c6d4a9a5",
    "bit120-root-01000000000000403800000008100000.cert":
        "dbeaf4a648294efe362a8659d7299aa8043c7d7f",
    "bit33-bareiss-verify.json":
        "68947dc77cdffe0f63147abd1664ecba64d4a719",
    "bit33-root-00000000000000403800000208100000.bigint.json":
        "74469e631e4514bec342bb22bd98c57cb3ad70cf",
    "bit33-root-00000000000000403800000208100000.cert":
        "bcc45876c54a548d372c9fc6dab076e44d4e7d47",
    "bit33-root-00000000000000403800000208100000.cert.part1of1.summary.json":
        "29bec5223f7dfc0b29af29f10f36efb060bdfad4",
    "bit38-bareiss-verify.json":
        "3d17d0340442ff2dd1d51c75d4b84bf2afe5be8a",
    "bit38-root-00000000000000403800004008100000.bigint.json":
        "b1f12a702f25883d2dd3a37e2e3da99d8f149bba",
    "bit38-root-00000000000000403800004008100000.cert":
        "65ed7517f216e5c4c159c4481180836f5f89b30d",
    "bit38-root-00000000000000403800004008100000.cert.part1of1.summary.json":
        "2e4fa8a286998f36501bb2ce80e0f60e3eaf968d",
    "bit4-bareiss-verify.json":
        "7c504f8e024010e77c24e097e073eac52c9309a8",
    "bit4-root-00000000000000403800000008100010.bigint.json":
        "d57e17491f509d05824408aca16eca9805f227d9",
    "bit4-root-00000000000000403800000008100010.cert":
        "c0911621828cc098c240f6b2a38ee407a740d956",
    "bit4-root-00000000000000403800000008100010.cert.part1of1.summary.json":
        "0d624ed5bdacfa26231cc5946671cd379676706a",
    "bit42-bareiss-verify.json":
        "2b9cd8333605b3c10b265ef7fc1dd91f7772d091",
    "bit42-root-00000000000000403800040008100000.bigint.json":
        "9d680309cfd119873a8f1f63d4dfc22553bb090b",
    "bit42-root-00000000000000403800040008100000.cert":
        "ac6649de93627daaedb69ffdb5d1a1f4b7db1c94",
    "bit42-root-00000000000000403800040008100000.cert.part1of1.summary.json":
        "8c98ce9fbe2d8f805acbb6c473fea461fbf94aee",
    "bit44-bareiss-verify.json":
        "bfdaafe0231e5ed6122eebf90c019d9c9e9c3ecb",
    "bit44-root-00000000000000403800100008100000.bigint.json":
        "1c568f7853d57cdf31ea9186b40f0e2310efe272",
    "bit44-root-00000000000000403800100008100000.cert":
        "2a79c84e1f0bcfe724cd888461d1d025e4fd29b8",
    "bit44-root-00000000000000403800100008100000.cert.part1of1.summary.json":
        "b9acd307f48183428629119c5030b0c32d52ca97",
    "bit49-bareiss-verify.json":
        "4ff5f64ef316888b53fb81d918f45a437a0b9952",
    "bit49-root-00000000000000403802000008100000.bigint.json":
        "3cb6c869a86fc505d90608accdc7b3a85df96c9a",
    "bit49-root-00000000000000403802000008100000.cert":
        "ba7aef3f186620c89101e7f74564cec591ca4fbd",
    "bit49-root-00000000000000403802000008100000.cert.part1of1.summary.json":
        "4e8b66209490275b37e153dda3d432446f10ae90",
    "bit6-bareiss-verify.json":
        "5068b9964d59de4e452179d21d989f0597517b54",
    "bit6-root-00000000000000403800000008100040.bigint.json":
        "861bf16afcd3678e7582d06d79e7bfa68c0a28a6",
    "bit6-root-00000000000000403800000008100040.cert":
        "96c5574f04a496a124bdd16ecd8926226fbc9786",
    "bit6-root-00000000000000403800000008100040.cert.part1of1.summary.json":
        "f38fd7149ff2d9208f6e91f8faadf0dc7774756d",
    "bit68-bareiss-verify.json":
        "39125d5b1c5b71050893e252baab02a35d384c9b",
    "bit68-root-00000000000000503800000008100000.bigint.json":
        "3346a8e25a02a723ae260b58544c7cac9de65368",
    "bit68-root-00000000000000503800000008100000.cert":
        "5f889da88fd89be51f1defe6db2f6677d037bd09",
    "bit68-root-00000000000000503800000008100000.cert.part1of1.summary.json":
        "e8a5ef41d89efa055c985d587c057b6aeff6bb27",
    "bit74-bareiss-verify.json":
        "25ecfb18827a174480ce1f3b451bef93f14bc8d6",
    "bit74-root-00000000000004403800000008100000.bigint.json":
        "9c53cc70137ddcf9e1066f8b197d8f3547c0537d",
    "bit74-root-00000000000004403800000008100000.cert":
        "3f4f5ab294f6e7dd84e9c95fa9d4120add4392cb",
    "bit74-root-00000000000004403800000008100000.cert.part1of1.summary.json":
        "c9c7a03f731972ad815f93f377faeb7f294cf72c",
    "bit76-bareiss-verify.json":
        "af65bbd0383123a473bccba9111c52e88792bacd",
    "bit76-root-00000000000010403800000008100000.bigint.json":
        "945cc677c0906595ceae3611a4a3b9748444c3f3",
    "bit76-root-00000000000010403800000008100000.cert":
        "350cf706c408d0f008482618debb0565c52a7851",
    "bit76-root-00000000000010403800000008100000.cert.part1of1.summary.json":
        "1dffef3a5097cfab612f523b60b24a533e184f3f",
    "bit77-bareiss-verify.json":
        "35d3fcf0c4bb5a928e341095cce4e5692b122ed0",
    "bit77-root-00000000000020403800000008100000.bigint.json":
        "59de2e3b6340ca993d406ffdb089a0b4c3d370e3",
    "bit77-root-00000000000020403800000008100000.cert":
        "dec4b93727d5048ce25f59fd894ba86a45302f18",
    "bit77-root-00000000000020403800000008100000.cert.part1of1.summary.json":
        "309a866cf161d967d39fd9c56479a4b0731b252a",
    "bit78-bareiss-verify.json":
        "76169d7b04684b8b42b364dcd307da3ef907e5f7",
    "bit78-root-00000000000040403800000008100000.bigint.json":
        "f073dc9ad27289c893e40888f528f9349fbf5521",
    "bit78-root-00000000000040403800000008100000.cert":
        "d5cdce8917dc1fa7ae45ceeb1e7a47049782aa2f",
    "bit78-root-00000000000040403800000008100000.cert.part1of1.summary.json":
        "5c004209e1ed3a5c6041cbf866310f7a81e49370",
    "bit79-bareiss-verify.json":
        "2199dac993b2e72a4f9c8d5667474befb7c3f8f2",
    "bit79-root-00000000000080403800000008100000.bigint.json":
        "be5e36bc46429965d21f2bf96f815729f4fc6530",
    "bit79-root-00000000000080403800000008100000.cert":
        "3c61d138dead96bf6905beb86c17acd275ecf06e",
    "bit79-root-00000000000080403800000008100000.cert.part1of1.summary.json":
        "eab8617cf7eaf27c2691c08b0776ee5e2fe5745c",
    "bit8-bareiss-verify.json":
        "5aff5201da66cb4555d2dcc1007ddb08ed30145c",
    "bit8-root-00000000000000403800000008100100.bigint.json":
        "cc0dd5797f1046940e2923ea3e25a742a35165c0",
    "bit8-root-00000000000000403800000008100100.cert":
        "db414850ef78b6c338fcb6094d32e9a546b81089",
    "bit8-root-00000000000000403800000008100100.cert.part1of1.summary.json":
        "6b6920c6451db838af9d9bc37de7b40dea7b8315",
    "bit83-bareiss-verify.json":
        "0bd96c56bd1bbb3f8c110d02cf018ef909eb8374",
    "bit83-root-00000000000800403800000008100000.bigint.json":
        "db93dc86e9bbbd584011462da4b64e7aa6f07f8e",
    "bit83-root-00000000000800403800000008100000.cert":
        "d9454bbd5dec5c81d1782496079f344166c4e96e",
    "bit83-root-00000000000800403800000008100000.cert.part1of1.summary.json":
        "b60e0d6204228646d98a4c8a9ad8d57d777bf517",
    "bit89-bareiss-verify.json":
        "29e53d438719f05ae42cfef2db2566d500dd02c1",
    "bit89-root-00000000020000403800000008100000.bigint.json":
        "632abf6da4a02ad6d4736a833777186d9e1b9bbd",
    "bit89-root-00000000020000403800000008100000.cert":
        "5e174da908f8617c87e761112db50f5b093669f8",
    "bit89-root-00000000020000403800000008100000.cert.part1of1.summary.json":
        "d41160c8d21ea5ca15e3fe26d105f47bdf1fc4a0",
    "bit91-bareiss-verify.json":
        "bcc779edde2be66864cee17c385666524fad06a3",
    "bit91-root-00000000080000403800000008100000.bigint.json":
        "0be5384de3e87e9a1a3f2d669200042065157fd5",
    "bit91-root-00000000080000403800000008100000.cert":
        "bc433641c6caecf440bdeb13842cc9e4bcfe6041",
    "bit91-root-00000000080000403800000008100000.cert.part1of1.summary.json":
        "f3f9044ca442b57522bcfbb77044ef36f519d71b",
}

CERT_HEADER = "n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS"
HEX = 32


def md5hex(data):
    return hashlib.md5(data).hexdigest()


def sha256hex(data):
    return hashlib.sha256(data).hexdigest()


def load_jsonl(path):
    return [json.loads(x) for x in path.read_text().splitlines() if x.strip()]


def main():
    checks = {}
    # ---------- 1. input blob verification --------------------------------
    pins = {
        PREREG_JSON: PREREG_BLOB,
        CLAIM_JSON: CLAIM_BLOB,
        AUDIT_JSON: AUDIT_BLOB,
        RERUN_JSON: RERUN_BLOB,
        THIRD_JSON: THIRD_BLOB,
        V15_JSONL: V15_BLOB,
        FOLD76D77E_JSON: "8d4bc622f9da22b8754f2e398e5481359656d956",
        FOLD66C_JSON: FOLD66C_BLOB,
        CENSUS_JSON: CENSUS_BLOB,
    }
    claim = json.loads((OUT / CLAIM_JSON).read_text())
    for path, sha in claim["published_artifacts"]["raw_batches"]:
        pins[path.rsplit("/", 1)[-1]] = sha
    for name, blob in pins.items():
        assert git_blob_sha((OUT / name).read_bytes()) == blob, name
    checks["C1_input_blob_pins"] = len(pins)
    for name, blob in CERT_PINS.items():
        assert git_blob_sha((OUT / CERTDIR / name).read_bytes()) == blob, name
    assert set(CERT_PINS) == {p.name for p in (OUT / CERTDIR).iterdir()}, \
        "certificate directory contents do not match the pinned listing"
    checks["C2_cert_dir_87_pins"] = len(CERT_PINS)
    print(f"CONTROL {len(pins)} lane pins + {len(CERT_PINS)} cert-dir pins "
          "blob-verified")

    prereg = json.loads((OUT / PREREG_JSON).read_text())
    audit = json.loads((OUT / AUDIT_JSON).read_text())
    rerun = json.loads((OUT / RERUN_JSON).read_text())
    third = json.loads((OUT / THIRD_JSON).read_text())
    census = json.loads((OUT / CENSUS_JSON).read_text())
    fold76d77e = json.loads((OUT / FOLD76D77E_JSON).read_text())

    # ---------- 2. basis reproduction to head 1452 ------------------------
    manifest, classes, incidences, winners, rejected = pre.load_basis()
    pre.manifest_holder[0] = manifest
    frontier, summary = pre.make_frontier(classes, incidences, rejected)
    basis_roots = reconstruct()
    assert len(basis_roots) == 771
    folded_canons = {canon(r) for r in basis_roots}
    assert len(folded_canons) == 756
    solved = set(winners)
    for r in basis_roots:
        solved |= covers(r)
    keys = ("solved_s6_in_manifest", "remaining_s5_orbits",
            "unique_remaining_s6", "sum_remaining_cost",
            "s6_needed_by_open_classes", "cost_needed_by_open_classes")
    assert tuple(summary(solved)[k] for k in keys) == HEAD_1450
    for lane, bit in [("76d", 19), ("76d", 49), ("77e", 37), ("77e", 69)]:
        root = int(pre.ROOTS[(lane, bit)], 16)
        assert popcount(root) == 7
        c = canon(root)
        assert c not in folded_canons
        folded_canons.add(c)
        solved |= covers(root)
    st1452 = summary(solved)
    assert tuple(st1452[k] for k in keys) == HEAD_1452
    fa = fold76d77e["frontier_after_cost76d77e"]
    assert [fa[k] for k in keys] == list(HEAD_1452)
    assert prereg["basis_head_numbers"] == list(HEAD_1452)
    assert prereg["basis_demand_histogram"] == st1452["hist"]
    assert prereg["basis_receipt_roots"] == 775
    assert prereg["basis_distinct_d4_canons"] == 760
    checks["C3_head_1452_reproduced"] = list(HEAD_1452)
    hist_before = st1452["hist"]
    print("CONTROL head 1452 reproduced (basis 771/756 + 4 receipts)")

    # ---------- 3. sweep re-derivation from the raw batches ---------------
    child_v = int(CHILD, 16)
    cands = sorted(legal_candidates(CHILD)[1])
    assert cands == sorted(claim["legal_candidates"])
    assert len(cands) == 64
    bit_recs = {}
    pilots = 0
    for n in range(1, 9):
        for r in load_jsonl(OUT / f"class2-lane-cost64h-raw-batch{n}"
                            "-20261116.jsonl"):
            if "control" in r:
                assert r["loss"] is False and r["capped"] is False
                assert r["nodes"] == 3402
                pilots += 1
            else:
                assert r["bit"] not in bit_recs
                assert r["andclose"] is True and r["capped"] is False
                bit_recs[r["bit"]] = r
    assert pilots == 8
    assert sorted(bit_recs) == cands
    win = sorted(b for b, r in bit_recs.items() if r["loss"] is True)
    refuted = sorted(b for b, r in bit_recs.items() if r["loss"] is False)
    node_sum = sum(r["nodes"] for r in bit_recs.values())
    assert win == WIN_BITS == audit["sweep_totals"]["win7_d10_bits"]
    assert len(refuted) == 41 and audit["sweep_totals"]["refuted_d10_count"] == 41
    assert node_sum == 47017565 == audit["sweep_totals"]["node_sum"]
    assert audit["sweep_totals"]["capped_count"] == 0
    assert claim["sweep_results"]["candidates_resolved"] == 64
    assert claim["sweep_results"]["node_sum_v16"] == node_sum
    assert sorted(claim["sweep_results"]["win7_d10_bits"]) == win
    for r in bit_recs.values():
        assert r["terminalStoneRange"] == [13, 17]
    v15 = load_jsonl(OUT / V15_JSONL)
    v15_pilot = [r for r in v15 if "control" in r]
    assert len(v15_pilot) == 1
    assert all(r["loss"] is False and r["nodes"] == 5949 for r in v15_pilot)
    v15_bits = {r["bit"]: r for r in v15 if "control" not in r}
    assert sorted(v15_bits) == win      # v15 re-ran the 23 WIN bits only
    for r in v15_bits.values():
        assert r["loss"] is True and r["capped"] is False
        assert r["andclose"] is True
        assert r["terminalStoneRange"] == [13, 17]
    v15_win = sorted(b for b, r in v15_bits.items() if r["loss"] is True)
    assert v15_win == win
    v15_node_sum = sum(r["nodes"] for r in v15_bits.values())
    assert v15_node_sum == audit["v15_crosscheck"]["node_sum"] == 55171821
    assert audit["v15_crosscheck"]["all_23_loss_true"] is True
    assert audit["v15_crosscheck"]["win_bits_loss_true"] == win
    assert audit["v15_crosscheck"]["pilot_nodes"] == 5949
    checks["C4_sweep_rederived"] = {
        "win": len(win), "refuted": len(refuted), "capped": 0,
        "node_sum": node_sum, "pilots": pilots,
        "v15_pilots": len(v15_pilot), "v15_node_sum": v15_node_sum}
    # the published independent full re-run record
    for k, v in rerun["checks"].items():
        assert v is True, (k, v)
    assert rerun["totals"]["published_node_sum"] == node_sum
    assert rerun["totals"]["rerun_node_sum"] == node_sum
    assert sorted(rerun["totals"]["win7_d10_bits"]) == win
    assert rerun["totals"]["node_exact"] == 64 and rerun["totals"]["mismatches"] == 0
    checks["C5_published_rerun_record_all_true"] = len(rerun["checks"])
    print(f"CONTROL sweep re-derived: 23 WIN / 41 REFUTED / 0 capped, "
          f"node sum {node_sum}, v15 agrees; published re-run record "
          f"{len(rerun['checks'])}/9 checks true")

    # ---------- 4. certificate verification -------------------------------
    roots = {b: f"{child_v | (1 << b):0{HEX}x}" for b in win}
    assert {str(b): h for b, h in roots.items()} == \
        audit["sweep_totals"]["win_roots"]
    # per-root D4 self-canonicality flags (published dict, re-derived here)
    self_canon = {str(b): canon(int(h, 16)) == int(h, 16)
                  for b, h in roots.items()}
    assert self_canon == audit["sweep_totals"]["win_roots_d4_self_canonical"]
    assert audit["sweep_totals"]["andclose_all"] is True
    cert_report = []
    mobility = {}
    for b in win:
        root_hex = roots[b]
        cert_path = OUT / CERTDIR / f"bit{b}-root-{root_hex}.cert"
        data = cert_path.read_bytes()
        lines = data.decode().splitlines()
        assert lines[0] == CERT_HEADER, (b, lines[0])
        assert lines[1] == f"root {root_hex}", (b, lines[1])
        rows = [l.split()[0] for l in lines[2:] if l]
        hexes = [int(x, 16) for x in rows]
        sorted_unique = all(hexes[i] < hexes[i + 1]
                             for i in range(len(hexes) - 1))
        assert sorted_unique, (b, "strategy rows not sorted-unique")
        st, lc = legal_candidates(root_hex)
        assert popcount(int(root_hex, 16)) == 7 and len(st) == 7
        mobility[b] = len(lc)
        summ_path = OUT / CERTDIR / f"bit{b}-root-{root_hex}.cert.part1of1.summary.json"
        summ = json.loads(summ_path.read_text()) if summ_path.exists() else None
        if summ is not None:
            assert summ["child"] == CHILD and summ["bit"] == b
            assert summ["nRows"] == len(hexes)
            assert sorted(summ["moves"]) == sorted(lc)
            assert all(m["ok"] is True and m["capped"] is False
                       for m in summ["perMove"].values())
            assert sorted(map(int, summ["perMove"])) == sorted(lc)
            assert summ["fbt_drops"] == 0
            assert sum(m["nodes"] for m in summ["perMove"].values()) == \
                summ["sum"]
        rec = {"bit": b, "root_hex": root_hex, "bytes": len(data),
               "md5": md5hex(data), "sha256": sha256hex(data),
               "git_blob_sha": git_blob_sha(data), "nRows": len(hexes),
               "mobility": mobility[b], "sorted_unique": True,
               "summary_ok": summ is not None}
        # BigInt record (21 of 23 bits have one published)
        bi_path = OUT / CERTDIR / f"bit{b}-root-{root_hex}.bigint.json"
        if bi_path.exists():
            bi = json.loads(bi_path.read_text())
            assert bi["root_hex"] == root_hex
            assert bi["root_stones"] == 7 and bi["root_safe"] is True
            assert bi["root_mobility"] == mobility[b]
            assert bi["strategy_rows"] == len(hexes)
            assert bi["rows_sorted_unique"] is True
            assert bi["union_missing"] == 0 and bi["union_extra"] == 0
            assert bi["subroots_passed"] == mobility[b]
            assert bi["consumed_winner_rows"] == len(hexes)
            rec["bigint_record_ok"] = True
        else:
            rec["bigint_record_ok"] = None   # not published on main
        # Bareiss record (21 of 23 bits have one published)
        ba_path = OUT / CERTDIR / f"bit{b}-bareiss-verify.json"
        if ba_path.exists():
            ba = [json.loads(x) for x in
                  ba_path.read_text().strip().splitlines()]
            assert ba[0]["stones"] == 7
            assert ba[0]["loserMobility"] == mobility[b]
            assert ba[1]["rows"] == len(hexes)
            assert sorted(int(k[1:]) for k in ba[1]["stats"]) == sorted(lc)
            rec["bareiss_record_ok"] = True
        else:
            rec["bareiss_record_ok"] = None  # not published on main
        cert_report.append(rec)
    assert sum(1 for r in cert_report if r["bigint_record_ok"]) == 21
    assert sum(1 for r in cert_report if r["bareiss_record_ok"]) == 21
    assert {r["bit"] for r in cert_report
            if r["bigint_record_ok"] is None} == {116, 120}
    checks["C6_cert_bytes_verified"] = len(cert_report)
    checks["C7_cert_summary_rows_sorted_unique"] = len(cert_report)
    # bits 116 and 120 have no BigInt/Bareiss/summary records on main at
    # check time: independently run the published BigInt verifier here and
    # save the records (they are evidence produced by this lane, not
    # replacements for the missing publications)
    local_bigint = {}
    for b in (116, 120):
        p = OUT / ("class2-lane-cost64h-bit116-120-local-bigint-verification"
                   "-20261116.json")
        rec = json.loads(p.read_text())["records"][str(b)]
        assert rec["verdict"] == "WIN7 certificate independently verified"
        assert rec["root_hex"] == roots[b]
        assert rec["root_stones"] == 7 and rec["root_safe"] is True
        assert rec["root_mobility"] == mobility[b]
        assert rec["rows_sorted_unique"] is True
        assert rec["subroots_passed"] == mobility[b]
        assert rec["union_missing"] == 0 and rec["union_extra"] == 0
        mine = next(r for r in cert_report if r["bit"] == b)
        assert rec["strategy_rows"] == mine["nRows"]
        assert rec["consumed_winner_rows"] == mine["nRows"]
        assert rec["terminal_range"] == [13, 17]
        local_bigint[b] = rec
    checks["C10_local_bigint_116_120"] = {
        str(b): {"union_missing": r["union_missing"],
                 "union_extra": r["union_extra"],
                 "subroots_passed": r["subroots_passed"]}
        for b, r in local_bigint.items()}
    # cross-check the third-verification record (six certificates)
    third_bits = {c["bit"]: c for c in third["certificates"]}
    assert len(third_bits) == 6
    for b, c in third_bits.items():
        mine = next(r for r in cert_report if r["bit"] == b)
        assert c["root_hex"] == mine["root_hex"]
        assert c["bytes"] == mine["bytes"]
        assert c["blob_sha"] == mine["git_blob_sha"]
        assert c["strategy_rows"] == mine["nRows"]
        assert c["root_mobility"] == mine["mobility"]
        assert c["union_missing"] == 0 and c["union_extra"] == 0
    assert third["summary"]["union_missing"] == 0
    assert third["summary"]["union_extra"] == 0
    assert third["summary"]["published_certificate_files_in_target_directory"] \
        == third["summary"]["independently_verified"] == 6
    checks["C8_third_verification_crosscheck"] = sorted(third_bits)
    print(f"CONTROL 23 certificates byte-verified (21 with published "
          f"BigInt/Bareiss records, bits 116/120 locally re-verified with "
          f"the published BigInt verifier); third-verification record "
          f"cross-checked for bits {sorted(third_bits)}")

    # ---------- 5. conflict census ----------------------------------------
    for b in cands:
        c = canon(child_v | (1 << b))
        if b in win:
            assert c not in folded_canons
    win_canons = [canon(child_v | (1 << b)) for b in win]
    assert len(set(win_canons)) == 23
    overlaps = [b for b in cands
                if canon(child_v | (1 << b)) in folded_canons]
    assert not overlaps
    assert prereg["totals"]["conflict_census_overlaps"] == 0
    assert prereg["totals"]["pairwise_distinct_d4_canons"] is True
    # the published census marked all 64 bits open at head 1452
    tbl = census["bit_tables"].get(CHILD)
    assert tbl is not None and tbl["parent"] == PARENT_A
    assert len(tbl["bits"]) == 64
    assert all(x["status"] == "open" for x in tbl["bits"])
    for x in tbl["bits"]:            # published root canons re-derived
        assert f"{canon(child_v | (1 << x['bit'])):0{HEX}x}" == \
            x["root_canon"], x
    # the child is genuinely open at head 1452 on its two class-2 parents
    rem, uniq, dem, _ = frontier(solved)
    assert CHILD in uniq and CHILD in dem
    assert dem[CHILD] == {"c1": 0, "c2": 2, "c4": 0}
    assert PARENT_A in rem and PARENT_B in rem
    assert classes[PARENT_A] == 2 and classes[PARENT_B] == 2
    checks["C9_conflict_census"] = {"overlaps": 0, "win_canons": 23,
                                    "child_open_parents": 2}
    print("CONTROL conflict census: 0 overlaps, 23 pairwise-distinct WIN "
          "canons, child open on both class-2 parents at head 1452")

    # ---------- 6. independent fold projection ----------------------------
    receipts = []
    for b in win:                       # ascending bit order (prereg order)
        root = child_v | (1 << b)
        cov = covers(root)
        marg = cov - solved
        marg_m = marg & manifest
        receipts.append({
            "bit": b, "root_hex": f"{root:0{HEX}x}",
            "d4_canonical_hex": f"{canon(root):0{HEX}x}",
            "covers": len(cov), "marginal": len(marg),
            "marginal_hexes": sorted(f"{x:0{HEX}x}" for x in marg),
            "marginal_in_manifest": len(marg_m),
            "marginal_manifest_hexes": sorted(f"{x:0{HEX}x}" for x in marg_m),
            "d4_orbit_distinct_from_all_folded_roots":
                canon(root) not in folded_canons})
        solved |= cov
        folded_canons.add(canon(root))
    st_after = summary(solved)
    projected_head = {k: st_after[k] for k in keys}
    # closed manifest rows = union of in-manifest marginals
    closed_rows = sorted({h for r in receipts
                          for h in r["marginal_manifest_hexes"]})
    child_closed_by = [r["bit"] for r in receipts
                       if CHILD in r["marginal_manifest_hexes"]]
    assert len(child_closed_by) == 1
    # demand histogram deltas
    deltas = {}
    for k in hist_before:
        d = st_after["hist"].get(k, 0) - hist_before[k]
        deltas[k] = d
    # affected parents
    rem2, uniq2, dem2, _ = frontier(solved)
    before_by_parent = defaultdict(list)
    for p, rows in rem.items():
        before_by_parent[p] = [r for r in rows]
    after_by_parent = defaultdict(list)
    for p, rows in rem2.items():
        after_by_parent[p] = [r for r in rows]
    affected = {}
    incid = 0
    cost_delta = 0
    closed_set = set(closed_rows)
    for p in sorted(before_by_parent):
        rows_b = {r["s6_hex"] for r in before_by_parent[p]}
        rows_a = {r["s6_hex"] for r in after_by_parent.get(p, [])}
        lost = sorted(rows_b - rows_a)
        if not lost:
            continue
        assert set(lost) <= closed_set
        cb = sum(int(r["s6_s7_edge_cost"]) for r in before_by_parent[p])
        ca = sum(int(r["s6_s7_edge_cost"]) for r in after_by_parent.get(p, []))
        assert cb - ca == sum(int(next(
            r["s6_s7_edge_cost"] for r in before_by_parent[p]
            if r["s6_hex"] == h)) for h in lost)
        affected[p] = {
            "s5_hex": p, "classes": classes[p],
            "rows_before": len(rows_b), "rows_after": len(rows_a),
            "edge_cost_before": cb, "edge_cost_after": ca,
            "lost_edge_cost": cb - ca, "lost_rows_hexes": lost}
        incid += len(lost)
        cost_delta += cb - ca
    # closed row -> parent map (from the incidences basis)
    closed_map = {}
    for h in closed_rows:
        closed_map[h] = sorted({r["s5_hex"] for r in incidences
                                if r["s6_hex"] == h})
    # verify every closed row was open at 1452 and is covered by a receipt
    for h in closed_rows:
        assert h in uniq, h
        assert h not in uniq2, h

    # ---------- 7. field-by-field agreement with the pre-registration -----
    agree = {}
    agree["win_bits_in_fold_order"] = \
        prereg["win_bits_in_fold_order"] == win
    agree["receipts"] = prereg["receipts"] == receipts
    agree["totals"] = (prereg["totals"]["receipts"] == 23 and
                       prereg["totals"]["total_marginal"] ==
                       sum(r["marginal"] for r in receipts) and
                       prereg["totals"]["total_marginal_in_manifest"] ==
                       sum(r["marginal_in_manifest"] for r in receipts) and
                       prereg["totals"]["closed_manifest_rows"] ==
                       closed_rows and
                       prereg["totals"]["child_closed_by_bit"] ==
                       child_closed_by[0] and
                       prereg["totals"]["conflict_census_overlaps"] == 0 and
                       prereg["totals"]["pairwise_distinct_d4_canons"] is True)
    agree["basis_head"] = prereg["basis_head"] == 1452
    agree["projected_head"] = prereg["projected_head"] == projected_head
    agree["projected_demand_histogram"] = \
        prereg["projected_demand_histogram"] == st_after["hist"]
    agree["demand_histogram_deltas"] = \
        prereg["demand_histogram_deltas"] == deltas
    agree["affected_parents"] = prereg["affected_parents"] == affected
    agree["parent_row_incidences"] = \
        prereg["parent_row_incidences"] == incid
    agree["parent_edge_cost_delta"] = \
        prereg["parent_edge_cost_delta"] == cost_delta
    agree["closed_row_parent_map"] = \
        prereg["closed_row_parent_map"] == closed_map
    agree["child"] = (prereg["child"]["s6_hex"] == CHILD and
                      prereg["child"]["legal_candidates"] == 64 and
                      prereg["child"]["closed_by_receipt_bit"] ==
                      child_closed_by[0] and
                      prereg["child"]["open_at_basis_head"] is True and
                      prereg["child"]["demand_at_1452"] ==
                      {"c1": 0, "c2": 2, "c4": 0} and
                      prereg["child"]["d4_canonical_hex"] == CHILD)
    checks["C11_prereg_field_agreement"] = {k: bool(v)
                                           for k, v in agree.items()}
    assert all(agree.values()), {k: v for k, v in agree.items() if not v}
    print(f"CONTROL pre-registration agreement: "
          f"{sum(1 for v in agree.values() if v)}/{len(agree)} "
          "field groups identical")

    result = {
        "schema": "n11-class2-lane-cost64h-prereg-independent-agreement-"
                  "20261116-v1",
        "date": "2026-11-16",
        "role": ("second-implementation agreement check: this lane did not "
                 "run the cost-64h sweep, did not extract the certificates "
                 "and did not write the pre-registration; every consumed "
                 "artifact is blob-pinned and independently re-derived "
                 "here in a fresh environment"),
        "preregistration": {
            "json": PREREG_JSON, "git_blob_sha": PREREG_BLOB,
            "git_commit": PREREG_COMMIT,
            "published_before_fold_receipt_lands":
                prereg["published_before_fold_receipt_lands"]},
        "basis_reproduction": {
            "head_1452": list(HEAD_1452),
            "receipt_roots": 775, "distinct_d4_canons": 760,
            "fold_json": f"{FOLD76D77E_JSON} (git blob sha "
                          "8d4bc622f9da22b8754f2e398e5481359656d956)"},
        "sweep_rederivation": {
            "raw_batches": 8, "pilots": pilots,
            "win7_d10_bits": win, "refuted_d10_count": len(refuted),
            "capped_count": 0, "node_sum": node_sum,
            "v15_crosscheck": {"pilot_nodes": 5949,
                               "win_bits_loss_true": v15_win,
                               "node_sum": v15_node_sum},
            "published_rerun_record": rerun["checks"]},
        "certificates": {
            "count": 23,
            "bytes_total": sum(r["bytes"] for r in cert_report),
            "bigint_records_published": 21,
            "bareiss_records_published": 21,
            "records_gap_note": ("bits 116 and 120 have no published "
                                 "BigInt/Bareiss records on main at check "
                                 "time and bit 120 also lacks its summary "
                                 "(the certificate-auxiliary publication "
                                 "wave stopped after bit 116's summary; a "
                                 "local mirror of bit 120's summary was a "
                                 "404 placeholder and was removed); both "
                                 "certificates are byte-pinned here and "
                                 "were locally re-verified with the "
                                 "published independent BigInt verifier"),
            "local_bigint_verification": {
                "verifier": ("verify_win7_certificate_bigint_independent"
                              ".mjs (git blob sha 62b5d9413daafb172f6e1024"
                              "9976ee6808f7b454, fetched byte-faithfully "
                              "from main and re-hashed here)"),
                "records": {str(b): r for b, r in local_bigint.items()}},
            "per_bit": cert_report},
        "conflict_census": {
            "candidate_overlaps_with_folded_roots": 0,
            "win_canons_pairwise_distinct": True,
            "child_open_class2_parents": [PARENT_A, PARENT_B]},
        "independent_projection": {
            "win_bits_in_fold_order": win,
            "receipts": receipts,
            "totals": {
                "receipts": 23,
                "total_marginal": sum(r["marginal"] for r in receipts),
                "total_marginal_in_manifest":
                    sum(r["marginal_in_manifest"] for r in receipts),
                "closed_manifest_rows": closed_rows,
                "child_closed_by_bit": child_closed_by[0]},
            "projected_head": projected_head,
            "demand_histogram_deltas": deltas,
            "affected_parents": affected,
            "parent_row_incidences": incid,
            "parent_edge_cost_delta": cost_delta,
            "closed_row_parent_map": closed_map},
        "agreement": {k: bool(v) for k, v in agree.items()},
        "checks": checks,
        "interpretation_guard": ("bookkeeping verification only; no engine "
                                "search was run, no verdict was created and "
                                "no row was closed by this script; the "
                                "23-receipt fold projection is a projection "
                                "until the fold receipt lands and is "
                                "recomputed; solved counts measure manifest "
                                "coverage, not the game-theoretic value of "
                                "any position; WIN7 certificates prove a "
                                "first-player win within depth 10 from the "
                                "individual 7-stone roots only; REFUTED-D10 "
                                "is not a LOSS proof; the 11x11 empty board, "
                                "two-stone roots {49,60} and {59,60}, S2 "
                                "{59,60} and classes 1/2/4 all remain "
                                "UNKNOWN"),
    }
    out_path = OUT / ("class2-lane-cost64h-prereg-independent-agreement-"
                      "20261116.json")
    with open(out_path, "w") as f:
        json.dump(result, f, indent=1, sort_keys=True)
        f.write("\n")
    print("wrote", out_path.name, "blob",
          git_blob_sha(out_path.read_bytes())[:12])
    print("ALL CONTROLS PASS")


if __name__ == "__main__":
    main()
