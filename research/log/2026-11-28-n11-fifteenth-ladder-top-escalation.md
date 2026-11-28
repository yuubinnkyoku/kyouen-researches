# n11 fifteenth ladder-top class 5804 batch escalation completion (2026-11-28)

Completion log of the escalation declared in
`research/log/2026-11-28-n11-fifteenth-ladder-top-escalation-declaration.md`
(declaration commit `8340f669`, amendment `c8eed460`, single owner,
publish-then-execute). Kit:
`research/experiments/n11-fifteenth-ladder-top-escalation-20261128/`
(16 files, fetch-back 16/16 blob-sha byte-identical at kit commit
`a33217ca`).

## Outcome

- Selected by the fifteenth ladder-top selection (ladder-top class
  5804, 3 remaining unknown S5 keys: k01 `6053682324116078592:0`
  (s5_index 207094, legal 82), k02 `6052837899185946628:128`
  (s5_index 212115, legal 87), k03 `6053400849139367936:128`
  (s5_index 212536, legal 92), head `a66f636e...` 6,897 rows
  WIN 215 / LOSS 6,682).
- Declaration amendment: commit `8340f669` mis-stated the
  class-5804 parenthetical key string; amendment `c8eed460`
  corrected it to the three selection-kit keys and was published
  BEFORE any stage-1 run of this Part. Scope, key set, method and
  order unchanged.
- Stage-1 (2M cold pair each, declared order k01-k03): all three
  keys **UNKNOWN(0), nodes 2,000,000**, pairs node-identical
  (k03 fully byte-identical; k01 wall_s 10 vs 9, k02 wall_s 9 vs 8,
  host timing only).
- 15M escalation: **k01 `6053682324116078592:0` (s5_index 207094,
  legal 82) is WIN(1), nodes 12,803,283**, cold pair
  node-identical (wall_s 70 vs 69). k01 is the key that stayed 2M
  UNKNOWN as the fourteenth batch's k02; this is its first
  resolution.
- **WIN-stop fired**: k02/k03 escalations suppressed; they stay
  stage-1 2M UNKNOWN (parking/L50M only under a future declaration).
  No other key was run at any higher budget in this Part.
- Calibration (pre-declaration, disclosed in the declaration): u01
  `1153485622925590528:0` 2M cold run reproduces the published
  fourteenth escalation calibration raw values exactly (result 0,
  nodes 2,000,000, forbidden quadruples 95,670, wall_s 9); only
  stdout footer line ordering differs between hosts (buffering),
  so this kit's cal raw sha (05ce2090...) differs from the
  fourteenth kit's raw (a8c9480d...) while no values differ.
- Runner jsreplay.js sha256 `84585617...` fetched fresh from main
  (`research/experiments/n11-s4bd-fresh-corpus-regen-20261121/scripts/`)
  and sha-verified before the runs.

## Claim status

Batch bookkeeping only: NO verdict is consumed. The k01 WIN row is
single-implementation (jsreplay replica, cold pair). Before any
adoption Part it requires the C++ second-implementation scrutiny
gate (expected gate row `82,15000000,1,12803283` at the standing
15M cap) plus a third-implementation corroboration, and a k01
adoption would additionally require the standing WIN-side
flip-census review. Class 5804 is NOT complete (k02/k03 remain
unknown), so no free_now flip is claimed here.

## Next work

- k01 WIN 3-pillar Part (C++ gate + third_impl corroboration) under
  a separate single-owner declaration; then k01-only adoption
  (head 6,897 -> 6,898 rows WIN 215 -> 216) and its flip-census/
  reaudit follow-up; then the k02/k03 re-escalation decision
  (fresh declaration).

## Guards

The standard 11x11 empty board: UNKNOWN. All 19 central-reply
roots: UNKNOWN. Two-stone root {60,27}: UNKNOWN. Third-move pair
{100,108}: UNKNOWN. Nodes are bookkeeping, never verdicts. (kit
commit `a33217ca`, log commit below)
