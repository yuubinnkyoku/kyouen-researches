# 2026-11-26 z=23 floor-17 (z−6, sub-critical) pre-declaration census kit — exploration log

Lane: high-speed lane (this run, continuation of the same-day
session that published the z=21 floor-15 kit `5b01e14c`). Status of
this document: PRIMARY RECORD of the pre-declaration census kit
`research/experiments/strip-z23-floor17-20261126/`. No K slot is
claimed, no universal statement is claimed. Everything below is
finite machine observation against the pinned raw engine, plus
engine-free closed-form pre-computations, plus disclosed hand
derivations written BEFORE the first run of the frozen file. The
declaration lane (a later run) picks up from here.

## 1. Context, prior-lane state and slot check

Latest main at this run's start: `5b01e14c` (the z=21 floor-15
pre-declaration census kit + log, 2026-11-26T01:59:00Z, fetch-back
verified 5/5 byte-identical in this session). AGENTS.md and the
knowledge README conventions followed (no branch/PR, main direct,
publish-then-verify). No unresolved-item list contradicts this
lane; no strip-series commit landed since `5b01e14c`.

The registered targets for the high-speed lane at this point were
the published z21-floor15 kit log §5 handoffs (commit `5b01e14c`):
(a) **z=23 floor-17 (odd, the head-empty 5/5 candidate + preservation
of the published T-Z23/K1344 critical lattice)** — taken here;
(b) **the NINETEENTH-tail (k=28, even form) pre-computation** —
bundled here; plus (c) the TWENTIETH-tail (k=29, odd form) as the
natural next of the same family. The z=24 floor-18 lattice prediction
was left to the lane that owns z ≥ 24.

Slot check at kit-build time: no `strip-z23-floor17*` /
`strip-z23-min17*` experiment directory and no z=23 floor-17 census,
log or item exists on main (`z23f17` / `strip-z23-floor17` /
`filename:explore_z23` searches return only the critical z23-min18
kit; `nineteenth`/`twentieth` searches return no supply-identity
kit). The consumed published bytes (`explore_z23f18.py`-family
frozen .out, `explore_z21f15.py` template, `engine_block.py`) were
fetch-verified byte-identical against main before use (engine
`582c93c1…` byte-clone asserted by the startup pin `bd5f22e4…`).

## 2. Kit construction (publish-then-execute, frozen before publication)

- `engine_block.py` — byte-clone of the published chain engine
  (sha256 `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`),
  identical to the strip-z20-min15 / strip-z22-floor16 /
  strip-z20-floor14 / strip-z21-floor15 kit bytes.
- `explore_z23f17.py` (sha256
  `fa75fc51d2bb157be43d265eae8e2cfde9b2cc2368e11edef093d930b2fb4c96`,
  39,025 bytes) — adapted from the published frozen
  `explore_z21f15.py` (z21-floor15 census kit, commit `5b01e14c`) by
  the disclosed parameter diff (slice z 21→23, floor 15→17, cell
  s-domain {0}∪{17..48}, rungs j=1..17 with the j=18
  non-derivability disclosed, strip m ∈ {17..22} with m=17 the NEW
  open row, the NEW m=17 base spot, below-band z'=24, identity
  sections 14th..18th rechecks over the extended domain
  {0}∪{12..63} + the NEW NINETEENTH-tail and TWENTIETH-tail
  pre-computations with BOTH components predeclared each).
