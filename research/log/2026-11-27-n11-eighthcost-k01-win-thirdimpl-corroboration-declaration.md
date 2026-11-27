# 2026-11-27 n11 eighth-cost k01 WIN row third-implementation corroboration (declaration)

Wave A declaration of the third-implementation corroboration pillar for the
eighth-cost k01 WIN row (checkpoint:
`research/log/2026-11-27-n11-eighthcost-class1297036692750860288-probe-checkpoint.md`,
commit 0005e5b1).

## Target and pinned inputs

- Target: k01 (pos 1) key `1297036692750860288:64`, legal 84, stage-2 15M
  budget. Replica (jsreplay 84585617) cold pair: **WIN(1), nodes 8,514,427,
  pair node-identical** (published raws sha256 3be9db9b... each).
- Third implementation: the standing pinned `third_impl.js`
  (sha256 08ea958f...), byte-clone from the Part SY kit
  (research/experiments/n11-seventhcost-thirdimpl-corroboration-20261127/scripts/third_impl.js).
- Pinned invocation (Part SY runner form):
  `node third_impl.js --lo=1297036692750860288 --hi=64 --stones=5 --legal=84
  --row=k01.pN --cap=15000000 --wallcap=260 --memo-power=22`
  for N = 1, 2 (two fresh cold passes, one process per pass).

## Pre-registered judgment

Verdict-level agreement requires both passes to report result 1 (WIN) with
mutually identical expansion counts (the expansions field is bookkeeping;
verdict agreement is the corroboration claim). Any disagreement, crash, or
time-out is recorded as-is and the corroboration FAILS (fail-closed; no
retry harvesting). This is one of the two pillars required before any
adoption of the k01 WIN row; the C++ second-implementation scrutiny gate
(Part SR/SW/SX pattern) remains pending regardless of this outcome. The
verdict is NOT consumed either way.

## Guards

The standard 11x11 empty board: UNKNOWN. All 19 central-reply roots:
UNKNOWN. Two-stone root {60,27}: UNKNOWN. Third-move pair {100,108}:
UNKNOWN. Every closure class: UNKNOWN unless a published Part says
otherwise. A third-implementation WIN(1) agreement is not a class closure
claim, not a root verdict, and transfers nothing.
