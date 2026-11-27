# 2026-11-27 n11 ninth-cost parked-3 L50M rows third-impl corroboration: single-owner declaration (wave A)

## Claim

This lane claims the third-implementation corroboration Part for the three
ninth-cost stage-3 L50M resolved rows k02 / k04 / k07, published in wave B
commit 41b331d1 (raws + `output/batch-summary-l50m.json`, schema
n11-ninthcost-parked3-l50m-summary-v1) of the kit
`research/experiments/n11-ninthcost-class-s5-exclusive-probe-1297036692683751424-20261127/`.

Single-owner: no other lane has declared or published a third-impl kit for
these three rows (main HEAD at push time is 8b79ef3a, commit list
machine-checked; no parked3-L50M thirdimpl or cppgate kit exists on main).
The k01/k03/k05/k06, k08..k11, and k12 third-impl kits are disjoint targets
of other Parts and are not touched here.

Publish-then-execute: this declaration is pushed before any third_impl
invocation of k02/k04/k07 starts on this host. No third_impl run of these
three keys has been made by this lane before this push.

## Targets (published single-implementation rows, verdict NOT consumed)

| key | s5 state (lo,hi) | legal | published L50M row (replica jsreplay 84585617) |
| --- | --- | --- | --- |
| k02 | 1297036692683751424, 201326592 | 87 | WIN(1), nodes 18,123,017, cold pair node-identical |
| k04 | 1152921504607903744, 536903680 | 98 | LOSS(2), nodes 24,309,957, cold pair node-identical |
| k07 | 1152923703765368832, 68719476736 | 96 | WIN(1), nodes 27,621,128, cold pair node-identical |

## Pre-registered execution policy

- Engine: the standing third implementation `third_impl.js` (sha256
  08ea958ff59c3234ec5ac55c5c40689bd0999a34e101a88ea0546800cc4a1998,
  byte-clone of the published k12-win thirdimpl kit copy, byte-verified
  against its MANIFEST pin before this declaration).
- Inputs: `input/k02.input.csv` (8c2a0438...), `input/k04.input.csv`
  (dc3bfeb4...), `input/k07.input.csv` (928a1b98...) of the ninth-cost
  exclusive-probe kit, each byte-verified against the kit MANIFEST pins
  in `batch-summary-l50m.json` before this declaration.
- Protocol (k12 / seventh-cost batch precedent): cap=400000000,
  wallcap=260, memo-power=22, two fresh cold passes per key (one node
  process per pass, node_rc captured directly by the shell in the same
  command). Key order: k02, k04, k07.
- Pre-registered acceptance: verdict-level agreement with the published
  replica rows (k02 result 1 WIN, k04 result 2 LOSS, k07 result 1 WIN),
  legal derived == published legal, reason clean, node_rc=0, and the two
  cold passes per key identical on every field except wall_s => the row
  gains the third-impl pillar (single-implementation row remains
  adoption-gated). Any INDET / discarded / failed pass is disclosed, not
  silently rerun (honest-negative rule). Expansions are bookkeeping and
  are not expected to match the replica nodes.

## Freshness basis

Canonical head of record at declaration time: sha256
0935c94c03a9a3fbdf2a55aca90bb986a019dfd26c0097ab2c75709d590e9ca4
(`merged-exact-s5-chain-plus-eighthcost-k01-20261127.cache`, 6,875 rows
WIN 203 / LOSS 6,672, 287,808 bytes), fetched and byte-verified on this
host. Machine-checked: all three (lo,hi) pairs are ABSENT from the head
cache (3/3). No ninth-cost adoption Part has been published on main.

## Guards

Verdict NOT consumed. WIN(1)/LOSS(2) rows are single-implementation
cache-bookkeeping rows only: a third-impl agreement is not a class
closure claim, not a root verdict, and transfers nothing. The standard
11x11 empty board: UNKNOWN. All 19 central-reply roots: UNKNOWN.
Two-stone root {60,27}: UNKNOWN. Third-move pair {100,108}: UNKNOWN.
Every closure class: UNKNOWN unless a published Part says otherwise.
Nodes and expansions are never evidence of WIN or LOSS.
