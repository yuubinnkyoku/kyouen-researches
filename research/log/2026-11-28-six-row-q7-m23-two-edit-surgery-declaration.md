# 2026-11-28 six-row q7 6x23 two-edit surgery — single-owner declaration (publish-then-execute)

- Task: complete two-edit surgery (S' = seed - R + A, |R| <= 2,
  |A| <= 2, final size <= 35, A on empty cells, target cell T occupied
  or blocked) of the published 6x22 witness
  (six-row-q7-m22-class-split-20261127, class {2} krow=2:5 minpos=7,
  35 stones rows [6,6,5,6,6,6]) on the **6x23 board**, the current
  M_{6,7} frontier (range [23,402]). A safe-maximal S' would give
  **M_{6,7} >= 24**.
- Known structure (published): the +1 right-shift of the m=22 witness
  on 6x23 is safe but leaves cell (0,2) unblocked
  (shift1_on_m23.json); class {2} k=5 minpos 6/7/8 pieces all INDET at
  262s caps (4.93M..5.06M conflicts).
- Sweep plan: surgery at both placements — +1 shift with T=(0,3-free
  column, published as (0,2)) and shift-0 with T the shift-0 uncovered
  cell (measured before the run, disclosed in the completion). Engine:
  surgery_general.py (byte-clone of the six-row-q6-m26 kit script,
  sha256 8ae82dde...b6b6b6a, q/board parameterized). Calibration: the
  published 6x26 case reproduced byte-exactly this session
  (calib-m26.json sha 7cfe56c7... == published surgery-m26.run1.json).
- Declaration-time HEAD: 2df06c1b5 (parallel sessions own
  6x31 q5 class {2} (631d2204), 7x32 q6 class {3} (7d49c0e6),
  (7,8) 7x26 q8 (93c10bc78), 6x26 multi-deficiency (3131cf9f7), the
  n11 ladder lanes, and 3-row q4 m=30; this lane is disjoint).
- Non-claims: no 11x11 root / two-stone root {60,27} / third move
  {100,108} / S2 / closure-class verdict is created, consumed, or
  transferred; all remain UNKNOWN. A negative result is a local
  (edit-distance <= 2) negative only, not an absence claim for 6x23.
- This declaration takes single ownership of the 6x23 (6,7) two-edit
  surgery for this session; parallel executions of the same cells
  should defer.
