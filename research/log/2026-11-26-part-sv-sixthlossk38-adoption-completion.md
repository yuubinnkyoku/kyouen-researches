# n11 sixthlossk38 LOSS-only canonical adoption: completion log (2026-11-26)

Part SV closes complete. Closes the single-owner fresh declaration
research/log/2026-11-26-part-sv-sixthlossk38-adoption-declaration.md
(wave A push c9cd786d), executing the canonical adoption of the last
standing unconsumed loss-resolved row of the sixth-cost exclusive S5
probe batch (k38) into the central-reply merged exact-S5 chain.

## Outcome

LOSS-only canonical adoption, head of record advanced. The single
fresh exact-LOSS row k38 `10376293541461626880:66048` (legal 100,
nodes 21,839,049 cold two-pass node-exact at the pinned 50,000,000
budget; C++-gated by the Part SS GATE-PASS target quadruple
100,50000000,2,21839049; third-implementation-corroborated LOSS(2) by
Part SU with auditor re-run live 31/31 x2 byte-identical) is consumed
into the canonical chain via the fail-closed union merger byte-clone:

- BASE = the Part ST head of record (sha256 dade15780..., 6,831 rows
  WIN 201 / LOSS 6,630, 285,726 B) -> new head of record
  merged-exact-s5-chain-plus-sixthlossk38-20261126.cache (sha256
  42dbb58f..., 6,832 rows WIN 201 / LOSS 6,631, 285,776 B), reproduced
  3/3 byte-identical runs, WIN/LOSS conflict-free
  (base_cache_absent_hits_for_emitted 0, quarantine_hits 0).
- increment = 1 LOSS row (sha256 977780ef...), adopted-table digest
  75a45f99...; SSOT pins in increments-manifest.json (sha256
  2619f1b3..., schema sixthlossk38-adoption-increments-manifest-v1).
- The maker's merged_cache_bytes is measured live with a fail-closed
  gate (the draft's hardcoded byte count was wrong by 7 B; fixed
  before publication, manifest regenerated; the head sha 42dbb58f
  was correct throughout).

NO verdict transfer: LOSS-only adoption flips no root verdict, frees
no class, excludes no class and changes no coverage claim
(status_flip_count = 0, verified). Census unchanged at 34,405
unknown / 115 excluded_now / 39 free_now / 390 excluded; serving
class 3077 stays excluded_now with cost-unknown 61 -> 60; closure
ladder, per-root coverage and probe worklist measured byte-identical
to BASE (joint greedy 36,789 unchanged; worklist_total 64,275
unchanged, regen pin b946ed06... 3,715,960 B identical BASE/SCEN);
update8 refresh resolved 281 / remaining 31,445 identical.

With this Part the sixth-cost probe batch has ZERO standing
unconsumed loss-resolved rows (standing_unconsumed_parked_keys = 0).
The next adoption Part against the new BASE 42dbb58f has no fresh
loss-resolved candidate on the table; the lane returns to the
adaptive coordinator for the next certificate/probe selection.

## Waves (fetch-back byte-verified by git blob sha)

- Wave A declaration: commit `c9cd786d` (fetch-back identical).
- Wave B kit scripts (3): commit `2bb3a4bf` (fetch-back: merger
  90711961 / maker 15b1ed74 / measurer 2695e618, all blob-identical).
- Wave C kit output (7): commit `7fc923d9`. Fetch-back found a real
  publication defect: the census and manifest blobs did not match the
  local generator output because the publishing step had round-tripped
  the JSON through JS Number precision, corrupting the 20-digit key
  10376293541461626880 to 10376293541461627000 (same byte
  length, different digits). The increment cache, the three merge
  audits and the merged head (998b98e8..., 285,776 B) were verified
  blob-identical and unaffected.
- Wave C2 correction: commit `28211442` republished census
  dc3d4e3c and manifest 2619f1b3 byte-exact; all 7 output blobs now
  match the local git blob shas exactly. The sha256 pins of record
  (in the wave A declaration) were never wrong.
- Wave D reaudit + kit front matter: commit `4ca5e51c` (refresh
  runner 9500cc66, refresh-summary 451c1e36, closure-classes
  0eb19c89 and per-root-coverage 1828d7f7 both byte-identical to the
  published BASE state, kit README.md and MANIFEST-sha256.txt with
  14 file pins and the wave C2 correction of record); all 6 blobs
  fetch-back verified.
- Wave F: this completion log.

## Reaudit record

`reaudit/scripts/refresh_adoption_sixthlossk38.py` (sha256
9500cc66..., structural clone of the Part ST refresh runner with the
k38 scenario deltas) re-derives the closure ladder, per-root coverage
and probe worklist against the SCEN head 42dbb58f and asserts them
byte-identical to the published BASE state (zero churn, zero
re-routing). Output refresh-summary.json (sha256 451c1e36...).
The probe worklist (3,715,960 B) is not published (size policy); both
BASE and SCEN regen pins are identical (b946ed06...).

## Verdict status

The standard 11x11 empty board: UNKNOWN. All 19 central-reply roots:
UNKNOWN. Two-stone root {60,27}: UNKNOWN. Third-move pair {100,108}:
UNKNOWN. Every closure class: UNKNOWN unless a published Part says
otherwise. This Part consumes exactly 1 exact-LOSS leaf row and
nothing else; nodes are bookkeeping, never verdicts; no partial,
pn/dn or node-count value is read as a verdict.
