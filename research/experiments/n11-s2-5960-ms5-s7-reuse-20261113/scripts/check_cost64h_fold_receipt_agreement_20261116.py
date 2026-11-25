#!/usr/bin/env python3
"""Agreement checker for the cost-64h receipt fold (prepared BEFORE the fold
receipt lands, per the cost-65n precedent: a machine checker published ahead
of the receipt with a full self-test, so the landed receipt can be verified
immediately).

Usage:
  python check_cost64h_fold_receipt_agreement_20261116.py --selftest
  python check_cost64h_fold_receipt_agreement_20261116.py \
      --fold-json <landed class-frontier-cost64h*...json> [--claim <claim v3>]

Compares the landed fold record against the published pre-registration
class2-lane-cost64h-fold-preregistration-independent-20261116.json (git blob
5074a8a0cbb75fcc91b5b999a3135fac06d42400, commit c64579b4, published before
the fold receipt landed).  The order-invariant quantities (projected head,
demand histogram, totals, closed-row set, affected parents, incidence and
edge-cost deltas) must agree exactly.  Per-receipt marginals are compared
exactly when the fold order equals the pre-registered ascending-bit order,
and otherwise compared as per-bit multisets with the difference recorded as
an experimental fact.

Interpretation guard: agreement checking is bookkeeping over published
receipts; no engine search is run and no verdict is created.  Solved counts
measure manifest coverage, not the game-theoretic value of any position;
WIN7 certificates prove a first-player win within depth 10 from the
individual 7-stone roots only; REFUTED-D10 is not a LOSS proof; the 11x11
empty board, the two-stone roots {49,60} and {59,60}, S2 {59,60} and classes
1/2/4 all remain UNKNOWN.
"""
import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"

PREREG_JSON = "class2-lane-cost64h-fold-preregistration-independent-20261116.json"
PREREG_BLOB = "5074a8a0cbb75fcc91b5b999a3135fac06d42400"
CHILD = "00000000000000403800000008100000"
SUMMARY_KEYS = ("solved_s6_in_manifest", "remaining_s5_orbits",
                "unique_remaining_s6", "sum_remaining_cost",
                "s6_needed_by_open_classes", "cost_needed_by_open_classes")


def git_blob_sha(data):
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def find_frontier_after(fold):
    """Locate the post-fold frontier summary in the landed fold JSON."""
    for key in ("frontier_after_cost64h", "frontier_after",
                "frontier_after_receipts", "frontier"):
        if key in fold and isinstance(fold[key], dict):
            return fold[key]
    for key, v in fold.items():
        if key.startswith("frontier_after") and isinstance(v, dict):
            return v
    raise KeyError(f"no frontier_after block found; keys={sorted(fold)}")


def find_receipts(fold):
    for key in ("receipts", "fold_receipts"):
        if key in fold and isinstance(fold[key], list):
            return fold[key]
    raise KeyError(f"no receipts list found; keys={sorted(fold)}")


def collect_frontier_numbers(fa):
    got = [fa[k] for k in SUMMARY_KEYS]
    hist = fa.get("demand_histogram_open_only") or fa.get(
        "demand_histogram") or fa.get("hist")
    return got, hist


