# z17-min12 pre-declaration exploration kit (frozen)

This directory is the publish-then-execute PRIMARY RECORD for the pre-declaration
census of the z=17 min>=12 (floor-12) slice — the next slice of the vertical-fiber
strip series after the K1322 (T-Z16) completion. No K slot is claimed by this kit
and no claim is made here: everything below is machine observation. The declaration
lane (a later run) picks up the slot claim, the paper proof, the verification
machine and the official runs.

## Contents

- `engine_block.py` — sha256 `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`
  (the pinned engine block, byte-identical to the K1282..K1322 chain; sha256 of the
  embedded block itself is the startup pin `bd5f22e4…`).
- `explore_z17m12.py` — sha256
  `410fea310b00da6733e6d336fa6b275890307ad16e6603683fc1f4500bdef7b0`
  (adapted from the frozen published `explore_z16pre.py`
  `87f3bb71a28908038646fc67d0d40fb93b2c775f73f184407e444f31f2ab4b0e` by the
  disclosed textual diff: z 16→17, cell budget j+17→j+18, floor 11→12, rungs
  10→11 with the provisional 11th-rank label `A5` (small token 11 — the THIRD
  consecutive in-band base child; z*(11)=21 > 17), s domain {0}∪{12..42},
  strip m∈{12..16} at the provisional T-Z17 claim position, an IN-BAND
  m=11-row record at z=17 (R=29, the T-Z17 base-child position AND the FIRST
  entry of the K1322 published residual band m=11 z∈{17..20}), a NEW IN-BAND
  m=10-row record at z=17 (R=28, the second and last entry of the K1320
  published residual band m=10 z∈{16,17}; the z=16 entry was measured by the
  published z16-min11 kit), a NEW m=8-row beyond record in the EXACT published
  z=16 362-shape enumeration form (S∈{8..47}, X=(8,)∪parts(S−8,8,3)) for
  position-by-position cross-slice comparability, strip spots m∈{17..20},
  the m=12 base spot, and the below-band bottom-rung child census
  `H(18;Y;18)` vs `v(s,18,18)`. Per-cell `H.cache_clear()` retained
  (z=13 shared-cache OOM lesson).
- `explore_z17m12.out` — sha256
  `f3579f0d0502e742de6503ee742af1c09a08cd3e62d4bd8fcabf5161d82054b6`
  (the frozen stdout; deterministic — three runs with default,
  PYTHONHASHSEED=random same cwd and env -i isolated dir all byte-identical,
  rc 0, ~19.5 s per run; no randomness, no wall-clock, no hash-order
  dependence).

## What the census recorded (observation, judgment-free; see the predecl log)

- 11 floor-12 cells at z=17 (`Cell_j(s) := H(j+18;{j}∪Y;17)`, Y tokens >= 12):
  ALL cells s-only (multivalue rows 0) over 155 shapes each
  (s ∈ {0}∪{12..42}, arity 0..4). Deviant structure:
  **F {s=16 DOWN:1 (collapse 2), HOLE s=17, CONSTANT-2 UP TAIL for ALL s>=18
  (26 s-values, shapes 1..18, value 2 vs collapse 0)}** — the F-family EIGHTH
  tail typology: the persistent 2-tail REBORN one slice after the z=16
  single-point seventh form, with the SAME s-profile as the z=15 sixth form
  (DOWN@(z−1), hole@z, tail@(z+1)) shifted by +2 (F15f10: 14/15/16 ->
  F17f12: 16/17/18); **G {s=16 DOWN:0} only** (loses its published z=16 UP:2
  partner); **E {s=14 DOWN:1, s=16 UP:2}**; **D {s=14 DOWN:0}** (loses its
  z=16 s=12 deviant); **C {s=12 DOWN:1, s=14 UP:2}** (new s=14 UP:2);
  **B {s=12 DOWN:0}** (z=16's s=12 UP:2 flipped DOWN); **A {s=12 UP:2}** —
  the A-RANK BREAKS the z=16 four-rung collapse run (A16f11 fully collapsed;
  the first floor-12 deviant sits at the FIRST A-rank, a structurally new
  ladder head); **A2/A3/A4/A5 NONE (four consecutive full collapses)** —
  A5 (j=11, min=11) is the THIRD consecutive in-band base child and it fully
  collapses over its cell domain (Y tokens >= 12); the "UP:2 climbs by
  rungs" chain A@12 -> C@14 -> E@16 -> F-tail(s>=18) and the interleaved
  DOWN chain B@12 -> C@12/D@14 -> E@14/F@16/G@16 are the two supply
  structures the declaration lane must derive.
- NO death-point event: all three published z=16 (K1322) source positions
  {12, 14, 16} are >= floor 12 and ALL SURVIVE, exactly as the floor
  criterion predicts (death events remain: z=13->z=14's s=8 branch and
  z=15->z=16's s=10 branch only). The deviant restructuring ACROSS ranks is
  nevertheless substantial (B flips UP->DOWN, C gains an UP:2 partner, D and
  G lose one deviant, A gains one, F rebuilds a persistent tail).
- F tail spots s∈{43..50}: **8/8 MISMATCH, all F (value 2 vs collapse 0)** —
  the persistent F tail is confirmed OUTSIDE the census domain too (the
  other 80 tail spots match; 88 rows total). The z=16 kit had 0 tail
  mismatches, so a persistent F tail returns to this series for the first
  time since z=15's F15f10 (sixth form).
- Below-band bottom-rung child census: `H(18;Y;18)` = `v(s,18,18)` for ALL
  155 floor-12 shapes (0 deviants, 0 multivalue) — the THIRD consecutive full
  collapse of the below-band supply child (z=15: lemma BB, z=16: published
  183-shape collapse), itself the leading candidate supply source for the
  rebuilt F tail; the exact absorption-identity break belongs to the
  declaration lane.
- Provisional T-Z17 claim position (m∈{12..16}, arity<=3, parts>=m):
  **358 shapes, 0 violations** (cumulative per m: 12→107, 13→191, 14→259,
  15→314, 16→358).
- IN-BAND m=11-row record at z=17 (R=29, parts >= 11 INCLUDING co-token 11
  shapes, arity<=3, S∈{11..49}): **110 shapes, 0 separations** — the FIRST
  affirmative data for the K1322 published residual band (m=11, z∈{17..20});
  together with A517f12's full cell collapse this fixes the T-Z17 base m=12
  as the THIRD consecutive trivial-absorption base.
- IN-BAND m=10-row record at z=17 (R=28, parts >= 10, arity<=3,
  S∈{10..48}): **130 shapes, 0 separations** — COMPLETES the K1320 published
  residual band m=10 z∈{16,17} with BOTH entries 0 (z=16: 130/0 by the
  published z16-min11 kit) — a candidate m=10-row closure lemma for a
  separate declaration lane; observational only here.
- m=8-row z=17 BEYOND record (362 shapes, the EXACT published enumeration
  form; z*(8)=14, third slice beyond): **EXACTLY 1 separation: X=(8,10)
  DOWN:0 (collapse 1) at S=18** — the published z=16 set was {(8,8) DOWN 0v2,
  (8,10) UP 2v1}. So the (8,8) separation is RESORBED into the collapse and
  (8,10) FLIPS UP->DOWN. The beyond separation set sequence is now
  {(8,8)UP} (z=14) -> {(8,8)DOWN} (z=15) -> {(8,8)DOWN,(8,10)UP} (z=16) ->
  {(8,10)DOWN} (z=17): the z=16 "beyond separation set GROWS with z"
  observation is REFUTED at z=17 by the first SHRINK event; the growth rule
  is replaced by an alternating flip/reabsorb structure. Observational only.
- Strip spots m∈{17..20}: 12/12 match. m=12 base spot H(30;(12,12);17)=1=
  v(24,17,30) (the z=16 m=11 base spot analog was 0).

See `research/log/2026-11-25-z17m12-predecl-exploration.md` for the
primary-source timeline, honest disclosure and handoff instructions.

## Standard caveats

Everything in this kit is a FINITE machine observation against the pinned raw
engine. Nothing here is a theorem, nothing universal is claimed, and no verdict
of any game position (11x11 standard board, two-stone roots, S2, class 1/2/4 —
all UNKNOWN) is consumed. Battery/point counts are engine cross-checks, not
proofs. The paper proofs, the slot claim and the verification machine belong to
the declaration lane.
