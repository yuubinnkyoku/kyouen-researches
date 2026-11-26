# strip-z24-floor18 — z=24 floor-18 (z−6, sub-critical) pre-declaration census kit

TENTH edition of the floor-(z−6) series (z=15 K1321, z=16 `059c531e`,
z=17 `82f98ef4`, z=18 `0bb7e440`, z=19 `5b2275bc`, z=20 `2d8cea40`,
z=21 `5b01e14c`, z=22 `fb215b76`/`daa9a805`, z=23 `9577fadc`), and
the FIFTH EVEN edition of the registered head-trio / 11-entry
lattice prediction. This kit is a FINITE machine census against the
pinned raw engine plus engine-free closed-form pre-computations plus
a disclosed hand derivation written BEFORE the first run. NO K slot
is claimed, NO universal statement is claimed; the declaration lane
(a later run, e.g. a future T-Z24) picks up from here.

Counter-probe (required before claiming, per the registered
handoffs): NO T-Z24 declaration exists on main at kit-build time;
no z24-min19 census kit exists (`filename:explore_z24` returns
nothing). This kit is therefore a pure pre-declaration exploration
of the unsurveyed z=24 lattice — the natural pre-cursor of the
future T-Z24 lane, in the exact role the published z23-min18 kit
played for K1344.

## Files

- `explore_z24f18.py` — frozen pre-declaration explorer, sha256
  `891debacc49c7d74560076a155ce1ad8b1ec55eefe6e30944761241329c759f1`
  (37,589 bytes). Adapted from the published `explore_z23f17.py`
  (z23-floor17 census kit, commit `9577fadc`) by the disclosed
  parameter diff (slice z 23→24, floor 17→18, cell s-domain
  {0}∪{18..49}, rungs j=1..17 with the j=18 non-derivability
  disclosed, strip m ∈ {18..23} — ALL segments NEW (no T-Z24), the
  NEW m=18 base spot with its single disclosed observational
  dependency, below-band z'=25, identity sections 15th..20th
  rechecks + the NEW TWENTY-FIRST-tail over the extended domain
  {0}∪{12..64}). The full hand derivation of the s=18 head row
  (17 points, including the registered even head trio) is frozen in
  the docstring BEFORE the first run (see below).
- `engine_block.py` — byte-clone of the published chain engine
  (sha256 `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`),
  identical to the strip-z20-min15 / z22-floor16 / z20-floor14 /
  z21-floor15 / z23-floor17 kit bytes; the embedded ENGINE_BLOCK
  startup pin `bd5f22e4…` is asserted by the machinery (engine_gate
  PASS in the frozen output).
- `explore_z24f18.out` — frozen stdout, sha256
  `bdda90701726fd196b817017151ad7889438f74fbf5e819f60af3ede979c364c`
  (39,540 bytes). Determinism: SIX runs all byte-identical (first
  frozen run + default ×2 at freeze time + PYTHONHASHSEED=random
  same-cwd + env -i isolated directories ×2 via
  /usr/local/bin/python3), rc 0, ~31 s per run.

## Registered targets taken by this kit (before the fact)

The published z21-floor15 kit log §5 (commit `5b01e14c`) and the
z23-floor17 kit log §5 (commit `9577fadc`) registered, BEFORE this
kit ran:

1. "z=24 floor-18 (even, the registered 11-entry lattice prediction
   at positions {18,20,22,24} — the lane that owns z ≥ 24;
   counter-probe of the parallel T-Z24 target before claiming)".
2. "The TWENTY-FIRST-tail (k=30, even form, v(s,31,31) vs
   v(s,30,31)) is the natural next pre-computation (z=30 supply;
   even-form candidate: hold {0} U {12..29}, 0v2@30, UNIFORM 2v1
   s ≥ 31)".

Both are executed here. The head derivation is the FIRST of the
series with NO observational dependency (all 17 C-hand children are
PROVED T-Z23/K1344 constants — the z=23 lattice is fully proved).

## Headline results (all finite observations, no universal claim)

1. **The registered EVEN HEAD TRIO prediction hit VALUE-EXACT**: at
   s=18 the measured deviants are exactly {B(j=6) DOWN 0v2,
   A(j=7) UP 1v0, A2(j=8) UP 2v1} with all 14 other rungs
   conforming exactly as hand-derived (17-point derivation,
   disclosed per-rung before the first run). The even head trio
   chain (z=16 `059c531e`, z=18 `0bb7e440`, z=20 `2d8cea40`,
   z=22 `fb215b76`) reaches its candidate **5/5**, the mirror of
   the odd head-empty rule 5/5 (z=15/17/19/21/23). The
   option-set-exotic A-cell {2, 0, 1^2=3} → mex 1 (UP 1v0) was
   predeclared from the PROVED T-Z23 class constants.
2. **The registered 11-ENTRY EVEN LATTICE hit VALUE-EXACT at the
   read positions {20,22,24}** (blind candidates, scaled +2 from
   the measured value-exact even chain): s=20 {C UP 1v0, B UP 2v1,
   D DOWN 0v2}, s=22 {E UP 1v0, D UP 2v1, G DOWN 0v2}, s=24 {F UP
   1v0, G UP 2v1} — and NO other deviant row in {19..35}; the even
   full-lattice value-exact chain reaches **5/5** (z=16/18/20/22
   + z=24 here). Machine cross-slice compare vs the published
   frozen `explore_z22f16.out` under the +2 s-shift: 15/15 cells
   IDENTICAL (0 diffs) — the z=24 lattice is structurally the
   z=22 lattice shifted by two, at every shared rung.
