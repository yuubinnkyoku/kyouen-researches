# 2026-11-26 z=21 floor-15 (z−6, sub-critical) pre-declaration census kit — exploration log

Lane: high-speed lane (this run). Status of this document: PRIMARY
RECORD of the pre-declaration census kit
`research/experiments/strip-z21-floor15-20261126/`. No K slot is
claimed, no universal statement is claimed. Everything below is
finite machine observation against the pinned raw engine, plus
engine-free closed-form pre-computations, plus disclosed hand
derivations written BEFORE the first run of the frozen file. The
declaration lane (a later run) picks up from here.

## 1. Context, prior-lane state and slot check

Latest main at this run's start: `cf699df2` (Part EU repaired-kit
second-host spot re-execution log, 2026-11-26T01:29:52Z). AGENTS.md
and the knowledge README re-read; no unresolved-item list or landing
commit contradicts this lane (the long-term lanes' Part EV/EU/EV
dossier chain is orthogonal to the strip series; no strip-series
commit landed since `2d8cea40`).

The registered targets for the high-speed lane at this point were the
published z20-floor14 kit log §5 handoffs (commit `2d8cea40`):
(a) **z=21 floor-15 (odd, the head candidate is EMPTY per the
odd-edition pattern 3/3 published)** — taken here;
(b) **the EIGHTEENTH-tail (k=27, odd form) pre-computation** —
bundled here;
(c) z=24 floor-18 (even, the registered 11-entry lattice prediction)
— left for the lane that owns z≥23 (counter-probe of the parallel
T-Z24 target required there). The halted 2026-11-26 session had
hand-prepared (never published, never executed) candidate packages
for both; this run re-derived everything from published PROVED facts
and executed from scratch.

Slot check at kit-build time: no `strip-z21-floor15*` /
`strip-z21-min15*` experiment directory and no z=21 floor-15 census,
log or item exists on main (path probes; `z21f15` /
`filename:explore_z21` searches return only the critical z21-min16
kit; `eighteenth` search returns no supply-identity kit). The
consumed published bytes (`explore_z21f16.py`/`.out` frozen census
output `10f94100…`, `explore_z20f14.py` `ba6528e0…` template,
`engine_block.py`, K1335 item, z20f14/ z21min16 logs) were
fetch-verified byte-identical against main before use
(engine `582c93c1…` byte-clone asserted by the startup pin
`bd5f22e4…`).

## 2. Kit construction (publish-then-execute, frozen before publication)

- `engine_block.py` — byte-clone of the published chain engine
  (sha256 `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`),
  identical to the strip-z20-min15 / strip-z22-floor16 /
  strip-z20-floor14 kit bytes; the embedded ENGINE_BLOCK startup pin
  `bd5f22e4…` is asserted by the machinery (engine_gate PASS in the
  frozen output).
- `explore_z21f15.py` (sha256
  `f644b43c2f75fe4d57effda2b0ae20137170b1b06cd17e24cb9650d07d58835e`,
  36,791 bytes) — adapted from the published frozen
  `explore_z21f16.py` (z21-min16 census kit) by the disclosed
  parameter diff (floor 16→15, cell s-domain {0}∪{15..46}, rungs
  j=1..15 with the j=16 non-derivability disclosed, strip
  m ∈ {15..20} with m=15 the NEW open row, the NEW m=15 base spot,
  below-band z'=22, identity sections 12th..17th rechecks over the
  extended domain {0}∪{12..62} + the NEW EIGHTEENTH-tail
  pre-computation with BOTH components predeclared).
- THE HAND DERIVATION of the complete s=15 head row (15 points) and
  of the m=15 base spot was written BEFORE the first run, disclosed
  in the file docstring: every option set computable from four
  published inputs — (1) the C-hand child of Cell_j(15) is exactly
  the published PROVED z=20 critical-ladder position
  H(j+21;{j,15};20) (K1335/T-Z20 cell constants; the whole published
  z=20 ladder row at s=15 conforms; j=15 is the PROVED T-Z20
  m=15-row base position H(36;(15,15);20)=v(30,20,36)=0);
  (2) the K1264 stair equality covers every 15→14 B-hand child
  (j,14) at R=j+21 EXACTLY for j ≤ 14 (min=j);
  (3) the small-token child is the in-kit cascade Cell_{j−1}(15),
  with the j=1 removal child the stair position H(22;(15,);22)=
  v(15,22,22)=1; (4) the sole NON-proved input, disclosed: both
  j=15 B-hand children land on (36;(14,15);21) = the published
  z=21 m=14-row OBSERVATIONAL record position (z21-min16 census
  kit: 62 shapes 0 separations) => H(36;(14,15);21)=v(29,21,36)=1 —
  a single observational dependency for the whole s=15 row
  (mirroring the published z20-f14 kit's own
  single-observational-dependency pattern at its j=14 rung).
  The input literals were cross-checked against a drafting scratch
  engine evaluation BEFORE the freeze (K1344-D6 discipline); the
  declared OUTCOME values were NOT engine-checked before the freeze.
  The m=15 base spot derivation (disclosed before the first run):
  B-children → H(36;(14,15);21) = 1 (observational record),
  C-child → 1^H(36;(15,15);20) = 1^v(30,20,36) = 1 (PROVED T-Z20)
  → options {1,1} → mex 0 = collapse v(30,21,37)=0, CONFORMING
  candidate.
