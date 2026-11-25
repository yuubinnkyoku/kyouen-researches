#!/usr/bin/env python3
"""Verification-side crosscheck of the per-parent bookkeeping of the three
published head-1410 -> head-1476 fold records that touch the rank-1
partial-STERILE S5 parent's channel and its neighbouring parents:

  - class-frontier-cost76d77e-receipts-recompute-20261116.json (head 1450->1452)
  - class-frontier-cost76c-receipts-recompute-20261117.json   (head 1472->1473)
  - class-frontier-cost66i-bit19-receipts-recompute-20261118.json (head 1473->1476)

For every S5 parent listed in these records the script recomputes, from the raw
pinned head-1410 worklist (6,438 remaining S6 rows), the full D4 orbit join
(exists sigma in D4 with sigma(P) subset R) and then verifies:

  - receipt coverage: every closed/marginal row is a canon one-stone reduction
    of its fold's WIN7-D10 root (orbit-level receipt semantics),
  - membership: every lost row of a parent is a D4 child of that parent,
  - arithmetic: lost-row cost sums, rows_before/after and edge-cost deltas,
  - baselines: rows_before never exceeds the head-1410 join count; the
    difference is recorded per parent as the effect of earlier folds,
  - the cost66i marginal incidences (7 parent-incidences over 3 unique rows).

No engine is run; no new verdict is produced. REFUTED-D10 is not a LOSS proof.

Usage: python3 crosscheck_fold_parent_bookkeeping_20261118.py --input-dir in --output out.json
"""
import argparse
import csv
import hashlib
import json
import sys

N = 11

TFS = [
    lambda x, y: (x, y),
    lambda x, y: (y, N - 1 - x),
    lambda x, y: (N - 1 - x, N - 1 - y),
    lambda x, y: (N - 1 - y, x),
    lambda x, y: (N - 1 - x, y),
    lambda x, y: (x, N - 1 - y),
    lambda x, y: (y, x),
    lambda x, y: (N - 1 - y, N - 1 - x),
]

INPUT_PINS = {
    "worklist1410.csv": "2fee1d0718547a62e346d35f5858d7913e37c097",
    "fold76d77e.json": "8d4bc622f9da22b8754f2e398e5481359656d956",
    "fold76c.json": "953beaea054989e8b1de33f48b1f2ebc13ae7e11",
    "fold66i.json": "a555ee3a575df04ecddf98ce890bd8eec53dd415",
    "claim76c.json": "678211c5a35c25cf41b4a56473942860903647f6",
    "claim66i.json": "f8556f6c054d821e845b7ebe5035b8c280d2e97b",
    "reconc.json": "6992f2dcc8b87a5409cff31c8a87134fc4283a6a",
}

ROW_76C = "00000000010000809002000001000000"
ROW_76D = "00000000040000003800080008000000"
ROW_77E = "00000000040000809002000000004000"

CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append({"check": name, "pass": bool(ok), "detail": detail if isinstance(detail, str) else json.dumps(detail)})


def stone_bits(mask):
    return [i for i in range(N * N) if (mask >> i) & 1]


def apply_t(mask, t):
    out = 0
    for i in stone_bits(mask):
        x, y = i % N, i // N
        x2, y2 = t(x, y)
        out |= 1 << (y2 * N + x2)
    return out


def canon(mask):
    return min(apply_t(mask, t) for t in TFS)


def hx(mask):
    return format(mask, "032x")


def popcount(m):
    return bin(m).count("1")


def git_blob_sha(data):
    return hashlib.sha1(b"blob %d\x00" % len(data) + data).hexdigest()


