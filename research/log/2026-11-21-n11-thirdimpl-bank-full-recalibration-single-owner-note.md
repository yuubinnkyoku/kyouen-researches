# n11 third-implementation bank full-band recalibration: single-owner note (2026-11-21)

Declared: 2026-11-21T22:40Z (lane: the n11 long-term lane that published the
sixth-cost third-implementation verdict re-verification
`ceb4eed71`/`ea73c3e3` and the sixth-cost/third-cost exclusive probe batches).
HEAD at the moment of this note's composition: `5c4cfca9f267bb849475ae25d9f03e3f7a182ec0`.
The immediate pre-push re-fetch observed HEAD `0b2a6466fa43cea5c5e956a020789476f1801af7`
(22:33:17Z, five-row q6/q5 sd(4,3)/(3,4) partial-sweep declaration, non-n11, disjoint
from every path this lane touches; re-fetch included in the push gate).

## Scope: the deferred follow-up of the third-implementation lane

The `ea73c3e3` session log defers two items to follow-up runs of this lane. This
session takes the first one: **bank full-band recalibration**.

- Fixed third implementation `third_impl.js` (sha256
  `08ea958ff59c3234ec5ac55c5c40689bd0999a34e101a88ea0546800cc4a1998`,
  byte-equal to the published MANIFEST pin, re-verified on this host) against the
  published probe-13 chain cache `merged-exact-s5-after-js-probe-13.cache` (sha256
  `60e0dc3476920d4e99043dd4f132398ea72e4dfdcd9f3dbb8fc686ba65bc28c6`, 5,756
  s5verdict rows, stones 5: 158 WIN / 5,598 LOSS).
- Bank set = all 158 WIN rows + a 40-row LOSS sample (`run_bank.py` order:
  `--wins all --loss-sample 40`). The 14 WIN rows already agreed clean in
  `out/bank-fixed-A/` are seed-copied into the new outdir so the idempotent runner
  continues rather than re-proving them; the 2 wall-inconclusive sample rows
  (runlimit at 55s, 18.5M/19.0M expansions) are re-run. Per-row wall cap escalated
  55s -> 90s for this batch (honest rationale: the two sample runlimit rows had not
  finished at 55s; the sample's clean rows all finished within 48s).
- Optional stretch if wall-clock allows and only after the bank batch lands: the 37
  third-cost exclusive LOSS rows of `merged-exact-s5-after-class-excl-1.cache`
  (sha256 `bb4495e0...`) verdict-level (stretch item 4 of the lane declaration,
  unchanged and still optional).

## Acceptance conditions (fail-closed; A1-A5 of the lane note unchanged, plus)

- C1 Calibration on this host before any bank row counts (already executed this
  session, raw lines preserved in the kit and published with the results):
  `verify_tbl.js` quad equality (replica 95,670 == mine 95,670; 195,044 triples,
  0 mismatches) AND anchor w1 `10376293541461626880:67109120` reproducing WIN(1)
  with expansions 11,663,909, ttHits 6,284,843, ttOverwrites 7,469,605 identical to
  the published witness rows (wall time only differs: 33.80s vs 34.24/34.43s).
- C2 One clean or aborted run per bank row (the published bank-sample protocol);
  each output file records `expect,<verdict>,<nodes>` plus the full third_impl
  stdout row. runlimit rows are never reported as agreement.
- C3 Any WIN/LOSS disagreement between third_impl and the cache row is a hard stop
  for the batch (A3 of the lane note): no interpretation in the same session;
  publish the raw outputs and hand the divergence to the next run / the scrutiny
  owner.
- C4 No verdict is consumed, no cache increment, no chain merge, no class-status
  change, no coverage or third-move statement. Nodes/expansions are never read as
  verdicts. **The standard 11x11 empty board, the two-stone root {60,27}, and
  third moves {100,108} remain UNKNOWN throughout.**
- C5 The pre-registered adoption gate for WIN rows is unchanged (delegated C++
  second-implementation verification, `cpp/solvers/kyouen_dfpn_root.cpp` sha256
  `9193f5b6...` at 15M). This recalibration is additional cross-implementation
  evidence only; adoption/judgment stays with the scrutiny owner.

## Not-do

- No K item and no knowledge README edit (measurement-level cross-check, following
  this lane's convention for verdict-unconsumed batches).
- No shared-file edits: only new files under this lane's own experiment dir
  (`out/bank-full-B/` and a run summary) plus a README appendix to the lane's own
  experiment README, a new session log under `research/log/`, and an additive
  MANIFEST.sha256 update of this experiment dir.

## Disjointness

Lanes active on latest main since 22:06Z (five-row q6/q5 m21/m25-species surgery
`5c4cfca9`/`c2010307`, seven-row q4 m69 batch 2 `c476182a`, six-row q4 m52
`4a314f4c`/`bf6030ad`) are non-n11 and touch none of this lane's paths. The n11
sixth-cost k03..k43 batch stays halted per its own stop rule; its keys are exactly
this bank's provenance rows and remain unconsumed. No new keys are claimed anywhere.

## Environment facts

- Node v22.20.0, Python 3.12.14, 2 cores, serial execution (one row at a time).
- Repo unauthenticated fetches (raw/api) remained unavailable in the last session;
  if that recurs, publish/fetch-back goes through the GitHub App tool path as before.
- No C++ toolchain; package installation forbidden (re-verified; delegated gate
  unchanged).
