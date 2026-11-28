# 2026-11-28 seven-row q8 7x26 SAT-side class {3} krow/minpos decomposition — single-owner declaration (publish-then-execute)

- Task: attack the new (7,8) frontier width 7x26 in the SAT direction with the
  same krow/minpos class-split machinery (class {3} single-deficiency central
  class, krow=3:6, minpos P=0..12 sound H-split, floor((m-1)/2)=12)) that
  resolved 7x25 as SAT (M_{7,8} >= 26; current published range [26,651]).
  A SAT piece at 7x26 would give M_{7,8} >= 27.
- Known structure (published): a +1 right-shift of the 7x25 witness onto
  7x26 is safe but leaves exactly cell (0,3) unblocked (not maximal), so 7x26
  needs a genuinely new witness; no mirror-class INDET baseline exists for
  7x26 yet (7x25's was INDET at 250s before the class split resolved it).
- Sweep plan: pieces minpos=0,1,2,... in ascending order, kissat 4.0.4
  (pinned binary sha256 21da5d98...), cap <= 275s per piece, WIN-stop rule:
  on the first SAT stop the sweep and publish (remaining minpos values are
  not swept and no absence is claimed for them). UNSAT/INDET pieces are
  honest negatives per piece only.
- Pre-declaration calibration (disclosed here, ran before this commit):
  regenerated the 7x25 class {3} krow=3:6 minpos=2 CNF and re-ran kissat:
  SAT, 666,158 conflicts — bit-exact reproduction of the published deciding
  instance (kit seven-row-q8-m25-class-split-20261128, commit 7c400d18).
- Machinery: sat3.js/sat2.js/sat.js/verify_frac.py as published in the
  seven-row-q8-m25-class-split-20261128 kit (byte-clones of the m22 kit;
  MANIFEST sha256 bda3754f pins them).
- Declaration-time HEAD: 1615e0a6e198653099ddc2935be5859ff7d023aa.
- Non-claims: no 11x11 root / two-stone root {60,27} / third move
  {100,108} / S2 / closure-class verdict is created, consumed, or
  transferred; all remain UNKNOWN. Conflict counts are bookkeeping.
- This declaration takes single ownership of the 7x26 (7,8) class-split
  lane for this session; parallel executions of the same cells should defer.
