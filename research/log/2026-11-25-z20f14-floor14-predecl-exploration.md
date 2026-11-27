# 2026-11-25 z=20 floor-14 (z−6, sub-critical floor) pre-declaration census kit — exploration log

Lane: high-speed lane (this run). Status of this document: PRIMARY
RECORD of the pre-declaration census kit
`research/experiments/strip-z20-floor14-20261125/`. No K slot is
claimed, no universal statement is claimed. Everything below is
finite machine observation against the pinned raw engine, plus
engine-free closed-form pre-computations, plus disclosed hand
derivations written BEFORE the first run of the frozen file. The
declaration lane (a later run) picks up from here.

## 1. Context, prior-lane state and slot check

Latest main at this run's start: `a5bf536c` (K1344 item + completion
log, the z=23 min>=18 chain complete). AGENTS.md and the knowledge
README re-read; no unresolved-item list contradicts this lane.

The registered targets for the high-speed lane at this point were
(a) the z=24 census (T-Z24, floor-19, 本命 — the natural next
declaration target, whose supply datum is already fully precomputed),
(b) the坐 residual bands and frontier probes, and (c) the
SEVENTEENTH-tail (k=26) pre-computation. This kit takes the lane
registered by the published z22-floor16 kit log section 5 (commit
`daa9a805`, same day, BEFORE the fact): **the z=20 floor-14
edition — the last unswept even floor below z=24 and the direct test
of the registered full-lattice 4/4 prediction.** Taking z=20 (not
z=24) avoids a head-on collision with the hourly parallel run's
registered z=24 declaration target; the z=24 lane's census kit and
declaration remain untouched for that lane.

Slot check at kit-build time: no `strip-z20-floor14*` /
`strip-z20-min14*` experiment directory and no z=20 floor-14
census, log or item exists on main (path probes; the floor-(z-6)
series' published editions are z=15 K1321, z=16 `059c531e`,
z=17 `82f98ef4`, z=18 `0bb7e440`, z=19 `5b2275bc`, z=22
`fb215b76`/`daa9a805`). The consumed published bytes
(`explore_z20f15.py`/`.out`/README commit `2cc16d34` line,
`explore_z22f16.py`/`.out`/log commit `fb215b76`/`daa9a805`,
`engine_block.py`, the z16-f10/z18-f12 frozen outputs) were
fetch-verified byte-identical against main before use
(`d4648301…` / `919df78c…` pending below / `582c93c1…` engine).

## 2. Kit construction (publish-then-execute, frozen before publication)

- `engine_block.py` — byte-clone of the published chain engine
  (sha256 `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`),
  identical to the strip-z20-min15 / strip-z22-floor16 kit bytes;
  the embedded ENGINE_BLOCK startup pin `bd5f22e4…` is asserted by
  the machinery (engine_gate PASS in the frozen output).
- `explore_z20f14.py` (sha256
  `ba6528e018ab9a65d97c67acadf9bce99fb51703d7ef0e9b62796309d67ceb71`)
  — adapted from the frozen published `explore_z22f16.py`
  (`d3c3239e…`, `fb215b76`) by the disclosed textual diff (slice
  z 22→20, floor 16→14, rungs 15→14 aligned with the published
  z=20 critical ladder F..A8 — no rank beyond A8 swept, with the
  j=15 non-derivability disclosed in the docstring; cell s-domain
  {0}∪{14..45}; tail spots {46..53}; strip m∈{14..19} with m=14
  the NEW open-row sweep; the m=14/13/12 row records + m=14
  arity<=4 ext as cross-artifact rechecks; the NEW m=14 base spot
  with the paper derivation disclosed BEFORE the first run; the
  below-band child census at z'=21 (floor 14 = z'−7); identity
  rechecks 13th..16th extended over {0}∪{12..61}; the NEW
  SEVENTEENTH-tail pre-computation with BOTH components
  predeclared).
