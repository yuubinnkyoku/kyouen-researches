# n11 sixth-cost class 10376293541461626880:65536 parked-4-keys S5 L50M ladder - session log (2026-11-26, halted on WIN k13+k19)

Session of the recurring n11 long-term lane; declaration
`research/log/2026-11-26-n11-sixthcost-class10376293541461626880-parked4-s5-l50m-ladder-single-owner.md`
(commit `9e042a5f`, pushed 07:38:16Z, HEAD immediately before the push `a8c830ec`).
Kit: `research/experiments/n11-sixthcost-class10376293541461626880-parked4-s5-l50m-ladder-20261126/`.

## Why this lane

The fifth-resumption parent batch (k09..k43, same class) parked four exclusive
single-live-parent keys at UNKNOWN@15M (k13 `1152921573327376384:536870912`,
k19 `10376293541461626880:65664`, k20 `10376293541461626880:33619968`, k33
`12682136550675320832:65536`; parent checkpoints `2af0d7f2` / `e0be4063` /
`5ba9b673` / `948f1f1c`). They are minimal blockers for closing the sixth-cost
class. This lane raised the budget 15M -> 50M on the identical exact-replay
protocol, per the third-cost parked2 L50M precedent, as a SINGLE-OWNER lane in
a new experiment directory (no shared files with the parent dir, avoiding the
status.log clobber class of incident observed 07:02 the same day).

## Timeline (UTC, this 2-core host; Node v22.20.0; serial per-key stages, at
most 2 concurrent worker processes; one jsreplay process per run)

- 07:30-07:36  repo snapshot via codeload tarball at HEAD `238fa09c`; engine
  pin verified (`jsreplay.js` sha256 `84585617...`, identical in the two
  published source locations); selection JSON pin `d5e9b059...` verified;
  the four exact (key_lo, key_hi) pairs machine-verified ABSENT from the chain
  head of record `6e49dd84` (6,792 rows) and from the quarantine registry (2
  entries); no pre-existing parked4/L50M sixth-cost lane (search probes 0 hits);
  no C++ toolchain on PATH (re-verified).
- 07:35-07:36  validation gate on this host: 4/4 node-exact (at2m x2 0 /
  2,000,000 / legal 98, 99; 15M rows 2 / 3,651,923 and 2 / 5,040,200 / legal
  98, 99), walls 9/9/17/25 s.
- 07:38:16  declaration pushed (`9e042a5f`), fetch-back byte-identical
  (sha256 `51f55249...` local = published).
- 07:38:31  ladder start: k13 (worker A, with k20 queued) and k19 (worker B,
  with k33 queued); per-key stage order base15m -> l50m-run1 -> l50m-run2 ->
  (margin32m on resolve).
- ~07:41  base15m parked baselines reproduced exactly, per key fresh single
  runs: result 0, nodes 15,000,000 (walls 163/173 s under 2-process
  concurrency).
- ~07:46-07:49  both 50M determinism pairs came back **WIN(1)**, identical
  nodes: k19 15,379,062, k13 16,402,480. The first observed WIN was k19
  l50m-run1; both keys had already STARTED their pre-registered stages at
  07:38:31 (before any 50M result existed), so both keys legitimately
  completed their stages. Stopping rule 1 engaged: k20 and k33 were NEVER
  started (no lane artifact of any kind for them; they remain parked@15M,
  claimable by a later lane).
