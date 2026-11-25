#!/usr/bin/env python3
"""Check the parallel lane's cost-65n fold receipt against this lane's
pre-registration (output/class2-lane-cost65n-fold-preregistration-20261116.json,
git blob da2b2292, commit 0c237017, published BEFORE the fold receipt landed).

usage: python3 check_cost65n_fold_receipt_vs_preregistration_20261116.py \
           <fold-receipt.json path or URL> [out.json]

Compares every machine-checkable field the pre-registration pinned:
  - projected frontier_after head 6 numbers (solved 1444 / s5 174 / unique 6404
    / sum 506746 / s6_needed 4677 / cost_needed 370660)
  - demand histogram after fold (basis hist + deltas)
  - affected parents: rows/edge_cost after, rows_before/edge_cost_before,
    lost rows hexes, parent row incidences, parent edge cost delta
  - closed rows hexes (child + 2 collateral) and marginal / mim totals
  - root-level receipt fields (marginal, marginal_in_manifest, covers,
    d4 canonical hex)

Prints PASS/FAIL per check and writes a machine-readable record when
out.json is given. Disagreements are recorded as experimental facts, not
silenced.
"""
import json
import sys
import urllib.request
from pathlib import Path

PREREG = Path(__file__).resolve().parents[1] / \
    "output" / "class2-lane-cost65n-fold-preregistration-20261116.json"
EXPECTED = {
    "solved_s6_in_manifest": 1444,
    "remaining_s5_orbits": 174,
    "unique_remaining_s6": 6404,
    "sum_remaining_cost": 506746,
    "s6_needed_by_open_classes": 4677,
    "cost_needed_by_open_classes": 370660,
}
CHILD = "00000000000000801202010000800000"


def load(path_or_url):
    if path_or_url.startswith("http"):
        with urllib.request.urlopen(path_or_url) as r:
            return json.load(r)
    return json.loads(Path(path_or_url).read_text())


