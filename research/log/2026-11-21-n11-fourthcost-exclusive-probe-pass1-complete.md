# 2026-11-21 n11 fourth-cost class 1297107061427929088:0 — exclusive S5 probe pass-1 ladder COMPLETE (33 LOSS / 8 UNKNOWN@15M / 0 WIN)

## What this note records
The single-owner fourth-cost exclusive S5 probe batch (declaration commit 1f94f501,
41 keys, machine list published in the experiment dir input/) finished its
pass-1 ladder for all 41 keys this session. Every raw row cited below is
published under the experiment dir output/raw/ (per-key at2m plus both 15M
runs, pushed incrementally in checkpoints k01-k05, k06-k09, k10-k15, k16-k21,
k22-k27, k28-k33, k34-k41). This note is compiled from those published rows.

## Headline tally (41/41 keys)
- LOSS (solver-trusted exact, cache rows emitted): 33
- UNKNOWN@15,000,000 (parked, no cache row): 8
- WIN: 0  -> the batch stop rule (stop on first WIN) never fired
- Determinism: every key that resolved at the 15M stage ran twice with fresh
  solvers; result and nodes identical on both runs for every decided key
  (byte-published per key). 5 keys resolved already at the 2M stage.

## Per-key outcomes (order = exclusive_unclaimed_probe_order)
- LOSS at 2M stage (5): k01 1297107061427929088:65536 (1,914,160 n), k03
  1297107061427937280:0 (1,762,669), k05 1297107061428060160:0 (1,814,500),
  k28 1297388536404639744:0 (1,840,295), k33 5908793079855316992:0 (1,777,780).
- LOSS at 15M stage (28, nodes identical across both runs): k04
  1297107061427994624:0 (2,631,074), k06 1297107061444706304:0 (2,066,625),
  k07 1297107062501670912:0 (2,229,083), k08 1297247798916284416:0 (9,756,391),
  k09 10416825938107961344:0 (2,702,511), k10 1152921504607895552:1627389952
  (4,749,179), k12 1161928703861592064:805306368 (5,713,123), k14
  1297107061427929088:16 (5,757,693), k15 1297107061427929088:128 (2,333,629),
  k16 1297107061427929088:16384 (6,870,618), k18 1297107061427929089:0
  (2,527,617), k19 1297107061427929092:0 (2,644,692), k20 1297107061427929120:0
  (3,029,060), k21 1297107061427929216:0 (2,228,132), k22 1297107061427929344:0
  (4,344,852), k24 1297107061427961856:0 (7,307,808), k25 1297107061562146816:0
  (2,905,241), k26 1297107061696364544:0 (4,755,671), k27 1297108160939556864:0
  (3,027,775), k29 1369164655465857024:0 (5,755,774), k30 1585337437579640832:0
  (5,185,651), k34 10380797141088997376:8 (3,221,348), k35
  10380797141088997376:131072 (4,193,333), k36 10380797141088997376:67108864
  (3,116,170), k37 1152921504606851072:805306369 (3,615,154), k39
  1152930300699873280:805306368 (5,519,163), k40 1297107061427929088:16777216
  (8,109,091), k41 1297107336305836032:0 (2,515,856).
- UNKNOWN@15M parked (8, both runs result 0 at 15,000,000 nodes): k02
  1297107061427929088:67108864 (legal 82), k11 1152921504809222144:68719476736
  (91), k13 1297107061427929088:8 (99), k17 1297107061427929088:536870912 (93),
  k23 1297107061427933184:0 (95), k31 1873567813731352576:0 (91), k32
  3602950070641623040:0 (91), k38 1152921504607899648:805306368 (102).

## Machine verification state
verify_probe_batch.py verify ran against the raw dir and reported:
loss2m=5 loss15m=28 parked=8 wins=0 rows=33, producing probe/probe-verify-audit.json
and probe/new-rows.cache (33 strict rows, sha256
bb4097963136970f465a16ab615317c87cbc767d9f17bf687a16399cea6a9048).
The locally generated audit JSON and new-rows.cache publish and the
fail-closed union merge (base merged-exact-s5-after-class-excl-1.cache =
bb4495e0, 5,793 rows + 33 new rows, expected 5,826) are still PENDING: the
sandbox execution environment went temporarily unavailable right at the merge
step. Both artifacts are deterministic reruns from the published raws and
published merge base, so the next session can regenerate them byte-exactly
without any unrecoverable local state.

## What is NOT claimed
- The fourth-cost class 1297107061427929088:0 is NOT closed: it carries 100
  unknown S5 children; this pass decided 33 of the 41 keys this lane claimed;
  the 57 shared children were never claimed by this lane, and the 8 parked
  keys stay UNKNOWN.
- No WIN was found anywhere in the batch; no witness; no cache WIN row.
- The 11x11 empty board, the two-stone root {60,27}, and third moves 100/108
  remain UNKNOWN. Nodes and verdict counts are per-key solver facts, never
  board-level verdicts.
