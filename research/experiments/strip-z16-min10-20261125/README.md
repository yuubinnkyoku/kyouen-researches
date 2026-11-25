# z16-min10 pre-declaration exploration kit (frozen)

This directory is the publish-then-execute PRIMARY RECORD for the pre-declaration
census of the z=16 min>=10 (floor-10) cell ladder — the K1320-system-2 m=10-row
z=16 residual edition. No K slot is claimed by this kit and no claim is made
here: everything below is machine observation. A later declaration lane picks up
any slot claim, paper proof, verification machine and official runs (candidate:
an m=10-row z=16 (+ z=17) closure statement, NOT a T-Z17-slice claim).

## Contents

- `engine_block.py` — sha256 `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`
  (the pinned engine block, byte-identical to the K1282..K1322 chain; sha256 of
  the embedded block itself is the startup pin `bd5f22e4…`).
- `explore_z16f10.py` — sha256
  `ad2b44a8d9e156ad880395d394d2e50c9319094a51f455de19d7d7b173d1f4de`
  (adapted from the frozen published `explore_z16pre.py`
  `87f3bb71a28908038646fc67d0d40fb93b2c775f73f184407e444f31f2ab4b0e` (the
  floor-11 edition) by the disclosed textual diff: floor 11→10 (same z=16, same
  rung budget R=j+17), s domain {0}∪{11..41}→{0}∪{10..40} (the EXACT
  221-shape-per-cell domain of the published z=15 floor-10 kit for cross-slice
  comparability), the strip/base/row sections REPLACED by this edition's
  questions: the 10th rung A416f10 (j=10, R=27) IS the full m=10-row z=16
  domain (min=10 strictly, co-token 10 shapes, arity<=4), tail spots s∈{41..48}
  for all 10 cells, and the FLOOR-10 below-band child census
  `H(17;Y;17)` vs `v(s,17,17)`. Per-cell `H.cache_clear()` retained).
- `explore_z16f10.out` — sha256
  `45aa409a458e5704263ab8dc29d0c783fd324f2e4dc7ae4f125cd55701db50a1`
  (the frozen stdout; deterministic — three runs with default,
  PYTHONHASHSEED=random same cwd and env -i isolated dir all byte-identical,
  rc 0, ~12 s per run; no randomness, no wall-clock, no hash-order dependence).

## What the census recorded (observation, judgment-free; see the predecl log)

- 10 floor-10 cells at z=16 (`Cell_j(s) := H(j+17;{j}∪Y;16)`, Y tokens >= 10):
  ALL cells s-only (multivalue rows 0) over 221 shapes each
  (s ∈ {0}∪{10..40}, arity 0..4). Deviant structure:
  **F {s=16 UP:1}**, **G {s=14 DOWN:0, s=16 UP:2}**, **E {s=14 UP:1}**,
  **D {s=12 DOWN:0, s=14 UP:2}**, **C {s=12 UP:1}**,
  **B {s=10 DOWN:0, s=12 UP:2}**, **A {s=10 UP:1}**, **A2 {s=10 UP:2}**,
  **A3 NONE, A4 NONE (two consecutive full collapses at the ladder top)**.
- **The s>=12 classes are IDENTICAL to the published floor-11 (K1322) deviant
  table** — for s >= 12 the two floors share shapes and the measured tables
  agree cell-by-cell (F/G/E/D/C and the s=12 B), an automatic engine-level
  cross-check against the published z16-min11 census.
- **s=10 REVIVAL — the second "death event" is a DOMAIN EXCLUSION, not a
  z-transition**: at floor 11 the z=15 s=10 source classes sit below the floor
  and vanish from the census (K1322); re-admitting s=10 at floor 10 they are
  ALIVE at z=16, restructured from the published z=15 positions {A,B,C}@10 to
  **{B DOWN:0, A UP:1, A2 UP:2}@10** (C loses its s=10 partner; the class
  climbs one rank at the A-side and B flips direction). Death events in this
  series are therefore floor-definition effects on the OBSERVED census; the
  underlying z-transition only restructures the class, it does not kill it.
- **A416f10 (j=10, R=27) — the FULL m=10-row z=16 domain — collapses
  COMPLETELY: 221 shapes, 0 deviants, 0 multivalue, arity<=4, min=10 strictly
  with co-token 10 shapes included.** Together with the published z16-min11
  section-(d) record (arity<=3, S∈{10..48}: 130 shapes, 0 separations) and the
  8/8 single-token tail matches below, this is the complete in-domain evidence
  for an m=10-row z=16 closure candidate (declaration lane owns the universal
  claim). A316f10 also collapses in-domain.
- Tail spots s∈{41..48}, all 10 cells: **80/80 match the collapse** — no
  persistent tail anywhere at floor 10 z=16 (consistent with the K1322 seventh
  F-tail-form: the z=16 single-point F structure {s=16 UP:1} persists with no
  s>=17 tail at both floors; the tail REBIRTH is a z=17 event, measured by the
  z17-min12 kit, not a floor event).
- Below-band bottom-rung child census at FLOOR 10:
  `H(17;Y;17)` = `v(s,17,17)` for ALL 221 floor-10 shapes (0 deviants, 0
  multivalue) — the full-collapse of the below-band supply child EXTENDS from
  the published floor-11 domain (183 shapes) to the broader floor-10 domain
  (min(Y)>=10, co-token 10 shapes included), the z=16 analog of the K1320
  lemma-BB family. Whether this extends to a floor-10 lemma-BB-style universal
  statement belongs to the declaration lane.

See `research/log/2026-11-25-z16f10-predecl-exploration.md` for the
primary-source timeline, honest disclosure and handoff instructions.

## Standard caveats

Everything in this kit is a FINITE machine observation against the pinned raw
engine. Nothing here is a theorem, nothing universal is claimed, and no verdict
of any game position (11x11 standard board, two-stone roots, S2, class 1/2/4 —
all UNKNOWN) is consumed. Battery/point counts are engine cross-checks, not
proofs. The paper proofs, the slot claim and the verification machine belong to
the declaration lane.
