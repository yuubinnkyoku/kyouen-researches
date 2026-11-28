# 2026-11-28 six-row q7 6x23 class {2} minpos continuation + classes {0}/{1} first coverage — single-owner declaration (publish-then-execute)

- Task: continue the (6,7) 6x23 SAT-side sweep. Unswept pieces:
  class {2} krow=2:5 minpos 0..5 and 9..11 (the published sweep
  covered only minpos 6/7/8, all INDET at 262s caps 4.93M..5.06M
  conflicts), and first-time classes {0} krow=0:5 / {1} krow=1:5 at
  minpos=0 (H-mirror covers {5}/{4}). A SAT piece at 6x23 gives
  **M_{6,7} >= 24** (range currently [23,402]).
- Known structure: the m=22 witness (class {2} krow=2:5 minpos=7)
  resolves 6x22; the two-edit surgery of that witness on 6x23 is
  negative at both placements (published this session, kit
  six-row-q7-m23-two-edit-surgery-20261128); sound minpos bound at
  m=23 is floor((23-1)/2)=11.
- Sweep plan: calibration control first (6x20 q7 class {2}, expect SAT
  641,859 conflicts per the published control), then class {2} minpos
  0,1,2,... ascending, then 9,10,11, then class {0} minpos=0 and
  class {1} minpos=0 as time allows. kissat 4.0.4 (pinned binary
  21da5d98...ac93a1), cap <= 272s per piece, WIN-stop rule: on the
  first SAT stop and publish. INDET pieces are honest negatives per
  piece only.
- Machinery: byte-clones of the seven-row-q7-m27-class-split-20261128
  kit scripts (sat.js fcc0cfd8 / sat2.js 14ceb854 / sat3.js e04581eb /
  verify_frac.py 837fe24b), pinned by that kit's MANIFEST.
- Declaration-time HEAD: cac230d05. Disjoint from all
  parallel-owned lanes (6x31 q5, 7x32 q6, (7,8) 7x26 q8, 6x26
  multi-deficiency, n11 ladder, 3-row q4 m=30, 4-row q6 m=35).
- Non-claims: no 11x11 root / two-stone root {60,27} / third move
  {100,108} / S2 / closure-class verdict is created, consumed, or
  transferred; all remain UNKNOWN. Conflict counts are bookkeeping.
- This declaration takes single ownership of the 6x23 (6,7) SAT-side
  sweep pieces listed above for this session; parallel executions of
  the same cells should defer.
