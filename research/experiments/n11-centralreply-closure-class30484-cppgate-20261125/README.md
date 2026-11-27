# n11-centralreply-closure-class30484-cppgate-20261125 (Part EN)

First-ever execution of the scrutiny-owner C++ second-implementation gate
(`kyouen_dfpn_root.cpp` at commit `154f3b7a67b97e13acbaee8b04dc74ddca728d19`,
sha256 `9193f5b6065e0fbcad2ef7c65f386187701cafa1f5b718cc35a5cbb0d138f92e`)
on closure class 30484's 4 remaining unconsumed probe-level WIN rows
{aj030, aj049, aj050, ai048}, the pre-registered sixth-cost k04 delegated row,
and 3 published-baseline anchors. Declaration:
`research/log/2026-11-25-part-en-cppgate-30484win4-declaration.md`.

Verdicts are NOT consumed by this experiment: adoption of WIN rows stays a
separate Part. The standard 11x11 empty board and every closure class remain
UNKNOWN. Nodes are never verdicts.

## Layout

- `scripts/gate_runner.sh` - two fresh-cold passes per row, fail-closed,
  compares (legal, budget, result, nodes) vs the pinned expectation.
- `scripts/audit_gate.py` - G1-G5 machine audit (structure, determinism,
  published-raw node-exactness, status accounting, input sha pins),
  emits `output/audit_gate.json`, rc=1 on any gate failure.
- `input/` - byte-clones of the published kit inputs (sha256 pins in
  audit_gate.py G5; verified against the source-kit MANIFESTs at main
  `680894b7`).
- `output/` - raws (p1/p2 per row), `gate-status.log`, `audit_gate.json`,
  tamper battery record. Published after the run with fixed-commit fetch-back
  byte verification.

## Machine section

- gate binary: compiled in-session from the pinned source with
  `zig c++ -std=c++20 -O2` (zig 0.13.0; binary sha256
  `d27acf47de52e781d9aa48c6567fcdbfe52ddcf8a5ddf15798d2b47a112192f1`).
  The binary itself is not published (19 MB); it is reproducible from the pinned
  source pins in the declaration via any C++20 toolchain.
- replication config (jsreplay-documented): `--n=11 --memo=22 --only=5
  --exact-order=count --exact-replay=<csv> --exact-replay-budget=<budget>`.
- run record, MANIFEST-sha256.txt, and the close-out log are appended after
  the official execution.

## Run record (official execution, 2026-11-25)

All 8 rows GATE-PASS (2-pass fresh-cold determinism + published-raw
node-exact). One process per pass, single sequential worker.

| row | key_lo | key_hi (span) | legal | budget | result | nodes (p1, p2 identical) |
|---|---|---|---|---|---|---|
| aj030 | 1152922604135251976 | 65536 | 83 | 30M | 1 | 15,284,699 |
| aj049 | 1152921574400065536 | 1114112 | 80 | 30M | 1 | 4,998,452 |
| aj050 | 1152921574400065536 | 68157440 | 80 | 15M | 1 | 1,871,594 |
| ai048 | 1152921573327372288 | 68157440 | 68 | 15M | 1 | 2,232,854 |
| k04 | 10376293541461626888 | 65536 | 83 | 15M | 1 | 9,433,024 |
| anchor-at2m | 1152921504606851072 | 536870946 | 98 | 2M | 0 (budget ceiling) | 2,000,000 |
| anchor-af039 | 1152921504607895681 | 68719476736 | 89 | 30M | 2 (budget ceiling) | 19,234,232 |
| anchor-aj001 | 1152922604269469696 | 65536 | 84 | 30M | 2 (budget ceiling) | 5,156,075 |

- Field semantics: result 0 = budget ceiling in jsreplay convention, 1/2 are
  replay-path outcomes as pinned from the published raws; nodes are node
  counts, never verdicts. The 3 anchors reproduce published budget-ceiling
  baselines exactly (at2m/af039/aj001 observed == published, field-exact).
- Gate rows total nodes observed: 33,836,623 (both passes: 67,673,246);
  anchors 26,390,307 per pass. No WIN row was downgraded or altered; the 4
  class-30484 WIN rows are now independently re-derivable from the pinned
  source, but remain UNCONSUMED pending the adoption Part.
- Cross-check vs published source raws (field-wise, wall_s excluded):
  aj030 (EK), aj049 (EK and b39; b39's budget differs, nodes identical),
  aj050 (b39), ai048 (b38), k04 (sixthcost kit): all non-wall fields
  identical where the budgets match; aj049/b39 differs only in budget and
  still matches nodes exactly.
- Machine audit rev4: 41 gates, rc=0, run 3 times plus once canonically;
  all four `audit_gate*.json` byte-identical, sha256
  `f35cddd24f7062c1e0861563fbce737edabd2620ae3028d3c2d42fd937c407af`.
- Tamper battery (output/tamper.log): T1 corrupt published pin (aj030
  15284699->15284698) -> G3:aj030 FAIL rc=1; T2 tamper raw aj049.p1 nodes
  -> G2:aj049 FAIL rc=1; T3 inject GATE-FAIL line into status log -> G4 FAIL
  rc=1; control untouched copy -> rc=0 with audit byte-identical to
  canonical. 3/3 fail-closed, 1/1 control clean.

## Honesty notes (fix chain during this Part)

- runner rev2 (`3a8ee4fd`): CSV field indices f3=stones f4=legal were wrong in
  rev1; fixed before any target row was executed (only the inject guard and
  an at2m rehearsal touch rev1 semantics).
- audit rev2 (`7dbc0dd2`): G2 wall_s exclusion index.
- audit rev3 (`91adeff1`): G1 wrongly required a jsreplay telemetry line
  (`# forbidden quadruples:`) that the pinned C++ standalone driver does not
  print; fixed to require the driver's own header lines.
- audit rev4 (`319ebe5c`) CRITICAL: the REPLAY regex had 11 capture groups
  instead of 10, so under rev1-rev3 G2/G3 silently never matched and the
  tampers T1/T2 were false negatives. Caught by the tamper battery itself;
  the official audit was then redone fresh with rev4. Raws and status log
  were never affected; the audit is a check, not a producer.

## Reproduction

- Compile the pinned source (with its two header pins sha256
  `5976935dcfccb9b5a26fa68f8de20868ce45363dd8c372dcd67d9b841167e7f5` and
  `2e36d69481fafcde7aede8ae4fedf3d5477f91ee9846bcd4ae2975f32a4ba1a5`,
  per the declaration) with any
  C++20 toolchain; in-session build used `zig c++ -std=c++20 -O2` (zig 0.13.0,
  binary sha256 `d27acf47...`). Then per row:
  `kyouen_dfpn_root --n=11 --memo=22 --only=5 --exact-order=count
  --exact-replay=input/<row>.input.csv --exact-replay-budget=<budget>`,
  twice, one process per pass, and compare `legal,budget,result,nodes` with
  the pinned expectations above (gate_runner.sh automates this and
  audit_gate.py re-checks everything from files).
