# n11-centralreply-closure-class34908-cppgate-20261125 (Part EO)

Second execution of the scrutiny-owner C++ second-implementation gate
(`kyouen_dfpn_root.cpp` at commit `154f3b7a67b97e13acbaee8b04dc74ddca728d19`,
sha256 `9193f5b6065e0fbcad2ef7c65f386187701cafa1f5b718cc35a5cbb0d138f92e`),
on closure class 34908's 6 remaining unconsumed probe-level WIN rows
{af029, af047, af050, af053, af023, af048} (per the Part EG per-row provenance),
plus the same 3 published-baseline anchors used by Part EN
(anchor-at2m / anchor-af039 / anchor-aj001). Declaration:
`research/log/2026-11-25-part-eo-cppgate-34908win6-declaration.md`.

Verdicts are NOT consumed by this experiment: adoption of WIN rows stays a
separate Part. The standard 11x11 empty board and every closure class remain
UNKNOWN. Nodes are never verdicts.

## Layout

- `scripts/gate_runner.sh` - two fresh-cold passes per row, fail-closed,
  compares (legal, budget, result, nodes) vs the pinned expectation.
  Machine-identical to the Part EN runner rev2 (`3a8ee4fd` bytes; only the
  header comment block names Part EO and records the EN rev1 field-index lesson
  as inherited-from-the-start).
- `scripts/audit_gate.py` - G1-G5 machine audit (structure, determinism,
  published-raw node-exactness, status accounting, input sha pins),
  emits `output/audit_gate.json`, rc=1 on any gate failure. Adapted from the
  Part EN audit rev4 (`319ebe5c` bytes) with the EN rev4 lesson structurally
  enforced: the REPLAY regex is asserted to have exactly 10 capture groups
  before use.
- `input/` - byte-clones of the published kit inputs (sha256 pins in
  audit_gate.py G5; the six WIN-row CSVs verified against the EG kit inputs
  at commit `bb661fbb` and the three anchor CSVs against the EN kit inputs
  at commit `949e68a7`).
- `output/` - raws (p1/p2 per row), `gate-status.log`, `audit_gate.json`,
  tamper battery record. Published after the run with fixed-commit fetch-back
  byte verification.

## Machine section

- gate binary: compiled in-session from the pinned source with
  `zig c++ -std=c++20 -O2` (zig 0.13.0; binary sha256 recorded in the
  declaration). The binary itself is not published; it is reproducible from
  the pinned source pins in the declaration via any C++20 toolchain.
- replication config (jsreplay-documented, provenance pin sha256
  `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`):
  `--n=11 --memo=22 --only=5 --exact-order=count
  --exact-replay=<csv> --exact-replay-budget=<budget>`.
- run record, MANIFEST-sha256.txt, and the close-out log are appended after
  the official execution.

## Official batch rows (budget/result/nodes pinned from published source raws)

| row | key_lo | key_hi (span) | legal | budget | result | nodes (pinned) |
|---|---|---|---|---|---|---|
| af029 | 1152921504607895553 | 68720525312 | 86 | 15M | 1 | 4,862,485 |
| af047 | 1152921504607895809 | 68719476736 | 84 | 15M | 1 | 9,841,975 |
| af050 | 1152921504607899649 | 68719476736 | 94 | 15M | 1 | 7,311,834 |
| af053 | 1152921504606852096 | 17660905521152 | 90 | 15M | 1 | 5,182,129 |
| af023 | 1152921504607895553 | 68719478784 | 94 | 30M | 1 | 28,933,179 |
| af048 | 1152921508902862849 | 68719476736 | 87 | 30M | 1 | 17,816,616 |
| anchor-at2m | 1152921504606851072 | 536870946 | 98 | 2M | 0 (budget ceiling) | 2,000,000 |
| anchor-af039 | 1152921504607895681 | 68719476736 | 89 | 30M | 2 (budget ceiling) | 19,234,232 |
| anchor-aj001 | 1152922604269469696 | 65536 | 84 | 30M | 2 (budget ceiling) | 5,156,075 |

Published raw provenance per row is recorded in `scripts/audit_gate.py`
(RAW_PROV) and cross-checked field-wise against the EG kit sources
(b33-raw at 15M for af029/af047/af050/af053; ea-raw at 30M for af023/af048;
the ea-raw af029 30M anchor row additionally shows identical nodes
4,862,485 at the higher budget) and the EN kit outputs for the anchors,
fetched fixed-commit (`bb661fbb` / `949e68a7`) this session before declaration.

