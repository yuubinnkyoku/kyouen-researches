# 2026-11-28 eight-row q9 8x29 class-split continuation (classes {0},{1},{3} krow/minpos) — single-owner declaration (publish-then-execute)

## Scope (single-owner)

- Board family (w,q)=(8,9), deficient-maximal band. Current published state
  (results/fixed-width/mwq_stabilization.csv (8,9) row; m29 row-split completion
  log 2026-11-28): witness band 8x9..8x28, M_{8,9} in [29,984], frontier 8x29.
  Decided at 8x29 so far: single-deficiency row class {2} (=rowY=2, UNSAT
  5,079,168 conflicts) is witness-free. rowY=3/0/1 direct: INDET @280s.
  class {3} krow=3:7 minpos 0/1: INDET 5,424,393 / 5,228,774 @280s.
- This Part sweeps the unswept class-split pieces of the remaining
  single-deficiency row classes at 8x29, in this order:
  1. class {3} krow=3:7 minpos p=2..13 (sound H-split bound floor((29-1)/2)=14,
     so p covers 0..13; p=0/1 already INDET, disclosed)
  2. class {0} krow=0:7 minpos p=0..13 (fresh, first evaluation)
  3. class {1} krow=1:7 minpos p=0..13 (fresh, first evaluation)
- Time cap per instance: 280 s (container piece cap). Any INDET is an honest
  negative with disclosed conflicts; no absence claim from INDET.
- WIN-stop rule: the first SAT piece stops the sweep; a witness at any 8x29
  piece resolves the band extension (M_{8,9} >= 30) and remaining pieces stay
  unswept and are disclosed as such. Any result is accepted; SAT pieces go
  through the dual-verification protocol below.
- Per-piece absence semantics: UNSAT of (class {c}, krow=c:7, minpos=p) is a
  per-piece absence claim for that sub-bucket only. A class is witness-free
  only if all its deciding pieces are UNSAT with none INDET-undetermined.

## Pre-registered calibration (executed after this declaration is published)

- Cold rerun of the published positive control 8x28 class {3} krow=3:7
  minpos=1 (the second 63-stone witness piece): expected **SAT, conflicts
  3,013,059** (m29 row-split kit, class-split control). Bit-exact conflicts
  expected; wall time is host-dependent and disclosed, not gated. CNF
  regeneration determinism check (regen x2 byte-identical).

## Toolchain pins (all fetched from main before this declaration)

- Scripts VERBATIM from research/experiments/eight-row-q9-m29-row-split-20261128/scripts
  (sha256 pins: genfast.js 409b5216..., decode_verify.js bf64e428..., sat.js
  fcc0cfd8..., sat2.js 14ceb854..., sat3.js e04581eb..., verify_witness.py
  298ff590..., clsrun.sh 38e6e293...), re-fetched and sha-verified from main at
  commit 1e813043 before execution.
- kissat 4.0.4 official linux-amd64, sha256 21da5d984e38b74f620f14c62442f834f
  27b9158decdb722540d97f98aac93a1 (reused pinned binary, sha re-verified).

## Verification protocol on SAT

- Model decode via sat3.js decode (jsVerify verifyConfig) + independent
  exact-Fraction verify_witness.py (pyVerify); both must PASS (safe + maximal
  + deficient). Cold pair: the deciding piece is rerun cold; conflicts must
  be identical (wall time may differ).

## Non-goals / disclaimers

- No 11x11 claim: the standard 11x11 empty board, 19 central-reply roots,
  two-stone root {60,27}, third move {100,108}, S2, and all closure classes
  remain UNKNOWN at all times; verdicts here are not consumed by any 11x11
  bookkeeping.
- No multi-deficiency (2-deficient-row) coverage at 8x29 is claimed by this
  Part unless explicitly run and disclosed.
- Parallel-lane hygiene: latest main was re-fetched immediately before this
  declaration (HEAD 9def0879, the t>=2 blocking-duality declaration). Active
  single-owner lanes observed today: t>=2 blocking-duality sweep, n11
  escalation/adoption lanes, 5x28 sweep, six-row q8 band4 takeover (m=109..370),
  6x32 class-split. No other eight-row q9 8x29 lane is declared or in flight.
- Declaration-time HEAD: 9def08790034abc9f87f02203cfd027a7a3733e8
- This is the single-owner declaration for this session's 8x29 class-split
  continuation sweep. Parallel runs must defer this cell.
