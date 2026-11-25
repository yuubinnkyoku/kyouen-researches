#!/usr/bin/env python3
"""Rank the nine cost66i WIN7-D10 candidates by *current MS5 manifest
marginal*, using the published independent head-1450 projection tool.

This is a bookkeeping audit only. It does not extract or verify
certificates, does not create verdicts, and does not change the canonical
head. The pending cost-64h and cost-76c receipt folds have NOT landed;
this audit projects at the head-1452 baseline (the same basis the
published cost76c marginals audit used) and separately accounts for the
overlap between candidate marginals and the pending folds.
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
PREREG64H_JSON = OUT / "class2-lane-cost64h-fold-preregistration-independent-20261116.json"
CLAIM66I_JSON = OUT / "class2-lane-cost66i-inflight-20261116.json"
RAW_AUDIT_JSON = OUT / "class2-lane-cost66i-raw-audit-20261116.json"
PRESWEEP_V2_JSON = OUT / "class2-lane-next-target-presweep-1452-v2-20261116.json"
OUTPUT_JSON = OUT / "class2-lane-cost66i-candidate-manifest-marginals-20261116.json"

BLOBS = {
    "tool": "49fcd8ae6706c075b39eea5b115b2a045c2950cf",
    "prereg64h": "5074a8a0cbb75fcc91b5b999a3135fac06d42400",
    "claim66i": "738443c0d1076115d723029edac2de3cb67c3e86",
    "raw_audit66i": "f7d8bad610fe07fee6b365e711838600722737e2",
    "presweep_v2": "67d6a5c192953b9bc95fd13b356e5aabeac2a12c",
}

HEAD_KEYS = (
    "solved_s6_in_manifest", "remaining_s5_orbits", "unique_remaining_s6",
    "sum_remaining_cost", "s6_needed_by_open_classes",
    "cost_needed_by_open_classes",
)
HEAD_1452 = (1452, 174, 6396, 506144, 4669, 370058)
BASE4 = [
    "00000000040000003800080008080000",
    "00000000040000003802080008000000",
    "00000000040000809002002000004000",
    "00000000040000a09002000000004000",
]
PENDING_76C_FOLD_ROW = "00000000010000809002000001000000"
WIN_BITS = [19, 28, 29, 58, 88, 90, 99, 103, 112]


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
    """Run the published projection tool and read its root-count output."""
    path = OUT / (
        f"class2-lane-fold-projection-basis1450-{len(roots)}roots-20261116.json"
    )
    subprocess.run(
        [sys.executable, str(TOOL), *roots],
        cwd=HERE.parents[1],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    result = json.loads(path.read_text(encoding="utf-8"))
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
    assert git_blob_sha(TOOL.read_bytes()) == BLOBS["tool"]
    tool = runpy.run_path(str(TOOL))
    canon = tool["canon"]
    covers = tool["covers"]

    prereg = read_pinned(PREREG64H_JSON, BLOBS["prereg64h"])
    claim = read_pinned(CLAIM66I_JSON, BLOBS["claim66i"])
    raw_audit = read_pinned(RAW_AUDIT_JSON, BLOBS["raw_audit66i"])
    read_pinned(PRESWEEP_V2_JSON, BLOBS["presweep_v2"])

    assert claim["s6_child"] == raw_audit["target"]["s6_child"]
    child_hex = claim["s6_child"]
    child = int(child_hex, 16)
    assert claim["s5"] == raw_audit["target"]["s5"]
    assert raw_audit["verdicts"]["win7_d10_bits"] == WIN_BITS
    assert raw_audit["verdicts"]["capped_count"] == 0

    closed64h = set(prereg["closed_row_parent_map"])
    assert len(closed64h) == 20

    candidates = []
    for rec in claim["actual_execution"]["winner_roots"]:
        bit = rec["bit"]
        root = child | (1 << bit)
        root_hex = f"{root:032x}"
        root_canon = f"{canon(root):032x}"
        assert root_canon == rec["root_canon"], (bit, root_canon)
        candidates.append({
            "bit": bit,
            "root_hex": root_hex,
            "root_canon": root_canon,
            "nodes": rec["nodes"],
        })
    candidates.sort(key=lambda r: r["bit"])
    assert [r["bit"] for r in candidates] == WIN_BITS
    assert len({r["root_canon"] for r in candidates}) == 9

    manifest = load_manifest()
    cover_sets = {r["bit"]: covers(int(r["root_hex"], 16)) for r in candidates}
    cover_union = set().union(*cover_sets.values())
    manifest_union = cover_union & manifest
    # 9 roots x 7 covers with the child row shared by all nine
    assert len(cover_union) == 55, len(cover_union)
    assert len(manifest_union) == 20, len(manifest_union)

    # --- single-candidate projections at the head-1452 baseline
    singles = []
    for candidate in candidates:
        projection = run_projection(BASE4 + [candidate["root_hex"]])
        assert head_tuple(projection["projected_head"])[0] == \
            HEAD_1452[0] + projection["receipts"][-1]["marginal_in_manifest"]
        receipt = projection["receipts"][-1]
        assert receipt["root_hex"] == candidate["root_hex"]
        assert receipt["covers"] == 7
        overlap64h = sorted(set(receipt["marginal_manifest_hexes"]) & closed64h)
        overlap76c = sorted(
            set(receipt["marginal_manifest_hexes"]) & {PENDING_76C_FOLD_ROW})
        singles.append({
            **candidate,
            "covers_d4_s6_orbits": receipt["covers"],
            "marginal_d4_s6_orbits": receipt["marginal"],
            "marginal_manifest_rows": receipt["marginal_in_manifest"],
            "marginal_manifest_hexes": receipt["marginal_manifest_hexes"],
            "overlap_with_pending_64h_fold_rows": overlap64h,
            "overlap_with_pending_76c_fold_rows": overlap76c,
            "marginal_manifest_rows_net_of_pending_64h_fold":
                receipt["marginal_in_manifest"] - len(overlap64h),
            "projected_head": projection["projected_head"],
        })

    # --- combined projection, ascending bit order
    combined = run_projection(BASE4 + [r["root_hex"] for r in candidates])
    combined_receipts = combined["receipts"][-9:]
    assert [r["root_hex"] for r in combined_receipts] == \
        [r["root_hex"] for r in candidates]
    assert head_tuple(combined["projected_head"])[0] == \
        HEAD_1452[0] + sum(r["marginal_in_manifest"] for r in combined_receipts)

    new_cover_union = set()
    for r in combined_receipts:
        new_cover_union.update(int(x, 16) for x in r["marginal_hexes"])

    min_nodes = min(r["nodes"] for r in candidates)
    for r in singles:
        r["nodes_relative_to_cheapest"] = round(r["nodes"] / min_nodes, 6)
        r["new_non_manifest_marginal"] = (
            r["marginal_d4_s6_orbits"] - r["marginal_manifest_rows"])

    # recommendation: marginal first (net of the pending 64h fold overlap),
    # then fewest raw search nodes
    order = sorted(singles, key=lambda r: (
        -r["marginal_manifest_rows_net_of_pending_64h_fold"], r["nodes"]))
    first = order[0]

    result = {
        "schema": "n11-class2-lane-cost66i-candidate-manifest-marginals-20261116-v1",
        "date": "2026-11-16",
        "status": "projection-audited; certificate-extraction-pending; no-fold",
        "basis": {
            "head_at_projection": list(HEAD_1452),
            "manifest_rows": len(manifest),
            "baseline_receipt_roots": BASE4,
            "pending_folds_note": (
                "the cost-64h fold (prereg blob 5074a8a0..., projected head "
                "1472, 20 closed rows) and the cost-76c fold (projected head "
                "1453, row 00000000010000809002000001000000) had NOT landed "
                "on main at audit time; projections are made at the "
                "head-1452 baseline and the overlaps are accounted "
                "separately per candidate"),
        },
        "source_blob_pins": {
            "fold_projection_head1450_tool": BLOBS["tool"],
            "cost64h_fold_prereg": BLOBS["prereg64h"],
            "cost66i_claim_v2": BLOBS["claim66i"],
            "cost66i_raw_audit": BLOBS["raw_audit66i"],
            "head1452_presweep_v2": BLOBS["presweep_v2"],
        },
        "candidate_cover_union": {
            "candidate_count": 9,
            "distinct_d4_s6_orbits": len(cover_union),
            "manifest_intersection": len(manifest_union),
            "outside_manifest_orbits": len(cover_union - manifest),
            "new_orbits_if_all_nine_are_folded": len(new_cover_union),
            "new_manifest_orbits_if_all_nine_are_folded":
                len(new_cover_union & manifest),
            "new_non_manifest_orbits_if_all_nine_are_folded":
                len(new_cover_union - manifest),
        },
        "single_candidate_projections": singles,
        "combined_projection": {
            "fold_order_bits": WIN_BITS,
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
        },
        "recommendation": {
            "first_certificate_extraction_bit": first["bit"],
            "extraction_order": [r["bit"] for r in order],
            "reason": (
                "Bit 19 alone closes 4 currently-open manifest rows "
                "(3 net of the one row it shares with the pending cost-64h "
                "fold), the largest marginal of the nine candidates; bit 28 "
                "is second (3 rows, 2 net); bits 88/99/103 each close the "
                "child row plus one row of the 000000000000008890020000... "
                "family; bits 29/58/90/112 close only the child row "
                "00000000000000801226000000000000, which any other candidate "
                "also closes, so they add nothing if another candidate is "
                "folded first."),
            "node_ratios_vs_cheapest": {
                str(r["bit"]): r["nodes_relative_to_cheapest"] for r in singles
            },
            "caveat": (
                "Raw search-node count is not certificate-extraction cost; "
                "the extraction run must measure its own cost. All nine "
                "remain WIN7-D10 search candidates, not LOSS proofs. The "
                "marginals are computed at the head-1452 baseline; after the "
                "pending cost-64h/cost-76c folds land, the shared rows "
                "drop out and the projection must be re-derived against "
                "the then-current canonical head before any 66i fold."),
        },
        "interpretation_guard": (
            "This is a manifest-coverage projection over published receipt "
            "roots and raw WIN7-D10 candidates only. No certificate was "
            "extracted or independently verified, no new verdict was "
            "created, and no receipt fold was applied. REFUTED-D10 is not a "
            "LOSS proof. The standard 11x11 empty board, two-stone roots "
            "{49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN."
        ),
    }
    OUTPUT_JSON.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print("output:", OUTPUT_JSON.name)
    print("candidate union:", result["candidate_cover_union"])
    print("single marginals:", [
        (r["bit"], r["marginal_manifest_rows"],
         r["marginal_manifest_rows_net_of_pending_64h_fold"],
         r["marginal_manifest_hexes"]) for r in singles])
    print("combined marginals:", result["combined_projection"]["per_candidate_marginal"])
    print("combined projected head:", combined["projected_head"])
    print("extraction order:", result["recommendation"]["extraction_order"])


if __name__ == "__main__":
    main()
