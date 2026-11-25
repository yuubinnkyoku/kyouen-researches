# 2026-11-14 class2-lane after-cost68b frontier recompute — solved 898 -> 903, best class-2 18 -> 16 orbits

## Method

Direct extension of `recompute_frontier_cost67_20261114.py` (`recompute_frontier_cost68b_20261114.py`):
every published staged control (baseline 638 through after-merged 887 and after-cost67
898/6,949/546,687/5,202/409,163) is reproduced exactly (asserted) from the public inputs on
main, then the class2-lane cost-68b receipt is added: 2 WIN7 roots (bits 23/118 of S6 child
`00000000000000809082000040000000`), both fully verified certificates on main.
Two consecutive runs produced byte-identical outputs (md5-checked).

## Frontier after cost-68b

- solved_s6_in_manifest: **903** (898 + 5 in-manifest marginals)
- unique_remaining_s6: **6,944**
- sum_remaining_cost: **546,334**
- s6_needed_by_open_classes: **5,201** / cost_needed_by_open_classes: **409,091**
- cost-68b addition: 13 covers / 11 marginal / 5 in-manifest
- best class-2 blocker S5 `00000000000000809082000000000000`: **18 -> 16 orbits, cost 1,260 -> 1,123**
- best class-4 blocker S5 `00000000020000003800000080000000`: 18/1,460 unchanged

Cheapest unswept class-2 children after this stage (from the after-cost68b top-candidates
CSV): the cost-69 band `00000000000000809082000000000400`, `00000000000000809082000000400000`,
`00000000000000809082040000000000`, `000000000000008090c2000000000000` (all c1=2,c2=2,c4=0
except the third, c2=1).

## Artifacts

- `scripts/recompute_frontier_cost68b_20261114.py`
- `output/class-frontier-cost68b-recompute-20261114.json`
- `output/class-frontier-s5-ranking-after-cost68b-20261114.csv`
- `output/class-frontier-top-candidates-s6-after-cost68b-20261114.csv`

11x11 empty board, two-stone root {49,60}, S2 {59,60}, class 2 and class 4 all
remain UNKNOWN; this is bookkeeping over receipts, not a board-outcome result.
