#!/usr/bin/env python3
"""Rank the three cost76c WIN7-D10 candidates by *current MS5 manifest
marginal*, using the published independent head-1450 projection tool.

This is a bookkeeping audit only. It does not extract or verify certificates,
does not create verdicts, and does not change the canonical head.
"""
import csv
import hashlib
import json
import runpy
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
MS5 = HERE.parent / "n11-s2-5960-milestone5-20261112" / "output"
SCRIPTS = HERE / "scripts"

TOOL = SCRIPTS / "fold_projection_head1450_tool_20261116.py"
C66C_SCRIPT = SCRIPTS / "recompute_frontier_cost66c_receipts_20261116.py"
BASELINE_JSON = OUT / "class2-lane-fold-projection-basis1450-4roots-20261116.json"
FOLD7677_JSON = OUT / "class-frontier-cost76d77e-receipts-recompute-20261116.json"
CLAIM_INPUT_JSON = OUT / "class2-lane-cost76c-claim-input-20261117.json"
RAW_AUDIT_JSON = OUT / "class2-lane-cost76c-raw-audit-20261117.json"
PRESWEEP_JSON = OUT / "class2-lane-next-target-presweep-1452-20261116.json"
OUTPUT_JSON = OUT / "class2-lane-cost76c-candidate-manifest-marginals-20261117.json"

BLOBS = {
    "tool": "49fcd8ae6706c075b39eea5b115b2a045c2950cf",
    "cost66c_script": "898cfa614e63049e52f19f080cdc398a22e0f6c9",
    "cost66c_fold": "8783993e5c73cc9697c3ca48aef981725f422be8",
    "baseline_1452_projection": "005423113c601301e2b5c208d1138e17283cb774",
    "cost76d77e_fold": "8d4bc622f9da22b8754f2e398e5481359656d956",
    "cost76c_claim_input": "8932f2d5e100325549a5f251a1d883558cae0708",
    "cost76c_raw_audit": "7160490ce5d49f732acdecbf629fc0d79e6081ef",
    "head1452_presweep": "0d9a94a272de9fe45708757f17bfea60239a3c9b",
}

HEAD_KEYS = (
    "solved_s6_in_manifest", "remaining_s5_orbits", "unique_remaining_s6",
    "sum_remaining_cost", "s6_needed_by_open_classes",
    "cost_needed_by_open_classes",
)
HEAD_1452 = (1452, 174, 6396, 506144, 4669, 370058)
HEAD_1453 = (1453, 174, 6395, 506068, 4668, 369982)
EXPECTED_7677 = [
    "00000000040000003800080008080000",
    "00000000040000003802080008000000",
    "00000000040000809002002000004000",
    "00000000040000a09002000000004000",
]


def git_blob_sha(data):
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def read_pinned(path, expected):
    data = path.read_bytes()
    got = git_blob_sha(data)
    assert got == expected, f"{path.name}: blob {got} != {expected}"
    return json.loads(data.decode("utf-8"))


def head_tuple(head):
    return tuple(head[k] for k in HEAD_KEYS)


