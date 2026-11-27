# n11 ultra-cheap batch stage-1 sweep: completion log (2026-11-27)

Execution Part of the single-owner declaration
`research/log/2026-11-27-n11-ultra-cheap-batch-declaration.md`
(commit `3781d82f`).  Kit:
`research/experiments/n11-ultra-cheap-batch-stage1-2m-20261127`.

## What ran (exactly the declared protocol, nothing else)

- Stage-1: u01..u04 at 2,000,000 budget, two cold passes each, on the
  pinned Node.js replica jsreplay.js (`84585617...`, byte-clone of the
  published tenth/eleventh selection kit copy, sha256 re-verified
  locally before execution; not republished in the kit).
- 15M escalation in declared order with the WIN-stopping rule active.

## Results

- Stage-1: 4/4 UNKNOWN at 2M, all cold pairs node-identical
  (u02/u03 pairs fully byte-identical; u01/u04 pairs differ only in
  wall_s).
- Escalation: **u01 `1153485622925590528:0` (class 1849, legal 88,
  s5_index 81011) resolves WIN(1) at nodes 4,893,014**, cold pair
  node-identical.  WIN-stop fired: u02/u03/u04 stay UNKNOWN at 2M
  (escalation-suppressed; no L50M parking without a future declaration).
- No overreach: no suppressed key at any higher budget.

## Honest disclosures

- The wave-A declaration push raced a parallel session commit
  (6bf68e4b -> f4e65734); the identical payload was re-pushed against
  the fresh head (final declaration commit 3781d82f).
- Pre-declaration mechanical calibration: one 50k-budget INDET cold run
  of u01 (disclosed in the declaration; result 0, no verdict
  information, legal count 88 fail-closed match).
- Wall_s fields differ across passes; timing is not evidence.
- The batch-summary.json json was machine-generated from the raws.

## What this does NOT mean

Single-implementation bookkeeping only.  The u01 WIN row is NOT
consumed: no cache increment, no class-status change, no coverage
claim.  Before any adoption it needs the C++ second-implementation
scrutiny gate, a third-implementation corroboration, and the standing
WIN-side flip-census review; class 1849 completion would be
Board-verified free_now at adoption time only.  Nodes are never
evidence.  The standard 11x11 empty board: UNKNOWN.  All 19
central-reply roots: UNKNOWN.  The two-stone root {60,27} and its
remaining third moves 100/108: UNKNOWN.  All closure classes: UNKNOWN.

Next Part (this lane): u01 WIN-row pillars (C++ gate
`9193f5b6` @`154f3b7a` lineage via zig 0.13.0, expected quadruple
88,15000000,1,4893014; third_impl `08ea958f` cap 400M, 2 cold passes),
under separate declarations if not already claimed by another lane.
