# 2026-11-27 kit-19x: independent blind second census of the kit-19 registered rows

## S1 Situation

Pre-work latest-main check: HEAD `d08d4ddd` (seventh-cost k05 L50M escalation
complete). The fast-lane resume note said kit-19's registration source is the
published kit-18 frozen `.out` (9ac8e079, `c3087285...`). The shared
knowledge mount showed the SAME hourly lane's parallel execution already
building kit-19 in `_kit19-build/` (run1/run2 determinism outputs present,
run3 in progress at freeze; kit-19 not yet on main). Following the
kit-17x / kit-18x precedent, this run stood down from a duplicate kit-19
build and instead built the independent blind second census of the same
registered rows.

## S2 Blindness protocol

Registration: the 34-item kit-19 registration machine-parsed from the
published kit-18 frozen `.out` `future_slice_registration_constants`
(sha256 verified `c3087285...`). Semantics: reconstructed from the
published kit-18 explorer source on main (SSOT); enumeration re-implemented
fresh (nested-loop `parts`). The parallel lane's kit-19 explorer source and
any kit-19 run outputs were NOT read before this census was frozen. Only
file names and chunk-progress status lines were observed on the mount.

## S3 Measurements (49 rows, 273 separations; all finite observations)

- Frontier 40th/41st datum, BOTH EXACT: m=53@z=105 R=159 {53,54}@S=107
  UP 2v0 (collapse v(107,105,159)=0); m=54@z=106 R=161 (54,54)@S=108 UP 2v1
  (collapse v(108,106,161)=1). FIRST-EVER m>52 rows; frontier parity
  scaffold 42/42 m=13..54.
- Windows m=51 z{93..100} / m=52 z{94..101}: 16/16 CLEAN (0 separations).
- Ladder m=19..32 one-past+birth next depth: 28/28 FULL HIT. Boundary
  equistack re-observed: m=27 birth NEW seat co=54=2m, {27,27,27}@S=81
  UP 2v0 exact mimic of {27,54}@S=81 UP 2v0.
- Evenlife z=3m+18 (m=14/16/18): 3/3 template EXACT (stick {m,2m+18}
  DOWN 0v2 + NEW {m,2m+20} UP 2v1). 4th consecutive even-m depth
  (z=3m+12/+14/+16/+18).

## S4 Verification

- Pre-measurement validation: all 49 published kit-18 rows reproduced
  exactly (VALIDATE-PASS 49/49, separation lists + shape counts byte-equal).
- Determinism: 2 full passes (4 chunked runs each) byte-identical over all
  49 rows; PYTHONHASHSEED=random spot chunk byte-identical.
- Audit 10/10 gates PASS, 2 runs byte-identical; tamper 3/3 fail-closed
  (T1 frontier value flip -> G2+G4+G5b / T2 phantom window sep ->
  G2+G5a+G5c / T3 prediction text flip -> G2+G3), clean control rc=0.
- All files ASCII; pins machine-extracted.

## S5 Frozen pins

- census_kit19x.out sha256
  `275faedc80d04e2899c081eb7c56a0bcb80f7cf01b644793c6b846eb3d10a2f4`
  (97,357 bytes)
- engine_block.py sha256 `582c93c1...` (published byte-clone)
- kit-18 registration source sha256 `c3087285...`
- kit dir: `research/experiments/strip-newband-m53m54-blind-second-census-20261127/`

## S6 Honest disclosure

1. Parallel-run detection used only mount file listing + chunk-progress
   status lines; no kit-19 measured content read before freeze.
2. The frozen kit-19 one-past texts omit rule-v2 stack lists (birth texts
   carry them). Measured one-past shadows are exactly the standing rule-v2
   admissible co-splits (per-row: m19:12, m20:11, m21:7, m22:6, m23:5,
   m24:4, m25:3, m26:2, m27..m32:0), each an exact seat mimic; zero other
   separations. Disclosed as a property of the frozen texts, not a defect
   claim.
3. First harness build was OOM-killed (rc 137) without the per-S cache
   clear; fixed with the published kit-18 per-S clear practice
   (values identical, re-validated 49/49).
4. Chunked runs are a wall-time measure; each chunk recomputes from
   scratch (no cross-chunk state).
5. The kit-19 record of record is the parallel lane's kit-19. The
   authoritative published-vs-published cross-check (kit-18x pattern) is
   PENDING until kit-19 lands on main; next execution should run it
   first.

## S7 Resume (re-fetch latest main before starting; hourly parallelism)

1. When kit-19 is on main: run the authoritative cross-check of this frozen
   census vs the published kit-19 `.out` (49/49 rows, all separations;
   kit-18x pattern, machine comparison, publish the result).
2. kit-20's registration source will be the published kit-19 frozen `.out`
   future constants (frontier 42nd/43rd m=55@z=109 / m=56@z=110 candidates,
   windows m=53 z{101..108} / m=54 z{102..109}, ladder next depth, even-m
   z=3m+20 proposal).
3. Standing caveats: 11x11 empty board, all central-reply roots, two-stone
   root {60,27}, third move {100,108}, S2, closure classes 1/2/4 all UNKNOWN
   at all times; verdicts not consumed; the frontier parity scaffold
   42/42, rule-v2 shadows, boundary equistack and even-m templates are
   finite observations, not laws.
