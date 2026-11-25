# z20-min15 pre-declaration exploration kit (frozen)

This directory is the publish-then-execute PRIMARY RECORD for the pre-declaration
census of the z=20 min>=15 (floor-15) slice — the next slice of the vertical-fiber
strip series after the K1330 (T-Z19) official runs (OFFICIAL-PASS at `25aafdda`).
No K slot is claimed by this kit and no claim is made here: everything below is
machine observation. The declaration lane (a later run) picks up the slot claim,
the paper proof, the verification machine and the official runs.

## Contents

- `engine_block.py` — sha256 `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`
  (the pinned engine block, byte-identical to the K1282..K1330 chain; sha256 of the
  embedded block itself is the startup pin `bd5f22e4…`).
- `explore_z20f15.py` — sha256
  `d46483016507bbc6e99d778baa528a053e57b325ded3d236564355eee13a2897`
  (adapted from the frozen published `explore_z19f14.py`
  `e41138e20d254922030c14b4bc07a06de838de9c51527967a3ec5029722ef325` by the
  disclosed textual diff: z 19→20, cell budget j+20→j+21, floor 14→15, rungs
  13→14 with the provisional 14th-rank label `A8` (small token 14 — the SIXTH
  consecutive in-band base child; z*(14)=26 > 20), s domain {0}∪{15..45},
  strip m∈{15..19} at the provisional T-Z20 claim position, an IN-BAND
  m=14-row record at z=20 (R=35, the T-Z20 base-child position AND the FIRST
  entry of the K1330 published residual band m=14 z∈{20..25}, frontier z=26;
  published residual-band style arity<=3 TOTAL, plus an arity<=4 co-token
  extension sweep), an IN-BAND m=13-row record at z=20 (R=34, the SECOND
  entry of the K1328 published residual band m=13 z∈{19..24}; SAME enumeration
  as the published z=19 census / z=20 probe entries → same 76 shapes,
  cross-artifact consistency), an IN-BAND m=12-row record at z=20 (R=33, the
  THIRD entry of the K1325 published residual band m=12 z∈{18..21}; SAME
  enumeration as the published entries → same 92 shapes; the m=11 z=20 row is
  NOT re-swept: its K1322 band was closed by the published z20 probe kit),
  strip spots m∈{20..23}, the m=15 base spot (cross-checked against the
  published z20 probe value), the below-band bottom-rung child census
  `H(21;Y;21)` vs `v(s,21,21)`, and section (g): the ELEVENTH-tail supply
  identity RECHECK `v(s,21,21)` vs `v(s,20,21)` (published by the z19 census +
  z20 probe kits; rechecked and extended over s∈{0}∪{12..57}), the TWELFTH-tail
  supply identity RECHECK `v(s,22,22)` vs `v(s,21,22)` (published by the z20
  probe kit; rechecked over the same extended domain), plus the NEW
  engine-free THIRTEENTH-tail supply pre-computation `v(s,23,23)` vs
  `v(s,22,23)`. Per-cell `H.cache_clear()` retained (z=13 shared-cache OOM
  lesson).
- `explore_z20f15.out` — sha256
  `09e9026a436bf25aed05eabaf3629975971bd320a4c4c5ce5da122239f19f789`
  (the frozen stdout; deterministic — FIVE runs: default, default re-run,
  PYTHONHASHSEED=1 same cwd and env -i isolated dirs ×2, all byte-identical,
  rc 0, ~21 s per run; no randomness, no wall-clock, no hash-order
  dependence).

## What the census recorded (observation, judgment-free; see the predecl log)

- 14 floor-15 cells at z=20 (`Cell_j(s) := H(j+21;{j}∪Y;20)`, Y tokens >= 15):
  ALL cells s-only (multivalue rows 0) over 105 shapes each
  (s ∈ {0}∪{15..45}, arity 0..4). Deviant structure — the deviant position
  set is **{16, 18, 20}**: the position-14 classes of the published z=19
  census fall BELOW floor 15 = **the 4th recorded definition-domain exclusion**
  (after the s=12 exclusion at z=17→18; the z=19 shift excluded nothing).
  Candidate law observation (3 consecutive pairs): the deviant position set is
  shared by z=16/z=17 ({12,14,16}) and z=18/z=19 ({14,16,18}), and each even
  step shifts it +2 — the z=20 set {16,18,20} is the +2 shift of z=18's
  {14,16,18}, leapfrogging nothing.
  - **F {s=20 UP:1 (collapse 0), single point, no hole, no tail}** — the
    F-family ELEVENTH tail typology = **SINGLE POINT at s=z**: the even-z
    single-point form is now 3/3 even slices (z=16 s=16, z=18 s=18, z=20
    s=20) and the single@(even z)/hole+tail@(odd z) typology alternation has
    **SIX consecutive consistent slices (z15..z20)**. Tail spots
    s∈{46..53}: **112/112 match** (z=19 showed the persistent tail piercing
    the census window 8/8; at even z there is no tail to pierce — the 0/112
    mismatch count is itself the even-form signature).
  - G {s=18 DOWN:0 (collapse 2), s=20 UP:2 (collapse 1)};
    E {s=18 UP:1 (collapse 0)};
    D {s=16 DOWN:0 (collapse 2), s=18 UP:2 (collapse 1)};
    C {s=16 UP:1 (collapse 0)};
    B {s=16 UP:2 (collapse 1)};
    A..A8: fully collapsed — **EIGHT consecutive full collapses, the longest
    A-family collapse run of the series**. The z=19 A-rank deviant at
    s=14=z−5 is floor-excluded (14 < 15); parity note (observation): at even
    z the A-break position z−5 is ODD and every deviant class ever observed
    in the series sits at even s — an A-break at even z would require an
    odd-s deviant class, none has ever been observed (the z=17/z=19 A-breaks
    at s=z−5 even are consistent; z=21 predicts s=16=z−5).
  - The ladder carries the even-z station triplet **{DOWN:0, UP:1, UP:2}**
    at three positions: {D,C,B}@16, {G,E,D}@18, {F,G}@20 — the EXACT z=18
    station pattern (z=18: {D,C,B}@14, {G,E,D}@16, {F,G}@18), +2 in
    position, with the same rank heads D(j=4), G(j=2), F(j=1). The newest
    even-z station form is now 2/2 (z=18, z=20).
  - **A820f15 (j=14, min=14, z*(14)=26 > 20) fully collapsed over its
    105-shape domain — the SIXTH consecutive in-band base child** = the
    T-Z20 base-m=15 trivial-absorption candidate.
- Strip sweep at the provisional T-Z20 claim position m∈{15..19}:
  **185 shapes, 0 violations** (cumulative 55/99/134/162/185).
- m=14-row z=20 record (R=35; K1330 residual band FIRST entry; published
  style): **62 shapes, 0 separations**; arity<=4 co-token extension:
  **61 shapes, 0 separations**.
- m=13-row z=20 record (R=34; K1328 residual band SECOND entry):
  **76 shapes, 0 separations** — exactly the published z20 probe values
  (cross-artifact shape-for-shape consistency machine-checked).
- m=12-row z=20 record (R=33; K1325 residual band THIRD entry):
  **92 shapes, 0 separations** — exactly the published entries.
- Strip spots m∈{20..23}: **12/12 match**.
- m=15 base spot `H(36;(15,15);20)` = **0** = `v(30,20,36)` — exactly the
  published z20 probe value; the cross-floor base-spot z-parity sequence is
  now **0 (z16), 1 (z17), 0 (z18), 1 (z19), 0 (z20)** — five data points.
- Below-band child census `H(21;Y;21)` vs `v(s,21,21)`: 105 shapes,
  **0 deviants, 0 multivalue — SIXTH consecutive full collapse** of the
  below-band supply child.
- ELEVENTH-tail identity recheck: `v(s,21,21)=v(s,20,21)` holds exactly on
  **{0}∪{12..19}**, breaks at s=20 as 0v2, then uniformly 2v1 for all
  s∈{21..57} (published domain {12..56} rechecked + extended by one).
- TWELFTH-tail identity recheck: `v(s,22,22)=v(s,21,22)` holds exactly on
  **{0}∪{12..21}**, uniform 0v1 break for all s∈{22..57} (published z20
  probe values reproduced).
- **THIRTEENTH-tail identity (NEW)**: `v(s,23,23)=v(s,22,23)` holds exactly
  on **{0}∪{12..21}**, breaks at **s=22 as 0v2**, then **uniformly 2v1 for
  all s∈{23..57}** — the predeclared candidate (break start s=22 AND shape
  0v2@z + uniform 2v1@(z+1)+) is **CONFIRMED on both components**; the
  newest even-z supply-identity form is now 3/3 (z=18, z=20, z=22 supply).
  This is the z=22 slice's supply datum.

## Independent ordered-engine cross-check (outside the frozen artifact)

The FULL census re-enumerated and re-evaluated with `H_ordered` against the
frozen canonical-engine output: 1,470 cell shapes (14 cells × 105), 112 tail
spots, 185 strip shapes, 62+61+76+92 record shapes, 12 strip spots, the base
spot, 105 below-band shapes, and all identity hold/break rows: **0
mismatches**; every frozen row (deviant lists, multivalue counts, shape
counts, separation lists, tail-spot rows, identity rows) reproduced exactly.
Per-record `H.cache_clear()` (published OOM lesson).

See `research/log/2026-11-25-z20m15-predecl-exploration.md` for the
primary-source timeline, honest disclosure and handoff instructions.

## Standard caveats

Everything in this kit is a FINITE machine observation against the pinned raw
engine. Nothing here is a theorem, nothing universal is claimed, and no verdict
of any game position (11x11 standard board, two-stone roots, S2, class 1/2/4 —
all UNKNOWN) is consumed. Battery/point counts are engine cross-checks, not
proofs. The paper proofs, the slot claim and the verification machine belong to
the declaration lane. Section (g) is a pure closed-form pre-computation: it uses
no engine recursion at all and inherits only the published K0832 single-token
closed form.
