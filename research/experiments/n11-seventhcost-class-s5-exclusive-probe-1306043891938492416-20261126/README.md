# n11-seventhcost-class-s5-exclusive-probe-1306043891938492416-20261126

Exclusive single-live-parent S5 probe batch for the seventh-cost candidate
class `1306043891938492416:0` (coverage {100, 103, 105, 108}), the
adaptive-coordinator next selection after the Part SV canonical adoption
closed the sixth-cost batch (canonical head of record 42dbb58f..., 6,832
rows WIN 201 / LOSS 6,631). Declared in
`research/log/2026-11-26-n11-seventhcost-class1306043891938492416-exclusive-s5-probe-single-owner.md`
(wave A commit 8d8c3c5c).

## Status

Checkpoint state: selection published, ladder in progress. See
`output/raw/` for per-key checkpoint rows and the log for the latest
checkpoint summary. No verdict of this table may be consumed before the full
batch audit, the merged cache increment and the SHA-256 manifest are
published by the closing commit of this lane.

## Contents

- `scripts/select_seventh_exclusive.py`: fail-closed batch selector (fresh
  implementation of the published sixth-cost selector structure; freshness
  basis = the CURRENT canonical head 42dbb58f instead of probe-13 + the
  third-cost increment; 214 gates, deterministic).
- `scripts/jsreplay.js`: byte-clone of the pinned published Node.js replica
  (sha256 84585617...) of the standalone exact replay path of
  `cpp/solvers/kyouen_dfpn_root.cpp` at commit 154f3b7a.
- `input/k01..k42.input.csv`: per-key batch inputs (ascending truncated-cost
  proxy, then key).
- `input/val-gate/`: the published two-target-design validation rows.
- `output/seventh-cost-exclusive-keys.json`: the authoritative machine list
  (schema n11-seventhcost-exclusive-selection-v1).
- `output/val-gate-summary.json`: validation gate 4/4 node-exact on this
  execution host.
- `output/raw/`: per-key replay raw checkpoints (at2m / at15m-run1 /
  at15m-run2 / at2m-run2 rows as the pre-registered stages require).

## Selection summary (head basis, authoritative)

108 S5 children; 100 unknown under the head; 42 exclusive unknown children;
58 shared; proxy_exclusive_sum 226,065,724; bands 5,041,585 x4 / 5,234,938
x28 / 5,932,112 x10. The published probe-13-basis priority row (s5_unknown
101 / unknown_exclusive 41 / proxy_exclusive_sum 220,830,786) is retained
inside the selection JSON as the historical basis and is superseded by the
head-basis recomputation.

## Guards

Selection and scheduling only; no verdict is claimed or implied. The
standard 11x11 empty board: UNKNOWN. All 19 central-reply roots: UNKNOWN.
Two-stone root {60,27}: UNKNOWN. Third-move pair {100,108}: UNKNOWN. Every
closure class: UNKNOWN unless a published Part says otherwise.
