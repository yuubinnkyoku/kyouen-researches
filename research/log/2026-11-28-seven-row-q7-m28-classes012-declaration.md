# 2026-11-28 seven-row q7 7x28 SAT-side classes {0}/{1}/{2} + class {3} minpos 5/6 — single-owner declaration (publish-then-execute)

- Task: continue the (7,7) 7x28 class-split sweep over the pieces left
  unswept by seven-row-q7-m28-class-split-20261128 (commit c11fe4d7):
  the first-time mirror classes {0}/{1}/{2} (krow=y:5 each; H-mirror
  covers {6}/{5}/{4}) and the class {3} continuation pieces minpos=5
  and minpos=6 (krow=3:5). A SAT piece at 7x28 gives **M_{7,7} >= 29**
  (range currently [28,708]).
- Known structure (published): class {3} pieces minpos 0,1,2,3,4,7 all
  INDET at 275s caps, near-uniform resistance (2,730,916..3,454,167
  conflicts); the +1 shift of the 7x27 witness leaves (0,3) unblocked,
  so a genuinely new witness is needed.
- Sweep plan: calibration control first (7x24 q7 class {3} krow=3:5
  minpos=1, expect SAT 64,031 conflicts per the published family
  control), then class {3} minpos=5, minpos=6, then class {0} krow=0:5
  minpos=0, class {1} krow=1:5 minpos=0, class {2} krow=2:5 minpos=0,
  ascending minpos within each class as time allows. kissat 4.0.4
  (official linux-amd64 binary, sha256 21da5d98...ac93a1), cap <= 275s
  per piece, WIN-stop rule: on the first SAT stop and publish
  (remaining pieces not swept, no absence claimed). INDET pieces are
  honest negatives per piece only.
- Machinery: byte-clones of the seven-row-q7-m27-class-split-20261128
  kit scripts (sat.js fcc0cfd8 / sat2.js 14ceb854 / sat3.js e04581eb /
  verify_frac.py 837fe24b), MANIFEST-pinned in that kit.
- Declaration-time HEAD: 3686a5c0f (parallel sessions own
  6x31 q5 class {2} (631d2204), 7x32 q6 class {3} (7d49c0e6),
  (7,8) 7x26 q8 (93c10bc78), 6x26 multi-deficiency (3131cf9f7), the
  n11 ladder lanes, and 3-row q4 m=30; this lane is disjoint from all
  of them).
- Non-claims: no 11x11 root / two-stone root {60,27} / third move
  {100,108} / S2 / closure-class verdict is created, consumed, or
  transferred; all remain UNKNOWN. Conflict counts are bookkeeping.
- This declaration takes single ownership of the 7x28 (7,7) classes
  {0}/{1}/{2} and class {3} minpos 5/6 pieces for this session;
  parallel executions of the same cells should defer.
