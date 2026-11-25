# z18-min12 pre-declaration exploration kit (frozen)

This directory is the publish-then-execute PRIMARY RECORD for the
pre-declaration census of the z=18 min>=12 (floor-12) slice — the FIFTH
edition of the floor-(z−6) series (after z=15 K1321, the z=16 min>=10 kit
`059c531e`, the z=17 min>=11 kit `82f98ef4`, and the z=19 min>=13 kit of
this same run). No K slot is claimed by this kit and no claim is made here:
everything below is finite machine observation against the pinned engine.
The declaration lane (a later run) picks up the slot claim (candidate
T-Z18(min>=12)), the paper proof, the verification machine and the official
runs.

## Contents

- `engine_block.py` — sha256
  `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`
  (the pinned engine block, byte-identical to the K1282..K1335 chain; sha256
  of the embedded block itself is the startup pin `bd5f22e4…`).
- `explore_z18f12.py` — sha256
  `c5f8e704da5697f24ff55dc55f3c5f8c14c6f6d8740a955be8894aab02b4dafb`
  (adapted from the frozen published `explore_z18f13.py` `152fd2d8…` by the
  disclosed textual diff: floor 13→12, cell budget R=j+19 with 13 rungs
  (provisional label `A7`, small token 13, one rank beyond the published
  T-Z18 cell table depth), s domain {0}∪{12..43}, tail spots {44..51},
  strip m∈{12..16} (m=12 base-claim column NEW; m=13..16 re-measure the
  published z18f13 sweep), boundary s=12 special children d1/d2/d3, strip
  spots m∈{17..20}, the m=12 base spot, the below-band child census
  H(19;Y;19) vs v(s,19,19), the NINTH-tail supply identity recheck over
  s∈{0}∪{12..55}, and the z=17 PARTNER identity recheck (the odd-z
  k=17 supply form) over the same domain. The FULL predeclared (m4)
  candidate — the ENGINE-FREE closed-form revival cascade {B DOWN 0v2,
  A UP 1v0, A2 UP 2v1}@s=12, derived from the published z=17 s=12
  (iii)-hand supply constants before the first run — is in the file
  docstring. Per-cell `H.cache_clear()` retained.
- `explore_z18f12.out` — sha256
  `a5389e448be06106465d7fe56c6a05fad67c85cf1e671e6c1c9c0f5f3bb3bf51`
  (the frozen stdout; deterministic — SIX runs: default ×3,
  PYTHONHASHSEED=1 same-cwd, env -i isolated dirs ×2 (explicit
  `/usr/local/bin/python3`), all byte-identical, rc 0, ~24-27 s per run;
  no randomness, no wall-clock, no hash-order dependence).

## What the census recorded (observation, judgment-free; see the predecl log)

- 13 floor-12 cells at z=18 (`Cell_j(s) := H(j+19;{j}∪Y;18)`, Y tokens
  >= 12, s ∈ {0}∪{12..43}, arity 0..4): ALL cells s-only (multivalue rows 0)
  over 174 shapes each.
- **THE s=12 REVIVAL CASCADE, EXACTLY THE PREDECLARED (m4) PROFILE
  {B DOWN 0v2, A UP 1v0, A2 UP 2v1}** — B {12: value 0 vs collapse 2},
  A {12: value 1 vs collapse 0}, A2 {12: value 2 vs collapse 1}, one
  shape each, and NOTHING else at s=12. The even-z floor revival profile
  is now **value-exact 2/2** (z=16 floor-10 `059c531e`: {B,A,A2} =
  {0v2, 1v0, 2v1} at s=10; z=18 floor-12 here: identical constants at
  s=12): the +2-revival candidate (the reopened even floor re-loads the
  same {B,A,A2} triple at s=z−6 with unchanged values) is now a 2/2
  value-exact pair, and the engine-free pre-cascade (`precascade.py`,
  pure published K0832 constants, written before the first run) predicted
  it correctly on every component. The j=13 rung (the kit's open case,
  depending on two UNPUBLISHED children) CONFORMS (see d2/d3 below).
- The deviant structure above s=12 is the published floor-13 profile
  {14,16,18} plus the z=18 even-slice F single-point form: F
  {18: UP 1v0} (single point at s=z, NO hole, NO tail; tail spots
  44..51: 104/104 match across all cells); G {16: DOWN 0v2, 18: UP 2v1};
  E {16: UP 1v0}; D {14: DOWN 0v2, 16: UP 2v1}; C {14: UP 1v0};
  A3..A7 fully collapsed. The even-z station structure
  {DOWN:0, UP:1, UP:2} at consecutive stations — identical rank heads and
  constants to the published z=18/z=20/z=22 even slices: the z=18 ladder
  profile is z-slice-invariant under the floor 13→12 drop except for the
  revived s=12 triple.
- Boundary s=12 special children: (d1) H(30;{12,11};18) = 0 = collapse,
  cross-artifact with the published m=11-row z=18 record member
  (K1322 band, closed); (d2) H(31;{13,11};18) = 1 = v(24,18,31) collapse —
  the UNPUBLISHED (i)-child of rung 13 measured and conforming;
  (d3) H(31;{13,12};17) = 0 = v(25,17,31) collapse — the UNPUBLISHED
  (iii)-child (min 13, R=31, z=17, one above the proved T-Z17 m=12 claim
  position; a simultaneous min-drop probe). The sharp j=13 open case
  resolves CONFORM.
- Strip sweep m∈{12..16} (z=18, S∈{m..m+39}, arity<=3 parts): **358
  shapes, 0 violations** (cumulative 107/191/259/314/358); the m=12 column
  (107 shapes, 0 violations) is the NEW candidate T-Z18(min>=12) claim
  position; the m=13..16 columns reproduce the published z18f13 sweep
  (cross-artifact consistency).
- m=12 base spot H(31;(12,12);18) = **1** = v(24,18,31), the K1334
  lemma-S candidate (12+1)%2 = 1 CONFIRMED; strip spots m∈{17..20}:
  12/12 match.
- Below-band bottom-rung child H(19;Y;19) vs v(s,19,19): 174 shapes,
  **0 deviants, 0 multivalue**.
- NINTH-tail supply identity recheck (engine-free K0832): v(s,19,19) =
  v(s,18,19) holds exactly on {0}∪{12..17}, breaks 0v2 at s=18, then
  uniformly 2v1 for ALL s∈{19..55} — the published z18 constants
  reproduced and extended.
- z=17 PARTNER identity recheck (engine-free K0832): v(s,18,18) =
  v(s,17,18) holds exactly on {0}∪{12..17}, uniform 1v0 break for ALL
  s∈{18..55} — the odd-z k=17 supply form, cross-artifact with this run's
  z19/z21/z22 identity chain.

## Independent ordered-engine cross-check (outside the frozen artifact)

14 key positions of the frozen output (the full revival triple {B,A,A2}@12,
the surviving-profile rows of F/G/E/D/C, d1/d2/d3, the base spot)
recomputed with the independent H_ordered engine: **0 mismatches**
(`ordered_crosscheck_final.log`, 37/37 across this run's three kits —
after correcting an R-offset bug in the crosscheck script's first draft
that mis-mapped kit-2 rows; the kits' own frozen outputs were never
affected, and the corrected crosscheck passes every row).

## Honesty notes

- The (m4) predeclaration was derived ENGINE-FREE (pure published K0832
  closed form, `precascade.py`) before the first run; the frozen artifact
  matched it exactly (revival triple, j=1..12 conform, boundary children).
- Everything is finite observation; no universal statement is claimed; no
  verdict of any game position is consumed. Standard 11×11 empty board and
  all central-reply roots: UNKNOWN, unchanged. The declaration lane owns
  any T-Z18(min>=12) slot claim.
