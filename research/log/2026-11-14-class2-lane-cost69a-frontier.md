# 2026-11-14 class2-lane after-cost69a frontier recompute — solved 903 -> 909, best class-2 16 -> 15 orbits

Direct extension of recompute_frontier_cost68b_20261114.py
(recompute_frontier_cost69a_20261114.py): every published staged control reproduces
the published frontiers exactly (asserted, including after-cost68b
903/6944/546334/5201/409091), then the class2-lane cost-69a receipt is added
(3 WIN7 roots: bits 48/70/103 of S6 child 00000000000000809082000000000400,
all fully verified certificates on main). Two consecutive runs byte-identical.

## Frontier after cost-69a

- solved_s6_in_manifest: **909** (903 + 6 in-manifest marginals)
- unique_remaining_s6: **6,938** / sum_remaining_cost: **545,893**
- open: **5,199 / 408,942**
- cost-69a addition: 18 covers / 15 marginal / 6 in-manifest
- best class-2 S5 00000000000000809082000000000000: **16 -> 15 orbits, cost 1,123 -> 1,054**
- best class-4 (18/1,460) unchanged

Cheapest unswept class-2 children after this stage: the remaining cost-69 band
(00000000000000809082000000400000, 00000000000000809082000000800000,
00000000000000809082040000000000, 000000000000008090c2000000000000).

## Artifacts

- `scripts/recompute_frontier_cost69a_20261114.py`
- `output/class-frontier-cost69a-recompute-20261114.json`
- `output/class-frontier-s5-ranking-after-cost69a-20261114.csv`
- `output/class-frontier-top-candidates-s6-after-cost69a-20261114.csv`

11x11 empty board, two-stone root {49,60}, S2 {59,60}, class 2 and class 4 all
remain UNKNOWN; this is bookkeeping over receipts, not a board-outcome result.
