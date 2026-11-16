# 2026-11-16 n11 class2-lane: second-candidate S5 depth-10 unclosable (cost-71 row STERILE, second-implementation verification)

## What

Second-implementation verification (independent parser, independent D4
canonicalization, no engine run) of a structural fact implicit in the
published head-1452 presweep census but with an unstated theorem-level
consequence:

The cost-71 row `00000000000000801202000040000400` of the second coverable
class-2 candidate S5 `00000000000000801202000040000000` has ALL 71 legal
candidate 7-stone roots already verdict-resolved REFUTED-D10 by
D4-canonical transfer from published sweeps (71/71 `harvested_refuted`,
0 open, 0 receipt_win at head 1452 AND at the projected head 1472).
The row is STERILE in the K0863 sense without a single engine run of its
own.

By K0863 (STERILE-row unclosability, commit 4122ea73), no WIN7-D10 receipt
can ever cover this row (own-row or cross-cover, present or future).
Therefore the second coverable class-2 candidate S5
`00000000000000801202000040000000` (3 rows / 211 edge cost at head 1452:
the cost-71 row, the cost-64 row `00000000000000801282000040000000` and
the cost-76c row `00000000010000809002000001000000`) can never be fully
closed within the depth-10 receipt system. It should be reclassified from
coverable class-2 to the depth>10-evidence-waiting category, exactly like
the best coverable class-2 S5 `00000000000000801202000000200000`
(K0863/K0865). Census target ranking loses one coverable class-2
candidate; the coverable class-2 population shrinks by one orbit.

Out-of-sample K0863 test: the 23 published cost-64h receipts (projected
head 1472) cover none of the row's 71 candidate canons - a passing
prediction of the theorem on a row never swept as a lane.

## How (verification protocol)

- Head-1452 basis reproduced exactly as the published cost-64h fold
  pre-registration does: blob-pinned `fold_projection_head1450_tool`
  (basis 771 roots at head 1450) + the four published cost-76d/77e
  receipt roots = 775 roots / 760 distinct D4 canons; published head-1452
  six-number summary (1452/174/6396/506144/4669/370058) and demand
  histogram re-asserted.
- Independent harvest parser (different code path from the census glob):
  recursive bit-list collection with per-class identity assertion and a
  dedicated audit-schema path (per-transfer D4 canon cross-check), plus
  raw-batch JSONL parsing for cost-76d/77e/64h (pilot control 3402,
  per-bit conflict assertion at every canon insertion). The phase-A map
  over the exact published census input set reproduces the published
  census totals exactly: 3548 distinct verdict canons / 353 WIN7-D10 /
  3195 REFUTED-D10 / 0 conflicts. Phase B (cost-64h raw sweep,
  postdates the census): 64 new canons (23 WIN / 41 REFUTED), node_sum
  47,017,565 matches the published claim v2, 0 conflicts with phase A
  (cross-agreement).
- Independent D4 canonicalization asserted equal to the published tool
  canon on all 121 single-stone masks and all 760 folded canons.
- Legal candidate enumeration via `legal_candidates.py` (exact Bareiss
  4x4); child safety over all 15 stone quadruples asserted.
- Deterministic: two consecutive runs byte-identical
  (sha256 953a9d4a913ab80ac33646af0c094d93d26482ce733939dfc607c80240eb5166).

## Takeover prep recorded in the same artifact

- cost-76c row `00000000010000809002000001000000` (stale claim
  2026-11-15T20:54Z, zero raw batches published): 76 candidates =
  5 harvested_refuted (census transfers 0/56/59/102/117) + 71 open at
  head 1452 and at projected head 1472. Its S5-parent closure motivation
  is void per the K0863 consequence above; remaining value is the row
  itself for its second parent `00000000000000801202000100000000`
  (69 rows / 5758 at head 1452) and the harvest verdicts.
- cost-69a row `00000000000000801222000000800000` (stale claim
  2026-11-16T01:31Z, zero raw batches): 69 candidates = 8
  harvested_refuted + 61 open. The published claim v1 listed only 3
  transferred bits (55/65/109); the rebuilt harvest finds 5 additional
  transfers from newer sweeps. Parents at head 1452:
  `00000000000000801222000000000000` (70 rows / 5345) and
  `00000000000000003800000008002000` (25 rows / 1748).

## Files

- `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/verify_secondcandidate_cost71_sterile_20261116.py`
- `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-secondcandidate-cost71-row-sterile-verification-20261116.json`

## Interpretation guard

This is bookkeeping over published verdicts only; no engine search was
run and no new verdict was created. REFUTED-D10 is a depth-10 refutation
of the individual 7-stone root, NOT a LOSS proof of any position. STERILE
means unclosable within the depth-10 WIN7-D10 receipt system, NOT a LOSS
proof of the row, the parent S5, any S2 root or the board. Solved counts
are manifest bookkeeping. The 11x11 empty board, the two-stone roots
{49,60} and {59,60}, S2 {59,60}, and classes 1/2/4 all remain UNKNOWN.
