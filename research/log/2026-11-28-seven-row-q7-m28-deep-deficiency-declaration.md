# 2026-11-28 seven-row q7 7x28 deep-deficiency (krow=3:4 / 3:3) + remaining krow=3:5 minpos — single-owner declaration (publish-then-execute)

- Task: continue the (7,7) class-split lane at the frontier width 7x28
  into the **unswept deep-deficiency and remaining-single-deficiency
  pieces** of class {3} (central row, V-symmetric class). A SAT piece at
  7x28 would give **M_{7,7} >= 29** (range currently [28,708]).
- Sweep plan (kissat 4.0.4 official linux-amd64 binary, sha256
  21da5d98...ac93a1, cap <= 275s per piece, sound minpos H-split
  P=0..13, floor((m-1)/2)=13 at m=28), ascending within each family:
  1. class {3} krow=3:4 (exactly 4 stones in row 3, all other rows
     full at 6; 40-stone 2-deficient witnesses would be the first
     deep-deficiency witnesses beyond m=14 in this family) — minpos
     0,1,2,... ascending;
  2. class {3} krow=3:3 (39-stone 3-deficient) — minpos ascending;
  3. the unswept krow=3:5 single-deficiency pieces minpos 5,6,8..13
     (continuation of commit 9bdabb7c's sweep, which covered
     0,1,2,3,4,7 as INDET at 275s caps).
  WIN-stop rule: on the first SAT, stop, dual-verify (sat.js decode
  verifyConfig + fresh Python exact-Fraction verifier verify_frac.py),
  run negative controls, and publish; remaining pieces not swept, no
  absence claimed. UNSAT/INDET pieces are honest negatives per piece
  only.
- Rationale (measured, disclosed): at 7x28 the krow=3:5 single-deficiency
  pieces resist near-uniformly (2,730,916..3,454,167 conflicts at 275s);
  the (6,6) 6x26 class {0} krow=0:4 deep-deficiency pieces measured a
  conflicts band ~40% below the single-deficiency band under the same
  cap, so deep-deficient rows plausibly have structurally smaller
  branching and are the highest-information unswept family at 7x28.
- Calibration (run after this declaration is published): regenerate the
  7x27 deciding instance class {3} krow=3:5 minpos=0 CNF and require
  SAT with 1,458,793 conflicts bit-exact vs the published kit
  (seven-row-q7-m27-class-split-20261128) before any 7x28 piece runs.
- Machinery: the seven-row-q7-m27-class-split-20261128 kit scripts
  (sat.js fcc0cfd8 / sat2.js 14ceb854 / sat3.js e04581eb /
  verify_frac.py 837fe24b), byte-verified at fetch.
- Declaration-time HEAD: 6ffc8a387d0c637d30b54dee67cf5ab15fb8a0c0 (n11 fifteenth ladder-top adoption lane
  declared by a parallel session at 6ffc8a38; this lane is disjoint).
- Non-claims: no 11x11 root / two-stone root {60,27} / third move
  {100,108} / S2 / closure-class verdict is created, consumed, or
  transferred; all remain UNKNOWN. Conflict counts are bookkeeping.
- This declaration takes single ownership of the 7x28 (7,7) class {3}
  deep-deficiency + remaining-minpos sweep for this session; parallel
  executions of the same cells should defer.
