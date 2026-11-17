#!/usr/bin/env python3
"""Cross-check of the coordinator sterile-parent correction against the lane's own
published data (verification-side audit, 2026-11-18).

The coordinator correction (commits 1d05b0a1/e3db912a/4ffdf3b6/8c04f41e) replaced
the cost82d claim v2 next-action (which pointed at the census v18/v19 runner-up as
the next D10 receipt-closure target) after the K0865-based sterile-parent filter
showed that the entire remaining v18/v19 pool belongs to a single
all_remaining_sterile S5 parent. The cost82e sweep was launched from claim v1
(43f9e07a) before the correction landed and is published as a labelled
cross-version revalidation of the historical STERILE row.

This script independently re-derives the correction's factual basis from four
pinned inputs, using only data already on main (no engine run):

  * census v19 (this lane, blob a0c6abaf0df163eddc35f8b8dc0f8c0eb4268fe6, commit 122cb6c6)
  * the K0865 head-1410 receipt-unclosability census (blob 9c251da3138c5cb0516e097be5e5d0427dfaf5f0)
  * the v18 sterile-parent filter audit (blob 60233241c6c48ab5085bf125b3edfb1cf56941a6)
  * the cost82e raw-batches audit (blob 49757780129b0e7de130245306237f3f108aa79d, commit beb41b19)

Checks:
  A. K0865 census totals (174/3/57/114/91/12274/12183) match the filter audit's k0865 block.
  B. The class-4 unclosable parent entry in K0865 matches the filter audit's parent block.
  C. Structure of the parent's 18 sterile refs: each ref differs from the parent by
     exactly one bit, ref hex == D4 canon(parent | 1<<bit), all 18 distinct, cost sum 1460.
  D. The filter audit's 9-row v18 candidate pool: all parents == the sterile parent,
     all rows among the 18 sterile refs, costs match, distinct, 0 eligible after the filter.
  E. census v19 ranking (8 rows) == filter-audit pool minus the swept cost82d row, and
     open_after_census_v19 == open_after_v18 - 2 for every one of the 8 rows
     (the 82d verdict map canon-covers 2 symmetric bits of every sibling row).
  F. census v19 families[parent] == the 18 sterile refs exactly; 10 rows are
     swept/excluded, 8 rows remain unswept, and the two sets are disjoint.
  G. cost82e cross-version revalidation consistency: the child is one of the 18 sterile
     refs (cost 82); the published sweep audit gives 0 WIN7-D10 / 82 REFUTED-D10 / 0 capped
     over exactly the census v19 selected_target bits (63 sweep + 19 confirmation = 82),
     with every per-bit root canon re-derived here as D4 canon(child | 1<<bit) - all
     REFUTED-D10, consistent with the K0865 STERILE classification of this row.
  H. Pin check of the four inputs (git blob sha1 of "blob <len>\\0" + content).

No new game verdict is created here. REFUTED-D10 is not a LOSS proof, STERILE is not
a LOSS proof, and the 11x11 empty board, the two-stone roots {49,60}/{59,60}, S2
{59,60} and classes 1/2/4 all remain UNKNOWN.
"""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]          # experiments/n11-s2-5960-ms5-s7-reuse-20261113/
EXP = HERE.parent                                    # experiments/
LANE_OUT = HERE / "output"
K0865 = EXP / "n11-head1410-receipt-unclosability-census-20261116" / "output" / "n11-head1410-receipt-unclosability-census-20261116.json"

PINS = {
    "census_v19": ("class2-lane-next-target-presweep-1473-v19-20261118.json", "a0c6abaf0df163eddc35f8b8dc0f8c0eb4268fe6"),
    "k0865": ("n11-head1410-receipt-unclosability-census-20261116.json", "9c251da3138c5cb0516e097be5e5d0427dfaf5f0"),
    "filter_audit": ("class2-lane-presweep-v18-sterile-parent-filter-audit-20261118.json", "60233241c6c48ab5085bf125b3edfb1cf56941a6"),
    "cost82e_audit": ("class2-lane-cost82e-raw-batches-1-8-audit-20261118.json", "49757780129b0e7de130245306237f3f108aa79d"),
}
PARENT = int("00000000020000003800000080000000", 16)
COST82D_ROW = "00000000020000003800000080000800"
COST82E_CHILD = "00000000020000003800000090000000"


