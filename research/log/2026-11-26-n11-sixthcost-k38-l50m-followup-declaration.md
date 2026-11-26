# k38 L50M follow-up declaration (sixth-cost exclusive S5 probe, fifth parked key)

Date: 2026-11-26 (long-term lane session). Single-owner publish-then-execute
declaration for the L50M escalation of the fifth-resumption PARKED key k38.

## Claimed territory

Exactly one key: k38 `10376293541461626880:66048` (legal 100, band-2 proxy
5,234,938, fifth resumption, machine order position 38 of the sixth-cost
exclusive S5 batch). Status at declaration time: 2M stage UNKNOWN
(`at2m-k38.out.csv`, result 0, nodes 2,000,000), escalated 15M cold pair BOTH
exhausted result 0 (nodes 15,000,000, walls 85/83 s, checkpoint `e43ba7ba`).
PARKED. No other key is claimed by this declaration; no further exclusive key
of the batch is started this session under any outcome.

## Why this Part

The Part SR completion log records the standing coverage asymmetry: the 30
fifth-resumption LOSS rows now have the delegated pinned C++ second-implementation
gate (Part SR, 33/33 GATE-PASS), while k38 stays parked@15M with NO L50M
follow-up claimed. This Part fills that vacancy with the pre-registered
escalation step (same protocol family as the third-cost and parked4/parked4rest2
L50M precedents).

## Pre-registered execution

- Implementation: the pinned Node.js first-implementation replica
  `scripts/jsreplay.js` (sha256
  845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df,
  byte-verified against main HEAD c6da9fd8 on this host before this push).
- Input: byte-clone of the published batch input `input/k38.input.csv`
  (`target,0,5,10376293541461626880,66048,100,0,0,0,0,0`), sha-verified
  against main HEAD c6da9fd8.
- Budget: 50,000,000 nodes, fresh cold solver process per run (empty 2^22 PnTT,
  --memo=22, order=count-asc, no shared TT), two independent cold runs
  (run1 then run2).
- Validation gate BEFORE the target runs, on this host, against the pinned
  val-gate inputs, expected quadruples (published, node-exact, wall may vary):
  at2m x2: (98, 2000000, 0, 2000000) and (99, 2000000, 0, 2000000);
  15M rows: (98, 15000000, 2, 3651923) and (99, 15000000, 2, 5040200).
- Expected per-key outcomes (pre-registered, exclusive):
  (a) LOSS(2) with identical (result, nodes) on both cold runs, nodes < 50,000,000
  -> k38 becomes a loss-resolved row of the batch (adoption remains a separately
  declared Part; verdict NOT consumed here);
  (b) WIN(1) with identical (result, nodes) on both cold runs -> pre-registered
  WIN stopping rule: no further claimed-key starts this session, witness
  publication (if-adopted analysis against the pinned canonical head) follows;
  (c) parked@50M: result 0, nodes 50,000,000 on both cold runs -> k38 stays
  PARKED, recorded honestly, higher-budget escalation left to a later declaration.
- Session-scoped stop rules (re-declared): this session escalates k38 only;
  any infrastructure failure of a run is recorded honestly and re-executed
  fresh (a truncated local scratch artifact is never published); the published
  raw is only the clean completed run.
- Publication paths (pre-registered):
  `research/experiments/n11-sixthcost-class-s5-exclusive-probe-10376293541461626880-20261121/output/raw/at50m-run1-k38.out.csv`
  and `.../at50m-run2-k38.out.csv`, plus a status log addendum and this
  declaration log. No cache file is modified by this Part.

## Verdict scope

NO verdict is consumed. A LOSS(2) or WIN(1) outcome is a batch row, not an
adoption: no cache increment, no class-status change, no coverage claim. The
standard 11x11 empty board, the 19 central-reply roots, the two-stone root
{60,27}, its remaining third moves {100,108}, S2, class 1/2/4 and all closure
classes stay UNKNOWN throughout. Nodes are bookkeeping, never verdicts.

## Environment and counter-probe

Counter-probe at declaration time: latest main HEAD c6da9fd8 (kit-14 wave D,
18:22:13Z); no commit touching k38 / L50M / parked escalation territory in the
30 minutes before this push (verified by listing HEAD commits at 18:54Z).
Execution host: upgraded sandbox with native Node.js v22.20.0; the D2
validation gate ran 4/4 node-exact on this host BEFORE this declaration push
(walls 9/9/17/26 s vs published-host walls, only wall_s differs), recorded in
the completion addendum.
