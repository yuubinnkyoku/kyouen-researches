# 2026-11-28 n11 twenty-first ladder-top escalation declaration

Single-owner declaration (publish-then-execute) for the 15M WIN-stop
escalation of the ten parked keys k02-k11 of the twentieth ladder-top
selection (class 34269 `1152921504624672768:68719476736`, twentieth
escalation kit `44290797`, completion `6cbb5da8`), against the
canonical head of record `1f1430f3...` (twentieth k01 adoption,
6,906 rows WIN 224 / LOSS 6,682, adoption `c70ac8cf`, completion
`6292a823`; measured by the twentieth k01 adoption reaudit at
`2b96c5d9`, kit `d2d3c398`, completion `6c33d59f`).  Declaration
published at main HEAD `b05edce7` before the declared execution;
this lane is the declared owner of this Part.

## Pre-registered plan and predictions

- Keys (all verified fresh/UNCLAIMED/quarantine-free/D4-canonical/
  canonical-safe/dual-legal by the published twentieth selection
  `de1a99db`; stage-1 2M cold pairs all UNKNOWN(0) with budget
  exhaustion, pairs node-identical, published in the twentieth
  escalation kit `44290797`):
  k02 `1153484454578094080:68719476736` (s5 178184, legal 85),
  k03 `1152921504624738304:68719476736` (s5 355050, legal 85),
  k04 `1152921504624705536:68719476736` (s5 809575, legal 90),
  k05 `1152921573344149504:68719476736` (s5 900276, legal 82),
  k06 `1152921504624672768:68720525312` (s5 900687, legal 80),
  k07 `1152921504624689152:68719476736` (s5 941211, legal 83),
  k08 `1152921504624672770:68719476736` (s5 956329, legal 84),
  k09 `1152921504624676864:68719476736` (s5 957713, legal 88),
  k10 `1152921508919640064:68719476736` (s5 958080, legal 76),
  k11 `1152921504607899648:73014444032` (s5 958143, legal 76).
  Input rows: byte-identical copies of the published twentieth
  escalation kit's `k02..k11.input.csv` (shas in that kit's
  MANIFEST at `44290797`).
- Stage-1 is NOT repeated: the published stage-1 2M cold pairs of
  `44290797` remain the standing stage-1 record for k02-k11.
- Runner: jsreplay replica sha256 `84585617...` (the published
  pinned replica of the C++ standalone exact-replay path at commit
  154f3b7a), fresh cold solver per row, budget-pinned
  (`--only=5 --memo=22`).
- Calibration (after this declaration, before the 15M runs): u01
  `1153485622925590528:0` at 2M must reproduce the published
  sixteenth escalation kit's calibration raw VALUES (result 0,
  nodes 2,000,000, forbidden quadruples 95,670).
- 15M escalation in the declared order k02 -> k03 -> ... -> k11,
  cold pair each (two independent fresh runs).  **WIN-stop rule**:
  the first key that resolves WIN(1) stops the escalation (later
  keys stay parked at the published stage-1 2M UNKNOWN); a LOSS(2)
  resolution completes that key's own pair and the order continues
  to the next key; a 15M UNKNOWN parks that key (L50M only under a
  future declaration).  Prediction (not a gate): given the k01
  resolution pattern and the uniform 2M exhaustion, most keys are
  expected to need a large fraction of the 15M budget or park.
- Owner-union precheck (inherited unchanged from the twentieth
  escalation declaration `f04f1fe2`, graph-derived from the frozen
  graph `54f9c364`; owner unions are graph-invariant and unaffected
  by the head move `e1a9cacc` -> `1f1430f3`), disclosed:
  k02 [4715, 34269] / k03 [10153, 10691, 34269] /
  k04 [25815, 25867, 26064, 34269] / k05 [30322, 34269] /
  k06 [30341, 34269] / k07 [32720, 32748, 32861, 34269] /
  k08 [34080, 34081, 34269, 34903] / k09 [34207, 34269, 34912] /
  k10 [34255, 34266, 34269] / k11 [34269, 34912]; serving class
  34269 is ladder rank 1 (unknown_now 10 after the twentieth k01
  adoption reaudit, closure ladder `1a96311e`, 797 rows).
  Shared-owner pre-exclusion caveat applies to any adoption-side
  flip census: the owner union is a supertype of the eventual flip
  list.
- Outputs: raws for every run (calibration, 15M pairs) +
  batch-summary (schema `n11-twenty-first-ladder-top-escalation-summary-v1`)
  published as a kit with MANIFEST + fetch-back, then a completion
  log.

## Claim status

Escalation bookkeeping only: NO verdict is claimed or consumed.  Any
WIN/LOSS row produced here is single-implementation (jsreplay
replica) and requires the C++ second-implementation scrutiny gate
plus a third-implementation corroboration before any adoption Part.
The standard 11x11 empty board, all 19 central-reply roots, the
two-stone root {60,27}, the third-move pair {100,108} and every
closure class (including 34269) stay UNKNOWN.  Nodes, expansions
and wall_s are bookkeeping, never verdicts.
