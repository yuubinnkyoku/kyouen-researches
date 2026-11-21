# 2026-11-21 n11 sixth-cost class 10376293541461626880:65536 exclusive S5 probe: session log (batch halted on a fresh WIN at k02)

Companion to the single-owner declaration
`research/log/2026-11-21-n11-sixthcost-class10376293541461626880-exclusive-s5-probe-single-owner.md`
(commit `30e694a6`, HEAD at declaration `d6b478bab8`) and the Part 1 selection commit
`1b262355`. Experiment directory:
`research/experiments/n11-sixthcost-class-s5-exclusive-probe-10376293541461626880-20261121/`.

## Timeline

- Selection: `scripts/select_sixth_exclusive.py` (43-key exclusive machine order,
  `output/sixth-cost-exclusive-keys.json`, schema `n11-sixthcost-exclusive-selection-v1`,
  229 fail-closed gates PASS). Every concurrent lane's claim set re-derived
  machine-side from its pinned published source; no claim list hand-copied.
- Validation gate re-run on this execution host: 4/4 published two-target-design
  replay rows reproduce exactly (result, nodes, legal, stones, is_or, budget), only
  `wall_s` differs (`output/val-gate-summary.json`, all_pass=true).
- Ladder execution (serial, cold runs, fresh empty 2^22 PnTT per row, one solver at a
  time, exec order k01 then k02):
  - k01 `1297036692683751424:1114112`: 2M UNKNOWN (2,000,000 nodes, `at2m-k01`),
    then LOSS(2) at 15M, nodes 10,369,650, determinism pair identical
    (`at15m-run1-k01`, `at15m-run2-k01`).
  - k02 `1297036692683751424:68157440`: 2M UNKNOWN (2,000,000 nodes, `at2m-k02`),
    then **WIN(1)** at 15M, **nodes 7,717,432, determinism pair identical**
    (`at15m-run1-k02`, `at15m-run2-k02`), then a voluntary third cold replay with
    identical (result, nodes) (`at15m-run3-verify-k02`, honestly labeled as beyond the
    declared pair).
- Pre-registered stopping rule (1) fired: the batch stops starting further claimed
  keys this session; k03..k43 were NOT started. `output/raw/status.log` records the
  per-run completion lines (rc=0 on every line).

## What the WIN means and does NOT mean

- Verdicts NOT consumed: no cache increment published, no class-status change on
  main, no coverage claim. Nodes are never verdicts.
- `scripts/analyze_win_finding.py` (69 fail-closed gates, deterministic
  byte-identical output) computes the machine-checked IF-ADOPTED scenario against
  the pinned chain base `bb4495e0...` (5,793 rows)
  `output/win-finding-ifadopted.json`:
  - adopting the two fresh rows would flip exactly two classes UNKNOWN->WIN: the
    sixth-cost candidate class `10376293541461626880:65536` (coverage {80, 84, 100,
    108}) and the NON-candidate class `1297037792211107840:0` (coverage {24, 30,
    80, 84}) (the win child has two parents; both flips are WIN-side).
  - live candidate classes 62 -> 61 (candidate pool delta: the sixth-cost class
    is WIN-eliminated as a LOSS-completion route for moves {100, 108});
  - secured third-move coverage UNCHANGED at 117/119 (remaining {100, 108}); this is
    NOT a coverage event and NOT a route to the root certificate;
  - no class becomes LOSS; the k01 LOSS row only decrements the sixth class's
    unknown-child count (101 -> 99);
  - scenario_no_base_conflict: zero conflict with the pinned base; the class's
    published `bin_prior_all_loss_index` 0.34616 was mixed, not LOSS-only.
- Adoption requirement (WIN-row precedent, as with the third-cost parked-pair L50M
  WIN): a second-implementation verification with the pinned C++ solver
  (`cpp/solvers/kyouen_dfpn_root.cpp`, sha256 `9193f5b6...`): target rows
  `target,0,5,1297036692683751424,68157440,87,0,0,0,0,0` at budget 15,000,000
  (expected result 1, nodes 7,717,432) and
  `target,0,5,1297036692683751424,1114112,87,0,0,0,0,0` (expected result 2,
  nodes 10,369,650). No C++ toolchain exists in this sandbox (verified), so this
  verification is delegated and recorded; any later C++ disagreement fails closed in
  favor of discarding the rows.

## Concurrency record

- Part 1 push (declaration + selection) accepted at commits `30e694a6` / `1b262355`.
- Immediately before this Part 2 push, latest main was re-fetched: HEAD `c81d3c9527`,
  three newer commits from the concurrent K1058 finite-field arc-count lane
  (`3241efc62e`, `235676e911`, `c81d3c9527`); none touches any S5 cache/verdict
  file, so the fail-closed publication-conflict rule does not fire. No other lane
  has published any sixth-cost key.
- No k03+ start without a fresh declaration-check pass (hourly parallel executions
  of this lane may already be in flight elsewhere).

## Status guard

The standard 11x11 empty board, the two-stone root {60,27}, and its remaining third
moves 100/108 remain UNKNOWN. Nodes, budgets, solved counts and proxy values are
never verdicts. The WIN(1) row is a solver-trusted replica raw row pending C++
second-implementation verification, not a consumed class verdict.

## Next steps (for a later session of this lane)

1. C++ second-implementation verification of the two raw rows (delegated; gate row
   per the WIN-row precedent).
2. Only after that: re-run the selector against the then-latest chain caches, then
   resume the ladder (k03..k43) with a fresh declaration-check pass.
3. On full-batch completion: `output/probe-audit.json`, merged cache increment,
   SHA-256 manifest per the declaration's publication plan.
