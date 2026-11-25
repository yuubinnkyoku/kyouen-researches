#!/usr/bin/env python3
"""Audit the v18 target pool against the head-1410 STERILE parent census."""
from __future__ import annotations
import hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = ROOT / "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output"
V18_PATH = EXP / "class2-lane-next-target-presweep-1473-v18-20261118.json"
K0865_PATH = ROOT / "research/experiments/n11-head1410-receipt-unclosability-census-20261116/output/n11-head1410-receipt-unclosability-census-20261116.json"
OUT = EXP / "class2-lane-presweep-v18-sterile-parent-filter-audit-20261118.json"
V18_BLOB = "11306824f2363d5002559d4d1535d91a61509929"
K0865_BLOB = "9c251da3138c5cb0516e097be5e5d0427dfaf5f0"

def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\\0" + data).hexdigest()

def canon(mask: int) -> str:
    best = None
    for t in range(8):
        out = 0
        for p in range(121):
            if mask >> p & 1:
                x, y = p % 11, p // 11
                images = ((x,y),(y,10-x),(10-x,10-y),(10-y,x),
                          (10-x,y),(x,10-y),(y,x),(10-y,10-x))
                a,b = images[t]
                out |= 1 << (11*b+a)
        best = out if best is None or out < best else best
    return f"{best:032x}"

def main() -> None:
    v18_raw = V18_PATH.read_bytes()
    k_raw = K0865_PATH.read_bytes()
    assert git_blob_sha(v18_raw) == V18_BLOB
    assert git_blob_sha(k_raw) == K0865_BLOB
    v18, k = json.loads(v18_raw), json.loads(k_raw)
    unclosable = {x["d4_canon"] for x in k["unclosable_s5"]}
    sterile = {x["canon"] for x in k["sterile_row_registry"]}
    rows = []
    for parent, children in v18["families_v18"].items():
        for child in children:
            if not child.get("excluded") and child.get("open_after_census_v18",0) > 0:
                rows.append({
                    "parent":parent, "s6_hex":child["s6_hex"],
                    "parent_canon":canon(int(parent,16)),
                    "s6_canon":canon(int(child["s6_hex"],16)),
                    "cost":child["cost"],
                    "open_after_census_v18":child["open_after_census_v18"],
                    "demand":child["demand"],
                })
    parent_hex = "00000000020000003800000080000000"
    parent = next(x for x in k["unclosable_s5"] if x["d4_canon"] == canon(int(parent_hex,16)))
    selected = v18["selected_target"]
    runner = v18["ranking_top10"][1]
    eligible = [x for x in rows if x["parent_canon"] not in unclosable and x["s6_canon"] not in sterile]
    assert len(rows) == 9
    assert parent["rem"] == 18 and len(parent["sterile_refs"]) == 18
    assert all(x["parent_canon"] == parent["d4_canon"] for x in rows)
    assert all(x["s6_canon"] in sterile for x in rows)
    assert not eligible
    assert canon(int(selected["parent"],16)) in unclosable
    assert canon(int(selected["s6_hex"],16)) in sterile
    assert canon(int(runner["parent"],16)) in unclosable
    assert canon(int(runner["s6_hex"],16)) in sterile

    result = {
        "schema":"n11-class2-lane-presweep-v18-sterile-parent-filter-audit-20261118-v1",
        "source_pins":{"v18_json_blob":V18_BLOB,"K0865_census_blob":K0865_BLOB},
        "v18_candidate_pool":rows,
        "v18_candidate_count":len(rows),
        "selected_is_sterile":True,"runner_up_is_sterile":True,
        "parent":{"hex":parent["hex"],"d4_canon":parent["d4_canon"],
                  "classification":"all_remaining_sterile","remaining_s6":parent["rem"],
                  "remaining_edge_cost":parent["rem_cost"],
                  "sterile_refs":len(parent["sterile_refs"])},
        "census":{"open_s5":k["census_totals"]["open_s5"],
                  "all_remaining_sterile":k["census_totals"]["unclosable"],
                  "partial_sterile":k["census_totals"]["partial"],
                  "no_sterile":k["census_totals"]["no_sterile"],
                  "sterile_rows":k["census_totals"]["sterile_refs"]},
        "eligible_after_sterile_filter":eligible,
        "eligible_count_after_sterile_filter":len(eligible),
        "selection_policy_omits_K0865_filter":("K0865" not in v18["selection_policy"] and
                                                "sterile" not in v18["selection_policy"].lower()),
        "recommended_action":"Rebuild the next-target census from the current head-1473 worklist with K0865/K0863 STERILE-parent exclusions before ranking. Keep historical cross-version revalidation as a separate objective.",
        "interpretation_guard":"No game verdict is created. All nine remaining v18 candidates lie in one all_remaining_sterile parent; the v18 pool has zero D10 receipt-closure candidates. REFUTED-D10 is not LOSS.",
        "all_pass":True,
    }
    OUT.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\\n",encoding="utf-8")
    print(json.dumps(result,indent=2,ensure_ascii=False))

if __name__ == "__main__":
    main()
