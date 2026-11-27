# Part EN close-out: first-ever C++ second-implementation scrutiny gate executed - class 30484's 4 remaining unconsumed WIN rows independently re-derived, 8/8 GATE-PASS (2026-11-25)

Close-out of `research/experiments/n11-centralreply-closure-class30484-cppgate-20261125/`
(declaration: `research/log/2026-11-25-part-en-cppgate-30484win4-declaration.md`).
Single-owner session. Pre-push HEAD observed at `319ebe5c` (this Part's own
audit rev4; the Part EJ takeover at `90c75f9f` is a disjoint class-30118
lane, no path overlap).

## 1. Outcome in one line

The scrutiny-owner C++ second implementation (`cpp/solvers/kyouen_dfpn_root.cpp`,
payload pin `9193f5b6...` = full sha256
`9193f5b6065e0fbcad2ef7c65f386187701cafa1f5b718cc35a5cbb0d138f92e`,
resolved byte-exact to commit `154f3b7a67b97e13acbaee8b04dc74ddca728d19`)
was compiled and executed for the first time in this program, and reproduced
every pinned published row node-exactly, 2-pass deterministic, fail-closed.

**No verdict was consumed.** The 4 class-30484 WIN rows {aj030, aj049, aj050,
ai048} plus the sixth-cost k04 delegated row are now independently
re-derivable from the pinned source, but adoption stays with the separate
adoption Part (pinned fail-closed union merger `90711961...` route). The
standard 11x11 empty board remains UNKNOWN; closure class 30484's unknown
count is unchanged at 4.

## 2. Execution summary (all 8 rows GATE-PASS)

Config per pass: `--n=11 --memo=22 --only=5 --exact-order=count
--exact-replay=input/<row>.input.csv --exact-replay-budget=<budget>`.
One process per pass, fresh-cold, single sequential worker.

| row | key_lo | key_hi span | legal | budget | result | nodes (p1, p2 identical) | published source of the pin |
|---|---|---|---|---|---|---|---|
| aj030 | 1152922604135251976 | 65536 | 83 | 30M | 1 | 15,284,699 | EK kit raw |
| aj049 | 1152921574400065536 | 1114112 | 80 | 30M | 1 | 4,998,452 | EK kit raw (b39 kit raw also pinned; budget differs, nodes identical) |
| aj050 | 1152921574400065536 | 68157440 | 80 | 15M | 1 | 1,871,594 | b39 kit raw |
| ai048 | 1152921573327372288 | 68157440 | 68 | 15M | 1 | 2,232,854 | b38 kit raw |
| k04 | 10376293541461626888 | 65536 | 83 | 15M | 1 | 9,433,024 | sixthcost k01-k03 kit raw (pre-registered 2026-11-22) |
| anchor-at2m | 1152921504606851072 | 536870946 | 98 | 2M | 0 | 2,000,000 | EK at2m val-gate raw |
| anchor-af039 | 1152921504607895681 | 68719476736 | 89 | 30M | 2 | 19,234,232 | EK kit raw |
| anchor-aj001 | 1152922604269469696 | 65536 | 84 | 30M | 2 | 5,156,075 | EK kit raw |

Result semantics: result 0/2 = budget ceiling (anchors reproduce published
budget-ceiling baselines exactly); result 1 = replay-path WIN outcome as
pinned from the published raws; nodes are node counts and are never
verdicts. Gate rows total nodes: 33,836,623 per pass. Raw files:
`output/raw/<row>.{p1,p2}.out`, status: `output/gate-status.log` (8 PASS
lines, zero MISMATCH/FAIL/CRASH).

Field-wise cross-check against the published source raws (wall_s excluded):
identical on every field where the pinned budgets match (aj030/EK, aj049/EK,
aj050/b39, ai048/b38, k04/sixthcost); the b39/aj049 source row ran under a
different budget and the nodes still match exactly.

## 3. Toolchain and reproducibility

- In-session build: `zig c++ -std=c++20 -O2` (zig 0.13.0); binary sha256
  `d27acf47de52e781d9aa48c6567fcdbfe52ddcf8a5ddf15798d2b47a112192f1`.
  Binary deliberately not published (19 MB); reproducible from the pins.
