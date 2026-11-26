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

## k04 addendum: third-implementation re-verification of the fresh second-resumption WIN row (same session, later this day)

Declared separately (single-owner WIN-row precedent) in
`research/log/2026-11-22-n11-sixthcost-k04-thirdimpl-verdict-single-owner-note.md`
(commit `d33d752b`), extending this dir's program to **k04
`10376293541461626888:65536`** (stones 5, legal 83): the third fresh WIN raw of
the n11 exclusive-probe program, published minutes earlier at commit
`cb7ffe05` (probe-lane raw: 2M UNKNOWN, then WIN(1) nodes 9,433,024 at 15M,
three cold runs identical). Implementation and pins are unchanged from the
parent program above; C1 calibration is honestly reused (the calibration raws
in `out/calib-*.txt` are from THIS host THIS session, per the addendum note).

| row (lo:hi, legal) | replica raw (published at `cb7ffe05`) | third_impl (this addendum) | runs | expansions | wall |
|---|---|---|---|---|---|
| k04 `10376293541461626888:65536`, 83 | WIN(1), nodes 9,433,024 @15M (x3); 2M UNKNOWN (nodes 2,000,000, result 0) | **WIN(1)** | x3 (a, b, v=verify-legal) | 11,020,407 (identical x3; ttHits 6,092,599; ttOverwrites 6,826,103; quads 95,670) | 31.05 / 30.82 / 54.92s |

- Verdict-level agreement with the replica raws (result 1 vs 1). Expansion
  counts are compared only across the third implementation's own cold runs,
  never against the replica's node counts (the implementations count
  different quantities).
- C4 fail-closed input gates on k04, both GATE_FAIL with process exit status
  1: declared legal 84 vs derived 83; declared stones 6 vs bits 5.
- The four replica raw copies consumed at `cb7ffe05` are re-published inside
  this dir at `out/k04-replica-raws/` so the auditor is self-contained; each is
  pinned by its probe-lane sha256 inside `audit_k04.py` (`repl_sha_*` gates) and
  byte-compared against the just-published blobs before this push.
- `audit_k04.py` is a separate auditor so the published `audit.py` stays
  byte-frozen. It re-verifies every addendum gate (31) from the raw files,
  resolves the pinned third_impl.js / verify_tbl.js / jsreplay.js from either
  this dir + the probe dir (repo checkout) or the executable kit, is
  deterministic (byte-identical output across runs), and exits 0 only if all
  gates pass. Negative (tamper) controls on full kit copies detect a k04
  verdict flip (1 -> 2: `C2_k04_determinism_3runs_identical` +
  `C2_k04_win_verdict_level_vs_replica`) and a replica-raw nodes edit
  (`repl_sha_*` + `repl_row_*` + `repl_k04_win_3runs_unanimous`), each failing
  closed with rc=1 (`out/audit-tamper-controls-k04.txt`).
- Honest audit note: this addendum's auditor had a generation slip before its
  first execution (a malformed determinism-check expression left in
  `C2_k04_determinism_3runs_identical`); it was caught and removed BEFORE any
  run, no raw predates or postdates any audit edit, and the published
  `out/audit-k04-summary.json` is the output of the clean auditor.
- No verdict is consumed. The delegated pinned C++ gate for k04
  (`cpp/solvers/kyouen_dfpn_root.cpp` sha256 `9193f5b6...`,
  `target,0,5,10376293541461626888,65536,83,0,0,0,0,0` @15,000,000, expected
  result 1, nodes 9,433,024) is recorded and UNCHANGED; adoption stays with the
  scrutiny owner. **The standard 11x11 empty board, the two-stone root {60,27},
  and its remaining third moves {100,108} remain UNKNOWN. Node/expansion counts
  are never verdicts.**

### Reproduce (addendum)

```
node third_impl.js --lo=10376293541461626888 --hi=65536 --stones=5 --legal=83 \
  --row=k04-a --cap=400000000 --wallcap=270 --memo-power=22   # cold run
node third_impl.js --lo=10376293541461626888 --hi=65536 --stones=5 --legal=83 \
  --row=k04-v --verify-legal=1 --cap=400000000 --wallcap=270 --memo-power=22
node third_impl.js --lo=10376293541461626888 --hi=65536 --stones=5 --legal=84 \
  --row=ng1-k04 --cap=4000000 --wallcap=60 --memo-power=22  # GATE_FAIL, rc=1
node third_impl.js --lo=10376293541461626888 --hi=65536 --stones=6 --legal=83 \
  --row=ng2-k04 --cap=4000000 --wallcap=60 --memo-power=22  # GATE_FAIL, rc=1
python3 audit_k04.py                 # 31/31 gates, rc=0, deterministic
```

Input row spec: `input/k04.input.csv`
(`target,0,5,10376293541461626888,65536,83,0,0,0,0,0`).

## k05 addendum: third-implementation re-verification of the third-resumption WIN row (new host, 2026-11-26)

Declared separately (single-owner WIN-row precedent) in
`research/log/2026-11-26-n11-sixthcost-k05-thirdimpl-verdict-single-owner-note.md`,
extending this dir's program to **k05 `10376293541461757952:65536`**
(stones 5, legal 88): the fifth fresh WIN raw of the n11 exclusive-probe
program, published at commit `704cb3ef` (probe-lane raw: 2M UNKNOWN
nodes 2,000,000 result 0, then WIN(1) nodes 13,397,611 at 15M, three cold
runs identical). Implementation and pins are unchanged from the parent
program above. This addendum was executed on a NEW host (a fresh sandbox
without a C++ toolchain), so the C1 calibration was re-executed THIS
session on THIS host rather than reusing the 2026-11-22 calibration
raws (honest non-reuse; new raws below).

