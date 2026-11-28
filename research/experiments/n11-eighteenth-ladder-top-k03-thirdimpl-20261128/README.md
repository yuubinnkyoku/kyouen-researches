# n11 eighteenth ladder-top k03 third-implementation corroboration

Execution kit of the third-implementation corroboration for the
eighteenth class 20421 k03 WIN row (`1155173441859489792:131072`,
class 20421, legal 73, s5_index 605961, WIN(1) nodes 5,266,012
@15M, eighteenth escalation kit `88e825d5`), declared in
`research/log/2026-11-28-n11-eighteenth-ladder-top-k03-pillars-declaration.md`
(commit `26143236`, single owner, publish-then-execute).

## Result

- `third_impl.js` (sha256 `08ea958f...`, the pinned standing third
  implementation, byte-verified local copy) with
  `--row=k03 --stones=5 --legal=73 --lo=1155173441859489792
  --hi=131072 --cap=400000000 --wallcap=260 --memo-power=22`:
  **result 1, expansions 6,039,011, nodes 3,524,008, quads 95,670,
  ttOverwrites 1,865,863 - identical on both cold passes**
  (wall_s 18.29 / 17.77, host timing only).
  **CORROBORATION-PASS**: result 1 is consistent with the
  published 15M WIN(1) row.
- With the companion C++ scrutiny gate kit
  (`n11-eighteenth-ladder-top-k03-win-cppgate-20261128`,
  GATE-PASS `73,15000000,1,5266012`), the two-pillar requirement
  for the k03 WIN row is COMPLETE: verdict-level WIN(1) agreement
  across all three implementations (jsreplay replica, C++ gate,
  third implementation).
- Adoption remains a separate declared Part (standing WIN-side
  flip-census review; owner union k03 [18136, 18143, 20128,
  20421]). Class 20421 is NOT complete (k04-k05 remain stage-1 2M
  UNKNOWN). NO verdict consumed. 11x11 UNKNOWN.
  nodes/expansions are bookkeeping and are not required to match
  across implementations.

## Files

- `output/pillars-summary.json` - machine-readable summary
  (schema `n11-eighteenth-ladder-top-k03-thirdimpl-summary-v1`).
- `output/ti/k03.p1.txt`, `output/ti/k03.p2.txt` - the two cold
  passes (identical except wall_s).
- `MANIFEST-sha256.txt` - sha256 of every kit file.
