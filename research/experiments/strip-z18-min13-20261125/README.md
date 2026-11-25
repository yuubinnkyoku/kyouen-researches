# z18-min13 pre-declaration exploration kit (frozen)

This directory is the publish-then-execute PRIMARY RECORD for the pre-declaration
census of the z=18 min>=13 (floor-13) slice — the next slice of the vertical-fiber
strip series after the K1325 (T-Z17) completion. No K slot is claimed by this kit
and no claim is made here: everything below is machine observation. The
declaration lane (a later run) picks up the slot claim, the paper proof, the
verification machine and the official runs.

## Contents

- `engine_block.py` — sha256 `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`
  (the pinned engine block, byte-identical to the K1282..K1325 chain; sha256 of the
  embedded block itself is the startup pin `bd5f22e4…`).
- `explore_z18f13.py` — sha256
  `152fd2d8814f958e5aaef275f83b4abb1763b58929d375d7ec9cb864f2a94ff4`
  (adapted from the frozen published `explore_z17m12.py`
  `410fea310b00da6733e6d336fa6b275890307ad16e6603683fc1f4500bdef7b0` by the
  disclosed textual diff: z 17→18, cell budget j+18→j+19, floor 12→13, rungs
  11→12 with the provisional 12th-rank label `A6` (small token 12 — the FOURTH
  consecutive in-band base child; z*(12)=22 > 18), s domain {0}∪{13..43},
  strip m∈{13..17} at the provisional T-Z18 claim position, an IN-BAND
  m=12-row record at z=18 (R=31, the T-Z18 base-child position AND the FIRST
  entry of the K1325 published residual band m=12 z∈{18..21}; published
  residual-band style arity<=3 TOTAL, plus an arity<=4 co-token extension
  sweep), an IN-BAND m=11-row record at z=18 (R=30, the SECOND entry of the
  K1322 published residual band m=11 z∈{17..20}; SAME enumeration as the
  published z=17 entry → same 110 shapes), a NEW m=10-row z=18 FRONTIER
  record (z=18 = z*(10), the first even-m frontier data point of the
  series; published frontier style, 170 shapes), a m=9-row z=18
  beyond-frontier record (arithmetic form IDENTICAL to the published
  z=17 m=9 frontier record → same 234 shapes), a m=8-row z=18 beyond
  record in the EXACT published 362-shape enumeration form
  (S∈{8..47}, X=(8,)∪parts(S−8,8,3)) for position-by-position cross-slice
  comparability, strip spots m∈{18..21}, the m=13 base spot, the below-band
  bottom-rung child census `H(19;Y;19)` vs `v(s,19,19)`, and the NEW
  engine-free NINTH-TAIL SUPPLY PRE-COMPUTATION section (g): the pure
  K0832 closed-form comparison `v(s,19,19)` vs `v(s,18,19)` over
  s∈{0}∪{12..55} together with a recheck of the published z=17 supply
  identity `v(s,18,18)` vs `v(s,17,18)`. Per-cell `H.cache_clear()` retained
  (z=13 shared-cache OOM lesson).
- `explore_z18f13.out` — sha256
  `c4e7757c587883bb41b0f297de336128cd6bafc55865ba10673b28c7338d0b0b`
  (the frozen stdout; deterministic — FIVE runs: default, PYTHONHASHSEED=1
  same cwd and env -i isolated dirs ×2, all byte-identical, rc 0, ~23.7 s
  per run; no randomness, no wall-clock, no hash-order dependence).

## What the census recorded (observation, judgment-free; see the predecl log)

- 12 floor-13 cells at z=18 (`Cell_j(s) := H(j+19;{j}∪Y;18)`, Y tokens >= 13):
  ALL cells s-only (multivalue rows 0) over 133 shapes each
  (s ∈ {0}∪{13..43}, arity 0..4). Deviant structure — the whole deviant
  position set is **{14, 16, 18}**, a clean +2 SHIFT of the z=17 set
  {12,14,16} (the z=17 s=12 classes A/B/C fell below floor 13 — the
  third recorded instance of the definition-domain-exclusion mechanism,
  NOT a class death):
  **F {s=18 UP:1 (collapse 0), SINGLE POINT, no hole, NO persistent tail}**
  — the F-family NINTH tail typology: after the z=17 hole-plus-tail
  eighth form the persistent tail RE-COLLAPSES to a single point, giving
  the typology alternation single@(even z) / hole+tail@(odd z) a FOURTH
  consistent data point (z=16 single, z=17 hole+tail, z=18 single, plus
  z=15 hole+tail); **G {s=16 DOWN:0 (collapse 2), s=18 UP:2 (collapse 1)}**;
  **E {s=16 UP:1 (collapse 0)}**; **D {s=14 DOWN:0 (collapse 2), s=16
  UP:2 (collapse 1)}**; **C {s=14 UP:1 (collapse 0)}**; **B {s=14 UP:2
  (collapse 1)}** — B flips from the z=17 DOWN carrier to an UP:2 carrier
  one position up; **A..A6 NONE (SIX consecutive full collapses)** — the
  z=17 A-rank break (A17f12 {12 UP:2}) did NOT survive the floor shift:
  its s=12 position is domain-excluded at floor 13 and the A-family
  collapse run restarts at SIX rungs, the longest of the series; A6
  (j=12, min=12) is the FOURTH consecutive in-band base child and it fully
  collapses over its cell domain (Y tokens >= 13) — the T-Z18 base m=13
  trivial-absorption candidate. Per-position triplets: position 14 carries
  {D DOWN:0, C UP:1, B UP:2} and position 16 carries {G DOWN:0, E UP:1,
  D UP:2} — the z=17 two-supply-chain picture generalizes to a repeating
  DOWN:0 / UP:1 / UP:2 triplet climbing s=14 → s=16 → s=18; position 18
  carries only {F UP:1, G UP:2} (its DOWN:0 slot is EMPTY: no cell maps a
  0-vs-2 deviant at s=18).
- Tail spots s∈{44..51}, all 12 cells: **96 rows, 0 mismatches** — no cell
  carries deviant structure beyond the census window (contrast z=17:
  8/8 F mismatches from the persistent eighth-form tail). The
  single-point ninth form is window-external too.
- Below-band bottom-rung child census: `H(19;Y;19)` = `v(s,19,19)` for ALL
  133 floor-13 shapes (0 deviants, 0 multivalue) — the FOURTH consecutive
  full collapse of the below-band supply child.
- **NINTH-TAIL SUPPLY PRE-COMPUTATION (engine-free, section g)**: the naive
  +2-shift extrapolation of the supply identity predicts hold on
  {0}∪{13..19} with a uniform 1-vs-0 break for s>=20. MEASURED (pure
  K0832 closed form): the identity `v(s,19,19)=v(s,18,19)` HOLDS exactly on
  **{0}∪{12..17}**, BREAKS at **s=18 as 0-vs-2** and breaks for ALL
  s>=19 uniformly as **2-vs-1** — the naive prediction is CONTRADICTED on
  both the break start (s=18, two positions EARLY) and the constants
  (0v2/2v1, never 1v0). The published z=17 partner identity
  `v(s,18,18)=v(s,17,18)` is RECHECKED in the same loop and reproduces the
  published statement's substance exactly: hold on {0}∪{12..17}, uniform
  break for all s>=18 with measured constants, in identity order,
  v(s,18,18)=0 vs v(s,17,18)=1 over the whole break range s∈{18..55}
  (the published K1325 summary names the break constants "1 vs 0"; the
  orientation of that pair in the published note is not restated here —
  the raw values are in the .out for the declaration lane to match). The F18f13 single-point deviant sits EXACTLY at the
  identity's first break position (s=18); the s>=19 uniform 2v1 break
  produces NO F deviants at all (F matches the collapse there) — the
  supply-to-deviant mapping of the z=18 slice is qualitative new
  structure for the declaration lane.
- Provisional T-Z18 claim position (m∈{13..17}, arity<=3, parts>=m):
  **286 shapes, 0 violations** (cumulative per m: 13→84, 14→152, 15→207,
  16→251, 17→286).
- IN-BAND m=12-row record at z=18 (R=31, parts >= 12 INCLUDING co-token 12
  shapes, arity<=3 TOTAL, S∈{12..50}): **92 shapes, 0 separations** — the
  FIRST affirmative data for the K1325 published residual band (m=12,
  z∈{18..21}); the arity<=4 extension sweep: **95 shapes, 0 separations**;
  together with A618f13's full cell collapse this fixes the T-Z18 base
  m=13 as the FOURTH consecutive trivial-absorption base candidate.
- IN-BAND m=11-row record at z=18 (R=30, published residual-band style,
  SAME enumeration as the z=17 entry): **110 shapes, 0 separations** — the
  SECOND entry of the K1322 published residual band m=11 z∈{17..20}.
- **m=10-row z=18 FRONTIER record (z=18 = z*(10); NEW data)**: 170 shapes
  (published frontier style), **EXACTLY 1 separation: X=(10,10) S=20
  UP:2 (collapse 1)** — the DIAGONAL spot. With the published m=8 z=14
  frontier (diagonal (8,8)) and the m=9 z=17 frontier
  (off-diagonal (9,10)), the frontier structure now shows even-m →
  diagonal (m,m), odd-m → (m,m+1): a 2/2 candidate parity regularity
  for the frontier separation shape. Observational only.
- m=9-row z=18 BEYOND-frontier record (234 shapes, the IDENTICAL published
  enumeration; z*(9)=17, second odd-m beyond data point): **EXACTLY 1
  separation: X=(10,9) S=19 UP:1 (collapse 0)** — the SAME (9,10) position
  as the z=17 frontier separation (which was UP:2, collapse 0):
  persistence WITHOUT reabsorption, with the value DECAYING 2→1 one
  slice beyond the frontier. Contrast: the m=8 (8,8) separation
  re-absorbed between z=15 and z=16 while (8,10) flipped; odd-m frontier
  separations so far PERSIST at fixed position.
- m=8-row z=18 BEYOND record (362 shapes, the EXACT published
  enumeration; z*(8)=14, fourth consecutive beyond data point):
  **0 separations** — the beyond separation set becomes EMPTY for the
  first time in the series: sequence {(8,8)UP}@z14 → {(8,8)DOWN}@z15 →
  {(8,8)DOWN,(8,10)UP}@z16 → {(8,10)DOWN}@z17 → {}@z18. The (8,10)
  separation now re-absorbs exactly two slices after (8,8) did — the
  flip/reabsorb alternation continues with a 2-slice lag per position;
  the z=17 SHRINK event is confirmed as the precursor of total
  reabsorption. Observational only.
- Strip spots m∈{18..21}: 12/12 match. m=13 base spot H(32;(13,13);18)=0=
  v(26,18,32) — the base-spot sequence across floors reads 0 (z=16, m=11),
  1 (z=17, m=12), 0 (z=18, m=13): a z-parity alternation candidate
  (observation, 3 data points).

See `research/log/2026-11-25-z18m13-predecl-exploration.md` for the
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

## Verification machine (added post-declaration, 2026-11-25)

The declaration lane published the slot-claim + declaration note
(`research/log/2026-11-25-strip-z18-min13-single-owner-note.md`,
commits 71c66058 + name-repair b94835e0, sha256 693829551b5db06e3eb99be83c77c9eb761288a2fa183739fc6e4aaaa90ed77a)
with the full paper proof pre-disclosed (publish-then-execute), and this
verification machine completes the kit:

- `verify_k1328.py` (sha256 pinned here in the commit message; structural
  copy of the published verify_k1325.py z=17 machine with the disclosed
  z 17→18 textual adaptation disclosed in the machine docstring: 12 rungs,
  floor 13, R budget j+19, D3 anchor set = the z=17 line transcriptions
  + T-Z17 C-hand anchors, D5 z-grid extended to z=19, battery
  re-declared). Embedded engine block byte-identical chain, startup pin
  bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92 (sha
  gate, rc 2 on mismatch). NOTE: the declared provisional number in the
  earliest draft was K1326; the conic lane published K1326/K1327 (pg2q8
  cap-orbit items) in the interim, so the declaration renumbered to
  K1328 per AGENTS.md; no competing T-Z18 declaration ever appeared.

Battery (fail-closed, declared totals exact or FAIL): D1 cells 1,596 =
12 cells x 133 exhaustive floor-13 shapes (s ∈ {0}∪{13..43}, arity 0..4);
D2 strip 286 (m ∈ {13..17}, cumulative 84/152/207/251/286 — identical
sweep to kit section (c)); D3 z17 anchors 382 (11 transcribed K1325 lines
x 32 s-values = 352 + 30 T-Z17 C-hand anchors m ∈ {12..17});
D4 stair anchors 372 (12 x 31, s ∈ {13..43}); D5 self anchors 12,780
(x ∈ {1..30} x z ∈ {0..19} x 21 R-points = 12,600 + 180 empty positions);
D6 deviant/collapse witnesses 22; D7 extension anchors 109 (tail spots
s ∈ {44..51} x 12 = 96 ALL FLAT — the ninth form has no persistent tail —
+ 12 strip spots m ∈ {18..21} + the m=13 base spot 0); D8 belowband
anchors 133 (H(19;Y;19) vs v(s,19,19) over the floor-13 census domain —
the supply-source collapse of lemma BB''). Total 15,680 points.

Predry (this lane, pre-publication): 8 runs — default x2,
PYTHONHASHSEED=random/1/0 (same cwd), env -i isolated x3 (explicit
/usr/local/bin/python3) — ALL byte-identical, stdout sha256
246aa6fdca5a128b9b1611a7902af41b87d101b1fcafc27ec41c9d8533928d3b,
overall_bad 0, rc 0. Tamper battery 8/8 fail-closed: --tamper-engine rc 2;
--tamper=cell|strip|anchor17|stair|deviant|ext|belowband each rc 1 with
bad=1 on exactly the targeted gate.

The universal claims (12 cell lemmas, T-Z18, corollaries) are proven on
paper in the declaration note section 2; the battery is a finite engine
cross-check, not a proof. Official runs follow from the published bytes
(official_runs/run1..run4.out + detcheck.json) per the publish-then-
execute protocol. 11x11 UNKNOWN unchanged throughout; verdict not
consumed.
