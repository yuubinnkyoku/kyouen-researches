# 2026-11-28 n11 twentieth ladder-top escalation declaration

Single-owner declaration (publish-then-execute) for the stage-1 2M
cold-pair screen plus the 15M WIN-stop escalation of the eleven
selected keys of the twentieth ladder-top selection (class 34269
`1152921504624672768:68719476736`, kit `de1a99db`, completion
`f3a43b7f`), against the canonical head of record `e1a9cacc...`
(6,905 rows WIN 223 / LOSS 6,682).  Declaration published at main
HEAD `f3a43b7f`; this lane is the declared owner of this Part.

## Pre-registered plan and predictions

- Keys (all verified fresh to the head by the published twentieth
  selection selector, UNCLAIMED, quarantine-free, D4-canonical,
  canonical-safe, dual-legal agreement):
  k01 `10376293541479448576:68719476736` (s5 38891, legal 87),
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
  selection kit's `input/k01..k11.input.csv` (shas in that kit's
  MANIFEST at `de1a99db`).
- Runner: jsreplay replica sha256 `84585617...` (the published
  pinned replica of the C++ standalone exact-replay path at commit
  154f3b7a), fresh cold solver per row, budget-pinned
  (`--only=5 --memo=22`).
- Calibration (after this declaration, before the 15M runs): u01
  `1153485622925590528:0` at 2M must reproduce the published
  sixteenth escalation kit's calibration raw VALUES (result 0,
  nodes 2,000,000, forbidden quadruples 95,670).
- Stage-1: each of the eleven keys at 2,000,000 as a cold pair
  (two independent runs); expected stage-1 outcome is UNKNOWN(0)
  with budget exhaustion for the larger keys (prediction, not a
  gate).
- 15M escalation in the declared order k01 -> k02 -> ... -> k11,
  cold pair each; **WIN-stop rule**: the first key that resolves
  WIN(1) stops the escalation (later keys stay at stage-1); a
  LOSS(2) resolution also stops that key's own escalation (pair
  complete) and the order continues to the next key.  A 15M
  UNKNOWN parks that key (L50M only under a future declaration).
- Owner-union precheck (derived from the frozen graph
  `54f9c364` on this host, disclosed): k01 [769, 34269] /
  k02 [4715, 34269] / k03 [10153, 10691, 34269] /
  k04 [25815, 25867, 26064, 34269] / k05 [30322, 34269] /
  k06 [30341, 34269] / k07 [32720, 32748, 32861, 34269] /
  k08 [34080, 34081, 34269, 34903] / k09 [34207, 34269, 34912] /
  k10 [34255, 34266, 34269] / k11 [34269, 34912]; serving class
  34269 is ladder rank 1 (unknown_now 11).  Shared-owner
  pre-exclusion caveat applies to any adoption-side flip census:
  the owner union is a supertype of the eventual flip list.
- Outputs: raws for every run (stage-1 pairs, calibration, 15M
  pairs) + batch-summary (schema
  `n11-twentieth-ladder-top-escalation-summary-v1`) published as a
  kit with MANIFEST + fetch-back, then a completion log.

## Claim status

Escalation bookkeeping only: NO verdict is claimed or consumed.  Any
WIN/LOSS row produced here is single-implementation (jsreplay
replica) and requires the C++ second-implementation scrutiny gate
plus a third-implementation corroboration before any adoption Part.
The standard 11x11 empty board, all 19 central-reply roots, the
two-stone root {60,27}, the third-move pair {100,108} and every
closure class (including 34269) stay UNKNOWN.  Nodes, expansions
and wall_s are bookkeeping, never verdicts.
