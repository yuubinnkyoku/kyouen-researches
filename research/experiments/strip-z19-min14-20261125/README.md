# z19-min14 pre-declaration exploration kit (frozen)

This directory is the publish-then-execute PRIMARY RECORD for the pre-declaration
census of the z=19 min>=14 (floor-14) slice — the next slice of the vertical-fiber
strip series after the K1328 (T-Z18) official runs. No K slot is claimed by this
kit and no claim is made here: everything below is machine observation. The
declaration lane (a later run) picks up the slot claim, the paper proof, the
verification machine and the official runs.

## Contents

- `engine_block.py` — sha256 `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`
  (the pinned engine block, byte-identical to the K1282..K1328 chain; sha256 of the
  embedded block itself is the startup pin `bd5f22e4…`).
- `explore_z19f14.py` — sha256
  `e41138e20d254922030c14b4bc07a06de838de9c51527967a3ec5029722ef325`
  (adapted from the frozen published `explore_z18f13.py`
  `152fd2d8814f958e5aaef275f83b4abb1763b58929d375d7ec9cb864f2a94ff4` by the
  disclosed textual diff: z 18→19, cell budget j+19→j+20, floor 13→14, rungs
  12→13 with the provisional 13th-rank label `A7` (small token 13 — the FIFTH
  consecutive in-band base child; z*(13)=25 > 19), s domain {0}∪{14..44},
  strip m∈{14..18} at the provisional T-Z19 claim position, an IN-BAND
  m=13-row record at z=19 (R=33, the T-Z19 base-child position AND the FIRST
  entry of the K1328 published residual band m=13 z∈{19..24}, frontier z=25;
  published residual-band style arity<=3 TOTAL, plus an arity<=4 co-token
  extension sweep), an IN-BAND m=12-row record at z=19 (R=32, the SECOND
  entry of the K1325 published residual band m=12 z∈{18..21}; SAME enumeration
  as the published z=18 entry → same 92 shapes), an IN-BAND m=11-row record
  at z=19 (R=31, the THIRD entry of the K1322 published residual band
  m=11 z∈{17..20}; SAME enumeration as the published z=17/z=18 entries →
  same 110 shapes), strip spots m∈{19..22}, the m=14 base spot (cross-checked
  against the published z19 probe value), the below-band bottom-rung child
  census `H(20;Y;20)` vs `v(s,20,20)`, and section (g): the TENTH-tail
  supply identity RECHECK `v(s,20,20)` vs `v(s,19,20)` (published by the
  z19 probe kit; rechecked and extended over s∈{0}∪{12..56}) plus the NEW
  engine-free ELEVENTH-tail supply pre-computation `v(s,21,21)` vs
  `v(s,20,21)`. Per-cell `H.cache_clear()` retained (z=13 shared-cache OOM
  lesson).
- `explore_z19f14.out` — sha256
  `3354dfc6c7f65dedc02aeb95fa257e8a19526e1a5a25fd45e040b287d9dd510f`
  (the frozen stdout; deterministic — FIVE runs: default, default re-run,
  PYTHONHASHSEED=1 same cwd and env -i isolated dirs ×2, all byte-identical,
  rc 0, ~19 s per run; no randomness, no wall-clock, no hash-order
  dependence).

## What the census recorded (observation, judgment-free; see the predecl log)

- 13 floor-14 cells at z=19 (`Cell_j(s) := H(j+20;{j}∪Y;19)`, Y tokens >= 14):
  ALL cells s-only (multivalue rows 0) over 117 shapes each
  (s ∈ {0}∪{14..44}, arity 0..4). Deviant structure — the deviant positions
  are **{14, 16, 18} plus the F tail from s>=20**. The whole published z=18
  position set {14,16,18} survives the floor shift (all >= floor 14):
  **the fourth consecutive floor shift triggers NO definition-domain
  exclusion** (contrast the s=12 exclusion at z=17→18); instead the profile
  RE organizes:
  **F {s=18 DOWN:1 (collapse 2), s=19 HOLE, s>=20 persistent tail UP:2
  (collapse 0)}** — the F-family TENTH tail typology = **HOLE+TAIL**: the
  z-relative profile is IDENTICAL to the z=15 (sixth) and z=17 (eighth)
  forms (DOWN:1 at z−1, hole at z, persistent UP:2 tail from z+1): the
  odd-z profile is now 3/3 odd slices and the typology alternation
  single@(even z) / hole+tail@(odd z) has FIVE consecutive consistent
  slices. Tail spots s∈{45..52}: F mismatches 8/8 (value 2 vs collapse 0);
  all other 96 rows match — the tenth-form tail is persistent and
  window-external, like the z=17 eighth form.
  **G {s=18 DOWN:0 (collapse 1)}**; **E {s=16 DOWN:1 (collapse 2), s=18
  UP:2 (collapse 0)}**; **D {s=16 DOWN:0 (collapse 1)}**; **C {s=14 DOWN:1
  (collapse 2), s=16 UP:2 (collapse 0)}**; **B {s=14 DOWN:0 (collapse 1)}**;
  **A {s=14 UP:2 (collapse 0)}** — the FIRST A-rank deviant since z=17
  (A17f12 {12 UP:2}), and it sits at s=14 = z−5, exactly the z−5 relative
  position of the z=17 A break (s=12 = 17−5); **A2..A7 NONE (SIX consecutive
  full collapses after the single A break)**; **A7 (j=13, min=13) fully
  collapsed over its 117-shape cell domain** — the FIFTH consecutive
  in-band base child (z*(13)=25 > 19), the T-Z19 base m=14
  trivial-absorption candidate. Per-position triplets: the z=19 ladder
  carries a repeating **{DOWN:1, DOWN:0, UP:2}** triplet at positions
  14/16/18 (position 14 = {C,B,A}, 16 = {E,D,C}, 18 = {F,G,E}), one rank
  LOWER per position than the z=18 ladder, and its value multiset is
  exactly the z=17 base-position triplet {C17f12 DOWN:1, B17f12 DOWN:0,
  A17f12 UP:2} — the odd-z ladder base triplet appears to repeat (2/2 odd
  slices, observation).
- Provisional T-Z19 claim position sweep (m∈{14..18}, arity<=3, parts>=m):
  **230 shapes, 0 violations** (cumulative per m: 14→68, 15→123, 16→167,
  17→202, 18→230).
- IN-BAND m=13-row record at z=19 (R=33, published residual-band style,
  parts >= 13 INCLUDING co-token 13, arity<=3 TOTAL, S∈{13..51}): **76
  shapes, 0 separations** — the FIRST entry of the K1328 published residual
  band m=13 z∈{19..24} AND the T-Z19 base-child record; the arity<=4
  co-token extension sweep: **75 shapes, 0 separations** (75 = 76 − the
  single-token row (13,): the co-token enumeration omits it and no arity-4
  shape fits S<=51; machine-checked). Together with A719f14's full cell
  collapse this fixes the T-Z19 base m=14 as the FIFTH consecutive
  trivial-absorption base candidate.
- IN-BAND m=12-row record at z=19 (R=32, SAME enumeration as the published
  z=18 entry): **92 shapes, 0 separations** — the SECOND entry of the
  K1325 published residual band m=12 z∈{18..21}.
- IN-BAND m=11-row record at z=19 (R=31, SAME enumeration as the published
  z=17/z=18 entries): **110 shapes, 0 separations** — the THIRD entry of
  the K1322 published residual band m=11 z∈{17..20}.
- Strip spots m∈{19..22}: 12/12 match. m=14 base spot H(34;(14,14);19) = 1 =
  v(28,19,34) — EXACTLY the published z19 probe value (cross-artifact
  consistency; the cross-floor base-spot sequence 0/1/0/1 stands at four
  floors).
- Below-band bottom-rung child census: `H(20;Y;20)` = `v(s,20,20)` for ALL
  117 floor-14 shapes (0 deviants, 0 multivalue) — the FIFTH consecutive
  full collapse of the below-band supply child.
- **TENTH-tail supply identity RECHECK (engine-free, section g1)**: the
  published z19 probe statement reproduces exactly on the extended domain:
  `v(s,20,20)=v(s,19,20)` HOLDS on **{0}∪{12..19}**, breaks UNIFORMLY as
  0-vs-1 for ALL s∈{20..56}. The F19f14 hole sits at s=19, the identity's
  final hold point (= z), and the tail starts exactly at the first break
  position (s=20) — the supply-to-deviant alignment is exact.
- **ELEVENTH-tail supply pre-computation (engine-free, NEW, section g2)**:
  `v(s,21,21)=v(s,20,21)` HOLDS on **{0}∪{12..19}**, breaks at **s=20 as
  0-vs-2**, then UNIFORMLY as **2-vs-1 for ALL s∈{21..56}** — the EXACT
  z=18 even-z identity shape ({0v2@z, 2v1@(z+1)+}), predeclared candidate
  "break starts at s=20" confirmed. The even-z identity form now reads:
  z=16 uniform 1-vs-0 (published), z=18 and z=20 (pre-computed here for the
  z=20 slice) the {0v2@z + 2v1@(z+1)+} form, 2/2 on the newest form. This
  is the z=20 slice's supply datum (z=20 census F-cell: single-point
  candidate at s=20).
- Independent ordered-engine cross-check (outside the frozen artifact):
  the FULL census re-enumerated and re-evaluated with `H_ordered` —
  1,521 cell shapes + 104 tail spots + 230 strip shapes + 76/75/92/110
  record shapes + 12 strip spots + the base spot + 117 below-band shapes:
  **0 mismatches**; every frozen row (deviant lists, shape counts,
  separation lists, identity hold/break rows) reproduced.

See `research/log/2026-11-25-z19m14-predecl-exploration.md` for the
primary-source timeline, honest disclosure and handoff instructions.

## Standard caveats

Everything in this kit is a FINITE machine observation against the pinned raw
engine. Nothing here is a theorem, nothing universal is claimed, and no verdict
of any game position (11x11 standard board, two-stone roots, S2, class 1/2/4 —
all UNKNOWN) is consumed. Battery/point counts are engine cross-checks, not
proofs. The paper proofs, the slot claim and the verification machine belong to
the declaration lane. Section (g) is a pure closed-form pre-computation: it uses
no engine recursion at all and inherits only the published K0832 single-token
closed form.
