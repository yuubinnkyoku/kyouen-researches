# n11 fourth-cost class 1297107061427929088:0 exclusive S5 probe (JS replica)

Single-owner batch declared in `research/log/2026-11-21-n11-s5-wave2-refresh-union-merge-fourthcost-probe-single-owner.md` (commit `1f94f501`): 41 exclusive unclaimed keys of the fourth-cost class `1297107061427929088:0` (coverage {26, 28, 100, 108}), ascending truncated-cost proxy band then key. Evidence class: replica solver-trusted exact (`jsreplay.js`, pinned sha256 `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`), node-exact against the published C++ raw rows.

## Machine lists and gates

- `output/fourth-cost-exclusive-keys.json`: the authoritative 41-key order (`exclusive_unclaimed_probe_order`), machine-derived by the wave-2 refresh and cross-checked against the declaration note enumeration (fail-closed).
- `output/precheck-audit.json`: 41/41 keys pass every geometry/coordination gate: 5 stones, D4-canonical-safe and quadruple-free (published canonical-safe policy), independent integer `Board.legal` count == ledger legal (published repo-independent implementation), exclusive live parent == the fourth-cost class, absent from the probe-13 merged cache and the active quarantine registry, disjoint from all five concurrent lanes' fixed claim sets (focus35 / cert38 / third39 / sbd99+2), ascending (proxy, key) order with band histogram 9 / 27 / 5.
- `input/k01..k41.input.csv`: per-key replica inputs (`target,0,5,<lo>,<hi>,<legal>,...`).
- `input/val-gate/` + `output/val-gate/`: the four published two-target validation rows re-run fresh this session, node-exact (identical stones/legal/budget/result/nodes; only wall_s differs).

## Execution (this experiment)

Budget ladder 2,000,000 first (fresh 2^22-entry PnTT solver per row), then 15,000,000 twice (independent fresh solvers) only on UNKNOWN; deadline 0, publish=ALL, exact order=count; serial execution. Stopping rules are pre-registered in the declaration note (WIN stops the batch; UNKNOWN at 15M parks the key with no cache row; determinism mismatches stop the lane). Per-key raws are recorded in `output/raw/` as they complete. Verdicts stay at solver-trusted cache increment level; no class closure claim is made even if all 41 keys resolve LOSS (57 shared children remain unclaimed under this lane's declaration).

## Status guard

The standard 11x11 empty board, the two-stone root {60,27}, and third moves 100/108 remain UNKNOWN throughout. Nodes and budgets are never read as verdicts.

Note: the precheck additionally gates every key against the latest main merged chain cache (the third-cost lane increment, sha256 `bb4495e0...`), which this lane confirmed reproduces byte-identically as probe-13 base + 37 LOSS rows with its own union merger. The final published increment of this experiment will be merged onto that latest cache base.
