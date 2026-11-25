# z20 beyond/frontier spot-probe kit (frozen)

This directory is the publish-then-execute PRIMARY RECORD of a FROZEN
spot-probe measuring the z=20 discriminating data points of the active
observation series of the vertical-fiber strip program, published
immediately after the z19-min14 census kit as its first follow-up
(same session). No K slot is claimed and no claim is made: everything is
finite machine observation against the pinned raw engine, plus
engine-free closed-form pre-computations. The T-Z19 declaration lane and
the (future) z=20 census lane are NOT prejudiced by anything here.

## Contents

- `engine_block.py` — sha256 `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`
  (the pinned engine block, byte-identical to the K1282..K1328 chain and
  the z18-min13 / z19-beyond / z19-min14 kits; embedded startup pin
  `bd5f22e4…`).
- `beyond_z20.py` — sha256
  `17974ab0dd476c91e4c81863102cc5c31fc3da4e7f8b4a05e61dec8b43d26ff3`
  (sections (1)-(10), all predeclared in the docstring BEFORE the first
  run: the m=10/m=9/m=8-row z=20 beyond records in the IDENTICAL published
  enumerations (170/234/362 shapes), the m=11-row z=20 record — the
  FOURTH AND FINAL entry of the K1322 published residual band m=11
  z∈{17..20} —, the m=12-row z=20 record (THIRD entry, K1325 band
  m=12 z∈{18..21}), the m=13-row z=20 record + arity<=4 co-token
  extension (SECOND entry, K1328 band m=13 z∈{19..24}), z=20 strip
  spots m∈{14..18} at the provisional T-Z20 claim positions R=m+21,
  the m=15 base spot (z-parity candidate 0), the engine-free
  ELEVENTH-tail supply identity recheck v(s,21,21) vs v(s,20,21)
  (published as the z19-min14 census kit section (g2)) and the NEW
  engine-free TWELFTH-tail supply identity pre-computation
  v(s,22,22) vs v(s,21,22) over s∈{0}∪{12..57}).
- `beyond_z20.out` — sha256
  `281311e87db85da3b608d80f5b5f79843e40ff5fcc8bb792ba0217654d19094c`
  (the frozen stdout; FIVE runs — default, default re-run,
  PYTHONHASHSEED=1 same cwd, env -i isolated dirs ×2, all
  byte-identical, rc 0, ~10.4 s per run; no randomness, no wall-clock,
  no hash-order dependence).
- Ordered-engine independent cross-check (outside the frozen artifact,
  re-executed in full in this session): ALL 1,119 record shapes
  (170+234+362+110+92+76+75) re-enumerated and re-evaluated with
  `H_ordered` against the canonical engine — **0 mismatches**; every
  frozen record's shape count and separation list reproduced exactly;
  the 15 strip spots, the base spot and both identities' full
  hold/break row sets re-derived and byte-exact against the frozen
  rows.

## What the probe recorded (observation, judgment-free)

- **m=10-row z=20 beyond record (second beyond slice, +2 past the
  frontier z*(10)=18; R=31; 170 shapes, identical enumeration):
  2 separations**:
  - X=(10,10), S=20, DOWN: 0 (collapse 2) — the flipped diagonal
    PERSISTS DOWN at +2, exactly the (8,8) arc's +2 behavior
    ({(8,8)DOWN}@z16 before reabsorbing at +3);
  - X=(10,12), S=22, UP: 2 (collapse 1) — a NEW separation BORN at +2
    past the frontier at gap +2 (position (m,m+2)); it MATCHED the
    collapse at z=18/z=19 inside the same enumerated shapes and
    separates only now. Compare the (8,10) birth (gap +2, +2 past the
    frontier): the even-m gap+2 birth rule now reads 2/2 (m=8, m=10);
    the predeclared REABSORB candidate for the m=10 row is
    COUNTEREXAMPLIFIED (no separation vanished; a second was born).
- **m=9-row z=20 beyond record (third beyond slice, +3; R=30; 234
  shapes, identical enumeration): 1 separation**: X=(9,12), S=21, UP: 1
  (collapse 0) — the z=19 birth PERSISTS with value decay 2→1, and
  **(9,10) REABSORBS at +3** — precisely the (8,8)-analogy prediction
  (reabsorption around +3) recorded in the published z19 probe's
  handoff; both predeclared directions resolved as predicted.
