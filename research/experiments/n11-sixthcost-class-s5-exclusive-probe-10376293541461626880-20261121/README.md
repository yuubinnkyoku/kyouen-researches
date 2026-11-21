# n11-sixthcost-class-s5-exclusive-probe-10376293541461626880-20261121 (checkpoint state: batch halted on a fresh WIN at k02)

Exclusive single-live-parent S5 probe batch for the sixth-cost candidate class
`10376293541461626880:65536` (coverage {80, 84, 100, 108}),
rank 6 by `proxy_total` in the published class-closure-priority measurement
(all of the top-5 classes' exclusive keys are claimed by other lanes). Declared in
`research/log/2026-11-21-n11-sixthcost-class10376293541461626880-exclusive-s5-probe-single-owner.md`.

Status at this checkpoint commit:

- Selection (`output/sixth-cost-exclusive-keys.json`, schema `n11-sixthcost-exclusive-selection-v1`):
  229 fail-closed gates PASS under the pinned inputs (geometry 3,384 classes; probe-13
  merged exact S5 cache `60e0dc34...` 5,756 rows; latest chain increment base
  `bb4495e0...` 5,793 rows cross-checked: zero third-cost rows touch this class;
  supply 4,562; live candidates 62). The class has 108 S5 children, 7 LOSS / 0 WIN /
  101 UNKNOWN; the 43 exclusive (single-live-parent) unknown children are the
  authoritative machine list `exclusive_probe_order` (ascending truncated-cost proxy,
  then key; bands 5,041,585 x12 / 5,234,938 x22 / 5,932,112 x9;
  proxy_exclusive_sum 229,056,664). Every selected key: 5 stones, D4-canonical, safe
  (no forbidden quadruple), independent-integer-geometry legal count == supply ledger,
  live candidate parent set exactly the declared class, absent from the probe-13 base
  cache, the third-cost increment cache and the active quarantine registry, and
  disjoint from ALL concurrent lanes' machine-verified claim sets (focus35 / cert38 /
  third39 / fourth41 / fifth44 / sbd101 / parked-2) — every one of those claim sets is
  itself machine-read from its pinned published source in this selector, never
  hand-copied (ast extraction from the sha-pinned fifth-cost selector for the four
  embedded lists, keymap.json for sbd, the published fifth-cost machine list JSON for
  fifth44, the sha-pinned L50M ladder batch input CSVs for the parked-2 keys).
- Validation gate 4/4 reproduced on this execution host (`input/val-gate/`,
  `output/val/`, `output/val-gate-summary.json` all_pass=true): the pinned Node.js
  replica reproduces all four published two-target-design replay rows exactly
  (at2m x2: result 0 / nodes 2,000,000 / legal 98, 99; 15M x2: result 2 /
  nodes 3,651,923 and 5,040,200 / legal 98, 99), only `wall_s` differs.
- Per-key raw rows are pushed incrementally to `output/raw/` as checkpoints
  (`at2m-kNN`, and, only when the 2M stage is UNKNOWN, `at15m-run1-kNN` and
  `at15m-run2-kNN` per key; a key that settles at the 2M stage gets a second
  independent 2M run `at2m-run2-kNN` for the resolving-stage determinism pair).
  No verdict of this table may be consumed before the full batch audit
  (`output/probe-audit.json`), the merged cache increment and the SHA-256 manifest are
  published by the final commit of this lane.
- Expected per-key outcome under the pre-registered stopping rules: exact LOSS
  within the ladder (identical (result, nodes) on the determinism pair), or parked
  UNKNOWN at 15M (both runs recorded, no cache row). Any WIN stops further claimed-key
  starts this session and triggers witness publication instead.

## Checkpoint at k02: batch halted on a fresh WIN (verdict NOT consumed)

At this checkpoint the ladder ran k01 and k02 only, then halted on the
pre-registered WIN stopping rule:

- k01 `1297036692683751424:1114112`: 2M UNKNOWN (2,000,000 nodes), then LOSS(2) at
  15M with nodes 10,369,650 on both independent cold runs (`at15m-run1-k01`,
  `at15m-run2-k01`), determinism pair identical.
