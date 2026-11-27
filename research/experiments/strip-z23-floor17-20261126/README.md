# strip-z23-floor17 — z=23 floor-17 (z−6, sub-critical) pre-declaration census kit

NINTH edition of the floor-(z−6) series (z=15 K1321, z=16 `059c531e`,
z=17 `82f98ef4`, z=18 `0bb7e440`, z=19 `5b2275bc`, z=20 `2d8cea40`,
z=21 `5b01e14c`, z=22 `fb215b76`/`daa9a805`), and the fifth ODD
edition of the head-empty pattern. This kit is a FINITE machine census
against the pinned raw engine plus engine-free closed-form
pre-computations plus a disclosed hand derivation written BEFORE the
first run. NO K slot is claimed, NO universal statement is claimed;
the declaration lane (a later run) picks up from here.

## Files

- `explore_z23f17.py` — frozen pre-declaration explorer, sha256
  `fa75fc51d2bb157be43d265eae8e2cfde9b2cc2368e11edef093d930b2fb4c96`
  (39,025 bytes). Adapted from the published `explore_z21f15.py`
  (z21-floor15 census kit, commit `5b01e14c`) by the disclosed
  parameter diff (slice z 21→23, floor 15→17, s-domain
  {0}∪{17..48}, rungs j=1..17 with the j=18 non-derivability
  disclosed, strip m ∈ {17..22} with m=17 the NEW open row, the NEW
  m=17 base spot, below-band z'=24, the identity sections
  14th..18th-recheck + the NEW NINETEENTH-tail and NEW TWENTIETH-tail
  over the extended domain {0}∪{12..63}). The full hand derivation of
  the s=17 head row (17 points) is frozen in the docstring BEFORE the
  first run (see below).
- `engine_block.py` — byte-clone of the published chain engine
  (sha256 `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`),
  identical to the strip-z20-min15 / strip-z22-floor16 /
  strip-z20-floor14 / strip-z21-floor15 kit bytes; the embedded
  ENGINE_BLOCK startup pin `bd5f22e4…` is asserted by the machinery
  (engine_gate PASS in the frozen output).
- `explore_z23f17.out` — frozen stdout, sha256
  `e77043cc8a676780b8f829b97c5e7e84116a473176f09d40e4b678628fb8c45c`
  (41,024 bytes). Determinism: SIX runs all byte-identical (first
  frozen run + default ×2 at freeze time + PYTHONHASHSEED=random
  same-cwd + env -i isolated directories ×2 via
  /usr/local/bin/python3), rc 0, ~31 s per run.

## Registered targets taken by this kit (before the fact)

The published z21-floor15 kit log section 5 (commit `5b01e14c`,
2026-11-26) registered, BEFORE this kit ran:

1. "Next floor-(z−6) series data points: **z=23 floor-17 (odd, the
   head-empty 5/5 candidate + preservation of the published
   T-Z23/K1344 critical lattice)**".
2. "The **NINETEENTH-tail (k=28, even form, v(s,29,29) vs
   v(s,28,29))** is the natural next pre-computation (z=28 supply;
   even-form candidate: hold {0} U {12..27}, 0v2@28, UNIFORM 2v1
   s >= 29; both components derivable from the current closed-form
   data)".

Both are executed here, plus the TWENTIETH-tail (k=29, odd form) as
the natural next of the same family. Slot check at kit-build time:
no `strip-z23-floor17*` experiment directory, census, log or item
exists on main (path probes; `z23f17` / `strip-z23-floor17` searches
return only the critical-lattice z23-min18 kit; `filename:explore_z23`
returns only the f18 kit).

## Headline results (all finite observations, no universal claim)

1. **The registered EMPTY ODD HEAD prediction hit EXACTLY**: the
   s=17 row (17 rungs — one rank FURTHER than any previous edition,
   the j=17 C-hand child being covered by the PROVED T-Z22 m=17-row
   base — single shape (j,17)) is fully conforming — zero deviant
   classes at s=z−6 — extending the published odd-edition head-empty
   pattern (z=15 K1321, z=17 `82f98ef4`, z=19 `5b2275bc`, z=21
   `5b01e14c`) to its candidate **5/5**, the mirror of the even head
   trio registered value-exact 4/4 (z in {16,18,20,22}). The single
   observational dependency of the derivation (j=17: the published
   z=23 m=16-row record value v(33,23,40)=1) is disclosed.
2. **The critical-lattice profile is preserved cellwise EXACT** by
   the floor drop 18→17: deviant classes = the published
   F23f18..A1123f18 profile (F {22: DOWN 1v2, 23: HOLE (conforming),
   24..48: UP 2v0 persistent tail}, G {22: DOWN 0v1}, E {20: DOWN
   1v2, 22: UP 2v0}, D {20: DOWN 0v1}, C {18: DOWN 1v2, 20: UP
   2v0}, B {18: DOWN 0v1}, A {18: UP 2v0 = the A RANK BREAK REBIRTH
   class birth s=z−5, SURVIVING the floor drop — the
   definition-domain-exclusion NON-event 4th consecutive},
   A2..A11 collapsed) — machine continuity compare vs the published
   frozen `explore_z23f18.out`: shared-block deviant sets ({18..33}),
   136 tail-spot rows and 12 strip-spot rows ALL IDENTICAL (0
   diffs).
