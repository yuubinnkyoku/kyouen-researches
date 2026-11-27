# n11 ultra-cheap u03 WIN-row canonical adoption completion (2026-11-27)

Completion log of the adoption declared in
`research/log/2026-11-27-n11-ultra-cheap-u03-win-adoption-declaration.md`
(commit `3c7bf8d9`).  Kit:
`research/experiments/n11-ultra-cheap-u03-win-adoption-20261127/`
(commit `ab50c3ca`, fetch-back 9/9 git-blob-sha identical including the
288,723-byte merged cache).

## Outcome

- **New head of record:
  `merged-exact-s5-chain-plus-ultra-cheap-u03-20261127.cache`**, sha256
  `c5082866c1bb61e9cbcb86b80b29c3b2a141b4b5e93a0b8d4b46e04151b631c8`,
  **6,893 rows WIN 211 / LOSS 6,682** - exactly the pre-registered shape
  (6,892+1 / 210+1 / 6,682+0).
- Increment: 1 WIN row
  `s5verdict,1153202979851993088,272,5,1,2909040`
  (increment sha256 `0796a210...`).
- BASE: `82b52577...` (u02 head, 6,892 rows WIN 210 / LOSS 6,682).
- MAKER-PASS x2 (all outputs byte-identical between runs,
  `fad5c8ea...` x2); merger `90711961...` x3 byte-identical
  (merge-audit `499b7ff8...` x3).

## Gates (all PASS, fail-closed)

G0 pins + published-kit MANIFEST self-verification (escalation
`36f0cd2c` + pillars `d6577e97` kits); G1 live gate_runner re-run on a
scratch copy (`u03 GATE-PASS 78,15000000,1,2909040`, 2 fresh-cold C++
passes node-exact vs the published raws); G2 three-pillar re-parse
(replica 15M cold pair byte-identical, C++ gate pair, third_impl pair
WIN(1) expansions 3,305,845 x2 clean); G3 freshness (u03 absent from
BASE) + no duplicates + no WIN/LOSS conflicts; G4 quarantine-free +
canonical-safe; G5/G6 increment + merge x3 + shape check.

## Disclosures

- The gate binary was rebuilt from the pinned source `9193f5b6...` in
  this execution environment (binary provenance disclosed in the
  declaration); the live re-run re-verified anchors and target
  node-exact.
- u04 (`1152921505747697664:1032`, class 23101) stays UNKNOWN at 2M
  (escalation-suppressed at the u03 escalation by the WIN-stop rule);
  its re-escalation requires a future declaration.

## Status guard

Adoption bookkeeping only: the adopted row is cache bookkeeping, NOT
a class closure, NOT a root verdict, transfers nothing.  The WIN-side
flip-census review of the u03 row's owner-class union (class 16371
completion would be Board-verified free_now at adoption time) is the
declared follow-up Part of this lane (u01/u02 precedent).  The
standard 11x11 empty board, the two-stone root {60,27} and its
remaining third moves 100/108 stay UNKNOWN.
