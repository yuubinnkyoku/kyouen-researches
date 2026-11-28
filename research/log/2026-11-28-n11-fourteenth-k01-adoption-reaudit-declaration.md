# 2026-11-28 n11 fourteenth k01 adoption reaudit (flip-census/refresh) declaration

Single-owner declaration (publish-then-execute) for the WIN-side
flip-census/reaudit Part of the fourteenth ladder-top class-5804 k01
canonical adoption, declared as follow-up in the adoption completion
log (e1f8f904, kit n11-fourteenth-ladder-top-k01-adoption-20261128);
this lane is the declared owner of this Part.  Declaration published
at main HEAD e1f8f904 before any of the declared computation runs.

## Pre-registered plan and predictions

- SCENARIO cache (measured head of record):
  `merged-exact-s5-chain-plus-fourteenth-k01-20261128.cache`
  sha256 `a66f636ed4314b7385b713ed6e24798409db0b284eb252a9bda626ad3dcd67dc`
  (6,897 rows WIN 215 / LOSS 6,682), adopted at 4f0ba5c9 + fix
  0139fd4c (read-cap truncation republished full).
- BASE for the census comparison: d772f73c (6,896 rows WIN 214 /
  LOSS 6,682, thirteenth k01+k02 head of record, measured by the
  published thirteenth reaudit kit): refresh-summary 0d02503c,
  closure-classes be8bcff1 (800 rows), per-root 96cf51b7,
  census json 7b6027d3, BASE worklist regen pin da2d22e1
  (3,714,716 B, unpublished per size policy).
- The refresh is a byte-clone of the published thirteenth
  adoption-reaudit refresh (kit n11-thirteenth-k01k02-adoption-
  reaudit-20261128, script sha c24e9072) differing in EXACTLY three
  regions (docstring, CACHE path, expected cache sha); every
  computation byte identical.  Three sequential runs must be
  byte-identical (fail-closed otherwise).
- Adopted row (increment c87d9afb, manifest 845031dd):
  k01 `6053401124017274880:0`, WIN(1) nodes 4,360,661, s5 index
  198576, legal 86, serving class 5804 (mask 6053400849139367936:0).
- Pre-registered census prediction (from the owner-union precheck
  kit n11-fourteenth-owner-union-precheck-20261128, 509afbdb): the
  naive graph-derived owner-union flip prediction is [5308, 5804,
  8811] all unknown -> excluded_now, expected census unknown
  34,374 -> 34,371, excluded_now 146 -> 149, free_now 39 -> 39.
  Caveats (pre-registered): (a) u03 precedent - an owner class may
  already be excluded_now on the BASE side; census status must be
  measured, not assumed; (b) unlike the thirteenth case the serving
  class 5804 is NOT pre-excluded (it is the rank-1 closure ladder
  row with unknown_now 4), so a genuine serving-class
  unknown -> excluded_now flip is expected while the class STAYS in
  the ladder (unknown_now 4 -> 3, NOT a ladder exit, per the
  precheck measurement); (c) owner 8811 is itself a ladder row
  (rank 17, unknown_now 52) - its census status and any ladder
  unknown_now churn must be measured; (d) the measurement decides;
  deviations replace the naive prediction without adjustment.
- Dependency pins (all pre-verified sha256 on this host before the
  computation): frozen dependency graph 54f9c364, update8
  repaired-joint-plan b658290a, independent.py 954d3a10,
  s5_evidence_policy 78655e94, quarantine registry 81d23160,
  merger 90711961, BASE cache d772f73c, SCEN cache a66f636e,
  increment c87d9afb, adoption manifest 845031dd.
- Measurer: structural descendant of the published thirteenth
  measurer (d5263fc7), assertions adapted to the fourteenth
  adoption; expected values are pre-measured on this host from the
  declared refresh outputs before the final 3-run byte-identical
  gate (u03 precedent).  Tamper battery fail-closed.

## Claim status

Flip-census/class-status bookkeeping only: NO verdict consumed, no
class closure, no coverage claim.  The standard 11x11 empty board,
all 19 central-reply roots, the two-stone root {60,27}, the
third-move pair {100,108} and every closure class stay UNKNOWN.
Nodes are bookkeeping, never verdicts.
