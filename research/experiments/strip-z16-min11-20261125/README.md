# z16-min11 pre-declaration exploration kit (frozen)

This directory is the publish-then-execute PRIMARY RECORD for the pre-declaration
census of the z=16 min>=11 (floor-11) slice — the next slice of the vertical-fiber
strip series after the K1320 (T-Z15) completion. No K slot is claimed by this kit
and no claim is made here: everything below is machine observation. The declaration
lane (a later run) picks up the slot claim, the paper proof, the verification
machine and the official runs.

## Contents

- `engine_block.py` — sha256 `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`
  (the pinned engine block, byte-identical to the K1282..K1320 chain; sha256 of the
  embedded block itself is the startup pin `bd5f22e4…`).
- `explore_z16pre.py` — sha256
  `87f3bb71a28908038646fc67d0d40fb93b2c775f73f184407e444f31f2ab4b0e`
  (adapted from the frozen published `explore_z15pre.py`
  `3e2a8ab863212efc3806a6acb93caeb7c9020ead468e1afa9cb6ffd4c2714513` by the
  disclosed textual diff: z 15→16, cell budget j+16→j+17, floor 10→11, rungs
  9→10 with the provisional 10th-rank label `A4` (small token 10 — the SECOND
  consecutive in-band base child; z*(10)=18 > 16), s domain {0}∪{11..41},
  strip m∈{11..15} at the T-Z16 claim position, an IN-BAND m=10-row record at
  z=16 (R=27, the T-Z16 base-child position AND the K1320 section-6 leftover
  m=10 row residual z=16), strip spots m∈{16..19}, the m=11 base spot, and the
  below-band bottom-rung child census `H(17;Y;17)` vs `v(s,17,17)`.
  Per-cell `H.cache_clear()` retained (z=13 shared-cache OOM lesson).
  HONEST NOTE: the docstring structural note first written for this kit
  wrongly predicted the s=12 sources to die under floor 11; the error was
  caught while checking the census output (s=12 deviants survive) and
  corrected BEFORE freezing and publication. The .out bytes were never
  affected (docstring only)).
- `explore_z16pre.out` — sha256
  `16b10d0bb6be2b618208b258422608509fc9adafc97672d9d02d345d4e0c11db`
  (the frozen stdout; deterministic — three runs with default,
  PYTHONHASHSEED=1 and env -i isolated dir all byte-identical, rc 0,
  ~15 s per run; no randomness, no wall-clock, no hash-order dependence).

## What the census recorded (observation, judgment-free; see the predecl log)

- 10 floor-11 cells at z=16 (`Cell_j(s) := H(j+17;{j}∪Y;16)`, Y tokens >= 11):
  ALL cells s-only (multivalue rows 0) over 183 shapes each
  (s ∈ {0}∪{11..41}, arity 0..4). Deviant structure:
  **F {s=16 UP:1}** (a SINGLE above-floor UP point — the F-family SEVENTH tail
  typology candidate: the z=15 sixth-form tail (DOWN@14, hole@15, constant-2
  tail s>=16) does NOT carry over; all 8 F tail spots s∈{42..49} match the
  collapse), **G {s=14 DOWN:0, s=16 UP:2}**, **E {s=14 UP:1}**,
  **D {s=12 DOWN:0, s=14 UP:2}**, **C {s=12 UP:1}**, **B {s=12 UP:2}**,
  **A NONE, A2 NONE, A3 NONE, A4 NONE (four consecutive full collapses)** —
  A4 (j=10, min=10) is the SECOND consecutive in-band base child and it
  fully collapses over its cell domain (Y tokens >= 11).
- Death-point deactivation, SECOND event of the series, CONFIRMED for the
  s=10 branch exactly as the floor criterion predicts: every z=15 source
  position s=10 (C15f10/B15f10/A15f10) is below the new floor 11 and NO s=10
  deviant appears anywhere at z=16 (contrast: at z=13→z=14 all sources survived;
  the first death event was z=13→z=14's s=8 branch... precisely: the z=13
  s=8 sources died at z=14). The s=12 and s=14 sources survive but their
  deviant structure is RESTRUCTURED across ranks (values change, E loses its
  s=12 deviant, D gains an s=14 UP, B switches from s=10 DOWN to s=12 UP).
