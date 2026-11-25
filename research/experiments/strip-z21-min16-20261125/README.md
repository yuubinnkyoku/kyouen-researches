# z21-min16 pre-declaration exploration kit (frozen)

This directory is the publish-then-execute PRIMARY RECORD for the pre-declaration
census of the z=21 min>=16 (floor-16) slice — the next slice of the vertical-fiber
strip series after the z20-min15 census kit (`2cc16d34`). No K slot is claimed
by this kit and no claim is made here: everything below is machine observation.
The declaration lane (a later run) picks up the slot claim, the paper proof, the
verification machine and the official runs.

## Contents

- `engine_block.py` — sha256 `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`
  (the pinned engine block, byte-identical to the K1282..K1330 chain; sha256 of the
  embedded block itself is the startup pin `bd5f22e4…`).
- `explore_z21f16.py` — sha256
  `edb31ad07c83f43cf742a3cf3b139edbe16f9c797d6ce606f475010d624c1a81`
  (adapted from the frozen published `explore_z20f15.py`
  `d46483016507bbc6e99d778baa528a053e57b325ded3d236564355eee13a2897` by the
  disclosed textual diff: z 20→21, cell budget j+21→j+22, floor 15→16, rungs
  14→15 with the provisional 15th-rank label `A9` (small token 15 — the SEVENTH
  consecutive in-band base child; z*(15)=29 > 21), s domain {0}∪{16..46},
  tail spots {47..54}, strip m∈{16..20} at the provisional T-Z21 claim
  position, an IN-BAND m=15-row record at z=21 (R=37, the T-Z21 base-child
  position AND the CANDIDATE FIRST entry of the future T-Z20 residual band
  m=15 z∈{21..28}, frontier z=29; published residual-band style arity<=3
  TOTAL, plus an arity<=4 co-token extension sweep), an IN-BAND m=14-row
  record at z=21 (R=36, the SECOND entry of the K1330 published residual band
  m=14 z∈{20..25}; SAME enumeration as the published z=20 census entry → same
  62 shapes, cross-artifact consistency), an IN-BAND m=13-row record at z=21
  (R=35, the THIRD entry of the K1328 published residual band m=13 z∈{19..24};
  same 76 shapes), an IN-BAND m=12-row record at z=21 (R=34, the FOURTH AND
  FINAL entry of the K1325 published residual band m=12 z∈{18..21} — the band
  CLOSES at this entry; same 92 shapes), strip spots m∈{21..24}, the m=16
  base spot (never measured by any published kit; candidate 1 from the
  base-spot z-parity sequence), the below-band bottom-rung child census
  `H(22;Y;22)` vs `v(s,22,22)`, and section (g): the TWELFTH-tail supply
  identity RECHECK `v(s,22,22)` vs `v(s,21,22)` (published by the z20 probe +
  z20 census kits; the z=21 F-cell supply datum; rechecked and extended over
  s∈{0}∪{12..58}), the THIRTEENTH-tail supply identity RECHECK
  `v(s,23,23)` vs `v(s,22,23)` (published by the z20 census kit; rechecked
  extended), plus the NEW engine-free FOURTEENTH-tail supply pre-computation
  `v(s,24,24)` vs `v(s,23,24)` with BOTH break components predeclared. The
  FULL predeclared deviant-profile candidate (derived from the published z=19
  odd profile `6a6832ce` shifted +2) is in the file docstring, written before
  the first run. Per-cell `H.cache_clear()` retained (z=13 shared-cache OOM
  lesson).
- `explore_z21f16.out` — sha256
  `10f94100eb6240a807a32ac5d0e91f532800f86320a64d40e3ae47891dd2f643`
  (the frozen stdout; deterministic — SIX runs: default ×3, PYTHONHASHSEED=1
  same-cwd, env -i isolated dirs ×2, all byte-identical, rc 0, ~22 s per
  run; no randomness, no wall-clock, no hash-order dependence).

## What the census recorded (observation, judgment-free; see the predecl log)

- 15 floor-16 cells at z=21 (`Cell_j(s) := H(j+22;{j}∪Y;21)`, Y tokens >= 16):
  ALL cells s-only (multivalue rows 0) over 96 shapes each
  (s ∈ {0}∪{16..46}, arity 0..4). Deviant structure — the deviant position
  set is **{16, 18, 20}, INHERITED from z=20 exactly as predeclared** (the
  (even, following-odd) pair rule is now **3/3 pairs**: {12,14,16} shared by
  z16/z17, {14,16,18} by z18/z19, {16,18,20} by z20/z21; no shift, no new
  exclusion at the odd step).
  - **A21f16 {s=16 UP:2 (collapse 0)} — the A-RANK BREAK REBIRTH at s=16=z−5,
    exactly the predeclared parity-law candidate**. The A-break series is now
    **3/3 odd slices** (z=17 s=12, z=19 s=14, z=21 s=16, ALL UP 2v0), and the
    even-z exclusion mechanism (position z−5 odd at even z; no odd-s deviant
    class ever observed) is now 4/4 even slices (z=16..z=20 A..A8 all
    collapsed). The z=20 kit §5 prediction is CONFIRMED.
  - The odd-z station triplet **{DOWN:1, DOWN:0, UP:2}** at the predeclared
    positions: **{C,B,A}@16** (C DOWN:1v2, B DOWN:0v1, A UP:2v0), **{E,D}@18**
    (E DOWN:1v2, D DOWN:0v1), **{F,G,E}@20** (F DOWN:1v2, G DOWN:0v1,
    E UP:2v0) — the EXACT +2 shift of the published z=19 profile
    ({C,B,A}@14, {E,D}@16, {F,G,E}@18), same rank heads. The odd-z station
    form is now 3/3 (z=17, z=19, z=21) — the z=17 leg VERIFIED against the
    published z17-min12 kit (`2c74f1c6`: {C,B,A}@12 with C DOWN:1v2 /
    B DOWN:0v1 / A UP:2v0, {E,D}@14, {F,G,E}@16, F hole@17 + tail 2v0
    from s=18 — identical rank heads and constants to z=19/z=21).
  - **C21f16 carries a second deviant {s=18 UP:2 (collapse 0)}** — this class
    was NOT spelled out in the docstring's station enumeration (predeclaration
    text incomplete by one class; disclosed in the log): it is the exact +2
    shift of the published z=19 C-cell second deviant (C19f14 UP:2v0@16), so
    the measured profile is the complete +2 shift of the published z=19
    per-cell deviant list, class for class.
  - **F {s=20 DOWN:1 (collapse 2); s=21 conforming (the HOLE); tail
    s∈{22..46} UP:2v0}** — the TWELFTH-tail hole+tail form exactly as
    predeclared: DOWN at z−1, hole at z (the final hold position of the
    twelfth-tail supply identity), persistent tail 2v0 from z+1. The
    single@(even z)/hole+tail@(odd z) typology alternation has **SEVEN
    consecutive consistent slices (z15..z21)**. Tail spots s∈{47..54}:
    **F 8/8 mismatch, all other cells 112/112 match** (the odd-form
    signature, contrast z=20's 112/112 match).
  - A2..A9: fully collapsed — EIGHT consecutive full collapses past the
    A-boundary rung, matching the z=19 pattern (A2..A7).
  - **A921f16 (j=15, min=15, z*(15)=29 > 21) fully collapsed over its
    96-shape domain — the SEVENTH consecutive in-band base child** = the
    T-Z21 base-m=16 trivial-absorption candidate.
- Strip sweep at the provisional T-Z21 claim position m∈{16..20}:
  **150 shapes, 0 violations** (cumulative 44/79/107/130/150).
- m=15-row z=21 record (R=37; SEVENTH consecutive base child; candidate FIRST
  entry of the future T-Z20 residual band m=15 z∈{21..28}): **50 shapes,
  0 separations**; arity<=4 co-token extension: **49 shapes, 0 separations**.
- m=14-row z=21 record (R=36; K1330 residual band SECOND entry):
  **62 shapes, 0 separations** — exactly the published z20 census count
  (cross-artifact shape-for-shape consistency machine-checked).
- m=13-row z=21 record (R=35; K1328 residual band THIRD entry):
  **76 shapes, 0 separations** — exactly the published entries.
- m=12-row z=21 record (R=34; K1325 residual band FOURTH AND FINAL entry):
  **92 shapes, 0 separations** — the published m=12 residual band
  z∈{18..21} **CLOSES** (frontier z*(12)=22).
- Strip spots m∈{21..24}: **12/12 match**.
- m=16 base spot `H(38;(16,16);21)` = **1** = `v(32,21,38)` — the predeclared
  candidate value; the base-spot z-parity sequence is now
  **0 (z16), 1 (z17), 0 (z18), 1 (z19), 0 (z20), 1 (z21)** — six data points.
- Below-band child census `H(22;Y;22)` vs `v(s,22,22)`: 96 shapes,
  **0 deviants, 0 multivalue — SEVENTH consecutive full collapse** of the
  below-band supply child.
- TWELFTH-tail identity recheck: `v(s,22,22)=v(s,21,22)` holds exactly on
  **{0}∪{12..21}**, uniform 0v1 break for all s∈{22..58} (published domain
  {12..57} rechecked + extended by one). Final hold s=21 = the F hole; first
  break s=22 = the tail start: supply-to-deviant alignment exact.
- THIRTEENTH-tail identity recheck: `v(s,23,23)=v(s,22,23)` holds exactly on
  **{0}∪{12..21}**, breaks at s=22 as 0v2, then uniformly 2v1 for all
  s∈{23..58} (published z20 census values reproduced, extended).
- **FOURTEENTH-tail identity (NEW)**: `v(s,24,24)=v(s,23,24)` holds exactly on **{0}∪{12..23}**, breaks at
  **s=24 as 0v1**, then **uniformly 0v1 for all s∈{24..58}** — BOTH
  predeclared components (break start s=24=z+1 AND uniform 0v1 shape)
  **CONFIRMED**; the odd-z supply-identity form is now **3/3** (z=19, z=21,
  z=23-supply) — the first odd-slice fully-predeclared-and-confirmed
  identity. This is the z=23 slice's supply datum.

## Independent ordered-engine cross-check (outside the frozen artifact)

The FULL census re-enumerated and re-evaluated with `H_ordered` against the
frozen canonical-engine output: 1,440 cell shapes (15 cells × 96), 120 tail
spots, 150 strip shapes, 50+49+62+76+92 record shapes, 12 strip spots, the
base spot, 96 below-band shapes, and ALL identity hold/break rows compared as
full rows (values included, stronger than the z20 xcheck): **0 mismatches**;
every frozen row reproduced exactly. Per-record `H.cache_clear()`
(published OOM lesson).

See `research/log/2026-11-25-z21m16-predecl-exploration.md` for the
primary-source timeline, honest disclosure (including the one predeclaration
text gap) and handoff instructions.

## Standard caveats

Everything in this kit is a FINITE machine observation against the pinned raw
engine. Nothing here is a theorem, nothing universal is claimed, and no verdict
of any game position (11x11 standard board, two-stone roots, S2, class 1/2/4 —
all UNKNOWN) is consumed. Battery/point counts are engine cross-checks, not
proofs. The paper proofs, the slot claim and the verification machine belong
to the declaration lane. Section (g) is a pure closed-form pre-computation: it
uses no engine recursion at all and inherits only the published K0832
single-token closed form.
