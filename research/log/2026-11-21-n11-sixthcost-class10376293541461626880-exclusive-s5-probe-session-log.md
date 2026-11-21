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

## Re-execution and fetch-back verification (post-push)

- Part 2 commit: `e0a30fab` (12 files). Push pre-conditions: all 12 local files
  SHA-256 gated before upload; the interposed concurrent commit `4f60cbecfc`
  (K1058 knowledge item only) touches none of this lane's paths or any S5
  cache/verdict file.
- Fetch-back byte audit at the fixed commit `e0a30fab`: all 12 files match by git
  blob SHA-1 (remote-reported vs locally recomputed), 12/12.
- Re-execution verification on the pushed checkpoint state: `python3
  scripts/analyze_win_finding.py` run twice -> all 69 fail-closed gates PASS both
  times, output byte-identical to the published `output/win-finding-ifadopted.json`
  (sha256 `39ae0e8d...`) on both runs.

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

## Session 3 (resumption batch k03..k43, 2026-11-21 ~21:37Z): WIN at k03 after one key, batch halted again

Environment: fresh execution host this session (2 cores, Node v22.20.0, Python 3.12.14);
no C++ toolchain (re-verified); package installation forbidden; unauthenticated
raw.githubusercontent.com answered throughout this session.

1. Re-fetch of latest main before any work: HEAD `ac118f45f2` (then re-checked twice:
   `73cb82bd6`, and at declaration push the parent had moved again; the parallel
   third-implementation re-verification note `ceb4eed71` (20:45Z) and the fourth-cost
   pass-1 raws (`b1a3dfbd3`) are disjoint from the k03..k43 resumption and no newer S5
   chain increment exists: chain tip still `bb4495e0...` 5,793 rows).
2. Declaration-check pass before the ladder (as required for resumption):
   `scripts/select_sixth_exclusive.py` re-run unmodified: ALL 229 gates PASS;
   regenerated selection JSON byte-identical to the published one (sha256 `d5e9b059...`);
   regenerated k03..k43 input CSVs byte-identical to the published batch inputs;
   validation gate re-run on THIS host: 4/4 node-exact (only wall_s differs).
3. Resumption single-owner declaration published
   (`research/log/2026-11-21-n11-sixthcost-class10376293541461626880-exclusive-s5-probe-resume-k03-k43-single-owner-note.md`).
4. Ladder start at k03 `10376293541461626880:65792` (machine position 3, legal 81):
   2M UNKNOWN (result 0, nodes 2,000,000, 9s); 15M run1 **WIN(1) nodes 9,255,414**
   (49s); pre-registered WIN stopping rule fired immediately; determinism pair closed
   with run2 15M **WIN(1) nodes 9,255,414** (48s) identical; voluntary third cold
   verification run 15M **WIN(1) nodes 9,255,414** (48s) identical, honestly labeled
   beyond the declared pair. k04..k43 NOT started this session.
5. If-adopted analysis `scripts/analyze_win_finding_k03.py` (117 fail-closed gates,
   cp of the published k02 analyzer extended with two scenarios): two runs
   byte-identical (sha256 `b0d2498b...` for `output/win-finding-ifadopted-k03.json`);
   negative control (one raw node count tampered by -1) fails closed at gate
   `k03_15m_pair`; restored raw re-verified byte-identical and the analysis re-PASSes.
   Scenario A (k03 only): 2 classes flip UNKNOWN->WIN (sixth-cost class 10376293541461626880:65536
   and NON-candidate 1297319267171041280:0 {48,50,80,84}); the k03 membership class
   1297036692683751424:64 is already base-stage WIN (no flip). Scenario B (k01+k02+k03):
   3 classes flip (adding 1297037792211107840:0 {24,30,80,84}, the k02 flip). Both:
   live 62->61, secured third-move coverage unchanged 117/119, remaining {100,108}
   unchanged, no class to LOSS, no coverage event, no root route. The sixth-cost class
   would hold TWO fresh WIN children (k02, k03).
6. Publication: raws + status.log + analyzer + analysis JSON + README checkpoint
   section + this log appendix in one commit; pre-push SHA-256 gate on all files;
   fetch-back byte audit by git blob SHA-1 at the pushed commit.

verdict consumption state (unchanged in kind): k01 LOSS / k02 WIN / k03 WIN are ALL
still unconsumed replica raw rows; adoption of any of them stays gated on the delegated
pinned C++ second-implementation verification, and the concurrent third-implementation
re-verification is additional evidence only; judgment stays with the scrutiny owner.

## Next steps (for a later session of this lane)

1. C++ second-implementation verification of the three raw rows (delegated; targets
   listed in the README k03 checkpoint section; any disagreement fails closed).
2. The third-implementation re-verification lane (in flight since 20:45Z) may fold the
   k01/k02/k03 rows into its program only with a fresh declaration covering them.
3. Resumption of k04..k43 requires a fresh declaration-check pass (selector re-run
   against the then-latest chain caches and claim sets); note that TWO WIN rows now
   sit unconsumed in this class's exclusive children, so the batch outcome evidence
   should be weighed by the scrutiny owner first.
4. On eventual full-batch completion: `output/probe-audit.json`, merged cache
   increment, SHA-256 manifest per the parent declaration's publication plan
   (WIN rows only with their C++ gate passed).
