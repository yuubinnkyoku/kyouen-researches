# 2026-11-14 class-frontier cost-69c recompute — solved 909→912

Direct extension of recompute_frontier_cost69a_20261114.py. All staged controls
(baseline 638 through after-cost68b 903 and after-cost69a) reproduce the published
frontiers exactly (asserted). Sterile sweeps cost-69b / cost-69d / cost-70
(class2-lane) are control-confirmed (win7_d10 == 0, capped == 0 in each sweep record).

The class2-lane cost-69c receipt (1 WIN7 root `00000080000000809082040000000000`,
bit 103 of S6 child `00000000000000809082040000000000`) is added on top of
after-cost69a: 7 covers / 6 marginal / 3 in-manifest (fully additive, no overlap
with previously solved S6).

**Frontier after cost-69c:**
- **solved_s6_in_manifest 912** (909 + 3)
- **unique_remaining_s6 6935, sum 545666**
- **open 5198/408868**
- best class-2 S5 `00000000000000809082000000000000`: **14 orbits / 985** (was 15/1054 at after-cost69a)
- next class-2: `00000000000000809102000000000000` (40/2850), `00000000000000803202000000000000` (41/2776)
- best class-4 S5 `00000000020000003800000080000000`: 18 orbits / 1460 (unchanged)

Re-run byte-identical. Ranking + top-candidates CSVs regenerated (after-cost69c).

11x11 empty board, two-stone root {49,60}, S2 {59,60}, class 2 and class 4 all
remain UNKNOWN.
