# n11 sixth-cost k01/k03 third-implementation verdict re-verification: single-owner note (2026-11-22)

Declared: 2026-11-22T00:41Z (lane: the n11 long-term lane; this session inherits the
sixth-cost/third-cost exclusive-probe program and the third-implementation
re-verification program of ceb4eed71/ea73c3e3/451e0fe8).
HEAD at the moment of this note's composition: `51d4fa71556bd47cff2d4ea95eeb604f904d6b16`
(latest main at 00:41Z, s4bd fresh-corpus-regen resume checkpoint, disjoint from every
path this lane touches).

## Scope: the fresh declaration the published k03 checkpoint explicitly requires

The published sixth-cost resumption checkpoint README states that the concurrent
third-implementation lane "did not include k03 at its declaration time and its program
extends only with a fresh declaration". This note is that fresh declaration. Target
rows: the two unconsumed sixth-cost resumption-batch rows that have NO
third-implementation reproduction yet (k02, the parked pair, and the four legacy
two-target rows are already covered by ea73c3e3):

- PRIMARY: k03 `10376293541461626880:65792` (stones 5, legal 81; replica raw
  WIN(1), nodes 9,255,414 at 15M, three cold runs identical) - the only unconsumed
  WIN raw of the n11 exclusive-probe program without an independent
  third-implementation verdict. Row spec:
  `target,0,5,10376293541461626880,65792,81,0,0,0,0,0`.
- SECONDARY: k01 `1297036692683751424:1114112` (stones 5, legal 87; replica raw
  LOSS(2), nodes 10,369,650 at 15M, determinism pair identical) - the batch's only
  solved-LOSS row; completing it gives all three rows of the resumption batch
  an independent implementation's verdict.

Inputs are consumed ONLY from sha-pinned published sources (git-commit-fixed raw
fetches, byte-compared against the publishing lane's own pins where published):
k03/k01 input CSVs and all six replica raws from
`research/experiments/n11-sixthcost-class-s5-exclusive-probe-10376293541461626880-20261121/`
(pinned to `51d4fa71` at fetch time), the fixed third implementation
`third_impl.js` sha256
`08ea958ff59c3234ec5ac55c5c40689bd0999a34e101a88ea0546800cc4a1998` and
`verify_tbl.js` sha256 `c8c52528f70b3a9b438edc3feb4e432fbe705d6be21650383d3955efc6790251`
(experiment dir of ea73c3e3, its own MANIFEST pins re-verified on this host), and the
pinned replica `jsreplay.js` sha256
`845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df` (verify_tbl
dependency only). No corpus, cache, or quarantine file is modified.

## Acceptance conditions (fail-closed)

- A1 New experiment dir
  `research/experiments/n11-sixthcost-k01-k03-thirdimpl-verdict-reverification-20261122/`
  only; new session log under `research/log/`; no edits to any pre-existing file.
- C1 Calibration on this host before any target row: `verify_tbl.js` equality
  (forbidden quads 95,670 == replica 95,670; 195,044 triples, 0 mismatches), plus a
  host anchor row: legacy W2 `10376293541461626880:131328` must reproduce WIN(1)
  with expansions 7,583,990 (the published ea73c3e3 witness value) before k03/k01
  outputs count.
- C2 k03 verdict-level expectation: WIN(1) (replica raw nodes 9,255,414 are the
  replica's own count; third-impl expansion counts are ONLY compared across the
  third implementation's own cold runs, never to the replica's node count).
  Determinism: at least two full cold runs of third_impl on the k03 row with
  identical (result, expansions, ttHits), plus one `--verify-legal=1` run whose
  (result, expansions) must equal the cold runs.
- C3 k01 verdict-level expectation: LOSS(2). Determinism: at least two full cold
  runs with identical (result, expansions, ttHits).
- C4 Negative controls (fail-closed input gates, both must GATE_FAIL and write
  nothing into the agreement table): declared legal 82 (vs derived 81) on k03;
  declared stones 6 on k03.
- C5 Any WIN/LOSS disagreement is a hard stop: publish the raw outputs, no
  interpretation in this session, hand the divergence to the scrutiny owner.
- C6 No verdict is consumed: no cache increment, no chain merge, no class-status
  change, no coverage statement, no new claimed key, no selector run. The remaining
  delegated C++ second-implementation gate for k01/k02/k03
  (`cpp/solvers/kyouen_dfpn_root.cpp` sha256 `9193f5b6...` at 15M) is UNCHANGED;
  this re-verification is additional cross-implementation evidence only.
  Node/expansion counts are never read as verdicts. **The standard 11x11 empty
  board, the two-stone root {60,27}, and third moves {100,108} remain UNKNOWN
  throughout.**

## Not-do

- No K item, no knowledge README edit (verdict-unconsumed cross-check, following
  the ceb4eed71/ea73c3e3/451e0fe8 lane convention).
- No selector execution, no new keys, no k04..k43 starts (that batch stays halted
  by its own pre-registered stop rule; resuming it needs its own fresh declaration).
- No edits to the third-implementation experiment dir of ea73c3e3/451e0fe8.

## Disjointness

- A concurrent run of the bankfull thirdimpl follow-up (its declared optional
  stretch-37 item; local kit writes observed 00:29-00:30Z) is active on
  `out/stretch-37/` inside the ea73c3e3/451e0fe8 experiment dir; this lane touches
  none of those paths (new dir only).
- Other lanes on latest main since 00:15Z: n11-s4bd fresh corpus regen (pass2
  determinism checkpoints), six-row (6,6)/(6,7) lanes, five-row sd sweep, seven-row
  m69 - all disjoint from this lane's paths.
- Per-execution re-fetch of latest main precedes every push of this lane.

## Environment facts

- Node v22.20.0, Python 3.12.x, 2 cores, serial execution (one row at a time).
- No C++ toolchain (g++/gcc/clang absent, re-verified this session); package
  installation forbidden; delegated C++ gate unchanged.
- Unauthenticated raw fetches (raw.githubusercontent.com) working this session,
  pinned to fixed commit shas for every input.