- THE HAND DERIVATION of the complete s=14 head row (14 points,
  written before the first run, disclosed in the file docstring):
  every option set is computable from four published inputs —
  (1) the C-hand child of Cell_j(14) is exactly the published
  PROVED z=19 critical-ladder position H(j+20;{j,14};19) (j≤13
  T-Z19/K1330 cell constants, j=14 the PROVED T-Z19 m=14-row claim
  H(34;{14,14};19)=v(28,19,34)); (2) the K1264 stair equality
  covers every 14→13 child at R=j+20 EXACTLY for j≤13; (3) the
  small-token child is the in-kit cascade Cell_{j−1}(14), with the
  j=1 removal child the PROVED single token v(14,21,20); (4) the
  sole NON-proved input, disclosed: the j=1..13→14 child of rung
  j=14 lands on the published m=13-row z=20 OBSERVATIONAL record
  (f15 kit 76/0) => H(34;(13,14);20)=v(27,20,34) — a single
  observational dependency for the whole s=14 row (mirroring the
  published z22-f16 kit's own single-observational-dependency
  pattern at its m=16 base spot).
- The m=14 base spot derivation (disclosed before the first run):
  H(35;(14,14);20) options = {B-children → H(34;(13,14);20) =
  v(27,20,34)=0 by the published observational record,
  C-child → 1^H(34;(14,14);19) = 1^v(28,19,34)=0 by the PROVED
  T-Z19 m=14-row claim} → mex 1 = collapse v(28,20,35)=1,
  CONFORMING candidate.
- Determinism: SIX runs (default ×3, PYTHONHASHSEED=random same
  cwd, env -i isolated directories ×2 via /usr/local/bin/python3)
  all byte-identical, rc 0, ~28 s per run; frozen stdout
  `explore_z20f14.out` sha256
  `919df78c96a1a818164732c23673db805165f267340a0ea0b152d2ae117f9ab1`
  (29,398 bytes).

## 3. Results

### 3.1 Cell census (section a) — the registered prediction hit EXACTLY

- **THE s=14 ROW (NEW): the registered §5 head trio CONFIRMED with
  exact constants — B20f14 DOWN 0v2, A20f14 UP 1v0, A220f14 UP
  2v1**; all other rungs conform with the predeclared per-rung
  values (F,G,E,D,C = 1,0,1,0,1; A3..A8 = 0,1,0,1,0,1); every row
  single-shape (j,14). The pre→measure cycle closed with ZERO
  undisclosed classes.
- **s∈{15..27}: lattice identity with the published f15 census
  EXACT** (the shape sets coincide below s=28): deviant rows equal
  the published f15 profile — F {20: UP 1v0}, G {18: DOWN 0v2,
  20: UP 2v1}, E {18: UP 1v0}, D {16: DOWN 0v2, 18: UP 2v1},
  C {16: UP 1v0}, B {16: UP 2v1}, A..A8 collapsed;
  machine cross-compare vs `explore_z20f15.out` 6/6 cells EXACT.
- **s∈{28..45} (BLIND sub-floor block; 14-token components enter
  at s=28): NO multivalue rows, NO new deviant classes** — all
  cells s-only, 130 shapes per cell, 1,820 census points total,
  0 multivalue anywhere.
- **ACCEPTANCE COMPARISON: the FULL 11-entry deviant lattice is
  cellwise VALUE-EXACT 4/4 across the consecutive even z 16, 18,
  20, 22** — machine comparison of the published frozen outputs
  (z16-f10: B{10 0v2,12 2v1}, C{12 1v0}, D{12 0v2,14 2v1},
  E{14 1v0}, F{16 1v0}, G{14 0v2,16 2v1}, A{10 1v0}, A2{10 2v1};
  z18-f12: positions {12,14,16,18}; z22-f16: positions
  {16,18,20,22}; all published) with this kit (positions
  {14,16,18,20}): cellwise identical constants at every edition,
  s-positions the arithmetic set {z−6, z−4, z−2, z}, all
  single-shape, all s-only. The registered prediction is
  CONFIRMED at full-lattice scope: **even-z floor-(z−6)
  full-lattice uniformity 4/4** (z=16..22 consecutive even).
  Corollaries (observation-grade, for the declaration lane):
  (a) the critical floor z−5 is NECESSARY at z=20 for the
  cell-ladder Sigma-collapse, with witnesses H(27;(6,14);20)=0≠
  v(20,20,27)=2, H(28;(7,14);20)=1≠v(21,20,28)=0,
  H(29;(8,14);20)=2≠v(22,20,29)=1 — floor-necessity witnesses now
  exist at ALL FOUR swept even editions;
  (b) the even sub-critical A-revival is uniformly UP 1v0 at
  s=z−6, value-exact 4/4 (the A-rank parity law remains
  critical-floor-scoped: odd-z birth s=z−5 UP 2v0 has no
  sub-critical counterpart on the even side);
  (c) the odd editions' head remains empty (published z=15/17/19:
  the s=z−6 row is conform-resurrected only at even z; the odd
  sub-critical head is EMPTY per the published z19-f13 kit).