- NEW above-floor deviant class at s=16 (F UP:1, G UP:2) — no prior slice
  had s=16 deviants in the F/G rungs; the declaration lane must derive
  their supply.
- Tail spots s∈{42..49} all 10 cells: 80/80 match (no F tail at this slice).
- Below-band bottom-rung child census: `H(17;Y;17)` = `v(s,17,17)` for ALL
  183 floor-11 shapes (0 deviants, 0 multivalue) — the z=16 analog of the
  K1320 lemma-BB supply source, itself a full collapse.
- T-Z16 claim position (m∈{11..15}, arity<=3, parts>=m): **456 shapes,
  0 violations** (cumulative per m: 11→142, 12→249, 13→333, 14→401, 15→456).
- IN-BAND m=10-row record at z=16 (R=27, parts >= 10 INCLUDING co-token 10
  shapes, arity<=3, S∈{10..48}): **130 shapes, 0 separations** — the first
  affirmative data for the K1320 section-6 leftover (m=10 row residual
  z=16; the z=15 analog measured 152/0 for the m=9 row).
- Strip spots m∈{16..19}: 12/12 match. m=11 base spot H(28;(11,11);16)=0=
  v(22,16,28) (the m=10 analog at z=15 was 1).

See `research/log/2026-11-25-z16-predecl-exploration.md` for the primary-source
timeline, honest disclosure and handoff instructions.

## Standard caveats

Everything in this kit is a FINITE machine observation against the pinned raw
engine. Nothing here is a theorem, nothing universal is claimed, and no verdict
of any game position (11x11 standard board, two-stone roots, S2, class 1/2/4 —
all UNKNOWN) is consumed. Battery/point counts are engine cross-checks, not
proofs. The paper proofs, the slot claim and the verification machine belong to
the declaration lane.

## Verification machine (K1322, publish-then-execute wave 2)

- `verify_k1322.py` — sha256
  `27e37152896a67798ab7cdf13e08fd2d5b80b4960bbceb7ea00025e87a96097c`
  (structural copy of the published verify_k1320.py `081fe719…`; disclosed
  changes: z 15→16, cell budget j+16→j+17, floor 10→11, rungs 9→10 with the
  provisional 10th-rank label `A4` adopted as final **A416f11** (min=10, the
  SECOND consecutive in-band base child), D3 anchors = the published K1320
  z=15 lines F15f10..A315f10 + T-Z15 C-hand anchors (m ∈ {11..15}),
  D4 31 floor-11 s-values, D5 grid x ∈ {1..29}, z ∈ {0..17}, 19 R-points per
  pair + empty anchors, D6 19 deviant/collapse witnesses (incl. the F16f11
  absorption-break UP, the s>=17 uniform-absorption witness, the FLAT
  absorptions at the in-run supply points, and the four fully collapsing
  A-ranks' spots + the in-band base spot), D7 tail spots × 10 cells + strip
  spots m ∈ {16..19} + m=11 base spot, D8 below-band gate sweeping
  H(17;Y;17) vs v(s,17,17) over the full floor-11 census domain).
  Battery: **13,293 fail-closed points** (D1 1830 / D2 456 / D3 322 / D4 310 /
  D5 10080 / D6 19 / D7 93 / D8 183); engine pin `bd5f22e4…` startup gate;
  `--tamper-engine` rc 2 + 7 value modes rc 1 each flagging exactly one declared
  gate (8/8 measured pre-publication).
  Predry (pre-publication): 7 runs (default; PYTHONHASHSEED=random/1/0 same cwd;
  3× env -i isolated dirs) all rc 0, stdout byte-identical, sha256
  `e0c6559f523f768204e7704e5e9ce42022d694d680bb059fef515f6d34bbad04`
  (~16 s per run). The official 4-run protocol from these published bytes
  follows in wave 3. No verdict claimed; 11x11 stays UNKNOWN.
