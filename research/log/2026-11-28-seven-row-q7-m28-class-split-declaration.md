# 2026-11-28 seven-row q7 7x28 SAT-side class {3} krow/minpos decomposition — single-owner declaration (publish-then-execute)

- Task: continue the (7,7) class-split lane one width further. Attack the
  new frontier width 7x28 with the same machinery that resolved 7x27 as
  SAT this session (class {3} single-deficiency central class,
  krow=3:5, minpos P=0..13 sound H-split, floor((m-1)/2)=13 at m=28).
  A SAT piece at 7x28 would give **M_{7,7} >= 29** (range currently
  [28,708] after the 7x27 completion commit d22d0587).
- Known structure (measured this session, disclosed): a +1 right-shift
  of the new 7x27 witness onto 7x28 is safe but leaves exactly cell
  (0,3) unblocked (not maximal); the shift-0 placement leaves (27,3);
  so 7x28 needs a genuinely new witness (same one-stone-short pattern
  as the (7,8) 7x25 -> 7x26 transition).
- Sweep plan: pieces minpos=0,1,2,... ascending, kissat 4.0.4
  (official linux-amd64 binary, sha256 21da5d98...ac93a1), cap <= 275s
  per piece, WIN-stop rule: on the first SAT stop and publish
  (remaining pieces not swept, no absence claimed). UNSAT/INDET pieces
  are honest negatives per piece only. If the first pieces are INDET,
  continue up to the piece budget of this session and publish the
  honest negatives.
- Machinery: the seven-row-q7-m27-class-split-20261128 kit scripts
  (sat.js fcc0cfd8 / sat2.js 14ceb854 / sat3.js e04581eb /
  verify_frac.py 837fe24b), already calibrated this session
  (6x20 class {2} 641,859 bit-exact; 7x24 class {3} krow=3:5 minpos=1
  SAT 64,031 family control; 7x27 deciding instance cold pair
  byte-identical).
- Declaration-time HEAD: 3131cf9f7 (six-row 6x26 multi-deficiency lane
  declared by a parallel session at 3131cf9f7; this lane is disjoint).
- Non-claims: no 11x11 root / two-stone root {60,27} / third move
  {100,108} / S2 / closure-class verdict is created, consumed, or
  transferred; all remain UNKNOWN. Conflict counts are bookkeeping.
- This declaration takes single ownership of the 7x28 (7,7)
  class-split lane for this session; parallel executions of the same
  cells should defer.
