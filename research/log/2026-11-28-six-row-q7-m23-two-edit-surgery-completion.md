# 2026-11-28 six-row q7 6x23 two-edit surgery — completion

Single-owner lane declared in
`research/log/2026-11-28-six-row-q7-m23-two-edit-surgery-declaration.md`
(declaration commit `2affdf63`, declaration-time HEAD `2df06c1b`).
Kit: `research/experiments/six-row-q7-m23-two-edit-surgery-20261128`.

## Result: complete two-edit surgery negative at both placements; honest negative, not absence

- Seed: the published 6x22 witness (w67_22.json, 35 stones, rows
  [6,6,5,6,6,6], class {2} krow=2:5 minpos=7) on the 6x23 board, both
  placements.
- +1 shift, T=(0,2) (published shift1_on_m23.json uncovered cell):
  **777,360 unique candidates, 0 safe, 0 safe-maximal witnesses**.
- shift-0, T=(22,2) (machine-measured unique uncovered cell):
  **777,360 unique candidates, 0 safe, 0 witnesses**.
- Local negative only (edit distance <= 2 of either placement of the
  m=22 seed). **M_{6,7} stays in [23,402]; frontier stays 6x23.**
- **One-curve frontier** (recurring structure): T-curve census exactly
  {c4: 0, c5: 1} at both placements — the only curve through the
  frontier cell with >= 4 seed stones is the deficient row-2 line
  itself; the same pattern was measured the same day at the (7,7) 7x28
  frontier. All <= 2-edit blocking routes must complete the single
  deficient line and every completion fails safety. This recurring
  one-curve structure across families (with witness jumps sd 12..40)
  suggests frontier surgery needs >= 3 edits or a different seed
  family.

## Controls

- q=7 engine calibration byte-exact: `calib-m22.json` sha256
  `1ac7c6d84d7865e31cd6b18f87a4b4d42a53225cf154d2730d4fd5e66ff51d86`
  identical to the published `surgery-m22.run1.json`
  (six-row-q7-m22-two-edit-surgery-20261127), candidates 692,655 /
  safe 0 / witnesses 0, published m21 seed a84ace92...
- Determinism: run1/run2 sha256-identical both placements
  (`76312bac...`, `70f48e0d...`).
- Integer-conic spot-check 300/300 engine rejections confirmed, 0
  missed witnesses.

## Bookkeeping

- `results/fixed-width/mwq_stabilization.csv` (6,7) note extended
  (73,411 B -> 74,137 B, one line changed); range unchanged.
- Not done here: SAT-side continuation of the 6x23 class {2} minpos
  sweep (0..5, 9+) or classes {0}/{1}; no absence claim at any width.

## Non-claims

No 11x11 root / two-stone root {60,27} / third move {100,108} / S2 /
closure-class verdict is created, consumed, or transferred; all remain
UNKNOWN. Candidate counts are bookkeeping.
