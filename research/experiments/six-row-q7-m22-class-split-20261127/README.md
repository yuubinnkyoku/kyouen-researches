# Six-row q=7, 6x22: SAT-side class {2} krow/minpos decomposition — witness, M_{6,7} >= 23 (2026-11-27 fast lane)

Single-owner lane declared in
`research/log/2026-11-27-six-row-q7-m22-class-split-declaration.md`
(declaration commit `d35234a7`, declaration-time HEAD `a4ea02e4`).

## Headline result

The krow/minpos decomposition of the (6,7) unresolved frontier width 6x22
**is SAT in sub-instance class {2}, krow=2:5, minpos=7**:

- kissat 4.0.4 (official linux-amd64 binary, sha256
  `21da5d984e38b74f620f14c62442f834f27b9158decdb722540d97f98aac93a1`),
  2,050,424 conflicts, SAT, cold pair run1/run2 identical (conflicts and model
  v-lines byte-identical).
- Decoded witness: **35 stones, rows [6,6,5,6,6,6]** (`output/w67_22.json`),
  genuinely using the 6x22 board (stone at (21,2); full column span 0..21).
- Dual independent verification, both PASS:
  - sat.js `verifyConfig` (census-free integer) — ok, size 35, rows
    [6,6,5,6,6,6];
  - fresh Python exact-Fraction verifier `scripts/verify_frac.py`
    (stone-pair primitive lines / stone-triple circumcenter circles, no repo
    code) — safe (max curve occupancy 6 = q-1), maximal (0 unblocked cells).

**Therefore M_{6,7} >= 23; the (6,7) range becomes [23, 402]** (upper bound
K0806/K0318 substitution unchanged). This resolves the previously published
6x22 status (class {2} plain 280s INDET at 5,038,264 conflicts; two-edit
surgery around the m=21 seed NEGATIVE) in the SAT direction: a witness exists
at distance (sd 12, i.e. >= 6 stone moves) from the m=21 witness family,
consistent with the two-edit negative.

Witness geometry (`output/geometry.json`): rows [6,6,5,6,6,6], row 2 stones
at x = 7, 9, 16, 19, 21 (leftmost x = 7 = the minpos pin); min symmetric
difference vs the m=21 witness over all 8 dihedral images x translations
(dx -4..4) is 12; translation census R(S) = {22} (full span); the free-column
right-shift to 6x23 fails (cell (0,2) unblocked), so 6x23 is a real frontier.

## Extension probes (disclosed as beyond the declared 6x22 target)

6x23 q=7 class {2} krow=2:5 minpos 6/7/8 all **INDET** at 262s caps
(4,968,075 / 5,055,896 / 4,935,522 conflicts) — honest negatives, not
absence; near-uniform frontier resistance. The new frontier is 6x23.

## Controls

- **Positive control**: 6x20 q=7 class {2} reproduced the published value
  bit-exactly (SAT, 641,859 conflicts; `six-row-q7-m21-class-split-20261114`
  reports 641,859 / 29.1s).
- **Negative controls** (fresh Fraction verifier): removing stone (21,2)
  -> not maximal, rc=1, exactly [(21,2)] unblocked; adding stone (2,0)
  -> rejected, rc=1.
- **Verifier self-test**: the published m=21 witness `w67_21.json`
  (sha256 `5f01a133...`) verifies PASS through the same fresh verifier path.
- Determinism: cold pair on the deciding CNF identical; encoder metadata
  (vars/clauses) in `output/meta_*.json`; CNFs are regenerable
  (`node sat3.js 6 22 7 --class=2 --krow=2:5 --minpos=7 <out>`), not
  published (size policy, same as the m21 kit).

## Scope and non-claims

- Witness existence only. No absence claim at any width (the 34 other
  canonical classes at 6x22 remain unswept; 6x23 INDET probes are not
  absence). M_{6,7} exact value unknown; upper 402 unchanged.
- Standard 11x11 empty board, two-stone roots, third move, S2, closure
  classes: UNKNOWN at all times; verdicts not consumed; conflict counts are
  bookkeeping.

## Honest disclosures

- One execution-environment reset occurred mid-session (a batched command
  exceeded the wall-clock cap); the pre-reset first observation of the
  deciding instance (SAT, 2,050,424 conflicts, identical decoded witness
  stones) and the pre-reset 6x23 minpos=7 single run (INDET 5,076,037
  conflicts at a 265s cap, same trajectory as the official 5,055,896 at
  262s) are disclosed here; all published raw logs were regenerated
  post-reset from re-fetched byte-identical scripts and the re-downloaded
  pinned kissat binary, and reproduce those observations exactly.
- The 6x20 calibration run happened before the declaration commit (disclosed
  in the declaration); all published 6x22/6x23 measurements ran after it.
- Scripts are byte-clones of the published m21 kit (sha256 in MANIFEST);
  `scripts/verify_frac.py` is a fresh implementation written for this kit.

## Files

- `scripts/sat3.js` / `sat2.js` / `sat.js`: class-split machinery (K0818/K0810
  core), byte-clones of the published m21 kit scripts.
- `scripts/verify_frac.py`: fresh independent exact-Fraction verifier.
- `output/w67_22.json`: the witness (stones + both verifications).
- `output/r6x20q7_c2.txt`: positive-control raw log (SAT, model included).
- `output/r6x22q7_c2k5p7.run1.txt` / `.run2.txt`: deciding instance, cold
  pair (SAT, models included).
- `output/r6x23q7_c2k5p{6,7,8}.txt`: frontier INDET raw logs.
- `output/records.jsonl`, `output/summary.json`, `output/geometry.json`,
  `output/negctrl_*.json`, `output/shift1_on_m23.json`, `output/meta_*.json`.
- `MANIFEST-sha256.txt`: sha256 of every published file.
