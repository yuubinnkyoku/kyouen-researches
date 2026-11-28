# Seven-row q=8, 7x25: SAT-side class {3} krow/minpos decomposition — witness, M_{7,8} >= 26 (2026-11-28 fast lane)

Single-owner lane declared in
`research/log/2026-11-28-seven-row-q8-m25-class-split-declaration.md`
(declaration commit `2fd5f28f`, declaration-time HEAD `4505b70a`).

## Headline result

The krow/minpos decomposition of the (7,8) unresolved frontier width 7x25
**is SAT in sub-instance class {3}, krow=3:6, minpos=2**:

- kissat 4.0.4 (official linux-amd64 binary, sha256
  `21da5d984e38b74f620f14c62442f834f27b9158decdb722540d97f98aac93a1`),
  666,158 conflicts, SAT, cold pair run1/run2: model and v-lines
  byte-identical (c-line progress/wall-clock differ, disclosed).
- Decoded witness: **48 stones, rows [7,7,7,6,7,7,7]** (`output/w78_25.json`),
  deficient row 3 stones at x = 2, 5, 18, 21, 23, 24 (leftmost x = 2 = the
  minpos pin); full column span 0..24 (genuinely using the 7x25 board).
- Dual independent verification, both PASS:
  - sat.js `verifyConfig` (census-free integer) — ok, size 48, rows
    [7,7,7,6,7,7,7];
  - fresh Python exact-Fraction verifier `scripts/verify_frac.py`
    (stone-pair primitive lines / stone-triple circumcenter circles, no repo
    code) — safe (max curve occupancy 7 = q-1), maximal (0 unblocked cells).

**Therefore M_{7,8} >= 26; the (7,8) range becomes [26, 651]** (upper bound
K0825/K0318 substitution unchanged). This resolves the previously published
7x25 status (all 4 mirror classes INDET at 250s: rowY=3 3,534,747, rowY=0/1/2
3,613,768/3,717,333/3,678,867; `seven-row-q5-q8-sat-frontier-20261115`) in
the SAT direction, mirroring the six-row-q7-m22-class-split-20261127 pattern.
The witness family extends to m=8..25 (single-deficiency 48 stones
[7,7,7,6,7,7,7]-type from m=13).

## Sweep pieces (WIN-stop at minpos=2)

- minpos=0: INDET at 275s cap, 4,443,950 conflicts (SIGTERM time-cut) — honest
  negative, not absence.
- minpos=1: INDET at 275s cap, 4,488,644 conflicts (SIGTERM time-cut) — honest
  negative, not absence.
- minpos=2: **SAT, 666,158 conflicts** (deciding instance).
- minpos=3..12 not swept (WIN-stop rule fired); classes {0}/{1}/{2} and all
  multi-deficiency classes not swept. **No absence claim at any width.**

## Controls

- **Positive control**: 7x24 q8 class {3} krow=6 — SAT, 869,797 conflicts,
  decoded 48 stones rows [7,7,7,6,7,7,7], dual-verified. Ran once before the
  declaration commit (disclosed in the declaration as calibration) and once
  after, reproducing the conflict count exactly (the pre-declaration artifacts
  were lost to the environment reset disclosed below; the published raw is the
  post-reset run).
- **Negative controls** (fresh Fraction verifier): removing stone (2,3)
  -> safe but not maximal (rc=1, unblocked cells include (2,3),(3,3),(9,3));
  adding stone (0,0) -> rejected UNSAFE (curve with 8 stones, rc=1).
- Determinism: deciding-instance cold pair identical (above); CNFs are
  regenerable (`node scripts/sat3.js 7 25 8 --class=3 --krow=3:6 --minpos=P
  <out>`), not published (size policy, same as the m22 kit).

## Witness geometry (`output/geometry.json`)

rows [7,7,7,6,7,7,7], row 3 stones at x = 2, 5, 18, 21, 23, 24; min symmetric
difference vs the 7x24 control witness over 4 reflection images x translations
dx -6..6 is **28** (>= 14 stone moves) — the consecutive-width witness jump is
large, consistent with the m=22/m=23, m=25/m=24 and other published jumps.
The free-column right-shift (+1) of the m=25 witness onto 7x26 is
**safe but not maximal**: exactly cell (0,3) is unblocked (one-stone-short
structure), so 7x26 is a real frontier (`output/shift1_on_m26.json`).

## Scope and non-claims

- Witness existence only. No absence claim at any width. M_{7,8} exact value
  unknown; upper 651 unchanged.
- Standard 11x11 empty board, two-stone roots, third move, S2, closure
  classes: UNKNOWN at all times; verdicts not consumed; conflict counts are
  bookkeeping.

## Honest disclosures

- One execution-environment reset occurred early in the session (a batched
  command with two 272s-capped pieces exceeded the 300s wall-clock cap): the
  workspace was rebuilt from re-fetched byte-identical scripts (sha256
  verified: sat.js `fcc0cfd8...`, sat2.js `14ceb854...`, sat3.js
  `e04581eb...`, verify_frac.py `837fe24b...` — byte-clones of the published
  six-row-q7-m22-class-split-20261127 kit) and the pinned kissat binary.
  All published measurements (control, p0, p1, deciding pair) ran
  post-reset; the pre-declaration calibration observation (869,797
  conflicts) is disclosed in the declaration and reproduced post-reset
  exactly.
- kissat wall-clock caps (275s) exceed the previously published 250-262s
  frontier caps; INDET pieces are SIGTERM time-cuts, honest negatives.

## Files

- `scripts/sat3.js` / `sat2.js` / `sat.js`: class-split machinery
  (K0818/K0810 core), byte-clones of the published m22 kit scripts.
- `scripts/verify_frac.py`: fresh independent exact-Fraction verifier.
- `output/w78_25.json`: the witness (stones + both verifications).
- `output/r7x24q8_c3k6_ctrl.txt`: positive-control raw log (SAT, model incl.).
- `output/r7x25q8_c3k6k6p2.run1.txt` / `.run2.txt`: deciding instance, cold
  pair (SAT, models included).
- `output/r7x25q8_c3k6k6p0.txt` / `p1.txt`: INDET raw logs (time-cut).
- `output/records.jsonl`, `output/summary.json`, `output/geometry.json`,
  `output/negctrl_rm.json`, `output/negctrl_add.json`,
  `output/shift1_on_m26.json`, `output/output_ctrl24.json`,
  `output/meta_gen_p{0,1,2}.json`.
- `MANIFEST-sha256.txt`: sha256 of every published file.