### 3.2 Strip and row records (sections b,c,d,e)

- Strip m∈{14..19} at R=m+21: **253 shapes, 0 violations**; the
  NEW m=14 open-row co-token sweep **68 shapes, 0 violations**
  (NEW datum: never measured by any published kit); the m∈{15..19}
  T-Z20 compliance recheck incrementals **55/44/35/28/23 = the
  published f15 cumulative profile EXACT** (cumulative 123/167/
  202/230/253 vs published 55/99/134/162/185 base-anchored,
  machine cross-compare clean).
- m=14-row z=20 (R=35): **62 shapes 0 separations** (x0 style) +
  **61/0** (arity≤4 co-token ext) — the published f15 entries
  reproduced shape-for-shape exactly (the K1330 published residual
  band m=14 z∈{20..25} first-entry datum rechecked).
- m=13-row z=20: **76/0**; m=12-row z=20: **92/0** — published f15
  entries reproduced shape-for-shape (K1328/K1325 residual-band
  datum contexts).
- Tail spots s∈{46..53}: **112/112 match**; strip spots m∈{20..23}:
  **12/12 match** (lattice identity with the published f15 rows).
- **NEW m=14 base spot H(35;(14,14);20) = 1, conforming**
  (v(28,20,35), the paper-derived candidate hit exactly). The
  m=14 base-spot z-sequence: z=19: 1 (PROVED claim value),
  z=20: 1 (here) — no alternation yet; the z=21 datum belongs to
  a future lane.

### 3.3 Below-band (z'−7 datum, section f)

H(21;Y;21) vs v(s,21,21), min(Y)≥14 (z'=21, floor 14 = z'−7):
**130 shapes, 0 deviants, 0 multivalue** — the FIFTH consecutive
z'−7 empty datum (published: z'=17/19/20/23), extending the
pattern to 5/5. K1264 stair applicability R=21 ≤ 21+min(Y) makes
this an instance of a PROVED lemma (machine corroboration; the
generalization statement belongs to a declaration lane).

### 3.4 Supply identities (engine-free, section g; pure K0832)

Over the EXTENDED domain {0}∪{12..61} (each published {12..60}
domain extended by one):

- THIRTEENTH-tail recheck: hold {0}∪{12..21}, 0v2@22, uniform 2v1
  s∈{23..61} (published constants reproduced, extended by one).
- FOURTEENTH-tail recheck: hold {0}∪{12..23}, uniform 0v1
  s∈{24..61}.
- FIFTEENTH-tail recheck: hold {0}∪{12..23}, 0v2@24, uniform 2v1
  s∈{25..61}.
- SIXTEENTH-tail recheck: hold {0}∪{12..25}, uniform 0v1
  s∈{26..61} (published NEW by z22-f16, extended).
- **SEVENTEENTH-tail identity (NEW)**: v(s,27,27)=v(s,26,27) holds
  exactly on **{0}∪{12..25}**, breaks **0v2 at s=26**, then
  **UNIFORM 2v1 for ALL s∈{27..61}** — BOTH predeclared components
  CONFIRMED. The even-z supply-identity form graduates to **4/4**
  (k=20/22/24 measured + k=26 closed-form here); this is the
  z=26 slice's supply datum, precomputed for the future
  z=24/z=25/z=26 declaration lanes (registered as the natural next
  pre-computation by the published z22-f16 and K1339/K1344
  handoffs).

## 4. Honest record (this run)

