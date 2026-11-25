# 2026-11-25 z=18 min>=12 (floor-12) pre-declaration census kit — exploration log

Lane: high-speed lane (this run). Status of this document: PRIMARY RECORD of
the pre-declaration census kit `research/experiments/strip-z18-min12-20261125/`.
No K slot is claimed, no universal statement is claimed. Everything below is
finite machine observation against the pinned raw engine, plus engine-free
closed-form pre-computations. The declaration lane (a later run) picks up
from here (candidate T-Z18(min>=12)).

## 1. Context, prior-lane state and slot check

Floor-(z−6) series state at kit-build time: z=15 min>=9 (K1321);
z=16 min>=10 (kit `059c531e` — the s=10 class REVIVAL, the first even-floor
LOAD datum); z=17 min>=11 (kit `82f98ef4` — odd entry EMPTY); z=19 min>=13
(this run's first kit, odd entry EMPTY 2/2). z=18 min>=12 was UNMEASURED:
the second even-floor datum, and the first chance to test the revival
profile as an ENGINE-FREE PREDECLARATION (the z=16 revival had been observed
first, predicted after). Checked: no `research/experiments/strip-z18-min12*`
directory, no z18m12 log; the published z18-min13 kit and the K1328/K1330
chains are the floor-13 references; main tip at build `4761668e`.

## 2. Kit construction (publish-then-execute, frozen before publication)

- `engine_block.py` — byte-clone of the published chain engine (sha256
  `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`);
  embedded startup pin `bd5f22e4…` asserted by the script (gate PASS).
- `explore_z18f12.py` (sha256
  `c5f8e704da5697f24ff55dc55f3c5f8c14c6f6d8740a955be8894aab02b4dafb`)
  — adapted from the frozen published `explore_z18f13.py` (`152fd2d8…`)
  by the disclosed diff: 13 floor-12 cells Cell_j(s) := H(j+19;{j}∪Y;18)
  (Y>=12, s∈{0}∪{12..43}, arity<=4; provisional 13th-rung label A7, small
  token 13 — one rank beyond the published T-Z18 table depth), tail spots
  {44..51}, strip m∈{12..16} at the candidate T-Z18(min>=12) claim position
  (m=12 column NEW; m=13..16 re-measure the published z18f13 sweep),
  boundary s=12 special children (d1/d2/d3), strip spots m∈{17..20}, the
  m=12 base spot, the below-band child census H(19;Y;19) vs v(s,19,19),
  the NINTH-tail recheck, and the z=17 PARTNER identity recheck (both
  engine-free) over s∈{0}∪{12..55}.
- THE FULL PREDECLARED CANDIDATE (docstring (m4), written before the first
  run): an ENGINE-FREE revival cascade (`precascade.py`, pure published
  K0832 closed form and the published z=17 floor-12 supply constants; NO
  raw-engine values) predicting the s=12 domain entry RE-LOADS the classes
  with profile **{B DOWN 0v2, A UP 1v0, A2 UP 2v1}** — the same
  {B,A,A2} = {0,1,2}-form constants as the z=16 floor-10 revival — plus
  j=1..11 conform, j=12 conform (observed (i)-child use), and the SHARP
  j=13 open case (two UNPUBLISHED children d2/d3). Per-cell
  `H.cache_clear()` retained.
- Determination protocol: SIX runs (default ×3, PYTHONHASHSEED=1, env -i
  isolated ×2), all byte-identical (sha256
  `a5389e448be06106465d7fe56c6a05fad67c85cf1e671e6c1c9c0f5f3bb3bf51`,
  rc 0, ~24-27 s each). The frozen `explore_z18f12.out` IS that stdout.
- Independent ordered-engine cross-check: 14 key positions (the revival
  triple, the surviving rows of F/G/E/D/C, d1/d2/d3, the base spot) with
  H_ordered: 0 mismatches after the crosscheck's own first-draft R-offset
  bug was corrected (see §4).

## 3. Observations (all judgment-free)

- 13 cells, 174 shapes each, ALL s-only (multivalue 0).
- **THE s=12 REVIVAL CASCADE: {B DOWN 0v2, A UP 1v0, A2 UP 2v1} EXACTLY
  THE ENGINE-FREE PREDECLARATION.** B {12: 0 vs 2}, A {12: 1 vs 0}, A2
  {12: 2 vs 1}, one shape each, nothing else at s=12. The even-floor
  revival profile is now value-exact 2/2 (z=16 s=10, z=18 s=12), a +2
  candidate: the reopened even floor re-loads the same {B,A,A2} triple at
  s=z−6 with unchanged values. The engine-free pre-cascade predicted it
  correctly on every component (including the conform of j=1..12 and the
  j=13 open case, whose two unknown children measured d2=1, d3=0 and the
  rung collapsed).
- The deviant structure above s=12 is the published floor-13 profile
  {14,16,18} plus the even-slice F single-point form: F {18: UP 1v0}
  (single point at s=z, no hole, no tail; tail spots 104/104 match across
  all cells); G {16: DOWN 0v2, 18: UP 2v1}; E {16: UP 1v0}; D
  {14: DOWN 0v2, 16: UP 2v1}; C {14: UP 1v0}; A3..A7 fully collapsed.
  Even stations {DOWN:0, UP:1, UP:2} — identical rank heads and constants
  to the published z=18/z=20/z=22 even slices.
- Boundary: d1 H(30;{12,11};18) = 0 = collapse (cross-artifact, published
  m=11-row z=18 record member); d2 H(31;{13,11};18) = 1 = v(24,18,31)
  collapse (UNPUBLISHED, measured); d3 H(31;{13,12};17) = 0 = v(25,17,31)
  collapse (UNPUBLISHED, measured; a min-drop probe one above the proved
  T-Z17 m=12 claim position).
- Strip m∈{12..16}: 358 shapes, **0 violations** (107/191/259/314/358) —
  the m=12 column is the NEW candidate T-Z18(min>=12) base-claim dossier;
  m=13..16 columns reproduce the published z18f13 sweep.
- m=12 base spot H(31;(12,12);18) = 1 = collapse — K1334 lemma-S candidate
  (12+1)%2 = 1 CONFIRMED. Strip spots m∈{17..20}: 12/12 match.
- Below-band child H(19;Y;19) vs v(s,19,19): 174 shapes, 0 deviants,
  0 multivalue.
- NINTH-tail recheck: hold {0}∪{12..17}, 0v2 break at s=18, uniformly 2v1
  for s∈{19..55} — published z18 constants reproduced, extended.
- z=17 PARTNER recheck: hold {0}∪{12..17}, uniform 1v0 break for
  s∈{18..55} — the odd-z k=17 supply form, cross-artifact with this run's
  z19/z21/z22 identity chain.

## 4. Honest record (this run)

- The (m4) predeclaration was derived BEFORE the first run, engine-free
  (K0832 closed form + published z=17 supply constants only): this is the
  first floor-revival of the series predicted in writing before measurement.
  The frozen artifact matched it exactly (revival triple AND the j-rung
  conform story).
- Crosscheck disclosure: the shared ordered-engine crosscheck's first
  draft mis-mapped this kit's cells at R=j+20 (correct: R=j+19); three
  FAIL lines were printed against wrong-R expectations and corrected in
  the final crosscheck, which passes all rows. The kit's own frozen
  output (R=j+19 from the start) was never wrong.
- Push protocol: latest main re-fetched immediately before the push; the
  z18-min12 slot confirmed unclaimed. No wall-clock, no randomness, no
  hash-order dependence.

## 5. Handoff to the declaration lane

- The candidate T-Z18(min>=12) declaration has its measured dossier: the
  13-cell ladder (with the revival triple isolated at s=12 and everything
  else profile-invariant from floor-13), the strip m=12 ledger (107/0),
  the base spot (lemma-S), the boundary children, the below-band census.
  A proof structure that handles the revived {B,A,A2} classes at s=12
  is the key new burden relative to the floor-13 proof; the z=16
  floor-10 precedent (`059c531e` + K1321-adjacent material) is the
  template.
- The floor-necessity open rule now reads: even floors LOAD s=z−6 classes
  (3/3, value-exact 2/2), odd floors load nothing (2/2). The even-side
  next datum (z=20 floor-14, s=14 revival {B,A,A2}) and the odd-side z=21
  floor-15 entry are the natural follow-ups.
- The revival constants extend the supply-side story: the s=12 revival
  profile is the SAME {B,A,A2} = {0,1,2} ladder the z=16 kit measured;
  any universal claim about even-floor revival remains for the
  declaration lane.

## 6. Standard caveats

Everything in this kit and log is FINITE machine observation against the
pinned raw engine, plus pure closed-form pre-computations. Nothing here is
a theorem; no universal statement is claimed; no verdict of any game
position is consumed. Standard 11×11 empty board, two-stone roots
{49,60}/{59,60}, S2 {59,60}, classes 1/2/4, and all central-reply roots:
all UNKNOWN, unchanged.