- ~07:50-07:52  32M budget-margin re-proofs: both keys reproduced (result 1,
  identical nodes), so each WIN is a full df-pn proof completing below the
  16.5M node level (~1.02-1.09x of the 15M park budget explains the parent
  probe's parking).
- 07:52  voluntary third cold 50M verification runs launched for both WIN
  keys (k02/k03/k04/k05/k08 precedent).
- Honest environment incident (disclosed also in the kit README): the FIRST
  launch of the two verify runs died with the launching shell process when
  that bash invocation returned (header-only truncated LOCAL scratch files,
  never published, deleted); the verify runs were re-executed fresh and
  cleanly with the ladder-proven nohup launch pattern. No raw row was
  affected; the declared pair and margins had already completed before the
  incident.
- 08:07:36  both verify runs completed: identical (result 1, nodes) - k13
  16,402,480, k19 15,379,062. FOUR identical WIN runs per key in total (pair +
  margin + verify).
- 08:08-08:11  fail-closed audit `scripts/audit_parked4_l50m.py`: **ALL 77
  PRE-WIN GATES PASS -> HALTED ON WIN [k13, k19]**, rc=2, `output/halt-audit.json`
  written, NO OK audit, NO cache file (declared no-increment rule). Second
  audit run: byte-identical halt-audit.json. Tamper battery on a scratch
  clone of the staged tree: T1 run2 verdict flip 1->2 -> GATE FAIL
  `k13.determinism` rc=1; T2 baseline nodes 15,000,000 -> 14,999,999 -> GATE
  FAIL `k19.base15m_parked_reproduced` rc=1; T3 fake raw artifact injected
  for never-started k20 -> GATE FAIL `k20.base15m_row` rc=1; clean controls
  rc=2 twice. (Battery note: the first T2 attempt had a non-matching sed
  pattern and legitimately passed; the corrected T2b tamper failed closed as
  required.)
- Concurrent lane commits observed mid-lane (territory-disjoint from this
  lane's exclusive keys and files): parent fifth-resumption k42/k43
  checkpoints `a8c830ec` / `0971173e` (07:37:39 / 07:40:09, k43 FINAL key of
  the selection), z-strip lane `dc7f36e1` (07:44:30, z=27/z=28 in-band rows
  kit), third-impl lane k06/k07/k08 declaration `b9dc2bb3` + addendum
  `ebdc7de7` (07:58:32 / 08:07:12, verdict-level agreement on all three
  rows). HEAD immediately before this session's publication pushes recorded
  in the publication commit messages.

## Results (all verdict-unconsumed raw evidence; no cache row)

- k13 `1152921573327376384:536870912` (legal 95, machine-order position 13):
  **WIN(1) in nodes 16,402,480** - identical on 2 cold 50M runs + 32M margin +
  voluntary 50M verify (4 runs).
- k19 `10376293541461626880:65664` (legal 95, position 19): **WIN(1) in nodes
  15,379,062** - identical on the same 4-run battery.
- These are the NINTH and TENTH fresh WIN children of the sixth-cost class in
  the unconsumed batch record (after k02/k03/k04/k05/k08), and the first of
  them found BELOW 16.5M nodes (the parent batch's WINs needed 6.2M-13.4M;
  these two are the first WINs that a prior 15M probe parked rather than
  missed - the parent's park semantics are thereby exercised on the WIN side
  for the first time, exactly the situation the L50M precedent resolved for
  the third-cost class).
- If-adopted (NOT adopted; recorded only in halt-audit.json against the head
  of record `6e49dd84`): the class would hold 2 WIN / 8 LOSS / 98 UNKNOWN of
  its 108 children.

## Mandatory scrutiny before any consumption (handed to scrutiny owners)

1. Second-implementation re-verification. BOTH fresh WIN rows need it. The
   pinned C++ `cpp/solvers/kyouen_dfpn_root.cpp` (source sha256
   `9193f5b6...`) is still not executable in this sandbox (no C++ toolchain,
   re-verified) - delegated targets recorded in halt-audit.json
   (`target,0,5,1152921573327376384,536870912,95,0,0,0,0,0` @50,000,000
   expected result 1, nodes 16,402,480;
   `target,0,5,10376293541461626880,65664,95,0,0,0,0,0` @50,000,000 expected
   result 1, nodes 15,379,062). The third-implementation re-verification
   program (currently through k06/k07/k08 via `ebdc7de7`) extends only with a
   fresh declaration; k13/k19 are the natural next two targets.
2. Game-theoretic consistency review against the historical WIN rows in the
   chain and the class-vs-root backward chain (K0414/K0416 lineage owners).
3. Only then: cache emission through the parent batch's full audit under the
   WIN/LOSS conflict policy. Until then both rows stay unconsumed. Note the
   WITNESS-side asymmetry: the parent batch's witness scripts
   (analyze_win_finding_kNN) have not been extended to these keys by this lane;
   any if-adopted flip analysis for the class census belongs to the witness
   lane, not to this record-only lane.

## Resume notes for the next run (re-fetch latest main before starting)

- k20 `10376293541461626880:33619968` and k33 `12682136550675320832:65536`
  remain parked@15M and UNCLAIMED beyond this batch's own parent declaration:
  a later lane can re-raise the budget for them (this lane's L50M protocol
  and machinery are directly reusable; WIN must re-trigger the halt rules).
- The parent fifth-resumption batch has now run its k43 FINAL key
  (`0971173e`); its close-out (witness/README appendix/session log,
  if not already pushed when this log lands) belongs to that lane, not this
  one.
- The sixth-cost class killer question remains open: with k13/k19 as fresh
  WIN raws pending scrutiny, the class's hypothetical WIN-status evidence
  (2 WIN / 8 LOSS / 98 UNKNOWN if adopted) is NOT a class claim; the class is
  NOT closed either way (58 shared unknown children remain outside this
  batch).

## Status guard

The standard 11x11 empty board remains UNKNOWN. The two-stone root {60,27}
and its remaining third moves 100/108 remain UNKNOWN at every point of this
session. Nodes, budgets, solver counts and proxy values are never verdicts.
Nothing was adopted, no cache file was written, no class/root/board claim is
made by this session.
