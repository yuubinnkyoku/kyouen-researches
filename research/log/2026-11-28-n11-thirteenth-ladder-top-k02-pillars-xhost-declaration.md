# 2026-11-28 n11 thirteenth k02 pillars independent cross-host replication declaration

Single-owner declaration (publish-then-execute) for an independent
cross-host replication of BOTH verification pillars of the thirteenth
ladder-top k02 WIN row `1152922672837951488:65792` (class 16757,
legal 72, s5_index 558553, WIN(1) nodes 3,485,963 @15M, published in
`n11-thirteenth-ladder-top-k02-escalation-20261128`, commit `3087c38b`),
pillar-verified by the parallel lane in
`n11-thirteenth-ladder-top-k02-win-cppgate-20261128` (GATE-PASS
`72,15000000,1,3485963`) and
`n11-thirteenth-ladder-top-k02-thirdimpl-20261128`
(CORROBORATION-PASS, result 1, expansions 3,910,009, nodes 2,425,008,
quads 95,670, ttOverwrites 268,071) under declaration `177b1086`
(completion commit `7ebf903e`).  Pattern precedent: the k01 xhost
replication kit (this lane, `eb542121`).  This Part is disjoint from
any adoption Part.

## Pre-declaration scratch (disclosed)

This host already reproduced all three pinned anchors node-exactly in
the k01 xhost Part (at2m `98,2000000,0,2000000` raws byte-identical,
aj001 `84,30000000,2,5156075`, af039 `89,30000000,2,19234232`,
wall-only differences disclosed there).  The gate binary is the same
fresh zig 0.13.0 build (source `9193f5b6...` + headers
`5976935d...`/`2e36d694...`, tarball pin `d45312e6`, all sha-verified).
No k02 target run has happened on this host at any budget.

## What will be run (only after this declaration is on main)

1. C++ gate on k02 @15M cold pair.  Expected, pinned fail-closed from
   the published k02 escalation raw and cppgate kit:
   **`72,15000000,1,3485963`**.
2. third_impl.js `08ea958f...` (standing pin), `--row=k02 --stones=5
   --legal=72 --lo=1152922672837951488 --hi=65792 --cap=400000000
   --wallcap=260 --memo-power=22`, two fresh-cold passes.  Expected,
   pinned fail-closed from the published thirdimpl kit: result 1,
   expansions 3,910,009, nodes 2,425,008, quads 95,670,
   ttOverwrites 268,071.

Acceptance: XHOST-PASS only if the gate pair is node-identical and
matches the pinned expected value exactly, and the third_impl passes
are field-identical to each other and to the pinned published values
(wall seconds may differ).  Any mismatch is a HARD-STOP recorded as a
measured fact.

## Scope and guards

Only key `1152922672837951488:65792` at 15M (gate) and at the pinned
third_impl configuration may be run in this Part.  NO verdict is
consumed: this is a third-party determinism/replication check of
already-published pillar evidence.  The standard 11x11 empty board,
the 19 central-reply roots, the two-stone root {60,27} and third moves
100/108 stay UNKNOWN.  Nodes, expansions and wall seconds are
bookkeeping, never verdicts.

Execution begins only after this declaration is on main.
