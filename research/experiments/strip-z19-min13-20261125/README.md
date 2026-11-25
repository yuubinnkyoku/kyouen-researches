# z19-min13 pre-declaration exploration kit (frozen)

This directory is the publish-then-execute PRIMARY RECORD for the
pre-declaration census of the z=19 min>=13 (floor-13) slice — the FOURTH
edition of the floor-(z−6) series (after z=15 min>=9 proved in K1321, the
z=16 min>=10 kit `059c531e`, and the z=17 min>=11 kit `82f98ef4`). No K slot
is claimed by this kit and no claim is made here: everything below is finite
machine observation against the pinned engine. The declaration lane (a later
run) picks up the slot claim (candidate T-Z19(min>=13)), the paper proof, the
verification machine and the official runs.

## Contents

- `engine_block.py` — sha256
  `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`
  (the pinned engine block, byte-identical to the K1282..K1335 chain; sha256
  of the embedded block itself is the startup pin `bd5f22e4…`).
- `explore_z19f13.py` — sha256
  `f83b7955ca59d4325cf077f6bea3fee47bd35637a10cd9859cd4231fcdc3ad0e`
  (adapted from the frozen published `explore_z19f14.py`
  `e41138e2…` by the disclosed textual diff: floor 14→13, cell budget
  R=j+20 with 14 rungs (provisional 15th-rank-style label `A8`, small token
  14, one rank beyond the published T-Z19 cell table), s domain
  {0}∪{13..44}, tail spots {45..52}, strip m∈{13..17} (m=13 base-claim
  column NEW; m=14..17 re-measure the published z19f14 sweep), boundary
  s=13 special children d1/d2/d3, strip spots m∈{18..21}, the m=13 base
  spot, the below-band child census H(20;Y;20) vs v(s,20,20), and the
  TENTH-tail supply identity recheck over s∈{0}∪{12..56}. The FULL
  predeclared (n1)-(n4) candidate (engine-free K0832 cascade for
  j=1..14 at s=13, written before the first run) is in the file docstring.
  Per-cell `H.cache_clear()` retained.
- `explore_z19f13.out` — sha256
  `4e9c668c711e9accf7beb6d75c526acc2eaad242c4bde5cfeda16c175d2db275`
  (the frozen stdout; deterministic — SIX runs: default ×3,
  PYTHONHASHSEED=1 same-cwd, env -i isolated dirs ×2 (explicit
  `/usr/local/bin/python3`), all byte-identical, rc 0, ~27-30 s per run;
  no randomness, no wall-clock, no hash-order dependence).

## What the census recorded (observation, judgment-free; see the predecl log)

- 14 floor-13 cells at z=19 (`Cell_j(s) := H(j+20;{j}∪Y;19)`, Y tokens
  >= 13, s ∈ {0}∪{13..44}, arity 0..4): ALL cells s-only (multivalue rows 0)
  over 149 shapes each.
- **NO s=13 class anywhere — the odd-s domain entry is EMPTY, the predeclared
  (n1)/(n4) candidate CONFIRMED. The odd-s class absence rule is now 2/2**
  (z=17 s=11 empty in the published kit `82f98ef4`; z=19 s=13 empty here),
  pairing with the even-z floor revival rule (z=16 s=10, z=18 s=12 both
  LOAD classes — 3/3 with the z=18 revival confirmed engine-free-first in
  the z18-min12 kit of this same run).
- The deviant structure above s=13 is **exactly the published floor-14
  profile {14,16,18} ∪ {F tail s>=20}, shifted nowhere**: F {18: DOWN 1v2} +
  conforming hole@19 + tail UP 2v0 from s=20 (shape counts 1,1,1,1,1,1,2,2,
  3,3,4,4,5,5,6,6,7,7,8,9,10,11,13,14,16 over s=20..44, F tail spots
  45..52: 8/8 rate-2 mismatch, all other cells 104/104 match); G
  {18: DOWN 0v1}; E {16: DOWN 1v2, 18: UP 2v0}; D {16: DOWN 0v1}; C
  {14: DOWN 1v2, 16: UP 2v0}; B {14: DOWN 0v1}; A {14: UP 2v0};
  A2..A8 fully collapsed (SEVENTH consecutive full collapse past the A rung
  in the series' odd slices). The odd-z station triplet
  {DOWN:1, DOWN:0, UP:2} at {C,B,A}@14, {E,D}@16, {F,G,E}@18 — identical
  rank heads and constants to the published z17/z19/z21 odd slices: the
  z=19 ladder profile is z-slice-invariant under the floor 14→13 drop.
- **Rungs 13 and 14 (A7/A8, outside/matching the boundary of the published
  cell tables) FULLY COLLAPSED** — the (n2)/(n3) and the sharp open case
  (n4) j=14 BOTH RESOLVED AS CONFORM. The two UNPUBLISHED boundary
  children measured directly: (d2) H(33;{14,12};19) = 0 = v(26,19,33)
  (collapse; the (i)-child injects 0, not the value 1 that would have
  broken the rung) and (d3) H(33;{14,13};18) = 1 = v(27,18,33) (collapse;
  a simultaneous min-drop probe one position above the proved T-Z18 m=13
  claim). (d1) H(32;{13,12};19) = 1 = collapse, cross-artifact with the
  published m=12-row z=19 record member.
- Strip sweep m∈{13..17} (z=19, S∈{m..m+39}, arity<=3 parts): **286
  shapes, 0 violations** (cumulative 84/152/207/251/286); the m=13 column
  (84 shapes, 0 violations) is the NEW candidate T-Z19(min>=13) claim
  position; the m=14..17 columns reproduce the published z19f14 sweep
  (cross-artifact consistency).
- m=13 base spot H(33;(13,13);19) = **0** = v(25,19,33), the K1334
  lemma-S candidate (13+1)%2 = 0 CONFIRMED; strip spots m∈{18..21}:
  12/12 match.
- Below-band bottom-rung child H(20;Y;20) vs v(s,20,20): 149 shapes,
  **0 deviants, 0 multivalue** (the floor-13 edition of the below-band
  collapse).
- TENTH-tail supply identity recheck (engine-free K0832): v(s,20,20) =
  v(s,19,20) holds exactly on {0}∪{12..19}, uniform 0v1 break for ALL
  s∈{20..56} — the published z19 probe + z19-min14 constants reproduced
  and extended.

## Independent ordered-engine cross-check (outside the frozen artifact)

30 key positions of the frozen output (the full deviant set of
cells F/G/E/C/B/A, the surviving-profile class rows, d1/d2/d3, the base
spot, the A7/A8 rung-13/14 rows) recomputed with the independent
H_ordered engine: **0 mismatches** (`ordered_crosscheck_final.log`,
37/37 across this run's three kits).

## Honesty notes

- The (n4) predeclaration was derived ENGINE-FREE (pure published K0832
  closed form, `precascade.py`) before the first run, per the
  publish-then-execute protocol; the frozen artifact then matched it on
  every component (no text gap, no undisclosed class this time).
- Everything is finite observation; no universal statement is claimed; no
  verdict of any game position is consumed. Standard 11×11 empty board and
  all central-reply roots: UNKNOWN, unchanged. The declaration lane owns
  any T-Z19(min>=13) slot claim.
