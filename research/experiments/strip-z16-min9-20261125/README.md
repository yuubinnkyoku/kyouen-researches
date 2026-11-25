# z16-min9 pre-declaration exploration kit (frozen) — m=9-row z=16/z=17 campaign

This directory is the publish-then-execute PRIMARY RECORD for the pre-declaration
census of the z=16 **floor-9** cell ladder (min(Y)>=9, 9 rungs incl. the
A316f9 claim-position rung) together with the m=9-row **z=16 (last in-band
slice)** record, the **m=9-row z=17 FRONTIER** record (z=17 = z*(9), the
first odd-m frontier observation of the strip series), and the **m=8
beyond-frontier z=15** record (transplanted from this lane's raced z=15
census build so it is published exactly once — see provenance below).
Registered as the K1320 completion log's next tasks 1-2. **NOT the T-Z16
(floor-11) predecl census**: the z=16 strip-series next-slice kit would use
floor 11 = z-5; that is a separate lane decision. No K slot is claimed by
this kit and no claim is made here: everything below is machine observation.

## Provenance (honest disclosure)

A parallel hourly run published the z=15 floor-9 census of the same campaign
first (`research/experiments/strip-z15-min9-20261125`, commit `5ec6c35d`);
this lane had independently built an equivalent z=15 census in the same
window, detected the parallel publication at push time per the racing
protocol, cancelled the duplicate publication, and converted to verification
mode (byte-reproduction of the published z=15 kit from its published bytes,
3 runs byte-identical, plus value-level cross-check of every shared section:
all 8 shared cells' deviant tables identical, below-band collapse identical
— see `research/log/2026-11-25-z15m9-kit-second-lane-verification.md`).
The section (g) measurement below existed only in this lane's z=15 build and
is transplanted here unchanged. The z=16/z=17 sections were measured only by
this lane.

## Contents

- `engine_block.py` — sha256 `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`
  (the pinned engine block, byte-identical to the K1282..K1320 chain; sha256 of the
  embedded block itself is the startup pin `bd5f22e4…`).
- `explore_z16f9pre.py` — sha256
  `e153b0089362ee7fa8958f97b5b77be918e70aff59a62aeb6af042541988a382`
  (adapted from the frozen `explore_z15pre.py` `3e2a8ab8…` by the textual
  splice discipline: ENGINE_BLOCK kept byte-identical, docstring/body
  rewritten — z 15→16, cell budget j+17, floor 9, 9 rungs j∈{1..9}
  (labels F..A3 with suffix 16f9, the j=9 rung A316f9 mirroring the published
  z=15 kit's A315f9 claim-position rung), s domain {0}∪{9..40}, the m=9-row
  z=16 record at R=26 with the arity≤4 min-exactly-9 protocol, m=9-row z=16
  tail spots, the below-band child census `H(17;Y;17)` vs `v(s,17,17)` at
  floor 9, the m=9-row z=17 frontier record (R=27, published z14pre frontier
  parameter style), the m=9 base spot at z=16, and the transplanted section
  (g) m=8 beyond-frontier z=15 record. Per-cell `H.cache_clear()` retained).
- `explore_z16f9pre.out` — sha256
  `7b1469b1d6070b80fe1a1501219ba7d064421dd897d2612558dd6b3642fa1876`
  (the frozen stdout; deterministic — three runs with default,
  PYTHONHASHSEED=random and env -i isolated all byte-identical, rc 0,
  ~21 s per run; no randomness, no wall-clock, no hash-order dependence).

## What the census recorded (observation, judgment-free; see the predecl log)

- 9 floor-9 cells at z=16 (`Cell_j(s) := H(j+17;{j}∪Y;16)`, Y tokens >= 9):
  ALL cells s-only (multivalue rows 0) over 312 shapes each (2,808 total);
  the s-only collapse survives at floor 9 on the second slice up.
- Deviant structure (vs `v(s+j,16,j+17)`) — **STRUCTURALLY NEW vs z=15**:
  F {s=16 UP single point, **NO constant tail** (contrast F15f9/F15f10:
  the F-family tail DIED at z=16 floor-9 — a 7th F-family tail-form data
  point)}, G {s=14 DOWN, s=16 UP}, E {s=14 UP}, D {s=12 DOWN, s=14 UP},
  C {s=12 UP}, B {s=10 DOWN, s=12 UP}, A (j=7) {s=10 UP}, **A2 (j=8)
  {s=10 UP} — the A2 rung, fully collapsed at both z=15 floors, carries a
  deviant for the first time in the strip series**, A3 (j=9, the m=9-row
  z=16 claim-position cell) NONE (full collapse, mirroring A315f9).
- Tail spots s∈{41..48} all 9 cells: **0 mismatches** (72/72 collapse —
  confirming the F tail is dead at this slice, unlike z=15 where F broke
  all 8 of its tail spots).
- **m=9-row z=16 record** (R=26, min(X)=9 exactly, co-token 9 included,
  arity<=4, S∈{9..47}): **235 shapes, 0 separations** — the LAST in-band
  slice (z*(9)=17) of the m=9 row shows the row collapse uniformly,
  matching the published z=15 records (in-band 152-shape arity≤3 record +
  265-shape arity≤3 strip row + 312-shape A315f9 rung census, all
  separation-free). Row tail spots S∈{48..60}: 13/13 match.
  m=9 base spot H(26;(9,9);16)=0=v(18,16,26).
- Below-band bottom-rung child census (floor 9 at z=16): `H(17;Y;17)` =
  `v(s,17,17)` for ALL 312 floor-9 shapes (0 deviants, 0 multivalue rows).
- **m=9-row z=17 FRONTIER record** (z=17 = z*(9), the frontier slice itself,
  R=27, S∈{9..47}, mandatory 9 token, extras >= 9, arity<=3): 234 shapes,
  **exactly 1 separation: X=(10,9), S=19, value 2 vs collapse 0 (UP)**.
  First odd-m frontier observation of the strip series: unlike the even-m
  frontier (m=8 at z=14: the lone separation at the (m,m)=(8,8) shape), the
  **(9,9) shape is NOT separated (collapses) — the odd-m frontier separation
  sits at (m, m+1) = (9,10)**. All other 233 shapes collapse.
- **m=8 beyond-frontier z=15 record** (transplanted section (g); m=8 at
  z=15, one slice beyond z*(8)=14, R=24, S∈{8..47}, arity<=4, published
  z14pre section-(d) parameter style): 362 shapes, **exactly 1 separation,
  X=(8,8), value 0 vs collapse 1 (DOWN)**. The lone frontier separation
  (8,8) of the published z=14 frontier record (value 2 vs collapse 1, UP)
  **PERSISTS one slice beyond the frontier and FLIPS direction UP→DOWN** —
  the first beyond-frontier data point of the strip series.

See `research/log/2026-11-25-z16-min9-m9row-predecl-exploration.md` for the
full primary-source timeline, honest disclosure and handoff instructions.
