# z20-floor14 pre-declaration exploration kit (frozen)

This directory is the publish-then-execute PRIMARY RECORD for the
pre-declaration census of the z=20 FLOOR-14 (z-6, SUB-CRITICAL floor)
lattice — the floor-NECESSITY exploration of the z=20 slice and the
test of the REGISTERED PREDICTION of the published z=22 floor-16 kit
log section 5 (commit `daa9a805`: "head trio {B 0v2, A 1v0, A2 2v1}
at s=14 and the ladder B {16 UP 2v1}, C {16 UP 1v0}, D {16 DOWN 0v2,
18 UP 2v1}, E {18 UP 1v0}, F {20 UP 1v0}, G {18 DOWN 0v2, 20 UP 2v1}
— 11 entries total, the same cellwise constants, all cells s-only,
0 multivalue rows; each row single-shape, matching the arithmetic
set {z-6, z-4, z-2, z} at z=20. If the z=20 edition hits this
profile exactly, the full-lattice uniformity reaches 4/4 across ALL
consecutive even z 16..22.").

This kit is the SEVENTH edition of the published floor-(z-6)
sub-critical series (after z=15 K1321, the z=16 min>=10 kit
`059c531e`, the z=17 min>=11 kit `82f98ef4`, the z=18 min>=12 kit
`0bb7e440`, the z=19 min>=13 kit `5b2275bc` and the z=22 floor-16
kit `fb215b76`/`daa9a805`), and the LAST unswept even floor below
z=24; the z=20 floor-14 census itself was unclaimed at kit-build
time (path probe: no `strip-z20-floor14*` / `strip-z20-min14*`
directory; the odd z=21 sub-critical slot is a separate open lane).
NO K slot is claimed by this kit and no universal statement is made
here: everything below is machine observation plus disclosed paper
derivations written BEFORE the first run of the frozen file. The
declaration lane (a later run) picks up any slot claim, the paper
proof, the verification machine and the official runs.

## Contents

- `engine_block.py` — sha256 `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`
  (byte-clone of the published chain engine; identical to the
  strip-z22-floor16 / strip-z20-min15 kit bytes; the embedded
  block's sha256 is the startup pin `bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92`).
- `explore_z20f14.py` — sha256
  `ba6528e018ab9a65d97c67acadf9bce99fb51703d7ef0e9b62796309d67ceb71`
  (adapted from the frozen published `explore_z22f16.py`
  `d3c3239e…` (commit `fb215b76`) by the disclosed textual diff:
  slice z 22→20 with floor 16→14, rungs 15→14 aligned with the
  published z=20 critical ladder F20f15..A820f15 (no rank beyond A8
  is swept — a j=15 rung's s=14 point is not paper-derivable from
  any published fact; disclosed in the docstring), cell s-domain
  {0}∪{14..45}, tail spots {46..53}, strip m∈{14..19} (m=14 NEW
  open-row co-token sweep S∈{14..53}; m∈{15..19} proved T-Z20
  compliance recheck), the m=14/13/12 row records plus the m=14
  arity<=4 extension as cross-artifact rechecks, the NEW m=14 base
  spot H(35;(14,14);20) with the paper-derived candidate disclosed
  in the docstring BEFORE the first run, the below-band child
  census at z'-7 (z'=21, floor 14 = z'-7), the identity rechecks
  13th..16th extended to {0}∪{12..61}, plus the NEW SEVENTEENTH-tail
  engine-free pre-computation with BOTH components predeclared).
- `explore_z20f14.out` — sha256
  `919df78c96a1a818164732c23673db805165f267340a0ea0b152d2ae117f9ab1`
  (the frozen stdout, 29,398 bytes; deterministic — SIX runs:
  default ×3, PYTHONHASHSEED=random same-cwd, env -i isolated
  directories ×2 via /usr/local/bin/python3, all byte-identical,
  rc 0 each, ~28 s per run; no randomness, no wall-clock, no
  hash-order dependence).

Honest disclosure (frozen into the docstring): the s=14 head-row
hand derivation was written in-session from published PROVED facts
only (T-Z19/K1330 z=19 critical ladder constants, the K1264 stair
equality, the K0832 closed form, the published T-Z19 m=14-row claim,
the published f15 census constants) and its child-position input
constants were cross-checked against a drafting scratch engine
evaluation BEFORE the freeze (the K1344-D6 discipline: derivation →
engine cross-check of the input literals → freeze); the file itself
ran for the first time only after the freeze and was never edited
after any of its runs (two docstring typo fixes were made BEFORE the
six frozen runs; the stdout is a pure function of the code bytes and
was verified byte-identical across the typo fix). The genuinely blind
pre-declarations (none engine-checked before the freeze): the
sub-floor block s∈{28..45}, the multivalue census, the strip/row/
base-spot/below-band/identity measurements, and every measured
count. Row/strip shape counts are measured counts, not predeclared,
per series convention.

## The predeclaration and how it landed (observation, judgment-free)

THE MEASUREMENT HIT THE COMPLETE PREDECLARED PROFILE EXACTLY —
the architecture predicted by the registered §5 prediction AND the
in-file hand-derivation landed with zero undisclosed classes; all
14 cells s-only, 0 multivalue rows anywhere (the third fully-closed
pre→measure cycle of the floor-(z-6) series after z=18's (m4)
cascade and z=22's complete cycle; this kit's is the second COMPLETE
cell-ladder profile at a sub-critical floor).

### Floor necessity + the registered even full-lattice prediction (section a)

- **THE s=14 ROW (NEW, head of the floor-14 ladder): the registered
  head trio CONFIRMED — B20f14 DOWN 0v2, A20f14 UP 1v0, A220f14 UP
  2v1** (H(27;(6,14);20)=0 != v(20,20,27)=2, H(28;(7,14);20)=1 !=
  v(21,20,28)=0, H(29;(8,14);20)=2 != v(22,20,29)=1); every other
  rung CONFORMS exactly as predeclared (F/G/E/D/C conform
  1/0/1/0/1; A3..A8 conform 0/1/0/1/0/1), all single-shape (j,14).
  Consequences (observation, recorded for the declaration lane):
  (1) the critical floor 15 = z-5 is NECESSARY at z=20 for the
  cell-ladder Sigma-collapse — the universal floor-14 cell claim
  FAILS with the three witnesses above (the z=22 result reproduces
  at z=20: the floor-necessity witnesses now exist at BOTH swept
  even editions z>=20... together with the published z16/z18
  editions, at all four);
  (2) the even-z A-rank sub-critical revival is value-exact 4/4
  (z=16 s=10, z=18 s=12, z=20 s=14, z=22 s=16 — all UP 1v0 at
  s=z-6; never the odd-z s=z-5 UP 2v0 birth form);
  (3) **the FULL 11-entry deviant lattice is cellwise VALUE-EXACT
  4/4 across the consecutive even z 16,18,20,22** — at z=20 the
  measured lattice is B {14 DOWN 0v2, 16 UP 2v1}, C {16 UP 1v0},
  D {16 DOWN 0v2, 18 UP 2v1}, E {18 UP 1v0}, F {20 UP 1v0},
  G {18 DOWN 0v2, 20 UP 2v1}, A {14 UP 1v0}, A2 {14 UP 2v1}, the
  s-positions exactly the arithmetic set {14,16,18,20} =
  {z-6, z-4, z-2, z}; machine acceptance comparison against the
  published z16-f10/z18-f12 frozen outputs and the published
  z22-f16 .out: cellwise identical constants (see the log §3.1).
- **s∈{15..27}: LATTICE IDENTITY with the published f15 census EXACT**
  (the Y-shape sets coincide below s=28; every deviant row equal to
  the published f15 profile — F {20 UP 1v0}, G {18 DOWN 0v2,
  20 UP 2v1}, E {18 UP 1v0}, D {16 DOWN 0v2, 18 UP 2v1},
  C {16 UP 1v0}, B {16 UP 2v1}, A..A8 collapsed — machine
  cross-compare 6/6 cells recorded in the log; the shared engine
  points are identical by determinism).
- **s∈{28..45} (BLIND sub-floor block; 14-token components enter
  at s=28): NO multivalue rows, NO new deviant classes** — the
  f14-only shapes conform to the same s-value pattern; s-only
  survives at z=20 as it did at z=22 (the second sub-critical
  multi-token test of the series).

### Strip, row records, spots (sections b,c,d,e)

- Strip m∈{14..19} (R=m+21): **253 shapes, 0 violations**; the NEW
  m=14 open-row co-token sweep carries **68 shapes, 0 violations**;
  the m∈{15..19} T-Z20 compliance recheck: incrementals
  55/44/35/28/23 = the published f15 cumulative profile EXACT
  (cross-artifact machine-compare recorded in the log).
- m=14-row z=20 (R=35): **62 shapes 0 separations** (x0 style) +
  **61 shapes 0 separations** (arity<=4 co-token ext) — the
  published f15 entries reproduced shape-for-shape (expected 62/61,
  hit exactly; the K1330 published residual band m=14 z∈{20..25}
  first-entry datum rechecked).
- m=13-row z=20: **76/0**; m=12-row z=20: **92/0** — the published
  f15 entries reproduced shape-for-shape (K1328/K1325 residual-band
  datum contexts).
- Tail spots s∈{46..53}: **112/112 match**; strip spots m∈{20..23}:
  **12/12 match** (lattice identity with the published f15 rows).
- **NEW m=14 base spot H(35;(14,14);20) = 1, conforming** (=
  v(28,20,35); the paper-derived candidate hit exactly; never
  measured by any published kit). The m=14 base-spot z-sequence:
  z=19: 1 (the PROVED T-Z19 claim value), z=20: 1 (here) — no
  alternation yet; z=21 datum pending a future lane.

### Below-band (z'-7 datum, section f)

H(21;Y;21) vs v(s,21,21), min(Y)>=14 (child slice z'=21, floor
14 = z'-7): **130 shapes, 0 deviants, 0 multivalue** — full
collapse of the below-band supply child at floor z'-7; the FIFTH
recorded z'-7 empty datum (published: z'=17/19/20/23; here z'=21),
extending the empty pattern to 5/5. The published K1264 stair
applicability R=21 <= 21+min(Y) makes this collapse an instance of
a PROVED lemma (machine corroboration, not a new theorem); the
generalization belongs to the declaration lane.

### Supply identities (engine-free, pure published K0832 closed form)

All over the EXTENDED domain {0}∪{12..61} (each published
{0}∪{12..60} domain extended by one point):

- THIRTEENTH-tail recheck: hold {0}∪{12..21} (11 rows), 0v2@22,
  uniform 2v1 for ALL s∈{23..61} (published constants reproduced,
  extended by one).
- FOURTEENTH-tail recheck: hold {0}∪{12..23} (13 rows), uniform
  0v1 for ALL s∈{24..61}.
- FIFTEENTH-tail recheck: hold {0}∪{12..23} (13 rows), 0v2@24,
  uniform 2v1 for ALL s∈{25..61}.
- SIXTEENTH-tail recheck: hold {0}∪{12..25} (15 rows), uniform 0v1
  for ALL s∈{26..61} (published NEW by the z22-f16 kit, extended).
- **SEVENTEENTH-tail identity (NEW)**: v(s,27,27)=v(s,26,27) holds
  exactly on **{0}∪{12..25}** (15 rows), breaks **0v2 at s=26**,
  then **UNIFORM 2v1 for ALL s∈{27..61}** — BOTH predeclared
  components CONFIRMED (break start s=26 AND the uniform 2v1
  shape). The even-z supply-identity form is now **4/4**
  (z=20/z=22/z=24 measured + z=26 closed-form pre-computation
  here) — the z=26 slice's supply datum, registered for the future
  z=24/z=25/z=26 declaration lanes.

## Independent ordered-engine cross-check (outside the frozen artifact)

A local (unpublished) ordered-engine re-evaluation of all 1,820
cell-census positions (H_ordered over the same shape sets) found 0
multivalue rows and 0 mismatches with the frozen canonical values:
`checked 1820 ordered-engine mismatches 0`. Recorded here per the
series convention; the script itself stays local exactly like the
z22-f16 kit's crosscheck.

## Standard caveats

Everything in this kit is FINITE machine observation against the
pinned raw engine, plus pure closed-form pre-computations, plus
disclosed hand derivations whose status is that of candidates
written before measurement (the s=14 head row and the base spot
with the disclosed pre-freeze drafting engine verification of the
input constants; everything else blind). Nothing here is a theorem;
no universal statement is claimed; the witnesses are single-position
evaluations of the defining recursion recorded per the series'
observation convention. Standard 11×11 empty board, two-stone roots,
S2, class 1/2/4 and all central-reply roots: all UNKNOWN, unchanged;
no verdict consumed. The battery/point counts are engine
cross-checks, not proof substitutes.
