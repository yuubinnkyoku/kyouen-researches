# z19 beyond/frontier spot-probe kit (frozen)

This directory is the publish-then-execute PRIMARY RECORD of a FROZEN
spot-probe extending three active observation series of the vertical-fiber
strip program one slice ahead (z=19), published immediately after the
z18-min13 census kit as its first follow-up. No K slot is claimed and no
claim is made: everything is finite machine observation against the pinned
raw engine, plus one engine-free closed-form pre-computation. The z=19
census kit and the T-Z18/T-Z19 declaration lanes are NOT prejudiced by
anything here.

## Contents

- `engine_block.py` — sha256 `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`
  (the pinned engine block, byte-identical to the K1282..K1325 chain and
  the z18-min13 kit; embedded startup pin `bd5f22e4…`).
- `beyond_z19.py` — sha256
  `9af65882f81eda64dccee85380a06caa1a3aaab282fe109b217762a5badd0f5b`
  (sections (a)-(e): the m=10/m=9/m=8-row z=19 records in the IDENTICAL
  published enumerations of the z=18 records, the engine-free TENTH-tail
  supply identity pre-computation v(s,20,20) vs v(s,19,20) plus the z=18
  identity recheck, z=19 strip spots for m in {13..17} at the provisional
  T-Z19 claim positions, and the m=14 base spot).
- `beyond_z19.out` — sha256
  `045df5208318c7628c1cb705d44e2be95a9a8b2c8ee9f1f76417934d1a1ffc03`
  (the frozen stdout; FIVE runs — default, PYTHONHASHSEED=1 same cwd,
  env -i isolated dirs x2 — all byte-identical, rc 0, ~6.5 s per run).
- Ordered-engine independent cross-check (outside the frozen artifact):
  all 766 shapes of the three records re-evaluated with H_ordered —
  0 mismatches.

## What the probe recorded (observation, judgment-free)

- **m=10-row z=19 record (first beyond slice for min=10; R=30; 170
  shapes, identical enumeration): EXACTLY 1 separation, X=(10,10), S=20,
  DOWN: 0 (collapse 1)** — the (10,10) frontier separation FLIPS
  UP->DOWN exactly one slice beyond the frontier, precisely the
  (8,8) arc's flip-at-+1 behavior (z=14 UP -> z=15 DOWN). The even-m
  beyond-arc rule now reads flip-at-+1 on 2/2 even-m data points
  (m=8, m=10).
- **m=9-row z=19 record (second odd-m beyond slice; R=29; 234 shapes,
  identical enumeration): 2 separations**:
  - X=(9,10), S=19, DOWN: 1 (collapse 2) — the (9,10) position FLIPS
    UP->DOWN at +2 (it decayed 2->1 at +1 without flipping), so the
    odd-m arc DOES flip eventually: at +2, not at +1;
  - X=(9,12), S=21, UP: 2 (collapse 0) — a NEW separation, born at +2
    past the frontier at gap +3 (position (m, m+3)); it MATCHED the
    collapse at z=17/z=18 inside the same enumerated shapes and
    separates only now. Compare the (8,10) birth at gap +2 at +2 past
    the frontier: odd m grows at gap +3, even m at gap +2 (2 data
    points each).
- **m=8-row z=19 record (fifth consecutive beyond slice; R=27; 362
  shapes, identical enumeration): 0 separations** — the EMPTY beyond
  set PERSISTS (z=18 -> z=19 both empty): total reabsorption is a
  stable terminal state; no re-emergence has ever been observed.
- **TENTH-tail supply identity pre-computation (engine-free)**:
  v(s,20,20)=v(s,19,20) HOLDS exactly on {0}∪{12..19} and breaks
  UNIFORMLY as 0 vs 1 for ALL s>=20 — the even/odd structure of the
  closed-form supply identities now reads: odd z (17, 19): hold through
  s=z, uniform 0v1 break from s=z+1, matching the hole+tail F-tail
  class at odd z; even z (16, 18): break starting AT s=z (z=18 with the
  anomalous 0v2@(18) + 2v1@(19+) double profile; z=16 published single
  break at 16), matching the single-point F-tail class at even z. The
  z=18 identity is rechecked over the extended domain {0}∪{12..47}: the
  published statement reproduces (hold {0,12..17}, 0v2 break at 18,
  2v1 for s>=19, including the two new tail values at s=56,57).
- **z=19 strip spots at the provisional T-Z19 claim positions
  (m∈{13..17}, R=m+20): 15/15 match.**
- **m=14 base spot H(34;(14,14);19) = 1 = v(28,19,34)** — the base-spot
  alternation across floors extends to 0 (z16/m11), 1 (z17/m12),
  0 (z18/m13), 1 (z19/m14): four data points, alternating with z
  parity.

## Standard caveats

Everything in this kit is a FINITE machine observation against the pinned
raw engine, plus a pure closed-form pre-computation. Nothing here is a
theorem, nothing universal is claimed, and no verdict of any game position
(11x11 standard board, two-stone roots, S2, class 1/2/4 — all UNKNOWN) is
consumed. The z=19 census kit and any declaration lane keep full freedom
to re-measure, extend or contradict anything recorded here.
