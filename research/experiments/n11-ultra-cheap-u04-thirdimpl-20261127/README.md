# n11 ultra-cheap u04 WIN-row third-implementation corroboration

Execution kit of the Part declared in
`research/log/2026-11-27-n11-ultra-cheap-u04-thirdimpl-declaration.md`
(commit `f2210464`): the third-implementation corroboration pillar of
the u04 escalation WIN row (kit
`n11-ultra-cheap-u04-escalation-15m-20261127`, commit `24c5b85f`).

## Result

- **CORROBORATION-PASS.**  third_impl.js (sha256 `08ea958f...`, the
  same pinned script as the u01/u02/u03 pillar kits, byte-fetched and
  sha-verified; not republished here), invoked with
  `--row=u04 --stones=5 --legal=85 --lo=1152921505747697664 --hi=1032
  --cap=400000000 --wallcap=260 --memo-power=22`, returns **result 1
  (A wins) with expansions 10,728,035, nodes 5,758,042, quads 95,670,
  ttOverwrites 6,533,731** on both fresh-cold passes (all fields
  identical except wall seconds 32.02 vs 32.46).  This is consistent
  with the escalation WIN(1) row (nodes 9,149,084 @15M budget,
  jsreplay single implementation).
- Expansions were MEASURED by this Part (not pre-registered),
  mirroring the u03 pillar kit.

## Honest disclosure: the C++ scrutiny gate pillar stays OPEN

This environment has no C/C++ toolchain and package installation is
forbidden, so the C++ second-implementation scrutiny gate could NOT
be executed here (the gate source `9193f5b6...` was byte-fetched and
sha-verified, but cannot be compiled; it was previously built via
zig 0.13.0, tarball pin `d45312e6`).  The gate pillar remains REQUIRED
and OPEN: the u04 row MAY NOT be adopted until a GATE-PASS kit for
this row exists (expected `85,15000000,1,9149084` cold pair, plus the
published anchor set and the 4/4 tamper battery, per the u03 pillars
kit protocol).  This Part claims only the third-implementation
corroboration and does not weaken the two-pillar requirement.

## Files

- output/pillars-summary.json - machine summary (schema
  n11-ultra-cheap-u04-thirdimpl-summary-v1).
- output/ti/u04.p1.txt, output/ti/u04.p2.txt - the two cold passes.
- MANIFEST-sha256.txt - sha256 of every published file (excluding
  itself).

## Status guard

Verification bookkeeping only; NO verdict consumed.  The u04 WIN row
is cache bookkeeping, not a class closure, not a root verdict, and
transfers nothing until BOTH pillars and the adoption review complete.
The standard 11x11 empty board, the two-stone root {60,27} and its
remaining third moves 100/108 stay UNKNOWN.
