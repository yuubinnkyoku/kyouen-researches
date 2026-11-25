# 2026-11-14 class2-lane after-cost67 frontier recompute — solved 887 -> 898, best class-2 21 -> 18 orbits

## Method

Direct extension of `recompute_frontier_merged_20261114.py` (recompute_frontier_cost67_20261114.py):
every published staged control (baseline 638 through after-cost78b 875, after-cost65c 881,
after-cost65d 884, after-merged 887) is reproduced exactly (asserted) from the public inputs
on main, then the class2-lane cost-67 receipt is added: 4 WIN7 roots (bits 18/34/101/118 of
S6 child 00000000000000809082020000000000), all four fully verified certificates on main.
Sterile sweeps confirmed as controls: class4-lane cost-80c/81/82 and class2-lane cost-66a/66b.
Two consecutive runs produced byte-identical outputs.

## Frontier after cost-67

- solved_s6_in_manifest: **898** (887 + 11 in-manifest marginals)
- unique_remaining_s6: **6,949**
- sum_remaining_cost: **546,687**
- s6_needed_by_open_classes: **5,202** / cost_needed_by_open_classes: **409,163**
- cost-67 addition: 25 covers / 23 marginal / 11 in-manifest
- best class-2 blocker S5 `00000000000000809082000000000000`: **21 -> 18 orbits, cost 1,471 -> 1,260**
- best class-4 blocker S5 `00000000020000003800000080000000`: 18/1,460 unchanged

Cheapest unswept class-2 child after this stage (from the after-cost67 top-candidates CSV):
cost-68 `00000000000000809082000040000000` (c1=2,c2=2,c4=0).

## Artifacts

- `scripts/recompute_frontier_cost67_20261114.py`
- `output/class-frontier-cost67-recompute-20261114.json`
- `output/class-frontier-s5-ranking-after-cost67-20261114.csv`
- `output/class-frontier-top-candidates-s6-after-cost67-20261114.csv`

11x11 empty board, two-stone root {49,60}, S2 {59,60}, class 2 and class 4 all
remain UNKNOWN; this is bookkeeping over receipts, not a board-outcome result.
