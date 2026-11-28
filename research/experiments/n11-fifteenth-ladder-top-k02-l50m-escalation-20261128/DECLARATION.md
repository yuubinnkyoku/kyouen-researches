# Declaration: n11 fifteenth ladder-top k02 L50M escalation (single-owner, publish-then-execute)

Single-owner declaration by the long-term 11x11 lane. Published BEFORE
any run of this Part. Any parallel lane must not run k02 above its
published 15M budget until this Part's completion log appears.

## Scope

L50M (budget 50,000,000 nodes) escalation of the single remaining
cost-unknown child of the rank-1 closure-ladder class 5804:
k02 `6052837899185946628:128` (s5_index 212115, legal 87), which is
UNKNOWN(0) with nodes 15,000,000 (budget exhausted) in the published
k02/k03 re-escalation kit (`09358acd`, declaration `88a24418`).
Current head of record basis: `3a527d39...` (6,899 rows WIN 217 /
LOSS 6,682, fifteenth k03 head, adoption `bc535153`, reaudit `e6ceb133`
+ `d7a91957`). Declaration HEAD pin: main at push time.

## Pre-registered expectations

- Runner: jsreplay.js pin `84585617...` (published s4bd regen kit),
  `--n=11 --memo=22 --only=5` cold solver per row, no shared TT;
  input `k02.input.csv` byte-identical to the published re-escalation
  kit's `fda5d01d...` copy (probe row `target,0,5,6052837899185946628,
  128,87,0,0,0,0,0`).
- Calibration BEFORE the 50M runs: u01 `1153485622925590528:0` at 2M
  budget must reproduce the published calibration values (result 0,
  nodes 2,000,000, fq 95,670) on this host.
- Two sequential cold 50M runs (fresh process each). Outcomes are
  measured, not predicted: any of WIN(1)/LOSS(2)/UNKNOWN(0,
  budget exhausted) is an acceptable result. A node-identical
  (or byte-identical) pair is required for determinism; a mismatch
  fails this Part.
- If k02 resolves WIN(1) or LOSS(2), it stays single-implementation:
  adoption requires the 3-pillar scrutiny chain (C++ gate +
  third_impl corroboration) under a fresh declaration. If UNKNOWN
  at 50M, k02 stays UNKNOWN; parking/L100M only under a future
  declaration.
- No verdict is consumed by this Part regardless of outcome: the
  standard 11x11 empty board and all 19 central-reply roots stay
  UNKNOWN.

## Method

1. Publish this declaration (this commit).
2. Calibration u01@2M, compared to the published raw values.
3. k02 50M cold run 1, then cold run 2 (fresh processes, no shared
   TT), raws recorded per run.
4. Kit + completion log published with raws, batch summary
   (schema `n11-fifteenth-ladder-top-k02-l50m-summary-v1`), and the
   pair determinism verdict.

## Non-meaning

Nodes are bookkeeping, never verdicts. Class 5804 is NOT complete
while k02 is UNKNOWN; even a WIN would first need the 3-pillar
chain and canonical adoption before any class-status claim. The
standard 11x11 empty board, all 19 central-reply roots, the
two-stone root {60,27}, the third-move pair {100,108} and every
closure class stay UNKNOWN.

## Disclosures

- This lane runs without access to the user's computer (scheduled
  task); publication is via the GitHub API only.
- 50M cold runs are long single-process jobs; wall times vary by
  host load; nodes/result are the deterministic quantities.
