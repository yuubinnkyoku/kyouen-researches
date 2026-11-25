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