| row (lo:hi, legal) | replica raw (published at `704cb3ef`) | third_impl (this addendum) | runs | expansions | wall |
|---|---|---|---|---|---|
| k05 `10376293541461757952:65536`, 88 | WIN(1), nodes 13,397,611 @15M (x3); 2M UNKNOWN (nodes 2,000,000, result 0) | **WIN(1)** | x3 (a, b, v=verify-legal) | 15,949,585 (identical x3; ttHits 8,391,212; ttOverwrites 11,755,281; quads 95,670) | 44.44 / 45.13 / 80.42s |

- Verdict-level agreement with the replica raws (result 1 vs 1). Expansion
  counts are compared only across the third implementation's own cold runs,
  never against the replica's node counts (the implementations count
  different quantities).
- C1 calibration re-executed on THIS host THIS session:
  `out/k05-calib-verify-tbl.txt` (replica 95,670 == mine 95,670; 195,044
  triples, 0 mismatches, rc=0) and anchor w2
  `10376293541461626880:131328` reproducing WIN(1) with expansions
  7,583,990 == the published ea73c3e3 witness value (two executions,
  22.51s rc-annotated kept in `out/k05-calib-anchor-w2.txt`, 22.17s in
  `out/k05-calib-anchor-w2-run2.txt`; identical counts both runs).
- C4 fail-closed input gates on k05, both GATE_FAIL with process exit status
  1: declared legal 89 vs derived 88; declared stones 6 vs bits 5.
- The four replica raw copies consumed at `704cb3ef` are re-published inside
  this dir at `out/k05-replica-raws/` so the auditor is self-contained; each
  is pinned by its probe-lane sha256 inside `audit_k05.py` (`repl_sha_*`
  gates) and byte-compared against the just-published blobs before this push.
- `audit_k05.py` is a separate auditor so the published `audit.py` and
  `audit_k04.py` stay byte-frozen. It re-verifies every addendum gate (31)
  from the raw files, resolves the pinned third_impl.js / verify_tbl.js /
  jsreplay.js from either this dir + the probe dir (repo checkout) or the
  executable kit, is deterministic (byte-identical output across runs), and
  exits 0 only if all gates pass. Negative (tamper) controls on full kit
  copies detect a k05 verdict flip (1 -> 2:
  `C2_k05_determinism_3runs_identical` + `C2_k05_win_verdict_level_vs_replica`)
  and a replica-raw nodes edit (`repl_sha_*` + `repl_row_*` +
  `repl_k05_win_3runs_unanimous`), each failing closed with rc=1
  (`out/audit-tamper-controls-k05.txt`; kit restores byte-verified, final
  clean control rc=0 byte-identical to baseline).
- Honest note: the tamper-control log was reassembled from the executed
  control transcript after an inline gate-listing helper printed a
  SyntaxError to the transcript; the rc values and failed-gate lists in the
  published log come directly from the control JSON outputs and all
  restores were byte-verified. No raw predates or postdates any audit edit;
  the published `out/audit-k05-summary.json` is the output of the clean
  auditor.
- No verdict is consumed. The delegated pinned C++ gate for k05
  (`cpp/solvers/kyouen_dfpn_root.cpp` sha256 `9193f5b6...`,
  `target,0,5,10376293541461757952,65536,88,0,0,0,0,0` @15,000,000, expected
  result 1, nodes 13,397,611) is recorded and UNCHANGED; adoption stays with
  the scrutiny owner. **The standard 11x11 empty board, the two-stone root
  {60,27}, and its remaining third moves {100,108} remain UNKNOWN.
  Node/expansion counts are never verdicts.**

### Reproduce (addendum k05)

```
node verify_tbl.js                       # C1a gate (needs pinned jsreplay.js)
node third_impl.js --lo=10376293541461626880 --hi=131328 --stones=5 --legal=80 \
  --row=w2-anchor-k05 --cap=400000000 --wallcap=270 --memo-power=22    # C1b anchor
node third_impl.js --lo=10376293541461757952 --hi=65536 --stones=5 --legal=88 \
  --row=k05-a --cap=400000000 --wallcap=270 --memo-power=22        # k05 cold
node third_impl.js --lo=10376293541461757952 --hi=65536 --stones=5 --legal=88 \
  --row=k05-b --cap=400000000 --wallcap=270 --memo-power=22        # k05 cold
node third_impl.js --lo=10376293541461757952 --hi=65536 --stones=5 --legal=88 \
  --row=k05-v --verify-legal=1 --cap=400000000 --wallcap=270 --memo-power=22
node third_impl.js --lo=10376293541461757952 --hi=65536 --stones=5 --legal=89 \
  --row=ng1-k05 --cap=4000000 --wallcap=60 --memo-power=22  # GATE_FAIL, rc=1
node third_impl.js --lo=10376293541461757952 --hi=65536 --stones=6 --legal=88 \
  --row=ng2-k05 --cap=4000000 --wallcap=60 --memo-power=22  # GATE_FAIL, rc=1
python3 audit_k05.py                 # 31/31 gates, rc=0, deterministic
```

Input row spec: `input/k05.input.csv`
(`target,0,5,10376293541461757952,65536,88,0,0,0,0,0`).

## k06/k07/k08 addendum: third-implementation re-verification of the three fourth-resumption rows (new host, 2026-11-26)

