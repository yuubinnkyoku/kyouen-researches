# 2026-11-28 eight-row q9 8x29 row-split — completion log

Declaration: `research/log/2026-11-28-eight-row-q9-m29-row-split-declaration.md`
(commit `ec68f8f4`, declaration-time HEAD `ed37b8ab`). Kit:
`research/experiments/eight-row-q9-m29-row-split-20261128/`. CSV (8,9) row note
updated (`results/fixed-width/mwq_stabilization.csv`).

## What was measured (all publish-then-execute, after the declaration)

- Calibration (pre-registered): 8x28 rowY=3 cold rerun SAT **3,049,989
  conflicts, bit-exact with the published record**; witness stones
  **bit-identical** to the published m=28 witness; jsVerify + pyVerify PASS.
- **8x29 rowY=2: UNSAT 5,079,168 conflicts (decided 205.0 s)** — first width
  beyond the published 8x28 frontier ever evaluated, and the first decided
  absence piece there: single-deficiency row classes {2}/{5} are witness-free
  at 8x29. Cold pair bit-exact across a full execution-environment reset.
- 8x29 rowY=3/0/1: INDET at 280 s caps (honest negatives; pre- and post-reset
  same-trajectory conflict counts disclosed in the kit records).
- 8x29 rowY=3 lex=H cross-encoding: INDET 4,972,540 @ 280 s.
- 8x29 class {3} krow=3:7 minpos 0/1 (sat3.js class-split probes): INDET
  5,424,393 / 5,228,774 @ 280 s. Positive control 8x28 class {3} krow=3:7
  minpos=1 SAT 3,013,059 — decoded a **second 63-stone witness at 8x28,
  D4-non-congruent to the published one** (bonus observation: the 8x28
  witness is not unique up to symmetry).

## Bottom line

M_{8,9} stays in [29,984]; the frontier stays 8x29. Absence at 8x29 is decided
only for the single-deficiency row classes {2}/{5}; classes {0}/{1}/{3} are
INDET-undetermined at these caps and multi-deficiency classes are unswept —
no overall absence claim.

## Disclosures

- One mid-lane execution-environment reset (Koyeb artifact-save failure, the
  known file-loss mode) lost the first-pass raw logs; all published raw logs
  are post-reset reruns. Verdicts are deterministic: the SAT calibration and
  the UNSAT rowY=2 piece reproduced bit-exactly (conflicts identical across
  the reset); INDET wall-clock-cut conflict counts are host-dependent and both
  observations are disclosed per piece.
- 11x11 empty board, two-stone roots, third move, S2, closure classes:
  UNKNOWN at all times; verdicts not consumed; conflicts are bookkeeping.

## Resume notes (next execution)

- Re-fetch latest main before starting (hourly parallel runs).
- 8x29 open pieces: rowY=3/0/1 and class {3} krow/minpos p=2..13, classes
  {0}/{1} krow splits, krow=3:6 (deeper deficiency), multi-deficiency classes
  — all unswept; heavier caps or a different decomposition are needed (the
  280 s caps show near-uniform 4.7-5.6M resistance).
- Toolchain pins and runners are in the kit `scripts/` (sha-pinned in the
  declaration and MANIFEST).
