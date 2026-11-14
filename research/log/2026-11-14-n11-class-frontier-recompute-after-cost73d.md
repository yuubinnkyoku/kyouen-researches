# 2026-11-14 n11 class frontier recompute after cost-73d: solved 920, best class-2 11 orbits

Long-term lane session 9. Direct extension of `recompute_frontier_cost71_20261114.py`: every staged control through after-cost71 is reproduced exactly (asserted 917 / 6,930 / 545,301 / 5,197 / 408,797), the sterile cost-73b / cost-73c / cost-73e sweeps are asserted receipt-free (win7_d10=0, capped=0), then the cost-73d receipt (1 WIN7 root `00000000000000809083000000004000`, verified certificate: 59/59 sub-roots PASS, union 0/0) is added.

- cost-73d addition: **7 covers / 6 marginal / 3 in-manifest**.
- **after cost-73d: solved 920 · unique remaining 6,927 · sum 545,068 · open 5,196 / 408,718**.
- best class-2 target S5 `00000000000000809082000000000000`: 12 -> **11 orbits** (844 -> 771). best class-4 unchanged (18 / 1,460).
- cost-73a is still in flight on the parallel lane (1 WIN7 bit 81 reported, records not yet landed) and contributes no receipt here.
- Two runs byte-identical (`class-frontier-cost73d-recompute-20261114.json` md5 `7b7eea8e49273bad555ba8b915980b11`).

Files: script `recompute_frontier_cost73d_20261114.py`, result `class-frontier-cost73d-recompute-20261114.json`, ranking CSVs `class-frontier-s5-ranking-after-cost73d-20261114.csv` / `class-frontier-top-candidates-s6-after-cost73d-20261114.csv`, receipt `class2-lane-cost73d-win7-certificates-20261114.json`.

## Status

Bookkeeping over published receipts only. 11x11 empty root, two-stone root {49,60}, S2 {59,60}, class 2, class 4: **UNKNOWN**.