- Gate source header pins (both required by the .cpp includes):
  `5976935dcfccb9b5a26fa68f8de20868ce45363dd8c372dcd67d9b841167e7f5`,
  `2e36d69481fafcde7aede8ae4fedf3d5477f91ee9846bcd4ae2975f32a4ba1a5`.
- jsreplay provenance pin: sha256
  `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`.
- Current main's `cpp/solvers/kyouen_dfpn_root.cpp` (sha256 `a0786acb...`,
  2026-10-22 revision) is a DIFFERENT revision from the gate pin; the gate
  pin is anchored at commit `154f3b7a67` per jsreplay's header statement.
  This divergence is recorded deliberately: adoption gates pin the source
  revision the published rows were produced under.

## 4. Commit chain of this Part (all direct to main, no branch/PR)

1. `66a2e7f2` - declaration + kit v1 (README, inputs, runner rev1, audit rev1)
2. `3a8ee4fd` - runner rev2: fix CSV field indices (f3=stones f4=legal);
   fail-closed inject guard before any target row ran
3. `7dbc0dd2` - audit rev2: G2 wall_s exclusion index
4. `91adeff1` - audit rev3: G1 must not require jsreplay telemetry the C++
   standalone driver does not print
5. `319ebe5c` - audit rev4 (CRITICAL): REPLAY regex 11 capture groups -> 10;
   under rev1-rev3 G2/G3 silently never matched
6. this commit - outputs (raws 16, status 8 PASS, audit 4x, tamper.log),
   README run record + honesty notes, MANIFEST-sha256.txt, this close-out

## 5. Honesty incidents (all fixed in-session, none touched the raws)

- runner rev1 had swapped CSV field indices; caught by the inject guard
  before any target row executed; only an at2m rehearsal used rev1.
- audit rev1-rev3: three sequential bugs (wall_s index, G1 over-requirement,
  and the CRITICAL regex group count that made G2/G3 vacuous). The vacuous
  audit would have passed ANY raws - exactly the failure mode the tamper
  battery exists to catch, and it did: T1/T2 were false negatives under
  rev3, which exposed the regex bug. The official audit was then redone
  fresh under rev4 on the untouched raws. The audit is a check, not a
  producer; the runner's own fail-closed comparisons (f1 == f2 == expected)
  were correct from rev2 onward and independent of the audit bugs.

## 6. Machine audit (rev4) and tamper battery

- 41 gates (G5 input pins x8, G1 structure x16, G2 determinism x8,
  G3 published pins x8, G4 accounting x1): rc=0, overall PASS. Run three
  extra times: all `audit_gate*.json` byte-identical, sha256
  `f35cddd24f7062c1e0861563fbce737edabd2620ae3028d3c2d42fd937c407af`.
- Tamper battery (`output/tamper.log`, reproduced as a fresh artifact):
  - T1 corrupt published pin (aj030 nodes 15284699 -> 15284698): FAIL
    `G3:aj030`, rc=1
  - T2 tamper raw (aj049.p1 nodes 4998452 -> 4898452): FAIL `G2:aj049`, rc=1
  - T3 inject phantom GATE-FAIL into gate-status.log: FAIL `G4`, rc=1
  - CONTROL untouched copy: rc=0, audit byte-identical to canonical
  - verdict: 3/3 fail-closed, control clean. Each tamper pre-asserted that
    the tampered file's sha256 actually changed.

## 7. UNKNOWN guard / next steps

- The standard 11x11 empty board: UNKNOWN. The 19 two-stone roots and every
  closure class: UNKNOWN. Class 30484: unknown count still 4 (the 4 WIN
  rows are gate-verified but UNCONSUMED). Nodes are not verdicts; probe-level
  WIN labels from df-pn with a budget ceiling are not class verdicts.
- Next lane options, in value order:
  (a) adoption Part: consume the 4 verified WIN rows of class 30484 via the
      pinned merger `90711961...` route (board re-verification required),
      dropping class 30484 to 0 unknown;
  (b) gate the 6 WIN rows of class 34908 (af029/af047/af050/af053/af023/
      af048 per the EG per-row provenance) - the natural next scrutiny batch;
  (c) batch-41 on class 30345 (26 unknown rows remaining) stays available;
  (d) the Part EJ lane (`90c75f9f` takeover, class 30118) is running in
      parallel and disjoint.
- Toolchain note: the zig build environment in this session is ephemeral;
  the kit is reproducible from source pins with any C++20 toolchain.
