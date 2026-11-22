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

## Batch 2 - restricted fresh 3-for-3 (in progress, checkpoint publication)

Declared in `research/log/2026-11-21-seven-row-q4-band-m69-batch2-restricted-3edit-single-owner-note.md`
(declaration HEAD `b1f82cc3`). Checkpoint of the same single-owner lane; the swept
fraction is stated below and NO completed-neighborhood negative claim is made yet.

- Search space: complete fresh 3-for-3 replacement neighborhoods (remove exactly 3
  stones, add exactly 3 cells NOT in the base, within window columns x >= 52 at width
  69; final shape exactly [3,3,3,3,3,3,2]) of all 199 published bases plus the
  width-68 witness as seed, priority w65 -> w66 -> pool anchors -> w61..w64 -> w68witness.
  A verified width-69 witness would move K0827 and the README headline to
  M_{7,4} in [70, 1929].
- Engine `scripts/enum_three.js`: exact integer geometry, reuses the pinned
  `enum_two.js` Board unchanged. Safety case split complete ({1 add + 3 kept}
  skip-masked badT, {2 add + 2 kept} badP, {3 add + 1 kept} direct 4x4 determinant
  without growing the shared curve cache, base-safety precondition). Maximality case
  split complete over EVERY deficient-row empty cell including removed base cells:
  {3 kept} remBlocked, {1 add + 2 kept} coverBy recorded for all targets (a deliberate
  difference to pinned fresh-mode enum_two, whose occupied-target skip was immaterial
  for batch 1 because the holes superset run also returned 0), {2 add + 1 kept} key3
  curve marks, {3 add} determinant.
- Calibration (11 controls, all PASS, `output/w69/three/calibration.json`, runner
  `scripts/three_control.js`):
  A positive known-answer: the published width-68 witness is re-found via the
  holes-refill control mode at window x >= 52 (24,657 / 13,954 / 7 maximal,
  including the published witness itself);
  B window negative x >= 56 (0 re-found; 770 / 256 / 1);
  C unsafe-base guard throws; D determinism (counters + witnesses byte-equal across
  reruns); E fresh-mode join run (20,128 / 11,737 / 0);
  F all emitted witnesses pass the independent brute 4x4-determinant + triple-curve
  maximality re-judge (7/7);
  G window monotonicity (all B counters <= corresponding A counters);
  H naive independent exhaustion cross-check at window x >= 56: 31,932 holes combos
  and 27,072 fresh combos fully re-judged by the brute third-system verifier, maximal
  sets exactly equal to the engine's in both modes;
  I fresh structural invariant |final & base| = 17 (in fresh mode a 3-edit candidate
  cannot degenerate to 2-for-2; also asserted at production save time).
- Driver `scripts/sweep_three.js`: budget-chunked with per-base append to
  `output/w69/three/results.jsonl` and resumable `output/w69/three/state.json`;
  budget-exceeding bases are deferred to escalated retries. Checkpoint totals at push
  time: 19/200 bases completed (w65 family first), 56,663,096 triples examined /
  43,160,550 safe / 0 safe maximal row-deficient candidates; 0 brute-verification
  failures.
- Honest scope: fresh 3-for-3 within window x >= 52 only; the sweep is NOT complete at
  this checkpoint and no absence claim is made; declared tier x >= 48 and the batch-1
  independent-verification gates for any found witness remain open.
- Reproduction: `node scripts/three_control.js`, then
  `node scripts/sweep_three.js --budget-ms 160000 --max-bases 4` repeated until
  `state.json: complete = true`.