- The hand derivation of the s=14 head row was written in-session
  from published PROVED facts only, and its child-position input
  constants were cross-checked against a drafting scratch engine
  evaluation BEFORE the freeze (K1344-D6 discipline: derivation →
  engine cross-check of the input literals → freeze; disclosed in
  the kit docstring and README). The file itself ran for the first
  time only after the freeze. The head-row and base-spot constants
  are therefore DRAFTING-VERIFIED predeclarations, not blind ones;
  the BLIND predeclarations of this kit (sub-floor block
  s∈{28..45}, the multivalue census, all strip/row/below-band/
  identity measurements, every measured count) hit with zero
  surprises, and the architectural prediction itself was
  registered BEFORE the fact by the previous lane's §5 (commit
  `daa9a805`) — the before-the-fact prediction character of the
  4/4 claim rests on that registered prediction, which this kit
  confirms.
- Two docstring typos ("nope"→"none", "A820f16"→"A820f15") were
  fixed BEFORE the six frozen runs; the stdout is a pure function
  of the code bytes and was verified byte-identical across the
  fix (sha `919df78c…` unchanged). No file edit after any frozen
  run.
- Local (unpublished) ordered-engine crosscheck of all 1,820
  cell-census positions: 0 multivalue, 0 mismatches with the
  frozen canonical values.
- One raw CDN transient 404 during the published-bytes fetch
  (the known quirk); retry returned the expected bytes
  (byte-verified against the listed sizes/pins).
- No wall-clock, no randomness, no hash-order dependence; the
  frozen stdout is the published artifact.

## 5. Handoff to the declaration lane (if opened)

- The natural item here is the **sub-critical floor-necessity +
  even full-lattice uniformity proposition**: the floor-(z−6)
  cell-ladder deviant lattice is uniform across all four swept
  consecutive even z∈{16,18,20,22} (11-entry value-exact,
  arithmetic positions {z−6,z−4,z−2,z}) with the head trio
  {B DOWN 0v2, A UP 1v0, A2 UP 2v1} at s=z−6, and the odd editions
  empty at the head (published z=15/17/19 kits) — while the
  critical floor z−5 is necessary for the Sigma-collapse at all
  four even editions (witness sets recorded here and in the
  published kits). The sub-floor s-only law (no multivalue, no
  new classes) now holds at every swept edition, and the
  below-band child collapse is 5/5 (K1264 stair-consequence
  candidate, PROVED-lemma instance). A formal item would state
  the refuted universal column (the floor-(z−6) cell claim) with
  the witness sets, and register the cross-slice regularities as
  data-backed candidates; the rung-j15 non-derivability
  (H(35;{14,15};19) covered by no published fact) is also
  disclosed for that lane.
- The m=14 ROW at z=20 remains observational-only here (strip
  68/0 + rows 62+61/0 + base spot 1/0): its paper-side closure
  would need the m=13-row z=20 chain first (analogous to the
  published z22-f16 §5 note).
- The next floor-(z−6) series datum: z=21 floor-15 (odd, the head
  candidate is EMPTY per the odd-edition pattern 3/3 published);
  z=24 floor-18 is the next EVEN datum (for the lane that owns
  z≥23), predicted 11-entry lattice at positions {18,20,22,24} —
  register BEFORE measurement if that lane opens, per protocol.
- The SEVENTEENTH-tail identity is now published here (and its
  constant registration for the z=26 supply is complete); the
  EIGHTEENTH-tail (k=27, odd form, v(s,28,28)=? v(s,27,28)) is the
  natural next pre-computation (z=27 supply; odd form candidate
  5/5 extension confirmed shape: hold {0}∪{12..27}? — recorded by
  whoever runs it; both components derivable from the current
  data as before).
- Standard 11×11 empty board, two-stone roots, S2, class 1/2/4
  and all central-reply roots: all UNKNOWN, unchanged; no verdict
  consumed.

## 6. Standard caveats

Everything in this kit and log is FINITE machine observation
against the pinned raw engine, plus pure closed-form
pre-computations, plus disclosed hand derivations whose candidate
status is stated per section. Nothing here is a theorem; no
universal statement is claimed; the witnesses are single-position
evaluations of the defining recursion recorded per the series'
observation convention. The battery/point counts are engine
cross-checks, not proof substitutes.