Declared separately (single-owner, fresh-declaration program rule) in
`research/log/2026-11-26-n11-sixthcost-k06-k07-k08-thirdimpl-verdict-single-owner-note.md`
(push `b9dc2bb3`), extending this dir's program to the three resolved rows of the
fourth-resumption chain with no independent third-implementation verdict yet:
**k06 `10376293541462675456:65536`** (stones 5, legal 89) and
**k07 `10376293542535368704:65536`** (stones 5, legal 87), the batch's second and
third solved-LOSS rows (published probe raws at `585d99ef` / `3780887d`:
k06 2M UNKNOWN then 15M pair LOSS(2) nodes 8,182,231; k07 2M determinism pair
LOSS(2) nodes 1,419,823 plus a 15M cold pair with identical counts), and
**k08 `10376293610182148096:68719476736`** (stones 5, legal 89), the batch's
fifth fresh WIN row (published at `575a58fe`: 2M UNKNOWN then a 15M triple all
WIN(1) nodes 6,195,897; first non-65536 key_hi row of the selection).
Implementation and pins are unchanged from the parent program above. This
addendum ran on a NEW host (fresh sandbox, no C++ toolchain), so the C1
calibration was re-executed THIS session on THIS host rather than reusing any
earlier calibration raws (honest non-reuse; new raws below).

| row (lo:hi, legal) | replica raw (published) | third_impl (this addendum) | runs | expansions | wall |
|---|---|---|---|---|---|
| k06 `10376293541462675456:65536`, 89 | LOSS(2), nodes 8,182,231 @15M (x2); 2M UNKNOWN (nodes 2,000,000, result 0) | **LOSS(2)** | x2 (a, b) | 9,474,431 (identical x2; ttHits 5,163,124; ttOverwrites 5,280,127; quads 95,670) | 27.38 / 28.03s |
| k07 `10376293542535368704:65536`, 87 | LOSS(2), nodes 1,419,823 (2M pair x2 + 15M pair x2, all four identical) | **LOSS(2)** | x2 (a, b) | 1,608,994 (identical x2; ttHits 935,234; ttOverwrites 169; quads 95,670) | 4.83 / 4.84s |
| k08 `10376293610182148096:68719476736`, 89 | WIN(1), nodes 6,195,897 @15M (x3); 2M UNKNOWN (nodes 2,000,000, result 0) | **WIN(1)** | x3 (a, b, v=verify-legal) | 7,243,596 (identical x3; ttHits 3,873,045; ttOverwrites 3,050,565; quads 95,670) | 19.88 / 19.77 / 35.67s |

- Verdict-level agreement with the replica raws on all three rows (2 vs 2, 2 vs 2,
  1 vs 1). Expansion counts are compared only across the third implementation's
  own cold runs, never against the replica's node counts (the implementations
  count different quantities).
- C1 calibration re-executed on THIS host THIS session:
  `out/calib-verify-tbl-k06k07k08.txt` (replica 95,670 == mine 95,670; 195,044
  triples, 0 mismatches, rc=0) and anchor w2
  `10376293541461626880:131328` reproducing WIN(1) with expansions 7,583,990 ==
  the published ea73c3e3 witness value on two executions (21.57s kept in
  `out/calib-anchor-w2-k06k07k08.txt`, 21.65s in
  `out/calib-anchor-w2-run2-k06k07k08.txt`; identical counts both runs).
- C4 fail-closed input gates per row, all GATE_FAIL with process exit status 1:
  k07 row legal 88 vs derived 87; k06/k08 legal 90 vs derived 89; stones 6 vs
  bits 5 (`out/neg-gate-*.txt`).
- The eleven replica raw copies consumed at HEAD `dc7f36e1` are re-published
  inside this dir at `out/k06-replica-raws/`, `out/k07-replica-raws/` and
  `out/k08-replica-raws/` so the auditor is self-contained; each is pinned by
  its probe-lane sha256 inside `audit_k06k07k08.py` (`repl_sha_*` gates) and
  byte-compared against the republished blobs before this push.
- `audit_k06k07k08.py` is a separate auditor so the published audit.py,
  audit_k04.py and audit_k05.py stay byte-frozen. It re-verifies every addendum
  gate (82: 11 repl_sha + 11 repl_row + 5 repl unanimity/UNKNOWN + 3 C1 + 28
  third-row + 12 C2 + 6 C4 + 3 script pins + 3 input-spec pins), resolves
  the pinned third_impl.js / verify_tbl.js / jsreplay.js
  from either this dir + the probe dir (repo checkout) or the executable kit
  layout, is deterministic (byte-identical output across runs in a fixed
  layout; the only layout-dependent bytes are resolved-path detail strings,
  normalized-identical across layouts), and exits 0 only if all gates pass.
  Negative (tamper) controls on full kit copies detect a k08 verdict flip
  (1 -> 2: `C2_k08_determinism_3runs_identical` +
  `C2_k08_win_verdict_level_vs_replica`) and a k06 replica-raw nodes edit
  (`repl_sha_*` + `repl_row_*` + `repl_k06_loss_2runs_unanimous`), each failing
  closed with rc=1, kit restores byte-verified, final clean control rc=0
  (`out/audit-tamper-controls-k06k07k08.txt`).
- No verdict is consumed. The delegated pinned C++ gates for k06/k07/k08
  (cpp/solvers/kyouen_dfpn_root.cpp sha256 `9193f5b6...`, expectations as
  published in output/win-finding-ifadopted-k08.json: k06 2/8,182,231 @15M;
  k07 2/1,419,823 @>=1.42M; k08 1/6,195,897 @15M) are recorded and UNCHANGED;
  they could NOT be run on this host (no C++ toolchain in this sandbox) and
  remain delegated to the scrutiny owner; adoption stays with the scrutiny
  owner. **The standard 11x11 empty board, the two-stone root {60,27}, and its
  remaining third moves {100,108} remain UNKNOWN. Node/expansion counts are
  never verdicts.**

