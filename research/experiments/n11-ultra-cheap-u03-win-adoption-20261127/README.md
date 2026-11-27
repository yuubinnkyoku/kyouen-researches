# n11 ultra-cheap u03 WIN-row canonical adoption (2026-11-27)

Execution kit of the adoption declared in
`research/log/2026-11-27-n11-ultra-cheap-u03-win-adoption-declaration.md`
(publish-then-execute, declaration commit `3c7bf8d9`).  Adopts exactly
one published row into the canonical head of record:

- u03 `1153202979851993088:272` (class 16371, legal 78, s5 index
  550879) **WIN(1) nodes 2,909,040** - escalation kit
  `n11-ultra-cheap-u03-escalation-15m-20261127` (commit `36f0cd2c`,
  15M cold pair byte-identical) and pillars kit
  `n11-ultra-cheap-u03-win-pillars-20261127` (commit `d6577e97`,
  C++ gate GATE-PASS `78,15000000,1,2909040` with anchors 3/3 and
  tamper 4/4 fail-closed; third_impl `08ea958f` CORROBORATION-PASS
  WIN(1) expansions 3,305,845 x2 identical).

## New head of record

**`merged-exact-s5-chain-plus-ultra-cheap-u03-20261127.cache`**, sha256
`c5082866c1bb61e9cbcb86b80b29c3b2a141b4b5e93a0b8d4b46e04151b631c8`,
**6,893 rows WIN 211 / LOSS 6,682** (288,723 bytes) - exactly the
pre-registered shape (BASE 6,892/210/6,682 + 1 WIN).

- BASE: `82b52577...` (merged-exact-s5-chain-plus-ultra-cheap-u02-20261127.cache,
  6,892 rows WIN 210 / LOSS 6,682), sha-verified; u03 verified fresh.
- Increment: 1 WIN row, sha256 `0796a210...`
  (`output/increment-ultra-cheap-u03-adoption-20261127.cache`).
- Manifest: `adoption-manifest.json` sha256 `f09075f0...` (schema
  n11-ultra-cheap-u03-win-adoption-manifest-v1).
- Merger `90711961...` x3 byte-identical (merge-audits `499b7ff8...` x3).

## Gates (all PASS, fail-closed; maker x2 byte-identical)

G0 pins (merger/policy/quarantine/BASE head/gate source+headers) +
published-kit MANIFEST self-verification (escalation + pillars kits);
G1 LIVE re-run of the published gate_runner.sh on a scratch pillar
copy (2 fresh-cold C++ passes, node-exact vs the published raws);
G2 three-pillar re-parse (replica pair, C++ gate pair, third_impl
pair, verdict/legal/key checks); G3 freshness (u03 absent from BASE) +
no duplicates + no WIN/LOSS conflicts; G4 quarantine-free +
canonical-safe per s5_evidence_policy; G5 increment build; G6 merger
x3 + shape check.  Both maker runs (post-declaration) produced
byte-identical outputs (`fad5c8ea...` x2).

## Disclosures

- The gate binary was rebuilt from the pinned source `9193f5b6...` in
  this execution environment (binary provenance disclosed in the
  declaration); the live gate re-run re-verified the anchors and the
  target row node-exact against the published raws.
- The u03 key is NOT the u04 key: u04 (`1152921505747697664:1032`,
  class 23101) stays UNKNOWN at 2M (escalation-suppressed at the u03
  escalation, WIN-stop rule).

## Status guard

Adoption bookkeeping only: the adopted row is cache bookkeeping, NOT
a class closure, NOT a root verdict, transfers nothing.  The
WIN-side flip-census review of the u03 row's owner-class union (class
16371 completion would be Board-verified free_now at adoption time)
is the declared follow-up Part of this lane (u01/u02 precedent).  The
standard 11x11 empty board, the two-stone root {60,27} and its
remaining third moves 100/108 stay UNKNOWN.
