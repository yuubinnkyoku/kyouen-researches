# Seven-row q=4, width 70: holes-mode two-edit extension (2026-11-27)

Single-owner lane declared in `research/log/2026-11-27-seven-row-q4-w70-holes-single-owner.md`
(declaration-time HEAD `02e40e9ef4bd2944d7e28d0a75dae9ddfe120720`).

## Headline result

- Holes 2-for-2 neighborhood (at most 2 removals, at most 2 additions,
  additions may refill the two removed stones' positions, thereby also
  covering 1-swap and refill final states; final size exactly 20 stones with
  row multiset {3,3,3,3,3,3,2}) of **all 199 published bases** on the **7x70**
  board contains **no safe row-deficient maximal configuration**:
  199/199 bases, 448,782,213 row-capacity candidates, 48,971,845 safe,
  **0 safe maximal row-deficient** (aggregate of run1; run2 identical).
- Holes mode is a strict superset of fresh 2-for-2 mode, so the fresh 2-for-2
  negative at width 70 is subsumed for the same bases.
- D4-mirror x integer-translation census (K1211 procedure) at target width 70
  over all 199 bases (4 board-symmetry images, dx = 0..199): the largest
  translation-covered width is still **67** (width-65 chain bases);
  **no image/shift covers width 70** (0 hits).
- This is a **local negative only**: it does not claim that a width-69 or
  width-70 witness is absent (witnesses at edit distance >= 3 from every
  published base, or constructions outside these neighborhoods, are not
  excluded). **M_{7,4} stays in [69, 1929]** (witness band m=4..68; upper
  bound K0068 unchanged). Frontier: 7x69.

## Method

- `scripts/enum_two.js`: byte-clone of the published calibrated enumerator
  (sha256 `ab58c34a…`; fresh mode calibrated byte-for-byte against the pinned
  `audit_two_swap.cpp`). Exact integer geometry only.
- `scripts/sweep_driver.js`: chunked resume-safe driver of the published
  `sweep69run.js` / `sweep69hrun.js` procedure (same enumeration, same
  record schema, generalized width parameter; wall-budget stop between
  bases, sig-based resume).
- `scripts/census_translate.py`: byte-clone of the published analytic
  translation census, invoked with target width 70.
- `scripts/make_calibration70.js`: machine-generates
  `output/w70/calibration.json` (all gates below).
- Board symmetry note: the 7x70 board is invariant under x-mirror (x -> 69-x)
  and y-mirror (y -> 6-y); swept neighborhoods at dx = 0 already include the
  D4 images' neighborhoods, only nonzero shifts are genuinely new, and those
  are exactly what the census scans.

## Calibration, positive control, determinism, tamper (all_pass true)

`output/w70/calibration.json` (machine-generated):

- pinned `base53` on 7x57 fresh: 1,436,643 / 60,921 / 2 (published values
  reproduced exactly);
- published `stats_69` for the width-68 witness base on width 69 fresh:
  2,141,205 / 199,290 / 0 (published values reproduced exactly);
- positive control: the 23 `w65` bases at width 68 fresh, exactly 3
  neighborhoods produce exactly 1 maximum each, all three identical to the
  published unique width-68 witness (published claim reproduced);
- machinery cross-check: full 199/199 cold reproduction of the published
  width-69 holes records (`output/calib/repro_w69_holes.jsonl` vs the
  published `results_holes.jsonl` byte-clone): tag/sig/rcc/safe/
  shape_errors/maximal identical 199/199 (published totals 435,695,973 /
  45,368,697 / 0 reproduced exactly);
- determinism: w70 holes run1 vs run2, all 199 records identical modulo
  wall-time fields;
- tamper controls at width 70: moving one base stone and removing one base
  stone both fail closed (`unsafe base`).

## Outputs

- `output/w70/bases.json`: byte-clone of the published 199-base pool
  (sha256 `d8e977ec…`).
- `output/w70/results_holes70_run1.jsonl`, `results_holes70_run2.jsonl`:
  199 per-base holes records each (two full cold runs).
- `output/w70/calibration.json`: calibration/positive-control/reproduction/
  determinism/tamper record.
- `output/w70/census_stdout70.txt`: width-70 census record (0 hits;
  `census-hits70.json` not written, 0 hits).
- `output/calib/published_w69_holes.jsonl`: byte-clone of the published
  width-69 holes records; `output/calib/repro_w69_holes.jsonl`: the full
  cold reproduction; `output/calib/witnesses_68.json`: byte-clone of the
  published width-68 witness (calibration inputs).

## Honest limits

- Enumeration is complete over the stated holes two-edit neighborhoods of the
  stated 199 bases only, at width 70. No absence claim at width 69 or 70
  overall. No claim about widths > 70.
- `results/fixed-width/mwq_stabilization.csv` intentionally not updated
  (K1201/K1209/K1211/w69 precedent): the interval M_{7,4} in [69,1929] is
  unchanged.
- checked/safe/maximal counters are bookkeeping, not win/loss statements.
- Disclosed: the first driver implementation had a wall-budget bug (timer
  reset per base, so the budget never fired and one invocation was killed by
  the shell timeout after 98 valid records); the fix only changes when the
  process stops between bases, never the enumeration; the 98 records already
  written by the buggy invocation are byte-identical to the corresponding
  run1 records (resume reuses them). All 199 records of run1 were verified
  against a full independent second run.
- Standard 11x11 empty board, 19 central-reply roots, two-stone root
  {60,27}, third move {100,108}, S2, closure classes are untouched by this
  lane and remain UNKNOWN.