### Reproduce (addendum k06/k07/k08)

```
node verify_tbl.js                       # C1a gate (needs pinned jsreplay.js)
node third_impl.js --lo=10376293541461626880 --hi=131328 --stones=5 --legal=80 \
  --row=w2-anchor-k06k07k08 --cap=400000000 --wallcap=270 --memo-power=22   # C1b anchor
node third_impl.js --lo=10376293541462675456 --hi=65536 --stones=5 --legal=89 \
  --row=k06-a --cap=400000000 --wallcap=270 --memo-power=22        # k06 cold
node third_impl.js --lo=10376293541462675456 --hi=65536 --stones=5 --legal=89 \
  --row=k06-b --cap=400000000 --wallcap=270 --memo-power=22        # k06 cold
node third_impl.js --lo=10376293542535368704 --hi=65536 --stones=5 --legal=87 \
  --row=k07-a --cap=400000000 --wallcap=270 --memo-power=22        # k07 cold
node third_impl.js --lo=10376293542535368704 --hi=65536 --stones=5 --legal=87 \
  --row=k07-b --cap=400000000 --wallcap=270 --memo-power=22        # k07 cold
node third_impl.js --lo=10376293610182148096 --hi=68719476736 --stones=5 --legal=89 \
  --row=k08-a --cap=400000000 --wallcap=270 --memo-power=22        # k08 cold
node third_impl.js --lo=10376293610182148096 --hi=68719476736 --stones=5 --legal=89 \
  --row=k08-b --cap=400000000 --wallcap=270 --memo-power=22        # k08 cold
node third_impl.js --lo=10376293610182148096 --hi=68719476736 --stones=5 --legal=89 \
  --row=k08-v --verify-legal=1 --cap=400000000 --wallcap=270 --memo-power=22
node third_impl.js --lo=10376293541462675456 --hi=65536 --stones=5 --legal=90 \
  --row=ng1-k06 --cap=4000000 --wallcap=60 --memo-power=22  # GATE_FAIL, rc=1
node third_impl.js --lo=10376293541462675456 --hi=65536 --stones=6 --legal=89 \
  --row=ng2-k06 --cap=4000000 --wallcap=60 --memo-power=22  # GATE_FAIL, rc=1
node third_impl.js --lo=10376293542535368704 --hi=65536 --stones=5 --legal=88 \
  --row=ng1-k07 --cap=4000000 --wallcap=60 --memo-power=22  # GATE_FAIL, rc=1
node third_impl.js --lo=10376293542535368704 --hi=65536 --stones=6 --legal=87 \
  --row=ng2-k07 --cap=4000000 --wallcap=60 --memo-power=22  # GATE_FAIL, rc=1
node third_impl.js --lo=10376293610182148096 --hi=68719476736 --stones=5 --legal=90 \
  --row=ng1-k08 --cap=4000000 --wallcap=60 --memo-power=22  # GATE_FAIL, rc=1
node third_impl.js --lo=10376293610182148096 --hi=68719476736 --stones=6 --legal=89 \
  --row=ng2-k08 --cap=4000000 --wallcap=60 --memo-power=22  # GATE_FAIL, rc=1
python3 audit_k06k07k08.py           # 82/82 gates, rc=0, deterministic
```

Input row specs: `input/k06.input.csv`, `input/k07.input.csv`,
`input/k08.input.csv`
(`target,0,5,<lo>,<hi>,<legal>,0,0,0,0,0`; exact published batch input bytes,
sha-pinned inside the auditor).

## k09..k43 resolved-batch addendum: third-implementation re-verification of all
thirty fifth-resumption resolved-LOSS rows plus the parked4-L50M-ladder WIN rows
k13/k19 (same host, same session, 2026-11-26)

Declared separately (single-owner, fresh-declaration program rule) in
`research/log/2026-11-26-n11-sixthcost-k09-k43-resolved32-thirdimpl-batch-single-owner-note.md`
(push `4d1b7db7`), extending this dir's program to the THIRTY resolved-LOSS rows
of the fifth-resumption batch of the sixth-cost exclusive S5 probe (k09..k43 minus
the three keys parked at that close: k20/k33/k38, which stay parked with NO new
verdict) AND to the two fresh WIN rows **k13 `1152921573327376384:536870912`** and
**k19 `10376293541461626880:65664`** published minutes before by the parked4 L50M
ladder (`73dfd4a7` checkpoint, halt-audit close-out `4e87e67b`), whose consumption
gate requires exactly this third-implementation scrutiny record as a separate
implementation family. Implementation and pins are unchanged from the parent
program; the C1 calibration raws of the k06/k07/k08 addendum (same host, same
session, no restart between them) are HONESTLY REUSED per the k04-addendum
precedent, as declared BEFORE any batch run.

**Dated corrections of the published declaration note** (declaration bytes
immutable; corrected here): the k13/k19 replica-raw count is TEN (five raws per
row: base15m, l50m-run1, l50m-run2, l50m-run3-verify, l50m-margin - not
"twelve"), and the total replica-raw count consumed by this batch is ONE HUNDRED
(90 fifth-resumption + 10 parked4-ladder - not "102"). No stage, verdict, key,
node count or scope statement of the declaration is affected.

