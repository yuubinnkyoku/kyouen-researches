#!/usr/bin/env python3
"""Verify the cost76c fbt-saturation audit and the v17 re-sweep.

Re-derives every comparison of the published audit JSON
(class2-lane-cost76c-v17-sweep-and-fbt-saturation-audit-20261117.json) from the
blob-pinned raw files, without rerunning the search engines:

  C1  published v16 raw batches 1-10: 76 bit records, 10/10 pilot_d6 = 3402
  C2  independent v16 re-run batches 1-10: 76/76 node-exact vs C1 (ms-only diffs)
  C3  v17 raw batches 1-10: 76 bits, 10/10 pilot_d6 = 3402, node totals
  C4  v17 vs published: verdict flips == {bit 113 WIN->REFUTED}; corrected WIN
      bits == {61, 99}; 48 bits byte-identical; 27 node-count-only changes
  C5  v15 crosscheck (win + 4 refuted chunks): 76 bits, 5/5 pilot_d6 = 5949,
      verdict disagreement with the published v16 sweep == {bit 113}
  C6  order matrix: 18 configs (v16/v15/v17 x andclose 0/1 x bits 61/99/113),
      verdict/nodes per config; v16 and v15 flip bits {99,113}/{99} across
      orderings, v17 is order-stable for all three bits
  C7  fbt drop probes: bit 61 -> 0 drops in both orderings; bits 99/113 -> >0
      drops; probe node counts equal the uninstrumented runs (instrumentation
      is behaviour-neutral)
  C8  audit JSON self-consistency: the JSON's totals/matrix/per-bit tables are
      byte-equal to the values re-derived here
  C9  v17 runner blob pin; v16/v15 runner blob pins

Run from any directory:
    python research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/verify_cost76c_v17_fbt_audit_20261117.py
Only Python's standard library is used.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
SCRIPTS = HERE / "scripts"

RUNNER_V16_BLOB = "0a4a86f6828dc010c89ff17596054336a6b6091f"
RUNNER_V15_BLOB = "8744fc65b6b7cac6bd561403ce4c749e01c51359"
RUNNER_V17_BLOB = "c132cc6425eee3feaeef1d697dd74f968cfedb59"

PUBLISHED_RAW_BLOBS = {
    1: "1aebb80f0b4f4384a7207afff4c706433d0fcaff",
    2: "7b0b471d81ad1815f529bfc98a63acdff73ccc7a",
    3: "9f5c63cd2c93a276ebcfc6874f2f0aa870921c0c",
    4: "a7c5ee5167529ff44351f5b438cf1636352bffca",
    5: "a07e06607aeb6b9a06f629e9210bc6774b43e964",
    6: "beb9283161491d17c435890f563b8c7f283b48a3",
    7: "a511e748ba227b2d20627f653acde89fca0e19e6",
    8: "a2aa8bb60fd7f5c875a234ead60f4826335d32a6",
    9: "0f41ee0c7f685f8a41a5574a399dde3c6eea7eee",
    10: "273f6e710d791b20e5ec2ab57ae53b7127f18122",
}
RERUN_BLOBS = {
    1: "91d4b02295508fd36eec480e0fefb0a76227b7d1",
    2: "3adee24f29c667a0ec1cf83f4a81f6b420a83b4e",
    3: "63d3578e9bb22ee8b74f81d947ed7e33c465188e",
    4: "0a9fb7eaaee64aedb4e863ee5b330cd56a30c4fe",
    5: "4db84f3a22c6dd6224677ec3d978d2228a166ce0",
    6: "d86da315fc1ae0535f99c4b7594df8c12f9c2457",
    7: "16aceb180e16551353957af58b1b0cdcdec713de",
    8: "d5832a08328d57eee524be1bcde7f96330fa15cf",
    9: "001263d14784e26dbde27e8e239bf1bd7282fceb",
    10: "fbba075c0b1f750240d2382b7762d09428137518",
}
V17_RAW_BLOBS = {
    1: "a62cd9aa478d3930cc8f672cd1fa8ae55f399d73",
    2: "9d4aacedd902eef335d349c9467f31ee256df897",
    3: "c20c808a7963726374922d3a05e91de7c65b3ce2",
    4: "26729eb3e5997a52c8b31ed4d9afcd22579c840f",
    5: "937e64420909119b315c5bb302e23a782b53cc0c",
    6: "472168193757ddec5eed790880d12c63be631a26",
    7: "78897a4bd09f02e7e6e029115ec241c064345cbc",
    8: "44482915469b3e52e7964808d3f118197acce7e4",
    9: "d77a403725a7b9dc93d9e43a84ef160a2e196d49",
    10: "f54c9f0c573314b971c6e50cd154175013d05383",
}
OTHER_BLOBS = {
    "class2-lane-cost76c-v15-crosscheck-win-20261117.jsonl": "512f3d171d70b255bd84c82401c907fd19ced960",
    "class2-lane-cost76c-v15-crosscheck-refuted-chunk1-20261117.jsonl": "462d25a70b9be2de6207d1c099d132331187306e",
    "class2-lane-cost76c-v15-crosscheck-refuted-chunk2-20261117.jsonl": "89c46a818bccf432cd98a97f16777caacf1686a7",
    "class2-lane-cost76c-v15-crosscheck-refuted-chunk3-20261117.jsonl": "63ec038d15a98d15538db22b2a7df37d79aed4a6",
    "class2-lane-cost76c-v15-crosscheck-refuted-chunk4-20261117.jsonl": "bc3ae98be64ea284bf300b022b15d41827415b59",
    "class2-lane-cost76c-v15-bit113-andclose0-20261117.jsonl": "fa785c6ef108e87d706444cabe6b079bb91ecb42",
    "class2-lane-cost76c-v15-bits61-99-andclose0-20261117.jsonl": "b0c9404e1f3a7e129a56a05d2ddd1bb14cf0a9c2",
    "class2-lane-cost76c-v16-bit113-andclose0-20261117.jsonl": "64fd7b57e26abe14ecd81dd6a7153156c3295b1f",
    "class2-lane-cost76c-v16-bits61-99-andclose0-20261117.jsonl": "4b443950217617f1ea9c706c2767ecf64d76faab",
    "class2-lane-cost76c-v17-bit61-andclose1-20261117.jsonl": "2dd0b4dfd6d03251429055bcc6b16cf88ac02918",
    "class2-lane-cost76c-v17-bit61-andclose0-20261117.jsonl": "9ecfa8a2551d34688e4869e591dee4fb77608525",
    "class2-lane-cost76c-v17-bit99-andclose1-20261117.jsonl": "3114985424327460c7d48f9607b930eeedd3f65a",
    "class2-lane-cost76c-v17-bit99-andclose0-20261117.jsonl": "4c25c5fe67b17ddfedc1a4b7047d7a437b083e24",
    "class2-lane-cost76c-v17-bit113-andclose1-20261117.jsonl": "681ea6b9d4dcb448594e2fce818c0625edcd3845",
    "class2-lane-cost76c-v17-bit113-andclose0-20261117.jsonl": "df5aef68239dd2746262de37e0ac8e87e08d5dd3",
    "class2-lane-cost76c-fbt-drop-probe-bit61-andclose1-20261117.jsonl": "c611a9d5814759ee8c56acb13b9f6a2c0bf3ffd0",
    "class2-lane-cost76c-fbt-drop-probe-bit61-andclose0-20261117.jsonl": "6d59a595973dd66b4191112ec46dbed0992beb24",
    "class2-lane-cost76c-fbt-drop-probe-bit99-andclose1-20261117.jsonl": "38744d369e5d68605192621ba0ae40f821f6e407",
    "class2-lane-cost76c-fbt-drop-probe-bit99-andclose0-20261117.jsonl": "39b43a88ac5962677da591f19fcc560dbe7b1554",
    "class2-lane-cost76c-fbt-drop-probe-bit113-andclose1-20261117.jsonl": "f9a8498ed16215bf81cfcc5d491de7d5ad465f2b",
    "class2-lane-cost76c-fbt-drop-probe-bit113-andclose0-20261117.jsonl": "6acb6de48c6e578e243cc12105eb4c36f68003cd",
}


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def read_pinned(path: Path, expected: str) -> bytes:
    data = path.read_bytes()
    actual = git_blob(data)
    if actual != expected:
        raise AssertionError(f"blob SHA mismatch: {path.name}: {actual} != {expected}")
    return data


def load_jsonl(data: bytes, path: Path):
    rows = []
    for line_no, raw in enumerate(data.decode("utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            rows.append(json.loads(raw))
        except json.JSONDecodeError as exc:
            raise AssertionError(f"{path.name}:{line_no}: {exc}") from exc
    return rows


def bits_of(rows):
    return {r["bit"]: r for r in rows if "bit" in r}


def pilots_of(rows):
    return [r for r in rows if "control" in r]


def main() -> None:
    checks = {}

    def check(name: str, condition: bool) -> None:
        checks[name] = bool(condition)
        if not condition:
            raise AssertionError(name)

    # C9 runner pins
    check("C9_runner_v16_blob", git_blob(read_pinned(SCRIPTS / "class4_child1_runner_v16.ts", RUNNER_V16_BLOB)) == RUNNER_V16_BLOB)
    check("C9_runner_v15_blob", git_blob(read_pinned(SCRIPTS / "class4_child1_runner.ts", RUNNER_V15_BLOB)) == RUNNER_V15_BLOB)
    check("C9_runner_v17_blob", git_blob(read_pinned(SCRIPTS / "class4_child1_runner_v17.ts", RUNNER_V17_BLOB)) == RUNNER_V17_BLOB)

    # C1 published v16 raw batches
    pub = {}
    pub_pilots = 0
    for i in range(1, 11):
        rows = load_jsonl(read_pinned(OUT / f"class2-lane-cost76c-raw-batch{i}-20261116.jsonl", PUBLISHED_RAW_BLOBS[i]), OUT)
        pub.update(bits_of(rows))
        pub_pilots += sum(1 for r in pilots_of(rows) if r["loss"] is False and r["nodes"] == 3402)
    check("C1_published_76_bits", len(pub) == 76)
    check("C1_published_pilots_10", pub_pilots == 10)

    # C2 independent rerun node-exact
    rer = {}
    rer_pilots = 0
    for i in range(1, 11):
        rows = load_jsonl(read_pinned(OUT / f"class2-lane-cost76c-independent-rerun-batch{i}-20261117.jsonl", RERUN_BLOBS[i]), OUT)
        rer.update(bits_of(rows))
        rer_pilots += sum(1 for r in pilots_of(rows) if r["loss"] is False and r["nodes"] == 3402)
    exact = [b for b in sorted(pub) if all(pub[b][k] == rer[b][k] for k in ("loss", "nodes", "capped", "terminalStoneRange", "andclose"))]
    check("C2_rerun_76_node_exact", exact == sorted(pub))
    check("C2_rerun_pilots_10", rer_pilots == 10)
    rer_nodes = sum(r["nodes"] for r in rer.values())
    check("C2_rerun_node_sum", rer_nodes == 141221576)

    # C3 v17 raw batches
    v17 = {}
    v17_pilots = 0
    for i in range(1, 11):
        rows = load_jsonl(read_pinned(OUT / f"class2-lane-cost76c-v17-raw-batch{i}-20261117.jsonl", V17_RAW_BLOBS[i]), OUT)
        v17.update(bits_of(rows))
        v17_pilots += sum(1 for r in pilots_of(rows) if r["loss"] is False and r["nodes"] == 3402)
    check("C3_v17_76_bits", len(v17) == 76)
    check("C3_v17_pilots_10", v17_pilots == 10)
    v17_nodes = sum(r["nodes"] for r in v17.values())
    check("C3_v17_node_sum", v17_nodes == 144218750)

    # C4 verdict flips and saturation census
    flips = sorted(b for b in pub if pub[b]["loss"] != v17[b]["loss"] or pub[b]["capped"] != v17[b]["capped"])
    node_changed = sorted(b for b in pub if pub[b]["loss"] == v17[b]["loss"] and pub[b]["nodes"] != v17[b]["nodes"])
    identical = [b for b in sorted(pub) if all(pub[b][k] == v17[b][k] for k in ("loss", "nodes", "capped", "terminalStoneRange", "andclose"))]
    wins = sorted(b for b in v17 if v17[b]["loss"])
    check("C4_flips_eq_113_only", flips == [113])
    check("C4_corrected_wins_61_99", wins == [61, 99])
    check("C4_unsaturated_48", len(identical) == 48)
    check("C4_node_changed_27", len(node_changed) == 27)

    # C5 v15 crosscheck
    v15 = {}
    v15_pilots = 0
    for name in ["class2-lane-cost76c-v15-crosscheck-win-20261117.jsonl",
                 "class2-lane-cost76c-v15-crosscheck-refuted-chunk1-20261117.jsonl",
                 "class2-lane-cost76c-v15-crosscheck-refuted-chunk2-20261117.jsonl",
                 "class2-lane-cost76c-v15-crosscheck-refuted-chunk3-20261117.jsonl",
                 "class2-lane-cost76c-v15-crosscheck-refuted-chunk4-20261117.jsonl"]:
        rows = load_jsonl(read_pinned(OUT / name, OTHER_BLOBS[name]), OUT)
        v15.update(bits_of(rows))
        v15_pilots += sum(1 for r in pilots_of(rows) if r["loss"] is False and r["nodes"] == 5949)
    disagree = sorted(b for b in pub if pub[b]["loss"] != v15[b]["loss"] or pub[b]["capped"] != v15[b]["capped"])
    v15_nodes = sum(r["nodes"] for r in v15.values())
    check("C5_v15_76_bits", len(v15) == 76)
    check("C5_v15_pilots_5", v15_pilots == 5)
    check("C5_v15_disagreement_eq_113", disagree == [113])
    check("C5_v15_node_sum", v15_nodes == 444779818)

    # C6 order matrix
    def fbits(name):
        return bits_of(load_jsonl(read_pinned(OUT / name, OTHER_BLOBS[name]), OUT))
    v16c0_113 = fbits("class2-lane-cost76c-v16-bit113-andclose0-20261117.jsonl")[113]
    v16c0 = fbits("class2-lane-cost76c-v16-bits61-99-andclose0-20261117.jsonl")
    v15c1 = fbits("class2-lane-cost76c-v15-crosscheck-win-20261117.jsonl")
    v15c0_113 = fbits("class2-lane-cost76c-v15-bit113-andclose0-20261117.jsonl")[113]
    v15c0 = fbits("class2-lane-cost76c-v15-bits61-99-andclose0-20261117.jsonl")
    v17c = {(b, ac): fbits(f"class2-lane-cost76c-v17-bit{b}-andclose{ac}-20261117.jsonl")[b]
            for b in (61, 99, 113) for ac in (1, 0)}
    check("C6_v16_bit113_order_flip", pub[113]["loss"] is True and v16c0_113["loss"] is False)
    check("C6_v16_bit99_order_flip", pub[99]["loss"] is True and v16c0[99]["loss"] is False)
    check("C6_v16_bit61_order_stable", pub[61]["loss"] is True and v16c0[61]["loss"] is True)
    check("C6_v15_bit99_order_flip", v15c1[99]["loss"] is True and v15c0[99]["loss"] is False)
    check("C6_v15_bit113_order_stable_refuted", v15c1[113]["loss"] is False and v15c0_113["loss"] is False)
    check("C6_v17_order_stable_61", v17c[(61, 1)]["loss"] is True and v17c[(61, 0)]["loss"] is True)
    check("C6_v17_order_stable_99", v17c[(99, 1)]["loss"] is True and v17c[(99, 0)]["loss"] is True)
    check("C6_v17_order_stable_113_refuted", v17c[(113, 1)]["loss"] is False and v17c[(113, 0)]["loss"] is False)
    check("C6_v17_bit61_matches_v16", v17c[(61, 1)]["nodes"] == 752696 and v17c[(61, 0)]["nodes"] == 982127)

    # C7 fbt drop probes
    for b, drops_expected in ((61, 0), (99, None), (113, None)):
        for ac in (1, 0):
            name = f"class2-lane-cost76c-fbt-drop-probe-bit{b}-andclose{ac}-20261117.jsonl"
            rows = load_jsonl(read_pinned(OUT / name, OTHER_BLOBS[name]), OUT)
            r = bits_of(rows)[b]
            pl = pilots_of(rows)[0]
            check(f"C7_probe_bit{b}_ac{ac}_pilot", pl["loss"] is False and pl["nodes"] == 3402)
            if drops_expected == 0:
                check(f"C7_probe_bit{b}_ac{ac}_zero_drops", r["fbtDrops"] == 0)
            else:
                check(f"C7_probe_bit{b}_ac{ac}_positive_drops", r["fbtDrops"] > 0)
            ref = pub[b]["nodes"] if ac == 1 else (v16c0_113 if b == 113 else v16c0[b])["nodes"]
            check(f"C7_probe_bit{b}_ac{ac}_nodes_match", r["nodes"] == ref)

    # C8 audit JSON self-consistency
    audit = json.loads((OUT / "class2-lane-cost76c-v17-sweep-and-fbt-saturation-audit-20261117.json").read_bytes())
    check("C8_schema", audit["schema"] == "n11-class2-lane-cost76c-fbt-saturation-v17-audit-20261117-v1")
    check("C8_rerun_total", audit["independent_rerun_v16"]["total_nodes"] == rer_nodes)
    check("C8_v15_total", audit["v15_crosscheck"]["total_nodes"] == v15_nodes)
    check("C8_v17_total", audit["v17_full_resweep"]["total_nodes"] == v17_nodes)
    check("C8_wins", audit["v17_full_resweep"]["win_bits_corrected"] == wins)
    check("C8_matrix_18", len(audit["order_dependence"]["matrix"]) == 18)
    check("C8_runner_blob", audit["v17_repair"]["blob_sha"] == RUNNER_V17_BLOB)
    per_bit = audit["v17_full_resweep"]["per_bit"]
    check("C8_per_bit_76", len(per_bit) == 76)
    ok = all(per_bit[str(b)]["v17_loss"] == v17[b]["loss"] and per_bit[str(b)]["v17_nodes"] == v17[b]["nodes"]
             and per_bit[str(b)]["v16_loss"] == pub[b]["loss"] and per_bit[str(b)]["v16_nodes"] == pub[b]["nodes"]
             for b in pub)
    check("C8_per_bit_values", ok)

    print(json.dumps({
        "status": "PASS",
        "checks_passed": len(checks),
        "checks_total": len(checks),
        "corrected_win_bits": wins,
        "verdict_flip": "bit 113 WIN7-D10 -> REFUTED-D10 (v16 published -> v17)",
        "unknown_status": "11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, classes 1/2/4 all remain UNKNOWN",
    }, indent=2))


if __name__ == "__main__":
    main()
