# strip-z21-floor15 — z=21 floor-15 (z−6, sub-critical) pre-declaration census kit

EIGHTH edition of the floor-(z−6) series (z=15 K1321, z=16 `059c531e`,
z=17 `82f98ef4`, z=18 `0bb7e440`, z=19 `5b2275bc`, z=20 `2d8cea40`,
z=22 `fb215b76`/`daa9a805`), and the last unswept ODD floor below
z=24. This kit is a FINITE machine census against the pinned raw
engine plus engine-free closed-form pre-computations plus a disclosed
hand derivation written BEFORE the first run. NO K slot is claimed, NO
universal statement is claimed; the declaration lane (a later run)
picks up from here.

## Files

- `explore_z21f15.py` — frozen pre-declaration explorer, sha256
  `f644b43c2f75fe4d57effda2b0ae20137170b1b06cd17e24cb9650d07d58835e`
  (36,791 bytes). Adapted from the published `explore_z21f16.py`
  (z21-min16 census kit) by the disclosed parameter diff (slice
  z 21, floor 16→15, s-domain {0}∪{15..46}, strip m ∈ {15..20} with
  m=15 the NEW open row, the NEW m=15 base spot, below-band z'=22, the
  identity sections 12th..17th + the NEW EIGHTEENTH-tail). The full
  hand derivation of the s=15 head row is frozen in the docstring
  BEFORE the first run (see below).
- `engine_block.py` — byte-clone of the published chain engine
  (sha256 `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`),
  identical to the strip-z20-min15 / strip-z22-floor16 / strip-z20-floor14
  kit bytes; the embedded ENGINE_BLOCK startup pin `bd5f22e4…` is
  asserted by the machinery (engine_gate PASS in the frozen output).
- `explore_z21f15.out` — frozen stdout, sha256
  `6b88288a144beaaa36490ee7dff60e21d0dd1d8c13467c0f128456dd8d770def`
  (38,446 bytes). Determinism: SIX runs all byte-identical (default ×2
  at freeze time + PYTHONHASHSEED=random same-cwd + env -i isolated
  directories ×2 via /usr/local/bin/python3 + first frozen run), rc 0,
  ~26 s per run.

## Registered targets taken by this kit (before the fact)

The published z20-floor14 kit log section 5 (commit `2d8cea40`)
registered, BEFORE this kit ran:

1. "The next floor-(z−6) series datum: z=21 floor-15 (odd, the head
   candidate is EMPTY per the odd-edition pattern 3/3 published)".
2. "the EIGHTEENTH-tail (k=27, odd form, v(s,28,28)=? v(s,27,28)) is
   the natural next pre-computation (z=27 supply; odd form candidate
   5/5 extension confirmed shape: hold {0} U {12..27}? — recorded by
   whoever runs it; both components derivable from the current data
   as before)".

Both are executed here. Slot check at kit-build time: no
`strip-z21-floor15*` / `strip-z21-min15*` experiment directory, census,
log or item exists on main (path probes; `z21f15` /
`filename:explore_z21` searches return only the critical-lattice
z21-min16 kit).

## Headline results (all finite observations, no universal claim)

1. **The registered EMPTY ODD HEAD prediction hit EXACTLY**: the
   s=15 row (15 rungs, single shape (j,15)) is fully conforming —
   zero deviant classes at s=z−6 — extending the published
   odd-edition head-empty pattern (z=15 K1321, z=17 `82f98ef4`,
   z=19 `5b2275bc`) to its candidate **4/4**, the mirror of the even
   head trio registered value-exact 4/4 (z in {16,18,20,22}).
