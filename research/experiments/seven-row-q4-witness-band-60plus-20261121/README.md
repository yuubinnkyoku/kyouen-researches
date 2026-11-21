# Seven-row q=4 witness band extension: widths 60+ (2026-11-21)

Single-owner lane declared in `research/log/2026-11-21-seven-row-q4-band-m60-single-owner.md`.
Goal: extend the 7-row q=4 unsafe deficient-maximal witness band beyond the
previously published width-59 end point (`seven-row-q4-width59-two-swap-20261115`),
raising the lower bound of M_{7,4}.

## Headline result

- Width-60 witnesses exist: the fresh-cell 2-for-2 neighborhood of the width-57
  witness A57 (`w57_0`) on the 7x60 board contains exactly 4 safe row-deficient
  maxima (verified), and the holes-complete 2-for-2 neighborhood contains more.
  Since the pinned 2026-11-15 audit tested only base53 and foundB at width 60,
  this closes the gap the previous lane left open.
- Chained 2-for-2 extension then reaches widths 61..67 (see `output/chain/`),
  so **M_{7,4} >= 68**, improving the previous band M_{7,4} ∈ [60, 1929] to
  **M_{7,4} ∈ [68, 1929]**. The upper bound is unchanged.

## Method

- `scripts/enum_two.js`: complete 2-for-2 replacement enumeration, exact
  integer geometry only (4x4 circle determinant; inclusion-exclusion for the
  neighborhood; per-removal-pair blocking bitmaps). Fresh-cell mode
  reproduces the pinned C++ audit byte-for-byte:
  - base53 on 7x57: row_capacity_candidates=1436643, safe=60921, maxima=2
    (both published witnesses reproduce identically),
  - base53 on 7x60: 1599648 / 83225 / 0,
  - foundB on 7x60: 1599648 / 110748 / 0.
  `--holes` mode also permits refilling the two removed stones' positions
  (strict superset of the pinned enumeration).
- `scripts/verify_witnesses.py`: independent exact verifier using normalized
  integer line/circle equations (system #2), generalized from the pinned
  verifier of `seven-row-q4-width59-two-swap-20261115`. Verifies: 20 distinct
  stones, row counts [3,3,3,3,3,3,2], no line/circle through 4 stones, and
  every empty deficient-row cell blocked by a 3-stone line/circle.
- `scripts/verify_third.py`: third independent system, pure brute force with
  direct 4x4 determinants |x y x^2+y^2 1| over all quadruples / all
  triple-cell combinations (record: `output/third_verify.json`).
  The 13 anchor + representative witnesses (A57, B59, 4x width 60,
  7x widths 61..67) pass all systems.

## Outputs

- `output/calibration.json`: pinned-audit calibration numbers.
- `output/w60/wit_w57_0_60.json`: width-60 sweep of the A57 base,
  fresh-cell mode; 4 witnesses (all stones listed).
- `output/w60/other_bases.jsonl`: for every other pooled base
  (base53/foundB/sa42..53 lines), the width-60 fresh 2-for-2 sweep gives
  0 safe row-deficient maxima (honest negative within those neighborhoods).
- `output/verification_m60.json`: system #2 verification of the pinned
  anchors A57, B59 and the four width-60 witnesses.
- `output/chain/`: chained 2-for-2 witnesses per width 61..67 plus chain
  statistics (`frontier_W.json`, `stats_W.json`, `witness_W.json`). Each
  chain step uses only kept witnesses of width W-1 as bases for width W,
  fresh-cell mode, greedy frontier cap 10 sorted by max stone x. At width 68
  the final 2 frontier witnesses of width 67 yield 0 witnesses
  (`frontier_68.json`, `stats_68.json`): the chain stops there within
  this greedy policy (no absence claim at width 68 overall).
- `output/chain/verification_chain.json`: system #2 verification of one
  representative witness per chain width (61..67).
- `output/third_verify.json`: system #3 verification record of the same
  witness set (all pass).

## Honest limits

- All enumerations are 2-for-2 replacement neighborhoods of the stated bases
  only. No claim is made that width-63+ witnesses do not exist outside them,
  and no claim is made at widths where the chain stopped (67 within the
  explored greedy frontier).
- Upper bound 1929 unchanged; witness type is the def-mode 20-stone
  unsafe-maximal configuration as in K0827.
