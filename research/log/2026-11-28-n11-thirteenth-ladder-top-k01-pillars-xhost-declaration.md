# 2026-11-28 n11 thirteenth k01 pillars independent cross-host replication declaration

Single-owner declaration (publish-then-execute) for an independent
cross-host replication of BOTH verification pillars of the thirteenth
ladder-top k01 WIN row `1153204147814662144:65536` (class 16757,
legal 72, WIN(1) nodes 2,678,305 @15M), originally published in
`n11-thirteenth-ladder-top-escalation-20261128` (`12d8359c`) and
pillar-verified in `n11-thirteenth-ladder-top-k01-win-cppgate-20261128`
and `n11-thirteenth-ladder-top-k01-thirdimpl-20261128` (commit
`f1f5c49d`, log `8dcb00fd`, owned by another lane).  Precedent: the
ultra-cheap u04 C++ gate cross-host replication kit
(`580be905`, XHOST-PASS).  This Part is disjoint from the k02
escalation declaration `b9c97423` and from any adoption Part.

## Pre-declaration scratch (disclosed)

On this host the gate source was freshly fetched and sha-verified
(`kyouen_dfpn_root.cpp` `9193f5b6...`, `kyouen_residual_micro.hpp`
`5976935d...`, `n11_s5_quarantine.hpp` `2e36d694...`), built with
zig 0.13.0 (tarball pin `d45312e6...`, verified), `-std=c++20 -O2`.
The three pinned anchors were run as scratch, cold pairs, and all
reproduce the published anchor values node-exactly: anchor-at2m
`98,2000000,0,2000000`, anchor-aj001 `84,30000000,2,5156075`,
anchor-af039 `89,30000000,2,19234232`.  No k01 target run has
happened yet on this host at any budget.

## What will be run (only after this declaration is on main)

1. C++ gate (this host's fresh zig 0.13.0 build) on k01 @15M cold pair.
   Expected, pinned fail-closed from the published escalation raw and
   the published cppgate kit: `72,15000000,1,2678305`.
2. third_impl.js (sha256 `08ea958f...`, the standing pin, byte-fetched
   and sha-verified), `--row=k01 --stones=5 --legal=72
   --lo=1153204147814662144 --hi=65536 --cap=400000000 --wallcap=260
   --memo-power=22`, two fresh-cold passes.  Expected, pinned
   fail-closed from the published thirdimpl kit: result 1, expansions
   3,024,529, nodes 1,801,458, quads 95,670, ttOverwrites 44,704.

Acceptance: XHOST-PASS only if every gate pair is node-identical and
matches the pinned expected values exactly (wall seconds may differ);
third_impl passes must be field-identical to each other and to the
pinned published values (wall seconds may differ).  Any mismatch is a
HARD-STOP recorded as a measured fact; nothing is reinterpreted.

## Scope and guards

Only key `1153204147814662144:65536` at 15M (gate) and at the pinned
third_impl configuration, plus the three disclosed anchors, may be run
in this Part.  NO verdict is consumed: this is a third-party
determinism/replication check of already-published pillar evidence.
The standard 11x11 empty board, the 19 central-reply roots, the
two-stone root {60,27} and third moves 100/108 stay UNKNOWN.  Nodes,
expansions and wall seconds are bookkeeping, never verdicts.

Execution begins only after this declaration is on main.