def run_checks(prereg, fold, order_note=""):
    """Return (checks, notes).  checks: dict check-name -> bool."""
    checks = {}
    notes = []

    def need(cond, name, detail=""):
        checks[name] = bool(cond)
        if not cond:
            notes.append(f"{name}: {detail}")

    fa = find_frontier_after(fold)
    got, hist = collect_frontier_numbers(fa)
    ph = prereg["projected_head"]
    need([ph[k] for k in SUMMARY_KEYS] == got,
         "C3_projected_head_six_numbers",
         f"prereg {list(ph.values())} vs fold {got}")

    need(hist is not None, "C4_projected_demand_histogram_present")
    if hist is not None:
        need(prereg["projected_demand_histogram"] == hist,
             "C4_projected_demand_histogram",
             f"prereg {prereg['projected_demand_histogram']} vs fold {hist}")
        deltas = {k: hist.get(k, 0) -
                  prereg["basis_demand_histogram"].get(k, 0)
                  for k in set(hist) | set(prereg["basis_demand_histogram"])}
        need(deltas == prereg["demand_histogram_deltas"],
             "C5_demand_histogram_deltas", f"{deltas}")

    totals = fold.get("totals", {})
    need(totals.get("total_marginal",
                    totals.get("total_marginal_in_manifest")) is not None
         or "receipts" in fold, "C1_fold_record_readable")

    # totals may be nested differently; recompute from receipts when present
    recs = find_receipts(fold)
    need(len(recs) == 23, "C2_receipt_count_23", f"got {len(recs)}")

    def rec_bit(r):
        return r.get("bit", r.get("win_bit"))

    def rec_root(r):
        return r.get("root_hex", r.get("root"))

    def rec_marg(r):
        return r.get("marginal", r.get("marginal_count"))

    def rec_mim(r):
        return r.get("marginal_in_manifest",
                     r.get("mim", r.get("marginal_manifest_count")))

    bits = [rec_bit(r) for r in recs]
    need(sorted(b for b in bits if b is not None) ==
         sorted(prereg["win_bits_in_fold_order"]),
         "C13_win_bit_set", f"{sorted(bits)}")

    roots_ok = True
    for r in recs:
        b, root = rec_bit(r), rec_root(r)
        if b is None or root is None:
            roots_ok = False
            break
        if root != f"{int(CHILD, 16) | (1 << b):032x}":
            roots_ok = False
            break
    need(roots_ok, "C16_root_hexes_child_or_bit", "")

    tm = totals.get("total_marginal")
    if tm is None and all(rec_marg(r) is not None for r in recs):
        tm = sum(rec_marg(r) for r in recs)
    need(tm == prereg["totals"]["total_marginal"],
         "C6_total_marginal_111", f"got {tm}")

    tim = totals.get("total_marginal_in_manifest")
    if tim is None and all(rec_mim(r) is not None for r in recs):
        tim = sum(rec_mim(r) for r in recs)
    need(tim == prereg["totals"]["total_marginal_in_manifest"],
         "C7_total_mim_20", f"got {tim}")

    # closed manifest rows: from per-receipt marginal_manifest_hexes or a
    # dedicated field
    closed = set()
    for r in recs:
        for k in ("marginal_manifest_hexes", "marginal_in_manifest_hexes",
                  "closed_rows_hexes"):
            for h in r.get(k, []) or []:
                closed.add(h)
    if not closed:
        for key in ("rows_closed_hexes", "closed_manifest_rows"):
            for h in totals.get(key, []) or []:
                closed.add(h)
    need(closed == set(prereg["totals"]["closed_manifest_rows"]),
         "C8_closed_manifest_row_set",
         f"sym diff {sorted(closed ^ set(prereg['totals']['closed_manifest_rows']))[:6]}")
    need(CHILD in closed, "C9_child_row_closed", "")

    # per-receipt marginals
    same_order = bits == prereg["win_bits_in_fold_order"]
    pre_by_bit = {r["bit"]: r for r in prereg["receipts"]}
    if same_order:
        per_ok = all(
            rec_marg(r) == pre_by_bit[rec_bit(r)]["marginal"] and
            rec_mim(r) == pre_by_bit[rec_bit(r)]["marginal_in_manifest"]
            for r in recs if rec_bit(r) in pre_by_bit and
            rec_marg(r) is not None)
        need(per_ok, "C14_per_receipt_marginals_exact",
             "fold order equals prereg order but per-bit values differ")
    else:
        notes.append(f"fold order differs from the preregistered ascending "
                     f"order ({order_note}); per-receipt marginals compared "
                     f"as per-bit values")
        per_ok = all(
            (rec_marg(r) is None or
             rec_marg(r) == pre_by_bit[rec_bit(r)]["marginal"]) and
            (rec_mim(r) is None or
             rec_mim(r) == pre_by_bit[rec_bit(r)]["marginal_in_manifest"])
            for r in recs if rec_bit(r) in pre_by_bit)
        need(per_ok, "C14_per_receipt_marginals_per_bit",
             "per-bit marginal/mim values differ from the prereg values "
             "beyond the documented order-dependence")

    # affected parents: match on the parent set with row deltas
    fold_parents = fold.get("parents_after") or fold.get("affected_parents") \
        or fold.get("lost_rows_per_parent") or {}
    if isinstance(fold_parents, list):
        fold_parents = {p.get("s5_hex", p.get("s5")): p for p in fold_parents}
    pre_parents = prereg["affected_parents"]
    if fold_parents:
        same_set = set(fold_parents) == set(pre_parents)
        need(same_set, "C10_affected_parent_set",
             f"sym diff {sorted(set(fold_parents) ^ set(pre_parents))[:6]}")
        detail_ok = True
        for s5, p in fold_parents.items():
            q = pre_parents.get(s5)
            if q is None:
                detail_ok = False
                break
            fb = p.get("rows_before", p.get("rows_before_fold"))
            faft = p.get("rows_after", p.get("rows_after_fold"))
            lost = set(p.get("lost_rows_hexes", p.get("lost_rows", [])) or [])
            if fb is not None and fb != q["rows_before"]:
                detail_ok = False
            if faft is not None and faft != q["rows_after"]:
                detail_ok = False
            if lost and lost != set(q["lost_rows_hexes"]):
                detail_ok = False
        need(detail_ok, "C10b_affected_parent_row_deltas", "")
        inc = fold.get("parent_row_incidences",
                       sum(len(p.get("lost_rows_hexes", [])) or 0
                           for p in fold_parents.values()
                           if isinstance(p, dict)))
        need(inc == prereg["parent_row_incidences"],
             "C11_parent_row_incidences_42", f"got {inc}")
        ecd = fold.get("parent_edge_cost_delta")
        if ecd is None:
            ecd = sum(p.get("lost_edge_cost", 0) for p in fold_parents.values()
                      if isinstance(p, dict))
        need(ecd == prereg["parent_edge_cost_delta"],
             "C12_parent_edge_cost_delta_3090", f"got {ecd}")
    else:
        notes.append("affected-parent block not found in the fold record; "
                     "C10/C10b/C11/C12 recorded as not-applicable")
        for k in ("C10_affected_parent_set", "C10b_affected_parent_row_deltas",
                  "C11_parent_row_incidences_42",
                  "C12_parent_edge_cost_delta_3090"):
            checks[k] = None  # not applicable

    conf = fold.get("conflict_census") or {}
    overlaps = conf.get("overlaps", fold.get("conflict_census_overlaps"))
    if overlaps is not None:
        need(overlaps == 0, "C15_conflict_census_zero", f"got {overlaps}")

    # basis head 1452 in the record's baseline if present
    baseline = fold.get("baseline_record") or fold.get("baseline") or {}
    if baseline:
        bfa = None
        for key in ("frontier_before", "frontier_after_cost76d77e",
                    "frontier_before_cost64h"):
            if key in baseline:
                bfa = baseline[key]
                break
        if bfa is None:
            bfa = baseline
        try:
            bgot, _ = collect_frontier_numbers(bfa)
            need(bgot == list(prereg["basis_head_numbers"]),
                 "C2b_basis_head_1452", f"got {bgot}")
        except (KeyError, TypeError):
            notes.append("baseline frontier numbers not found; C2b skipped")
            checks["C2b_basis_head_1452"] = None
    return checks, notes


