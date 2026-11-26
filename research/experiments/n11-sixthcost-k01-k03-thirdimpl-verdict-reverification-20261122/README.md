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
