#!/usr/bin/env python3
"""Independent agreement check: the landed cost-66c fold receipt vs the
pre-registration (2026-11-16).

The fold arm published the cost-66c fold receipt
(class-frontier-cost66c-receipts-recompute-20261116.json, commit 96e2dbac)
folding the 7 WIN7-D10 receipt roots (bits 73/75/79/87/96/97/112 of child
00000000000000003800000008002008) on the head-1444 basis, claiming the new
canonical head 1450/174/6398/506297/4671/370211.  The pre-registration
(class2-lane-cost66c-fold-preregistration-20261116.json, git blob
809ad05e1bc560b1086c3d30cc34ad78727e430a, commit aca9d762, published at
11:10:03Z, before the fold receipt landed at 11:19:20Z) contains the
independent fold projection with projected head
1450/174/6398/506297/4671/370211, total marginal 35, marginal-in-manifest 6.

This check is written from the pre-registration semantics only (it does not
reuse the fold arm's own check script) and compares every
machine-checkable field between the two published artifacts:

  C1  projected head 6-numbers == receipt frontier_after_cost66c
  C2  basis head numbers == receipt baseline head 1444, roots 764
  C3  demand histogram: receipt hist minus prereg basis hist == prereg deltas
  C4  per-receipt (publication order): bit, root_hex, d4_canonical_hex,
      covers, covers_hexes, marginal, marginal_hexes, marginal_in_manifest,
      marginal_manifest_hexes
  C5  totals: receipts 7, total marginal 35, marginal-in-manifest 6
  C6  rows closed == union of the prereg marginal_manifest_hexes (6)
  C7  affected parents: rows/edge_cost before/after and lost-row hexes
  C8  conflict census empty and all prereg D4 orbits distinct
  C9  parent edge-cost delta == sum of prereg lost_edge_cost
  C10 child closed exactly by bit 73
  C11 sweep nodes excluding pilots == 84180263
  C12 receipt_bits mapping (root hex -> bit) identical

Interpretation guard: bookkeeping agreement only; a fold changes manifest
coverage bookkeeping, not the game-theoretic value of any position; WIN7
certificates prove a first-player win within depth 10 from individual
7-stone roots only; REFUTED-D10 is not a LOSS proof; the 11x11 empty board,
the two-stone roots {49,60}/{59,60}, S2 {59,60} and classes 1/2/4 remain
UNKNOWN.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
PREREG = OUT / "class2-lane-cost66c-fold-preregistration-20261116.json"
RECEIPT = OUT / "class-frontier-cost66c-receipts-recompute-20261116.json"


def main():
    pre = json.loads(PREREG.read_text())
    rec = json.loads(RECEIPT.read_text())
    checks = {}

    # C1 projected head
    ph = pre["projected_head"]
    fa = rec["frontier_after_cost66c"]
    checks["C1_projected_head"] = {
        "prereg": ph,
        "receipt": {
            "solved_s6_in_manifest": fa["solved_s6_in_manifest"],
            "remaining_s5_orbits": fa["remaining_s5_orbits"],
            "unique_remaining_s6": fa["unique_remaining_s6"],
            "sum_remaining_cost": fa["sum_remaining_cost"],
            "s6_needed_by_open_classes": fa["s6_needed_by_open_classes"],
            "cost_needed_by_open_classes": fa["cost_needed_by_open_classes"],
        },
        "agree": (
            ph["solved_s6_in_manifest"] == fa["solved_s6_in_manifest"]
            and ph["remaining_s5_orbits"] == fa["remaining_s5_orbits"]
            and ph["unique_remaining_s6"] == fa["unique_remaining_s6"]
            and ph["sum_remaining_cost"] == fa["sum_remaining_cost"]
            and ph["s6_needed_by_open_classes"] == fa["s6_needed_by_open_classes"]
            and ph["cost_needed_by_open_classes"] == fa["cost_needed_by_open_classes"]
        ),
    }

    # C2 basis
    bl = rec["baseline_record"]
    checks["C2_basis"] = {
        "prereg_head_numbers": pre["basis_head_numbers"],
        "prereg_roots": pre["basis_roots"],
        "receipt_receipt_roots": bl["receipt_roots"]["count"],
        "receipt_distinct_d4_canons": bl["receipt_roots"]["distinct_d4_canons"],
        "agree": (
            pre["basis_head_numbers"] == [1444, 174, 6404, 506746, 4677, 370660]
            and pre["basis_roots"] == bl["receipt_roots"]["count"] == 764
        ),
    }

    # C3 demand histogram
    base_hist = pre["basis_summary"]["hist"]
    after_hist = fa["demand_histogram_open_only"]
    derived_deltas = {}
    all_keys = sorted(set(base_hist) | set(after_hist))
    for k in all_keys:
        derived_deltas[k] = after_hist.get(k, 0) - base_hist.get(k, 0)
    checks["C3_demand_histogram"] = {
        "prereg_deltas": pre["demand_histogram_deltas"],
        "derived_deltas": derived_deltas,
        "agree": derived_deltas == pre["demand_histogram_deltas"],
    }

    # C4 per-receipt fields in publication order
    per_receipt = []
    c4_ok = True
    for i, (pr, ra) in enumerate(zip(pre["receipts"], rec["cost66c_additions"])):
        fields = ["root_hex", "d4_canonical_hex", "covers", "covers_hexes",
                  "marginal", "marginal_hexes", "marginal_in_manifest",
                  "marginal_manifest_hexes"]
        agree = all(pr[f] == ra[f] for f in fields)
        agree = agree and pre["receipt_bits"][pr["root_hex"]] == ra["bit"]
        c4_ok = c4_ok and agree
        per_receipt.append({
            "order": i, "bit": ra["bit"], "root_hex": pr["root_hex"],
            "fields_agree": agree,
            "marginal": pr["marginal"],
            "marginal_in_manifest": pr["marginal_in_manifest"],
        })
    checks["C4_per_receipt"] = {
        "receipts": per_receipt,
        "agree": c4_ok and len(pre["receipts"]) == len(rec["cost66c_additions"]) == 7,
    }

    # C5 totals
    t = rec["totals"]
    checks["C5_totals"] = {
        "receipts": t["receipts"],
        "total_marginal": t["total_marginal"],
        "total_marginal_in_manifest": t["total_marginal_in_manifest"],
        "agree": t["receipts"] == 7 and t["total_marginal"] == 35
                 and t["total_marginal_in_manifest"] == 6
                 and sum(r["marginal"] for r in pre["receipts"]) == t["total_marginal"]
                 and sum(r["marginal_in_manifest"] for r in pre["receipts"])
                     == t["total_marginal_in_manifest"],
    }

    # C6 rows closed
    pre_rows = sorted({h for r in pre["receipts"]
                       for h in r["marginal_manifest_hexes"]})
    checks["C6_rows_closed"] = {
        "prereg_union_manifest_hexes": pre_rows,
        "receipt_rows_closed_hexes": sorted(t["rows_closed_hexes"]),
        "agree": pre_rows == sorted(t["rows_closed_hexes"]) and len(pre_rows) == 6,
    }

    # C7 affected parents
    parents_agree = True
    parent_detail = []
    for hex_, pa in rec["parents_after"].items():
        pp = pre["affected_parents"].get(hex_)
        ok = (pp is not None
              and pp["rows_before"] == pa["rows_before"]
              and pp["rows_after"] == pa["rows"]
              and pp["edge_cost_before"] == pa["edge_cost_before"]
              and pp["edge_cost_after"] == pa["edge_cost"]
              and sorted(pp["lost_rows_hexes"])
                  == sorted(rec["lost_rows_per_parent"][hex_].keys()))
        parents_agree = parents_agree and ok
        parent_detail.append({"s5_hex": hex_, "agree": ok})
    checks["C7_affected_parents"] = {
        "parents": parent_detail,
        "count": len(rec["parents_after"]),
        "agree": parents_agree and len(rec["parents_after"]) == 6
                 and sorted(pre["affected_parents"]) == sorted(rec["parents_after"]),
    }

    # C8 conflict census
    checks["C8_conflict_census"] = {
        "receipt_overlaps": t["conflict_census_overlaps"],
        "prereg_all_orbits_distinct": all(
            r["d4_orbit_distinct_from_all_folded_roots"] for r in pre["receipts"]),
        "agree": t["conflict_census_overlaps"] == [] and all(
            r["d4_orbit_distinct_from_all_folded_roots"] for r in pre["receipts"]),
    }

    # C9 parent edge-cost delta
    delta = sum(p["lost_edge_cost"] for p in pre["affected_parents"].values())
    checks["C9_parent_edge_cost_delta"] = {
        "prereg_sum_lost_edge_cost": delta,
        "receipt_parent_edge_cost_delta": t["parent_edge_cost_delta"],
        "agree": delta == t["parent_edge_cost_delta"],
    }

    # C10 child closed by bit 73
    child = pre["receipts"][0]["marginal_manifest_hexes"]
    checks["C10_child_closed"] = {
        "prereg_bit73_manifest_hexes": child,
        "receipt_child_closed_by_bit": t["child_closed_by_bit"],
        "agree": child == [rec["cost66c_additions"][0]["root_hex"]
                           .replace("000000000000020038", "000000000000000038")]
            and t["child_closed_by_bit"] == 73,
    }

    # C11 sweep nodes
    checks["C11_sweep_nodes"] = {
        "receipt_sweep_nodes_excluding_pilots": t["sweep_nodes_excluding_pilots"],
        "agree": t["sweep_nodes_excluding_pilots"] == 84180263,
    }

    # C12 receipt_bits mapping
    rb_rec = {a["root_hex"]: a["bit"] for a in rec["cost66c_additions"]}
    checks["C12_receipt_bits"] = {
        "agree": rb_rec == pre["receipt_bits"],
    }

    all_agree = all(c["agree"] for c in checks.values())
    result = {
        "schema": "n11-class2-lane-cost66c-fold-receipt-independent-agreement-20261116-v1",
        "date": "2026-11-16",
        "inputs": {
            "preregistration": "class2-lane-cost66c-fold-preregistration-20261116.json "
                "(git blob 809ad05e1bc560b1086c3d30cc34ad78727e430a, commit aca9d762, "
                "published 11:10:03Z, pinned locally by this lane before the fold landed)",
            "fold_receipt": "class-frontier-cost66c-receipts-recompute-20261116.json "
                "(commit 96e2dbac, landed 11:19:20Z)",
        },
        "method": ("independent field-by-field comparison written from the "
                   "pre-registration semantics only; does not reuse the fold "
                   "arm's own check script "
                   "(check_cost66c_fold_receipt_vs_preregistration_20261116.py)"),
        "checks": checks,
        "all_agree": all_agree,
        "interpretation_guard": ("bookkeeping agreement only; a fold changes "
            "manifest coverage bookkeeping, not the game-theoretic value of "
            "any position; WIN7 certificates prove a first-player win within "
            "depth 10 from individual 7-stone roots only; REFUTED-D10 is not "
            "a LOSS proof; the 11x11 empty board, the two-stone roots "
            "{49,60}/{59,60}, S2 {59,60} and classes 1/2/4 remain UNKNOWN"),
    }
    with open(OUT / "class2-lane-cost66c-fold-receipt-independent-agreement-20261116.json", "w") as f:
        json.dump(result, f, indent=1, sort_keys=True)
        f.write("\n")
    print("all_agree:", all_agree)
    for k, c in checks.items():
        print(" ", k, c["agree"])


if __name__ == "__main__":
    main()
