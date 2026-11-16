#!/usr/bin/env python3
"""Cross-check the two new implementations and the prior complete 2-for-2 audit."""
from __future__ import annotations
import json
import os
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3] if len(HERE.parents)>3 else None
OUT=HERE/"output"

def load(path):
    return json.loads(path.read_text())

def main():
    cpp=load(OUT/"cpp_audit.json")
    py=load(OUT/"python_audit.json")
    assert cpp["target_width"]==py["target_width"]==60
    assert cpp["required_row_profile"]==py["required_row_profile"]==[3,3,3,3,3,3,2]
    cr=cpp["results"]; pr=py["results"]
    assert [(r["seed"],r["native_width"],r["candidates"],r["safe"],r["safe_maximal"]) for r in cr] == \
           [(r["seed"],r["native_width"],r["candidates"],r["safe"],r["safe_maximal"]) for r in pr]
    assert all(r["safe_maximal"]==0 for r in cr)
    prior_path=(ROOT/"research/experiments/seven-row-q4-width59-two-swap-20261115/output/two_swap_audit.json") if ROOT is not None else Path(os.environ["PRIOR_AUDIT"])
    prior=load(prior_path)
    byname={r["name"]:r for r in prior["results"]}
    prior_rows=[]
    for name,seed in (("base53_on_7x60","base53"),("foundB_on_7x60","foundB_7x59")):
        r=byname[name]
        assert r["width"]==60 and r["row_capacity_candidates"]==1599648 and r["safe_maximal_row_deficient"]==0
        prior_rows.append({"seed":seed,"candidates":r["row_capacity_candidates"],
                           "safe":r["safe_candidates"],"safe_maximal":r["safe_maximal_row_deficient"]})
    one_rows=[{"seed":r["seed"],"candidates":r["candidates"],"safe":r["safe"],
               "safe_maximal":r["safe_maximal"]} for r in cr]
    out={
      "status":"finite-local-negative",
      "board":{"width":60,"height":7,"q":4},
      "required_row_profile":[3,3,3,3,3,3,2],
      "one_for_one":{"method":"independent exact integer implementations agree",
                      "cpp_method":cpp["method"],"python_method":py["method"],"results":one_rows},
      "prior_two_for_two":{"source":"research/experiments/seven-row-q4-width59-two-swap-20261115/output/two_swap_audit.json",
                           "results":prior_rows},
      "bounded_neighborhood_conclusion":"Neither seed has a safe maximal 7x60 configuration within 0, 1-for-1, or 2-for-2 relocations while preserving the 20-stone row profile.",
      "global_claim":False,
      "M_7_4_bound_unchanged":"60 <= M_{7,4} <= 1929",
      "all_checks_pass":True
    }
    path=OUT/"audit.json"
    path.write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+"\n")
    print(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True))

if __name__=="__main__": main()
