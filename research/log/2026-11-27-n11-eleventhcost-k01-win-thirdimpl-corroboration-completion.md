# 2026-11-27 n11 eleventh-cost k01 WIN third-impl corroboration completion

Completion log of the Part declared at commit 83804e01.  Kit:
`research/experiments/n11-eleventhcost-k01-win-thirdimpl-corroboration-20261127/`
(commit 26c7b04d, 5 files).

## Result: CORROBORATION-PASS (verdict-level)

- k01 `1297036696978718720:64`: third_impl.js (standing pin 08ea958f,
  byte-verified on this host) resolved **result 1 (WIN)** in both
  fresh cold passes, expansions 15,339,759 and ttHits 8,124,169
  mutually identical, reason clean, cap 400,000,000, wallcap 260,
  memoPower 22, node_rc=0 in both raws.  Wall 42.97 / 43.28 (timing is
  not evidence).
- Replica agreement: jsreplay 84585617 WIN(1) nodes 12,755,963 (cold
  pair node-identical, batch kit aaeb282c).  Verdict-level agreement
  across the two independent implementations.
- No exploratory lower-cap pass was needed (both passes clean at
  first attempt, disclosed in the kit README).

## Position

The k01 WIN row now has one of its two pillars.  Remaining before any
adoption: the C++ second-implementation scrutiny gate (expected
quadruple 88,15000000,1,12755963; gate source pin 9193f5b6 @154f3b7a
with headers, zig 0.13.0, SW/SX/tenth-gate lineage), then the
canonical adoption Part with WIN-side flip-census/reaudit review
(serving class 1297036696978718720:0 owner set).

## Guards

Pillar bookkeeping only; the verdict is NOT consumed: no cache
increment, no class-status change, no coverage claim, no adoption.
The standard 11x11 empty board: UNKNOWN.  All 19 central-reply
roots: UNKNOWN.  Two-stone root {60,27}: UNKNOWN.  Third-move pair
{100,108}: UNKNOWN.
