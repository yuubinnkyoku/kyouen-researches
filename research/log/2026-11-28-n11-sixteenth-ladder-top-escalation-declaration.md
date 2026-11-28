# 2026-11-28 n11 sixteenth ladder-top escalation declaration

Single-owner declaration (publish-then-execute) for the stage-1 2M
cold-pair screen plus the 15M WIN-stop escalation of the five
selected keys of the sixteenth ladder-top selection (class 20421
`1155173304420536320:131072`, kit `b4e338aa`, completion
`27829d8c`), against the canonical head of record `58110025...`
(6,900 rows WIN 218 / LOSS 6,682).  Declaration published at main
HEAD `27829d8c`; this lane is the declared owner of this Part.

## Pre-registered plan and predictions

- Keys (all verified fresh to the head by the published sixteenth
  selection selector, UNCLAIMED, quarantine-free, D4-canonical,
  canonical-safe, dual-legal agreement):
  k01 `1155454779397246976:131072` (s5 528689, legal 76),
  k02 `1156299204327378944:131072` (s5 543795, legal 73),
  k03 `1155173441859489792:131072` (s5 605961, legal 73),
  k04 `1153062242096250880:540672` (s5 620742, legal 83),
  k05 `1152921642046849024:68719477248` (s5 625899, legal 78).
  Input rows: byte-identical copies of the published sixteenth
  selection kit's `input/k01..k05.input.csv`
  (`6288b82f` / `67526707` / `ff63ed29` / `5ee6e813` /
  `565a6505`).
- Runner: jsreplay replica sha256 `84585617...` (the published
  pinned replica of the C++ standalone exact-replay path at commit
  154f3b7a), fresh cold solver per row, budget-pinned.
- Calibration (after this declaration, before the 15M runs): u01
  `1153485622925590528:0` at 2M must reproduce the published
  fifteenth escalation kit's calibration raw VALUES (result 0,
  nodes 2,000,000, forbidden quadruples 95,670).
- Stage-1: each of the five keys at 2,000,000 as a cold pair
  (two independent runs); expected stage-1 outcome is UNKNOWN(0)
  with budget exhaustion for the larger keys (prediction, not a
  gate).
- 15M escalation in the declared order k01 -> k02 -> k03 -> k04 ->
  k05, cold pair each; **WIN-stop rule**: the first key that
  resolves WIN(1) stops the escalation (later keys stay at
  stage-1); a LOSS(2) resolution also stops that key's own
  escalation (pair complete) and the order continues to the next
  key.  A 15M UNKNOWN parks that key (L50M only under a future
  declaration).
- Owner-union precheck (derived from the frozen graph
  `54f9c364` on this host, disclosed): k01 [15647, 16901, 20421] /
  k02 [16104, 16132, 16656, 20421] / k03 [18136, 18143, 20128,
  20421] / k04 [18534, 18554, 19885, 20421] / k05 [18683, 18710,
  20421]; serving class 20421 is ladder rank 1 (unknown_now 5).
  Shared-owner pre-exclusion caveat applies to any adoption-side
  flip census: the owner union is a supertype of the eventual
  flip list.
- Outputs: raws for every run (stage-1 pairs, calibration, 15M
  pairs) + batch-summary (schema
  `n11-sixteenth-ladder-top-escalation-summary-v1`) published as a
  kit with MANIFEST + fetch-back, then a completion log.

## Claim status

Escalation bookkeeping only: NO verdict is claimed or consumed.  Any
WIN/LOSS row produced here is single-implementation (jsreplay
replica) and requires the C++ second-implementation scrutiny gate
plus a third-implementation corroboration before any adoption Part.
The standard 11x11 empty board, all 19 central-reply roots, the
two-stone root {60,27}, the third-move pair {100,108} and every
closure class (including 20421) stay UNKNOWN.  Nodes, expansions
and wall_s are bookkeeping, never verdicts.
