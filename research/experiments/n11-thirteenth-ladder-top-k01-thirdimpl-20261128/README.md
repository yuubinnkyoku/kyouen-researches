# n11 thirteenth ladder-top k01 WIN-row third-implementation corroboration

Execution kit of the Part declared in
`research/log/2026-11-28-n11-thirteenth-ladder-top-k01-pillars-declaration.md`
(commit `c3cb9f7e`): the third-implementation corroboration pillar of
the thirteenth ladder-top escalation k01 WIN row (kit
`n11-thirteenth-ladder-top-escalation-20261128`, commit `12d8359c`).

## Result

- **CORROBORATION-PASS.**  third_impl.js (sha256 `08ea958f...`, the
  same pinned script as the standing thirdimpl kits, byte-fetched and
  sha-verified; not republished here), invoked with
  `--row=k01 --stones=5 --legal=72 --lo=1153204147814662144 --hi=65536
  --cap=400000000 --wallcap=260 --memo-power=22`, returns **result 1
  (A wins) with expansions 3,024,529, nodes 1,801,458, quads 95,670,
  ttOverwrites 44,704** on both fresh-cold passes (all fields
  identical except wall seconds 8.94 vs 8.90).  This is consistent
  with the escalation WIN(1) row (nodes 2,678,305 @15M budget,
  jsreplay single implementation).
- Expansions were MEASURED by this Part (not pre-registered),
  mirroring the u03/u04 pillar kits.
- The C++ scrutiny gate pillar is CLOSED by the companion kit
  `n11-thirteenth-ladder-top-k01-win-cppgate-20261128`
  (GATE-PASS `72,15000000,1,2678305`).  The two-pillar requirement
  for the k01 WIN row is now COMPLETE: verdict-level WIN(1) agreement
  across all three implementations.

## Files

- output/pillars-summary.json - machine summary (schema
  n11-thirteenth-ladder-top-k01-thirdimpl-summary-v1).
- output/ti/k01.p1.txt, output/ti/k01.p2.txt - the two cold passes.
- MANIFEST-sha256.txt - sha256 of every published file (excluding
  itself).

## Status guard

Verification bookkeeping only; NO verdict consumed.  The k01 WIN row
is cache bookkeeping, not a class closure, not a root verdict, and
transfers nothing until the adoption review completes.  Class 16757
completion additionally requires k02 (still 2M UNKNOWN) and
Board-verified free_now at adoption time.  The standard 11x11 empty
board, the two-stone root {60,27} and its remaining third moves
100/108 stay UNKNOWN.
