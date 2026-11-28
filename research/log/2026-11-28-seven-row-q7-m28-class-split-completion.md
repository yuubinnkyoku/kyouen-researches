# 2026-11-28 seven-row q7 7x28 class-split sweep completion — honest negatives, frontier stays 7x28

Completion of the single-owner lane declared in
`research/log/2026-11-28-seven-row-q7-m28-class-split-declaration.md`
(declaration commit `14c0281b`, HEAD at declaration `3131cf9f`).

## Result

- No SAT within the swept pieces: class {3} krow=3:5 minpos pieces
  0, 1, 2, 3, 4, 7 at 7x28 all INDET at 275s caps (SIGTERM time-cuts),
  2,730,916 / 2,774,923 / 2,923,793 / 2,989,734 / 3,112,441 / 3,454,167
  conflicts — near-uniform resistance, unlike 7x27 where the minpos=0
  piece fell at 1,458,793 conflicts / 141s. All honest negatives,
  **not absence**.
- Free-column probe: a +1 right-shift of the new 7x27 witness onto
  7x28 is safe but leaves exactly cell (0,3) unblocked (shift-0 leaves
  (27,3)) — the same one-stone-short pattern as the (7,8) 7x25 -> 7x26
  transition, so 7x28 needs a genuinely new witness.
- Unswept: minpos 5, 6, 8..13; classes {0}/{1}/{2}; multi-deficiency
  classes; deeper krow counts. No absence claim at any width.
- **M_{7,7} in [28,708] unchanged; the frontier stays 7x28.**

Kit: `research/experiments/seven-row-q7-m28-class-split-20261128/`
(commits 9bdabb7c / b37f1453 / 14cca960): README, MANIFEST-sha256,
records, summary, free-column probe json, 6 raw time-cut logs.

## Non-claims

No 11x11 root / two-stone root {60,27} / third move {100,108} / S2 /
closure-class verdict is created, consumed, or transferred; all remain
UNKNOWN. Conflict counts are bookkeeping.
