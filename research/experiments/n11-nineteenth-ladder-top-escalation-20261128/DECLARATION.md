# 2026-11-28 n11 nineteenth ladder-top escalation declaration (k04-k05)

Single-owner declaration (publish-then-execute) for the 15M WIN-stop
escalation of the two remaining stage-1 keys of the class-20421
ladder-top selection, against the canonical head of record
`3abecf8b...` (6,903 rows WIN 221 / LOSS 6,682; the eighteenth k03
adoption head).  This lane is the declared owner of this Part;
declaration published at the main HEAD of this commit's parent.

## Pre-registered plan and predictions

- Keys (both verified FRESH to the head `3abecf8b` on this host by
  direct cache scan; both stage-1 2M UNKNOWN since the published
  sixteenth escalation kit `85edd462`; both UNCLAIMED,
  quarantine-free, D4-canonical, canonical-safe, dual-legal
  agreement from the published sixteenth selection):
  k04 `1153062242096250880:540672` (s5 index 620742 verified
  against the frozen graph, legal 83), k05
  `1152921642046849024:68719477248` (s5 index 625899 verified,
  legal 78).  Input rows: byte-identical copies of the published
  sixteenth escalation kit's `k04.input.csv` (`5ee6e813`) and
  `k05.input.csv` (`5656a6505`).
- Owner-union precheck (re-derived from the frozen graph on this
  host, disclosed): k04 [18534, 18554, 19885, 20421] / k05
  [18683, 18710, 20421]; the serving class 20421 is closure-ladder
  rank 1 with unknown_now 2 (k04, k05 are its last two cost-unknown
  children; k01-k03 already adopted WIN).  Shared-owner
  pre-exclusion caveat: 20421 is already excluded_now, so an
  adoption-side flip census would flip at most the non-serving
  owners.
- Runner: jsreplay replica sha256 `84585617...` (the published
  pinned replica, re-verified byte-exact on this host), fresh cold
  solver per row, budget-pinned, no shared TT.
- Calibration (after this declaration, before the runs): u01
  `1153485622925590528:0` at 2M must reproduce the published
  calibration raw VALUES (result 0, nodes 2,000,000, forbidden
  quadruples 95,670; input csv `52d79efc`).
- 15M escalation in the declared order k04 -> k05, cold pair each;
  **WIN-stop rule**: the first key that resolves WIN(1) stops the
  escalation (the later key stays at stage-1); a LOSS(2) resolution
  also completes that key's pair and the order continues; a 15M
  UNKNOWN parks that key (L50M only under a future declaration).
  Prediction (not a gate): both keys resist at 15M (their stage-1
  2M budget exhaustion and the uniform 4.5-5.6M-conflict-scale
  resistance pattern of this family suggest UNKNOWN; the
  measurement replaces any prediction).
- Outputs: raws for every run (calibration + both 15M pairs) +
  batch-summary (schema
  `n11-nineteenth-ladder-top-escalation-summary-v1`) published as a
  kit with MANIFEST + fetch-back, then a completion log.

## Claim status

Escalation bookkeeping only: NO verdict is claimed or consumed.
Any WIN/LOSS row produced here is single-implementation (jsreplay
replica, cold pair) and requires the C++ second-implementation
scrutiny gate plus a third-implementation corroboration before any
adoption Part; an adoption would additionally require the standing
WIN-side flip-census review.  Class 20421 is NOT complete unless
every remaining cost-unknown child resolves.  The standard 11x11
empty board, all 19 central-reply roots, the two-stone root
{60,27} and third moves 100/108 remain UNKNOWN.  Nodes are
bookkeeping, never verdicts.
