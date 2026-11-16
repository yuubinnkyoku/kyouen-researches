#!/usr/bin/env python3
"""Reconcile the cost76c manifest projection with the repaired v17 sweep.

The geometry is not recomputed from scratch here: the prior pinned projection
already records the ordered marginal cover sets for bits 61, 99, and 113.
The v17 raw batches are independently reaggregated, bit 113 is removed because
its verdict changed to REFUTED-D10, and the remaining two-candidate projection
is derived by deleting bit 113's four final, non-manifest marginal orbits.
"""
import copy
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
OLD_PATH = OUT / "class2-lane-cost76c-candidate-manifest-marginals-20261117.json"
V17_PATH = OUT / "class2-lane-cost76c-v17-sweep-and-fbt-saturation-audit-20261117.json"
CLAIM_INPUT_PATH = OUT / "class2-lane-cost76c-claim-input-20261117.json"
OUTPUT_PATH = OUT / "class2-lane-cost76c-v17-corrected-candidate-manifest-marginals-20261117.json"

OLD_BLOB = "96916b0659a3366290882d29ff46158425058188"
V17_BLOB = "235f964365a7ab33e33986c915fc7f6861e4d686"
CLAIM_INPUT_BLOB = "8932f2d5e100325549a5f251a1d883558cae0708"
RUNNER_V17_BLOB = "c132cc6425eee3feaeef1d697dd74f968cfedb59"
RAW_BLOBS = {
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

def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()

def read_pinned(path: Path, expected: str):
    data = path.read_bytes()
    got = git_blob_sha(data)
    assert got == expected, f"{path.name}: blob {got} != {expected}"
    return json.loads(data.decode("utf-8"))

def main():
    old = read_pinned(OLD_PATH, OLD_BLOB)
    v17 = read_pinned(V17_PATH, V17_BLOB)
    claim_input = read_pinned(CLAIM_INPUT_PATH, CLAIM_INPUT_BLOB)
    per_bit = v17["v17_full_resweep"]["per_bit"]

    # Reaggregate all ten raw v17 batches rather than trusting the audit summary.
    raw_rows = []
    for batch, expected_blob in RAW_BLOBS.items():
        path = OUT / f"class2-lane-cost76c-v17-raw-batch{batch}-20261117.jsonl"
        data = path.read_bytes()
        got = git_blob_sha(data)
        assert got == expected_blob, f"{path.name}: blob {got} != {expected_blob}"
        raw_rows.extend(json.loads(line) for line in data.decode("utf-8").splitlines() if line)

    pilots = [r for r in raw_rows if r.get("control") == "pilot_d6"]
    bits = [r for r in raw_rows if isinstance(r.get("bit"), int)]
    by_bit = {r["bit"]: r for r in bits}
    legal = claim_input["legal_candidates"]
    assert len(raw_rows) == 86
    assert len(bits) == 76 and len(by_bit) == 76
    assert sorted(by_bit) == sorted(legal)
    assert len(pilots) == 10
    assert all(r["loss"] is False and r["nodes"] == 3402 and not r["capped"] for r in pilots)
    assert all(r["capped"] is False and r["andclose"] is True and
               r["terminalStoneRange"] == [13, 17] for r in bits)
    assert sum(r["nodes"] for r in bits) == 144_218_750

    # Every raw bit must agree with the v17 audit's per-bit table.
    for bit, raw in by_bit.items():
        rec = per_bit[str(bit)]
        assert raw["loss"] is rec["v17_loss"], bit
        assert raw["nodes"] == rec["v17_nodes"], bit
        assert raw["capped"] is False, bit

    winners = sorted(bit for bit, r in by_bit.items() if r["loss"] is True)
    refuted = sorted(bit for bit, r in by_bit.items() if r["loss"] is False)
    assert winners == [61, 99]
    assert len(refuted) == 74 and 113 in refuted

    # Cross-engine agreement on the three candidates: v15 and v17, andclose=1.
    matrix = v17["order_dependence"]["matrix"]
    cross_engine = {}
    for bit in (61, 99, 113):
        a = next(x for x in matrix if x["engine"] == "v15" and x["andclose"] == 1 and x["bit"] == bit)
        b = next(x for x in matrix if x["engine"] == "v17" and x["andclose"] == 1 and x["bit"] == bit)
        assert a["loss"] is b["loss"], bit
        cross_engine[str(bit)] = "WIN7-D10" if b["loss"] else "REFUTED-D10"

    # Restrict the already pinned three-candidate projection to the two v17 WIN roots.
    old_bits = [x["bit"] for x in old["single_candidate_projections"]]
    assert old_bits == [61, 99, 113]
    old_marginals = {x["bit"]: x for x in old["combined_projection"]["per_candidate_marginal"]}
    assert old["combined_projection"]["fold_order_bits"] == [61, 99, 113]
    assert old_marginals[61]["marginal_d4_s6_orbits"] == 5
    assert old_marginals[99]["marginal_d4_s6_orbits"] == 4
    assert old_marginals[113]["marginal_d4_s6_orbits"] == 4
    assert old_marginals[113]["marginal_manifest_rows"] == 0
    assert old["candidate_cover_union"]["distinct_d4_s6_orbits"] == 19
    assert old["candidate_cover_union"]["new_orbits_if_all_three_are_folded"] == 13
    assert old["candidate_cover_union"]["manifest_intersection"] == 7
    assert old["candidate_cover_union"]["already_covered_manifest_orbits_at_head1452"] == 6

    new_union = 19 - old_marginals[113]["marginal_d4_s6_orbits"]
    new_orbits = 13 - old_marginals[113]["marginal_d4_s6_orbits"]
    new_non_manifest = 12 - old_marginals[113]["marginal_d4_s6_orbits"]
    assert (new_union, new_orbits, new_non_manifest) == (15, 9, 8)

    out = copy.deepcopy(old)
    out["schema"] = "n11-class2-lane-cost76c-v17-corrected-candidate-manifest-marginals-20261117-v1"
    out["status"] = "v17-corrected two-WIN candidate projection; no certificate extracted; no fold"
    out["basis"].pop("head_after_all_three_cost76c_candidates", None)
    out["basis"]["head_after_all_two_cost76c_candidates"] = out["basis"]["head_after_any_one_cost76c_candidate"]

    out["candidate_cover_union"] = {
        "candidate_count": 2,
        "candidate_bits": [61, 99],
        "distinct_d4_s6_orbits": new_union,
        "manifest_intersection": 7,
        "already_covered_manifest_orbits_at_head1452": 6,
        "currently_open_manifest_orbits": 1,
        "currently_open_manifest_hexes": ["00000000010000809002000001000000"],
        "new_manifest_orbits_if_both_are_folded": 1,
        "new_non_manifest_orbits_if_both_are_folded": new_non_manifest,
        "new_orbits_if_both_are_folded": new_orbits,
        "outside_manifest_orbits": 8,
    }

    corrected_single = []
    for item in old["single_candidate_projections"]:
        if item["bit"] not in (61, 99):
            continue
        rec = copy.deepcopy(item)
        rec["v16_nodes"] = rec["nodes"]
        rec["nodes"] = by_bit[rec["bit"]]["nodes"]
        rec["nodes_source"] = "independently reaggregated v17 raw batch"
        corrected_single.append(rec)
    assert [x["bit"] for x in corrected_single] == [61, 99]
    out["single_candidate_projections"] = corrected_single

    out["combined_projection"]["fold_order_bits"] = [61, 99]
    out["combined_projection"]["per_candidate_marginal"] = [
        old_marginals[61], old_marginals[99]
    ]
    out["combined_projection"]["parent_effect_scope"] = (
        "The parent-row and parent-edge deltas below are the published bit61-first "
        "projection only; bit99 adds four D4 orbits but zero further manifest rows."
    )

    ratio99 = round(by_bit[99]["nodes"] / by_bit[61]["nodes"], 6)
    out["recommendation"] = {
        "first_certificate_extraction_bit": 61,
        "fallback_bits_if_extraction_fails": [99],
        "node_ratios_vs_bit61": {"61": 1.0, "99": ratio99},
        "reason": (
            "After excluding bit113 (v17 REFUTED-D10), bit61 contributes five new "
            "D4 S6 orbits and bit99 contributes four more. Both individually touch "
            "the same one open manifest row; in bit order the manifest marginals "
            "are 1/0. Bit61 has fewer v17 raw nodes (752696 vs 4140409)."
        ),
        "caveat": (
            "Raw search-node count is not certificate-extraction cost. Bit99 remains "
            "a backup WIN7-D10 search candidate, not a LOSS proof."
        ),
    }

    out["removed_candidate"] = {
        "bit": 113,
        "root_canon": "00000000040000809002000000400008",
        "v16_published": "WIN7-D10",
        "v17": "REFUTED-D10",
        "v16_nodes": 8174662,
        "v17_nodes": by_bit[113]["nodes"],
        "v15_v17_andclose1_agreement": True,
        "reason": "Excluded from certificate extraction and fold; the v17 repaired engine removes the v16 false-positive verdict.",
    }

    out["v17_raw_reaggregation"] = {
        "raw_records": len(raw_rows),
        "candidate_records": len(bits),
        "unique_candidate_bits": len(by_bit),
        "winner_bits": winners,
        "refuted_d10_count": len(refuted),
        "capped_count": sum(1 for r in bits if r["capped"]),
        "candidate_nodes": sum(r["nodes"] for r in bits),
        "pilot_count": len(pilots),
        "pilot_nodes_each": 3402,
        "terminal_stone_range": [13, 17],
        "andclose": True,
        "raw_batch_blob_pins": {str(k): v for k, v in RAW_BLOBS.items()},
        "v15_v17_andclose1_agreement": cross_engine,
        "checks": {
            "legal_candidate_set_exact": True,
            "no_duplicate_bits": True,
            "all_pilots_exact": True,
            "all_uncapped": True,
            "all_terminal_ranges_exact": True,
            "all_v17_per_bit_records_match": True,
        },
    }

    out["source_blob_pins"] = {
        "prior_three_candidate_projection": OLD_BLOB,
        "v17_fbt_saturation_audit": V17_BLOB,
        "claim_input_snapshot": CLAIM_INPUT_BLOB,
        "v17_runner": RUNNER_V17_BLOB,
        "raw_batches": {str(k): v for k, v in RAW_BLOBS.items()},
    }
    out["interpretation_guard"] = (
        "This is a corrected projection over two v17 WIN7-D10 candidates. "
        "The v17 raw sweep was independently reaggregated from all ten raw batches. "
        "The D4 cover geometry is a restriction of the prior pinned three-candidate "
        "projection after removing bit113's final four non-manifest marginal orbits; "
        "no new geometric engine run was performed. No certificate was extracted or "
        "independently verified, and no receipt fold was applied. REFUTED-D10 is not "
        "a LOSS proof. The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, "
        "S2 {59,60}, and classes 1/2/4 remain UNKNOWN."
    )

    OUTPUT_PATH.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