- **m=8-row z=20 beyond record (sixth beyond slice, +6; R=29; 362
  shapes, identical enumeration): 2 separations**:
  - X=(8,12), S=20, DOWN: 0 (collapse 2);
  - X=(8,14), S=22, UP: 2 (collapse 1).
  The beyond set was EMPTY at z=18 AND z=19; at z=20 it is NON-EMPTY
  again — **the FIRST OBSERVED RE-EMERGENCE of the series after total
  reabsorption**, and the re-emergence is at NEW positions (gap +4 and
  gap +6), not at the reabsorbed old positions. The predeclared
  candidate "remains empty" is COUNTEREXEMPLIFIED, and the z19 probe's
  "no re-emergence has ever been observed / total reabsorption is a
  stable terminal state" reading is thereby falsified as a rule
  candidate at its next test. Note also the S-structure: the m=8 and
  m=10 rows both carry exactly (DOWN at S=20, UP 2v1 at S=22) —
  the two rows' separation multisets coincide position-wise in S
  ((8,12)/(10,10) DOWN at S=20; (8,14)/(10,12) UP 2v1 at S=22)
  while sitting at different gaps (observation, 1 event).
- **m=11-row z=20 record (R=32, published residual-band style):
  110 shapes, 0 separations** — the FOURTH AND FINAL entry of the
  K1322 published residual band m=11 z∈{17..20}: the band closes 4/4
  with all four entries 110 shapes / 0 separations (identical
  enumerations; z*(11)=21, so the m=11 frontier z=21 belongs to the
  next slice).
- **m=12-row z=20 record (R=33): 92 shapes, 0 separations** — the
  THIRD entry of the K1325 published residual band m=12 z∈{18..21}
  (92/92/92 so far).
- **m=13-row z=20 record (R=34): 76 shapes, 0 separations** plus the
  arity<=4 co-token extension **75 shapes, 0 separations** — the SECOND
  entry of the K1328 published residual band m=13 z∈{19..24};
  cross-artifact consistent with the z19-min14 census kit's z=19 entry
  (76/75, same enumerations).
- **z=20 strip spots at the provisional T-Z20 claim positions
  (m∈{14..18}, R=m+21): 15/15 match.**
- **m=15 base spot H(36;(15,15);20) = 0 = v(30,20,36)** — the base-spot
  alternation across floors extends to 0 (z16/m11), 1 (z17/m12),
  0 (z18/m13), 1 (z19/m14), 0 (z20/m15): five data points, alternating
  with z parity as predeclared.
- **ELEVENTH-tail supply identity recheck (engine-free)**: the z19
  census kit's pre-computation reproduces exactly over the same domain:
  v(s,21,21)=v(s,20,21) HOLDS on {0}∪{12..19}, breaks at s=20 as
  0-vs-2, then UNIFORMLY as 2-vs-1 for ALL s∈{21..56} — the exact
  z=18 even-z identity shape, frozen cross-artifact consistency.
- **TWELFTH-tail supply identity pre-computation (engine-free, NEW)**:
  v(s,22,22)=v(s,21,22) HOLDS on **{0}∪{12..21}**, breaks UNIFORMLY as
  0-vs-1 for ALL s∈{22..57} — the predeclared odd-z=21 candidate
  (hold through s=z, uniform 0v1 break from s=z+1) CONFIRMED; the
  odd-z identity form is now 3/3 (z=17, z=19, z=21 pre-computed). This
  is the z=21 slice's supply datum.

## Standard caveats

Everything in this kit is a FINITE machine observation against the
pinned raw engine, plus pure closed-form pre-computations. Nothing here
is a theorem, nothing universal is claimed, and no verdict of any game
position (11x11 standard board, two-stone roots, S2, class 1/2/4 — all
UNKNOWN) is consumed. The T-Z19 declaration lane and the z=20 census
lane keep full freedom to re-measure, extend or contradict anything
recorded here. Section (9)/(10) are pure closed-form pre-computations:
no engine recursion is involved at all; they inherit only the
published K0832 single-token closed form.

See `research/log/2026-11-25-z20-beyond-probe.md` for the primary-source
timeline, honest disclosure and handoff instructions.
