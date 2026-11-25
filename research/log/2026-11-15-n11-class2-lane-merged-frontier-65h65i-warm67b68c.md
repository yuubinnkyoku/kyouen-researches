# n11 class2-lane: merged frontier of the two parallel branches (warm rebuilds + 67b/68c sweeps); solved 991 → 1012 with zero cross-branch overlap; second class-2 target down to 7 orbits / 513

Long-term lane session 13 (2026-11-15 JST). The two class2-lane branches that
forked at the after-cost-65h+65i frontier (solved 991 / unique remaining 6,856 /
sum 540,177 / open 5,126/403,900) are merged into a single chain:

- chain A (this lane, warm certificate rebuilds): cost-63e-warm (bits
  42/73/100/116/120) then cost-65g-warm (bits 0/15/44/52/75/105), published
  after-cost-65g-warm frontier solved 1005 / 6,842 / 539,174 / 5,112/402,897.
- chain B (parallel long-term lane execution, child sweeps): cost-67b
  (7 WIN7-D10, receipts bits 17/117/109) then cost-68c (5 WIN7-D10, receipts
  bits 21/11/118), published after-cost-68c frontier solved 998 / 6,849 /
  539,673 / 5,119/403,396.

## Merged recompute

`recompute_frontier_merged_after65h65i_warm_67b68c_20261115.py` reproduces both
branch endpoints byte-exactly by runpy (all staged controls of every script in
both chains re-asserted from the fork), reproduces the fork state directly
(`recompute_frontier_cost65h_65i_20261114.py`) and asserts it is a subset of
both endpoints, then re-adds all four receipt groups in one canonical
sequential order from the fork (63e-warm → 65g-warm → 67b → 68c), re-deriving
every per-bit marginal from the growing merged union.

- **Merged frontier: solved 1012 / unique remaining 6,835 / sum 538,670 /
  open 5,105/402,393.**
- **Branch additions are perfectly disjoint: |A|=58, |B|=30, overlap 0
  orbits (0 in manifest)** — 991 + 14 + 7 = 1012 with no double counting.
  The published per-bit marginals of all four groups reproduce exactly
  (chain-A groups against the fork-sequential state, chain-B groups compared
  with their published chain-B values; `marginal_reduced_vs_published` is
  false everywhere).
- Control: chain B is independently re-reproduced from the fork plus its own
  67b/68c covers (998 exact), and the merged replay set equals union(A, B).
- Two runs byte-identical (md5 over the recompute JSON and both CSVs).

## Ranking effect

The second class-2 target S5 `00000000000000803202000000000000` drops to
**7 remaining S6 orbits / 513 edge cost** — the smallest and best coverable
class-2 target (the 10-orbit S5 `00000000000000809082000000000000` remains
receipt-unclosable per the uncoverability audit). The warm receipts closed
both cost-69 children (`00000000000000803202000000008000` via 65g-warm bit-15,
`00000000000000803222000000000000` via 65g-warm bit-75), one cost-70 child
(`00000000000000803202100000000000` via 65g-warm bit-44), the cost-71 child
`00000000000000803202000000000040` (63e-warm bit-116) and the cost-72 child
`00000000000000803202000000000001` (65g-warm bit-0). Remaining children:
cost-70 `00000000000000803242000000000000`, cost-71
`00000000000000803202000000400000`, cost-72
`00000000000000803202000000000200`, and four cost-75 children — all demand
c1=0,c2=2,c4=0. Best class-4 unchanged (18 orbits / 1,460).

## Parallel-lane note (cost-69e)

The parallel lane's in-flight cost-69e sweep (raw batches 1-9 pushed, child
`00000000000000803202000000008000`, 11 WIN7-D10 + 58 REFUTED, 0 capped,
80,172,332 v16 nodes) targets a child that is **already solved in the merged
frontier** (65g-warm bit-15 receipt, the cost-61e-lesson pattern in reverse:
the claim was correct in the after-cost-68c chain-B state where the child was
still remaining). Its WIN7 certificates remain valid new evidence for the
individual 7-stone roots; when its records are published, the next frontier
recompute must re-derive their marginals against this merged state (expected
in-manifest marginal 0 for the child orbit itself; the other 6 covers of each
root may still contribute elsewhere). The sibling cost-69 child
`00000000000000803222000000000000` is likewise already covered (65g-warm
bit-75) and should not be swept for frontier purposes.

## Status

- 11×11 empty board, two-stone root {49,60}, S2 {59,60}, class 2, class 4:
  **UNKNOWN**. WIN7 certificates prove a win within depth 10 from the
  individual 7-stone roots only; REFUTED-D10 sweeps prove only the absence of
  such a win in that subtree; this merged recompute is bookkeeping over
  published receipts and proves no new game outcome.