- Determinism: SIX runs (first frozen run + default ×2,
  PYTHONHASHSEED=random same cwd, env -i isolated directories ×2
  via /usr/local/bin/python3) all byte-identical, rc 0, ~26 s per
  run; frozen stdout `explore_z21f15.out` sha256
  `6b88288a144beaaa36490ee7dff60e21d0dd1d8c13467c0f128456dd8d770def`
  (38,446 bytes).

## 3. Results

### 3.1 Cell census (section a) — the registered prediction hit EXACTLY

- **THE s=15 ROW (NEW): the registered §5 EMPTY ODD HEAD
  CONFIRMED** — zero deviant classes at s=15, the whole row
  conforming with the hand-derived per-rung values (the derived
  alternation 0,1,0,1,… identical to the collapse sequence at every
  rung); single shape (j,15) at every j; 0 multivalue at s=15.
  The odd-edition head-empty pattern (z=15 K1321, z=17 `82f98ef4`,
  z=19 `5b2275bc`) reaches its candidate **4/4**, the mirror of the
  even head trio {B DOWN 0v2, A UP 1v0, A2 UP 2v1} registered
  value-exact 4/4 at z ∈ {16,18,20,22}.
- **s ∈ {16..29}: lattice identity with the published f16 census
  EXACT** (no 15-token component fits below s=30): deviant rows
  equal the published f16 profile — F {20: DOWN 1v2, 21: HOLE,
  22..46: UP 2v0 tail}, G {20: DOWN 0v1}, E {18: DOWN 1v2, 20:
  UP 2v0}, D {18: DOWN 0v1}, C {16: DOWN 1v2, 18: UP 2v0},
  B {16: DOWN 0v1}, A {16: UP 2v0} (the A RANK BREAK REBIRTH class,
  birth s=z−5=16, SURVIVES the floor drop 16→15 — the
  definition-domain-exclusion NON-event 3rd consecutive),
  A2..A9 collapsed; machine cross-compare vs the published frozen
  `explore_z21f16.out` deviant sets 15/15 cells EXACT.
- **s ∈ {30..46} (BLIND sub-floor block; 15-token components enter
  at s=30): NO multivalue rows, NO new deviant classes** — 116
  shapes per cell, 1,856 census points total, 0 multivalue anywhere;
  the F persistent tail UP 2v0 passes through the block uniformly.
- Tail spots s ∈ {47..54}: F 8/8 mismatch, all other cells 112/120
  match — row-for-row identical to the published f16 tail spots
  (machine-verified 120/120).
- Local (unpublished) ordered-engine crosscheck of all 1,856
  census + below-band points: 0 mismatches with the frozen
  canonical values.

### 3.2 Strip and row records (sections b,c,d,e)

- Strip m ∈ {15..20} at R=m+22: **205 shapes, 0 violations**; the
  NEW m=15 open-row co-token sweep **55 shapes 0 violations** (a NEW
  datum: never measured by any published kit; published f16's m=15
  sweep existed only in the m=15-row x0 record style); the m ∈
  {16..20} T-Z21 compliance recheck incrementals **44/35/28/23/20 =
  the published f16 cumulative profile EXACT** (cumulative
  99/134/162/185/205 base-anchored, machine cross-check clean).
- m=15-row z=21 (R=37): **50 shapes 0 separations (x0 style) + 49/0
  (arity≤4 co-token ext)** — recheck of the published z21-min16
  record shape-for-shape; FIRST entry of the K1335-published T-Z20
  residual band m=15 z ∈ {21..28} reconfirmed.
- m=14-row z=21 (R=36): **62/0**; m=13-row z=21 (R=35): **76/0**;
  m=12-row z=21 (R=34): **92/0** — all cross-artifact rechecks
  shape-for-shape with the published z21-min16 entries (K1330
  second-entry / K1328 third-entry / K1325 fourth-final-entry
  residual-band contexts).
- Strip spots m ∈ {21..24}: **12/12 match** (row-for-row identity
  with the published f16 spots).
- **NEW m=15 base spot H(37;(15,15);21) = 0 = v(30,21,37)
  CONFORMING** (the paper-derived candidate hit exactly; derivation
  disclosed before the first run). The m=15 base-spot z-sequence:
  z=20: 0 (published), z=21: 0 (here) — no alternation yet; the
  z=22 datum belongs to a future lane.

