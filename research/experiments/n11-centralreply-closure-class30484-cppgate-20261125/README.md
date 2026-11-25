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