def images(mask):
    result = [0] * 8
    for p in range(121):
        if mask >> p & 1:
            x, y = p % 11, p // 11
            coords = ((x, y), (y, 10 - x), (10 - x, 10 - y), (10 - y, x),
                      (10 - x, y), (x, 10 - y), (y, x), (10 - y, 10 - x))
            for i, (a, b) in enumerate(coords):
                result[i] |= 1 << (11 * b + a)
    return result


IMG = [images(1 << p) for p in range(121)]


def canon(mask):
    best = None
    for r in range(8):
        v = 0
        for p in range(121):
            if mask >> p & 1:
                v |= IMG[p][r]
        if best is None or v < best:
            best = v
    return best


def gitblob(data):
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def main():
    results = {}
    checks = []

    def check(name, ok, detail=""):
        checks.append({"check": name, "pass": bool(ok), "detail": detail})
        if not ok:
            raise AssertionError("FAILED: %s %s" % (name, detail))
        print("PASS", name, detail)

    # ---- H. pin check
    files = {}
    for key, (name, pin) in PINS.items():
        path = LANE_OUT / name if key != "k0865" else K0865
        raw = path.read_bytes()
        b = gitblob(raw)
        check("H.pin.%s" % key, b == pin, "%s (%d bytes)" % (b, len(raw)))
        files[key] = json.loads(raw)
    v19, k0865, fa, c82e = files["census_v19"], files["k0865"], files["filter_audit"], files["cost82e_audit"]

    # ---- A. K0865 totals
    t = k0865["census_totals"]
    exp = {"open_s5": 174, "unclosable": 3, "partial": 57, "no_sterile": 114,
           "sterile_refs": 91, "remaining_row_refs": 12274, "eff_remaining": 12183}
    for k, v in exp.items():
        check("A.totals.%s" % k, t[k] == v, "%s" % t[k])
    fk = fa["k0865"]
    for k, v in exp.items():
        if k in fk:
            check("A.filter_audit_k0865.%s" % k, fk[k] == v, "%s" % fk[k])

    # ---- B. unclosable parent entry
    unc = [u for u in k0865["unclosable_s5"] if int(u["hex"], 16) == PARENT]
    check("B.parent_in_unclosable", len(unc) == 1, "%d entries" % len(unc))
    u = unc[0]
    check("B.parent_rem", u["rem"] == 18, str(u["rem"]))
    check("B.parent_rem_cost", u["rem_cost"] == 1460, str(u["rem_cost"]))
    check("B.parent_sterile_cost", u["sterile_cost"] == 1460, str(u["sterile_cost"]))
    refs = u["sterile_refs"]
    check("B.parent_sterile_refs_count", len(refs) == 18, str(len(refs)))
    check("B.parent_classes", u["classes"] == 4, str(u["classes"]))
    fp = fa["parent"]
    check("B.filter_parent_hex", fp["hex"] == u["hex"], fp["hex"])
    check("B.filter_parent_rem", fp["remaining_s6_orbits"] == 18, str(fp["remaining_s6_orbits"]))
    check("B.filter_parent_sterile_cost", fp["sterile_cost"] == 1460, str(fp["sterile_cost"]))
    check("B.filter_parent_all18", fp["all_18_rows_sterile"] is True)

    # ---- C. structure of the 18 sterile refs
    ref_hexes = [r["hex"] for r in refs]
    check("C.refs_distinct", len(set(ref_hexes)) == 18)
    diff_bits = {}
    cost_sum = 0
    for r in refs:
        m = int(r["hex"], 16)
        d = m ^ PARENT
        check("C.one_bit_diff.%s" % r["hex"],
              d != 0 and (d & (d - 1)) == 0,
              "xor %032x" % d)
        bit = d.bit_length() - 1
        diff_bits[r["hex"]] = bit
        rc = canon(PARENT | (1 << bit))
        check("C.canon_equals_hex.%s" % r["hex"], rc == m, "canon %032x" % rc)
        check("C.popcount_six.%s" % r["hex"], bin(m).count("1") == 6, str(bin(m).count("1")))
        cost_sum += r["cost"]
    check("C.cost_sum_1460", cost_sum == 1460, str(cost_sum))
    check("C.parent_popcount_five", bin(PARENT).count("1") == 5, str(bin(PARENT).count("1")))

    # ---- D. filter audit's 9-row pool
    pool = fa["v18_candidate_pool"]
    check("D.pool_rows", len(pool) == 9, str(len(pool)))
    check("D.pool_distinct", len(set(r["s6_hex"] for r in pool)) == 9)
    ref_cost = {r["hex"]: r["cost"] for r in refs}
    for r in pool:
        check("D.pool_parent.%s" % r["s6_hex"], r["parent"] == u["hex"])
        check("D.pool_in_sterile_refs.%s" % r["s6_hex"], r["s6_hex"] in ref_cost, "")
        check("D.pool_cost.%s" % r["s6_hex"], r["cost"] == ref_cost[r["s6_hex"]],
              "%d" % r["cost"])
    check("D.eligible_zero", fa["eligible_count_after_sterile_filter"] == 0)
    check("D.selected_unclosable", fa["selected_is_unclosable"] is True)
    check("D.runner_up_unclosable", fa["runner_up_is_unclosable"] is True)
    check("D.all_rows_same_parent", fa["all_pool_rows_same_unclosable_parent"] is True)
    check("D.all_rows_in_registry", fa["all_pool_rows_in_sterile_registry"] is True)

    # ---- E. census v19 ranking vs the filter-audit pool
    rank = v19["ranking_top10"]
    check("E.v19_ranking_rows", len(rank) == 8, str(len(rank)))
    pool_hexes = {r["s6_hex"] for r in pool}
    rank_hexes = {r["s6_hex"] for r in rank}
    check("E.v19_pool_minus_82d", rank_hexes == pool_hexes - {COST82D_ROW})
    pool_open = {r["s6_hex"]: r["open_after_census_v18"] for r in pool}
    for r in rank:
        h = r["s6_hex"]
        check("E.parent.%s" % h, r["parent"] == u["hex"])
        check("E.cost.%s" % h, r["cost"] == ref_cost[h], "%d" % r["cost"])
        check("E.open_minus_two.%s" % h,
              r["open_after_census_v19"] == pool_open[h] - 2,
              "v18 %d -> v19 %d" % (pool_open[h], r["open_after_census_v19"]))

    # ---- F. census v19 family rows == the 18 sterile refs
    fam = v19["families_v19"][u["hex"]]
    fam_hexes = [r["s6_hex"] for r in fam]
    check("F.family_rows", len(fam) == 18, str(len(fam)))
    check("F.family_equals_refs", set(fam_hexes) == set(ref_hexes))
    fam_cost = {r["s6_hex"]: r["cost"] for r in fam}
    for r in refs:
        check("F.family_cost.%s" % r["hex"], fam_cost[r["hex"]] == r["cost"])
    swept = [r for r in fam if r.get("excluded")]
    remaining = [r for r in fam if not r.get("excluded")]
    check("F.swept_rows", len(swept) == 10, str(len(swept)))
    check("F.remaining_rows", len(remaining) == 8, str(len(remaining)))
    check("F.remaining_equals_ranking", {r["s6_hex"] for r in remaining} == rank_hexes)
    check("F.swept_disjoint", not ({r["s6_hex"] for r in swept} & rank_hexes))

    # ---- G. cost82e revalidation consistency
    check("G.child_in_refs", COST82E_CHILD in ref_cost, "cost %d" % ref_cost.get(COST82E_CHILD, -1))
    sel = v19["selected_target"]
    check("G.selected_child", sel["s6_hex"] == COST82E_CHILD)
    conf_bits = set()
    for entry in sel["confirmation_bits"]:
        conf_bits.add(entry["bit"] if isinstance(entry, dict) else entry)
    sel_bits = set(sel["sweep_bits"]) | conf_bits
    check("G.selected_bits_82", len(sel_bits) == 82, str(len(sel_bits)))
    check("G.audit_counts", c82e["counts"] == {"win7_d10": 0, "refuted_d10": 82, "capped": 0, "total_bits": 82},
          json.dumps(c82e["counts"]))
    check("G.audit_total_nodes", c82e["total_candidate_nodes"] == 70583627, str(c82e["total_candidate_nodes"]))
    check("G.audit_bits_match", set(int(b) for b in c82e["per_bit"]) == sel_bits)
    child = int(COST82E_CHILD, 16)
    for bstr, rec in c82e["per_bit"].items():
        bit = int(bstr)
        rc = canon(child | (1 << bit))
        check("G.root_canon.bit%s" % bit, rc == int(rec["root_canon"], 16),
              "%032x vs %s" % (rc, rec["root_canon"]))
        check("G.refuted.bit%s" % bit, rec["verdict"] == "REFUTED-D10", rec["verdict"])
    check("G.confirmation_match", c82e["confirmation_prediction_match"].startswith("19/19 REFUTED-D10"))
    check("G.v15_agreement", c82e["v15_crosscheck"]["agreement"].startswith("19/19"))
    check("G.pilot_controls", c82e["pilot_controls_pass"] == "8/8")

    result = {
        "schema": "n11-class2-lane-sterile-parent-correction-crosscheck-20261118-v1",
        "date": "2026-11-18",
        "role": "verification-side crosscheck of the coordinator sterile-parent correction (commits 1d05b0a1/e3db912a/4ffdf3b6/8c04f41e) by the long-term lane that published census v19, the cost82e claim v1 and the cost82e revalidation sweep",
        "inputs": {
            "census_v19": "git blob a0c6abaf0df163eddc35f8b8dc0f8c0eb4268fe6 (commit 122cb6c6, this lane)",
            "k0865": "git blob 9c251da3138c5cb0516e097be5e5d0427dfaf5f0 (commit 5ada304a, parallel lane)",
            "filter_audit": "git blob 60233241c6c48ab5085bf125b3edfb1cf56941a6 (commit 1d05b0a1, parallel lane; audited_main 43f9e07a)",
            "cost82e_audit": "git blob 49757780129b0e7de130245306237f3f108aa79d (commit beb41b19, this lane)",
        },
        "parent": {
            "hex": u["hex"],
            "classification": "all_remaining_sterile (K0865)",
            "remaining_s6_orbits": 18,
            "sterile_cost": 1460,
            "one_bit_diff_bits": {h: diff_bits[h] for h in ref_hexes},
        },
        "checks": checks,
        "check_count": len(checks),
        "all_pass": True,
        "key_findings": {
            "v18_pool_rows": 9,
            "v18_pool_all_in_sterile_parent": True,
            "v19_ranking_rows": 8,
            "v19_ranking_equals_v18_pool_minus_cost82d": True,
            "open_delta_v18_to_v19": "every one of the 8 remaining rows lost exactly 2 open bits to the 82d verdict map (the 2 symmetric bits each sibling row shares with the swept 82d child)",
            "family_split": "18 sterile refs = 10 swept/excluded rows + 8 remaining rows, set-equal to the census v19 family table",
            "cost82e_revalidation": "the swept 82e child is sterile ref #11 (cost 82); its published v17 sweep (0 WIN7-D10 / 82 REFUTED-D10 / 0 capped, 70,583,627 candidate nodes, det1/det7 field-identical, v15 crosscheck 19/19, all 82 per-bit root canons re-derived here) is consistent with the K0865 STERILE classification - a cross-version revalidation, not new receipt-closure progress",
            "eligible_rows_after_sterile_filter": 0,
            "correction_confirmed": "the coordinator correction's factual basis is independently reproduced: no row of the v18/v19 remaining pool can produce a D10 WIN7 receipt for its parent (K0863), so a D10 receipt-closure sweep of any of them would be misdirected; further historical-row sweeps are only cross-version revalidations",
        },
        "interpretation_guard": "verification-side bookkeeping only: no engine run, no new verdict. REFUTED-D10 is not a LOSS proof, STERILE is not a LOSS proof, and the 11x11 empty board, the two-stone roots {49,60}/{59,60}, S2 {59,60} and classes 1/2/4 all remain UNKNOWN.",
    }
    out = LANE_OUT / "class2-lane-sterile-parent-correction-crosscheck-20261118.json"
    out.write_text(json.dumps(result, indent=1, ensure_ascii=True) + "\n")
    print("wrote", out)
    print("checks:", len(checks), "all_pass")


if __name__ == "__main__":
    main()
