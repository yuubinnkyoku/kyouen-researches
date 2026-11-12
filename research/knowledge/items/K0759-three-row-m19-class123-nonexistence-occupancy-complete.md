---
id: K0759
title: 5x19 three-row deficient class {1,2,3} nonexistence and completion of row-occupancy classification
kind: proposition
status: computed
topics: [rectangles, maximal-safe]
aliases: []
relations:
- type: depends_on
  target: K0745
- type: depends_on
  target: K0747
- type: depends_on
  target: K0749
- type: depends_on
  target: K0750
- type: depends_on
  target: K0751
- type: depends_on
  target: K0752
- type: depends_on
  target: K0753
- type: depends_on
  target: K0755
- type: depends_on
  target: K0756
- type: depends_on
  target: K0758
artifacts:
- path: research/experiments/five-row-q7-m19-20261110/scripts/multi_deficient_runner.ts
  role: solver
  note: 完全列挙ランナー（旧front matterから移行）
scope: ''旧front matterの evidence を移行: complete-enumeration''
evidence: complete-enumeration（verification: deterministic-machine）。本文の完全列挙・監査記述を参照。
---

# 5x19 three-row deficient class {1,2,3} nonexistence and completion of row-occupancy classification

## Claim

1. In the 5x19 integer grid, consider configurations where rows 1, 2, 3
   each hold at most 5 stones and rows 0, 4 each hold exactly 6 stones
   (row-mirror-invariant class, occupancy pattern (6,5,5,5,6)). For every
   one of the 8,378 mirror representatives, no maximal safe
   configuration exists: any maximal configuration in this class
   contains a forbidden quadruple (co-circle of size 7).
2. Corollary (with K0745 and all row-deficient classes K0738-K0758):
   every maximal safe configuration on the 5x19 grid has row occupancy
   exactly (6,6,6,6,6), i.e. exactly 30 stones. Row-deficient maximal
   safe configurations do not exist on 5x19.

## Method

Complete finite enumeration by multi_deficient_runner.ts with
DEF_ROWS=[1,2,3]: exact integer circle census (95 circles of size >= 7),
blocker obligation DFS with forced-stone/forced-empty propagation,
row-capacity constraints, complete fill enumeration of the
non-deficient rows 0, 4. 26 consecutive 600k-node slices covering all
idx 0..8377 (log appendix 26); two slices discarded and re-run after
process safety deadline failures; final slice completed with no cap.

## Result

- witnesses: 0, leaves: 0 across all 8,378 representatives.
- perK: k=5: 5,832, k=4: 1,956, k=3: 489, k=2: 90, k=1: 10, k=0: 1
  (total 8,378), k-block boundaries identical to all preceding classes
  (independent of DEF_ROWS).
- Node cost second-lightest of the six three-row classes (k=5 block max
  17,108 nodes/case; cf. {0,1,2} 43,641, {0,2,3} 27,106, {0,1,3} 24,147,
  {0,2,4} 17,781, {0,1,4} 15,799): the three consecutive deficient rows
  1-3 cluster at the center, concentrating blocker demand.

## Scope

Finite complete-enumeration results. Item 1 closes the last undetermined
occupancy class of the 5x19 row-deficient family (all 1- through 5-row
deficient classes enumerated: K0738-K0759). Item 2 is the conjunction of
those enumerations with the full-capacity witness existence (K0745); it
is machine-verified up to the correctness of the shared runner, and is
not a number-theoretic proof of the M_{5,7}=19 conjecture. Structure of
the full-capacity class itself (beyond the K0745 witness), other widths,
and the 11x11 empty board / two-stone root {49,60} remain open.
