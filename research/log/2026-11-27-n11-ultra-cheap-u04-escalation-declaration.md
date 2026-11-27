# n11 ultra-cheap u04 escalation: single-owner declaration (publish-then-execute)

- Date: 2026-11-27 (declared before execution; executed after this push).
- Owner lane: the long-term 11x11 lane (this session). Parallel hourly sessions: do not run this key at any budget; this declaration claims the 15M escalation of the single key below.

## Scope (exactly this one key)

| id | key | class_index | legal | s5_index |
|----|-----|-------------|-------|----------|
| u04 | 1152921505747697664:1032 | 23101 | 85 | 745184 |

- Runner: jsreplay.js sha256 845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df (byte-verified against the published batch-stage1 wave-A input kit and the twelfth-cost kit), --n=11 --memo=22 --only=5 cold solver per row, no shared TT.
- Budget: 15,000,000 per run; cold pair (2 independent cold runs).
- WIN-stop rule: active but moot (single key). If the key resolves WIN(1) or LOSS(2) it is a single-implementation result only; UNKNOWN(0) at 15M parks it (L50M only under a future declaration).
- Head basis: c5082866 (merged-exact-s5-chain-plus-ultra-cheap-u03-20261127.cache, 6,893 rows WIN 211 / LOSS 6,682, 6,894 lines incl. header), fetched from main and sha256-verified. The key verified absent from the head (fresh). u01 (1153485622925590528:0, WIN(1) nodes 4,893,014), u02 (1297036830121656320:131074, WIN(1) nodes 3,167,121) and u03 (1153202979851993088:272, WIN(1) nodes 2,909,040) verified present.
- Inputs: identical to the published wave-A input row (research/experiments/n11-ultra-cheap-batch-stage1-2m-20261127/input/u04.input.csv, sha256 e09332d76bd506e7a6613e29411fbd06b55135389c02260727336375c3fb6479, byte-verified): target row, is_or=0, stones=5, legal 85.

## Pre-declaration disclosures

- Calibration only (not part of the escalation): one 2M-budget cold run of u01 (1153485622925590528:0) reproducing the published stage-1 raw values exactly: result 0, nodes 2000000, forbidden quadruples 95670 (wall_s 9 on this host vs the published raw's 10; host wall-clock variance). No u04 run at any budget was performed before this declaration.
- No other key will be run at any budget in this Part.

## Status guard

Scheduling/batch bookkeeping only. Any WIN/LOSS row produced here is a single-implementation result: before any adoption it requires the C++ second-implementation scrutiny gate plus a third-implementation corroboration (separate Parts), and a WIN-side adoption additionally requires the standing flip-census review. No verdict is consumed; nodes are bookkeeping, never evidence. The standard 11x11 empty board, the two-stone root {60,27} and its remaining third moves 100/108 stay UNKNOWN.
