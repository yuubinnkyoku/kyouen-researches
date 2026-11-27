# Seven-row q=4, width 70: holes-mode two-edit extension — single-owner declaration (2026-11-27)

Publish-then-execute. Declaration-time HEAD: `02e40e9ef4bd2944d7e28d0a75dae9ddfe120720`.

## Scope claimed by this lane (single owner)

Extension of the published width-69 two-edit exhaustion
(`research/experiments/seven-row-q4-w69-two-edit-negative-20261127/`,
K0827 追記 2026-11-27) to **width 70 in holes 2-for-2 mode** over the same
published 199-base pool:

- holes 2-for-2 mode is a strict superset of fresh 2-for-2 mode (additions may
  refill the two removed stones' positions, thereby also covering 1-swap and
  refill final states), so a holes-negative at width 70 subsumes the fresh
  2-for-2 negative at width 70 for the same bases;
- board: 7x70, exact integer geometry only;
- bases: the published 199-base pool, byte-clone
  (`seven-row-q4-witness-band-60plus-20261121` `output/w68/bases.json`,
  sha256 `d8e977ec…`), unmodified;
- enumeration core: byte-clone of the published calibrated enumerator
  `enum_two.js` (sha256 `ab58c34a…`), no code changes;
- D4-mirror x integer-translation census at target width 70 (analytic,
  `census_translate.py` procedure).

## Planned pre-registered readings

- w70 holes 2-for-2, all 199 bases: per-base rcc/safe/shape_errors/maximal
  records, two full runs (determinism, byte-identical modulo wall-time);
- calibration (machine-generated, all gates must pass):
  pinned base53 7x57 fresh (1,436,643/60,921/2), pinned w68-witness-base
  width-69 fresh (2,141,205/199,290/0), positive control (w65 bases at
  width 68 fresh: exactly 3 producers of exactly 1 identical published
  width-68 witness), full 199/199 holes reproduction of the published
  width-69 holes records as a machinery cross-check, tamper controls
  fail-closed (moved stone / removed stone);
- census at width 70: report top translation-covered widths and hits>=70.

## Claim policy (pre-registered)

- A safe maximal row-deficient configuration found at width 70 would raise
  the constructive lower bound (M_{7,4} >= 71) and the interval would move;
  otherwise this is a **local negative only**: no absence claim at width 69
  or 70 overall, and **M_{7,4} stays in [69, 1929]**.
- `results/fixed-width/mwq_stabilization.csv` is not updated (K1201/K1209/
  K1211/w69 precedent) unless a witness is found.
- Counters are bookkeeping. **No verdict is consumed. The standard 11x11
  empty board, 19 central-reply roots, two-stone root {60,27}, third move
  {100,108}, S2 and all closure classes remain UNKNOWN.**

## Coordination

- Other active lanes (n11 ninth-cost, six-row q6/q7 SAT, kit-20 strip,
  (4,24,5) sweep) are disjoint; this lane does not touch them.
- Before publishing results, latest `main` will be re-fetched; on push
  conflict or concurrent write the situation is recorded and the work is
  handed to the next run.
