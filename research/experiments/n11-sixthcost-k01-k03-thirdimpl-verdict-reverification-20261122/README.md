# n11 sixth-cost k01/k03 third-implementation verdict re-verification (2026-11-22)

## What this is

A fresh single-owner declaration (declared 2026-11-22T00:41Z,
`research/log/2026-11-22-n11-sixthcost-k01-k03-thirdimpl-verdict-single-owner-note.md`,
commit `53d8fe28`) extending the third-implementation verdict re-verification
program (`ea73c3e3`) to the two unconsumed sixth-cost resumption-batch rows that
had no independent third-implementation verdict yet: **k03 `10376293541461626880:65792`**
(the only unconsumed WIN raw of the n11 exclusive-probe program without a
third-impl reproduction) and **k01 `1297036692683751424:1114112`** (the batch's
only solved-LOSS row; completing it covers all three rows of the resumption batch).

The sixth-cost class `10376293541461626880:65536` (coverage {80, 84, 100, 108}) is
the published rank-6 live candidate class in the class-closure-priority
measurement; its WIN-elimination as a LOSS-completion route for third moves
{100, 108} is the documented motivation of the exclusive probe batch it belongs to
(see the pinned README of
`n11-sixthcost-class-s5-exclusive-probe-10376293541461626880-20261121`).

**No verdict is consumed here. No cache increment, no chain merge, no class-status
change, no coverage claim. The standard 11x11 empty board, the two-stone root
{60,27}, and its remaining third moves {100,108} remain UNKNOWN. Node/expansion
counts are never read as verdicts.** The delegated C++ second-implementation gate
(`cpp/solvers/kyouen_dfpn_root.cpp` sha256 `9193f5b6...` at 15M, targets k01/k02/k03)
is UNCHANGED and remains the pre-registered adoption gate; this experiment is
additional cross-implementation evidence only.

## Implementation and pins (all consumed inputs sha-pinned, byte-verified on this host)

- Fixed third implementation `third_impl.js` sha256
  `08ea958ff59c3234ec5ac55c5c40689bd0999a34e101a88ea0546800cc4a1998`
  (byte-equal copy of the ea73c3e3 publication, re-published here for
  self-containedness; the verifying MANIFEST is that experiment dir's).
- `verify_tbl.js` sha256
  `c8c52528f70b3a9b438edc3feb4e432fbe705d6be21650383d3955efc6790251` (same
  provenance; its replica dependency is `jsreplay.js` sha256
  `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`, consumed
  from the pinned lane kit at the absolute path hardcoded in the published
  verify_tbl.js).
- k03/k01 row specs and all six replica raws (three 15M k03 WIN rows + one 2M
  UNKNOWN k03 row + two 15M k01 LOSS rows) consumed at commit `51d4fa71` from
  `research/experiments/n11-sixthcost-class-s5-exclusive-probe-10376293541461626880-20261121/`,
  each byte-compared to the publishing lane's own sha256 pins; per-file pins are
  enforced inside `audit.py` (`repl_sha_*` gates).

## Results (all gates of the declaration PASS; `audit.py` 39/39)

| row (lo:hi, legal) | replica raw (published) | third_impl (this session) | runs | expansions | wall |
|---|---|---|---|---|---|
| k03 `10376293541461626880:65792`, 81 | WIN(1), nodes 9,255,414 @15M (x3) | **WIN(1)** | x3 (a, b, v=verify-legal) | 10,896,601 (identical x3) | 30.46 / 30.24 / 54.00s |
| k01 `1297036692683751424:1114112`, 87 | LOSS(2), nodes 10,369,650 @15M (x2) | **LOSS(2)** | x2 (a, b) | 12,033,330 (identical x2) | 34.13 / 33.96s |

- Verdict-level agreement with the replica raws on both rows (result 1 vs 1,
  2 vs 2). Third-impl expansion counts are compared ONLY across the third
  implementation's own cold runs (never to the replica's node counts; the two
  implementations count different quantities).
- Determinism: (result, expansions, ttHits, ttOverwrites) identical across all
  cold runs, including the `--verify-legal=1` run of k03 (derived legal masks
  node-identical to from-scratch legality at every visited node).
- C1 calibration on this host BEFORE any target row: `verify_tbl.js`
  forbidden-quad equality (replica 95,670 == mine 95,670; 195,044 triples,
  0 mismatches) and anchor w2 `10376293541461626880:131328` reproducing WIN(1)
  with expansions 7,583,990 == the published ea73c3e3 witness value (two
  executions, 21.57s / 21.40s, identical counts; the rc-annotated second
  execution is the one kept in `out/calib-anchor-w2.txt`).
- C4 fail-closed input gates, both GATE_FAIL with process exit status 1:
  declared legal 82 vs derived 81 on k03; declared stones 6 vs bits 5 on k03.
- `audit.py` (deterministic, byte-identical output across runs) re-verifies every
  gate from the raw files and exits 0 only if all 39 pass; negative (tamper)
  controls on full kit copies detect a k03 verdict flip (1 -> 2:
  `C2_k03_determinism_3runs_identical` + `C2_k03_win_verdict_level_vs_replica`)
  and a k01 expansions perturbation (`C3_k01_determinism_2runs_identical`),
  each failing closed with rc=1 (`out/audit-tamper-controls.txt`).

## Honest session notes

- `audit.py` had two parser bugs during this session (replay-row field offsets;
  `third,`-only line matcher over replica CSVs). Both were caught by the gates
  themselves failing (never by eyeball), both fixed before publication, and the
  published `audit-summary.json` is the output of the FIXED auditor. The raw
  output files were never edited between runs; all experiment raws predate the
  audit fixes.
- Anchor w2 was first run through `tee` (wall 21.57s), then re-run without the
  pipeline to capture the process rc (wall 21.40s); both runs identical in
  (result, expansions) and the rc=0 file is the kept calibration raw.
- Serial execution, one node process at a time, 2 cores.

## Reproduce

```
node verify_tbl.js                       # C1a gate (needs pinned jsreplay.js)
node third_impl.js --lo=10376293541461626880 --hi=131328 --stones=5 --legal=80 \
  --row=w2-anchor --cap=400000000 --wallcap=270 --memo-power=22    # C1b anchor
node third_impl.js --lo=10376293541461626880 --hi=65792 --stones=5 --legal=81 \
  --row=k03-a  --cap=400000000 --wallcap=270 --memo-power=22        # k03 cold
node third_impl.js --lo=1297036692683751424 --hi=1114112 --stones=5 --legal=87 \
  --row=k01-a  --cap=400000000 --wallcap=270 --memo-power=22        # k01 cold
node third_impl.js --lo=10376293541461626880 --hi=65792 --stones=5 --legal=82 \
  --row=ng1 --cap=4000000 --wallcap=60 --memo-power=22    # GATE_FAIL expected, rc=1
python3 audit.py                        # 39/39 gates, rc=0, deterministic
```

Inputs (row specs): `input/k03.input.csv`, `input/k01.input.csv`
(`target,0,5,<lo>,<hi>,<legal>,0,0,0,0,0`).

## Status guard

The standard 11x11 empty board, the two-stone root {60,27}, and its remaining
third moves {100,108} remain UNKNOWN throughout. Expansion counts, budgets, wall
times and solved counts are never verdicts. Adoption of the unconsumed sixth-cost
batch rows stays with the scrutiny owner under the unchanged delegated C++
second-implementation gate.
