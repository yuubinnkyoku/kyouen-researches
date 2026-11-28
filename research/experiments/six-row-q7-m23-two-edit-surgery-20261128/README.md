# Six-row q=7, 6x23: complete two-edit surgery, negative (2026-11-28 fast lane)

Single-owner lane declared in
`research/log/2026-11-28-six-row-q7-m23-two-edit-surgery-declaration.md`
(declaration commit `2affdf63`, declaration-time HEAD `2df06c1b`).

## Headline result

- The complete two-edit neighborhood (S' = seed - R + A, |R| <= 2,
  |A| <= 2, final size <= 35, A on empty cells, target cell T occupied
  or blocked) of the published 6x22 witness
  (`six-row-q7-m22-class-split-20261127/output/w67_22.json`, 35 stones,
  rows [6,6,5,6,6,6], class {2} krow=2:5 minpos=7) on the **6x23 board**
  contains **no safe row-deficient maximal configuration** at either
  placement:
  - +1 right-shift, T=(0,2) (the published shift1_on_m23.json uncovered
    cell): **777,360 unique candidates, 0 safe, 0 safe-maximal
    witnesses**;
  - shift-0, T=(22,2) (machine-measured unique uncovered cell):
    **777,360 unique candidates, 0 safe, 0 witnesses**.
- Local negative only: no 6x23 witness within edit distance <= 2 of
  either placement of the m=22 seed. NOT an absence claim for 6x23
  overall. **M_{6,7} stays in [23, 402]**; the frontier stays 6x23
  (class {2} k=5 minpos 6/7/8 pieces already published INDET at 262s
  caps).

## One-curve frontier (structural, recurring)

At both placements the T-curve census is exactly `{c4: 0, c5: 1}`: the
only curve through the frontier cell carrying >= 4 seed stones is the
deficient row-2 horizontal line itself (5 stones). The same pattern was
measured this session at the (7,7) 7x28 frontier (T-curve census
{c4: 0, c5: 1} at both placements of the 7x27 witness). Across the
q-deficient single-deficiency witnesses measured so far the frontier
cell is generically "one-curve": all <= 2-edit blocking routes must
complete the deficient line, and every completion fails safety. This
recurring structure is consistent with the large consecutive-width
witness jumps (sd 12..40) measured across all families and suggests
witness surgery needs >= 3 edits or a different seed family at these
frontiers.

## Engine, calibration, controls

- `surgery_general.py` sha256 `8ae82dde...b6b6b6a` — byte-clone of the
  six-row-q6-m26-two-edit-surgery-20261127 kit script (q/board
  parameterized, exact Fraction arithmetic, seed-safety and
  target-unblocked fail-closed asserts). Not re-published here; pinned
  by that kit's MANIFEST.
- **Calibration (byte-exact, q=7)**: the published 6x22 q7 surgery case
  (m=21 K0815 seed, T=(21,2)) reproduced byte-for-byte —
  `output/calib-m22.json` sha256
  `1ac7c6d84d7865e31cd6b18f87a4b4d42a53225cf154d2730d4fd5e66ff51d86`
  identical to the published `surgery-m22.run1.json`
  (six-row-q7-m22-two-edit-surgery-20261127), candidates 692,655 /
  safe 0 / witnesses 0.
- **Determinism**: run1/run2 sha256-identical at both placements
  (`76312bac...` shift+1, `70f48e0d...` shift-0).
- **Independent spot-check**: `spotcheck_int.py` (integer-conic,
  method-disjoint, sha256 `8f57d6b0...49ea`) on a seeded-random sample
  of 300 engine-rejected candidates: 300/300 rejections confirmed, 0
  missed witnesses.

## Files

- `output/seed6x23_shift{0,1}.json`: surgery seeds (shift-0 built from
  the published w67_22.json; shift+1 is the published
  shift1_on_m23.json).
- `output/surgery-m23.run{1,2}.json` (+ `.sample.jsonl`),
  `output/surgery-m23-s0.run{1,2}.json`: surgery outputs.
- `output/calib-m22.json`, `output/published-m22.json` (fetched
  published reference), `output/m21.stones.json` (calibration seed):
  byte-exact calibration chain.
- `output/spotcheck-summary.txt`, `output/records.jsonl`,
  `output/summary.json`.

## Non-claims

No 11x11 root / two-stone root {60,27} / third move {100,108} / S2 /
closure-class verdict is created, consumed, or transferred; all remain
UNKNOWN. Conflict/candidate counts are bookkeeping.
