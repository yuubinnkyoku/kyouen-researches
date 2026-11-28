# n11 fifteenth ladder-top k02 third-implementation corroboration

Execution kit of the third-implementation corroboration for the
fifteenth class 5804 k02 WIN row (`6052837899185946628:128`,
class 5804, legal 87, s5_index 212115, WIN(1) nodes 18,247,029
@50M, L50M escalation kit
`n11-fifteenth-ladder-top-k02-l50m-escalation-20261128`, commits
declaration `5cc8e1fb` / kit+log `48ea76d8`), declared in
`research/log/2026-11-28-n11-fifteenth-ladder-top-k02-pillars-declaration.md`
(commit `66bb19d1`, single owner, publish-then-execute).

## Result

- `third_impl.js` (sha256 `08ea958f...`, the pinned standing third
  implementation, byte-verified local copy) with
  `--row=k02 --stones=5 --legal=87 --lo=6052837899185946628 --hi=128
  --cap=400000000 --wallcap=260 --memo-power=22`:
  **result 1, expansions 21,587,934, nodes 11,683,592,
  quads 95,670, ttOverwrites 17,393,630 - identical on both cold
  passes** (wall_s 63.70 / 63.75, host timing only).
  **CORROBORATION-PASS**: result 1 is consistent with the
  published L50M WIN(1) row.
- With the companion C++ scrutiny gate kit
  (`n11-fifteenth-ladder-top-k02-win-cppgate-20261128`,
  GATE-PASS `87,50000000,1,18247029`), the two-pillar requirement
  for the k02 WIN row is COMPLETE: verdict-level WIN(1) agreement
  across all three implementations (jsreplay replica, C++ gate,
  third implementation).
- Adoption remains a separate declared Part (standing WIN-side
  flip-census review). Class 5804 is NOT complete until the k02
  adoption Part (it stays excluded_now regardless). NO verdict
  consumed. 11x11 UNKNOWN.

## Files

- `output/pillars-summary.json` - machine-readable summary
  (schema `n11-fifteenth-ladder-top-k02-thirdimpl-summary-v1`).
- `output/ti/k02.p1.txt`, `output/ti/k02.p2.txt` - the two cold
  passes (identical except wall_s).
- `MANIFEST-sha256.txt` - sha256 of every kit file.