## Run record (official execution, 2026-11-25)

All 9 rows GATE-PASS (2-pass fresh-cold determinism + published-raw
node-exact). One process per pass, single sequential worker; batch window
19:27:04Z-19:35:07Z (~8 min wall). Zero MISMATCH/GATE-FAIL/GATE-CRASH lines.

| row | legal | budget | result | nodes (p1, p2 identical) | wall_s (p1/p2) |
|---|---|---|---|---|---|
| af029 | 86 | 15M | 1 | 4,862,485 | 9/9 |
| af047 | 84 | 15M | 1 | 9,841,975 | 21/20 |
| af050 | 94 | 15M | 1 | 7,311,834 | 15/15 |
| af053 | 90 | 15M | 1 | 5,182,129 | 11/10 |
| af023 | 94 | 30M | 1 | 28,933,179 | 61/62 |
| af048 | 87 | 30M | 1 | 17,816,616 | 37/37 |
| anchor-at2m | 98 | 2M | 0 (budget ceiling) | 2,000,000 | 3/3 |
| anchor-af039 | 89 | 30M | 2 (budget ceiling) | 19,234,232 | 41/40 |
| anchor-aj001 | 84 | 30M | 2 (budget ceiling) | 5,156,075 | 10/10 |

- Field semantics as in Part EN: nodes are node counts, never verdicts; the
  anchors reproduce the EN official-run published baselines field-exactly.
- Gate rows total nodes per pass: 73,948,218 (both passes 147,896,436);
  anchors 26,390,307 per pass; batch total 200,677,050 expansions.
- No WIN row was downgraded or altered: the 6 class-34908 rows are now
  independently re-derivable from the pinned source, but remain UNCONSUMED
  pending an adoption Part.
- af029 budget-independence (published observation, not re-run here): the
  ea-raw 30M anchor row records the identical nodes 4,862,485 at 30M.
- Machine audit (EN-rev4-adapted): 46 gates, rc=0, run 3 times plus once
  canonically; all four `audit_gate*.json` byte-identical, sha256
  `b46f2130e9855204b5d3a12c07833083af1e96fc4dd9013893f6be7ed0bfa057`.
- Tamper battery (`output/tamper.log`): T1 corrupt audit-source expected pin
  (af029 4862485 -> 4862486) -> G3:af029 FAIL rc=1; T2 tamper raw
  af029.p1 nodes byte -> G2:af029+G3:af029 FAIL rc=1; T3 inject phantom
  GATE-FAIL into status log -> G4 FAIL rc=1; control untouched copy -> rc=0,
  audit byte-identical to canonical. 3/3 fail-closed, control clean; every
  tampered file's sha256 was pre-asserted changed (EJ/EL lesson enforced).

## Honesty notes (this Part)

- No runner/audit fix chain occurred this time: the runner is
  machine-identical to the Part EN runner rev2, the audit is the EN rev4
  adaptation with the 10-capture-group regex assert built in from the start.
- The gate binary was rebuilt in this session from the same pinned source
  (zig 0.13.0): binary sha256
  `330ce0120904a080caabb2f445ffe57a26fffcf7ffee4f6dda266be0e8307745`,
  which differs from the EN session binary `d27acf47...` (different host /
  glibc shim). Disclosed in the declaration before execution; the binary is
  not the pin, the pinned source is. First zig download attempt timed out
  at 15 MB and completed via a resume loop (11 attempts), then sha-verified.
- Calibration was pre-declaration (at2m/af039 node-exact, k04 WIN
  node-exact) and the anchors were then re-run fresh-cold in the official
  batch; the batch reproduces all three anchor baselines exactly.

## Reproduction

- Compile the pinned source (with its two header pins sha256
  `5976935dcfccb9b5a26fa68f8de20868ce45363dd8c372dcd67d9b841167e7f5` and
  `2e36d69481fafcde7aede8ae4fedf3d5477f91ee9846bcd4ae2975f32a4ba1a5`,
  per the declaration) with any C++20 toolchain; in-session build used
  `zig c++ -std=c++20 -O2` (zig 0.13.0). Then per row:
  `kyouen_dfpn_root --n=11 --memo=22 --only=5 --exact-order=count
  --exact-replay=input/<row>.input.csv --exact-replay-budget=<budget>`,
  twice, one process per pass, and compare `legal,budget,result,nodes` with
  the pinned expectations above (gate_runner.sh automates this and
  audit_gate.py re-checks everything from files).
