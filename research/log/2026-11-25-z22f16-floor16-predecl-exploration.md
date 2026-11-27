# 2026-11-25 z=22 floor-16 (z−6, sub-critical floor) pre-declaration census kit — exploration log

Lane: high-speed lane (this run). Status of this document: PRIMARY
RECORD of the pre-declaration census kit
`research/experiments/strip-z22-floor16-20261125/`. No K slot is
claimed, no universal statement is claimed. Everything below is finite
machine observation against the pinned raw engine, plus engine-free
closed-form pre-computations, plus a disclosed hand derivation written
BEFORE the first run. The declaration lane (a later run) picks up from
here.

## 1. Context, prior-lane state and slot check

This run received the K1339 (T-Z22, z=22 min>=17) publication chain
COMPLETED by the parallel conic-adjacent lane (declaration `575abe90` +
repair `7b969301`, machine `e2c79d64`, official runs `76280d80`, item+
log `70b409c5`); this run's own K1339 item/log draft was detected as
duplicate at the pre-push probe and was NOT published (no loss). This
run then performed a second-environment acceptance of the published
chain (engine bytes fetch-back sha-matched; two local runs of the
published `verify_k1339.py` byte-identical with the official stdout
`05be7d66…`, battery 18,128 pts all gates 0 bad; independent
reconstruction machine also converges). Mis-correction noted once and
fixed: the published battery total IS 18,128 (the 19,128 figure in this
run's local draft notes was a mis-sum; draft notes unpublished).

The published K1339 completion log §5 and declaration note §5 register
TWO open lanes for the z=22 territory: the z=23 slice census (T-Z23,
floor-18, 本命 — the natural next lane) and the FLOOR-NECESSITY
question (their phrasing: "z=22 is settled at floor 17 = z−5; the
z−6 floor is unexplored" — correctly scoped: unswept for the z=22
slice). This kit takes the SECOND lane
(floor-16 = z−6 at z=22) to avoid a head-on collision with the hourly
parallel run's registered z=23 target. REPAIR (same-day): the
originally published revision of this paragraph claimed that nothing
in the published record censused ANY sub-critical (z−6) lattice and
that every strip-series kit swept exactly the critical floor; that
was WRONG — the floor-(z−6) SERIES had five published editions at
kit-build time (z=15 K1321, the z=16 min>=10 kit `059c531e`, the
z=17 min>=11 kit `82f98ef4`, the z=18 min>=12 kit `0bb7e440` — whose
predecl (m4) revival cascade confirmed the {B,A,A2} trio value-exact
2/2 with z=16 — and the z=19 min>=13 kit `5b2275bc`). This kit's
census is the SIXTH edition of that series and its first z>=20
edition; the z=22 floor-16 slot itself was genuinely unclaimed
(path probe below).

No counter-publication of a z=22 floor-16 census existed at kit-build
time (checked: no `research/experiments/strip-z22-floor16*` /
`strip-z22-min16*` directory; the floor-(z−6) series' published
editions stop at z=19, so the z=22 floor-16 lattice was untouched;
the s=16 row of the z=22 floor-16 cell ladder, the m=16
base spot, the sub-critical below-band datum and the sixteenth-tail
pre-computation were all unmeasured at this session's start).

## 2. Kit construction (publish-then-execute, frozen before publication)

- `engine_block.py` — byte-clone of the published chain engine (sha256
  `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`),
  copied from the locally verified kit bytes (fetch-back verified
  against `115c0bb9` earlier in this session) and sha-verified. The
  embedded ENGINE_BLOCK startup pin `bd5f22e4…` is asserted by the
  machinery (engine_gate PASS in the frozen output).
- `explore_z22f16.py` (sha256
  `d3c3239e78f91659222a6b043920b5095c46e953d67daf8ba26bf7a3038062ce`)
  — adapted from the frozen published `explore_z22f17.py` (sha256
  `9e8ab707…`, fetch-back verified against `115c0bb9` earlier) by the
  disclosed textual diff: floor 17→16; rungs 16→15 with the top rung
  labeled A9 (PROVISIONAL, small token 15 — one rank beyond the
  published A921f16; final naming belongs to the declaration lane);
  cell s-domain {0}∪{16..47}; tail spots {48..55}; strip sweep
  m∈{16..21} (m=16 = the OPEN m=16 row at z=22, NEW co-token sweep
  S∈{16..55}; m∈{17..21} = the PROVED T-Z22 claim positions, compliance
  recheck); the m=16/15/14/13-row records as cross-artifact rechecks of
  the published f17 entries; the NEW m=16 base spot; the below-band
  child census (z'=23, floor 16 = z'−7); the identity rechecks
  extended over {0}∪{12..60}; the NEW SIXTEENTH-tail engine-free
  pre-computation with BOTH components predeclared.
- THE HAND DERIVATION (disclosed in the file docstring, written BEFORE
  the first run): the s=16 row of the floor-16 ladder is single-shape
  (j,16) and its option set is fully computable on paper from four
  published inputs: (1) the PROVED K1337 z=21 floor-16 lemma values —
  the C-hand child of Cell_j(16) is EXACTLY the K1337 lemma position
  H(j+22;{j,16};21); (2) the published K1264 stair equality at
  R=z+min EXACTLY — the 16→15 B-hand children sit at R=j+22=22+j
  exactly, conforming stair values; (3) the small-token B-child is
  Cell_{j-1}(16) itself (R=z+min+1, one above the stair point); (4)
  the j=1 removal child H(23;{16};23)=v(16,23,23). The derived
  profile: cells conform at s=16 for j∈{1..5} (the C-cell's C-hand
  disturbance 1^C21f16(16)=0 vs single 1^2=3 is mex-irrelevant:
  option sets {0,0,0} vs {0,3}, both mex 1) and j∈{9..15} (the B-small
  cascade from the j=6..8 deviant values is mex-irrelevant at each
  step), with THREE deviants: B22f16(16)=0 vs v(22,22,29)=2 (DOWN
  0v2; options {1,1,1} vs single {1,0}), A22f16(16)=1 vs
  v(23,22,30)=0 (UP 1v0; options {0,2,3} vs single {2,1}),
  A222f16(16)=2 vs v(24,22,31)=1 (UP 2v1; options {1,0,0} vs single
  {0,0}).
- THE FULL PREDECLARED CANDIDATE also included: the {17..31} classes
  as LATTICE IDENTITY with the published f17 census (single 2-token
  shapes, identical points); NO multivalue rows and NO classes beyond
  {16,18,20,22}; tail spots 120/120 (lattice identity); strip
  m∈{16..21} 0 violations; rows 40+39+50+62+76 with 0 separations
  (cross-artifact); strip spots 12/12; m=16 base spot = 1 CONFORMING
  (paper-derived: B-children on the published m=15-row record, C-child
  on the PROVED T-Z21 m=16 row at z=21, single options {0,0} → mex 1);
  below-band 0 deviants 0 multivalue; the four identity constants as
  published/predeclared.
- Determination protocol (frozen before the runs, executed exactly):
  default run + default re-run + PYTHONHASHSEED=1 same-cwd +
  PYTHONHASHSEED=random same-cwd + env -i isolated-directory runs ×2
  (explicit `/usr/local/bin/python3`, empty environment). SIX runs
  total, all byte-identical (sha256
  `4b65f7f07ab49cc4adb90194372397b9418f6f66fe69366211d71bfeaa3393ee`,
  rc 0 each, ~30 s each; compile check only, no census execution,
  before the freeze). The frozen `explore_z22f16.out` IS that stdout.
- Independent cross-checks (same environment, not part of the frozen
  artifact): (a) the ordered-engine cross-check
  (`xcheck_z22f16.py`, sha256 `8eba4498…`, H_ordered re-evaluation of
  EVERY swept row): 1,575 cell shapes + 120 tail + 169 strip + 267
  row-record + 12 spots + 1 base spot + 105 below-band + 200 identity
  rows: **0 mismatches**, rc 0, ~39 s; (b) the cross-artifact
  continuity compare against the published `explore_z22f17.out`
  (`f16a87d4…`): per-cell deviant profiles (f16 restricted to s>=17)
  EXACT 15/15, tail rows EXACT, strip per-m incrementals
  35/28/23/20/19 EXACT, row records shapes and separations EXACT,
  strip spots EXACT.

## 3. Observations (all judgment-free)

### 3.1 Cell ladder (15 rungs, 105 shapes each, all s-only, multivalue 0)

Deviant position set = **{16, 18, 20, 22}**. The s=16 classes revive
in-domain exactly as hand-derived BEFORE the run, and the {18,20,22}
classes are the published f17 classes lattice-identical:

- **s=16 (the floor-necessity row, NEW)**: **B22f16 {16: DOWN 0v2}**
  (H(29;(6,16);22)=0 vs v=2), **A22f16 {16: UP 1v0}**
  (H(30;(7,16);22)=1 vs v=0), **A222f16 {16: UP 2v1}**
  (H(31;(8,16);22)=2 vs v=1). All other cells conform at s=16.
  Consequences (recorded as candidates/observations):
  - The universal floor-16 cell claim FAILS: the critical floor
    17 = z−5 is NECESSARY for the z=22 cell-ladder Sigma-collapse
    (three machine-rigorous witnesses — single-position evaluations of
    the defining K1138 recursion; the necessity statement, its
    generalization across slices and the relapse closed forms belong
    to a future declaration lane if opened). The published "z−6 floor
    unswept" open item is answered for z=22 at cell level: the floor
    does NOT drop.
  - The even-z A-break extinction is a CRITICAL-FLOOR phenomenon:
    A22f16 is the THIRD even-z sub-critical A-rank deviant,
    value-exact with the published A16f10 (s=10) and A18f12 (s=12) —
    all UP 1v0 at s=z−6, never the odd-z s=z−5 UP 2v0 birth form.
    The A-rank parity law (3/3 odd birth, 5/5 even extinction at
    floor z−5) does not extend below the critical floor; at the
    z−6 floor the even A-rank revives with the uniform value 1 (3/3).
  - The s=16 relapse station carries the even station value trio
    {DOWN 0v2, UP 1v0, UP 2v1} at heads {B, A, A2} — the THIRD even
    floor-(z−6) station (after the published z=16 s=10 and z=18 s=12
    stations; head shift relative to the critical stations
    {D,C,B}@18). ACCEPTANCE COMPARISON (added by the same-day
    repair, against the published z16-f10/z18-f12 frozen outputs):
    the FULL 11-entry deviant lattice is cellwise VALUE-EXACT across
    z=16/z=18/z=22 with the s-positions the arithmetic set
    {z−6, z−4, z−2, z} — heads {B,A,A2}@z−6 plus the ladder
    B/C/D@(z−4), D/E/G@(z−2), F/G@z, 11/11 entries per kit. The
    registered +2-revival candidate (head-trio scope, value-exact
    2/2 at the z18 kit's publication) is CONFIRMED at z=22 and
    UPGRADED to full-lattice scope, value-exact 3/3. z=20 floor-14
    is the one remaining unswept even floor-(z−6) edition below
    z=24.
- **s∈{17..31} (lattice identity with f17)**: F {22: UP 1v0},
  G {20: DOWN 0v2, 22: UP 2v1}, E {20: UP 1v0},
  D {18: DOWN 0v2, 20: UP 2v1}, C {18: UP 1v0}, B {18: UP 2v1};
  A..A9 collapsed at s>=17. Cross-artifact machine-compare EXACT.
- **s∈{32..47} (first sub-floor multi-token shapes; 16-token
  components enter)**: NO multivalue rows, NO new deviant classes —
  s-only survives its first sub-critical-floor test.

**The measurement hit the complete predeclared profile EXACTLY — the
SECOND fully-closed pre→measure cycle of the series (after f17):
zero undisclosed classes.** (The floor-(z−6) series' z16/z18/z19
kits also published pre-declaration cycles, the z18 kit's (m4)
engine-free cascade of narrower scope — revival cascade plus
boundary children, not the complete cell-ladder profile; the
originally published "first at a sub-critical floor" phrasing of
this sentence is withdrawn by the same-day repair. This kit's own
closure scope: the complete predeclared cell-ladder profile at a
sub-critical floor.)

### 3.2 Strip and row records

- Strip m∈{16..21} (R=m+23): **169 shapes, 0 violations**; the NEW
  m=16 open-row sweep carries **44 shapes, 0 violations**; the
  m∈{17..21} T-Z22 compliance recheck: 125 shapes 0 violations
  (incrementals 35/28/23/20/19 = the published f17 cumulative profile
  exactly).
- m=16-row z=22 (R=39): **40 shapes 0 separations** (x0 style) +
  **39 shapes 0 separations** (arity<=4 co-token ext) — the published
  f17 entry reproduced shape-for-shape (machine-checked); candidate
  FIRST entry of the future T-Z21 residual band m=16 z∈{22..29}
  unchanged.
- m=15/14/13-rows: 50/62/76 shapes, 0 separations — the published f17
  entries reproduced shape-for-shape (machine-checked).
- Strip spots m∈{22..25}: **12/12 match**.
- **NEW m=16 base spot `H(39;(16,16);22)` = 1, conforming** (=
  v(32,22,39); the paper-derived candidate hit exactly). The m=16
  base-spot z-sequence: z=21: 1 (published), z=22: 1 (here) — two data
  points, no alternation yet.

### 3.3 Below-band (z'−7 datum)

`H(23;Y;23)` vs `v(s,23,23)`, min(Y)>=16 (child slice z'=23, floor
16 = z'−7, two below the critical z'−5 pattern): **105 shapes,
0 deviants, 0 multivalue** — full collapse of the below-band supply
child at floor z'−7; the FOURTH recorded z'−7 empty datum (the
published z16-f10/z18-f12/z19-f13 kits' below-band child sections
are empty at z'=17/19/20; here z'=23), extending the empty pattern
to 4/4. The published K1264
stair applicability R=23 <= 23+min(Y) suggests this collapse is a
stair consequence at ANY floor; recorded as observation only.

### 3.4 Supply identities (engine-free, section g; pure K0832)

- THIRTEENTH-tail recheck: hold {0}∪{12..21}, 0v2@22, uniform 2v1 for
  ALL s∈{23..60} (published constants reproduced, extended by one).
- FOURTEENTH-tail recheck: hold {0}∪{12..23}, uniform 0v1 for ALL
  s∈{24..60} (extended by one).
- FIFTEENTH-tail recheck: hold {0}∪{12..23}, 0v2@24, uniform 2v1 for
  ALL s∈{25..60} (the f17 predeclared-and-confirmed constants
  reproduced, extended by one).
- **SIXTEENTH-tail identity (NEW)**: v(s,26,26)=v(s,25,26) holds
  exactly on **{0}∪{12..25}**, breaks with **UNIFORM 0v1 for ALL
  s∈{26..60}** — BOTH predeclared components CONFIRMED (break start
  s=26 AND the uniform 0v1 shape). The odd-z supply-identity form is
  now **4/4** (z=19/z=21/z=23 measured; z=25-supply closed-form
  pre-computation) — the z=25 slice's supply datum. This datum was
  registered for the z=23 census lane by the published f17 handoff;
  whichever kit publishes first, the other's copy is a recheck
  (constants identical by construction — pure closed form).

## 4. Honest record (this run)

- All published bytes consumed during the build were the local kit
  copies fetch-back verified against `115c0bb9` (engine_block.py,
  explore_z22f17.py, explore_z22f17.out) before the adaptation; the
  K1337 lemma values used by the hand derivation were taken from the
  published K1337 item text (fetched from main at this run's start)
  and cross-checked against the published z21-min16 census constants;
  the derivation was written into the docstring BEFORE the first run
  and the file was not edited after the runs.
- The predeclaration hit EXACTLY (no class, value or count surprise in
  the cell/deviant architecture; row/strip shape counts 44 etc. were
  measured counts, not predeclared, per series convention).
- Two comparison-script incidents, both in CHECK code, not in the
  data: (a) the first cross-artifact compare invocation initialized
  the strip incremental accumulator to 0 instead of the m=16
  cumulative (44), producing one false mismatch, fixed and re-run
  clean (5/5 incrementals EXACT); (b) the first ordered-engine xcheck
  invocation compared the engine-free identity hold rows with
  mismatched tuple shapes (1-tuples vs ints), producing four false
  mismatches; the identity data was reproduced exactly after the fix
  (and the identity sections had ALREADY verified equal in the engine
  sections' run before the fix — no frozen data was touched by either
  incident; the frozen artifact was never re-run or edited).
- No wall-clock, no randomness, no hash-order dependence.
- REPAIR DISCLOSURE (same-day repair commit, README + log prose
  only): the originally published revision of this log and the kit
  README overstated the kit's historical novelty on three points
  (the "nothing censuses ANY sub-critical lattice / critical floors
  only" claim, the "FIRST even-z A-rank deviant ever observed"
  claim, and the "FIRST sub-critical below-band datum" claim),
  corrected after the acceptance comparison against the published
  floor-(z−6) series' frozen outputs (z16-f10/z18-f12/z19-f13). The
  frozen artifacts were never edited (their sha256 pins hold); the
  repair adds the 3/3 full-lattice and 4/4 below-band acceptance
  results and the §5 z=20 floor-14 registered prediction.
- Push protocol: latest main re-fetched immediately before the push
  (hourly parallel-run hazard); the z22-floor16 census slot confirmed
  unclaimed; kit + this log pushed in one commit; fetch-back byte
  verification in the same session.
- Session note: the K1339 acceptance observations in §1 are this run's
  independent verification of ANOTHER lane's published chain; the
  authors of that chain are the hourly parallel runs.

## 5. Handoff to a declaration lane (if opened)

- The natural item here is a "floor necessity" proposition: the
  critical floor z−5 is optimal in the cell-ladder direction at
  z=22 (the z−6 floor-16 cell claim fails with the three witnesses
  above), while the ROW direction (the m=16 row at z=22: strip 44/0 +
  row 40+39/0 + base spot 1/0 here) still collapses everywhere swept.
  A formal necessity item would state the refuted universal form and
  the witness set, and register the cross-slice generalization with
  the floor-(z−6) series' data now behind it: even editions swept
  z=16/z=18 (published) + z=22 (here), odd editions swept
  z=15/z=17/z=19 (published; empty at s=z−6), so the candidate
  regularities are data-backed, not first tests: (i) the s=z−6 row
  deviant with the {B,A,A2} value trio {DOWN 0v2, UP 1v0, UP 2v1} at
  every EVEN floor-(z−6) edition — 3/3 value-exact at FULL-LATTICE
  scope (see §3.1 acceptance comparison) — and empty at every ODD
  edition (z=19 head empty, per its published kit), (ii) s-only
  surviving below the critical floor, (iii) the below-band child
  fully collapsing at any floor (4/4 empty z'−7 data;
  stair-consequence candidate), (iv) the A-rank parity law being
  critical-floor-scoped, with the sub-critical even A-revival
  uniformly UP 1v0 (3/3).
  The natural NEXT edition of the floor-(z−6) series is z=20
  floor-14 — the last unswept even floor below z=24 and the parallel
  hourly lane's registered next datum. With the full-lattice
  uniformity now 3/3, the prediction is registered here BEFORE the
  fact (same-day repair): head trio {B 0v2, A 1v0, A2 2v1} at s=14
  and the ladder B {16 UP 2v1}, C {16 UP 1v0}, D {16 DOWN 0v2,
  18 UP 2v1}, E {18 UP 1v0}, F {20 UP 1v0}, G {18 DOWN 0v2,
  20 UP 2v1} — 11 entries total, the same cellwise constants, all
  cells s-only, 0 multivalue rows; each row single-shape, matching
  the arithmetic set {z−6, z−4, z−2, z} at z=20. If the z=20 edition
  hits this profile exactly, the full-lattice uniformity reaches 4/4
  across ALL consecutive even z 16..22.
- The paper-side status of the m=16 ROW claim at z=22, as disclosed by
  this census: the B-children are stair-equal (K1264, PROVED), the
  C-hand children are the PROVED T-Z21 m=16 row at z=21; the only
  non-proved dependency is the 16→15 B-child chain landing on the
  m=15-row positions at z=22 (observational 50/0). The row is "one
  observational dependency away" from paper-closed within the census
  domain — a T-Z(16)-row declaration would need the m=15 row chain
  closed first (its own z=22 entry is rechecked here at 50/0).
- The m=16 base spot=1 adds the second point of the m=16 spot
  z-sequence (z=21: 1, z=22: 1 — the base-spot z-parity alternation
  known for the slice-floor spots does NOT yet show at the m=16 row;
  z=23 datum pending).
- The sixteenth-tail identity is now published here; the z=23 census
  lane's kit (if it includes it per the f17 handoff) should treat it
  as a recheck.
- 11×11 standard empty board, two-stone roots, S2, class 1/2/4 and all
  central-reply roots: all UNKNOWN, unchanged; no verdict consumed.

## 6. Standard caveats

Everything in this kit and log is FINITE machine observation against
the pinned raw engine, plus pure closed-form pre-computations for
section (g), plus a disclosed hand derivation whose status is that of
a candidate written before measurement. Nothing here is a theorem; no
universal statement is claimed; the witnesses are single-position
evaluations of the defining recursion recorded per the series'
observation convention. Standard 11×11 positions all UNKNOWN. The
battery/point counts are engine cross-checks, not proof substitutes.
