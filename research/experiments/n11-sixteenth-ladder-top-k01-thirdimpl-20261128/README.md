# n11 sixteenth ladder-top k01 third-implementation corroboration

Execution kit of the third-implementation corroboration for the
sixteenth class 20421 k01 WIN row (`1155454779397246976:131072`,
class 20421, legal 76, s5_index 528689, WIN(1) nodes 5,273,778 @15M,
sixteenth escalation kit `n11-sixteenth-ladder-top-escalation-20261128`,
declaration `4d361b73`, kit `85edd462`, completion log `775e1a6f`),
declared in `research/log/2026-11-28-n11-sixteenth-ladder-top-k01-pillars-declaration.md`
(commit `60f4bac8`, single owner, publish-then-execute).

## Result

- `third_impl.js` (sha256 `08ea958f...`, the pinned standing third
  implementation, byte-verified local copy) with
  `--row=k01 --stones=5 --legal=76 --lo=1155454779397246976 --hi=131072
  --cap=400000000 --wallcap=260 --memo-power=22`:
  **result 1, expansions 6,003,522, nodes 3,591,656,
  quads 95,670, ttOverwrites 1,831,190 - identical on both cold
  passes** (wall_s 18.85 / 19.47, host timing only).
  **CORROBORATION-PASS**: result 1 is consistent with the
  published 15M WIN(1) row.
- With the companion C++ scrutiny gate kit
  (`n11-sixteenth-ladder-top-k01-win-cppgate-20261128`,
  GATE-PASS `76,15000000,1,5273778`), the two-pillar requirement
  for the k01 WIN row is COMPLETE: verdict-level WIN(1) agreement
  across all three implementations (jsreplay replica, C++ gate,
  third implementation).
- Adoption remains a separate declared Part (standing WIN-side
  flip-census review). Class 20421 is NOT complete (k02-k05 remain
  stage-1 2M UNKNOWN). NO verdict consumed. 11x11 UNKNOWN.
  nodes/expansions are bookkeeping and are not required to match
  across implementations.

## Files

- `output/pillars-summary.json` - machine-readable summary
  (schema `n11-sixteenth-ladder-top-k01-thirdimpl-summary-v1`).
- `output/ti/k01.p1.txt`, `output/ti/k01.p2.txt` - the two cold
  passes (identical except wall_s).
- `MANIFEST-sha256.txt` - sha256 of every kit file.