| row | key lo:hi (legal) | replica raws (published) | third_impl | runs | expansions (ttHits / ttOverwrites) | wall (a-run) |
|---|---|---|---|---|---|---|
| k09 | `10377419441368469504:65536` (87) | 15M pair LOSS(2) x2 + 2M UNKNOWN: resolution nodes 4,018,184 | **LOSS(2)** | x2 (a, b) | 4,622,038 (2,607,830 / 652,622) | 13.66s |
| k10 | `10378545341275312128:65536` (84) | 15M pair LOSS(2) x2 + 2M UNKNOWN: resolution nodes 4,295,355 | **LOSS(2)** | x2 (a, b) | 4,945,820 (2,741,107 / 888,907) | 14.31s |
| k11 | `10412322338480590848:65536` (86) | 15M pair LOSS(2) x2 + 2M UNKNOWN: resolution nodes 7,012,218 | **LOSS(2)** | x2 (a, b) | 8,105,873 (4,437,184 / 3,911,738) | 23.28s |
| k12 | `10952754293765050368:65536` (83) | 15M pair LOSS(2) x2 + 2M UNKNOWN: resolution nodes 5,688,761 | **LOSS(2)** | x2 (a, b) | 6,593,392 (3,638,963 / 2,404,936) | 18.99s |
| k13 | `1152921573327376384:536870912` (95) | L50M pair + 32M margin + 50M verify, WIN(1) x4 identical + base15m parked baseline (UNKNOWN): nodes 16,402,480 x4 WIN | **WIN(1)** | x3 (a, b, v=verify-legal) | 19,433,195 (10,181,270 / 15,238,891) | 54.12s |
| k14 | `1152956757699461120:536870912` (99) | 15M pair LOSS(2) x2 + 2M UNKNOWN: resolution nodes 6,801,611 | **LOSS(2)** | x2 (a, b) | 7,836,133 (4,297,914 / 3,642,312) | 22.73s |
| k15 | `1297036692683751424:1064960` (99) | 15M pair LOSS(2) x2 + 2M UNKNOWN: resolution nodes 5,947,870 | **LOSS(2)** | x2 (a, b) | 6,903,671 (3,790,763 / 2,712,282) | 20.41s |
| k16 | `1297036761403228160:536870912` (95) | 15M pair LOSS(2) x2 + 2M UNKNOWN: resolution nodes 10,883,904 | **LOSS(2)** | x2 (a, b) | 12,650,074 (6,857,256 / 8,455,770) | 36.38s |
| k17 | `10376293541461626880:65537` (96) | 2M pair LOSS(2) x2 + 15M pair LOSS(2) x2 (identical nodes): resolution nodes 1,241,921 | **LOSS(2)** | x2 (a, b) | 1,405,334 (826,431 / 47) | 4.39s |
| k18 | `10376293541461626880:65544` (91) | 2M pair LOSS(2) x2 + 15M pair LOSS(2) x2 (identical nodes): resolution nodes 1,838,655 | **LOSS(2)** | x2 (a, b) | 2,098,799 (1,184,660 / 2,153) | 6.33s |
| k19 | `10376293541461626880:65664` (95) | L50M pair + 32M margin + 50M verify, WIN(1) x4 identical + base15m parked baseline (UNKNOWN): nodes 15,379,062 x4 WIN | **WIN(1)** | x3 (a, b, v=verify-legal) | 17,955,947 (9,504,863 / 13,761,643) | 50.94s |
| k21 | `10376293541461626880:67174400` (90) | 15M pair LOSS(2) x2 + 2M UNKNOWN: resolution nodes 3,649,839 | **LOSS(2)** | x2 (a, b) | 4,202,005 (2,326,723 / 392,033) | 12.60s |
| k22 | `10376293541461626880:268500992` (98) | 15M pair LOSS(2) x2 + 2M UNKNOWN: resolution nodes 7,527,812 | **LOSS(2)** | x2 (a, b) | 8,820,734 (4,653,093 / 4,626,471) | 25.71s |
| k23 | `10376293541461626912:65536` (97) | 15M pair LOSS(2) x2 + 2M UNKNOWN: resolution nodes 10,938,326 | **LOSS(2)** | x2 (a, b) | 12,654,986 (6,739,220 / 8,460,682) | 37.01s |
| k24 | `10376293541461627904:65536` (93) | 15M pair LOSS(2) x2 + 2M UNKNOWN: resolution nodes 4,796,315 | **LOSS(2)** | x2 (a, b) | 5,616,289 (3,010,163 / 1,467,038) | 16.20s |
| k25 | `10376293541461659648:65536` (91) | 15M pair LOSS(2) x2 + 2M UNKNOWN: resolution nodes 5,496,449 | **LOSS(2)** | x2 (a, b) | 6,336,310 (3,564,228 / 2,153,523) | 18.51s |
| k26 | `10376293541462151168:65536` (95) | 15M pair LOSS(2) x2 + 2M UNKNOWN: resolution nodes 14,439,424 | **LOSS(2)** | x2 (a, b) | 16,684,962 (8,721,684 / 12,490,658) | 47.31s |
| k27 | `10376293541478404096:65536` (93) | 15M pair LOSS(2) x2 + 2M UNKNOWN: resolution nodes 2,250,306 | **LOSS(2)** | x2 (a, b) | 2,578,044 (1,458,498 / 10,504) | 7.72s |
| k28 | `10376293541528735744:65536` (98) | 2M pair LOSS(2) x2: resolution nodes 1,918,850 | **LOSS(2)** | x2 (a, b) | 2,177,958 (1,274,689 / 2,777) | 6.59s |
| k29 | `10376293541595844608:65536` (97) | 15M pair LOSS(2) x2 + 2M UNKNOWN: resolution nodes 4,996,919 | **LOSS(2)** | x2 (a, b) | 5,797,487 (3,237,734 / 1,635,160) | 17.70s |
| k30 | `10376293610181103616:65536` (95) | 15M pair LOSS(2) x2 + 2M UNKNOWN: resolution nodes 3,933,511 | **LOSS(2)** | x2 (a, b) | 4,531,296 (2,619,620 / 597,949) | 13.72s |
| k31 | `10376856491415048192:65536` (92) | 15M pair LOSS(2) x2 + 2M UNKNOWN: resolution nodes 4,560,796 | **LOSS(2)** | x2 (a, b) | 5,269,285 (2,862,847 / 1,151,374) | 14.99s |
| k32 | `10664523917613338624:65536` (93) | 2M pair LOSS(2) x2: resolution nodes 1,989,908 | **LOSS(2)** | x2 (a, b) | 2,235,267 (1,374,600 / 3,852) | 7.08s |
| k34 | `14987979559889014784:65536` (96) | 15M pair LOSS(2) x2 + 2M UNKNOWN: resolution nodes 8,567,123 | **LOSS(2)** | x2 (a, b) | 9,966,873 (5,293,840 / 5,772,570) | 28.90s |
| k35 | `1152921573327372288:553648128` (100) | 15M pair LOSS(2) x2 + 2M UNKNOWN: resolution nodes 14,273,589 | **LOSS(2)** | x2 (a, b) | 16,896,018 (8,726,341 / 12,701,714) | 48.12s |
| k36 | `1224979167365300224:536870912` (100) | 15M pair LOSS(2) x2 + 2M UNKNOWN: resolution nodes 3,007,021 | **LOSS(2)** | x2 (a, b) | 3,440,325 (1,961,576 / 107,949) | 10.56s |
| k37 | `1297036692683751424:17825792` (103) | 15M pair LOSS(2) x2 + 2M UNKNOWN: resolution nodes 8,083,885 | **LOSS(2)** | x2 (a, b) | 9,510,402 (4,989,499 / 5,316,103) | 27.32s |
| k39 | `10376293541461626880:66560` (100) | 15M pair LOSS(2) x2 + 2M UNKNOWN: resolution nodes 5,725,348 | **LOSS(2)** | x2 (a, b) | 6,611,082 (3,659,270 / 2,422,272) | 19.31s |
| k40 | `10376293541461626880:67584` (102) | 15M pair LOSS(2) x2 + 2M UNKNOWN: resolution nodes 5,926,395 | **LOSS(2)** | x2 (a, b) | 6,894,081 (3,725,971 / 2,703,506) | 20.16s |
| k41 | `10376293541461626884:65536` (100) | 15M pair LOSS(2) x2 + 2M UNKNOWN: resolution nodes 6,536,846 | **LOSS(2)** | x2 (a, b) | 7,704,061 (4,018,770 / 3,510,186) | 22.54s |
| k42 | `10376293541461627136:65536` (101) | 15M pair LOSS(2) x2 + 2M UNKNOWN: resolution nodes 8,486,305 | **LOSS(2)** | x2 (a, b) | 10,223,560 (5,244,634 / 6,029,256) | 30.03s |
| k43 | `10376293541461692416:65536` (103) | 15M pair LOSS(2) x2 + 2M UNKNOWN: resolution nodes 6,916,669 | **LOSS(2)** | x2 (a, b) | 8,061,097 (4,354,662 / 3,867,018) | 23.17s |