- THE HAND DERIVATION of the complete s=17 head row (17 points, one
  rank further than any previous edition) and of the m=17 base spot
  was written BEFORE the first run, disclosed in the file docstring:
  every option set computable from four published inputs —
  (1) the C-hand child of Cell_j(17) is exactly the published PROVED
  z=22 floor-17 ladder position H(j+23;{j,17};22) (K1339/T-Z22 cell
  constants; the whole published z=22 ladder row at s=17 conforms;
  j=17 is the PROVED T-Z22 m=17-row base position
  H(40;(17,17);22)=v(34,22,40)=0); (2) the K1264 stair equality
  covers every 17→16 B-hand child (j,16) at R=j+23 EXACTLY for
  j ≤ 16 (min=j); (3) the small-token child is the in-kit cascade
  Cell_{j−1}(17), with the j=1 removal child the stair position
  H(24;(17,);24)=v(17,24,24)=1; (4) the sole NON-proved input,
  disclosed: both j=17 B-hand children land on (40;(16,17);23) =
  the published z=23 m=16-row OBSERVATIONAL record position
  (z23-min18 census kit: 40 shapes 0 separations) =>
  H(40;(16,17);23)=v(33,23,40)=1 — a single observational dependency
  for the whole s=17 row (mirroring the published z20-f14 / z21-f15
  kits' own single-observational-dependency pattern at their top
  rungs). The derivation walks: b_j = j%2 alternation (stairs),
  c_j = (j+1)%2 alternation (T-Z22 ladder row), d_j = (j+1)%2
  (collapses); j=1 {1,1,1}→0; j even {0,0,0}→1, j odd {1,1,1}→0
  through j=16; j=17 {1 (record), 1^0=1 (T-Z22)}→0. All 17 rungs
  conform. The input literals were cross-checked against a drafting
  scratch engine evaluation BEFORE the freeze (K1344-D6 discipline:
  C-children 17/17, B-stairs 16/16, j=17 record dependency,
  removal stair, base-spot B/C children, published z22-f17 row
  empty-at-s=17 — FAILS: NONE); the declared OUTCOME values were NOT
  engine-checked before the freeze.
  The m=17 base-spot derivation (disclosed before the first run):
  B-children → H(40;(16,17);23) = 1 (observational record),
  C-child → 1^H(40;(17,17);22) = 1^v(34,22,40) = 1 (PROVED T-Z22)
  → options {1,1} → mex 0 = collapse v(34,23,41)=0, CONFORMING
  candidate. The 19th/20th-tail constants were hand-derived from
  the K0832 closed form (engine-free) with BOTH components
  predeclared.
- Determinism: SIX runs (first frozen run + default ×2,
  PYTHONHASHSEED=random same cwd, env -i isolated directories ×2
  via /usr/local/bin/python3) all byte-identical, rc 0, ~31 s per
  run; frozen stdout `explore_z23f17.out` sha256
  `e77043cc8a676780b8f829b97c5e7e84116a473176f09d40e4b678628fb8c45c`
  (41,024 bytes).
- Local continuity checks (unpublished machines, series convention):
  ordered-engine crosscheck of 17×97 census + below-band
  (1,746 points): 0 mismatches; machine compare vs the published
  frozen `explore_z23f18.out`: shared-block deviant sets {18..33}
  17/17 cells EXACT, 136 tail-spot rows identical, 12 strip-spot
  rows identical, strip increments 28/23/20/19/18 with cumulatives
  minus the m=17 segment = the published 28/51/71/90/108 EXACT,
  five row records shape-for-shape (32/40/50/62/76, all 0 seps).

## 3. Results

### 3.1 Cell census (section a) — the registered prediction hit EXACTLY

- **THE s=17 ROW (NEW): the registered §5 EMPTY ODD HEAD
  CONFIRMED** — zero deviant classes at s=17, the whole row
  conforming with the hand-derived per-rung values (the derived
  alternation identical to the collapse sequence at every rung);
  single shape (j,17) at every j; 0 multivalue at s=17. The
  odd-edition head-empty pattern (z=15 K1321, z=17 `82f98ef4`, z=19
  `5b2275bc`, z=21 `5b01e14c`) reaches its candidate **5/5**, the
  mirror of the even head trio {B DOWN 0v2, A UP 1v0, A2 UP 2v1}
  registered value-exact 4/4 at z ∈ {16,18,20,22}.
- **s ∈ {18..33}: lattice identity with the published f18 census
  EXACT** (no 17-token component fits below s=34): deviant rows
  equal the published f18 profile — F {22: DOWN 1v2, 23: HOLE
  (conforming), 24..48: UP 2v0 tail}, G {22: DOWN 0v1}, E {20:
  DOWN 1v2, 22: UP 2v0}, D {20: DOWN 0v1}, C {18: DOWN 1v2, 20:
  UP 2v0}, B {18: DOWN 0v1}, A {18: UP 2v0} (the A RANK BREAK
  REBIRTH class, birth s=z−5=18, SURVIVES the floor drop 18→17 —
  the definition-domain-exclusion NON-event 4th consecutive),
  A2..A11 collapsed; machine cross-compare vs the published frozen
  `explore_z23f18.out` deviant sets 17/17 cells EXACT.