### 3.3 Below-band (z'−7 datum, section f)

H(22;Y;22) vs v(s,22,22), min(Y) ≥ 15 (z'=22, floor 15 = z'−7):
**116 shapes, 0 deviants, 0 multivalue rows** — the SIXTH
consecutive z'−7 empty datum (published: z'=17/19/20/21/23),
extending the pattern to 6/6. K1264 stair applicability
R=22 ≤ 22+min(Y) makes this an instance of a PROVED lemma (machine
corroboration; the generalization statement belongs to a declaration
lane).

### 3.4 Supply identities (engine-free, section g; pure K0832)

Over the EXTENDED domain {0}∪{12..62} (each published {12..61}
domain extended by one):

- TWELFTH-tail recheck (this slice's own F supply): hold
  {0}∪{12..21}, UNIFORM 0v1 s ∈ {22..62}.
- THIRTEENTH-tail recheck: hold {0}∪{12..21}, 0v2@22, UNIFORM
  2v1 s ∈ {23..62}.
- FOURTEENTH-tail recheck: hold {0}∪{12..23}, UNIFORM 0v1
  s ∈ {24..62}.
- FIFTEENTH-tail recheck: hold {0}∪{12..23}, 0v2@24, UNIFORM
  2v1 s ∈ {25..62}.
- SIXTEENTH-tail recheck: hold {0}∪{12..25}, UNIFORM 0v1
  s ∈ {26..62}.
- SEVENTEENTH-tail recheck: hold {0}∪{12..25}, 0v2@26, UNIFORM
  2v1 s ∈ {27..62}.
- **EIGHTEENTH-tail identity (NEW)**: v(s,28,28)=v(s,27,28) holds
  exactly on **{0}∪{12..27}**, breaks **0v1 at s=28**, then
  **UNIFORM 0v1 for ALL s ∈ {28..62}** — BOTH predeclared
  components CONFIRMED. The odd-z supply-identity form graduates
  to its candidate **5/5** (k=19/21/23/25 published + k=27
  closed-form here); this is the z=27 slice's supply datum,
  precomputed for the future z=27 declaration lane (registered as
  the natural next pre-computation by the published z22-f16 and
  z20-f14 and K1339/K1344 handoffs).

## 4. Honest record (this run)

- The hand derivations were written in-session from published
  PROVED facts only (the K1335 proved z=20 ladder row, the K1264
  stair, the K0832 closed form, the published z21-min16 census
  records), and the child-position input literals were
  cross-checked against a drafting scratch engine BEFORE the freeze
  (K1344-D6 discipline); the scratch machine is NOT published and
  evaluated none of the declared outcome values. The genuinely
  BLIND pre-declarations (head-row outcomes, blind block
  s ∈ {30..46}, multivalue census, strip/row/base-spot/below-band
  measurements, every measured count) hit with zero surprises, and
  the architectural prediction itself was registered BEFORE the
  fact by the published z20-floor14 kit's §5 (commit `2d8cea40`).
- No file edit after any frozen run; the frozen stdout is the
  published artifact. One README typo (a stray bracket) was fixed
  before publication; the frozen kit files are unchanged.
- The local ordered-engine crosscheck and the continuity compares
  against the published f16 .out are documented in the kit README;
  the crosscheck machine itself is unpublished (series convention).
- No wall-clock, no randomness, no hash-order dependence.

## 5. Handoff to the declaration lane (if opened)

- The natural proposition family here: the **floor-(z−6) odd
  sub-critical edition structure** — head row EMPTY at s=z−6
  (candidate 4/4: z=15/17/19/21; mirror of the even head trio 4/4),
  critical-lattice profile preserved cellwise, sub-floor s-only law
  (no multivalue, no new classes: now at every swept edition of the
  series), below-band child collapse 6/6 (K1264 stair-consequence
  candidate). A formal item would state the refuted/confirmed
  columns with the witness sets and register the cross-slice
  regularities as data-backed candidates.
- Next floor-(z−6) series data points: **z=23 floor-17 (odd, the
  head-empty 5/5 candidate + preservation of the published
  T-Z23/K1344 critical lattice)** and **z=24 floor-18 (even, the
  registered 11-entry lattice prediction at positions {18,20,22,24}
  — the lane that owns z≥23; counter-probe of the parallel T-Z24
  target before claiming)**. Register BEFORE measurement per
  protocol.
- The NINETEENTH-tail (k=28, even form, v(s,29,29) vs v(s,28,29))
  is the natural next pre-computation (z=28 supply; even-form
  candidate: hold {0}∪{12..27}, 0v2@28, UNIFORM 2v1 s ∈ {29..}; both
  components derivable from the current closed-form data).
- The m=15 base-spot z-sequence continues (z=22 datum: the
  m=15-row at z=22 is in-band, z*(15)=29 > 22).
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
