# 2026-11-28 n11 eighteenth ladder-top escalation declaration

Single-owner declaration (publish-then-execute) for the 15M
WIN-stop escalation of the three remaining keys of the sixteenth
ladder-top selection (class 20421 `1155173304420536320:131072`),
i.e. k03-k05, against the canonical head of record
`e56ca5ca8d9f4674d23bb4ddca87dd9b7907c312fd0a4564631ae997aae20302`
(6,902 rows WIN 220 / LOSS 6,682, the seventeenth k02 adoption
head, adoption kit `859e2598`, completion `b015cf6c`; reaudit kit
`ef730ced`, completion `f746bb97`). Declaration published at
main HEAD `cb3c2ad9914e06c9d7e77e7c89204e69a25be803`; this lane is the declared owner of this
Part.

## Pre-registered plan and predictions

- Keys (the three unescalated keys remaining after the seventeenth
  k02 WIN-stop; stage-1 2M UNKNOWN(0) cold pairs published in the
  sixteenth escalation kit `85edd462`; all three verified fresh
  to the current head `e56ca5ca...` on this host by direct row
  scan (0 rows each), UNCLAIMED, quarantine-free, D4-canonical,
  canonical-safe, dual-legal agreement, per the published
  selector plus the measured head-delta disclosure below):
  k03 `1155173441859489792:131072` (s5 605961, legal 73),
  k04 `1153062242096250880:540672` (s5 620742, legal 83),
  k05 `1152921642046849024:68719477248` (s5 625899, legal 78).
  Input rows: byte-identical copies of the published seventeenth
  escalation kit's `k03..k05.input.csv`
  (`ff63ed29` / `5ee6e813` / `565a6505`, re-verified this session
  against the published kit MANIFEST-sha256).
- Freshness to the current head (disclosed, host-measured): the
  only delta between the sixteenth k01 head `dbc1d950...`
  (6,901 rows) and the current head `e56ca5ca...` (6,902 rows) is
  the adopted k02 WIN row `1156299204327378944:131072`
  (increment `11b8669c...`, present once in the head, row
  re-verified); k03-k05 were verified fresh to `dbc1d950...` by
  the published seventeenth escalation and are measured fresh to
  `e56ca5ca...` on this host (0 rows for every k03-k05 key).
- Runner: jsreplay replica sha256
  `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`
  (re-fetched this session from the published kit
  `n11-twelfthcost-class-s5-exclusive-probe-20261127`, sha-verified;
  the published pinned replica of the C++ standalone
  exact-replay path at commit `154f3b7a`), fresh cold solver per
  row, budget-pinned.
- Calibration (after this declaration, before the 15M runs): u01
  `1153485622925590528:0` at 2M must reproduce the published
  calibration raw VALUES (result 0, nodes 2,000,000, forbidden
  quadruples 95,670; input csv byte-identical `52d79efc`).
- 15M escalation in the declared order k03 -> k04 -> k05, cold
  pair each (two independent runs); **WIN-stop rule**: the first
  key that resolves WIN(1) stops the escalation (later keys stay
  at stage-1 2M); a LOSS(2) resolution also stops that key's own
  escalation (pair complete) and the order continues to the next
  key. A 15M UNKNOWN parks that key (L50M only under a future
  declaration).
- Owner-union precheck (identical to the published seventeenth
  precheck, re-derived from the frozen graph `54f9c364`,
  disclosed): k03 [18136, 18143, 20128, 20421] / k04 [18534,
  18554, 19885, 20421] / k05 [18683, 18710, 20421]; serving
  class 20421 is ladder rank 1 (unknown_now 3 after the k02
  adoption, measured in the seventeenth reaudit kit `ef730ced`).
  Shared-owner pre-exclusion caveat applies to any adoption-side
  flip census: the owner union is a supertype of the eventual
  flip list.
- Outputs: raws for every run (calibration, 15M pairs) +
  batch-summary (schema
  `n11-eighteenth-ladder-top-escalation-summary-v1`) published as
  a kit with MANIFEST + fetch-back, then a completion log.

## Claim status

Escalation bookkeeping only: NO verdict is claimed or consumed.
Any WIN/LOSS row produced here is single-implementation (jsreplay
replica) and requires the C++ second-implementation scrutiny gate
plus a third-implementation corroboration before any adoption
Part. The standard 11x11 empty board, all 19 central-reply roots,
the two-stone root {60,27}, the third-move pair {100,108} and
every closure class (including 20421) stay UNKNOWN. Nodes,
expansions and wall_s are bookkeeping, never verdicts.