Batch totals (a-runs): 248,762,398 expansions; every row's cold runs
byte-identical in (verdict, expansions, ttHits, ttOverwrites). Verdict-level
agreement with the published replica raws on ALL THIRTY-TWO rows (30x LOSS 2v2,
1x WIN k13 1v-WIN4, 1x WIN k19 1v-WIN4 - the first independent third-implementation
confirmation of the parked4 L50M ladder halt). Expansion counts are compared only
across the third implementation's own cold runs and are never compared to replica
node counts (the implementations count different quantities; the auditor
additionally enforces expansions != replica resolution nodes on every run as an
anti-copy gate).

- C4 fail-closed input gates: 64/64 GATE_FAIL with process exit status 1 (per-row
  declared legal+1 and declared stones=6, `--cap=4000000 --wallcap=60`;
  `out/neg-gate-k*.txt`).
- All one hundred replica raws consumed over raw.githubusercontent.com at the
  recorded HEADs (90 fifth-resumption raws at `0971173e`, fetched from the probe
  dir; 10 parked4-ladder raws at `4e87e67b`) were re-fetched at publication time
  and byte-verified against BOTH current main and the recorded consumption HEAD
  (100/100 sha-identical to both; inputs likewise 32/32), then re-published inside
  this dir at `out/<row>-replica-raws/` so the auditor is self-contained; each is
  sha-pinned inside `audit_k09k43.py` (`repl_sha_*` gates).
