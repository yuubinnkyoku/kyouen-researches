# n11 ultra-cheap u03/u04 escalation: single-owner declaration (publish-then-execute)

- Date: 2026-11-27 (declared before execution; executed after this push).
- Owner lane: the long-term 11x11 lane (this session). Parallel hourly sessions: do not run these keys at any budget; this declaration claims the 15M escalation of the two keys below.

## Scope (exactly these two keys, declared order u03 -> u04)

| id | key | class_index | legal | s5_index |
|----|-----|-------------|-------|----------|
| u03 | 1153202979851993088:272 | 16371 | 78 | 550879 |
| u04 | 1152921505747697664:1032 | 23101 | 85 | 745184 |

- Runner: jsreplay.js sha256 845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df (byte-verified against research/experiments/n11-ultra-cheap-batch-stage1-2m-20261127 wave-A and the twelfth-cost kit), --n=11 --memo=22 --only=5 cold solver per row, no shared TT.
- Budget: 15,000,000 per run; cold pair (2 independent cold runs) per key.
- WIN-stop rule: active. If a key resolves WIN(1) or LOSS(2), the remaining declared keys in order are escalation-suppressed for this Part and stay UNKNOWN at 2M (parking/L50M only under a future declaration).
- Head basis: 82b52577 (merged-exact-s5-chain-plus-ultra-cheap-u02-20261127.cache, 6,892 rows WIN 210 / LOSS 6,682, 288,677 bytes), fetched from main and sha256-verified. Both keys verified absent from the head (fresh). u01 (1153485622925590528:0, WIN(1) nodes 4,893,014) and u02 (1297036830121656320:131074, WIN(1) nodes 3,167,121) verified present.
- Inputs: identical to the published wave-A input rows (research/experiments/n11-ultra-cheap-batch-stage1-2m-20261127/input/u03.input.csv, u04.input.csv; byte-verified): target rows, is_or=0, stones=5, legal as in the table above.

## Pre-declaration disclosures

- Calibration only (not part of the escalation): one 2M-budget cold run of u01 (1153485622925590528:0) reproducing the published at2m raw exactly: result 0, nodes 2000000, wall_s 10, forbidden quadruples 95670. No u03/u04 run at any budget was performed before this declaration.
- No other key will be run at any budget in this Part.

## Status guard

Scheduling/batch bookkeeping only. Any WIN/LOSS row produced here is a single-implementation result: before any adoption it requires the C++ second-implementation scrutiny gate plus a third-implementation corroboration (separate Parts), and a WIN-side adoption additionally requires the standing flip-census review. No verdict is consumed; nodes are bookkeeping, never evidence. The standard 11x11 empty board, the two-stone root {60,27} and its remaining third moves 100/108 stay UNKNOWN.
