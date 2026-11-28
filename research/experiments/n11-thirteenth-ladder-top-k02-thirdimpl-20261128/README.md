# n11 thirteenth ladder-top k02 WIN-row third-implementation corroboration

Execution kit of the Part declared in
`research/log/2026-11-28-n11-thirteenth-ladder-top-k02-pillars-declaration.md`
(commit `177b1086`): the third-implementation corroboration pillar
of the thirteenth ladder-top k02 escalation WIN row (kit
`n11-thirteenth-ladder-top-k02-escalation-20261128`, commit
`3087c38b`).

## Result

- **CORROBORATION-PASS.**  third_impl.js (sha256 `08ea958f...`, the
  same pinned script as the standing thirdimpl kits, byte-fetched and
  sha-verified; not republished here), invoked with
  `--row=k02 --stones=5 --legal=72 --lo=1152922672837951488
  --hi=65792 --cap=400000000 --wallcap=260 --memo-power=22`, returns
  **result 1 (A wins) with expansions 3,910,009, nodes 2,425,008,
  quads 95,670, ttOverwrites 268,071** on both fresh-cold passes
  (all fields identical except wall seconds 12.14 vs 12.04).  This is
  consistent with the k02 escalation WIN(1) row (nodes 3,485,963
  @15M budget, jsreplay single implementation).
- Expansions were MEASURED by this Part (not pre-registered),
  mirroring the u03/u04 pillar kits.
- The C++ scrutiny gate pillar is CLOSED by the companion kit
  `n11-thirteenth-ladder-top-k02-win-cppgate-20261128`
  (GATE-PASS `72,15000000,1,3485963`).  **Both class 16757 keys
  (k01 and k02) are now pillar-complete WIN rows**: verdict-level
  WIN(1) agreement across all three implementations for the entire
  class.

## Files

- output/pillars-summary.json (schema
  n11-thirteenth-ladder-top-k02-thirdimpl-summary-v1),
  output/ti/k02.p1.txt, output/ti/k02.p2.txt (the two cold passes),
  MANIFEST-sha256.txt (sha256 of every published file, excluding
  itself).

## Status guard

Verification bookkeeping only; NO verdict consumed.  The k02 WIN row
is cache bookkeeping, not a class closure, not a root verdict, and
transfers nothing until the adoption review completes.  A class
16757 adoption Part additionally requires the standing WIN-side
flip-census review and Board-verified free_now at adoption time.
The standard 11x11 empty board, the two-stone root {60,27} and its
remaining third moves 100/108 stay UNKNOWN.