3. **The BLIND sub-floor block s ∈ {34..48}** (17-token components
   enter at s=34): NO multivalue rows, NO new deviant classes —
   the F UP 2v0 tail passes through the block uniformly — 1,649
   census points, 97 shapes per cell, 0 multivalue anywhere;
   ordered-engine crosscheck 17×97+97 points 0 mismatches (local,
   unpublished machine).
4. **Strip m ∈ {17..22} at R=m+24**: 0 violations; the m ∈ {18..22}
   T-Z23 compliance increments 28/23/20/19/18 reproduce the
   published f18 cumulatives (28/51/71/90/108) EXACT;
   **m=17 is the NEW open-row co-token sweep: 35 shapes 0
   violations** (never measured by any published kit; z*(17)=33 > 23,
   in-band by the K1268 formula).
5. **Row records at z=23 (x0 published residual-band style)**:
   m=17-row 32/0 + arity≤4 ext 31/0 (recheck of the published
   z23-min18 record, CANDIDATE first entry of the future T-Z22
   declaration residual band m=17 z ∈ {23..32}), m=16-row 40/0,
   m=15-row 50/0 (K1335 T-Z20 residual band m=15 z ∈ {21..28}),
   m=14-row 62/0 (K1330 band m=14 z ∈ {20..25}), m=13-row 76/0
   (K1328 band m=13 z ∈ {19..24}, sixth consecutive 76/0) — all
   shape-for-shape with the published entries.
6. **NEW m=17 base spot H(41;(17,17);23) = 0 = v(34,23,41)
   CONFORMING** (paper-derived candidate hit exactly; B-children on
   the published z=23 m=16-row observational record, C-child on the
   PROVED T-Z22 m=17-row claim; option set {1,1} → mex 0). The m=17
   base-spot z-sequence: z=22: 0 (published z22-min17 kit), z=23: 0
   (here) — no alternation yet; the z=24 datum belongs to the z=24
   lane.
7. **Below-band z'=24 (floor 17 = z'−7): SEVENTH consecutive z'−7
   empty datum** — 97 shapes, 0 deviants, 0 multivalue rows (K1264
   stair-consequence candidate; PROVED-lemma instance, machine
   corroboration).
8. **NINETEENTH-tail supply identity (NEW pre-computation, pure
   K0832 closed form, engine-free)**: v(s,29,29)=v(s,28,29) holds
   exactly on **{0}∪{12..27}**, breaks **0v2 at s=28**, then
   **UNIFORM 2v1 for ALL s ∈ {29..63}** — BOTH predeclared
   components CONFIRMED. The even-z supply-identity form graduates
   to its candidate **5/5** (k=20/22/24/26 published + k=28 here);
   this is the z=28 slice's supply datum, precomputed for the
   future z=28 declaration lane.
9. **TWENTIETH-tail supply identity (NEW pre-computation)**:
   v(s,30,30)=v(s,29,30) holds exactly on **{0}∪{12..29}**, breaks
   UNIFORM **0v1 from s=30** for ALL s ∈ {30..63} — BOTH predeclared
   components CONFIRMED; the odd-z supply-identity form extends to
   its candidate **6/6** (k=19/21/23/25/27 published + k=29 here);
   the z=29 slice's supply datum for the future z=29 declaration
   lane. The 14th..18th-tail identities were rechecked over the
   extended domain {0}∪{12..63} with all published constants
   reproduced (hold endpoints and uniform break shapes as
   registered, 18th extended by one point from its z21-f15
   publication).

## Honest record

- The hand derivations (s=17 head row value derivation per rung
  j=1..17, m=17 base spot) were written in-session from published
  PROVED facts only (K1339/T-Z22 proved z=22 floor-17 ladder row at
  s=17, K1264 stair equality, K0832 closed form, published z23-min18
  m=16-row observational record), and the child-position INPUT
  LITERALS were cross-checked against a drafting scratch engine
  evaluation BEFORE the freeze (K1344-D6 discipline: derivation →
  engine cross-check of input literals → freeze). The scratch
  machine is NOT published and evaluated none of the declared
  outcome values.
- The BLIND pre-declarations (head-row outcome values, blind block
  {34..48}, multivalue census, strip/row/base-spot/below-band
  measurements, all measured counts, the 19th/20th-tail constants as
  closed-form precomputations) hit with zero surprises, and the
  architectural prediction itself was registered BEFORE the fact by
  the published z21-floor15 kit's log §5 (commit `5b01e14c`).
- No file was edited after any run; the frozen stdout is the
  published artifact.
- No wall-clock, no randomness, no hash-order dependence.

## Standard caveats

Everything here is FINITE machine observation against the pinned raw
engine, plus pure closed-form pre-computations, plus disclosed hand
derivations whose candidate status is stated per section. Nothing
here is a theorem; no universal statement is claimed. Standard 11×11
empty board, two-stone roots, S2, class 1/2/4 and all central-reply
roots: all UNKNOWN, unchanged; no verdict consumed.
