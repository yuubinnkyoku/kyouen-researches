# Seven-row q=7, 7x27: SAT-side class {3} krow/minpos decomposition — witness, M_{7,7} >= 28 (2026-11-28 fast lane)

Single-owner lane declared in
`research/log/2026-11-28-seven-row-q7-m27-class-split-declaration.md`
(declaration commit `40a05ee3`, declaration-time HEAD `580e3703`).

## Headline result

The krow/minpos decomposition of the (7,7) unresolved frontier width 7x27
**is SAT in the very first sub-instance: class {3}, krow=3:5, minpos=0**:

- kissat 4.0.4 (official linux-amd64 binary, sha256
  `21da5d984e38b74f620f14c62442f834f27b9158decdb722540d97f98aac93a1`),
  1,458,793 conflicts, SAT, cold pair run1/run2: v-lines byte-identical
  (wall 141.08s / 139.55s, disclosed as the only difference).
- Decoded witness (`output/w77_27.json`): **41 stones, rows
  [6,6,6,5,6,6,6]**, deficient row 3 stones at x = 0, 4, 11, 19, 25
  (leftmost x = 0 = the minpos pin), full column span 0..26 (genuinely
  using the 7x27 board).
- Dual independent verification, both PASS:
  - sat.js `verifyConfig` (census-free integer) — ok, size 41, rows
    [6,6,6,5,6,6,6];
  - fresh Python exact-Fraction verifier `scripts/verify_frac.py`
    (stone-pair primitive lines / stone-triple circumcenter circles, no
    repo code) — safe (max curve occupancy 6 = q-1), maximal
    (0 unblocked cells).

**Therefore M_{7,7} >= 28; the (7,7) range becomes [28, 708]** (upper
bound 708 by K0318 substitution, unchanged). This resolves the previously
published 7x27 status (all 4 rowY mirror classes INDET at 250-262s caps:
rowY=3 2,242,940, rowY=0/1/2 2,186,370 / 2,243,432 / 2,095,752;
`seven-row-q5-q8-sat-frontier-20261115`) in the SAT direction, extending
the K0826 witness band (7x7..7x26) to 7x27 with the same
[6,6,6,5,6,6,6] single-deficiency shape. The witness sits at symmetric
difference 34 from the published m=26 rowY=3 witness (min over D4 x
translations, i.e. >= 17 stone moves) — consecutive-width witness jumps
stay large, consistent with the (7,8) family (sd 28 at 7x25).

## Sweep pieces (WIN-stop at minpos=0)

- minpos=0: **SAT, 1,458,793 conflicts** (deciding instance, cold pair
  identical).
- minpos=1..13 not swept (WIN-stop rule fired); classes {0}/{1}/{2} and
  all multi-deficiency classes not swept. **No absence claim at any
  width.** The sound minpos bound at m=27 is floor((m-1)/2)=13.

## Controls

- **Toolchain calibration** (pre-declaration, disclosed in the
  declaration): 6x20 q7 class {2} — SAT, 641,859 conflicts, bit-exact
  with the published six-row-q7-m22-kit control
  (`six-row-q7-m21-class-split-20261114`).
- **Family control** (pre-declaration, disclosed): 7x24 q7 class {3}
  krow=3:5 minpos=1 (the piece containing the published m=24 witness
  row3=[1,3,6,19,21]) — SAT, 64,031 conflicts; the solver returned a
  different 41-stone witness in the same piece (row3=[1,11,15,17,23],
  disclosed), dual-verified identically.
- **Honest negatives** (pre-declaration, disclosed): 7x26 class {3}
  krow=3:5 plain — INDET at 280s, 1,575,348 conflicts; 7x26 minpos=0 —
  INDET at 285s, 1,575,157 conflicts. m=26 is known SAT by the rowY=3
  encoding, so these are cap-limited, not absence.
- **Negative controls on the witness** (fresh Fraction verifier):
  removing stone (0,3) -> safe but not maximal (unblocked cells include
  (0,3)); adding stone (26,0) -> rejected UNSAFE (a 7-stone curve,
  fail-loud assertion).
- Determinism: deciding-instance cold pair v-lines byte-identical
  (above); CNFs are regenerable
  (`node scripts/sat3.js 7 27 7 --class=3 --krow=3:5 --minpos=P <out>`),
  not published (size policy, same as the m22/m25 kits).

## Files

- `scripts/`: sat.js (fcc0cfd8), sat2.js (14ceb854), sat3.js (e04581eb),
  verify_frac.py (837fe24b) — byte-clones of the
  seven-row-q8-m25-class-split-20261128 kit scripts (themselves
  byte-clones of the six-row-q7-m22 kit), pinned by its MANIFEST
  sha256 bda3754f.
- `output/w77_27.json`: the witness (stones + both verifications).
- `output/geometry.json`: span/rows/minpos/sd-vs-m26.
- `output/records.jsonl`: all run records (deciding pair + controls).
- `output/summary.json`: machine-readable summary.
- `output/r7x27q7_c3k5p0.run1.txt` / `.run2.txt`: deciding instance raw
  logs (models included).
- `output/r6x20q7_c2.txt`, `output/r7x24q7_c3k5p1.txt`: calibration and
  family-control raw logs.
- `output/r7x26q7_c3k5.txt`, `output/r7x26q7_c3k5p0.txt`: honest-negative
  raw logs.
- `output/negctrl_rm.json`, `output/negctrl_add.json`: negative-control
  configs.
- `output/w77_24_ctrl.json`: family-control decoded witness.

## Non-claims

No 11x11 root / two-stone root {60,27} / third move {100,108} / S2 /
closure-class verdict is created, consumed, or transferred; all remain
UNKNOWN. Conflict counts are bookkeeping. The unswept pieces and classes
carry no absence claim; M_{7,7} <= 708 stands and exact M needs
persistence at m=28..707 or a tail bound.
