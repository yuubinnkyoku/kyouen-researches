# 2026-11-28 seven-row q8 7x25 class {3} krow/minpos split — completion

Executes the single-owner declaration
`research/log/2026-11-28-seven-row-q8-m25-class-split-declaration.md`
(declaration-time HEAD 4505b70a, kit commit 7c400d18, raw logs a7ce3bc8,
MANIFEST bda3754f).

## Result

- Class {3} (deficient row pattern {3}), krow=3:6, minpos=2 on 7x25 q8:
  **SAT** — kissat 4.0.4, 666,158 conflicts, 34.33s. Cold pair (two
  independent runs) identical: same model / v-line prefix, wall-clock-only
  difference. Decoded witness: 48 stones, rows [7,7,7,6,7,7,7], row 3 at
  x=[2,5,18,21,23,24], span 0..24. Dual-verified safe + maximal by
  sat.js verifyConfig and a fresh Python Fraction verifier
  (`verify_frac.py`), both PASS.
- Consequence: **M_{7,8} >= 26**, published range moves
  [25,651] -> [26,651] (mwq_stabilization.csv updated in the same commit).
- Positive control (disclosed pre-declaration): 7x24 q8 class {3} krow=6
  SAT 869,797 conflicts, reproducing the published m=24 witness.
- Honest negatives: minpos=0 and minpos=1 pieces INDET at 275s caps
  (4,443,950 / 4,488,644 conflicts, SIGTERM time-cut) — no absence claim.
  WIN-stop fired at the first SAT as declared; minpos 3..12 and classes
  {0}/{1}/{2} were not swept.
- Negative controls: removing stone (2,3) breaks maximality; adding (0,0)
  is unsafe. sd of the 7x25 witness = 28; a +1 shift onto 7x26 is safe but
  leaves cell (0,3) unblocked (not maximal), so 7x26 is a genuine frontier.

## Non-claims

No 11x11 root / two-stone root {60,27} / third move {100,108} / S2 /
closure-class verdict is created, consumed, or transferred; all remain
UNKNOWN. Conflict counts are bookkeeping.

## Artifacts

Kit `research/experiments/seven-row-q8-m25-class-split-20261128/`
(README, scripts sat.js/sat2.js/sat3.js/verify_frac.py byte-clones of the
m22 kit, output JSONs incl. witness w78_25.json and records.jsonl, 5 raw
kissat logs incl. the cold pair, MANIFEST-sha256.txt over 21 files; all
pushed file sha256 verified by commit-pinned raw fetch-back).
