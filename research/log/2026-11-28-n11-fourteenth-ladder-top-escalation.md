# n11 fourteenth ladder-top class 5804 batch escalation completion (2026-11-28)

Completion log of the escalation declared in
`research/log/2026-11-28-n11-fourteenth-ladder-top-escalation-declaration.md`
(declaration commit `86a8b791`, single owner, publish-then-execute).
Kit:
`research/experiments/n11-fourteenth-ladder-top-escalation-20261128/`
(19 files, fetch-back 19/19 byte-identical at kit commit `5c670bc6`).

## Outcome

- Selected by the fourteenth ladder-top selection (class 5804
  `6053400849139367936:0`, 4 remaining unknown S5 keys, head
  `d772f73c...` 6,896 rows WIN 214 / LOSS 6,682).
- Stage-1 (2M cold pair each, declared order k01-k04): all four keys
  **UNKNOWN(0), nodes 2,000,000**, pairs node-identical
  (k01/k02/k03 fully byte-identical; k04 wall_s 9 vs 8, host timing
  only).
- 15M escalation: **k01 `6053401124017274880:0` (s5_index 198576,
  legal 86) is WIN(1), nodes 4,360,661**, cold pair fully
  byte-identical (wall_s 20 both passes).
- **WIN-stop fired**: k02/k03/k04 escalations suppressed; they stay
  stage-1 2M UNKNOWN (parking/L50M only under a future declaration).
  No other key was run at any higher budget in this Part.
- Calibration (pre-declaration, disclosed in the declaration): u01
  `1153485622925590528:0` 2M cold run reproduces the published
  thirteenth escalation calibration raw values exactly (result 0,
  nodes 2,000,000, forbidden quadruples 95,670, wall_s 9); only
  stdout footer line ordering differs between hosts (buffering).
- Runner jsreplay.js sha256 `84585617...` fetched fresh from main
  (`research/experiments/n11-s4bd-fresh-corpus-regen-20261121/scripts/`)
  and sha-verified before the runs.

## Claim status

Batch bookkeeping only: NO verdict is consumed. The k01 WIN row is
single-implementation (jsreplay replica, cold pair). Before any
adoption Part it requires the C++ second-implementation scrutiny
gate (expected gate row `86,15000000,1,4360661` at the standing
15M cap) plus a third-implementation corroboration, and a k01
adoption would additionally require the standing WIN-side
flip-census review (owner-class union derived from the frozen graph;
note k04 shares its key mask base with the serving class
`6053400849139367936:0`). Class 5804 is NOT complete (k02/k03/k04
remain unknown), so no free_now flip is claimed here.

## Next work

- k01 WIN 3-pillar Part (C++ gate + third_impl corroboration) under a
  separate single-owner declaration; then k01-only adoption
  (head 6,896 -> 6,897 rows WIN 214 -> 215) and its flip-census/
  reaudit follow-up; then the k02/k03/k04 re-escalation decision
  (fresh declaration).

## Guards

The standard 11x11 empty board: UNKNOWN. All 19 central-reply
roots: UNKNOWN. Two-stone root {60,27}: UNKNOWN. Third-move pair
{100,108}: UNKNOWN. Nodes are bookkeeping, never verdicts. (kit
commit `5c670bc6`, log commit below)
