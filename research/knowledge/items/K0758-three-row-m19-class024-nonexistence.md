---
id: K0758
title: 5x19 three-row deficient class {0,2,4} nonexistence
status: established
established: 2026-11-12
evidence: complete-enumeration
verification: deterministic-machine
machine: research/experiments/five-row-q7-m19-20261110/scripts/multi_deficient_runner.ts
depends: [K0727, K0728, K0747, K0749, K0750, K0751, K0752, K0753, K0755, K0756]
---

# 5x19 three-row deficient class {0,2,4} nonexistence

## Claim

In the 5x19 integer grid, consider configurations where rows 0, 2, 4
each hold at most 5 stones and the non-deficient rows 1, 3 each hold
exactly 6 stones. For every one of the 8,378 mirror representatives of
the deficient-row-0 occupancy pattern, no maximal safe configuration
exists: any maximal configuration in this class contains a forbidden
quadruple (co-circle of size 7 in the integer census).

## Method

Complete finite enumeration by multi_deficient_runner.ts with
DEF_ROWS=[0,2,4] (the two non-deficient rows 1, 3 are the
upper-middle and lower-middle rows): exact integer circle census
(95 circles of size >= 7), blocker obligation DFS with
forced-stone/forced-empty propagation, row-capacity constraints,
complete fill enumeration of the non-deficient rows. 18 consecutive
600k-node slices covering all idx 0..8377 (log appendices 24-25),
final slice completing with no cap.

## Result

- witnesses: 0, leaves: 0 across all 8,378 representatives.
- perK: k=5: 5,832, k=4: 1,956, k=3: 489, k=2: 90, k=1: 10, k=0: 1
  (total 8,378), with the k-block boundaries identical to
  K0738/K0741/K0747/K0749/K0750/K0751/K0752/K0753/K0755/K0756,
  re-confirming that the per-k representative counts depend only on
  M=19.
- Node cost is third-lightest of the five determined three-row
  classes (k=5 block max 17,781 nodes/case in the 0,3,* band vs
  43,641 for {0,1,2}, 27,106 for {0,2,3}, 24,147 for {0,1,3},
  15,799 for {0,1,4}), consistent with the two non-deficient rows
  1, 3 being near-center (moderately strong fill/blocker
  interference). k=4 block max 12,499; k<=3 blocks very light
  (final 265-case slice completes well under the cap).

## Scope

Finite complete-enumeration result for the class {0,2,4} only. Fifth of
the six three-row-deficient mirror representatives of 5x19 determined.
Remaining undetermined occupancy classes in 5x19: the single
three-row-deficient mirror representative {1,2,3} (row-mirror
invariant, the last occupancy class of the row-deficient family).
