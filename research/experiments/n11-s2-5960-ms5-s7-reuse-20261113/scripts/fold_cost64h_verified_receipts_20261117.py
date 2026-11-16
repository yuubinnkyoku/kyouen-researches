#!/usr/bin/env python3
"""Promote the independently verified cost-64h WIN7 receipts into a fold record.

This is bookkeeping only: no engine search and no new verdicts are produced.
The pre-registration independently reconstructs head 1452 and the 23 receipt
marginals; its independent-agreement record cross-checks that projection.
This script adds byte-level certificate-file pins, the full-row v17 recheck,
and cross-lane conflict checks before writing the fold and audit JSONs.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
CERT_DIR = OUT / "class2-lane-cost64h-certificates"

FILES = {
    "prereg": ("class2-lane-cost64h-fold-preregistration-independent-20261116.json",
               "5074a8a0cbb75fcc91b5b999a3135fac06d42400"),
    "verifier": ("class2-lane-cost64h-certificate-python4-fourth-verification-20261116.json",
                 "276e70e3dc930ffa17a02fe2280dff52b72b724c"),
    "v17": ("class2-lane-cost64h-v17-full-row-recheck-20261117.json",
            "b1a6c23b2ad0504252ab6bda3a09c23161f98107"),
    "agreement": ("class2-lane-cost64h-prereg-independent-agreement-20261116.json",
                  "9ab473ac0163755ddf541d8a9a5e44da304f8095"),
    "audit66i": ("class2-lane-cost66i-raw-audit-20261116.json",
                 "f7d8bad610fe07fee6b365e711838600722737e2"),
    "audit76c": ("class2-lane-cost76c-v17-sweep-and-fbt-saturation-audit-20261117.json",
                 "235f964365a7ab33e33986c915fc7f6861e4d686"),
}

HEAD_KEYS = (
    "solved_s6_in_manifest", "remaining_s5_orbits", "unique_remaining_s6",
    "sum_remaining_cost", "s6_needed_by_open_classes",
    "cost_needed_by_open_classes",
)
HEAD_1452 = [1452, 174, 6396, 506144, 4669, 370058]
HEAD_1472 = [1472, 174, 6376, 504672, 4649, 368586]


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def read_pinned(key: str) -> tuple[dict, str]:
    name, expected = FILES[key]
    data = (OUT / name).read_bytes()
    actual = git_blob_sha(data)
    if actual != expected:
        raise AssertionError(f"{name}: blob {actual} != {expected}")
    return json.loads(data.decode("utf-8")), actual


def d4_image(mask: int, transform: int) -> int:
    out = 0
    for p in range(121):
        if not ((mask >> p) & 1):
            continue
        x, y = p % 11, p // 11
        if transform == 0:
            X, Y = x, y
        elif transform == 1:
            X, Y = y, 10 - x
        elif transform == 2:
            X, Y = 10 - x, 10 - y
        elif transform == 3:
            X, Y = 10 - y, x
        elif transform == 4:
            X, Y = 10 - x, y
        elif transform == 5:
            X, Y = x, 10 - y
        elif transform == 6:
            X, Y = y, x
        else:
            X, Y = 10 - y, 10 - x
        out |= 1 << (11 * Y + X)
    return out


def canon(mask: int) -> int:
    return min(d4_image(mask, t) for t in range(8))


def roots_for(child_hex: str, bits: list[int]) -> dict[int, int]:
    child = int(child_hex, 16)
    return {bit: child | (1 << bit) for bit in bits}


def main() -> None:
    src_pairs = {key: read_pinned(key) for key in FILES}
    src = {key: value[0] for key, value in src_pairs.items()}
    source_pins = {key: value[1] for key, value in src_pairs.items()}
    pre = src["prereg"]
    ver = src["verifier"]
    v17 = src["v17"]
    agreement = src["agreement"]
    audit66 = src["audit66i"]
    audit76 = src["audit76c"]

    checks: dict[str, bool] = {}
    def check(name: str, ok: bool) -> None:
        checks[name] = bool(ok)
        if not ok:
            raise AssertionError(name)

    check("basis_head_1452", pre["basis_head_numbers"] == HEAD_1452)
    check("projected_head_1472",
          [pre["projected_head"][k] for k in HEAD_KEYS] == HEAD_1472)
    check("independent_prereg_agreement",
          all(agreement["agreement"].values()))
    check("independent_sweep_23_41_0", (
        agreement["checks"]["C4_sweep_rederived"]["win"],
        agreement["checks"]["C4_sweep_rederived"]["refuted"],
        agreement["checks"]["C4_sweep_rederived"]["capped"],
    ) == (23, 41, 0))
    check("independent_certificate_verification_23",
          ver["summary"]["all_pass"] is True
          and ver["summary"]["independently_verified"] == 23
          and ver["summary"]["certificates_in_directory"] == 23
          and ver["summary"]["union_missing"] == 0
          and ver["summary"]["union_extra"] == 0)
    check("independent_agreement_certificate_bytes_23",
          agreement["checks"]["C6_cert_bytes_verified"] == 23)
    check("independent_conflict_census_zero",
          agreement["checks"]["C9_conflict_census"]["overlaps"] == 0)

    win_bits = pre["win_bits_in_fold_order"]
    certs = sorted(ver["certificates"], key=lambda x: x["bit"])
    receipts = sorted(pre["receipts"], key=lambda x: x["bit"])
    check("receipt_bits_match_prereg", [r["bit"] for r in receipts] == win_bits)
    check("certificate_bits_match_receipts",
          [c["bit"] for c in certs] == [r["bit"] for r in receipts])
    check("certificate_roots_match_receipts",
          all(c["root_hex"] == r["root_hex"] for c, r in zip(certs, receipts)))
    check("certificate_verifier_checks_all_true",
          all(all(c["checks"].values()) for c in certs))

    cert_rows = []
    for rec, cert in zip(receipts, certs):
        cert_path = OUT / cert["path"]
        data = cert_path.read_bytes()
        blob = git_blob_sha(data)
        check(f"cert_bit_{rec['bit']}_blob", blob == cert["blob_sha"])
        check(f"cert_bit_{rec['bit']}_bytes", len(data) == cert["bytes"])
        check(f"cert_bit_{rec['bit']}_root", cert["root_hex"] == rec["root_hex"])
        check(f"cert_bit_{rec['bit']}_terminal_range",
              cert["terminal_range"] == [13, 17])
        check(f"cert_bit_{rec['bit']}_union_exact",
              cert["union_missing"] == 0 and cert["union_extra"] == 0)
        cert_rows.append({
            **rec,
            "certificate": {
                "path": cert["path"],
                "git_blob_sha": cert["blob_sha"],
                "bytes": cert["bytes"],
                "strategy_rows": cert["strategy_rows"],
                "subroots_passed": cert["subroots_passed"],
                "root_mobility": cert["root_mobility"],
                "terminal_count": cert["terminal_count"],
                "terminal_range": cert["terminal_range"],
                "visited_states": cert["visited_states"],
                "loser_reply_edges": cert["loser_reply_edges"],
                "union_missing": cert["union_missing"],
                "union_extra": cert["union_extra"],
                "verifier_checks": cert["checks"],
            },
        })

    check("certificate_count_23", len(cert_rows) == 23)
    check("v17_all_64_identical", (
        v17["result"]["bits_checked"],
        v17["result"]["identical_bits"],
        v17["result"]["verdict_flips"],
        v17["result"]["node_count_changes"],
    ) == (64, 64, [], []))
    check("v17_verdict_totals_23_41", (
        len(v17["result"]["win_bits"]), v17["result"]["refuted_bits"]
    ) == (23, 41))
    check("v17_node_total_unchanged",
          v17["result"]["v17_total_nodes"] ==
          v17["result"]["v16_published_total_nodes"] == 47017565)
    check("v17_win_bits_match_prereg",
          v17["result"]["win_bits"] == win_bits)

    conflict = audit66["cross_source_conflict_scan"]
    check("cross_source_conflicts_zero", conflict["conflicts"] == 0)
    check("cross_source_includes_cost64h_and_cost76c",
          "cost64h raw batches 1-8" in conflict["sources"]
          and "cost76c v17 raw batches 1-10" in conflict["sources"])

    roots64 = roots_for(pre["child"]["s6_hex"], win_bits)
    roots66 = roots_for(audit66["target"]["s6_child"],
                        audit66["verdicts"]["win7_d10_bits"])
    roots76 = roots_for(audit76["target"]["s6_child"],
                        audit76["v17_full_resweep"]["win_bits_corrected"])
    canons64 = {bit: canon(root) for bit, root in roots64.items()}
    canons66 = {bit: canon(root) for bit, root in roots66.items()}
    canons76 = {bit: canon(root) for bit, root in roots76.items()}
    overlap66 = sorted(set(canons64.values()) & set(canons66.values()))
    overlap76 = sorted(set(canons64.values()) & set(canons76.values()))
    check("cost64h_d4_canons_pairwise_distinct",
          len(set(canons64.values())) == 23)
    check("no_d4_overlap_with_cost66i", not overlap66)
    check("no_d4_overlap_with_cost76c", not overlap76)
    check("cost66i_cross_source_audit_zero",
          conflict["conflicts"] == 0)
    check("cost76c_v17_wins_61_99",
          audit76["v17_full_resweep"]["win_bits_corrected"] == [61, 99])
    check("cost76c_bit113_refuted",
          audit76["v17_full_resweep"]["per_bit"]["113"]["v17_loss"] is False)

    projected = {k: pre["projected_head"][k] for k in HEAD_KEYS}
    after = dict(projected)
    after["demand_histogram_open_only"] = pre["projected_demand_histogram"]
    before = dict(zip(HEAD_KEYS, HEAD_1452))
    target_parent = pre["affected_parents"]["00000000000000403800000008000000"]
    check("twenty_manifest_rows_closed",
          len(pre["totals"]["closed_manifest_rows"]) == 20)
    check("seventeen_affected_parents",
          len(pre["affected_parents"]) == 17)
    check("forty_two_parent_row_incidences",
          pre["parent_row_incidences"] == 42)
    check("parent_edge_cost_delta_3090",
          pre["parent_edge_cost_delta"] == 3090)
    check("target_parent_18_to_12",
          (target_parent["rows_before"], target_parent["rows_after"]) == (18, 12))
    check("no_s5_parent_fully_closed",
          all(p["rows_after"] > 0 for p in pre["affected_parents"].values()))

    source_pins["cost64h_claim_v2_historical"] = pre["inputs_blob_pins"]["cost64h_claim_v2_json"]
    source_pins["generator_script"] = git_blob_sha(Path(__file__).read_bytes())
    cert_bytes = sum(c["bytes"] for c in certs)
    cert_rows_total = sum(c["strategy_rows"] for c in certs)
    fold = {
        "schema": "n11-class2-lane-cost64h-receipts-recompute-20261117-v1",
        "date": "2026-11-17",
        "status": "fold-complete",
        "basis_head": 1452,
        "baseline_record": {"frontier_before": before},
        "frontier_after_cost64h": after,
        "receipts": cert_rows,
        "totals": {
            **pre["totals"],
            "total_certificate_bytes": cert_bytes,
            "total_strategy_rows": cert_rows_total,
            "independently_verified_certificates": len(certs),
        },
        "parents_after": pre["affected_parents"],
        "parent_row_incidences": pre["parent_row_incidences"],
        "parent_edge_cost_delta": pre["parent_edge_cost_delta"],
        "conflict_census": {
            "overlaps": 0,
            "basis_receipt_roots": pre["basis_receipt_roots"],
            "basis_distinct_d4_canons": pre["basis_distinct_d4_canons"],
            "cost66i_win_root_overlaps": len(overlap66),
            "cost76c_win_root_overlaps": len(overlap76),
            "cost66i_cross_source_verdict_conflicts": conflict["conflicts"],
        },
        "source_blob_pins": source_pins,
        "certificate_verification": ver["summary"],
        "v17_full_row_recheck": v17["result"],
        "cross_lane": {
            "cost66i_win_bits": claim66["actual_execution"]["win7_d10_bits"],
            "cost66i_conflict_scan": conflict,
            "cost76c_win_bits": audit76["v17_full_resweep"]["win_bits_corrected"],
            "cost76c_bit113_refuted": True,
            "cost76c_v17_audit_blob": FILES["audit76c"][1],
            "d4_overlap_with_cost66i": overlap66,
            "d4_overlap_with_cost76c": overlap76,
        },
        "target_parent": target_parent,
        "parent_count_fully_closed": 0,
        "interpretation_guard": (
            "Bookkeeping fold over 23 independently verified WIN7-D10 receipts. "
            "No engine search or new verdict was created. The fold closes 20 "
            "manifest S6 rows and reduces open frontier demand only. It does "
            "not close any S5 parent and is not a LOSS proof for REFUTED-D10. "
            "The 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 "
            "{59,60}, and classes 1/2/4 remain UNKNOWN."
        ),
    }

    audit = {
        "schema": "n11-class2-lane-cost64h-fold-audit-20261117-v1",
        "date": "2026-11-17",
        "status": "PASS",
        "source_blob_pins": {k: v[1] for k, v in src.items()},
        "checks": checks,
        "certificate_count": len(certs),
        "certificate_bytes": cert_bytes,
        "strategy_rows": cert_rows_total,
        "visited_states": ver["summary"]["total_visited_states"],
        "loser_reply_edges": ver["summary"]["total_loser_reply_edges"],
        "terminal_count": ver["summary"]["total_terminals"],
        "terminal_range": ver["summary"]["terminal_range_union"],
        "fold": {
            "basis_head": HEAD_1452,
            "projected_head": [projected[k] for k in HEAD_KEYS],
            "receipts": len(receipts),
            "marginal": pre["totals"]["total_marginal"],
            "marginal_in_manifest": pre["totals"]["total_marginal_in_manifest"],
            "closed_manifest_rows": len(pre["totals"]["closed_manifest_rows"]),
            "affected_parents": len(pre["affected_parents"]),
            "parent_row_incidences": pre["parent_row_incidences"],
            "parent_edge_cost_delta": pre["parent_edge_cost_delta"],
            "target_parent_rows": [
                target_parent["rows_before"], target_parent["rows_after"]
            ],
            "target_parent_edge_cost": [
                target_parent["edge_cost_before"], target_parent["edge_cost_after"]
            ],
            "fully_closed_s5_parents": 0,
        },
        "cross_lane": fold["cross_lane"],
        "all_checks_pass": all(checks.values()),
        "interpretation_guard": fold["interpretation_guard"],
    }

    fold_path = OUT / "class-frontier-cost64h-receipts-recompute-20261117.json"
    audit_path = OUT / "class2-lane-cost64h-fold-audit-20261117.json"
    fold_path.write_text(json.dumps(fold, ensure_ascii=False, indent=1,
                                   sort_keys=True) + "\n", encoding="utf-8")
    audit_path.write_text(json.dumps(audit, ensure_ascii=False, indent=1,
                                    sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "fold": fold_path.name,
        "audit": audit_path.name,
        "all_checks_pass": audit["all_checks_pass"],
        "checks": len(checks),
        "head": [projected[k] for k in HEAD_KEYS],
        "closed_manifest_rows": len(pre["totals"]["closed_manifest_rows"]),
        "certificates": len(certs),
    }, indent=1, sort_keys=True))
    if not audit["all_checks_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