def run_projection(roots):
    """Run the already-published projection tool and read its root-count output."""
    path = OUT / (
        f"class2-lane-fold-projection-basis1450-{len(roots)}roots-20261116.json"
    )
    existed = path.exists()
    subprocess.run(
        [sys.executable, str(TOOL), *roots],
        cwd=HERE.parents[1],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    result = json.loads(path.read_text(encoding="utf-8"))
    if not existed:
        path.unlink()
    return result


def load_manifest():
    manifest = set()
    parts = sorted(MS5.glob("ms5_s6_manifest_part*.csv"))
    assert len(parts) == 6, len(parts)
    for path in parts:
        with path.open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                manifest.add(int(row["hex"], 16))
    assert len(manifest) == 7867, len(manifest)
    return manifest


def main():
    # Re-check the published projection implementation and its imported basis script.
    assert git_blob_sha(TOOL.read_bytes()) == BLOBS["tool"]
    assert git_blob_sha(C66C_SCRIPT.read_bytes()) == BLOBS["cost66c_script"]
    tool = runpy.run_path(str(TOOL))
    canon = tool["canon"]
    covers = tool["covers"]

    baseline = read_pinned(BASELINE_JSON, BLOBS["baseline_1452_projection"])
    fold7677 = read_pinned(FOLD7677_JSON, BLOBS["cost76d77e_fold"])
    claim_input = read_pinned(CLAIM_INPUT_JSON, BLOBS["cost76c_claim_input"])
    raw_audit = read_pinned(RAW_AUDIT_JSON, BLOBS["cost76c_raw_audit"])
    read_pinned(PRESWEEP_JSON, BLOBS["head1452_presweep"])

    assert claim_input["s6_child"] == raw_audit["target"]["s6_child"]
    child_hex = claim_input["s6_child"]
    child = int(child_hex, 16)
    assert claim_input["s5"] == raw_audit["target"]["s5"]
    assert raw_audit["result"]["win7_d10_bits"] == [61, 99, 113]

    roots7677 = [r["root_hex"] for r in fold7677["receipts"]]
    assert roots7677 == EXPECTED_7677
    assert [r["root_hex"] for r in baseline["receipts"]] == roots7677
    assert head_tuple(baseline["projected_head"]) == HEAD_1452

    candidates = []
    for rec in raw_audit["result"]["winner_roots"]:
        bit = rec["bit"]
        root = child | (1 << bit)
        root_hex = f"{root:032x}"
        root_canon = f"{canon(root):032x}"
        assert root_canon == rec["root_canon"], (bit, root_canon, rec["root_canon"])
        candidates.append({
            "bit": bit,
            "root_hex": root_hex,
            "root_canon": root_canon,
            "nodes": rec["nodes"],
        })
    candidates.sort(key=lambda r: r["bit"])
    assert [r["bit"] for r in candidates] == [61, 99, 113]
    assert len({r["root_canon"] for r in candidates}) == 3

    manifest = load_manifest()
    cover_sets = {
        r["bit"]: covers(int(r["root_hex"], 16))
        for r in candidates
    }
    cover_union = set().union(*cover_sets.values())
    manifest_union = cover_union & manifest
    assert len(cover_union) == 19, len(cover_union)
    assert len(manifest_union) == 7, len(manifest_union)

    # The published four-root projection is the exact head-1452 baseline.
    # Test each candidate alone against it, then all three in ascending bit order.
    singles = []
    for candidate in candidates:
        projection = run_projection(roots7677 + [candidate["root_hex"]])
        receipt = projection["receipts"][-1]
        assert receipt["root_hex"] == candidate["root_hex"]
        assert receipt["covers"] == 7
        assert receipt["marginal"] == 5
        assert receipt["marginal_in_manifest"] == 1
        assert receipt["marginal_manifest_hexes"] == [child_hex]
        assert head_tuple(projection["projected_head"]) == HEAD_1453
        singles.append({
            **candidate,
            "covers_d4_s6_orbits": receipt["covers"],
            "marginal_d4_s6_orbits": receipt["marginal"],
            "marginal_manifest_rows": receipt["marginal_in_manifest"],
            "marginal_hexes": receipt["marginal_hexes"],
            "marginal_manifest_hexes": receipt["marginal_manifest_hexes"],
            "projected_head": projection["projected_head"],
        })

    combined = run_projection(
        roots7677 + [r["root_hex"] for r in candidates]
    )
    combined_receipts = combined["receipts"][-3:]
    assert [(r["marginal"], r["marginal_in_manifest"])
            for r in combined_receipts] == [(5, 1), (4, 0), (4, 0)]
    assert combined_receipts[0]["marginal_manifest_hexes"] == [child_hex]
    assert combined_receipts[1]["marginal_manifest_hexes"] == []
    assert combined_receipts[2]["marginal_manifest_hexes"] == []
    assert head_tuple(combined["projected_head"]) == HEAD_1453

    current_open_manifest = set()
    for r in singles:
        current_open_manifest.update(r["marginal_manifest_hexes"])
    assert current_open_manifest == {child_hex}
    already_covered_manifest = manifest_union - {
        int(x, 16) for x in current_open_manifest
    }
    assert len(already_covered_manifest) == 6
    assert len(cover_union - manifest) == 12

    new_cover_union = set()
    for r in combined_receipts:
        new_cover_union.update(int(x, 16) for x in r["marginal_hexes"])
    assert len(new_cover_union) == 13
    assert len(new_cover_union & manifest) == 1
    assert len(new_cover_union - manifest) == 12

    bit61_projection = run_projection(roots7677 + [candidates[0]["root_hex"]])
    affected = bit61_projection["affected_parents"]
    parent_incidences = sum(len(p["lost_rows_hexes"]) for p in affected.values())
    edge_cost_delta = sum(p["lost_edge_cost"] for p in affected.values())
    assert len(affected) == 4
    assert parent_incidences == 6
    assert edge_cost_delta == 458

    min_nodes = min(r["nodes"] for r in candidates)
    for r in singles:
        r["nodes_relative_to_bit61"] = round(r["nodes"] / min_nodes, 6)
        r["new_non_manifest_marginal"] = (
            r["marginal_d4_s6_orbits"] - r["marginal_manifest_rows"]
        )

    result = {
        "schema": "n11-class2-lane-cost76c-candidate-manifest-marginals-20261117-v1",
        "date": "2026-11-17",
        "status": "projection-audited; certificate-extraction-pending; no-fold",
        "basis": {
            "head_before_cost76d77e": list(baseline["basis_head_numbers"]),
            "head_after_cost76d77e": list(HEAD_1452),
            "head_after_any_one_cost76c_candidate": list(HEAD_1453),
            "head_after_all_three_cost76c_candidates": list(HEAD_1453),
            "manifest_rows": len(manifest),
            "basis_receipt_roots": baseline["basis_roots"],
            "basis_distinct_d4_canons": baseline["basis_distinct_d4_canons"],
        },
        "source_blob_pins": {
            "fold_projection_head1450_tool": BLOBS["tool"],
            "cost66c_recompute_script": BLOBS["cost66c_script"],
            "cost66c_fold_json": BLOBS["cost66c_fold"],
            "head1452_four_root_projection": BLOBS["baseline_1452_projection"],
            "cost76d77e_fold_json": BLOBS["cost76d77e_fold"],
            "cost76c_claim_input_snapshot": BLOBS["cost76c_claim_input"],
            "cost76c_raw_audit": BLOBS["cost76c_raw_audit"],
            "head1452_presweep": BLOBS["head1452_presweep"],
        },
        "candidate_cover_union": {
            "candidate_count": 3,
            "distinct_d4_s6_orbits": len(cover_union),
            "manifest_intersection": len(manifest_union),
            "already_covered_manifest_orbits_at_head1452": len(already_covered_manifest),
            "currently_open_manifest_orbits": len(current_open_manifest),
            "currently_open_manifest_hexes": sorted(current_open_manifest),
            "outside_manifest_orbits": len(cover_union - manifest),
            "new_orbits_if_all_three_are_folded": len(new_cover_union),
            "new_manifest_orbits_if_all_three_are_folded": len(new_cover_union & manifest),
            "new_non_manifest_orbits_if_all_three_are_folded": len(new_cover_union - manifest),
        },
        "single_candidate_projections": singles,
        "combined_projection": {
            "fold_order_bits": [61, 99, 113],
            "per_candidate_marginal": [
                {
                    "bit": c["bit"],
                    "marginal_d4_s6_orbits": r["marginal"],
                    "marginal_manifest_rows": r["marginal_in_manifest"],
                    "marginal_manifest_hexes": r["marginal_manifest_hexes"],
                }
                for c, r in zip(candidates, combined_receipts)
            ],
            "projected_head": combined["projected_head"],
            "affected_parents_after_bit61": affected,
            "parent_row_incidences_lost": parent_incidences,
            "parent_edge_cost_lost": edge_cost_delta,
        },
        "recommendation": {
            "first_certificate_extraction_bit": 61,
            "fallback_bits_if_extraction_fails": [99, 113],
            "reason": (
                "Each candidate alone adds exactly the same one currently-open "
                "manifest row and projects the same head 1453. Folding all "
                "three adds no further manifest row: after bit 61, bits 99 "
                "and 113 each have zero manifest marginal. Bit 61 has the "
                "fewest raw search nodes (752696 vs 4168961 and 8174662)."
            ),
            "node_ratios_vs_bit61": {
                str(r["bit"]): r["nodes_relative_to_bit61"] for r in singles
            },
            "caveat": (
                "Raw search-node count is not certificate-extraction cost; "
                "the extraction run must measure its own cost. Bits 99 and "
                "113 remain backup WIN7-D10 search candidates, not LOSS proofs."
            ),
        },
        "interpretation_guard": (
            "This is a manifest-coverage projection over published receipt "
            "roots and raw WIN7-D10 candidates only. No certificate was "
            "extracted or independently verified, no new verdict was created, "
            "and no receipt fold was applied. REFUTED-D10 is not a LOSS proof. "
            "The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, "
            "S2 {59,60}, and classes 1/2/4 remain UNKNOWN."
        ),
    }
    OUTPUT_JSON.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print("output:", OUTPUT_JSON.name)
    print("candidate union:", result["candidate_cover_union"])
    print("single marginals:", [
        (r["bit"], r["nodes"], r["marginal_manifest_rows"],
         r["marginal_manifest_hexes"]) for r in singles
    ])
    print("combined marginals:", result["combined_projection"]["per_candidate_marginal"])
    print("projected head:", result["combined_projection"]["projected_head"])
    print("affected parents:", len(affected), "incidences:", parent_incidences,
          "edge cost:", edge_cost_delta)


if __name__ == "__main__":
    main()
