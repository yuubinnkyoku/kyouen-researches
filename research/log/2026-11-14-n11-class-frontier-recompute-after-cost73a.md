# 2026-11-14 n11 class frontier recompute after cost-73a: solved 921, best class-2 10 orbits, cost-73 band complete

Long-term lane session 11. Direct extension of `recompute_frontier_cost73d_20261114.py`:
every staged control through after-cost73d is reproduced exactly (asserted
920 / 6,927 / 545,068 / 5,196 / 408,718), the sterile cost-73b / cost-73c / cost-73e /
cost-74 sweeps are asserted receipt-free, the completed cost-73a sweep record is asserted
(1 WIN7-D10 bit81, 72 REFUTED, 0 capped, root
`00000000000200809082000000000010`), then the cost-73a receipt is added.

- cost-73a addition: **7 covers / 6 marginal / 1 in-manifest** (the swept child's own
  S6 orbit `00000000000000809082000000000010`).
- **after cost-73a: solved 921 · unique remaining 6,926 · sum 544,995 ·
  open 5,196 / 408,718** (open unchanged — the new cover is not demanded by any
  open-class S5 beyond this child's own orbit).
- best class-2 target S5 `00000000000000809082000000000000`: 11 -> **10 orbits**
  (771 -> 698). All 10 remaining S6 children of this target have now been swept and
  are sterile (65b/66a/66b/69b/69d/70/73b/73c/73e/74); sweeping this target's own
  subtree can no longer move its frontier. Closing it now requires either WIN7
  certificates from other parents covering those S6 orbits (cross-parent covers:
  each of those orbits has demand c1=2,c2=2, i.e. other S5 parents exist) or a
  direct refutation of the S5 candidate (SECOND_WIN route, as in the roadmap).
- best class-4 unchanged: `00000000020000003800000080000000` (18 / 1,460); the
  class4-lane parallel continues on the cost-84/cost-86 band.
- Two runs byte-identical. Files: script
  `recompute_frontier_cost73a_20261114.py`, result
  `class-frontier-cost73a-recompute-20261114.json`, ranking CSVs
  `class-frontier-s5-ranking-after-cost73a-20261114.csv` /
  `class-frontier-top-candidates-s6-after-cost73a-20261114.csv`, receipts
  `class2-lane-cost73a-win7-certificates-20261114.json` (bit81, fully verified:
  51/51 sub-roots PASS, union 0/0).

## Status

Bookkeeping over published receipts only. 11x11 empty root, two-stone root {49,60},
S2 {59,60}, class 2, class 4: **UNKNOWN**.

