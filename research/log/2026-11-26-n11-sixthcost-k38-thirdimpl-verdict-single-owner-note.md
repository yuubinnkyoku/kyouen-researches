# n11 sixth-cost k38 third-impl verdict re-verification: single-owner fresh declaration (2026-11-26)

Pre-registered publish-then-execute declaration for the k38 L50M LOSS row's
third-implementation corroboration, closing the vacancy that both the Part SS
completion and the Part ST completion left open: the k38 row
(10376293541461626880:66048, legal 100) is a loss-resolved row of the
sixth-cost exclusive S5 batch with (a) a first-implementation L50M cold pair
(at 2bc21cf3: both LOSS(2) nodes 21,839,049) and (b) a delegated pinned C++
second-implementation scrutiny gate (Part SS, 4/4 GATE-PASS, target quadruple
100,50000000,2,21839049 node-exact), but no third implementation. This Part
executes that third implementation and publishes the raws.

## Scope (single-owner, verification only)

- Third implementation: third_impl.js sha256
  `08ea958ff59c3234ec5ac55c5c40689bd0999a34e101a88ea0546800cc4a1998`
  (byte-clone of the k01-k03 third-impl kit script, the same pinned script the
  k20/k33 third-impl Part used), driven with --memo-power=22 defaults.
- Calibration battery verify_tbl.js sha256
  `c8c52528f70b3a9b438edc3feb4e432fbe705d6be21650383d3955efc6790251`,
  consuming the jsreplay.js byte-clone
  `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`
  placed at its expected fixed host path.
- Target row input: byte-clone of the published probe-kit input
  research/experiments/n11-sixthcost-class-s5-exclusive-probe-10376293541461626880-20261121/input/k38.input.csv
  (sha256 `b6ef9f439ee0b6c9a35af08ff065a9323d0bec627beabb4defb9426a11d6600e`,
  row `target,0,5,10376293541461626880,66048,100,0,0,0,0,0`).
- Replica raws (first implementation, machine-fetched at HEAD 1f1577b0 and
  sha-pinned): at2m `fbb16943aae1e72023c3417970444915b43606c4318f51c756521db7f2ba0f00`
  (2,000,000 UNKNOWN), at15m-run1 `fb93014e5553e2f175904134174f4c5937de7ac874c9f5ce2052097083944d65`
  and at15m-run2 `a38dc147d237f6416d96dcf93eeb4355d2d2ac2e72498cad335b86c56d34face`
  (15,000,000 UNKNOWN pair), at50m-run1 `f7e519586d8e9dd7c8378aef2c96ccd70479816056954e93ffdf16732178bfcc`
  and at50m-run2 `53d0f69d03d0b04520f9f832e517f177ed9b0e33c917db3f114a5a77a602fe03`
  (both LOSS(2) nodes 21,839,049, the published L50M cold pair).
- Second-implementation provenance: Part SS kit
  research/experiments/n11-sixthcost-k38-l50m-cppgate-20261126/ (4/4 GATE-PASS,
  3 anchors + k38 target node-exact; not re-run here).
- Freshness: the k38 pair (10376293541461626880, 66048) is machine-verified
  ABSENT from the canonical head of record `dade15780...` (6,831 rows WIN201 /
  LOSS6630, fetched and sha-verified `dade15780ce6625cc70d93ba77b1560145dd2b9f096a53dce556d2fccf7e312b`
  at HEAD 1f1577b0).

## Pre-registered outcomes (a) through (c), same as the k20/k33 Part

- (a) C1 fresh calibration on this host: verify_tbl replica quads battery
  (expected 95,670 quads, 195,044 triples, 0 mismatches, per the k05/k20k33
  precedents) and anchor w2 10376293541461626880:131328 WIN(1) expansions
  7,583,990 on two executions, identical quadruple.
- (b) C2 k38 cold runs a/b + verify-legal: pre-registered expectation
  verdict-level agreement LOSS(2) with the published replica raws. The
  third-impl expansion count is NOT pre-registered (different implementations
  count differently; anti-copy gate requires it to differ from 21,839,049).
- (c) C4 fail-closed input gates: legal 101 and stones 6 must both GATE_FAIL
  with process exit status 1.
- Hard stop: any verdict-level disagreement between the third implementation
  and the published replica raws is a C5 hard stop; the executing session stops
  without adoption, discloses, and does NOT proceed to any adoption Part.

## Kit (wave B) and completion (wave C)

Kit dir: research/experiments/n11-sixthcost-k38-l50m-thirdimpl-20261126/
(third_impl.js + verify_tbl.js + jsreplay.js byte-clones, input byte-clone,
run raws, calibration raws, negative-gate raws, tamper log, auditor
audit_k38.py, README, MANIFEST-sha256). Completion log in research/log/.
All pushes fetch-back byte-verified (raw CDN curl + sha256; contents API git
blob sha as authority where CDN is stale).

## Status guard

Verification only. No verdict consumed, no cache row published, no class
status flipped, no route to any root certificate laid. The standard 11x11
empty board, the two-stone root {60,27}, its remaining third moves
{100,108}, S2, class 1/2/4, and every closure class remain UNKNOWN
throughout. Nodes and expansions are bookkeeping, never verdicts. An S5 LOSS
raw is not a class closure claim, and LOSS rows transfer no root verdict. The
canonical head of record `dade15780...` is untouched by this Part. With this
Part, if the pre-registered outcome holds, k38 reaches the k13/k19/k20/k33
coverage level (ladder primary pair + C++ second-impl gate + third-impl
verdict-level) and becomes an adoption-eligible input for a future
adoption Part against BASE `dade15780`; that Part is explicitly NOT this
record and requires its own fresh declaration and a WIN/LOSS conflict
policy review.