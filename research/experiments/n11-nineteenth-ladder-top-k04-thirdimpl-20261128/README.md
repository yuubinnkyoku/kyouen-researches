# n11 nineteenth ladder-top k04 third-implementation corroboration

Execution kit of the third-implementation corroboration for the
nineteenth class 20421 k04 WIN row (`1153062242096250880:540672`,
class 20421, legal 83, s5 index 620742, WIN(1) nodes 6,877,739
@15M, nineteenth escalation kit `73cf1b2f`), declared in
`research/log/2026-11-28-n11-nineteenth-ladder-top-k04-pillars-declaration.md`
(commit `855d50fc`, single owner, publish-then-execute).

## Result

- `third_impl.js` (sha256 `08ea958f...`, the pinned standing third
  implementation, byte-verified local copy) with
  `--row=k04 --stones=5 --legal=83 --lo=1153062242096250880
  --hi=540672 --cap=400000000 --wallcap=260 --memo-power=22`:
  **result 1, expansions 7,920,095, nodes 4,544,365, quads 95,670,
  ttOverwrites 3,726,116 - identical on both cold passes**
  (wall_s 26.04 / 26.13, host timing only).
  **CORROBORATION-PASS**: result 1 is consistent with the
  published 15M WIN(1) row.
- With the companion C++ scrutiny gate kit
  (`n11-nineteenth-ladder-top-k04-win-cppgate-20261128`,
  GATE-PASS `83,15000000,1,6877739`), the two-pillar requirement
  for the k04 WIN row is COMPLETE: verdict-level WIN(1) agreement
  across all three implementations (jsreplay replica, C++ gate,
  third implementation).
- Adoption remains a separate declared Part (canonical merge +
  WIN-side flip-census/reaudit with owner union [18534, 18554,
  19885, 20421]; the serving class 20421 is already excluded_now).
  Class 20421 is NOT complete (k05 remains stage-1 2M UNKNOWN).
  NO verdict consumed. 11x11 UNKNOWN. nodes/expansions are
  bookkeeping and are not required to match across
  implementations.

## Files

- `output/pillars-summary.json` - machine-readable summary
  (schema `n11-nineteenth-ladder-top-k04-thirdimpl-summary-v1`).
- `output/ti/k04.p1.txt`, `output/ti/k04.p2.txt` - the two cold
  passes (identical except wall_s).
- `MANIFEST-sha256.txt` - sha256 of every kit file.

The runner `third_impl.js` itself is not included in the kit; it
is referenced by its standing sha256 pin `08ea958f...`
(byte-verified local copy used for the published passes).