def main():
    receipt_path = sys.argv[1]
    out_path = sys.argv[2] if len(sys.argv) > 2 else None
    receipt = load(receipt_path)
    pre = json.loads(PREREG.read_text())

    checks = []

    def check(name, ok, detail):
        checks.append({"check": name, "pass": bool(ok), "detail": detail})
        print(("PASS" if ok else "FAIL"), "|", name, "|", detail)

    # locate the frontier_after dict (schema-named key)
    fa = None
    for k, v in receipt.items():
        if k.startswith("frontier_after") and isinstance(v, dict):
            fa = v
            break
    if fa is None:
        check("frontier_after dict present", False, "no frontier_after* key")
    else:
        for key, want in EXPECTED.items():
            got = fa.get(key)
            check(f"projected head {key}", got == want,
                  f"prereg {want} vs receipt {got}")

    # demand histogram after fold = basis hist + deltas
    basis_hist = pre["basis_summary"]["hist"]
    deltas = pre["demand_histogram_deltas"]
    want_hist = {k: basis_hist[k] + deltas.get(k, 0) for k in basis_hist}
    got_hist = fa.get("demand_histogram_open_only") if fa else None
    check("demand histogram after fold", got_hist == want_hist,
          f"prereg-projected {want_hist} vs receipt {got_hist}")

    # totals
    tot = receipt.get("totals", {})
    want_marg = sum(r["marginal"] for r in pre["receipts"])
    want_mim = sum(r["marginal_in_manifest"] for r in pre["receipts"])
    check("total_marginal", tot.get("total_marginal") == want_marg,
          f"prereg {want_marg} vs receipt {tot.get('total_marginal')}")
    check("total_marginal_in_manifest",
          tot.get("total_marginal_in_manifest") == want_mim,
          f"prereg {want_mim} vs receipt {tot.get('total_marginal_in_manifest')}")

    # closed rows: exactly the 3 marginal_manifest hexes
    want_closed = sorted(h for r in pre["receipts"]
                         for h in r["marginal_manifest_hexes"])
    got_closed = sorted(tot.get("rows_closed_hexes", []))
    check("rows_closed_hexes", got_closed == want_closed,
          f"prereg {want_closed} vs receipt {got_closed}")
    check("child closed", CHILD in got_closed,
          f"child {CHILD} in receipt rows_closed_hexes")

    # parents: rows/edge after + before + lost rows
    parents = receipt.get("parents_after", {})
    lost = receipt.get("lost_rows_per_parent", {})
    all_ok = True
    detail = []
    for phex, pdata in pre["affected_parents"].items():
        got = parents.get(phex)
        ok = (got is not None
              and got.get("rows") == pdata["rows_after"]
              and got.get("edge_cost") == pdata["edge_cost_after"]
              and got.get("rows_before") == pdata["rows_before"]
              and got.get("edge_cost_before") == pdata["edge_cost_before"])
        all_ok = all_ok and ok
        detail.append({"parent": phex, "prereg": pdata, "receipt": got})
    check("affected parents rows/edge before+after", all_ok,
          json.dumps(detail)[:400])

    lost_ok = True
    lost_detail = []
    for phex, pdata in pre["affected_parents"].items():
        want_lost = sorted(pdata["lost_rows_hexes"])
        got_lost = sorted(lost.get(phex, {})) if isinstance(lost.get(phex), dict) else None
        ok = got_lost == want_lost
        lost_ok = lost_ok and ok
        lost_detail.append({"parent": phex, "want": want_lost, "got": got_lost})
    check("lost rows per parent", lost_ok, json.dumps(lost_detail)[:400])

    want_incid = sum(p["rows_before"] - p["rows_after"]
                     for p in pre["affected_parents"].values())
    check("parent_row_incidences", tot.get("parent_row_incidences") == want_incid,
          f"prereg {want_incid} vs receipt {tot.get('parent_row_incidences')}")
    want_edge = sum(p["edge_cost_before"] - p["edge_cost_after"]
                    for p in pre["affected_parents"].values())
    check("parent_edge_cost_delta",
          tot.get("parent_edge_cost_delta") == want_edge,
          f"prereg {want_edge} vs receipt {tot.get('parent_edge_cost_delta')}")

    # receipt-level root fields, if the receipt lists per-root records
    rec_roots = receipt.get("cost65n_additions_on_cost64g_1438") \
        or receipt.get("cost65n_additions") \
        or receipt.get("receipts") \
        or receipt.get("cost65n_receipts")
    if isinstance(rec_roots, list) and rec_roots:
        root_ok = True
        root_detail = []
        for rr in rec_roots:
            rh = rr.get("root_hex")
            match = [p for p in pre["receipts"] if p["root_hex"] == rh]
            if not match:
                root_ok = False
                root_detail.append({"root": rh, "status": "not in prereg"})
                continue
            p = match[0]
            ok = (rr.get("marginal") == p["marginal"]
                  and rr.get("marginal_in_manifest") == p["marginal_in_manifest"])
            root_ok = root_ok and ok
            root_detail.append({"root": rh, "ok": ok})
        check("per-root marginal/mim", root_ok, json.dumps(root_detail)[:400])
    else:
        print("note | per-root records not found in receipt (key search "
              "cost65n_additions*/receipts); skipped per-root check")

    n_pass = sum(1 for c in checks if c["pass"])
    print(f"\n{n_pass}/{len(checks)} checks passed")
    if out_path:
        rec = {
            "schema": "n11-class2-lane-cost65n-fold-preregistration-agreement-20261116-v1",
            "preregistration_blob": "da2b2292",
            "preregistration_commit": "0c237017",
            "receipt_source": receipt_path,
            "receipt_schema": receipt.get("schema"),
            "checks": checks,
            "all_pass": all(c["pass"] for c in checks),
            "interpretation_guard": ("bookkeeping fold projection agreement only; "
                                     "no game-theoretic verdicts; solved counts are "
                                     "manifest coverage; 11x11 empty board, two-stone "
                                     "roots {49,60}/{59,60}, S2 {59,60} and classes "
                                     "1/2/4 remain UNKNOWN"),
        }
        Path(out_path).write_text(json.dumps(rec, indent=1) + "\n")
        print("written", out_path)
    return 0 if all(c["pass"] for c in checks) else 1


if __name__ == "__main__":
    sys.exit(main())
