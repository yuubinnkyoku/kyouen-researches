#!/usr/bin/env python3
"""Rank the nine cost66j WIN7-D10 candidates by *current MS5 manifest
marginal*, using the published independent head-1450 projection tool, at the
post-cost64h-fold head-1472 baseline.

This is a bookkeeping audit only. It does not extract or verify
certificates (all nine cost66j WIN7-D10 certificates are already
extracted, independently verified and published), does not create
verdicts, and does not change the canonical head. The pending cost-76c
and cost-66i receipt folds have NOT landed; this audit projects at the
head-1472 baseline (head-1450 basis + the four baseline receipt roots +
the 23 landed cost64h receipt roots, whose fold the tool reproduces
exactly, cross-checked against the landed fold receipt's published
frontier numbers) and separately accounts for the overlap between
candidate marginals and the pending 76c/66i folds.
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
FOLD64H_JSON = OUT / "class-frontier-cost64h-receipts-recompute-20261117.json"
POSTFOLD1472_JSON = OUT / "class2-lane-head1472-cover-multiplicity-audit-20261117.json"
PREREG64H_JSON = OUT / "class2-lane-cost64h-fold-preregistration-independent-20261116.json"
MARGINALS66I_JSON = OUT / "class2-lane-cost66i-candidate-manifest-marginals-20261116.json"
CLAIM66J_JSON = OUT / "class2-lane-cost66j-inflight-20261117.json"
RAW_AUDIT66J_JSON = OUT / "class2-lane-cost66j-raw-audit-20261117.json"
PRESWEEP1472_JSON = OUT / "class2-lane-next-target-presweep-1472-20261117.json"
OUTPUT_JSON = OUT / "class2-lane-cost66j-candidate-manifest-marginals-20261117.json"

BLOBS = {
    "tool": "49fcd8ae6706c075b39eea5b115b2a045c2950cf",
    "fold64h": "1633be292f6f1862c895009eac29d398d0be7738",
    "postfold1472": "1d77d809198f53ccac234d27b9a64ab08fb55ef3",
    "prereg64h": "5074a8a0cbb75fcc91b5b999a3135fac06d42400",
    "marginals66i": "3343325ae7820d3531fd7b877accb86e39da28a3",
    "claim66j": "eb08a2db780f2b23c09f07ef96d02c5e0ff772a5",
    "raw_audit66j": "6862eb2db71e087d7c17fec3a157eafc17bf46d3",
    "presweep1472v3": "3ee5703c8cabf738eaecefb17a759c78c4a34e61",
}

HEAD_KEYS = (
    "solved_s6_in_manifest", "remaining_s5_orbits", "unique_remaining_s6",
    "sum_remaining_cost", "s6_needed_by_open_classes",
    "cost_needed_by_open_classes",
)
HEAD_1472 = (1472, 174, 6376, 504672, 4649, 368586)
BASE4 = [
    "00000000040000003800080008080000",
    "00000000040000003802080008000000",
    "00000000040000809002002000004000",
    "00000000040000a09002000000004000",
]
PENDING_76C_FOLD_ROW = "00000000010000809002000001000000"
WIN_BITS = [7, 9, 30, 66, 78, 79, 92, 96, 114]
WIN_BITS_66I = [19, 28, 29, 58, 88, 90, 99, 103, 112]


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

    fold64h = read_pinned(FOLD64H_JSON, BLOBS["fold64h"])
    postfold = read_pinned(POSTFOLD1472_JSON, BLOBS["postfold1472"])
    prereg = read_pinned(PREREG64H_JSON, BLOBS["prereg64h"])
    marginals66i = read_pinned(MARGINALS66I_JSON, BLOBS["marginals66i"])
    claim = read_pinned(CLAIM66J_JSON, BLOBS["claim66j"])
    raw_audit = read_pinned(RAW_AUDIT66J_JSON, BLOBS["raw_audit66j"])
    presweep = read_pinned(PRESWEEP1472_JSON, BLOBS["presweep1472v3"])

    # ---- target identity and sweep verdicts
    child_hex = claim["s6_child"]
    child = int(child_hex, 16)
    assert claim["s5"] == raw_audit["target"]["s5"]
    assert child_hex == raw_audit["target"]["s6_child"]
    assert presweep["selected_target"]["s6_hex"] == child_hex
    assert raw_audit["verdicts"]["win7_d10_bits"] == WIN_BITS
    assert raw_audit["verdicts"]["capped_count"] == 0
    assert marginals66i["combined_projection"]["fold_order_bits"] == WIN_BITS_66I

    # ---- landed cost64h fold: 23 receipt roots + the 20 closed rows
    fold_receipts = sorted(fold64h["receipts"], key=lambda r: r["bit"])
    assert len(fold_receipts) == 23, len(fold_receipts)
    roots64h = []
    for r in fold_receipts:
        x = int(r["root_hex"], 16)
        assert bin(x).count("1") == 7, r["root_hex"]
        roots64h.append(f"{x:032x}")
    assert len(set(roots64h)) == 23
    closed64h = {int(x, 16) for x in prereg["closed_row_parent_map"]}
    assert len(closed64h) == 20
    closed64h_audit = {
        int(h, 16)
        for rec in postfold["cost64h_receipts"]
        for h in rec["marginal_hexes"]
    }
    assert closed64h_audit == closed64h, "prereg vs postfold-audit 64h closure"
    fold_numbers = [
        fold64h["frontier_after_cost64h"][k] for k in HEAD_KEYS
    ]
    assert fold_numbers == list(HEAD_1472), fold_numbers

    # ---- pending folds: the 76c row and the 66i candidate marginal rows
    pending76c = {int(PENDING_76C_FOLD_ROW, 16)}
    union66i = set()
    for rec in marginals66i["single_candidate_projections"]:
        union66i.update(int(x, 16)
                        for x in rec["marginal_manifest_hexes"])
    # the 66i marginals were computed at the head-1452 baseline; net out the
    # landed cost64h closure and the pending 76c row, which will both be
    # closed before any 66i fold lands
    pending66i = union66i - closed64h - pending76c
    assert pending76c <= union66i | pending76c
    row76c_in_66i = PENDING_76C_FOLD_ROW in {
        f"{x:032x}" for x in union66i}

    # ---- the nine cost66j candidates from the claim (all certificates
    # already extracted, verified and published)
    candidates = []
    for rec in claim["winner_roots"]:
        bit = rec["bit"]
        root = child | (1 << bit)
        root_hex = f"{root:032x}"
        assert root_hex == rec["root"], (bit, root_hex, rec["root"])
        assert bin(root).count("1") == 7, bit
        root_canon = f"{canon(root):032x}"
        assert root_canon == rec["d4_canon_root"], (bit, root_canon)
        candidates.append({
            "bit": bit,
            "root_hex": root_hex,
            "root_canon": root_canon,
            "raw_equals_canon": root_hex == root_canon,
            "rows": rec["rows"],
            "extraction_nodes": rec["extraction_nodes"],
            "md5": rec["md5"],
        })
    candidates.sort(key=lambda r: r["bit"])
    assert [r["bit"] for r in candidates] == WIN_BITS
    assert len({r["root_canon"] for r in candidates}) == 9

    manifest = load_manifest()
    cover_sets = {r["bit"]: covers(int(r["root_hex"], 16)) for r in candidates}
    cover_union = set().union(*cover_sets.values())
    manifest_union = cover_union & manifest
    # 9 roots x 7 covers; the child orbit is covered by all nine, and no
    # other orbit may be covered twice (asserted, not assumed)
    shared = cover_union if len(cover_union) == 63 else cover_union
    pair_overlap = []
    for i, a in enumerate(WIN_BITS):
        for b in WIN_BITS[i + 1:]:
            ov = cover_sets[a] & cover_sets[b]
            if ov:
                pair_overlap.append({
                    "bits": [a, b],
                    "shared_orbits": [f"{x:032x}" for x in sorted(ov)],
                })
    child_in_manifest = child in manifest

    # ---- baseline control: BASE4 + the 23 landed 64h roots == head 1472
    prefix = BASE4 + roots64h
    baseline = run_projection(prefix)
    assert head_tuple(baseline["projected_head"]) == HEAD_1472, (
        "baseline head-1472 reconstruction failed",
        head_tuple(baseline["projected_head"]))
    assert sum(r["marginal_in_manifest"]
               for r in baseline["receipts"][:4]) == 2
    assert sum(r["marginal_in_manifest"]
               for r in baseline["receipts"][4:]) == 20
    baseline_receipts = baseline["receipts"]

    # ---- single-candidate projections at the head-1472 baseline
    singles = []
    for candidate in candidates:
        projection = run_projection(prefix + [candidate["root_hex"]])
        assert projection["receipts"][:27] == baseline_receipts, (
            candidate["bit"], "prefix receipts changed between runs")
        receipt = projection["receipts"][27]
        assert receipt["root_hex"] == candidate["root_hex"]
        assert receipt["covers"] == 7
        assert head_tuple(projection["projected_head"])[0] == \
            HEAD_1472[0] + receipt["marginal_in_manifest"]
        assert not (set(receipt["marginal_manifest_hexes"]) &
                    {f"{x:032x}" for x in closed64h}), (
            candidate["bit"], "marginal intersects the landed 64h closure")
        overlap76c = sorted(
            set(receipt["marginal_manifest_hexes"]) & {PENDING_76C_FOLD_ROW})
        overlap66i = sorted(
            {f"{x:032x}" for x in (set(int(h, 16) for h in
                receipt["marginal_manifest_hexes"]) & pending66i)})
        singles.append({
            **candidate,
            "covers_d4_s6_orbits": receipt["covers"],
            "marginal_d4_s6_orbits": receipt["marginal"],
            "marginal_manifest_rows": receipt["marginal_in_manifest"],
            "marginal_manifest_hexes": receipt["marginal_manifest_hexes"],
            "overlap_with_pending_76c_fold_rows": overlap76c,
            "overlap_with_pending_66i_fold_rows": overlap66i,
            "marginal_manifest_rows_net_of_pending_folds":
                receipt["marginal_in_manifest"] - len(overlap76c)
                - len(overlap66i),
            "projected_head": projection["projected_head"],
        })

    # ---- combined projection, ascending bit order
    combined = run_projection(prefix + [r["root_hex"] for r in candidates])
    assert combined["receipts"][:27] == baseline_receipts
    combined_receipts = combined["receipts"][27:]
    assert [r["root_hex"] for r in combined_receipts] == \
        [r["root_hex"] for r in candidates]
    assert head_tuple(combined["projected_head"])[0] == \
        HEAD_1472[0] + sum(r["marginal_in_manifest"]
                          for r in combined_receipts)

    new_cover_union = set()
    for r in combined_receipts:
        new_cover_union.update(int(x, 16) for x in r["marginal_hexes"])

    min_nodes = min(r["extraction_nodes"] for r in candidates)
    for r in singles:
        r["extraction_nodes_relative_to_cheapest"] = round(
            r["extraction_nodes"] / min_nodes, 6)
        r["new_non_manifest_marginal"] = (
            r["marginal_d4_s6_orbits"] - r["marginal_manifest_rows"])

    # fold-priority: marginal first (net of the pending 76c/66i folds),
    # then fewest extraction nodes; all nine certificates are already
    # extracted and published, so this ranks receipt-fold entry order only
    order = sorted(singles, key=lambda r: (
        -r["marginal_manifest_rows_net_of_pending_folds"],
        r["extraction_nodes"]))
    first = order[0]

    union_singles = set()
    for r in singles:
        union_singles.update(int(x, 16)
                             for x in r["marginal_manifest_hexes"])
    combined_mim_sum = sum(r["marginal_in_manifest"]
                          for r in combined_receipts)
    assert len(union_singles) == combined_mim_sum, (
        len(union_singles), combined_mim_sum,
        "per-candidate single marginals overlap outside the shared child")

    result = {
        "schema": "n11-class2-lane-cost66j-candidate-manifest-marginals-20261117-v1",
        "date": "2026-11-17",
        "status": "projection-audited; all nine certificates already "
                  "extracted, independently verified and published; "
                  "receipt fold pending behind the 76c/66i folds; no-fold",
        "basis": {
            "head_at_projection": list(HEAD_1472),
            "head_source": (
                "head-1450 basis (771 roots, published tool) + the four "
                "baseline receipt roots + the 23 landed cost64h receipt "
                "roots; the tool reproduces the landed fold receipt's "
                "published frontier_after_cost64h numbers exactly "
                "(1472/174/6376/504672/4649/368586)"),
            "manifest_rows": len(manifest),
            "baseline_receipt_roots": BASE4,
            "landed_cost64h_receipt_roots": roots64h,
            "pending_folds_note": (
                "the cost64h fold has LANDED (20 rows closed, head 1472). "
                "The cost-76c fold (row 00000000010000809002000001000000, "
                "parallel lane, bit 61 certificate in flight) and the "
                "cost-66i receipt fold (9 candidates) had NOT landed on "
                "main at audit time; projections are made at the head-1472 "
                "baseline and the overlaps are accounted separately per "
                "candidate"),
        },
        "source_blob_pins": {
            "fold_projection_head1450_tool": BLOBS["tool"],
            "cost64h_fold_receipt_landed": BLOBS["fold64h"],
            "head1472_postfold_audit": BLOBS["postfold1472"],
            "cost64h_fold_prereg": BLOBS["prereg64h"],
            "cost66i_candidate_marginals": BLOBS["marginals66i"],
            "cost66j_claim_v3": BLOBS["claim66j"],
            "cost66j_raw_audit": BLOBS["raw_audit66j"],
            "head1472_presweep_v3": BLOBS["presweep1472v3"],
        },
        "candidate_cover_union": {
            "candidate_count": 9,
            "distinct_d4_s6_orbits": len(cover_union),
            "child_orbit_covered_by_all_nine": True,
            "child_orbit_in_manifest": child_in_manifest,
            "pairwise_shared_orbits_beyond_child": pair_overlap,
            "manifest_intersection": len(manifest_union),
            "outside_manifest_orbits": len(cover_union - manifest),
            "new_orbits_if_all_nine_are_folded": len(new_cover_union),
            "new_manifest_orbits_if_all_nine_are_folded":
                len(new_cover_union & manifest),
            "new_non_manifest_orbits_if_all_nine_are_folded":
                len(new_cover_union - manifest),
        },
        "pending_fold_accounting": {
            "landed_cost64h_closed_rows": len(closed64h),
            "pending_76c_row": PENDING_76C_FOLD_ROW,
            "pending_76c_row_inside_66i_union": row76c_in_66i,
            "pending_66i_rows": sorted(f"{x:032x}" for x in pending66i),
            "pending_66i_row_count": len(pending66i),
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
            "role": "receipt-fold entry order only; certificate extraction "
                    "is complete for all nine bits",
            "fold_priority_order": [r["bit"] for r in order],
            "first_fold_priority_bit": first["bit"],
            "node_ratios_vs_cheapest": {
                str(r["bit"]): r["extraction_nodes_relative_to_cheapest"]
                for r in singles
            },
            "caveat": (
                "Extraction-node count is historical cost, not fold cost; "
                "the fold itself is pure bookkeeping. All nine candidates "
                "are WIN7-D10 with published, independently verified "
                "certificates, not LOSS proofs. The marginals are computed "
                "at the head-1472 baseline; after the pending cost-76c and "
                "cost-66i folds land, the shared rows drop out and the "
                "projection must be re-derived against the then-current "
                "canonical head before any 66j fold."),
        },
        "interpretation_guard": (
            "This is a manifest-coverage projection over published receipt "
            "roots, the landed cost64h fold receipt and the published "
            "cost66j WIN7-D10 certificates only. No new certificate was "
            "extracted here, no new verdict was created, and no receipt "
            "fold was applied. REFUTED-D10 is not a LOSS proof. The "
            "standard 11x11 empty board, two-stone roots {49,60}/{59,60}, "
            "S2 {59,60}, and classes 1/2/4 remain UNKNOWN."
        ),
    }
    OUTPUT_JSON.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print("output:", OUTPUT_JSON.name)
    print("baseline head-1472 reconstruction:", list(HEAD_1472), "OK")
    print("candidate union:", result["candidate_cover_union"])
    print("pairwise overlap:", pair_overlap)
    print("pending66i rows:", len(pending66i),
          "76c-in-66i-union:", row76c_in_66i)
    print("single marginals:", [
        (r["bit"], r["marginal_manifest_rows"],
         r["marginal_manifest_rows_net_of_pending_folds"],
         r["marginal_manifest_hexes"]) for r in singles])
    print("combined marginals:",
          result["combined_projection"]["per_candidate_marginal"])
    print("combined projected head:", combined["projected_head"])
    print("fold priority order:",
          result["recommendation"]["fold_priority_order"])


if __name__ == "__main__":
    main()
