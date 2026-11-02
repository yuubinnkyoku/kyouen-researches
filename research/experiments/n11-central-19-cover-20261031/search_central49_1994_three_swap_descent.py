#!/usr/bin/env python3
"""Bounded, deterministic exact 3-for-3 descent from independently checked 2049.

Each round enumerates all 15,180 removed triples and all fifteen matchings
of their six ordinary S5 vertices.  Emits each step before continuing so a
timeout does not erase evidence.  This is a conditional geometry search.
"""
import json

import audit_central49_2092_three_swap as exact
import verify_central49_2092_two_swap_local_optimum as base
from verify_central49_2049_three_swap import REMOVED as FIRST_RM, ADDED as FIRST_AD

SECOND_RM = (
    "00000000000000203800000010800000",
    "00000000000000801002002000100800",
    "00000000000040203800000000000200",
)
SECOND_AD = (
    "00000000000000203800000010001000",
    "00000000000000203808000000000200",
    "00000000000000801002002000084000",
)


def replace(selected, removed, added):
    rm = {int(k, 16) for k in removed}
    ad = {int(k, 16) for k in added}
    exact.need(len(rm) == len(ad) == 3 and rm <= selected and not ad & selected,
               "invalid exchange")
    return (selected - rm) | ad


def main():
    selected = set(base.reconstruct())
    selected = replace(selected, FIRST_RM, FIRST_AD)
    selected = replace(selected, SECOND_RM, SECOND_AD)
    current = 1994
    for step in range(1, 7):
        result = exact.audit(selected, expected_baseline=current)
        print(json.dumps({"round": step, **result}, ensure_ascii=False), flush=True)
        if result["best_distinct_s7"] == current:
            print(json.dumps({"stopped": "three_swap_local_optimum",
                              "rounds": step, "distinct_s7": current,
                              "selected_s6_sha256": base.digest(selected)}),
                  flush=True)
            break
        exact.need(result["best_distinct_s7"] < current and result["best_swap"],
                   "invalid descent step")
        move = result["best_swap"]
        selected = replace(selected, move["removed"], move["added"])
        current = result["best_distinct_s7"]
        print(json.dumps({"completed_round": step,
                          "new_distinct_s7": current,
                          "selected_s6_sha256": base.digest(selected)}),
              flush=True)
    else:
        print(json.dumps({"stopped": "six_round_budget", "distinct_s7": current,
                          "selected_s6_sha256": base.digest(selected)}),
              flush=True)


if __name__ == "__main__":
    main()