3. **The BLIND sub-floor block s ∈ {36..49}** (18-token components
   enter at s=36): NO multivalue rows, NO deviant rows at all —
   89 shapes per cell, 1,513 census points, 0 multivalue anywhere;
   ordered-engine crosscheck 1,602 points 0 mismatches (local,
   unpublished machine).
4. **Strip m ∈ {18..23} at R=m+25 (ALL NEW; no T-Z24 exists)**: 125
   cumulative shapes, **0 violations** — the m ∈ {19..23} segments
   are the would-be T-Z24 claim positions, measured clean for the
   first time; the m=18 head-floor segment measured 28 shapes 0
   violations. The m ∈ {18..22} cumulative counts reproduce the
   published z23 strip enumeration values (28/51/71/90/108 —
   identical enumerations) and the NEW m=23 segment adds 17 more.
5. **Row records at z=24 (x0 published residual-band style), SIX
   new all-0-separation entries**: m=18-row (R=43) **26/0 + arity≤4
   ext 25/0 — the FIRST-EVER z=24 m=18 row record** (in-band,
   z*(18)=34; the frontier target of the future T-Z24 lane);
   m=17-row (R=42) 32/0 (future T-Z22 residual band z=24 entry,
   same count as the published z=23 entry); m=16-row (R=41) 40/0;
   m=15-row (R=40) 50/0 (K1335 T-Z20 band z=24 entry); m=14-row
   (R=39) 62/0 (K1330 band); m=13-row (R=38) 76/0 (K1328 band
   z=24 entry — z*(13)=25 > 24 by one point, the
   closest-to-frontier row record of any published kit).
6. **Tail spots s ∈ {50..57}: 136/136 MATCH** — the EVEN-edition
   tail signature confirmed at its second even edition (z=22: the
   published f16 kit was 120/120 match; the odd editions' F 8/8
   mismatch signature does not appear at even z).
7. **NEW m=18 base spot H(43;(18,18);24) = 1 = v(36,24,43)
   CONFORMING** (paper-derived candidate hit exactly; B-children
   premised on the z=24 m=17-row entry conforming — the single
   observational dependency, MEASURED CONFORMING (32/0) by this
   kit's own (d2) section; C-child on the PROVED T-Z23 base m=18).
   The m=18 base-spot z-sequence extends to z=24 with value 1
   (z=16..24: 0,1,0,1,0,1,0,1,1 — the alternation breaks its
   pattern at the first even-z edition measured at the m=18 row).
8. **Below-band z'=25 (floor 18 = z'−7): EIGHTH consecutive z'−7
   empty datum** — 89 shapes, 0 deviants, 0 multivalue rows (K1264
   stair-consequence candidate; PROVED-lemma instance, machine
   corroboration).
9. **TWENTY-FIRST-tail supply identity (NEW pre-computation, pure
   K0832 closed form, engine-free)**: v(s,31,31)=v(s,30,31) holds
   exactly on **{0}∪{12..29}**, breaks **0v2 at s=30**, then
   **UNIFORM 2v1 for ALL s ∈ {31..64}** — BOTH predeclared
   components CONFIRMED. The even-z supply-identity form graduates
   to its candidate **6/6** (k=20/22/24/26/28 published + k=30
   here); the z=30 slice's supply datum, precomputed for the future
   z=30 declaration lane. The 15th..20th-tail identities were
   rechecked over the extended domain {0}∪{12..64} with all
   published constants reproduced.

## Honest record

- The hand derivations (s=18 head row value derivation per rung
  j=1..17, m=18 base spot) were written in-session from published
  PROVED facts only (the PROVED T-Z23/K1344 z=23 floor-18 ladder
  row constants at s=18 — including the three PROVED class values
  C DOWN 1v2 ⇒ 1, B DOWN 0v1 ⇒ 0, A UP 2v0 ⇒ 2 — the K1264 stair
  equality, the K0832 closed form), and the child-position INPUT
  LITERALS were cross-checked against a drafting scratch engine
  evaluation BEFORE the freeze (K1344-D6 discipline: derivation →
  engine cross-check of input literals → freeze; c_j 17/17 vs the
  published frozen z23f18 row, b_j stairs 17/17, removal, d_j
  collapses, base-spot inputs, 21st-tail constants — FAILS: NONE).
  The scratch machine is NOT published and evaluated none of the
  declared outcome values. The head derivation carries NO
  observational dependency (a first for the series); the base-spot
  derivation carries its single disclosed observational dependency
  (premise measured conforming by this kit's own record section).
- The BLIND pre-declarations (head-row outcome values, the
  11-entry lattice read at {20,22,24}, blind block {36..49},
  multivalue census, strip/row/base-spot/below-band measurements,
  all measured counts, the 21st-tail constants as closed-form
  precomputation) hit with zero surprises, and the architectural
  prediction itself was registered BEFORE the fact by the published
  z21-floor15 and z23-floor17 kits' §5.
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