- `audit_k09k43.py` is a separate data-driven auditor (audit.py, audit_k04.py,
  audit_k05.py and audit_k06k07k08.py stay byte-frozen): **850/850 gates ALL
  PASS, rc=0**, deterministic byte-identical output across runs in a fixed layout
  (resolved-path detail strings only being layout-dependent). Gates: 3 script
  pins + 32 row-spec input pins + 100 repl_sha + 100 repl_row + per-row unanimity/
  UNKNOWN/negative-input gates + 66 third-row gates (clean rc=0 derived-legal key
  quads per run) + 32 determinism + 32 verdict-level + 32 anti-copy + 32
  ttOverwrites pins + 64 C4 + 3 C1-reuse + 3 batch-level + 1 scope. Negative
  tamper controls on full kit copies: k43 verdict flip 2->1 and k13 verdict flip
  1->2 (each failing determinism + verdict-level gates, rc=1) and a k09 replica-raw
  nodes edit (sha gate + batch-count gate, rc=1, row skipped fail-closed);
  restores byte-verified; final clean control rc=0
  (`out/audit-tamper-controls-k09k43.txt`).
- Honest session notes: (1) the batch driver's first attempt mis-parsed the
  published row-spec table (an awk column-offset error), producing four
  mis-keyed or stones-mismatched invocations for k09..k12; all four outputs were
  GATE_FAIL/aborted, deleted, and never published; the driver was fixed and the
  four rows re-run cleanly (the pre-registered C4 fail-closed input gates are what
  caught the mismatch on invocation). (2) The first k19 -v (verify-legal) attempt
  was executed WITHOUT `--verify-legal=1` (identical counts, wall ~50.9s); it was
  superseded BEFORE publication by the flagged re-run (`out/k19-cold-v-legal.txt`,
  wall 90.65s, identical verdict/expansions/ttHits). (3) No verdict consumed; the
  still-parked keys k20/k33/k38 were neither measured nor claimed; k38's L50M
  follow-up remains unclaimed.
- The delegated pinned C++ second-implementation gate
  (cpp/solvers/kyouen_dfpn_root.cpp sha256 `9193f5b6...`) remains recorded and
  UNCHANGED for these 32 rows (k13/k19 expectations: node-exact WIN at 16,402,480
  / 15,379,062; the 30 LOSS rows at their published resolution nodes); this
  sandbox has no C++ toolchain (re-verified this session). The parallel C++-gate
  lane closed the k01..k08 chain separately (`28ed2d9c`); every verdict here and
  there stays UNCONSUMED and adoption stays with the scrutiny owner.
- **The standard 11x11 empty board, the two-stone root {60,27}, and its remaining
  third moves {100,108} remain UNKNOWN. Node/expansion counts, budgets and wall
  times are never verdicts.**

### Reproduce (addendum k09..k43)

```
# per LOSS row kNN (a and b independent cold runs), e.g. k09:
node third_impl.js --lo=10377419441368469504 --hi=65536 --stones=5 --legal=87 \
  --row=k09-a --cap=400000000 --wallcap=270 --memo-power=22
# per WIN row (k13 shown; k19 likewise), three runs incl. the verify-legal run:
node third_impl.js --lo=1152921573327376384 --hi=536870912 --stones=5 --legal=95 \
  --row=k13-a --cap=400000000 --wallcap=270 --memo-power=22
node third_impl.js --lo=1152921573327376384 --hi=536870912 --stones=5 --legal=95 \
  --row=k13-b --cap=400000000 --wallcap=270 --memo-power=22
node third_impl.js --lo=1152921573327376384 --hi=536870912 --stones=5 --legal=95 \
  --row=k13-v --verify-legal=1 --cap=400000000 --wallcap=270 --memo-power=22
# per row, both fail-closed input gates (GATE_FAIL, rc=1):
node third_impl.js --lo=<lo> --hi=<hi> --stones=5 --legal=<legal+1> \
  --row=ng1-<row> --cap=4000000 --wallcap=60 --memo-power=22
node third_impl.js --lo=<lo> --hi=<hi> --stones=6 --legal=<legal> \
  --row=ng2-<row> --cap=4000000 --wallcap=60 --memo-power=22
python3 audit_k09k43.py            # 850/850 gates, rc=0, deterministic
```

Input row specs: `input/k09.input.csv` ... `input/k43.input.csv` plus
`input/batch-k13.input.csv` and `input/batch-k19.input.csv` (exact published
batch input bytes, sha-pinned inside the auditor; the two WIN-row specs are the
parked4 ladder's consumed input bytes). Full per-row run raws: `out/kNN-cold-*.txt`;
per-row replica raw copies: `out/kNN-replica-raws/`.

## k20/k33 third-impl addendum: third-implementation verdict re-verification of
the two parked4rest2 L50M ladder WIN rows (fresh host, 2026-11-26)

Declared separately (single-owner, fresh-declaration program rule) in
`research/log/2026-11-26-n11-sixthcost-k20-k33-thirdimpl-verdict-single-owner-note.md`
(push `449ab209`), as pre-registered by the Part SN completion log: k20/k33
carry the ladder 4-run primary battery plus the Part SN delegated pinned C++
second-implementation gate (GATE-PASS, node-exact) but had NO
third-implementation corroboration. This addendum extends the program to
exactly those two rows. Implementation and pins unchanged from the parent
program; the C1 calibration was re-executed FRESH on this host (new host,
honest non-reuse of published calibration raws).

| row | key lo:hi (legal) | replica raws (published) | third_impl | runs | expansions (ttHits / ttOverwrites) | wall (a-run) |
|---|---|---|---|---|---|---|
| k20 | `10376293541461626880:33619968` (95) | L50M pair + 32M margin + 50M verify, WIN(1) x4 identical + base15m parked baseline (UNKNOWN): nodes 16,196,331 x4 WIN | **WIN(1)** | x3 (a, b, v=verify-legal) | 19,455,330 (10,071,309 / 15,261,026) | 57.46s |
| k33 | `12682136550675320832:65536` (91) | L50M pair + 32M margin + 50M verify, WIN(1) x4 identical + base15m parked baseline (UNKNOWN): nodes 15,842,649 x4 WIN | **WIN(1)** | x3 (a, b, v=verify-legal) | 18,829,006 (10,066,094 / 14,634,702) | 56.47s |

Verdict-level agreement with the published replica raws on BOTH rows (2x WIN
1v-WIN4). With this addendum k20/k33 reach the k13/k19 coverage level
(ladder 4-run primary + delegated C++ second-implementation gate +
third-implementation verdict-level corroboration) and become
adoption-eligible inputs for a future adoption Part; that Part is NOT this
addendum, weighs the coverage asymmetry explicitly, and stays with the
scrutiny owner. Expansion counts are compared only across the third
implementation's own cold runs and never to replica node counts (anti-copy
gates enforced by the auditor; k20 expansions != 16,196,331, k33
expansions != 15,842,649).

