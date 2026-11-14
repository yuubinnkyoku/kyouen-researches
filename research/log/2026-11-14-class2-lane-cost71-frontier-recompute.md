# 2026-11-14 class2-lane after-cost71 frontier recompute

Long-term lane, 8th session, fifth result. Direct extension of this session's
recompute_frontier_cost70b_20261114.py: every staged control through the
published after-cost70b frontier (solved 913 / unique remaining 6,934 / sum
545,596 / open 5,198/408,868) is reproduced exactly (asserted), then this
session's cost-71 receipt (2 WIN7 roots, bits 9 and 70 of S6 child
00000000000000809082000000000004, both fully verified certificates, 59/59 and
52/52 sub-roots PASS, union 0/0) is added.

## Result

- **after cost-71: solved 917 / unique remaining 6,930 / sum 545,301 /
  open 5,197/408,797** (cost-71 addition: 13 covers / 10 marginal / 4 in-manifest).
- **best class-2 target S5 00000000000000809082000000000000: 13 -> 12 orbits
  (915 -> 844)**. Best class-4 (18/1,460) unchanged.
- Two consecutive runs byte-identical (JSON + both CSVs, md5 match).
- Operational note: the cost-70b certificates record has no "verdict" key;
  the cost-70b stage in this script reads root_hex directly (assert len==1)
  instead of filtering on verdict.
- Cheapest unswept children of the best class-2 target per the new
  top-candidates CSV: the cost-73 band (5 children, c1=2,c2=2), then cost-74.

## Status

11x11 empty board: UNKNOWN. Two-stone root {49,60}: UNKNOWN. S2 {59,60}: UNKNOWN.
class 2 / class 4 blockers: UNKNOWN. (Frontier bookkeeping over published
receipts; WIN7 certificates prove only individual 7-stone roots' depth-10 wins.)
