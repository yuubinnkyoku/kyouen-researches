# 2026-11-27 n11 eighth-cost k01 WIN third-impl corroboration complete

Wave B/C completion of the Part declared in
`research/log/2026-11-27-n11-eighthcost-k01-win-thirdimpl-corroboration-declaration.md`
(wave A commit 8914c50c). Kit:
`research/experiments/n11-eighthcost-k01-win-thirdimpl-corroboration-20261127/`.

## Outcome: CORROBORATION-PASS (verdict-level, fail-closed judgment as pre-registered)

third_impl.js (pinned 08ea958f, byte-clone from the Part SY kit) ran the
pre-registered invocation on k01 (`1297036692750860288:64`, legal 84,
cap=15000000, wallcap=260, memo-power=22) in two fresh cold passes:

- p1: result 1 (WIN), expansions 9,987,963, ttHits 5,498,898, legal derived
  84 = legalIn 84, reason clean.
- p2: identical values (expansions and ttHits exactly equal).

The replica (jsreplay 84585617) had reported WIN(1), nodes 8,514,427, cold
pair node-identical. Verdict-level agreement holds: both implementations
say k01 is WIN(1). Expansions/nodes are bookkeeping and are not compared
across implementations.

## Honest disclosures

1. The raw files carry an `rc=0` trailer whose provenance is the shell echo
   chain (an intervening echo reset $?), not a direct capture of the node
   process rc; the node rc=0 was observed on the console line in the same
   command. Disclosed in the kit README; values unaffected.
2. wall_s differs per pass (28.66 / 28.78); timing is not evidence.
3. The corroboration is ONE of the two pillars required before any
   adoption of the k01 WIN row; the C++ second-implementation scrutiny
   gate (expected quadruple 84,15000000,1,8514427) remains pending and is
   the next Part of this lane.
4. The verdict is NOT consumed: no cache increment, no class-status
   change, no coverage claim. The standard 11x11 empty board, all 19
   central-reply roots, the two-stone root {60,27}, the third-move pair
   {100,108} and every closure class remain UNKNOWN.