JOIN_CACHE = {}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-dir", default="in")
    ap.add_argument("--output", default="out.json")
    args = ap.parse_args()
    from pathlib import Path

    d = Path(args.input_dir)
    for name, pin in INPUT_PINS.items():
        data = (d / name).read_bytes()
        check("pin." + name.rsplit(".", 1)[0], git_blob_sha(data) == pin, git_blob_sha(data))

    work_rows = list(csv.DictReader((d / "worklist1410.csv").open()))
    wl = {r["s6_canonical_hex"]: r for r in work_rows}
    cost = {h: int(r["own_candidates_s6_s7_edge_cost"]) for h, r in wl.items()}
    category = {h: r["category"] for h, r in wl.items()}
    fold76d77e = json.loads((d / "fold76d77e.json").read_bytes())
    fold76c = json.loads((d / "fold76c.json").read_bytes())
    fold66i = json.loads((d / "fold66i.json").read_bytes())
    claim76c = json.loads((d / "claim76c.json").read_bytes())
    claim66i = json.loads((d / "claim66i.json").read_bytes())
    reconc = json.loads((d / "reconc.json").read_bytes())

    check("book.worklist_rows", len(work_rows) == 6438, str(len(work_rows)))

    def join(parent_hex):
        """rows of the head-1410 worklist that are D4 children of the 5-stone parent"""
        if parent_hex in JOIN_CACHE:
            return JOIN_CACHE[parent_hex]
        pm = int(parent_hex, 16)
        imgs = [apply_t(pm, t) for t in TFS]
        kids = []
        for h in wl:
            rm = int(h, 16)
            if popcount(rm) != 6:
                continue
            for im in imgs:
                if im & ~rm == 0:
                    kids.append(h)
                    break
        JOIN_CACHE[parent_hex] = kids
        return kids

    # ---------- parent universe ----------
    parents = sorted(set(fold76d77e["parents_after"]) | set(fold76c["parents_after"]) | set(fold66i["parents_after"]))
    check("book.parents_union",
          len(parents) == 9 and all(popcount(int(p, 16)) == 5 for p in parents)
          and all(len(join(p)) >= 1 for p in parents), json.dumps(parents))
    join_stats = {}
    for p in parents:
        kids = join(p)
        join_stats[p] = {"rows_1410": len(kids), "cost_1410": sum(cost[h] for h in kids)}

    # ---------- fold76d77e ----------
    pa = fold76d77e["parents_after"]
    check("fd76d77e.parent_count", len(pa) == 3, str(len(pa)))
    jA, jB, jP = join("00000000000000003800000208000000"), join("00000000000000801202000000040000"), join("00000000000000801202000040000000")
    check("fd76d77e.membership",
          ROW_76D in jA and ROW_76D in jP and ROW_76D not in jB
          and ROW_77E in jB and ROW_77E in jP and ROW_77E not in jA, "")
    eA, eB, eP = pa["00000000000000003800000208000000"], pa["00000000000000801202000000040000"], pa["00000000000000801202000040000000"]
    check("fd76d77e.parent_A_arithmetic",
          eA["rows_before"] - eA["rows"] == 1 and eA["edge_cost_before"] - eA["edge_cost"] == cost[ROW_76D]
          and eA["rows_before"] == len(jA) and eA["edge_cost_before"] == join_stats["00000000000000003800000208000000"]["cost_1410"], "")
    check("fd76d77e.parent_B_arithmetic",
          eB["rows_before"] - eB["rows"] == 1 and eB["edge_cost_before"] - eB["edge_cost"] == cost[ROW_77E]
          and eB["rows_before"] <= len(jB)
          and join_stats["00000000000000801202000000040000"]["cost_1410"] - eB["edge_cost_before"] == 153, "")
    check("fd76d77e.parent_P_arithmetic",
          eP["rows_before"] - eP["rows"] == 2 and eP["edge_cost_before"] - eP["edge_cost"] == cost[ROW_76D] + cost[ROW_77E]
          and eP["rows_before"] == len(jP) and eP["edge_cost_before"] == 364, "")

    # ---------- fold76c ----------
    pa = fold76c["parents_after"]
    check("fd76c.parent_count", len(pa) == 4, str(len(pa)))
    ok = True
    lost_union = set()
    for ph, e in sorted(pa.items()):
        kids = join(ph)
        lost = e.get("lost_rows_hexes", [])
        lost_union |= set(lost)
        ok = ok and set(lost) <= set(kids)
        ok = ok and sum(cost[x] for x in lost) == e["lost_edge_cost"]
        ok = ok and e["rows_after"] == e["rows_before"] - e["lost_rows"]
        ok = ok and e["edge_cost_after"] == e["edge_cost_before"] - e["lost_edge_cost"]
        ok = ok and 0 <= e["rows_before"] <= join_stats[ph]["rows_1410"]
        ok = ok and 0 <= e["edge_cost_before"] <= join_stats[ph]["cost_1410"]
    check("fd76c.per_parent_membership_and_arithmetic", ok, "")
    check("fd76c.lost_union",
          lost_union == {ROW_76C, ROW_76D, ROW_77E}, json.dumps(sorted(lost_union)))
    check("fd76c.lost_rows_nonsterile",
          all(category[x] != "sterile" for x in lost_union), json.dumps({x: category[x] for x in sorted(lost_union)}))
    check("fd76c.basis_head",
          fold76c["basis_head"] == 1472 and fold76c["baseline_record"]["frontier_before"]["sum_remaining_cost"] == 504672
          and claim76c["receipt_fold"]["basis_head"] == [1472, 174, 6376, 504672, 4649, 368586], "")
    fr = fold76c["receipts"][0]
    root61 = int(fr["root_hex"], 16)
    reds61 = {hx(canon(root61 ^ (1 << b))) for b in stone_bits(root61)}
    check("fd76c.receipt_covers_marginal",
          len(reds61) == 7 and set(fr["marginal_manifest_hexes"]) <= reds61 and ROW_76C in fr["marginal_manifest_hexes"], "")
    check("fd76c.frontier_after",
          fold76c["frontier_after_cost76c"]["solved_s6_in_manifest"] == 1473
          and fold76c["frontier_after_cost76c"]["sum_remaining_cost"] == 504596
          and fold76c["frontier_after_cost76c"]["unique_remaining_s6"] == 6375, "")

    # ---------- fold66i ----------
    pa = fold66i["parents_after"]
    check("fd66i.parent_count", len(pa) == 5, str(len(pa)))
    r66 = fold66i["receipts"][0]
    marg = r66["marginal_manifest_hexes"]
    root66 = int(r66["root_hex"], 16)
    reds66 = {hx(canon(root66 ^ (1 << b))) for b in stone_bits(root66)}
    check("fd66i.receipt_covers_marginal",
          len(reds66) == 7 and set(marg) <= reds66 and all(hx(canon(int(m, 16))) == m for m in marg), "")
    check("fd66i.marginal_costs",
          all(m in cost for m in marg) and sum(cost[m] for m in marg) == 207
          and fold66i["totals"]["s6_edge_cost_removed"] == 207, json.dumps({m: cost[m] for m in marg}))
    ok = True
    incidences = 0
    derived_lost = {}
    for ph, e in sorted(pa.items()):
        kids = join(ph)
        derived = [m for m in marg if m in kids]
        derived_lost[ph] = derived
        incidences += len(derived)
        ok = ok and len(derived) == e["lost_rows"]
        ok = ok and sum(cost[m] for m in derived) == e["lost_edge_cost"]
        ok = ok and e["rows_after"] == e["rows_before"] - e["lost_rows"]
        ok = ok and e["edge_cost_after"] == e["edge_cost_before"] - e["lost_edge_cost"]
        ok = ok and 0 <= e["rows_before"] <= join_stats[ph]["rows_1410"]
        ok = ok and 0 <= e["edge_cost_before"] <= join_stats[ph]["cost_1410"]
    check("fd66i.per_parent_derived_lost_and_arithmetic", ok, json.dumps(derived_lost))
    check("fd66i.incidence_total", incidences == 7 and len(set(marg)) == 3, str(incidences))
    check("fd66i.basis_chain",
          fold66i["basis_head"]["solved_s6_in_manifest"] == 1473 and fold66i["basis_head"]["sum_remaining_cost"] == 504596
          and claim66i["receipt_fold"]["basis_head"] == [1473, 174, 6375, 504596, 4648, 368510]
          and [fold66i["frontier_after_cost66i_bit19"][k] for k in ("solved_s6_in_manifest", "remaining_s5_orbits", "unique_remaining_s6", "sum_remaining_cost", "s6_needed_by_open_classes", "cost_needed_by_open_classes")] == [1476, 174, 6372, 504389, 4645, 368303], "")
    check("fd66i.head_matches_reconciliation",
          reconc["current_parent"]["head"] == "1476/174/6372/504389/4645/368303"
          and reconc["fold_reconciliation"]["cost66i_bit19"]["target_parent_affected"] is False, "")

    # ---------- baseline deltas (facts, not assertions about unpublished folds) ----------
    baseline_facts = {}
    for tag, fold, key in (("fold76d77e", fold76d77e, None), ("fold76c", fold76c, None)):
        pas = fold["parents_after"]
        for ph, e in sorted(pas.items()):
            if tag == "fold76d77e":
                rb, eb = e["rows_before"], e["edge_cost_before"]
            else:
                rb, eb = e["rows_before"], e["edge_cost_before"]
            baseline_facts[tag + ":" + ph] = {
                "rows_before": rb, "edge_cost_before": eb,
                "join1410_rows": join_stats[ph]["rows_1410"], "join1410_cost": join_stats[ph]["cost_1410"],
                "rows_closed_by_earlier_folds": join_stats[ph]["rows_1410"] - rb,
                "cost_closed_by_earlier_folds": join_stats[ph]["cost_1410"] - eb,
            }
    ok = True
    for k, v in baseline_facts.items():
        if v["rows_closed_by_earlier_folds"] < 0 or v["cost_closed_by_earlier_folds"] < 0:
            ok = False
        if v["rows_closed_by_earlier_folds"] > 0 and v["cost_closed_by_earlier_folds"] <= 0:
            ok = False
        if v["rows_closed_by_earlier_folds"] == 0 and v["cost_closed_by_earlier_folds"] != 0:
            ok = False
    check("book.baseline_deltas_consistent", ok, json.dumps({k: v["rows_closed_by_earlier_folds"] for k, v in sorted(baseline_facts.items())}))

    all_pass = all(c["pass"] for c in CHECKS)
    out = {
        "schema": "n11-fold-parent-bookkeeping-crosscheck-20261118-v1",
        "date": "2026-11-18",
        "lane": "n11 long-term lane, verification-side crosscheck session (standard 11x11 weak-resolution)",
        "title": "per-parent bookkeeping crosscheck of the three head-1410->head-1476 fold records (cost76d+77e, cost76c bit61, cost66i bit19) against the raw head-1410 worklist: orbit-join membership, receipt orbit-coverage, cost/row arithmetic, and baseline deltas for all nine touched S5 parents",
        "inputs": {k: v for k, v in INPUT_PINS.items()},
        "method": "fourth-implementation D4 orbit join recomputed per parent from the pinned 6,438-row head-1410 worklist; canon one-stone reduction sets recomputed per folded WIN7-D10 root; per-parent lost rows derived independently for the cost66i fold from membership of the receipt's marginal rows; no engine, no new verdict",
        "derived": {
            "parent_join_stats_1410": join_stats,
            "fold66i_derived_lost_per_parent": derived_lost,
            "baseline_facts": baseline_facts,
            "folded_roots_scanned": [hx(root61), hx(root66)],
        },
        "checks": CHECKS,
        "check_count": len(CHECKS),
        "all_pass": all_pass,
        "interpretation_guard": "Bookkeeping verification only. Membership and arithmetic of published fold records are confirmed against the raw worklist; baseline differences (rows closed by earlier folds) are recorded as observed facts without re-deriving the intermediate folds. REFUTED-D10 is not a LOSS proof; no S5 parent is closed by this audit.",
        "unknown_status": "11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN.",
    }
    with open(args.output, "w") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")
    print("checks:", len(CHECKS), "all_pass:", all_pass)
    for c in CHECKS:
        if not c["pass"]:
            print("FAIL:", c["check"], c["detail"][:300])
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
