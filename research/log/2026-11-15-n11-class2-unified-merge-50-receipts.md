# n11 class2-lane: unified merge of all 50 reconciled receipts (13 68d-lane + 31 multiband2 + 6 70c-warm-batch2); chain head 1148 → 1154; reconciliation prediction confirmed

Long-term lane session (2026-11-15 JST). The unified-fold reconciliation
(`class2-lane-unified-fold-reconciliation-20261115.json`, commits f1427d99
corrected by a69fb813) audited the three divergent receipt groups extending
the 1,109 after-warm-multiband baseline — the 13 cost-68d/hygiene receipts
(solved 1,117), the 31 warm multiband 2 receipts (solved 1,140) and the
6 cost-70c warm batch-2 WIN7 receipts (certified under
`class2-lane-cost70c-certificates/`, bits 105/92/40/24/11/8 at child
`00000000000000803242000000000000`) — and predicted a unified solved count of
**1,154 = 1,148 + 6**, the merged head 1,148 (commit 19bb2abc) already folding
44 of the 50 receipts. This session executed the authoritative unified fold
specified by that reconciliation; no sweep claims are made here beyond the
published records — receipts only.

## Unified merge recompute

`recompute_frontier_unified_merge_20261115.py` (commit 7aaa7d83):

1. reproduces the 1,109 baseline and the 1,117 endpoint byte-identically by
   runpy of `recompute_frontier_cost68d_20261115.py` (asserted
   1,109/6,738/531,295/5,008/395,018 and 1,117/6,730/530,739/5,000/394,462);
2. reproduces the 1,140 endpoint byte-identically by runpy of
   `recompute_frontier_warm_multiband2_20261115.py` (asserted
   1,140/6,707/528,979/4,977/392,702), with the 1,109 baseline set asserted
   equal to that lane's chain-head set;
3. asserts the 6 cost-70c warm batch-2 receipts against the reconciliation
   (root == child | 1<<bit for the child `00000000000000803242000000000000`,
   rows, md5, per-receipt marginal hex, greedy order 105/92/40/24/11/8);
4. asserts the three-way root disjointness of the 50 receipts (12 distinct
   roots in the 13-receipt group because cost-71b bit-1 == cost-61d bit-22
   share one canonical root; 31 multiband2 roots; 6 cost-70c roots; pairwise
   intersections empty);
5. independently re-derives each group's marginal-in-manifest union versus
   the 1,109 baseline and asserts it equals the reconciliation's published
   hex lists (8 + 31 + 6, union 45, pairwise intersections empty);
6. folds the 50 receipts from the 1,109 baseline in the reconciliation's
   fold order (13 in published order, 31 in published order, 6 cost-70c in
   greedy order), re-deriving every per-record marginal from the growing
   union;
7. set-equality controls: after 13 receipts the solved set equals the 1,117
   endpoint; after 44 it equals s_1117 UNION s_1140 with the published
   merged-head numbers 1,148/6,699/528,423/4,969/392,146; after 50 it equals
   s_1117 UNION s_1140 UNION covers(6 cost-70c receipts);
8. asserts the expected unified solved-in-manifest 1,154 and produces the
   unified frontier + ranking CSV + top-candidates CSV.

Two local runs were byte-identical. All four pushed files were verified
byte-exact by git blob sha after landing.

## Unified frontier

- baseline (after warm multiband): 1,109 / 6,738 / 531,295 / 5,008 / 395,018
- merged head (after 44 receipts): 1,148 / 6,699 / 528,423 / 4,969 / 392,146
- unified merge (+6 cost-70c warm batch-2):
  **1,154 / 6,693 / 527,949 / 4,963 / 391,672** (175 remaining S5 orbits)

Receipt totals: 50 receipts, marginal 239 (13-receipt group 56 + multiband 2
154 + cost-70c 29), marginal-in-manifest 45 (8 + 31 + 6, exactly the
reconciliation's union), zero-marginal-in-manifest receipts 7 (cost-68d
bit 26 plus the six hygiene receipts, incl. the cost-61d bit-22 =
cost-71b bit-1 duplicate cross-check). Strategy rows folded: 268,572 +
236,012 + 1,200,258 + 253,196.

Open-demand histogram (open classes only): c2=0,c4=1: 527; c2=0,c4=2: 3,021;
c2=0,c4=3: 12; c2=1,c4=0: 239; c2=1,c4=1: 60; c2=1,c4=2: 9; c2=2,c4=0: 1,034;
c2=2,c4=1: 6; c2=2,c4=2: 55.

## Ranking effect / next targets

The three-way fork from the 1,109 baseline is now fully reconciled on main:
the 1,154 chain head contains exactly s_1117 UNION s_1140 UNION the six
cost-70c covers, and the reconciliation's set-union prediction is confirmed
against the fold arithmetic.

- best class-2 candidate S5 `00000000000000809102000000000000`: unchanged at
  **8 orbits / 588** (the cost-70c receipts did not touch its rows). Its
  remaining children include the two cost-69 children
  `00000000000000809102000000000008` (cost-69f, sweep complete on the
  parallel lane with 9 WIN7-D10, certificates unextracted — fold belongs to
  that lane) and `00000000000000809102000000002000` (cost 69, demand
  c1=0, c2=2, c4=2 — the next cheapest unswept child of this S5);
- audit-blocked class-2 S5 `00000000000000809082000000000000` (classes 3):
  10 orbits / 698, receipt-unclosable;
- class-4 bottleneck `00000000020000003800000080000000`: 18 orbits / 1,460
  unchanged; next class-4 `00000000000000003800002000800000` 60 / 4,216;
- cost-70c band: 9 of 13 WIN7 bits certified and folded; remaining
  uncertified WIN7 bits 3/42/86/103 (warm rebuild candidates).

## Not folded here

- the cost-69f WIN7 roots (9 bits) stay with the parallel lane pending
  certificate extraction;
- the parallel lane's bands (cost-65h/67b/68c warm candidates, the in-flight
  cost-65j sweep) stay with that lane;
- gain-0-in-manifest own-lane warm candidates without records advanced no
  manifest orbit at this head.

## Status

- 11×11 empty board, two-stone root {49,60}, S2 {59,60}, class 2, class 4:
  **UNKNOWN**. Solved counts measure manifest coverage, not the
  game-theoretic value of any position. REFUTED-D10 sweeps prove only the
  absence of a WIN7-D10 in that subtree; WIN7 certificates prove a win
  within depth 10 from the individual 7-stone roots only. This recompute is
  bookkeeping over published receipts and proves no new game outcome.
