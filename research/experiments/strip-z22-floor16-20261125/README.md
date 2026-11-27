# z22-floor16 pre-declaration exploration kit (frozen)

This directory is the publish-then-execute PRIMARY RECORD for the
pre-declaration census of the z=22 FLOOR-16 (z-6, SUB-CRITICAL floor)
lattice — the floor-NECESSITY exploration of the z=22 slice (the
"z-6 floor unswept" open item registered by the published K1339
completion log section 5 / K1339 declaration note section 5).
This kit is the SIXTH edition of the published floor-(z-6)
sub-critical series (after z=15 K1321, the z=16 min>=10 kit
`059c531e`, the z=17 min>=11 kit `82f98ef4`, the z=18 min>=12 kit
`0bb7e440` and the z=19 min>=13 kit `5b2275bc`) and its first
edition in the z >= 20 range; the z=22 floor-16 census itself was
unclaimed at kit-build time (path probe, no counter-publication).
NO K slot
is claimed by this kit and no universal statement is made here:
everything below is machine observation plus disclosed paper
derivations written BEFORE the first run. The declaration lane (a later
run) picks up any slot claim, the paper proof, the verification machine
and the official runs.

## Contents

- `engine_block.py` — sha256 `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`
  (byte-clone of the published chain engine; identical to the
  strip-z20/z21/z22-min17 kit bytes; the embedded block's sha256 is the
  startup pin `bd5f22e4…`).
- `explore_z22f16.py` — sha256
  `d3c3239e78f91659222a6b043920b5095c46e953d67daf8ba26bf7a3038062ce`
  (adapted from the frozen published `explore_z22f17.py`
  `9e8ab707…` (commit `115c0bb9`) by the disclosed textual diff: floor
  17→16, rungs 16→15 with the top rung labeled A9 (PROVISIONAL, small
  token 15), cell s-domain {0}∪{16..47}, tail spots {48..55}, strip
  m∈{16..21} (m=16 NEW open-row sweep; m∈{17..21} proved T-Z22
  compliance recheck), the m=16/15/14/13 row records as cross-artifact
  rechecks, the NEW m=16 base spot with the paper-derived candidate
  disclosed in the docstring BEFORE the first run, the below-band child census at z'-7 (z'=23, floor 16 = z'-7), the
  identity rechecks extended to {0}∪{12..60}, plus the NEW SIXTEENTH-tail
  engine-free pre-computation with BOTH components predeclared).
- `explore_z22f16.out` — sha256
  `4b65f7f07ab49cc4adb90194372397b9418f6f66fe69366211d71bfeaa3393ee`
  (the frozen stdout; deterministic — SIX runs: default ×2,
  PYTHONHASHSEED=1 same-cwd, PYTHONHASHSEED=random same-cwd, env -i
  isolated directories ×2 via /usr/local/bin/python3, all
  byte-identical, rc 0 each, ~30 s per run; no randomness, no
  wall-clock, no hash-order dependence).

## The predeclaration and how it landed (observation, judgment-free)

The docstring of `explore_z22f16.py` contains the COMPLETE predeclared
candidate profile, written before the first run: (i) the s=16 row
derived BY HAND on paper from the PROVED K1337 z=21 floor-16 lemma
values (the C-hand supply), the K1264 stair equality at R=z+min exactly
(the 16→15 B-hand children), the small-token B-child cascade, and the
K0832 closed form; (ii) the {17..31} lattice-identity classes inherited
from the published f17 census; (iii) s-only beyond s=31; (iv) no
multivalue rows. **The measurement hit the predeclared profile
EXACTLY — every class, every value, zero undisclosed classes** — the
SECOND fully-closed pre→measure cycle of the series (after the
f17 census). (The floor-(z−6) series' z16/z18/z19 kits also
published pre-declaration cycles — the z18 kit's (m4) engine-free
revival cascade is the closest precedent, of narrower scope — so the
originally published "first at a sub-critical floor" phrasing is
withdrawn by the same-day repair; what is this kit's own is the
complete cell-ladder profile closure at a sub-critical floor.)

### Floor necessity (the open item answered at cell level)

- The deviant position set at floor 16 is **{16, 18, 20, 22}**: the
  s=16 classes EXCLUDED from the floor-17 domain (the FIFTH
  domain-exclusion event) REvive in-domain at floor 16, exactly as
  predeclared, with the hand-derived values:
  **B22f16 {16: DOWN 0v2}, A22f16 {16: UP 1v0}, A222f16 {16: UP 2v1}**
  — witnesses H(29;(6,16);22)=0 ≠ v(22,22,29)=2,
  H(30;(7,16);22)=1 ≠ v(23,22,30)=0, H(31;(8,16);22)=2 ≠
  v(24,22,31)=1. **The universal floor-16 cell claim FAILS: the
  critical floor 17 = z−5 is NECESSARY for the z=22 cell-ladder
  Sigma-collapse** (within the census domain; the z−6 floor does not
  drop). The paper derivation in the docstring shows WHY only B/A/A2
  deviate: the C-cell's C-hand disturbance (1^C21f16(16)=0 vs the
  single token's 1^2=3) is mex-irrelevant, and the B-small cascade
  from the j=6..8 deviant values stays mex-irrelevant from j=9 on.
