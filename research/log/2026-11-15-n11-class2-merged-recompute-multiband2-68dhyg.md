# n11 class2-lane: merged frontier recompute after warm-multiband2 + cost-68d/hygiene (13 receipts); chain head 1140 → 1148; third class-2 target S5 down to 8 orbits / 588

Long-term lane session (2026-11-15 JST). The 1109 after-warm-multiband chain
head had two divergent published folds:

- this lane's cost-68d fold (`class-frontier-cost68d-recompute-20261115.json`,
  solved 1,117): the 7 cost-68d WIN7 receipts plus the 6 warm-band hygiene
  receipts;
- the concurrent lane's warm multiband 2 fold
  (`class-frontier-warm-multiband2-recompute-20261115.json`, solved 1,140):
  31 warm receipts.

The two receipt sets are pairwise disjoint — verified by the published
duplicate crosscheck (`class2-lane-warm-multiband2-duplicate-crosscheck-20261115.json`:
31 batch-2 roots vs the 13 cost-68d/hygiene roots, 54 entries checked,
byte-exact duplicates only, zero WIN/LOSS conflicts) — and the batch-2
selection explicitly deferred this lane's hygiene bits (cost-62a 1/89,
cost-63a 11/109, cost-61d bit-22 = cost-71b bit-1) and never touched the
cost-68d band. This session merged the fork; no sweep claims are made here
beyond the published cost-68d sweep record.

## Merged recompute

`recompute_frontier_merged_after_multiband2_68dhyg_20261115.py` (commit
19bb2abc):

1. reproduces the published 1,140 chain head by runpy (asserted
   1,140 / 6,707 / 528,979 / 4,977 / 392,702, byte-identical output);
2. asserts the receipt-set disjointness against the published crosscheck
   (31 batch-2 roots vs the 13 cost-68d/hygiene roots, intersection empty);
3. re-derives the cost-68d child membership with string keys at the 1,140
   state — the child `00000000000000809122000000000000` is genuinely still
   remaining there (the 31 batch-2 receipts never covered it; demand
   c1=0, c2=2, c4=0);
4. re-sums the completed cost-68d sweep from the 9 published raw batches
   (68 candidates: 7 WIN7-D10 + 61 REFUTED, 0 capped, 61,325,518 v16 nodes)
   with the determinism rerun node-exact (8 bits) and the v15 cross-engine
   anchors asserted;
5. asserts all 7 cost-68d records and all 6 hygiene records (rows,
   sub-roots, union 0/0, md5, sha256, root == child | 1<<bit);
6. folds the 13 receipts in published record order, re-deriving every
   per-record marginal from the growing union that already contains the
   31 batch-2 receipts; the cost-61d bit-22 root duplicates the cost-71b
   bit-1 root (byte-identical independent re-extraction; zero marginal on
   the duplicate is a positive cross-check, not double coverage);
7. produces the merged frontier + ranking CSV + top-candidates CSV.

Two local runs were byte-identical. All four pushed files were verified
byte-exact by git blob sha after landing.

## Merged frontier

- baseline (after warm multiband 2): 1,140 / 6,707 / 528,979 / 4,977 / 392,702
- merged (+13 receipts, +8 solved, all from cost-68d):
  **1,148 / 6,699 / 528,423 / 4,969 / 392,146**

Receipt totals: 13 receipts, marginal 56, marginal-in-manifest 8,
zero-marginal receipts 7 (cost-68d bit 26 plus the six hygiene receipts).
Open-demand histogram (open classes only): c2=0,c4=1: 527; c2=0,c4=2: 3,021;
c2=0,c4=3: 12; c2=1,c4=0: 239; c2=1,c4=1: 60; c2=1,c4=2: 9; c2=2,c4=0: 1,040;
c2=2,c4=1: 6; c2=2,c4=2: 55.

## Ranking effect / next targets

The third class-2 target S5 `00000000000000809102000000000000` drops from
12 orbits / 871 edge cost to **8 orbits / 588**. Its remaining cheapest
unswept children:

- `00000000000000809102000000000008` (cost 69) — swept concurrently by the
  parallel lane as cost-69f; the sweep is complete per its published audit
  (9 WIN7-D10 / 60 REFUTED-D10 / 0 capped, 112,752,229 nodes), but the WIN
  roots are unextracted, so nothing from it is folded here;
- `00000000000000809102000000002000` (cost 69, demand c1=0, c2=2, c4=2).

Bottlenecks unchanged: the audit-blocked class-2 S5
`00000000000000809082000000000000` (10 / 698, receipt-unclosable) and
class-4 `00000000020000003800000080000000` (18 / 1,460).

## Not folded here

- the parallel lane's bands (cost-65h/67b/68c warm candidates, the in-flight
  cost-65j sweep) stay with that lane;
- the six gain-1 cost-70c warm candidates belong to the parallel lane's
  band; they may now have non-zero marginal against this merged head, and
  their fold belongs to that lane or a later canonical recompute;
- gain-0-in-manifest own-lane warm candidates without records advanced no
  manifest orbit at this head.

## Status

- 11×11 empty board, two-stone root {49,60}, S2 {59,60}, class 2, class 4:
  **UNKNOWN**. Solved counts measure manifest coverage, not the
  game-theoretic value of any position. REFUTED-D10 sweeps prove only the
  absence of a WIN7-D10 in that subtree; WIN7 certificates prove a win
  within depth 10 from the individual 7-stone roots only. This recompute is
  bookkeeping over published receipts and proves no new game outcome.
