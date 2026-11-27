# Seven-row q=4, width 69: complete two-edit neighborhood exhaustion (2026-11-27)

Single-owner lane declared in `research/log/2026-11-27-seven-row-q4-band-m69-single-owner.md`
(declaration-time HEAD `b782b8468b5e0a0336b6bc74a9c617c905ca108c`).

## Headline result

- The complete two-edit neighborhood (at most 2 removals and at most 2 additions,
  final size exactly 20 stones with row multiset {3,3,3,3,3,3,2}) of **all 199
  published bases** (`output/w68/bases.json` of
  `seven-row-q4-witness-band-60plus-20261121`, byte-clone, sha256 `d8e977ec…`)
  on the 7x69 board contains **no safe row-deficient maximal configuration**:
  - fresh 2-for-2 mode: 199/199 bases, 426,099,795 row-capacity candidates,
    43,009,353 safe, **0 safe maximal row-deficient**;
  - holes 2-for-2 mode (strict superset: additions may refill removed
    positions, thereby also covering 1-swap final states): 199/199 bases,
    435,695,973 candidates, 45,368,697 safe, **0 safe maximal row-deficient**.
- D4-mirror x integer-translation census (K1211 procedure) over all 199 bases
  (4 board-symmetry images, dx = 0..199): the largest translation-covered width
  is **67** (reached by width-65 chain bases); no image/shift covers width 69.
- This is a **local negative only**: it does not claim that a width-69 witness
  is absent (witnesses at edit distance >= 3 swaps from every published base,
  or seeded-SA constructions outside these neighborhoods, are not excluded).
  **M_{7,4} stays in [69, 1929]** (witness band m=4..68; upper bound K0068
  unchanged). Frontier: 7x69.

## Method

- `scripts/enum_two.js`: byte-clone of the published calibrated enumerator
  (sha256 `ab58c34a…`, fresh mode reproduces the pinned `audit_two_swap.cpp`
  counters). Exact integer geometry only.
- `scripts/sweep69run.js` / `scripts/sweep69hrun.js`: resume-safe drivers of the
  published `sweep69.js` / `sweep69h.js` procedure (same enumeration, same
  width-69 Board, same record schema, sig-based resume).
- `scripts/census_translate.py`: fresh translation census; blocked
  deficient-row cells are computed analytically per image (line/row
  intersection: at most one x; circle/row: quadratic discriminant), then
  shifts are scanned arithmetically. Safety and row multiset are checked once
  per base (translation/mirror invariant), pure integer arithmetic.
- Board symmetry note: the 7x69 board is invariant under x-mirror (x -> 68-x)
  and y-mirror (y -> 6-y), so the swept neighborhoods of the 199 bases already
  include their D4 images' neighborhoods at dx = 0; only nonzero shifts are
  genuinely new, and those are exactly what the census scans.

## Calibration, positive control, determinism, tamper

`output/w69/calibration.json` (machine-generated, all_pass true):

- pinned `base53` on 7x57 fresh: 1,436,643 / 60,921 / 2 (published values
  reproduced exactly);
- published `stats_69` for the width-68 witness base on width 69 fresh:
  2,141,205 / 199,290 / 0 (published values reproduced exactly);
- positive control: sweeping the 23 `w65` bases at width 68 fresh, exactly 3
  neighborhoods produce exactly 1 maximum each and all three are the identical
  published unique width-68 witness (published claim reproduced);
- determinism: 3 records re-run in a fresh process, counters identical 3/3;
  census re-run byte-identical stdout;
- tamper controls: moving one base stone or removing one base stone both
  fail closed (`unsafe base`), and every fresh record has the uniform
  rcc = 2,141,205 with maximal = 0 (0/199 deviations).

## Outputs

- `output/w69/bases.json`: byte-clone of the published 199-base pool.
- `output/w69/results.jsonl`: 199 per-base fresh records.
- `output/w69/results_holes.jsonl`: 199 per-base holes records (holes safe
  counts >= fresh per base, 199/199).
- `output/w69/census_stdout.txt`: census record (rerun-identical);
  `output/w69/census-hits.json` not written (0 hits).
- `output/w69/calibration.json`: calibration/positive-control/determinism/
  tamper record.

## Honest limits

- All enumerations are complete over the stated two-edit neighborhoods of the
  stated 199 bases only. No absence claim at width 69 overall. No claim about
  widths > 69.
- `results/fixed-width/mwq_stabilization.csv` intentionally not updated
  (K1201/K1209/K1211 precedent): the interval M_{7,4} in [69,1929] is unchanged.
- checked/safe/maximal counters are bookkeeping, not win/loss statements.
- Standard 11x11 empty board, two-stone roots, S2, closure classes are
  untouched by this lane and remain UNKNOWN.