2. **The critical-lattice profile is preserved cellwise EXACT** by
   the floor drop 16→15: deviant classes = the published
   F21f16..A921f16 profile (F {20: DOWN 1v2, 21: HOLE, 22..46:
   UP 2v0 persistent tail}, G {20: DOWN 0v1}, E {18: DOWN 1v2, 20:
   UP 2v0}, D {18: DOWN 0v1}, C {16: DOWN 1v2, 18: UP 2v0},
   B {16: DOWN 0v1}, A {16: UP 2v0 = the A RANK BREAK REBIRTH class
   birth s=z−5, SURVIVING the floor drop}, A2..A9 collapsed) —
   machine continuity compare vs the published frozen
   `explore_z21f16.out`: deviant sets, 120 tail-spot rows and 12
   strip-spot rows ALL IDENTICAL (0 diffs).
3. **The BLIND sub-floor block s ∈ {30..46}** (15-token components
   enter at s=30): NO multivalue rows, NO new deviant classes —
   1,856 census points, 116 shapes per cell, 0 multivalue anywhere;
   ordered-engine crosscheck 1,856 points 0 mismatches (local,
   unpublished machine).
4. **Strip m ∈ {15..20} at R=m+22**: 0 violations; the m ∈ {16..20}
   T-Z21 compliance increments 44/35/28/23/20 reproduce the
   published f16 cumulatives EXACT; **m=15 is the NEW open-row
   co-token sweep: 55 shapes 0 violations** (never measured by any
   published kit).
5. **Row records at z=21 (x0 published residual-band style)**:
   m=15-row 50/0 + arity≤4 ext 49/0 (recheck of the published
   z21-min16 record, FIRST entry of the K1335-published T-Z20
   residual band m=15 z ∈ {21..28}), m=14-row 62/0, m=13-row 76/0,
   m=12-row 92/0 — all shape-for-shape with the published entries.
6. **NEW m=15 base spot H(37;(15,15);21) = 0 = v(30,21,37)
   CONFORMING** (paper-derived candidate hit exactly; the first
   option-set-only derivation of the z=21 slice's m=15-row base
   point; previously only the z=20 value 0 was published). The
   m=15 base-spot z-sequence: z=20: 0, z=21: 0 — no alternation
   yet; the z=22 datum belongs to a future lane.
7. **Below-band z'=22 (floor 15 = z'−7): SIXTH consecutive z'−7
   empty datum** — 116 shapes, 0 deviants, 0 multivalue rows
   (K1264 stair-consequence candidate; PROVED-lemma instance,
   machine corroboration).
8. **EIGHTEENTH-tail supply identity (NEW pre-computation, pure
   K0832 closed form, engine-free)**: v(s,28,28)=v(s,27,28) holds
   exactly on **{0}∪{12..27}**, breaks **0v1 at s=28**, then
   **UNIFORM 0v1 for ALL s ∈ {28..62}** — BOTH predeclared
   components CONFIRMED. The odd-z supply-identity form graduates
   to its candidate **5/5** (k=19/21/23/25 published + k=27 here);
   this is the z=27 slice's supply datum, precomputed for the
   future z=27 declaration lane. The 12th..17th-tail identities were
   rechecked over the extended domain {0}∪{12..62} with all
   published constants reproduced (hold endpoints and uniform break
   shapes as registered).

## Honest record

- The hand derivations (s=15 head row value derivation per rung,
  m=15 base spot) were written in-session from published PROVED
  facts only (K1335/T-Z20 proved z=20 floor-15 ladder row at s=15,
  K1264 stair equality, K0832 closed form, published z21-min16
  m=14-row observational record), and the child-position INPUT
  LITERALS were cross-checked against a drafting scratch engine
  evaluation BEFORE the freeze (K1344-D6 discipline: derivation →
  engine cross-check of input literals → freeze). The scratch
  machine is NOT published and evaluated none of the declared
  outcome values.
- The BLIND pre-declarations (head-row outcome values, blind block
  {30..46}, multivalue census, strip/row/base-spot/below-band
  measurements, all measured counts, the 18th-tail constants as
  closed-form precomputation) hit with zero surprises, and the
  architectural prediction itself was registered BEFORE the fact by
  the published z20-floor14 kit's log §5.
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
