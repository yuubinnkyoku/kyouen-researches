# z14-min9 pre-declaration exploration kit (frozen)

This directory is the publish-then-execute PRIMARY RECORD for the pre-declaration
census of the z=14 min>=9 (floor-9) slice — the next slice registered as open by
K1317 §5/§7 (T-Z14). No K slot is claimed by this kit and no claim is made here:
everything below is machine observation. The declaration lane (a later run) picks
up the slot claim, the paper proof, the verification machine and the official runs.

## Contents

- `engine_block.py` — sha256 `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`
  (the pinned engine block, byte-identical to the K1282..K1317 chain; sha256 of the
  embedded block itself is the startup pin `bd5f22e4…`).
- `explore_z14pre.py` — sha256 `2890def6cfa345bb45f03b596d3437aa520e88b3c81701a71908b056b7d02789`
  (adapted from the frozen `explore_k1317.py` by the disclosed textual diff:
  z 13→14, cell budget j+14→j+15, floor 8→9, 8 rungs j∈{1..8} with the provisional
  8th-rank label `A2`, s domain {0}∪{9..40}, strip m∈{9..13} at the T-Z14 claim
  position, an out-of-band frontier record for m=8 at z=14, strip spots m∈{14..17},
  and the m=9 base spot. Per-cell `H.cache_clear()` retained to avoid the z=13
  shared-cache OOM lesson).
- `explore_z14pre.out` — sha256 `0d57e481afc97c81c639c424d07e71f40df7410afaa4a345a9d51176f19257d6`
  (the frozen stdout; deterministic — two runs with default and PYTHONHASHSEED=1337
  byte-identical, rc 0, ~17 s per run; no randomness, no wall-clock, no hash-order
  dependence in the output).

## What the census recorded (observation, judgment-free; see the predecl log)

- 8 floor-9 cells at z=14 (`Cell_j(s) := H(j+15;{j}∪Y;14)`, Y tokens >= 9):
  ALL cells s-only (multivalue rows 0) over 312 shapes each (s ∈ {0}∪{9..40},
  arity 0..4). Deviant structure: F {s=14 UP}, G {s=12 DOWN, s=14 UP}, E {s=12 UP},
  D {s=10 DOWN, s=12 UP}, C {s=10 UP}, B {s=10 UP}, A (j=7) NONE (full collapse),
  A2 (j=8, min=8) NONE (full collapse — the T-Z14 base candidate cell).
- Tail spots s∈{41..48} all 8 cells: all match the Σ-collapse.
- T-Z14 claim position (m∈{9..13}, arity<=3, parts>=m): 791 shapes, 0 violations.
- m=9 base spot H(24;(9,9);14)=0=v(18,14,24).
- Frontier out-of-band record m=8 z=14 (z*(8)=14): 362 shapes, exactly ONE
  separation: S=16, X=(8,8), parent 2 vs single 1 (UP) — the L2 diagonal frontier
  witness with parent 2 single parity 1, exactly as the published K1268 front law
  prescribes for even m at z=z*(m) (recorded as observation, not a claim).

See `research/log/2026-11-25-z14-predecl-exploration.md` for the full primary-source
timeline, honest disclosure and handoff instructions.
