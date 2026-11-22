# Session log: n11 sixth-cost k01/k03 third-implementation verdict re-verification (2026-11-22)

Lane: the n11 long-term lane (sixth-cost/third-cost exclusive-probe program and the
third-implementation re-verification program). All work this session was within the
fresh single-owner declaration
`research/log/2026-11-22-n11-sixthcost-k01-k03-thirdimpl-verdict-single-owner-note.md`
(composition HEAD `51d4fa71`, pushed at commit `53d8fe28`).

## Why this session took this item

At session start, latest main (`c3c62fd4`, thirdimpl bank full-band recalibration
part4 + byte-fidelity repair) showed the bank recalibration published: 198/198 rows
verdict-level agree vs the probe-13 cache. A concurrent sibling run was observed
live on the declared optional stretch-37 item (local kit writes at 00:29-00:30Z), so
this session avoided the thirdimpl/bank paths entirely. The one remaining item on
the sixth-cost adoption critical path that this sandbox CAN execute (no C++
toolchain exists; the C++ second-implementation gate stays delegated) was the
explicitly-required fresh declaration extending the third-implementation
re-verification to k03: the only unconsumed WIN raw of the n11 exclusive-probe
program without an independent third-implementation verdict. k01 (the batch's only
solved-LOSS row) was added as the secondary row, completing independent
third-impl coverage of all three rows of the第六-cost resumption batch
(k01 LOSS / k02 WIN / k03 WIN; k02, the parked pair, and the four legacy
two-target rows were already covered by `ea73c3e3`).

## What ran (all on byte-pinned inputs; serial, one node process at a time)

- C1a `verify_tbl.js`: replica quads 95,670 == mine 95,670; 195,044 triples,
  0 mismatches.
- C1b host anchor w2 `10376293541461626880:131328`: WIN(1), expansions 7,583,990 ==
  the published ea73c3e3 witness value (two executions 21.57s / 21.40s identical
  counts; the rc-annotated one is the kept raw).
- k03 `10376293541461626880:65792` (legal 81), cap 400M, wallcap 270, memo 2^22:
  **WIN(1), expansions 10,896,601, ttHits 5,996,958, ttOverwrites 6,702,297,
  identical on three cold runs** (a 30.46s, b 30.24s, `--verify-legal=1` 54.00s;
  derived legal masks node-identical to from-scratch legality at every visited
  node in the third run). Verdict-level agreement with the published replica raw
  WIN(1) nodes 9,255,414 @15M (x3 cold, pinned shas re-verified).
- k01 `1297036692683751424:1114112` (legal 87): **LOSS(2), expansions 12,033,330,
  ttHits 6,620,470, ttOverwrites 7,839,026, identical on two cold runs**
  (34.13 / 33.96s). Verdict-level agreement with the published replica raw LOSS(2)
  nodes 10,369,650 @15M (x2, pinned shas re-verified).
- C4 fail-closed input gates: declared legal 82 vs derived 81 -> GATE_FAIL rc=1;
  declared stones 6 vs bits 5 -> GATE_FAIL rc=1.
- `audit.py` (deterministic, published in this experiment dir): **39/39 gates
  PASS**, byte-identical output across runs; tamper negative controls on full kit
  copies detect a k03 verdict flip and a k01 expansion perturbation, each failing
  closed rc=1 with the expected gate names.

## Honest facts

- `audit.py` had two parser bugs mid-session (replay-row field offsets; a
  `third,`-only line matcher over replica CSVs). Both were caught by the gates
  themselves failing (never by eyeball), fixed before publication, and the
  published `out/audit-summary.json` is the FIXED auditor's output. No experiment
  raw was edited at any time.
- Import-coupling note: the published `verify_tbl.js` requires the pinned
  `jsreplay.js` replica from an absolute lane-kit path (byte-pinned
  `84585617...`, re-verified). Reproduction on another host needs that file
  there, or the pin re-pointed; the sha gate inside `audit.py` enforces the pin
  wherever it runs.
- Expansion counts differ from replica node counts by design (the two
  implementations count different quantities); agreement is verdict-level only,
  and determinism is only ever claimed across the same implementation's cold runs.

## Publication record

- Declaration: commit `53d8fe28` (HEAD-before-push observed `51d4fa71`).
- Experiment dir
  `research/experiments/n11-sixthcost-k01-k03-thirdimpl-verdict-reverification-20261122/`
  (18 files incl. README, byte-identical script copies, inputs, 12 out/ raws and
  `MANIFEST.sha256`): commit `90f38c95` (HEAD-before-push observed `53d8fe28`,
  still main tip at push time). **Fetch-back: 18/18 byte-identical by cmp against
  the commit-fixed raw URLs (no trailing-newline stripping observed this session).**
- This session log: commit (see below).

## Claims made / not made

- Claimed: third-implementation verdict-level reproduction of the published
  sixth-cost k03 WIN raw and k01 LOSS raw, with pre-declared determinism and
  fail-closed gates, 39/39 machine-audited.
- NOT claimed: no verdict consumption, no cache increment, no chain merge, no
  class-status change (the sixth-cost class `10376293541461626880:65536` stays
  UNKNOWN with 2 unconsumed fresh WIN children), no coverage change (secured
  third-move coverage stays 117/119, remaining {100, 108}), no k04..k43 starts
  (that batch stays halted by its own pre-registered stop rule; resuming it needs
  its own fresh declaration), no root or board statement.
- **The standard 11x11 empty board, the two-stone root {60,27}, and its remaining
  third moves {100,108} remain UNKNOWN. Node/expansion counts are never verdicts.**
- The delegated C++ second-implementation gate for k01/k02/k03
  (`cpp/solvers/kyouen_dfpn_root.cpp` sha256 `9193f5b6...` at 15M) is UNCHANGED;
  adoption/judgment stays with the scrutiny owner. With this session, every
  unconsumed WIN raw of the n11 exclusive-probe program (parked pair, k02, k03)
  and the parked/batch LOSS rows now has both replica and third-implementation
  agreement, pending that C++ gate.

## Resume (next runs)

1. The C++ gate remains the top blocker for consuming k02/k03 (and the parked
   pair); it needs a host with the pinned toolchain, the scrutiny owner's call.
2. A sibling run is live on the stretch-37 item; avoid the thirdimpl bank paths
   until it publishes.
3. k04..k43 of the sixth-cost batch stay claimable under a fresh declaration
   (selector re-run + disjoint check precedes any key start), but more WINs add
   little while k02/k03 adoption is pending; the sibling lanes' fresh-corpus
   regen (s4bd) and the frontier census provide the current next-best measurements.
