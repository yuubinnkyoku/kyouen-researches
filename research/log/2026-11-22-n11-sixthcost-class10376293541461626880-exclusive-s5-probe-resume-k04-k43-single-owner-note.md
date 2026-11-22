# n11 sixth-cost exclusive S5 probe resumption batch k04..k43: single-owner note (2026-11-22, second resumption)

Declared: 2026-11-22T00:52Z (lane: the n11 long-term lane that published the sixth-cost
exclusive probe batch 30e694a6/1b262355/e0a30fab/f348343e, the first resumption k03
checkpoint 92ddb69b/28a038a5/3d1e5639, and today's k01/k03 third-implementation
verification 53d8fe28/90f38c95/d5371854). HEAD at the moment of this note's
composition, re-fetched immediately before push: `d5371854b0686b9a64d0c992e861d61720cb13b0`
(this lane's own session-log commit; no other lane has pushed since 00:37Z).

## Scope: resume the halted batch at k04..k43 (40 remaining keys, no new keys claimed)

The first resumption session halted at k03 on the pre-registered WIN stopping rule; that
stop is session-scoped ("no further claimed-key starts THIS session"), so this session
resumes the remaining 40 exclusive keys k04..k43 of the SAME published machine list
(`n11-sixthcost-exclusive-selection-v1`, output/sixth-cost-exclusive-keys.json). No new
key is claimed; the k01 LOSS and k02/k03 WIN raw rows and all their unconsumed verdicts
are unchanged. Since the k03 halt, the program's verification position materially
improved: k02 has a published third-implementation WIN reproduction (ea73c3e3) and
TODAY k03 gained one too (WIN x3, 10,896,601 expansions deterministic) plus k01 LOSS
x2 (90f38c95), while the third-implementation bank full-band recalibration landed
198/198 verdict-level agree (c3c62fd4). The delegated pinned C++ gate for k01/k02/k03
remains open with the scrutiny owner. This session's expectation is honest either way:
more band-1 WINs add redundancy against any single-row rejection, more LOSSes refine
the mixed bin prior (bin_prior_all_loss_index 0.34616); the batch never consumes verdicts.

Declarations re-run on this host BEFORE any ladder start:

- D1 Selector re-execution (scripts/select_sixth_exclusive.py, byte-identical to the
  published copy, sha-verified inputs at their repo paths fetched at HEAD d5371854):
  ALL 229 fail-closed gates PASS. The regenerated selection JSON is byte-identical to
  the published one (sha256 d5e9b059611849f7b7e69c7370a0e66cd7535c43b3a043ce9f5bfc0e5ff72e87)
  and all 43 regenerated k01..k43 input CSVs are byte-identical to the published batch
  inputs (43/43 cmp).
- D2 Validation gate on THIS execution host (input/val-gate/ 4 rows, pinned Node.js
  replica jsreplay.js sha256 845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df):
  4/4 node-exact PASS (at2m x2 result 0 / nodes 2,000,000 / legal 98, 99; 15M rows
  result 2 / nodes 3,651,923 and 5,040,200 / legal 98, 99); only wall_s differs. This
  host's rows will be published as a new val summary file (distinct name, no overwrite).

## Pre-registered ladder and stopping rules (fail-closed, identical to the first resumption)

- Per key, in ascending truncated-cost-proxy machine order k04..k43: stage 2M (one run);
  if result nonzero, a second independent 2M run must reproduce identical (result, nodes);
  if result 0 (UNKNOWN), escalate to 15M: two independent cold runs. Both 15M runs
  nonzero-and-identical => resolved; both 15M runs exhausted (result 0, nodes 15,000,000)
  => parked (no cache row). A disagreement across a determinism pair is a hard stop of
  the batch: record the anomaly, publish the raw outputs plainly, hand the divergence to
  the next run; no interpretation and no consumption in this session.
- Any WIN (result 1) at any stage stops further claimed-key starts in THIS session
  (rule (1) of the parent batch): publish the WIN checkpoint raws with honest labels
  (plus a voluntary third cold verification run for any WIN, honestly labeled, per the
  k02/k03 precedent); verdicts of the entire batch remain unconsumed.
- Raw rows are pushed incrementally to the published output/raw/ as per-key checkpoints
  (at2m-kNN, at15m-run1-kNN, at15m-run2-kNN, at15m-run3-verify-kNN) with status.log
  appended in the published format; the batch never claims a verdict before its full
  audit, merged cache increment and SHA-256 manifest are published.
- Consumption gate (only if this batch ever completes with zero WIN): rows resolved here
  (LOSS with identical determinism pairs) may enter a merged cache increment that
  byte-preserves the chain tip plus the new rows, under the WIN/LOSS conflict gate, with
  a fail-closed audit JSON and a sha256 manifest; k01/k02/k03 rows never enter any
  increment (delegated C++ gate). Before such an increment, main is re-fetched; if any
  third-implementation disagreement about this lane's rows has been published meanwhile,
  this batch also stays unconsumed and the increment is not published.
  A session wall-time budget is pre-registered: if the ladder is still running when the
  session budget ends, the batch stops at the last completed key (honest "budget-stop"
  status in status.log); remaining keys stay claimable by the next run.

## Concurrency and disjointness

- Visible sibling session running the thirdimpl bank-full follow-up (stretch-37 rows,
  out/stretch-37/): targets are published third-cost exclusive LOSS rows and the
  third-implementation experiment dir; fully disjoint from this ladder's k04..k43 keys
  and from this lane's other paths.
- n11-s4bd fresh corpus regen lane (pass2 checkpoints, high-frequency pushes): S4BD
  corpus rows, disjoint from these S5 exclusive keys (machine-checked inside D1 through
  the pinned keymap/claim sets).
- Non-n11 lanes on latest main (six-row m=25 crunch, five-row, seven-row): disjoint.
- This session pushes only: new output/raw/* checkpoint files, status.log appends, a new
  output/val-gate summary file for THIS host, README checkpoint append, this note, and a
  session log. No cache file is modified; no K item; no knowledge README edit
  (verdict-unconsumed-class batch per precedent).

## Environment facts

- Node v22.20.0, Python 3.12.14, 2 cores; serial single-process foreground ladder runs.
- No C++ toolchain (re-verified today); package installation forbidden; delegated C++ gate
  unchanged (k01 expected 2/10,369,650; k02 1/7,717,432; k03 1/9,255,414 @15M).
- Unauthenticated raw.githubusercontent.com working; every input fetched at pinned commit
  d5371854 and sha-verified by the selector's own fail-closed gates.

## Status guard

Scheduling and raw evidence only. The standard 11x11 empty board, the two-stone root
{60,27}, and its remaining third moves 100/108 remain UNKNOWN throughout. Nodes, budgets,
proxy values and solved counts are never verdicts. This batch cannot close the class
(58 shared children remain outside this lane); any class-level statement will only be
made machine-checked against the full 108-child set.
