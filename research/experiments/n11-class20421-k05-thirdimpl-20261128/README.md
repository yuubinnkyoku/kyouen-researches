# n11 class-20421 k05 third-implementation corroboration

Execution kit of the third-implementation corroboration for the
class-20421 k05 WIN row (`1152921642046849024:68719477248`,
class 20421, legal 78, s5 index 625899, WIN(1) nodes 2,007,513
@15M, class20421-k05 escalation kit `9a87750e`), declared in
`research/log/2026-11-28-n11-class20421-k05-pillars-declaration.md`
(commit `772c04bc`, single owner, publish-then-execute).

## Result

- `third_impl.js` (sha256 `08ea958f...`, the pinned standing third
  implementation, byte-verified local copy) with
  `--row=k05 --stones=5 --legal=78 --lo=1152921642046849024
  --hi=68719477248 --cap=400000000 --wallcap=260 --memo-power=22`:
  **result 1, expansions 2,292,427, nodes 1,279,838, quads 95,670,
  ttOverwrites 3,031 - identical on both cold passes**
  (wall_s 7.09 / 7.27, host timing only).
  **CORROBORATION-PASS**: result 1 is consistent with the
  published 15M WIN(1) row.
- With the companion C++ scrutiny gate kit
  (`n11-class20421-k05-win-cppgate-20261128`, GATE-PASS
  `78,15000000,1,2007513`), the two-pillar requirement for the
  k05 WIN row is COMPLETE: verdict-level WIN(1) agreement across
  all three implementations (jsreplay replica, C++ gate, third
  implementation).
- Adoption remains a separate declared Part (canonical merge to
  expected 6,905 rows WIN 223 / LOSS 6,682, merger `90711961`,
  maker + tamper) followed by the WIN-side flip-census/reaudit
  measuring the class-20421 closure-ladder EXIT (owner union
  [18683, 18710, 20421], the serving class 20421 rank 1
  unknown_now 1 -> 0 expected, with the standing pre-exclusion
  caveat on the serving class). NO verdict consumed. 11x11
  UNKNOWN. nodes/expansions are bookkeeping and are not required
  to match across implementations.

## Files

- `output/pillars-summary.json` - machine-readable summary
  (schema `n11-class20421-k05-thirdimpl-summary-v1`).
- `output/ti/k05.p1.txt`, `output/ti/k05.p2.txt` - the two cold
  passes (identical except wall_s).
- `MANIFEST-sha256.txt` - sha256 of every kit file.

The runner `third_impl.js` itself is not included in the kit; it
is referenced by its standing sha256 pin `08ea958f...`
(byte-verified local copy used for the published passes).