- **s ∈ {34..48} (BLIND sub-floor block; 17-token components enter
  at s=34): NO multivalue rows, NO new deviant classes** — 97
  shapes per cell, 1,649 census points total, 0 multivalue
  anywhere; the F persistent tail UP 2v0 passes through the block
  uniformly.
- Tail spots s ∈ {49..56}: F 8/8 mismatch, all other cells match —
  row-for-row identical to the published f18 tail spots
  (machine-verified 136/136).
- Local (unpublished) ordered-engine crosscheck of all 1,649
  census + below-band points: 0 mismatches with the frozen
  canonical values.

### 3.2 Strip and row records (sections b,c,d,e)

- Strip m ∈ {17..22} at R=m+24: **143 shapes, 0 violations**; the
  NEW m=17 open-row co-token sweep **35 shapes 0 violations** (a
  NEW datum: never measured by any published kit; in-band,
  z*(17)=33 > 23); the m ∈ {18..22} T-Z23 compliance recheck
  incrementals **28/23/20/19/18 = the published f18 cumulative
  profile EXACT** (cumulatives 63/86/106/125/143 minus the m=17
  segment reproduce 28/51/71/90/108, machine cross-check clean).
- m=17-row z=23 (R=41): **32 shapes 0 separations (x0 style) +
  31/0 (arity≤4 co-token ext)** — recheck of the published
  z23-min18 record shape-for-shape; CANDIDATE first entry of the
  future T-Z22 declaration residual band m=17 z ∈ {23..32}
  (frontier z*(17)=33) reconfirmed.
- m=16-row z=23 (R=40): **40/0**; m=15-row z=23 (R=39): **50/0**;
  m=14-row z=23 (R=38): **62/0**; m=13-row z=23 (R=37): **76/0**
  — all cross-artifact rechecks shape-for-shape with the published
  z23-min18 entries (future T-Z21 m=16 band / K1335 m=15 band /
  K1330 m=14 band / K1328 m=13 band sixth-consecutive contexts).
- Strip spots m ∈ {23..26} at R=m+24: **12/12 match** (row-for-row
  identity with the published f18 spots).
- **NEW m=17 base spot H(41;(17,17);23) = 0 = v(34,23,41)
  CONFORMING** (the paper-derived candidate hit exactly; derivation
  disclosed before the first run). The m=17 base-spot z-sequence:
  z=22: 0 (published z22-min17), z=23: 0 (here) — no alternation
  yet; the z=24 datum belongs to the z=24 lane.

### 3.3 Below-band (z'−7 datum, section f)

H(24;Y;24) vs v(s,24,24), min(Y) ≥ 17 (z'=24, floor 17 = z'−7):
**97 shapes, 0 deviants, 0 multivalue rows** — the SEVENTH
consecutive z'−7 empty datum (published: z'=17/19/20/21/22/23),
extending the pattern to 7/7. K1264 stair applicability
R=24 ≤ 24+min(Y) makes this an instance of a PROVED lemma (machine
corroboration; the generalization statement belongs to a declaration
lane).

### 3.4 Supply identities (engine-free, section g; pure K0832)

Over the EXTENDED domain {0}∪{12..63} (each published {12..62}
domain extended by one):