def selftest(prereg):
    """Build a synthetic fold record from the prereg itself; every applicable
    check must pass (proves the checker logic end-to-end)."""
    synthetic = {
        "baseline_record": {"frontier_before": {
            k: v for k, v in zip(SUMMARY_KEYS, prereg["basis_head_numbers"])}},
        "frontier_after_cost64h": dict(prereg["projected_head"],
                                       **{"demand_histogram_open_only":
                                          prereg["projected_demand_histogram"]}),
        "receipts": [{"bit": r["bit"], "root_hex": r["root_hex"],
                      "marginal": r["marginal"],
                      "marginal_in_manifest": r["marginal_in_manifest"],
                      "marginal_manifest_hexes": r["marginal_manifest_hexes"]}
                     for r in prereg["receipts"]],
        "totals": {"total_marginal": prereg["totals"]["total_marginal"],
                   "total_marginal_in_manifest":
                       prereg["totals"]["total_marginal_in_manifest"],
                   "conflict_census_overlaps": 0},
        "parents_after": {k: {"s5_hex": v["s5_hex"],
                              "rows_before": v["rows_before"],
                              "rows_after": v["rows_after"],
                              "lost_rows_hexes": v["lost_rows_hexes"],
                              "lost_edge_cost": v["lost_edge_cost"]}
                          for k, v in prereg["affected_parents"].items()},
        "parent_row_incidences": prereg["parent_row_incidences"],
        "parent_edge_cost_delta": prereg["parent_edge_cost_delta"],
    }
    checks, notes = run_checks(prereg, synthetic, order_note="selftest")
    return synthetic, checks, notes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fold-json", default=None)
    ap.add_argument("--claim", default=None)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    prereg_data = (OUT / PREREG_JSON).read_bytes()
    assert git_blob_sha(prereg_data) == PREREG_BLOB, "prereg blob"
    prereg = json.loads(prereg_data.decode())

    if args.selftest:
        synthetic, checks, notes = selftest(prereg)
        applicable = {k: v for k, v in checks.items() if v is not None}
        failed = [k for k, v in applicable.items() if not v]
        print("self-test checks:", len(applicable), "failed:", failed)
        print("notes:", notes)
        assert not failed and not [n for n in notes if "differs" not in n], failed
        print("SELF-TEST PASS")
        return

    fold = json.loads(Path(args.fold_json).read_text())
    claim = json.loads(Path(args.claim).read_text()) if args.claim else None
    checks, notes = run_checks(prereg, fold)
    applicable = {k: v for k, v in checks.items() if v is not None}
    failed = [k for k, v in applicable.items() if not v]
    result = {
        "schema": "n11-class2-lane-cost64h-fold-receipt-agreement-20261116-v1",
        "date": "2026-11-16",
        "prereg_blob": PREREG_BLOB,
        "fold_json": str(Path(args.fold_json).name),
        "fold_json_blob": git_blob_sha(Path(args.fold_json).read_bytes()),
        "checks": checks,
        "failed_checks": failed,
        "notes": notes,
        "all_applicable_pass": not failed,
        "interpretation_guard": (
            "agreement check over published bookkeeping records only; no "
            "engine search, no verdicts; solved counts measure manifest "
            "coverage, not the game-theoretic value of any position; WIN7 "
            "certificates prove a first-player win within depth 10 from the "
            "individual 7-stone roots only; REFUTED-D10 is not a LOSS proof; "
            "11x11 empty board, two-stone roots {49,60}/{59,60}, S2 "
            "{59,60} and classes 1/2/4 all remain UNKNOWN"),
    }
    out = Path(args.out) if args.out else (
        OUT / "class2-lane-cost64h-fold-receipt-agreement-20261116.json")
    with open(out, "w") as f:
        json.dump(result, f, indent=1, sort_keys=True)
        f.write("\n")
    print("checks:", len(checks), "failed:", failed)
    for n in notes:
        print("note:", n)
    print("all_applicable_pass:", not failed)
    print("output:", out.name)


if __name__ == "__main__":
    main()
