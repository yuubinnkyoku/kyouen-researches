# 2026-11-28 seven-row q7 7x27 class-split completion — M_{7,7} >= 28

Completion of the single-owner lane declared in
`research/log/2026-11-28-seven-row-q7-m27-class-split-declaration.md`
(declaration commit `40a05ee3`, HEAD at declaration `580e3703`).

## Result

- **7x27 (7,7) is SAT**: the first sound H-split piece, class {3}
  krow=3:5 minpos=0, resolved SAT with kissat 4.0.4 in 1,458,793
  conflicts; cold pair (run1/run2) both SAT with **v-lines
  byte-identical** (wall 141.08s / 139.55s — the only difference).
- Decoded witness: **41 stones, rows [6,6,6,5,6,6,6]**, deficient row 3
  at x = 0, 4, 11, 19, 25, column span 0..26 (genuinely 7x27).
- Dual verification PASS: sat.js `verifyConfig` (ok, size 41) and the
  fresh Python exact-Fraction verifier (safe, max curve 6 = q-1;
  maximal, 0 unblocked cells). Negative controls: rm (0,3) -> safe but
  not maximal; add (26,0) -> UNSAFE (7-stone curve, fail-loud).
- Witness sd = 34 vs the published m=26 rowY=3 witness (min over D4 x
  translations), i.e. >= 17 stone moves — consecutive-width jumps stay
  large, consistent with the (7,8) family.

**Consequence: M_{7,7} >= 28; the (7,7) range moves [27,708] -> [28,708].**
This extends the K0826 witness band (7x7..7x26) to 7x27 with the same
single-deficiency [6,6,6,5,6,6,6] shape, and resolves the published 7x27
wall (all 4 rowY mirror classes INDET at 250-262s caps, 2.1M-2.24M
conflicts) in the SAT direction. The (7,7) frontier moves to 7x28.

## Sweep bookkeeping (WIN-stop at minpos=0)

- minpos=0: SAT (deciding). minpos=1..13 not swept (WIN-stop rule).
- Classes {0}/{1}/{2} and all multi-deficiency classes not swept.
- **No absence claim at any width.**

## Kit

`research/experiments/seven-row-q7-m27-class-split-20261128/` (kit
commits bd51d376 / 6fc0f3fe / e46a6ced / f38c6e41): README,
MANIFEST-sha256 (18 files), byte-clone scripts (sat.js fcc0cfd8 /
sat2.js 14ceb854 / sat3.js e04581eb / verify_frac.py 837fe24b, pinned by
the seven-row-q8-m25 kit MANIFEST bda3754f), witness + geometry +
records + summary json, deciding-instance cold-pair raw logs, calibration
(6x20 class {2} SAT 641,859 — bit-exact with the published six-row-q7
kit control) and family-control (7x24 class {3} krow=3:5 minpos=1 SAT
64,031, a different witness in the piece containing the published m=24
one — disclosed) raw logs, and the 7x26 honest-negative logs (plain
INDET 280s 1,575,348; minpos=0 INDET 285s 1,575,157 — cap-limited, m=26
is known SAT by the rowY=3 encoding).

## Non-claims

No 11x11 root / two-stone root {60,27} / third move {100,108} / S2 /
closure-class verdict is created, consumed, or transferred; all remain
UNKNOWN. Conflict counts are bookkeeping.
