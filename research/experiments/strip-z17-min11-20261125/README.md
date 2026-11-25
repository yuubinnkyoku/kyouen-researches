# z17-min11 pre-declaration exploration kit (frozen)

This directory is the publish-then-execute PRIMARY RECORD for the pre-declaration
census of the z=17 min>=11 (floor-11) cell ladder — the K1322-system m=11-row
z=17 residual edition. No K slot is claimed by this kit and no claim is made
here: everything below is machine observation. A later declaration lane picks
up any slot claim, paper proof, verification machine and official runs
(candidates: the T-Z17 slice declaration (fed by the z17-min12 floor-12 kit)
and/or an m=11-row z=17 closure statement (fed by this kit's A5 rung)).

## Contents

- `engine_block.py` — sha256 `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`
  (the pinned engine block, byte-identical to the K1282..K1322 chain; sha256 of
  the embedded block itself is the startup pin `bd5f22e4…`).
- `explore_z17f11.py` — sha256
  `30dcc060bfa30e9ea62a2218ec7f56a53661584daa014be9a92e7284b743ff23`
  (adapted from the frozen published `explore_z17m12.py`
  `410fea310b00da6733e6d336fa6b275890307ad16e6603683fc1f4500bdef7b0` (the
  floor-12 edition, same `2c74f1c6` kit) by the disclosed textual diff: floor
  12→11, s domain {0}∪{12..42}→{0}∪{11..41} (the 183-shape-per-cell domain),
  the strip/row-record/spot sections REMOVED (all already published: strip
  358/0 and the m=11/m=10/m=8 records live in the z17-min12 kit), tail spots
  s∈{42..49}, and the FLOOR-11 below-band child census
  `H(18;Y;18)` vs `v(s,18,18)`. Per-cell `H.cache_clear()` retained).
- `explore_z17f11.out` — sha256
  `8ecbd60599a2b6212e6972c9eb9a4ee00306d64650ea085c0ed24c042122e627`
  (the frozen stdout; deterministic — three runs with default,
  PYTHONHASHSEED=random same cwd and env -i isolated dir all byte-identical,
  rc 0, ~13 s per run; no randomness, no wall-clock, no hash-order
  dependence).

## What the census recorded (observation, judgment-free; see the predecl log)

- 11 floor-11 cells at z=17 (`Cell_j(s) := H(j+18;{j}∪Y;17)`, Y tokens >= 11):
  ALL cells s-only (multivalue rows 0) over 183 shapes each
  (s ∈ {0}∪{11..41}, arity 0..4). Deviant structure:
  **F {s=16 DOWN:1, s=17 hole, persistent UP:2 tail for ALL s>=18}**,
  **G {s=16 DOWN:0}**, **E {s=14 DOWN:1, s=16 UP:2}**, **D {s=14 DOWN:0}**,
  **C {s=12 DOWN:1, s=14 UP:2}**, **B {s=12 DOWN:0}**, **A {s=12 UP:2}**,
  **A2/A3/A4/A5 NONE (four consecutive full collapses)**.
- **s=11 has NO deviant in ANY cell** — s=11 entering the domain is the FIRST
  odd-s domain entry of the series (all previously swept classes sit at even
  s in {8,10,12,14,16}) and NO odd-s class appears: the odd-s silence extends
  to the first direct test. Observational only.
- The s>=12 classes are IDENTICAL to the published floor-12 (z17-min12 kit)
  deviant table — for s >= 12 the two floors share shapes and the measured
  tables agree cell-by-cell, an automatic engine-level cross-check of the
  published z17-min12 census.
- **A517f11 (j=11, R=29) — the FULL m=11-row z=17 domain — collapses
  COMPLETELY: 183 shapes, 0 deviants, 0 multivalue, arity<=4, min=11 strictly
  with co-token 11 shapes included.** Together with the published z17-min12
  section-(d) record (arity<=3, S∈{11..49}: 110 shapes, 0 separations) and the
  8/8 A5 single-token tail matches below, this completes the in-domain
  evidence for an m=11-row z=17 closure candidate (the K1322 published
  residual band m=11 z∈{17..20} first entry). A417f11 also collapses
  in-domain. Declaration lane owns any universal claim.
- Tail spots s∈{42..49}: the F persistent tail is confirmed OUTSIDE the census
  domain (**8/8 F mismatches, value 2 vs collapse 0**; the other 80 spots
  match) — same F-tail structure as the floor-12 census: the F-family EIGHTH
  tail form (persistent tail reborn at z=17) is FLOOR-INSENSITIVE between
  floors 11 and 12.
- Below-band bottom-rung child census at FLOOR 11:
  `H(18;Y;18)` = `v(s,18,18)` for ALL 183 floor-11 shapes (0 deviants, 0
  multivalue) — the full-collapse of the z=17 below-band supply child now
  holds at BOTH floors 11 and 12 (floor-12: 155 shapes published), extending
  the K1320 lemma-BB family pattern to z=17. Whether it extends universally
  belongs to the declaration lane.

See `research/log/2026-11-25-z17f11-predecl-exploration.md` for the
primary-source timeline, honest disclosure and handoff instructions.

## Standard caveats

Everything in this kit is a FINITE machine observation against the pinned raw
engine. Nothing here is a theorem, nothing universal is claimed, and no verdict
of any game position (11x11 standard board, two-stone roots, S2, class 1/2/4 —
all UNKNOWN) is consumed. Battery/point counts are engine cross-checks, not
proofs. The paper proofs, the slot claim and the verification machine belong to
the declaration lane.
