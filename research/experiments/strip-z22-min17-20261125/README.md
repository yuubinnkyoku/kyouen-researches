# z22-min17 pre-declaration exploration kit (frozen)

This directory is the publish-then-execute PRIMARY RECORD for the pre-declaration
census of the z=22 min>=17 (floor-17) slice — the next slice of the vertical-fiber
strip series after the z21-min16 census kit (`8a106233`). No K slot is claimed
by this kit and no claim is made here: everything below is machine observation.
The declaration lane (a later run) picks up the slot claim, the paper proof, the
verification machine and the official runs.

## Contents

- `engine_block.py` — sha256 `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`
  (the pinned engine block, byte-identical to the K1282..K1331 chain; sha256 of the
  embedded block itself is the startup pin `bd5f22e4…`).
- `explore_z22f17.py` — sha256
  `9e8ab7073a5d9d119af7928a19953efa1ac409df15b5878c9dab473af2e5c3c9`
  (adapted from the frozen published `explore_z21f16.py`
  `edb31ad07c83f43cf742a3cf3b139edbe16f9c797d6ce606f475010d624c1a81` by the
  disclosed textual diff: z 21→22, cell budget j+22→j+23, floor 16→17, rungs
  15→16 with the provisional 16th-rank label `A10` (small token 16 — the EIGHTH
  consecutive in-band base child; z*(16)=30 > 22), s domain {0}∪{17..47},
  tail spots {48..55}, strip m∈{17..21} at the provisional T-Z22 claim
  position, an IN-BAND m=16-row record at z=22 (R=39, the T-Z22 base-child
  position AND the CANDIDATE FIRST entry of the future T-Z21 residual band
  m=16 z∈{22..29}, frontier z*(16)=30; published residual-band style arity<=3
  TOTAL, plus an arity<=4 co-token extension sweep), an IN-BAND m=15-row
  record at z=22 (R=38, the SECOND entry of the future T-Z20 residual band
  m=15 z∈{21..28}; same enumeration as the published z=21 census entry → same
  50 shapes, cross-artifact consistency), an IN-BAND m=14-row record at z=22
  (R=37, the THIRD entry of the K1330 published residual band m=14 z∈{20..25};
  same 62 shapes), an IN-BAND m=13-row record at z=22 (R=36, the FOURTH entry
  of the K1328 published residual band m=13 z∈{19..24}; same 76 shapes),
  strip spots m∈{22..25}, the m=17 base spot (never measured by any published
  kit; candidate 0 from the base-spot z-parity sequence), the below-band
  bottom-rung child census `H(23;Y;23)` vs `v(s,23,23)`, and section (g): the
  THIRTEENTH-tail supply identity RECHECK `v(s,23,23)` vs `v(s,22,23)`
  (published by the z20 census + z21 census kits; rechecked and extended over
  s∈{0}∪{12..59}), the FOURTEENTH-tail supply identity RECHECK
  `v(s,24,24)` vs `v(s,23,24)` (published by the z21 census kit; rechecked
  extended), plus the NEW engine-free FIFTEENTH-tail supply pre-computation
  `v(s,25,25)` vs `v(s,24,25)` with BOTH break components predeclared. The
  FULL predeclared per-cell deviant profile (derived from the published z=20
  even profile `2cc16d34` shifted +2, with the complete 8-class deviant list
  spelled out per cell — the z21 C-cell disclosure lesson applied) is in the
  file docstring, written before the first run. The m=12-row is NOT swept
  (the K1325 band m=12 z∈{18..21} closed at z=21). Per-cell
  `H.cache_clear()` retained (z=13 shared-cache OOM lesson).
- `explore_z22f17.out` — sha256
  `f16a87d447d61b631cca153665b4a577d844ab5fe96eb9f740a74e400c82c7ac`
  (the frozen stdout; deterministic — SIX runs: default ×3, PYTHONHASHSEED=1
  same-cwd, env -i isolated dirs ×2, all byte-identical, rc 0, ~24 s per
  run; no randomness, no wall-clock, no hash-order dependence).

## What the census recorded (observation, judgment-free; see the predecl log)

- 16 floor-17 cells at z=22 (`Cell_j(s) := H(j+23;{j}∪Y;22)`, Y tokens >= 17):
  ALL cells s-only (multivalue rows 0) over 88 shapes each
  (s ∈ {0}∪{17..47}, arity 0..4). Deviant structure — the deviant position
  set is **{18, 20, 22}, the exact +2 shift of z=21's {16, 18, 20} with the
  position-16 classes falling BELOW the floor-17 domain — the FIFTH
  domain-exclusion event, exactly as predeclared**.
  - The FULL predeclared 8-class per-cell deviant list hit **8/8 with ZERO
    undisclosed extra classes** — the first slice whose complete per-cell
    predeclaration (written from the published z=20 even profile
    `2cc16d34`, +2 shifted) matched the measurement class for class:
    **F {s=22 UP:1v0}** (single point at s=22=z, even form, NO tail),
    **G {s=20 DOWN:0v2, s=22 UP:2v1}**, **E {s=20 UP:1v0}**,
    **D {s=18 DOWN:0v2, s=20 UP:2v1}**, **C {s=18 UP:1v0}**,
    **B {s=18 UP:2v1}**. The even station structure
    {D,C,B}@18 → {G,E,D}@20 → {F,G}@22 (values DOWN 0v2 / UP 1v0 /
    UP 2v1) is the exact +2 successor of the z=20 stations — the
    even→even full-profile +2 shift law is now confirmed on consecutive
    steps z=18→z=20→z=22.
  - **A22f17 FULLY COLLAPSED — the A-break extinction/rebirth alternation
    continues**: extinct at z=20, reborn at z=21 (s=16=z−5 UP:2v0),
    extinct again at z=22 (the would-be break position z−5=17 is an odd s
    and no odd-s A-rank deviant class has ever been observed). The even-z
    A-break exclusion mechanism is now 5/5 even slices (z=16..z=22).
  - **F single-point form at z=22 (even)**: F deviates ONLY at s=22=z as
    UP:1v0 and CONFORMS everywhere else including all tail spots. The
    single@(even z)/hole+tail@(odd z) typology alternation has **EIGHT
    consecutive consistent slices (z15..z22)**. Tail spots s∈{48..55}:
    **128/128 match, all 16 cells** (the even-form signature, contrast
    z=21's F 8/8 mismatch).
  - A2..A10: fully collapsed — NINE consecutive full collapses past the
    A-boundary rung.
  - **A1022f17 (j=16, min=16, z*(16)=30 > 22) fully collapsed over its
    88-shape domain — the EIGHTH consecutive in-band base child** = the
    T-Z22 base-m=17 trivial-absorption candidate.
- Strip sweep at the provisional T-Z22 claim position m∈{17..21}:
  **125 shapes, 0 violations** (cumulative 35/63/86/106/125).
- m=16-row z=22 record (R=39; EIGHTH consecutive base child; candidate FIRST
  entry of the future T-Z21 residual band m=16 z∈{22..29}): **40 shapes,
  0 separations**; arity<=4 co-token extension: **39 shapes, 0 separations**.
- m=15-row z=22 record (R=38; future T-Z20 residual band SECOND entry):
  **50 shapes, 0 separations** — exactly the published z21 census count
  (cross-artifact shape-for-shape consistency machine-checked).
- m=14-row z=22 record (R=37; K1330 residual band THIRD entry):
  **62 shapes, 0 separations** — exactly the published z20/z21 entries.
- m=13-row z=22 record (R=36; K1328 residual band FOURTH entry):
  **76 shapes, 0 separations** — exactly the published entries.
- Strip spots m∈{22..25}: **12/12 match**.
- m=17 base spot `H(40;(17,17);22)` = **0**, conforming (= `v(34,22,40)`),
  the predeclared parity candidate; the base-spot z-parity sequence is now
  **0 (z16), 1 (z17), 0 (z18), 1 (z19), 0 (z20), 1 (z21), 0 (z22)** — seven
  data points.
- Below-band child census `H(23;Y;23)` vs `v(s,23,23)`: 88 shapes,
  **0 deviants, 0 multivalue — EIGHTH consecutive full collapse** of the
  below-band supply child.
- THIRTEENTH-tail identity recheck: `v(s,23,23)=v(s,22,23)` holds exactly on
  **{0}∪{12..21}**, breaks at s=22 as 0v2, then uniformly 2v1 for all
  s∈{23..59} (published z20/z21 values reproduced, extended by one).
- FOURTEENTH-tail identity recheck: `v(s,24,24)=v(s,23,24)` holds exactly on
  **{0}∪{12..23}**, uniform 0v1 break for all s∈{24..59} (published z21
  census constants reproduced, extended by one).
- **FIFTEENTH-tail identity (NEW)**: `v(s,25,25)=v(s,24,25)` holds exactly on
  **{0}∪{12..23}**, breaks at **s=24 as 0v2**, then **uniformly 2v1 for all
  s∈{25..59}** — BOTH predeclared components (break start s=24=z AND the
  0v2-then-uniform-2v1 shape) **CONFIRMED**; the even-z supply-identity form
  is now **4/4** (z=18, z=20, z=22 measured, z=24-supply closed-form
  pre-computation). This is the z=24 slice's supply datum.

## Independent ordered-engine cross-check (outside the frozen artifact)

The FULL census re-enumerated and re-evaluated with `H_ordered` against the
frozen canonical-engine output: 1,408 cell shapes (16 cells × 88), 128 tail
spots, 125 strip shapes, 40+39+50+62+76 record shapes, 12 strip spots, the
base spot, 88 below-band shapes, and ALL identity hold/break rows compared as
full rows (values included): **0 mismatches**; every frozen row reproduced
exactly. Per-record `H.cache_clear()` (published OOM lesson).

See `research/log/2026-11-25-z22m17-predecl-exploration.md` for the
primary-source timeline and handoff instructions.

## Standard caveats

Everything in this kit is a FINITE machine observation against the pinned raw
engine. Nothing here is a theorem, nothing universal is claimed, and no verdict
of any game position (11x11 standard board, two-stone roots, S2, class 1/2/4 —
all UNKNOWN) is consumed. Battery/point counts are engine cross-checks, not
proofs. The paper proofs, the slot claim and the verification machine belong
to the declaration lane. Section (g) is a pure closed-form pre-computation: it
uses no engine recursion at all and inherits only the published K0832
single-token closed form.

## Verify machine (added by the K1339 declaration lane)

- `verify_k1339.py` — sha256 `566543f76e18fcce67cf6e64cbcd7f42b35a8ceffcdd79f652a1038396dc5e07`
  (structural copy of the published `verify_k1337.py` machine with the disclosed
  diff: z 21→22, rung budget 15→16 (16th rung, provisional `A10` label
  formalized as **A1022f17**), floor 16→17, the declared z=22 closed forms
  in D1, the published K1337 z=21 cell transcriptions + T-Z21 claim-row anchors
  re-checked independently in D3, the (ii') below-band supply child
  H(23;Y;23) vs v(s,23,23) in D8. Provisionally named verify_k1338.py;
  renumbered to verify_k1339.py at the pre-push refetch after the parallel
  conic lane claimed K1338 (AG(2,7) size-by-size Grundy decomposition,
  docs/FINITE_RING_STATUS.md) — 2 label bytes differ, battery structure
  unchanged; the numbering incident is disclosed in the declaration note).
  The K1339 single-owner declaration note is
  `research/log/2026-11-25-strip-z22-min17-single-owner-note.md` (commit
  `575abe90`, label repair `7b969301`). Declaration battery **18,128 points,
  fail-closed** (per-gate declared point counts enforced; any deviation or any
  bad point → FAIL): D1 cells 1,408 / D2 strip 125 / D3 z21 anchors 510 /
  D4 stair anchors 496 / D5 self anchors 15,336 / D6 deviant/collapse
  witnesses 24 / D7 extension anchors 141 / D8 below-band anchors 88.
  Engine pin `bd5f22e4…` startup gate. Predry 8 runs byte-identical
  (default ×2, PYTHONHASHSEED=random/1/0 same-cwd, env -i isolated ×3):
  stdout sha256
  `05be7d667d9b278f1501c137e99b848a30f9257bdc8f807963b6169006158856`.
  Tamper 8/8 fail-closed (engine rc 2; cell/strip/anchor21/stair/deviant/ext/
  belowband each rc 1, flagging exactly its target gate with bad=1 and no
  other). Official runs (publish-then-execute, from these published bytes)
  follow in `official_runs/`.
