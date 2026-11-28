# Declaration: n11 fifteenth ladder-top class 5804 batch escalation (single-owner, publish-then-execute)

Single-owner declaration by the long-term 11x11 lane. Published BEFORE
execution. Any parallel lane must not probe or resolve the keys below
until this Part's completion log appears.

## Scope

Batch escalation of the three keys selected by the published
fifteenth ladder-top selection kit
(`research/experiments/n11-fifteenth-ladder-top-selection-20261128/`,
kit commit `6f6deac0`, log `7da320b9`): ladder-top class 5804, exactly 3
remaining unknown S5 keys:

- k01 `6053682324116078592:0` (s5 207094, legal 82)
- k02 `6052837899185946628:128` (s5 212115, legal 87)
- k03 `6053400849139367936:128` (s5 212536, legal 92)

Against the canonical head of record `a66f636e` (6,897 rows
WIN 215 / LOSS 6,682). Declaration HEAD pin: 7da320b94556c98ca3d93f30dec6af2c04ed9727.

## Method and declared order

Runner: the standing jsreplay replica `jsreplay.js` sha256
`845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`
(`--only=5 --memo=22` cold solver per row, no shared TT), fetched from
`research/experiments/n11-s4bd-fresh-corpus-regen-20261121/scripts/jsreplay.js`
and sha-verified. Declared order: k01, k02, k03.

1. Stage-1: each key 2M budget, cold pair (2 fresh runs), pair must be
   node-identical (byte-identity expected modulo wall_s).
2. Escalation: in declared order, 15M budget cold pair per key while
   no WIN has appeared; the WIN-stop rule fires on the first WIN(1)
   at 15M and suppresses all remaining keys' escalations (they stay
   stage-1 2M UNKNOWN; parking/L50M only under a future declaration).
   A LOSS(2) at 15M does NOT stop the batch; the next key escalates.
3. No L50M stage in this Part.

## Pre-declaration calibration (disclosed)

Before this declaration was published, a u01 (`1153485622925590528:0`)
2M cold run was executed on this host: result 0, nodes 2,000,000,
forbidden quadruples 95,670, wall_s 9 - values identical to the
published `cal-u01-at2m.raw` of the fourteenth ladder-top escalation
kit (same input csv sha `52d79efc...`). Only stdout footer line
ordering may differ between hosts (buffering); no values differ.

## Non-meaning

Batch bookkeeping only: NO verdict is consumed by this Part alone.
Any WIN row is single-implementation (jsreplay replica, cold pair)
and requires the C++ second-implementation scrutiny gate plus a
third-implementation corroboration before any adoption Part. Even if
all three keys resolve, class 5804 completion is a candidate free_now
flip only, Board-verified at adoption time - NOT a root or 11x11
verdict. The standard 11x11 empty board, all 19 central-reply roots,
the two-stone root {60,27} and its remaining third moves 100/108 stay
UNKNOWN. Nodes are bookkeeping, never verdicts.

## Disclosures

- This lane runs without access to the user's computer (scheduled
  task); publication is via the GitHub API only.
- The three input CSVs are byte-identical copies of the fifteenth
  selection kit's input files (legal 82/87/92, dual-implementation
  derived in the selection Part; byte-identical to the fourteenth
  selection kit's k02/k03/k04 inputs).
