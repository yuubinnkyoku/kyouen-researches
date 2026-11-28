# 2026-11-28 seven-row q7 7x27 SAT-side class {3} krow/minpos decomposition — single-owner declaration (publish-then-execute)

- Task: attack the (7,7) frontier width 7x27 in the SAT direction with the
  krow/minpos class-split machinery (class {3} single-deficiency central
  class, krow=3:5, minpos P=0..13 sound H-split, floor((m-1)/2)=13 at m=27)
  that resolved (6,7) 6x22 and (7,8) 7x25 as SAT. A SAT piece at 7x27 would
  give **M_{7,7} >= 28** (current published range [27,708]; K0826 witnesses
  7x7..7x26, frontier 7x27).
- Known structure (published, K0826): the m=25/m=26 witnesses are 41 stones
  rows [6,6,6,5,6,6,6] found by the rowY=3 fixed-row split (m=26: 1,951,966
  conflicts, parallel independent run); 7x27 rowY=0/1/2 INDET at 250s caps
  (2,186,370 / 2,243,432 / 2,095,752 conflicts) and rowY=3 INDET at 262s
  (2,242,940) — near-uniform resistance, none of them absence. The 7x27
  two-edit surgery around the m=26 seed is complete-negative (local only).
  This lane is the first class-split (krow/minpos) attack on 7x27.
- Sweep plan: pieces minpos=0,1,2,... ascending, kissat 4.0.4 (official
  linux-amd64 binary, sha256 21da5d98...ac93a1), cap <= 275s per piece,
  WIN-stop rule: on the first SAT stop the sweep and publish (remaining
  minpos values not swept, no absence claimed for them). UNSAT/INDET pieces
  are honest negatives per piece only.
- Pre-declaration calibrations (ran before this commit, disclosed here):
  1. 6x20 q7 class {2} (six-row-q7-m22 kit control): SAT, 641,859 conflicts —
     bit-exact with the published anchor (six-row-q7-m21-class-split-20261114).
  2. Family control 7x24 q7 class {3} krow=3:5 minpos=1 (the piece containing
     the published m=24 witness row3=[1,3,6,19,21]): SAT, 64,031 conflicts;
     decoded 41 stones rows [6,6,6,5,6,6,6], row3=[1,11,15,17,23] — a
     different witness in the same piece (disclosed), dual-verified
     (sat.js verifyConfig ok + fresh Python Fraction verifier safe/maximal).
  3. 7x26 q7 class {3} krow=3:5 plain: INDET at 280s, 1,575,348 conflicts;
     7x26 minpos=0: INDET at 285s, 1,575,157 conflicts — cap-limited honest
     negatives (m=26 is known SAT by the rowY=3 encoding; not absence).
- Machinery: sat3.js/sat2.js/sat.js/verify_frac.py byte-clones of the
  seven-row-q8-m25-class-split-20261128 kit scripts (MANIFEST sha256
  bda3754f pins them; sat.js fcc0cfd8, sat2.js 14ceb854, sat3.js e04581eb,
  verify_frac.py 837fe24b).
- Declaration-time HEAD: 580e37030f00dc1dadb3328e486e212cfe94b713.
- Non-claims: no 11x11 root / two-stone root {60,27} / third move
  {100,108} / S2 / closure-class verdict is created, consumed, or
  transferred; all remain UNKNOWN. Conflict counts are bookkeeping.
- This declaration takes single ownership of the 7x27 (7,7) class-split
  lane for this session; parallel executions of the same cells should defer.