- k02 `1297036692683751424:68157440`: 2M UNKNOWN (2,000,000 nodes), then **WIN(1)** at
  15M with **nodes 7,717,432 on both independent cold runs**, PLUS a voluntary third
  cold verification run with identical (result, nodes)
  (`at15m-run3-verify-k02.out.csv`; beyond the declared pair, honestly labeled).
- Per the declaration's pre-registered rule (1), the batch stops starting further
  claimed keys this session; k03..k43 were not started. Verdicts are NOT consumed:
  no cache increment, no class-status change, no coverage claim.
- `output/win-finding-ifadopted.json` (script `scripts/analyze_win_finding.py`, 69
  fail-closed gates, deterministic byte-identical output) computes the IF-ADOPTED
  scenario against the pinned chain base `bb4495e0...` (5,793 rows): the fresh WIN
  verdict would mark exactly two classes UNKNOWN->WIN, the sixth-cost class
  `10376293541461626880:65536` (coverage {80, 84, 100, 108}, a live candidate class)
  and the NON-candidate class `1297037792211107840:0` (coverage {24, 30, 80, 84});
  live candidate classes 62 -> 61; secured third-move coverage is UNCHANGED at
  117/119 (remaining {100, 108}); no class becomes LOSS; the k01 LOSS row only
  decrements the sixth class's unknown-child count (101 -> 99). This is NOT a
  coverage event and NOT a route to the root certificate; it removes the sixth-cost
  class as a LOSS-completion route for moves {100, 108}.
- Adoption requirement (per the exclusive-probe program's WIN-row precedent, as with
  the third-cost parked-pair L50M WIN): a second-implementation verification of the
  published replica raw with the pinned C++ solver
  (`cpp/solvers/kyouen_dfpn_root.cpp`, sha256 `9193f5b6...`): targets
  `target,0,5,1297036692683751424,68157440,87,0,0,0,0,0` at budget 15,000,000
  (expected result 1, nodes 7,717,432) and the k01 row
  `target,0,5,1297036692683751424,1114112,87,0,0,0,0,0` (expected result 2,
  nodes 10,369,650). No C++ toolchain is available in this sandbox (verified), so this
  verification is delegated and recorded; any later C++ disagreement fails closed in
  favor of discarding the row. The class's published bin prior
  (`bin_prior_all_loss_index` 0.34616 from the class-closure-priority measurement) is
  mixed, not LOSS-only; the raw rows and this honest framing are the evidence.

Inputs and consumed pins (sha-verified, not duplicated here):

- base cache `merged-exact-s5-after-js-probe-13.cache` (sha256 `60e0dc34...`) and the
  post-probe supply/ledger at
  `research/experiments/n11-reply27-s5-jsreplica-probe-10376293541461626880-40960-20261121/output/`;
- latest published chain increment `merged-exact-s5-after-class-excl-1.cache`
  (sha256 `bb4495e0...`, the third-cost lane increment) at
  `research/experiments/n11-class1297036830122704896-exclusive-s5-jsreplica-probe-20261121/output/`;
- geometry `geometry.json.gz` (sha256 `146be80b...`) and `historical-cost-profile.json`
  at `research/experiments/n11-strategy-redesign-20261010/output/`;
- published class-closure-priority measurement (`139eb0a0...`, this class is its
  rank-6 row) and the fifth-cost selector source (`af68af3c...`) at their published
  paths (see `scripts/select_sixth_exclusive.py` for the complete pin list);
- `independent.py` (sha256 `954d3a10...`) at
  `research/experiments/n11-independent-exact-audit-20261010/scripts/`;
- canonical-safe policy `s5_evidence_policy.py` at
  `research/experiments/n11-frontier-selection-20261005/scripts/`;
- `results/n11-s5-evidence-quarantine.json` (sha256 `81d23160...`).

## Status guard

The standard 11x11 empty board, the two-stone root {60,27}, and its remaining third
moves 100/108 remain UNKNOWN throughout. Nodes, budgets, proxy values and solved
counts are never verdicts. This batch alone cannot close the class (58 shared
children remain unclaimed under this lane's declaration); any class-level statement
will only be made machine-checked against the full 108-child set.
