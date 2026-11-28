# n11 seventeenth ladder-top k02 third-implementation corroboration

Execution kit of the third-implementation corroboration for the
seventeenth class 20421 k02 WIN row (`1156299204327378944:131072`,
class 20421, legal 73, s5_index 543795, WIN(1) nodes 4,997,146
@15M, seventeenth escalation kit
`n11-seventeenth-ladder-top-escalation-20261128`, declaration
`207339c8`, kit `bd63d669`, completion log `bd63d669`), declared
in `research/log/2026-11-28-n11-seventeenth-ladder-top-k02-pillars-declaration.md`
(commit `8e0e2c83`, single owner, publish-then-execute).

## Result

- `third_impl.js` (sha256 `08ea958f...`, the pinned standing third
  implementation, byte-verified local copy) with
  `--row=k02 --stones=5 --legal=73 --lo=1156299204327378944
  --hi=131072 --cap=400000000 --wallcap=260 --memo-power=22`:
  **result 1, expansions 5,731,617, nodes 3,309,634, quads 95,670,
  ttOverwrites 1,574,985 - identical on both cold passes**
  (wall_s 17.40 / 17.20, host timing only).
  **CORROBORATION-PASS**: result 1 is consistent with the
  published 15M WIN(1) row.
- With the companion C++ scrutiny gate kit
  (`n11-seventeenth-ladder-top-k02-win-cppgate-20261128`,
  GATE-PASS `73,15000000,1,4997146`), the two-pillar requirement
  for the k02 WIN row is COMPLETE: verdict-level WIN(1) agreement
  across all three implementations (jsreplay replica, C++ gate,
  third implementation).
- Adoption remains a separate declared Part (standing WIN-side
  flip-census review; owner union k02 [16104, 16132, 16656,
  20421]). Class 20421 is NOT complete (k03-k05 remain stage-1 2M
  UNKNOWN). NO verdict consumed. 11x11 UNKNOWN.
  nodes/expansions are bookkeeping and are not required to match
  across implementations.

## Files

- `output/pillars-summary.json` - machine-readable summary
  (schema `n11-seventeenth-ladder-top-k02-thirdimpl-summary-v1`).
- `output/ti/k02.p1.txt`, `output/ti/k02.p2.txt` - the two cold
  passes (identical except wall_s).
- `MANIFEST-sha256.txt` - sha256 of every kit file.
