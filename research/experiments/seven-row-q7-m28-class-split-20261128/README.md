# Seven-row q=7, 7x28: SAT-side class {3} krow/minpos sweep — honest negatives at 275s caps (2026-11-28 fast lane)

Single-owner lane declared in
`research/log/2026-11-28-seven-row-q7-m28-class-split-declaration.md`
(declaration commit `14c0281b`, declaration-time HEAD `3131cf9f`).

## Result: no SAT within the swept pieces — all INDET honest negatives

Pieces class {3} krow=3:5 at 7x28, kissat 4.0.4 (pinned binary
21da5d98...ac93a1), 275s caps, SIGTERM time-cuts:

- minpos=0: INDET, 2,730,916 conflicts
- minpos=1: INDET, 2,774,923 conflicts
- minpos=2: INDET, 2,923,793 conflicts
- minpos=3: INDET, 2,989,734 conflicts
- minpos=4: INDET, 3,112,441 conflicts
- minpos=7: INDET, 3,454,167 conflicts

Near-uniform resistance across the spread (unlike 7x27, where the
minpos=0 piece fell at 1,458,793 conflicts / 141s). **All honest
negatives, not absence.** Not swept: minpos 5, 6, 8..13; classes
{0}/{1}/{2}; multi-deficiency classes; deeper deficient-row counts
(krow=3:4 etc.). No absence claim at any width; M_{7,7} in [28,708]
unchanged, frontier 7x28.

## Free-column probe (frontier characterization)

`output/shift1_on_m28.json`: a +1 right-shift of the new 7x27 witness
onto 7x28 is safe (max curve 6) but not maximal — exactly cell (0,3)
unblocked; the shift-0 placement leaves (27,3). So 7x28 needs a
genuinely new witness (the same one-stone-short pattern as the (7,8)
7x25 -> 7x26 transition, where the +1 shift left (0,3) unblocked).
Verified with the fresh Python exact-Fraction verifier
(`scripts/verify_frac.py`, byte-clone of the m27 kit).

## Files

- `output/records.jsonl`: per-piece records.
- `output/summary.json`: machine-readable summary.
- `output/r7x28q7_c3k5p{0,1,2,3,4,7}.txt`: raw time-cut logs.
- Scripts: byte-clones of the seven-row-q7-m27-class-split-20261128 kit
  (sat.js fcc0cfd8 / sat2.js 14ceb854 / sat3.js e04581eb /
  verify_frac.py 837fe24b), not re-published here; see that kit's
  MANIFEST-sha256.

## Non-claims

No 11x11 root / two-stone root {60,27} / third move {100,108} / S2 /
closure-class verdict is created, consumed, or transferred; all remain
UNKNOWN. Conflict counts are bookkeeping.
