# Completion log: n11 nineteenth ladder-top escalation (k04-k05)

Completion of the Part declared in
`research/log/2026-11-28-n11-nineteenth-ladder-top-escalation-declaration.md`
(declaration commit `b27b8f24`, single owner, publish-then-execute,
parent HEAD `4b17d87f`).  Kit:
`research/experiments/n11-nineteenth-ladder-top-escalation-20261128/`
(commit `73cf1b2f`; fetch-back byte-identical against the kit
MANIFEST-sha256 via commit-pinned raw CDN + sha256).

## Result

Escalation of the two remaining stage-1 keys of the class-20421
ladder-top selection against the canonical head of record
`3abecf8b...` (6,903 rows WIN 221 / LOSS 6,682; both keys verified
fresh to the head by direct cache scan before the declaration).

- **k04 `1153062242096250880:540672` (s5 index 620742, legal 83,
  serving class 20421) is WIN(1) at the 15M budget, nodes 6,877,739
  (45.9% of budget), cold pair node-identical (wall_s 37/36).**
  The WIN-stop rule fired; k05 was not escalated.
- k05 `1152921642046849024:68719477248` (s5 index 625899, legal
  78) stays at stage-1 2M UNKNOWN (published sixteenth-kit stage-1
  raws; not rerun here).
- Calibration u01 `1153485622925590528:0` at 2M reproduces the
  published calibration VALUES exactly (result 0, nodes 2,000,000,
  forbidden quadruples 95,670, wall_s 9; the raw is byte-identical
  to the published sixteenth-kit calibration raw sha `05ce2090`).
- The declared prediction (both keys resist at 15M) did NOT hold
  for k04: k04 resolved WIN(1) at 45.9% of budget.  The measurement
  replaces the prediction; this deviation is disclosed here and in
  the kit README.
- Owner-union precheck (re-derived from the frozen graph on this
  host): k04 [18534, 18554, 19885, 20421] / k05 [18683, 18710,
  20421].  The serving class 20421 is closure-ladder rank 1 with
  unknown_now 2 before this Part; after a future k04 adoption (not
  performed here) k05 would be its last cost-unknown child.

## Claim status / next

This kit is escalation bookkeeping only: NO verdict is consumed.
The k04 WIN(1) row is single-implementation (jsreplay replica,
cold pair) and requires the C++ second-implementation scrutiny
gate (expected gate row `83,15000000,1,6877739` @15M cap) plus a
third-implementation corroboration before any adoption Part; a
k04 adoption would additionally require the standing WIN-side
flip-census review.  Class 20421 is NOT complete (k05 remains
stage-1 2M UNKNOWN; no ladder exit).  The standard 11x11 empty
board, all 19 central-reply roots, the two-stone root {60,27} and
third moves 100/108 remain UNKNOWN.  Nodes are bookkeeping, never
verdicts.

Next (separate declared Part): k04 WIN 3-pillars (C++ gate +
third_impl corroboration), then k04-only canonical adoption, then
the flip-census reaudit (owner union [18534, 18554, 19885, 20421]
with the standing pre-exclusion caveat on 20421), then the k05
escalation decision.
