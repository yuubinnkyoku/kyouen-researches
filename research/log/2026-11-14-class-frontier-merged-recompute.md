# 2026-11-14 class-frontier merged recompute — both lanes' receipts unified: solved 875→887

The class2-lane (cost-65c: 3 WIN7, cost-65d: 1 WIN7) and the parallel class4-lane
(cost-80b: 1 WIN7, plus sterile cost-80c/81/82) receipts were published
concurrently against the same after-cost78b baseline (875/6972/548362/5212/409908).

`scripts/recompute_frontier_merged_20261114.py` reproduces every staged control
(after-cost78b, after-cost65c 881/6966/547927, after-cost65d 884/6963/547712) and the
parallel lane's published after-cost80b (878/6969/548122) as a cross-check, then
adds the cost-80b receipt (7 covers / 6 marginal / 3 in-manifest) on top of the
class2-lane additions.

**Frontier after merged (all published receipts on main at merge time):**
- **solved_s6_in_manifest 887** (= 875 + 6 cost65c + 3 cost65d + 3 cost80b, fully
  additive, no double coverage between lanes)
- **unique_remaining_s6 6960, sum 547472**
- **open 5206/409451**
- best class-4 S5 `00000000020000003800000080000000`: 18 orbits / 1460
- best class-2 S5 `00000000000000809082000000000000`: 21 orbits / 1471

Re-run byte-identical. Ranking + top-candidates CSVs regenerated (after-merged).

11x11 empty board, two-stone root {49,60}, S2 {59,60}, class 2 and class 4 all
remain UNKNOWN.
