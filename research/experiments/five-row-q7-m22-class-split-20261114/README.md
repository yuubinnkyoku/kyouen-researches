# five-row q=7 m=22 class-split — takeover + completion IN FLIGHT claim

Date: 2026-11-15 (UTC). Fast lane takeover of the stalled batch-1 lane.

## Situation

Batch 1 (2026-11-14T15:25:57Z, commit 1029a0db) pushed 19 raw logs and stopped:

- 17/19 direct classes **UNSAT** (hardest {0,1}: 875,682 conflicts; {0,2,3} log complete:
  199,205 conflicts / 5.9 s);
- {0} and {1} plain instances **INDET** (SIGTERM at ~142 s process time each);
- no report, records, summary, or IN FLIGHT claim followed; the lane has been silent
  for 8+ hours.

## Claimed (in flight)

Completion of the 5x22 q=7 class-split by the K0816/K0821 protocol:

1. **Bit-exact re-run** of all 17 direct UNSAT classes with sat3.js byte-identical to
   five-row-q7-m21-class-split-20261114/scripts/sat3.js and the official kissat 4.0.4
   linux-amd64 binary; conflicts must match the batch-1 logs exactly.
2. **{0} and {1} by the complete k x minpos decomposition** (the K0816/K0821 protocol):
   k = 0..4 (krow-only, 5 instances each) + k = 5 x minpos = 0..10 (11 instances each;
   coverage: min(x1, 21-x5) <= 10 for every configuration, else x1 >= 11 and x5 <= 10
   contradict x1 <= x5; the column mirror preserves row occupancy, hence the class).
   Escalation for INDET sub-instances: --lex=H cross-encoding (class-preserving).
3. **Positive control**: 5x18 q=7 class {0} must be SAT and decode to a 29-stone
   row-deficient maximal witness passing census-free verifyConfig (K0816/K0821 control).
4. **Cross-encoding**: {0,1} and {2} re-checked UNSAT under --lex=H.

Any outcome is in scope: all-UNSAT gives witness-free width 22 (witness-free width set
of (5,7) extends to {19,20,21,22}); any SAT class decodes to a deficient maximal witness
(M_{5,7} >= 23).

## Not claimed

- 5x23+, other (w,q), the six-row frontier (see
  ../six-row-q7-m22-class-split-20261115/README.md), 11x11 lanes.

## Status

IN FLIGHT — computation starting; results to be pushed to this directory.
