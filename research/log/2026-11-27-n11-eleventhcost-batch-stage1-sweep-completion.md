# 2026-11-27 n11 eleventh-cost batch stage-1 sweep completion

Completion log of the eleventh-cost batch declared in
`research/log/2026-11-27-n11-eleventhcost-batch-stage1-sweep-declaration.md`
(wave A commit 8fbccf0b), executed publish-then-execute on this host.
Kit: `research/experiments/n11-eleventhcost-batch-stage1-2m-20261127/`
(commit aaeb282c, 97 files).  Selection kit:
`research/experiments/n11-eleventhcost-class-s5-exclusive-probe-20261127/`
(commits 56787fe0 / f8dd2c81; scripts restored at 89c75c00 after the
parallel lane's stale-index rebuild incident, byte-identical).

## Measured results (all finite observations; verdict NOT consumed)

- Stage-1 sweep: all 46 exclusive S5 keys of class
  `1297036696978718720:0` are UNKNOWN at the 2,000,000-budget cold
  pair (result 0, nodes 2,000,000).  46/46 cold pairs node-identical
  (92 raws).
- 15M escalation (interleaved key order, WIN-stopping rule active):
  **k01 `1297036696978718720:64` resolves WIN(1) at nodes 12,755,963**
  (cold pair node-identical, raws at15m-k01-p1/p2.raw, wall ~68s/run).
  The WIN stopping rule fired immediately: k02..k46 stay UNKNOWN at
  2M, escalation-suppressed, no overreach (no suppressed key was run
  at any higher budget).
- Node/expansion counts are bookkeeping, never evidence of WIN or
  LOSS.

## Pillar status and next work

The k01 WIN row is single-implementation (Node.js replica jsreplay
84585617...).  Before any adoption it requires, per the standing
pillar rules (tenth-cost k01/k02 precedent):
1. C++ second-implementation scrutiny gate (expected quadruple
   88,15000000,1,12755963; gate source pin 9193f5b6 @154f3b7a, zig
   0.13.0, SW/SX/tenth-gate lineage).
2. Third-implementation corroboration (standing third_impl 08ea958f,
   cap >= 15M runlimit-adequate budget per the k12 precedent, 2 cold
   passes).
3. Canonical adoption Part (fresh single-owner declaration, BASE
   head 16b34014..., WIN/LOSS conflict review, merger 90711961) with
   a WIN-side flip-census/reaudit review of the serving class
   `1297036696978718720:0` owner set (Part SZ/ninth/tenth precedent).

## Honest disclosures

- Pre-declaration k01 2M sanity run (disclosed in wave A): result 0,
  nodes 2,000,000, UNKNOWN; the published at2m-k01 pair is the
  official fresh pair.
- During this Part a parallel lane's stale-index rebuild dropped
  3,730 repo files (incident commits 1a1d337be/66e11623/b29b025f);
  this lane's selection kit lost scripts/select_eleventh_exclusive.py
  and scripts/jsreplay.js, which were republished byte-identical at
  89c75c00 (all other kit files verified present byte-identical).
- This lane runs without access to the user's computer (scheduled
  task); publication is via the GitHub API only.  Unauthenticated
  GitHub API rate limit was exhausted mid-Part; fetch-back used the
  raw CDN with propagation-delay retries.

## Guards

Scheduling/batch bookkeeping only: NO verdict is claimed or implied.
The standard 11x11 empty board: UNKNOWN.  All 19 central-reply roots:
UNKNOWN.  The two-stone root {60,27} and its remaining third moves
100/108: UNKNOWN.  The k01 WIN row is a cache-bookkeeping row, not a
class closure, not a root verdict, and transfers nothing.
