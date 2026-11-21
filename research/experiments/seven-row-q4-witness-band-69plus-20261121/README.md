# Seven-row q=4 witness band extension: width 69 (2026-11-21)

Single-owner lane declared in
`research/log/2026-11-21-seven-row-q4-band-m69-single-owner-note.md`
(declaration HEAD `94fe399ca6`, publication commit chain below).

## Headline result

- **No width-69 witness exists in the complete fresh 2-for-2 replacement
  neighborhood of ALL 199 published bases** (the deduplicated pool of
  `seven-row-q4-witness-band-60plus-20261121/output/w68/bases.json`:
  anchors base53/B59/w57_0/w57_1/sa42..53 lines/sa45/w60_a..d plus every chain
  witness of widths 61..67 plus the width-68 witness's bases pool).
  Totals: 426,099,795 row-capacity candidates / 43,009,353 safe / 0 safe
  maximal row-deficient.
- **The holes-mode 2-for-2 sweep (strict superset neighborhood: refilling the
  removed stones' cells is additionally allowed) over the same 199 bases also
  gives 0 witnesses.** Totals: 435,695,973 / 45,368,697 / 0.
- **1-for-0 direct maximality checks** (remove one stone from a base, test the
  remaining 19 stones as a row-deficient maximal configuration on 7x69, both
  deficient rows' full coverage): 3,980 configurations (199 bases x 20
  removals), 0 maxima. Checker validated by positive/negative controls
  (`output/w69/selftest_1f0.json`).
- This is a **complete finite negative for the (fresh + holes) 2-for-2
  replacement neighborhoods of all 199 published bases at width 69**, plus the
  1-for-0 removal neighborhood. It is NOT a width-69 absence claim: candidates
  outside these neighborhoods (3-edit or larger surgery, seeded SA, other
  seeds, other stone counts) remain open. **M_{7,4} stays in [69, 1929]**;
  the frontier remains 7x69. The upper bound 1929 (K0068) is unchanged.

This closes two of the four candidate moves listed in K0827 for the 7x69
frontier ("frontier の breadth 拡大" and "holes モード併用"); 3-for-3
neighborhoods and seeded SA remain untried.

## Method

- `scripts/enum_two.js`: byte-identical copy of the pinned engine from
  `seven-row-q4-witness-band-60plus-20261121/scripts/enum_two.js`
  (sha256 `ab58c34a75a752a28e4898b118a52292d79484341e7c64a2fa56eb02b8913169`,
  identical for both files). Exact integer geometry only (4x4 circle
  determinant, inclusion-exclusion, per-removal-pair blocking bitmaps).
- `scripts/sweep69.js`: width-parameterized driver for the fresh and holes
  2-for-2 sweep over the pooled bases, with the 1-for-0 check integrated.
  Auto-resume by base signature; per-base records appended to
  `output/w69/<mode>/results.jsonl` (rcc/safe/shape_errors/maximal and the
  1-for-0 counts are deterministic; the `ms` fields are informal wall clock).
- `scripts/selftest_1f0.js`: positive control (the published width-68 witness is
  maximal on 7x68) and negative control (same minus one stone is not maximal,
  first unblocked cell identified) for the 19-stone maximality checker.
- `scripts/calibrate69.js`: regenerates `output/calibration.json` and
  `output/summary.json`, re-verifying every published reference value:
  1. engine: base53 on 7x57 = 1,436,643 / 60,921 / 2 (pinned audit values);
  2. engine: the published width-68 witness's width-69 fresh neighborhood =
     2,141,205 / 199,290 / 0 (matches the published `stats_69.json` exactly);
  3. driver at W=68: 11 published per-base records reproduced
     (first 8 plus the three positive w65-tagged bases),
     and all three positive bases re-yield the published unique width-68
     witness stone-for-stone;
  4. holes semantics at W=60 on w57_0: the fresh 4 witnesses (identical to the
     published `wit_w57_0_60.json`) are a subset of the 23 holes witnesses;
     fresh counts match the published record;
  5. 1-for-0 self-test PASS.
  All 5 calibration blocks PASS (`output/calibration.json`,
  `overall_pass: true`). A determinism spot check (one base run twice,
  deep-equal counts and witness arrays) is recorded in the session log.
- `input/bases.json`: byte copy of the published pool
  (sha256 `d8e977ec3152346a53ae10090af2566abbc3d99743d8723c872c69678f060f04`).

## Reproduction

Run from this directory:

```sh
node scripts/sweep69.js 69 fresh 0 45   # repeat until totalDone = 199
node scripts/sweep69.js 69 holes 0 40   # repeat until totalDone = 199
node scripts/selftest_1f0.js
node scripts/calibrate69.js
```

Expected totals are in `output/summary.json`; the width-68/57/60 calibration
equalities re-verify against the published files noted above (fetch them from
`seven-row-q4-witness-band-60plus-20261121` at the pinned revision).

## Honest scope

- The 2-for-2 enumerations are complete fresh+holes replacement neighborhoods
  of the 199 stated bases at width 69 only. Larger neighborhoods, other bases,
  other stone counts (beyond the checked 20- and 19-stone shapes), and 3-edit
  surgery are NOT covered. No absence claim is made for width 69 overall.
- All geometry is exact integer arithmetic; no floating point, no randomness.
- K0827 is not updated by this batch (no witnesses found); this experiment and
  the session log are the record of the honest negative.
