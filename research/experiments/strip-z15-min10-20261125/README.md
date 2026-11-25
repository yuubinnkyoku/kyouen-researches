# z15-min10 pre-declaration exploration kit (frozen)

This directory is the publish-then-execute PRIMARY RECORD for the pre-declaration
census of the z=15 min>=10 (floor-10) slice — the next slice registered as open by
the K1319 declaration note §5/§7 (T-Z15). No K slot is claimed by this kit and no
claim is made here: everything below is machine observation. The declaration lane
(a later run) picks up the slot claim, the paper proof, the verification machine
and the official runs.

## Contents

- `engine_block.py` — sha256 `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`
  (the pinned engine block, byte-identical to the K1282..K1319 chain; sha256 of the
  embedded block itself is the startup pin `bd5f22e4…`).
- `explore_z15pre.py` — sha256 `3e2a8ab863212efc3806a6acb93caeb7c9020ead468e1afa9cb6ffd4c2714513`
  (adapted from the frozen `explore_z14pre.py` by the disclosed textual diff:
  z 14→15, cell budget j+15→j+16, floor 9→10, 9 rungs j∈{1..9} with the provisional
  9th-rank label `A3` (small token 9), s domain {0}∪{10..40}, strip m∈{10..14} at the
  T-Z15 claim position, an IN-BAND m=9-row record at z=15 (R=25, the T-Z15 base-child
  position — z*(9)=17>15 makes this the FIRST slice whose base child is in-band
  rather than on the frontier), strip spots m∈{15..18}, the m=10 base spot, and a
  below-band bottom-rung child census section (f) `H(16;Y;16)` vs `v(s,16,16)`.
  Per-cell `H.cache_clear()` retained to avoid the z=13 shared-cache OOM lesson).
- `explore_z15pre.out` — sha256 `2cf0a9664f46c2c1eff27e387a20d32b16eebb5cd45a19335f397bd9eb30dfe7`
  (the frozen stdout; deterministic — three runs with default, PYTHONHASHSEED=random
  and env -i isolated all byte-identical, rc 0, ~17 s per run; no randomness, no
  wall-clock, no hash-order dependence in the output).

## What the census recorded (observation, judgment-free; see the predecl log)

- 9 floor-10 cells at z=15 (`Cell_j(s) := H(j+16;{j}∪Y;15)`, Y tokens >= 10):
  ALL cells s-only (multivalue rows 0) over 221 shapes each (s ∈ {0}∪{10..40},
  arity 0..4). Deviant structure: **F {s=14 DOWN, s>=16 CONSTANT-2 UP TAIL with a
  clean hole at s=15}** (26 deviants in-domain, tail continuing through the tail
  spots s∈{41..48} — the F-family SIXTH tail form: the constant-2 tail is REBORN
  at z=15 after the tailless z=14, and unlike z=13 it is NOT C-hand-inherited
  (the C-hand source F14f9 is tailless) but generated through the below-band
  bottom-rung child, measured separately in section (f)), G {s=14 DOWN}, E {s=12
  DOWN, s=14 UP}, D {s=12 DOWN}, C {s=10 DOWN, s=12 UP}, B {s=10 DOWN}, A (j=7)
  {s=10 UP}, A2 (j=8) NONE (full collapse), **A3 (j=9, min=9 — the IN-BAND
  T-Z15 base-child cell) NONE (full collapse)**.
- NO death-point deactivation at this slice: every published z=14 deviant position
  ({10,12,14}) sits at or above the new floor 10, and the measured z=15 deviant
  positions are exactly the surviving supply-source positions (contrast: the
  z=13→z=14 transition killed the s=8 sources of C13f8/B13f8/A13f8).
- Tail spots s∈{41..48} all 9 cells: only F15f10 mismatches (8 rows, value 2 vs
  collapse 0, tail unbroken); the other 8 cells all match (64/64).
- Below-band bottom-rung child census (f): `H(16;Y;16)` = `v(s,16,16)` for ALL 221
  floor-10 shapes (0 deviants, 0 multivalue rows) — the new supply source is itself
  a full collapse (the z=15 analog of the z=13/z=14 (B2)/(B3) stair-bottom
  lemmas; the hand derivation of the complete F15f10 structure (DOWN at s=14,
  hole at s=15, tail from s=16) is consistent with it).
- T-Z15 claim position (m∈{10..14}, arity<=3, parts>=m): 594 shapes, 0 violations.
- IN-BAND m=9-row record at z=15 (R=25, parts >= 9 INCLUDING co-token 9 shapes,
  arity<=3, S∈{9..47}): **152 shapes, 0 separations** — strong affirmative data
  for the open m=9 row residual z∈{15,16} (z*(9)=17; contrast: the z=14 frontier
  out-of-band record had exactly one separation X=(8,8), outside the frontier on
  the m=8 row; here the position is strictly in-band and shows none).
- Strip spots m∈{15..18}: 12/12 match. m=10 base spot H(26;(10,10);15)=1=v(20,15,26).

See `research/log/2026-11-25-z15-predecl-exploration.md` for the full primary-source
timeline, honest disclosure and handoff instructions.