- **The even-z A-break extinction fails BELOW the critical floor**:
  A22f16 breaks at an EVEN z, at s=16=z−6 (not the odd-z s=z−5), UP
  1v0 (not UP 2v0) — the THIRD even-z sub-critical A-rank deviant,
  value-exact with the published A16f10 (s=10, UP 1v0) and A18f12
  (s=12, UP 1v0); never the birth form (UP 2v0). The A-rank parity
  law (birth iff z odd, s=z−5, UP 2v0; 3/3 odd,
  5/5 extinct at floor z−5) is a CRITICAL-FLOOR phenomenon and does
  not extend to the z−6 lattice, where the even A-rank revives with
  the uniform value 1 (3/3).
- The s=16 relapse station value trio {DOWN 0v2, UP 1v0, UP 2v1} at
  heads {B, A, A2} carries the even station value trio of the
  published f17 stations {18,20,22} at NEW heads — the THIRD even
  floor-(z−6) station (after the published z=16 s=10 and z=18 s=12
  stations). ACCEPTANCE COMPARISON (same-day, against the published
  z16-f10/z18-f12 kits' frozen outputs): the FULL 11-entry deviant
  lattice is cellwise VALUE-EXACT across z=16/z=18/z=22 with
  s-positions the arithmetic set {z−6, z−4, z−2, z} (11/11 entries
  per kit; C/D/E/F/G ladder included). The registered +2-revival
  candidate (head-trio scope, value-exact 2/2 at the z18 kit's
  publication) is hereby confirmed at z=22 and upgraded to
  FULL-LATTICE scope, value-exact 3/3; z=20 floor-14 is the one
  remaining unswept even floor-(z−6) edition below z=24.
- The {18,20,22} classes are the published f17 classes LATTICE-IDENTICAL
  (s∈{17..31} are single 2-token shapes (j,s), identical points in the
  f17 census): F {22: UP 1v0}, G {20: DOWN 0v2, 22: UP 2v1},
  E {20: UP 1v0}, D {18: DOWN 0v2, 20: UP 2v1}, C {18: UP 1v0},
  B {18: UP 2v1}, A3..A9 collapsed at s>=17. Machine cross-compare of
  the per-cell deviant profiles (f16 restricted to s>=17) against the
  published `explore_z22f17.out` (`f16a87d4…`): EXACT match, 15/15
  cells.
- **s-only SURVIVES the sub-critical floor**: the first 16-token
  multi-shapes (s∈{32..47}) all conform; multivalue rows 0 over all
  1,575 cell shapes (15 cells × 105 shapes). No new deviant class
  beyond {16,18,20,22}.

### Strip, row records, spots

- Strip m∈{16..21} at R=m+23: **169 shapes, 0 violations** — the NEW
  m=16 open-row sweep: 44 shapes 0 violations; the m∈{17..21} T-Z22
  compliance recheck: 125 shapes 0 violations (per-m incrementals
  35/28/23/20/19 = the published f17 cumulative profile exactly).
- m=16-row z=22 record: 40 shapes 0 separations (x0 style) + 39 shapes
  0 separations (arity<=4 co-token ext) — exactly the published f17
  entry, shape-for-shape (machine-checked), still the candidate FIRST
  entry of the future T-Z21 residual band m=16 z∈{22..29}.
- m=15/14/13-row z=22 records: 50/62/76 shapes, 0 separations — the
  published f17 entries reproduced shape-for-shape (machine-checked).
- Strip spots m∈{22..25}: **12/12 match** (lattice identity with the
  published f17 spots).
- **NEW m=16 base spot `H(39;(16,16);22)` = 1, conforming** (=
  v(32,22,39)) — the paper-derived candidate in the docstring hit
  exactly (B-children on the published m=15-row record positions,
  C-child on the PROVED T-Z21 m=16 row at z=21). Never measured by any
  published kit. The m=16 base-spot z-sequence now reads
  z=21: 1 (published), z=22: 1 (here) — two data points, no
  alternation yet.

### Below-band (z'−7 datum)

- `H(23;Y;23)` vs `v(s,23,23)` with min(Y)>=16 (the j=1 cell's B-move
  child; child slice z'=23 with floor 16 = z'−7, TWO below the critical
  z'−5 pattern): **105 shapes, 0 deviants, 0 multivalue** — full
  collapse of the below-band supply child; the FOURTH recorded
  below-band z'−7 empty datum (the z16-f10/z18-f12/z19-f13 kits'
  below-band child sections are empty at z'=17/19/20; here z'=23),
  extending the empty pattern to 4/4 (the published K1264
  stair applicability R=23 <= 23+min(Y) suggests a stair consequence
  at any floor; recorded as observation only).

### Supply identities (engine-free, pure published K0832 closed form)

- THIRTEENTH-tail recheck: v(s,23,23)=v(s,22,23) holds exactly on
  {0}∪{12..21}, 0v2 at s=22, uniformly 2v1 for ALL s∈{23..60}
  (published values reproduced, extended by one).
- FOURTEENTH-tail recheck: v(s,24,24)=v(s,23,24) holds on
  {0}∪{12..23}, uniform 0v1 for ALL s∈{24..60} (extended by one).
- FIFTEENTH-tail recheck: v(s,25,25)=v(s,24,25) holds on
  {0}∪{12..23}, 0v2 at s=24, uniformly 2v1 for ALL s∈{25..60}
  (the f17 kit's predeclared-and-confirmed constants reproduced,
  extended by one).
- **SIXTEENTH-tail identity (NEW)**: v(s,26,26)=v(s,25,26) holds
  exactly on **{0}∪{12..25}**, breaks with **UNIFORM 0v1 for ALL
  s∈{26..60}** — BOTH predeclared components (break start s=26 AND the
  uniform 0v1 shape) CONFIRMED. The odd-z supply-identity form is now
  **4/4** (z=19/z=21/z=23 measured, z=25-supply closed-form
  pre-computation) — the z=25 slice's supply datum, registered for the
  natural next-lane census by the published f17 kit handoff (whichever
  kit published first, the other copy is a recheck; constants identical
  by construction).

## Independent ordered-engine cross-check (outside the frozen artifact)

The FULL census re-enumerated and re-evaluated with `H_ordered` against
the frozen canonical-engine output (`xcheck_z22f16.py`, local, sha256
`8eba4498…`, not part of the frozen artifact): 1,575 cell shapes (15
cells × 105), 120 tail spots, 169 strip shapes, 267 row-record shapes
(40+39+50+62+76), 12 strip spots, the m=16 base spot, 105 below-band
shapes, and ALL 200 identity hold/break rows compared as full rows
(values included): **0 mismatches**; every frozen row reproduced
exactly. rc 0, ~39 s. Per-record `H.cache_clear()` retained.

See `research/log/2026-11-25-z22f16-floor16-predecl-exploration.md`
for the primary-source timeline, the hand-derivation disclosure record
and handoff instructions.

## Same-day repair record (2026-11-25)

An acceptance comparison against the published floor-(z−6) series
kits (frozen outputs of the z16-f10/z18-f12/z19-f13 editions) led to
this repair commit, which changes this README and the companion log
ONLY; the frozen `explore_z22f16.py` / `explore_z22f16.out` /
`engine_block.py` are byte-unchanged and every sha256 pin above still
holds. The originally published revision overstated the kit's
historical novelty on three points, now corrected above:

1. "every published kit of the strip series swept exactly the
   critical floor z−5 / nothing in the published record censuses ANY
   sub-critical (z−6) lattice" — WRONG: the floor-(z−6) series had
   five published editions at kit-build time (z=15 K1321, z=16
   `059c531e`, z=17 `82f98ef4`, z=18 `0bb7e440`, z=19 `5b2275bc`)
   and the even revival head trio was already registered value-exact
   2/2 (z16/z18). This kit is the z=22 edition of that series,
   extending it to 3/3 — and the acceptance comparison adds the new
   full-lattice 11/11 cellwise value-exact finding recorded above.
2. "the FIRST even-z A-rank deviant ever observed" — WRONG:
   A16f10 (s=10) and A18f12 (s=12), both UP 1v0, are published
   precedents; A22f16 is the third (value-exact) instance.
3. "the first sub-critical below-band datum" — WRONG: three z'−7
   below-band child sections were already published empty
   (z'=17/19/20); this kit's z'=23 instance extends it to 4/4.

The docstring of the frozen `explore_z22f16.py` contains the
corresponding historical sentences and is left byte-frozen
(declaration discipline); this section supersedes them. Everything
else — the measurement itself, the s=16 hand derivation, the
deviant witness values, the strip/row/spot/tail records, the
determinism and xcheck results — is unchanged. What remains
genuinely first in this kit: the z=22 floor-16 census itself, the
m=16 strip column 44/0, the m=16 base spot, the sixteenth-tail
identity, and the z'=23 below-band instance.

## Standard caveats

Everything in this kit is a FINITE machine observation against the
pinned raw engine, plus pure closed-form pre-computations for section
(g). Nothing here is a theorem; the floor-necessity observation is a
census-domain witness set, NOT a universal negative (the universal
necessity statement, the s=16 relapse lemma closed forms and the
below-band sub-critical generalization belong to a future declaration
lane if one is opened). No verdict of any game position (11x11 standard
board, two-stone roots, S2, class 1/2/4 — all UNKNOWN) is consumed.
Battery/point counts are engine cross-checks, not proofs.
