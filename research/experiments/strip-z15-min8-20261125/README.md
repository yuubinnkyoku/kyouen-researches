# z15-min8 pre-declaration exploration kit (frozen) — classical-floor necessity continuation

This directory is the publish-then-execute PRIMARY RECORD for the
pre-declaration census of the z=15 **floor-8** (min(Y)>=8, TWO floors below
the published z-5 floor-10, one below the published floor-9 kit) cell ladder
F15f8..A215f8 plus the m=8 beyond-frontier **z=16** record (one more slice
beyond the published z=15 record) — the NECESSITY side continuation of the
general-floor question (K1319 §5). No K slot is claimed by this kit and no
claim is made here: everything below is machine observation. The
declaration lane (a later run) owns all slot claims.

## Contents

- `engine_block.py` — sha256 `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`
  (the pinned engine block, byte-identical to the K1282..K1320 chain; sha256 of the
  embedded block itself is the startup pin `bd5f22e4…`).
- `explore_z15f8pre.py` — sha256
  `234902dbd9b336c410aacea882fca97d2f66d14e9a1ac2577faf2a79bf1daac4`
  (adapted from the frozen `explore_z15pre.py` `3e2a8ab8…` by the textual
  splice discipline: ENGINE_BLOCK kept byte-identical — z stays 15, cell
  budget j+16 stays, floor 9→8, 8 rungs j∈{1..8} (labels F..A2 with suffix
  15f8), s domain {0}∪{8..40}, the below-band child census at floor 8
  (`H(16;Y;16)` vs `v(s,16,16)`), and a NEW m=8 beyond-frontier z=16 record
  (the second slice beyond z*(8)=14, published frontier-record parameter
  style). Per-cell `H.cache_clear()` retained).
- `explore_z15f8pre.out` — sha256
  `a66fe53f2de77cdd07e6f9d0edd9feceb853d50e22c6523cd61a1a107698b000`
  (the frozen stdout; deterministic — three runs with default,
  PYTHONHASHSEED=random and env -i isolated all byte-identical, rc 0,
  ~21 s per run).

## What the census recorded (observation, judgment-free; see the predecl log)

- 8 floor-8 cells at z=15 (`Cell_j(s) := H(j+16;{j}∪Y;15)`, Y tokens >= 8):
  ALL cells s-only (multivalue rows 0) over 460 shapes each (s ∈ {0}∪{8..40},
  arity 0..4; 3,680 shapes total). **The s-only collapse survives at floor
  z-7** — the second consecutive affirmative data point below the published
  z-5 floor on this slice (floor 9: published kit; floor 8: this kit).
- Deviant structure (vs the Sigma-collapse `v(s+j,15,j+16)`):
  F {s=14 DOWN, clean hole at s=15, s>=16 CONSTANT-2 UP tail (26 in-domain
  deviants — tail spots unbroken through s=48)}, G {s=14 DOWN 0<1},
  E {s=12 DOWN 1<2, s=14 UP 2>0}, D {s=12 DOWN 0<1}, C {s=10 DOWN 1<2,
  s=12 UP 2>0}, B {s=10 DOWN 0<1}, **A (j=7) {s=8 DOWN 1<2, s=10 UP 2>0} —
  the A rung, clean at floors 9/10 except the s=10 point, GAINS an s=8
  deviant**, **A2 (j=8) {s=8 DOWN 0<1} — the bottom rung, fully collapsed
  at floor 9, GAINS its first deviant**.
- **The s=8 rows (outside the floor-9/10 sweep domains) carry deviants
  exactly at the bottom rungs (A/A2)** — the reintroduction side of the
  death-point mechanism (the z=13→z=14 transition killed the s=8 sources of
  C13f8/B13f8/A13f8 by raising the floor; LOWERING the floor to 8 at z=15
  re-admits s=8 structure onto the ladder for the first time). Note the
  internal consistency: A215f8 at s=8 is the shape X=(8,8), which is
  exactly the single published beyond-frontier separation at z=15 (0 vs 1
  DOWN) — the row record and the cell census agree.
- Tail spots s∈{41..48} all 8 cells: only F15f8 mismatches (8 rows, value 2
  vs collapse 0); the other 7 cells match (56/56).
- Below-band bottom-rung child census (floor 8): `H(16;Y;16)` = `v(s,16,16)`
  for ALL 460 floor-8 shapes (0 deviants, 0 multivalue rows).
- **m=8 z=16 beyond-beyond frontier record** (the SECOND slice beyond the
  frontier, R=25, S∈{8..47}, arity<=4): 362 shapes, **2 separations**:
  X=(8,8), value 0 vs collapse 2 (DOWN) — the lone (8,8) separation persists
  a second slice beyond the frontier (z=14 UP 2v1 → z=15 DOWN 0v1 → z=16
  DOWN 0v2) — and a NEW second separation **X=(8,10), S=18, value 2 vs
  collapse 1 (UP)**. The beyond-frontier separation set grows with z.

See `research/log/2026-11-25-z15-min8-predecl-exploration.md` for the full
primary-source timeline and handoff instructions.