- C1 fresh calibration on this host, before any k20/k33 row ran:
  (i) verify_tbl.js replica-vs-mine completion-table battery: replica quads
  95,670 == mine 95,670, 195,044 triples checked, 0 mismatches, rc=0
  (identical counts to the published k05 calibration raws)
  (`out/calib-verify-tbl.txt`); (ii) anchor w2 `10376293541461626880:131328`
  reproducing WIN(1) expansions 7,583,990 == the published witness value on
  both executions, identical quadruple (ttHits 4,157,314, ttOverwrites
  3,390,391; walls 22.98 / 23.07s)
  (`out/calib-anchor-w2-a.txt`, `out/calib-anchor-w2-b.txt`).
- All TEN replica raws (five per row) consumed at HEAD `a0166a12` over the
  raw CDN from the parked4rest2 ladder kit were fetched and sha-verified
  against the ladder MANIFEST BEFORE the declaration, and re-published
  inside this dir at `out/k20-replica-raws/` / `out/k33-replica-raws/` so the
  auditor is self-contained (each sha-pinned inside `audit_k20k33.py`).
- `audit_k20k33.py` is a separate data-driven auditor (audit.py,
  audit_k04.py, audit_k05.py, audit_k06k07k08.py and audit_k09k43.py stay
  byte-frozen): **49/49 gates ALL PASS, rc=0**, deterministic byte-identical
  output across two runs. Gates: 2 script pins + 2 row-spec input pins +
  2 input row-spec parses + 10 repl_sha + 10 repl_row + 2 stage-unanimity +
  3 C1 + 6 C2 per row x2 (clean runs, keys/derived-legal, determinism,
  verdict-level vs replica, verify-legal equality, anti-copy) + 4 C4
  fail-closed input gates + 1 scope (no cache file, exactly two rows).
  Negative tamper controls on full kit copies: k20 verdict flip 1->2 and
  k33 verdict flip 1->2 (each failing the determinism + verdict-level +
  verify-legal gates, rc=1) and a base15m-k33 replica-raw nodes edit
  (sha + row + unanimity gates, rc=1); restores byte-verified; final clean
  control rc=0 byte-identical to the baseline
  (`out/audit-tamper-controls-k20k33.txt`).
- Honest session notes: (1) the auditor had three pre-publication parse-bug
  iterations (replica CSV column offsets, a GATE_FAIL short-row parse)
  caught by its own crash/fail-closed behavior on the local kit; only the
  final byte is published. (2) No verdict consumed; the delegated pinned C++
  gate raws (Part SN, node-exact 16196331 / 15842649) are unchanged and
  cross-consistent; adoption stays with the scrutiny owner. (3) This
  sandbox has no C++ toolchain (re-verified).
- **The standard 11x11 empty board, the two-stone root {60,27}, and its
  remaining third moves {100,108} remain UNKNOWN. Node/expansion counts,
  budgets and wall times are never verdicts.**

### Reproduce (addendum k20/k33)

```
# per row (k20 shown; k33 likewise), three runs incl. the verify-legal run:
node third_impl.js --lo=10376293541461626880 --hi=33619968 --stones=5 --legal=95 \
  --row=k20-a --cap=400000000 --wallcap=270 --memo-power=22
node third_impl.js --lo=10376293541461626880 --hi=33619968 --stones=5 --legal=95 \
  --row=k20-b --cap=400000000 --wallcap=270 --memo-power=22
node third_impl.js --lo=10376293541461626880 --hi=33619968 --stones=5 --legal=95 \
  --row=k20-v --verify-legal=1 --cap=400000000 --wallcap=270 --memo-power=22
# per row, both fail-closed input gates (GATE_FAIL, rc=1):
node third_impl.js --lo=10376293541461626880 --hi=33619968 --stones=5 --legal=96 \
  --row=ng-k20-ng1 --cap=4000000 --wallcap=60 --memo-power=22
node third_impl.js --lo=10376293541461626880 --hi=33619968 --stones=6 --legal=95 \
  --row=ng-k20-ng2 --cap=4000000 --wallcap=60 --memo-power=22
python3 audit_k20k33.py            # 49/49 gates, rc=0, deterministic
```

Input row specs: `input/batch-k20.input.csv` and
`input/batch-k33.input.csv` (exact published ladder input bytes, sha-pinned
inside the auditor). Full per-row run raws: `out/k20-cold-*.txt` /
`out/k33-cold-*.txt`; calibration raws: `out/calib-*.txt`; per-row replica raw
copies: `out/k20-replica-raws/` / `out/k33-replica-raws/`; tamper battery
log: `out/audit-tamper-controls-k20k33.txt`.
