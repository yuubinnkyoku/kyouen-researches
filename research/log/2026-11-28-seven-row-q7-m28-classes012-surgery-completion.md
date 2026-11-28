# 2026-11-28 seven-row q7 7x28 classes {0}/{1}/{2} + class {3} minpos 5/6 + two-edit surgery — completion

Single-owner lane declared in
`research/log/2026-11-28-seven-row-q7-m28-classes012-declaration.md`
(declaration commit `bdb7513a`, declaration-time HEAD `3686a5c0`).
Kit: `research/experiments/seven-row-q7-m28-classes012-surgery-20261128`
(commits `eff3ea00` / `b7e85142` / `124ddb99` / `2c820ef1`, fetch-back
19/19 byte-identical against the kit MANIFEST at commit-pinned raws).

## Result: no SAT anywhere; all honest negatives, not absence

1. **Sweep pieces** (kissat 4.0.4 pinned binary 21da5d98, SIGTERM
   time-cuts): class {3} krow=3:5 minpos=5 INDET 2,914,708 conflicts
   (275s) and minpos=6 INDET 2,927,565 (272s); class {0} krow=0:5
   minpos=0 INDET 2,710,560, class {1} krow=1:5 minpos=0 INDET
   2,724,218, class {2} krow=2:5 minpos=0 INDET 2,570,306 (all 272s).
   All mirror classes now have first coverage at 7x28 krow=:5; the
   conflict band 2.57M..2.93M sits inside the class {3} band
   (2.73M..3.45M) — near-uniform resistance across all row positions.
2. **Complete two-edit surgery** of the published 7x27 witness on 7x28,
   both placements (shift-0 T=(27,3), +1-shift T=(0,3)):
   **2,158,423 unique candidates, 0 safe, 0 safe-maximal witnesses at
   both** (local negative, edit distance <= 2 only). Determinism:
   run1/run2 sha256-identical both placements
   (`4f80801b...`, `b37f4a78...`).
3. **One-curve frontier observation** (structural): at both placements
   the T-curve census is exactly `{c4: 0, c5: 1}` — the only curve
   through the frontier cell with >= 4 seed stones is the deficient
   row-3 line itself, so any <= 2-edit blocking must complete that
   single line, and every completion fails safety. Consistent with the
   large consecutive-width witness jumps (sd 28..34) in the family; a
   7x28 witness, if it exists, is not within 2 edits of the 7x27 witness
   in either placement.

## Controls

- Toolchain calibration 7x24 q7 class {3} krow=3:5 minpos=1: SAT 64,031
  conflicts, bit-exact with the published family control.
- Engine calibration byte-exact: `calib-m26.json` (6x26 published
  surgery case, published seed/target) sha256
  `7cfe56c7243591552c0f911ac2b46bd31e23c935c23cd505cf931c87b3e3a070`
  is byte-identical to the published `surgery-m26.run1.json` of the
  six-row-q6-m26-two-edit-surgery-20261127 kit.
- Integer-conic spot-check 300/300 engine rejections confirmed, 0 missed
  witnesses.

## Bookkeeping

- `results/fixed-width/mwq_stabilization.csv` (7,7) note extended
  (72,162 B -> 73,411 B, one line changed); range unchanged
  **M_{7,7} in [28,708]**, frontier stays 7x28.
- Not swept: minpos >= 1 for classes {0}/{1}/{2}, class {3} minpos
  8..13, krow=3:4 deep deficiency, multi-deficiency classes. No absence
  claim at any width.
- Resume pointers: a heavier-cap (>= 600s per piece needs a resumable
  or background runner; the 300s bash cap binds) or a different
  decomposition (e.g. two-curve-aware case split exploiting the
  one-curve frontier structure) is needed for further 7x28 progress on
  the SAT side; the surgery side could extend to 3 edits but the
  candidate count grows beyond this session's budget.

## Non-claims

No 11x11 root / two-stone root {60,27} / third move {100,108} / S2 /
closure-class verdict is created, consumed, or transferred; all remain
UNKNOWN. Conflict counts are bookkeeping.
