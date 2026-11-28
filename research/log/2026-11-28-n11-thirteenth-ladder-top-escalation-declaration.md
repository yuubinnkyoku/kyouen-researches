# n11 thirteenth ladder-top escalation: single-owner declaration (publish-then-execute)

- Date: 2026-11-28 (declared before execution; executed after this push).
- Owner lane: the long-term 11x11 lane (this session). Parallel hourly
  sessions: do not run these keys at any budget; this declaration
  claims the 2M cold-pair sweep and the 15M escalation of the two
  keys below (the selected batch of
  `research/experiments/n11-thirteenth-ladder-top-selection-20261128`,
  selection kit commit `fa4e6cb2`, declaration commit `7583169d`).

## Scope (exactly these two keys, the class 16757 batch)

| id | key | class_index | legal | s5_index |
|----|-----|-------------|-------|----------|
| k01 | 1153204147814662144:65536 | 16757 | 72 | 556117 |
| k02 | 1152922672837951488:65792 | 16757 | 72 | 558553 |

- Runner: jsreplay.js sha256
  845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df
  (byte-verified against the published twelfth-cost kit),
  `--only=5 --memo=22` cold solver per row, no shared TT.
- Stage 1: budget 2,000,000 per run; cold pair (2 independent cold
  runs) per key.
- Escalation: 15,000,000 per run cold pair for keys left UNKNOWN(0)
  at 2M, in k01 -> k02 order, with the standing WIN-stop rule (the
  first WIN(1) at 15M stops the remaining escalations; suppressed
  keys stay 2M UNKNOWN).
- Head basis: beecb024
  (merged-exact-s5-chain-plus-ultra-cheap-u04-20261127.cache, 6,894
  rows WIN 212 / LOSS 6,682), fetched from main and sha256-verified;
  both keys verified fresh/absent from the head by the selection
  Part's gates.
- Inputs: byte-identical to the selection kit's input rows
  (input/k01.input.csv sha256
  eda6e3d6d5d639039b7b57c34aaaaa960ffe5d1172b187aadfe63a9393b8e00f,
  input/k02.input.csv sha256
  6ff8d84eacaa5a3c8091ec91935caf743b74641116f91f9de9d2413e30682aa5).

## Pre-declaration disclosures

- Calibration only (not part of the escalation): one 2M-budget cold
  run of u01 (`1153485622925590528:0`) reproducing the published
  stage-1 raw values exactly: result 0, nodes 2000000, forbidden
  quadruples 95670, wall_s 9 (byte-equal to the published u03/u04
  escalation kits' calibration raw on this host). No k01/k02 run at
  any budget was performed before this declaration.
- Neither key is in the probe-13 supply, so no proxy prior exists;
  the 15M budget follows the standing ultra-cheap escalation
  convention.

## Status guard

Scheduling/batch bookkeeping only; NO verdict consumed. Any WIN/LOSS
row produced here is a single-implementation result: before any
adoption it requires the C++ second-implementation scrutiny gate plus
a third-implementation corroboration (separate Parts), and a WIN-side
adoption additionally requires the standing flip-census review (the
WIN keys would complete class 16757, a candidate free_now flip,
Board-verified at adoption time). Nodes are bookkeeping, never
evidence. The standard 11x11 empty board, the two-stone root {60,27}
and its remaining third moves 100/108 stay UNKNOWN.
