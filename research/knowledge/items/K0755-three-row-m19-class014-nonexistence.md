---
id: K0755
title: 5x19 three-row deficient class {0,1,4} nonexistence
kind: proposition
status: computed
topics: [rectangles, maximal-safe]
aliases: []
relations:
- type: depends_on
  target: K0727
- type: depends_on
  target: K0728
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
artifacts:
- path: research/experiments/five-row-q7-m19-20261110/scripts/multi_deficient_runner.ts
  role: solver
  note: 完全列挙ランナー（旧front matterから移行）
scope: '旧front matterの evidence を移行: complete-enumeration'
evidence: 'complete-enumeration（verification: deterministic-machine）。本文の完全列挙・監査記述を参照。'
---

# 5x19 three-row deficient class {0,1,4} nonexistence

## Claim

In the 5x19 integer grid, consider configurations where rows 0, 1, 4
each hold at most 5 stones and the non-deficient rows 2, 3 each hold
exactly 6 stones. For every one of the 8,378 mirror representatives of
the deficient-row-0 occupancy pattern, no maximal safe configuration
exists: any maximal configuration in this class contains a forbidden
quadruple (co-circle of size 7 in the integer census).

## Method

Complete finite enumeration by multi_deficient_runner.ts with
DEF_ROWS=[0,1,4] (the two non-deficient rows 2, 3 are
center-adjacent): exact integer circle census (95 circles of
size >= 7), blocker obligation DFS with forced-stone/forced-empty
propagation, row-capacity constraints, complete fill enumeration of
the non-deficient rows. 10 consecutive 600k-node slices covering all
idx 0..8377 (log appendices 18-19), final slice completing with no
cap.

## Result

- witnesses: 0, leaves: 0 across all 8,378 representatives.
- perK: k=5: 5,832, k=4: 1,956, k=3: 489, k=2: 90, k=1: 10, k=0: 1
  (total 8,378), with the k-block boundaries identical to
  K0738/K0741/K0747/K0749/K0750/K0751/K0752/K0753, re-confirming that
  the per-k representative counts depend only on M=19.
- Node cost is the lightest of the three determined three-row classes
  (k=5 block max 15,799 nodes/case vs 43,641 for {0,1,2} and 24,147
  for {0,1,3}), consistent with the two center-adjacent
  non-deficient rows 2, 3 creating the strongest fill/blocker
  interference.

## Scope

Finite complete-enumeration result for the class {0,1,4} only. Third of
the six three-row-deficient mirror representatives of 5x19 determined.
Remaining undetermined occupancy classes in 5x19: the three
three-row-deficient mirror representatives
({0,2,3}, {0,2,4}, {1,2,3}).
