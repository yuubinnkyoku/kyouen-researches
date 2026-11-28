# Declaration: n11 fourteenth ladder-top class 5804 batch escalation (single-owner, publish-then-execute)

Single-owner declaration by the long-term 11x11 lane. Published BEFORE
execution. Any parallel lane must not probe or resolve the keys below
until this Part's completion log appears.

## Scope

Batch escalation of the four keys selected by the published
fourteenth ladder-top selection kit
(`research/experiments/n11-fourteenth-ladder-top-selection-20261128/`,
kit commit `a85f9c20`, log commit `0d251e82`): class 5804
(`6053400849139367936:0`), exactly 4 remaining unknown S5 keys,
against the canonical head of record `d772f73c...` (6,896 rows
WIN 214 / LOSS 6,682). Declaration HEAD pin: `0d251e8210e16c5fdf3dada949a306200cb652b8`.

## Method and declared order

Runner: the standing jsreplay replica `jsreplay.js` sha256
`845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`
(`--only=5 --memo=22` cold solver per row, no shared TT), fetched from
`research/experiments/n11-s4bd-fresh-corpus-regen-20261121/scripts/jsreplay.js`
and sha-verified. Declared order: k01, k02, k03, k04.

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
published `cal-u01-at2m.raw` (sha256 `05ce2090...`) of the
thirteenth ladder-top escalation kit. Only line ordering of the
stdout footer differs between hosts (buffering); no values differ.

## Non-meaning

Batch bookkeeping only: NO verdict is consumed by this Part alone.
Any WIN row is single-implementation (jsreplay replica, cold pair)
and requires the C++ second-implementation scrutiny gate plus a
third-implementation corroboration before any adoption Part. Even if
all four keys resolve, class 5804 completion is a candidate free_now
flip only, Board-verified at adoption time - NOT a root or 11x11
verdict. The standard 11x11 empty board, all 19 central-reply roots,
the two-stone root {60,27} and its remaining third moves 100/108 stay
UNKNOWN. Nodes are bookkeeping, never verdicts.

## Disclosures

- This lane runs without access to the user's computer (scheduled
  task); publication is via the GitHub API only.
- The four input CSVs are byte-identical copies of the selection
  kit's `input/` files (legal column 86/82/87/92, dual-implementation
  derived in the selection Part).