- FOURTEENTH-tail recheck (this slice's own F supply): hold
  {0}∪{12..23}, UNIFORM 0v1 s ∈ {24..63}.
- FIFTEENTH-tail recheck: hold {0}∪{12..23}, 0v2@24, UNIFORM 2v1
  s ∈ {25..63}.
- SIXTEENTH-tail recheck: hold {0}∪{12..25}, UNIFORM 0v1
  s ∈ {26..63}.
- SEVENTEENTH-tail recheck: hold {0}∪{12..25}, 0v2@26, UNIFORM
  2v1 s ∈ {27..63}.
- EIGHTEENTH-tail recheck: hold {0}∪{12..27}, UNIFORM 0v1
  s ∈ {28..63} (NEW by the z21-floor15 kit; extended by one point
  here).
- **NINETEENTH-tail identity (NEW)**: v(s,29,29)=v(s,28,29) holds
  exactly on **{0}∪{12..27}**, breaks **0v2 at s=28**, then
  **UNIFORM 2v1 for ALL s ∈ {29..63}** — BOTH predeclared
  components CONFIRMED. The even-z supply-identity form graduates
  to its candidate **5/5** (k=20/22/24/26 published + k=28 here);
  the z=28 slice's supply datum, precomputed for the future z=28
  declaration lane (registered by the z21-floor15 kit §5 handoff).
- **TWENTIETH-tail identity (NEW)**: v(s,30,30)=v(s,29,30) holds
  exactly on **{0}∪{12..29}**, breaks **UNIFORM 0v1 from s=30** for
  ALL s ∈ {30..63} — BOTH predeclared components CONFIRMED; the
  odd-z supply form extends to its candidate **6/6**; the z=29
  slice's supply datum for the future z=29 declaration lane.

## 4. Honest record (this run)

- The hand derivations were written in-session from published
  PROVED facts only (the K1339 proved z=22 ladder row, the K1264
  stair, the K0832 closed form, the published z23-min18 census
  records), and the child-position input literals were
  cross-checked against a drafting scratch engine BEFORE the freeze
  (K1344-D6 discipline, FAILS: NONE); the scratch machine is NOT
  published and evaluated none of the declared outcome values. The
  genuinely BLIND pre-declarations (head-row outcomes, blind block
  s ∈ {34..48}, multivalue census, strip/row/base-spot/below-band
  measurements, every measured count) hit with zero surprises, and
  the architectural prediction itself was registered BEFORE the
  fact by the published z21-floor15 kit's §5 (commit `5b01e14c`).
- No file edit after any frozen run; the frozen stdout is the
  published artifact.
- The local ordered-engine crosscheck and the continuity compares
  against the published f18 .out are documented in the kit README;
  the crosscheck machines themselves are unpublished (series
  convention).
- No wall-clock, no randomness, no hash-order dependence.

## 5. Handoff to the declaration lane (if opened)

- The natural proposition family here: the **floor-(z−6)
  sub-critical edition structure** — odd head row EMPTY at s=z−6
  (candidate 5/5: z=15/17/19/21/23; mirror of the even head trio
  4/4), critical-lattice profile preserved cellwise (2nd odd
  edition witnessed; now witnessed at both odd and even editions
  4+5), sub-floor s-only law (no multivalue, no new classes at
  every swept edition of the series), below-band child collapse
  7/7 (K1264 stair-consequence candidate). A formal item would
  state the refuted/confirmed columns with the witness sets and
  register the cross-slice regularities as data-backed candidates.
- Next floor-(z−6) series data points: **z=24 floor-18 (even, the
  registered 11-entry lattice prediction at positions
  {18,20,22,24} — the lane that owns z ≥ 24; counter-probe of the
  parallel T-Z24 target before claiming)** and **z=25 floor-19
  (odd, the head-empty 6/6 candidate)**. Register BEFORE
  measurement per protocol.
- The TWENTY-FIRST-tail (k=30, even form, v(s,31,31) vs
  v(s,30,31)) is the natural next pre-computation (z=30 supply;
  even-form candidate: hold {0}∪{12..29}, 0v2@30, UNIFORM 2v1
  s ≥ 31; both components derivable from the current closed-form
  data).
- The m=17 base-spot z-sequence continues (z=24 datum: the z=24
  lane), as does the m=18 base-spot z-parity alternation sequence
  (0,1,0,1,0,1,0,1 at z=16..23 — next the z=24 lane).
- Standard 11×11 empty board, two-stone roots, S2, class 1/2/4 and
  all central-reply roots: all UNKNOWN, unchanged; no verdict
  consumed.

## 6. Standard caveats

Everything in this kit and log is FINITE machine observation against
the pinned raw engine, plus pure closed-form pre-computations, plus
disclosed hand derivations whose candidate status is stated per
section. Nothing here is a theorem; no universal statement is
claimed; the battery/point counts are engine cross-checks, not proof
substitutes.
