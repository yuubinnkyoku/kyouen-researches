---
id: K0751
title: 5x19 four-row deficient class {0,1,3,4} nonexistence
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
artifacts:
- path: research/experiments/five-row-q7-m19-20261110/scripts/multi_deficient_runner.ts
  role: solver
  note: 完全列挙ランナー（旧front matterから移行）
scope: '旧front matterの evidence を移行: complete-enumeration'
evidence: 'complete-enumeration（verification: deterministic-machine）。本文の完全列挙・監査記述を参照。'
---

# 5×19 four-row deficient class {0,1,3,4} nonexistence

## Claim

In the 5×19 integer grid (rows 0..4, columns 0..18), consider
configurations where rows 0, 1, 3, 4 each hold at most 5 stones and the
non-deficient center row 2 holds exactly 6 stones. Under the mirror
symmetry x -> 18 - x, there are 8,378 canonical representatives of the
deficient-row-0 occupancy pattern. For every representative, no maximal
safe configuration exists: any maximal configuration in this class
contains a forbidden quadruple.

## Method

Complete finite enumeration by the deterministic deficient-row
occupancy machine (multi_deficient_runner.ts, DEF_ROWS=[0,1,3,4]):
exact integer circle census (95 circles of size >= 7), blocker
obligation DFS with forced-stone/forced-empty propagation, row-capacity
constraints, and complete fill enumeration of the non-deficient row.
300,000-node global budget per slice, 14 consecutive slices covering
all idx 0..8377 with no cap at completion.

## Result

- witnesses: 0, leaves: 0 across all 8,378 representatives.
- perK: k=5: 5,832, k=4: 1,956, k=3: 489, k=2: 90, k=1: 10, k=0: 1
  (total 8,378). The k-block boundaries (5831/5832, 7787/7788,
  8276/8277, 8366/8367, 8377/8378) match K0738/K0741/K0747/K0749/K0750
  exactly, cross-validating that the per-k representative counts depend
  only on M=19 and not on the deficient row set.

## Scope

This is a finite complete-enumeration result for the class
{0,1,3,4} only, not a universal theorem over all widths. Together with
K0750 ({0,1,2,4}), both four-row-deficient mirror representatives of
5×19 are now fully determined: no maximal safe configuration exists in
either. Remaining undetermined occupancy classes in 5×19: the six
three-row-deficient mirror representatives
({0,1,2}, {0,1,3}, {0,1,4}, {0,2,3}, {0,2,4}, {1,2,3}).
