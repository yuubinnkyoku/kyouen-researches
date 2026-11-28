# 2026-11-28 n11 seventeenth ladder-top escalation declaration

Single-owner declaration (publish-then-execute) for the 15M
WIN-stop escalation of the four remaining keys of the sixteenth
ladder-top selection (class 20421 `1155173304420536320:131072`),
i.e. k02-k05, against the canonical head of record
`dbc1d9508dda61a353ba7b9ef60371bb28eb08cf8f4cd6d30122eafd6a72bc21`
(6,901 rows WIN 219 / LOSS 6,682, the sixteenth k01 adoption
head, adoption kit completion `d555c1d6`; reaudit `3241928c`).
Declaration published at main HEAD `3241928c`; this lane is the
declared owner of this Part.

## Pre-registered plan and predictions

- Keys (the four unescalated keys of the published sixteenth
  ladder-top selection, kit `b4e338aa`, completion `27829d8c`;
  stage-1 2M UNKNOWN(0) cold pairs published in the sixteenth
  escalation kit `85edd462`; all four verified fresh to the
  current head `dbc1d950...` on this host, UNCLAIMED,
  quarantine-free, D4-canonical, canonical-safe, dual-legal
  agreement, per the published selector plus the measured
  head-delta disclosure below):
  k02 `1156299204327378944:131072` (s5 543795, legal 73),
  k03 `1155173441859489792:131072` (s5 605961, legal 73),
  k04 `1153062242096250880:540672` (s5 620742, legal 83),
  k05 `1152921642046849024:68719477248` (s5 625899, legal 78).
  Input rows: byte-identical copies of the published sixteenth
  escalation kit's `input/k02..k05.input.csv`
  (`67526707` / `ff63ed29` / `5ee6e813` / `565a6505`,
  re-verified this session against the published kit MANIFEST at
  commit `85edd462`).
- Freshness to the current head (disclosed, host-measured): the
  only delta between the sixteenth head `58110025...` (6,900 rows)
  and the current head `dbc1d950...` (6,901 rows) is the adopted
  k01 WIN row `1155454779397246976:131072` (increment
  `bb029422...`); k02-k05 were verified fresh to `58110025...`
  by the published selector and are measured fresh to
  `dbc1d950...` on this host (no k02-k05 key appears in the
  head).
- Runner: jsreplay replica sha256
  `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`
  (re-fetched this session from the published kit
  `n11-centralreply-class2251-b29ckpt1-audit-thirdimpl-20261124`,
  sha-verified; the published pinned replica of the C++
  standalone exact-replay path at commit `154f3b7a`), fresh cold
  solver per row, budget-pinned.
- Calibration (after this declaration, before the 15M runs): u01
  `1153485622925590528:0` at 2M must reproduce the published
  calibration raw VALUES (result 0, nodes 2,000,000, forbidden
  quadruples 95,670; input csv byte-identical `52d79efc`).
- 15M escalation in the declared order k02 -> k03 -> k04 -> k05,
  cold pair each (two independent runs); **WIN-stop rule**: the
  first key that resolves WIN(1) stops the escalation (later
  keys stay at stage-1 2M); a LOSS(2) resolution also stops that
  key's own escalation (pair complete) and the order continues to
  the next key.  A 15M UNKNOWN parks that key (L50M only under a
  future declaration).
- Owner-union precheck (re-derived on this host from the frozen
  graph `54f9c364`, identical to the published sixteenth
  precheck, disclosed): k02 [16104, 16132, 16656, 20421] /
  k03 [18136, 18143, 20128, 20421] / k04 [18534, 18554, 19885,
  20421] / k05 [18683, 18710, 20421]; serving class 20421 is
  ladder rank 1 (unknown_now 4 after the k01 adoption, measured
  in the reaudit kit `3241928c`).  Shared-owner pre-exclusion
  caveat applies to any adoption-side flip census: the owner
  union is a supertype of the eventual flip list.
- Outputs: raws for every run (calibration, 15M pairs) +
  batch-summary (schema
  `n11-seventeenth-ladder-top-escalation-summary-v1`) published
  as a kit with MANIFEST + fetch-back, then a completion log.

## Claim status

Escalation bookkeeping only: NO verdict is claimed or consumed.
Any WIN/LOSS row produced here is single-implementation (jsreplay
replica) and requires the C++ second-implementation scrutiny gate
plus a third-implementation corroboration before any adoption
Part.  The standard 11x11 empty board, all 19 central-reply
roots, the two-stone root {60,27}, the third-move pair
{100,108} and every closure class (including 20421) stay
UNKNOWN.  Nodes, expansions and wall_s are bookkeeping, never
verdicts.
