# n11 ultra-cheap u04 WIN-row canonical adoption (2026-11-27)

Execution kit of the adoption declared in
`research/log/2026-11-27-n11-ultra-cheap-u04-win-adoption-declaration.md`
(publish-then-execute, declaration commit `218634ca`).  Adopts exactly
one published row into the canonical head of record:

- u04 `1152921505747697664:1032` (class 23101, legal 85, s5 index
  745184) **WIN(1) nodes 9,149,084** - escalation kit
  `n11-ultra-cheap-u04-escalation-15m-20261127` (commit `24c5b85f`,
  15M cold pair byte-identical), C++ scrutiny gate kit
  `n11-ultra-cheap-u04-win-cppgate-20261127` (commit `378ec332`,
  GATE-PASS `85,15000000,1,9149084` with anchors 3/3 and tamper 4/4
  fail-closed) and third-impl corroboration kit
  `n11-ultra-cheap-u04-thirdimpl-20261127` (commit `2691ac04`,
  CORROBORATION-PASS WIN(1) expansions 10,728,035 x2 identical).

This completes the ultra-cheap 4-key family: **u01, u02, u03 and u04
are all now adopted** into the canonical chain.

## New head of record

**`merged-exact-s5-chain-plus-ultra-cheap-u04-20261127.cache`**, sha256
`beecb024a648d0ddb29eaf261b09326f9412328cd09f85cb180ee2ffd9ed4544`,
**6,894 rows WIN 212 / LOSS 6,682** (288,770 bytes) - exactly the
pre-registered shape (BASE 6,893/211/6,682 + 1 WIN).

- BASE: `c5082866...` (merged-exact-s5-chain-plus-ultra-cheap-u03-20261127.cache,
  6,893 rows WIN 211 / LOSS 6,682), sha-verified; u04 verified fresh.
- Increment: 1 WIN row, sha256 `c6344d3a...`
  (`output/increment-ultra-cheap-u04-adoption-20261127.cache`).
- Manifest: `adoption-manifest.json` sha256 `3241759f...` (schema
  n11-ultra-cheap-u04-win-adoption-manifest-v1).
- Merger `90711961...` x3 byte-identical (merge-audits `077e10bf...`
  x3).

## Gates (all PASS, fail-closed; maker x2 byte-identical)

G0 pins (merger/policy/quarantine/BASE head/gate source+headers) +
published-kit MANIFEST self-verification (escalation + cppgate +
thirdimpl kits); G1 LIVE re-run of the published gate_runner.sh on a
scratch kit copy (2 fresh-cold C++ passes, node-exact vs the
published raws); G2 three-pillar re-parse (replica pair, C++ gate
pair, third_impl pair + third-impl summary cross-check,
verdict/legal/key/expansions checks); G3 freshness (u04 absent from
BASE) + no duplicates + no WIN/LOSS conflicts; G4 quarantine-free +
canonical-safe per s5_evidence_policy; G5 increment build; G6 merger
x3 + shape check.  Both maker runs (post-declaration) produced
byte-identical outputs (merged sha256 `beecb024...` x2, kitout
byte-identical by recursive diff).

## Disclosures

- The gate binary was rebuilt from the pinned source `9193f5b6...` in
  this execution environment (zig 0.13.0, tarball pin `d45312e6...`);
  the live gate re-run re-verified the target row node-exact against
  the published raws (G1).
- One in-session environment hiccup is recorded: a maker invocation
  without GATE_BIN exported and a rerun against a stale gaterun
  scratch were both caught fail-closed by the maker's own gates
  (no output written on either failed attempt).
- The u04 row is the last of the four ultra-cheap keys; no other key
  is adopted by this Part.

## Status guard

Adoption bookkeeping only: the adopted row is cache bookkeeping, NOT
a class closure, NOT a root verdict, transfers nothing.  The
WIN-side flip-census review of the u04 row's owner-class union
(serving class 23101 completion must be Board-verified free_now at
adoption time) is the declared follow-up Part of this lane
(u01/u02/u03 precedent).  The standard 11x11 empty board, the
two-stone root {60,27} and its remaining third moves 100/108 stay
UNKNOWN.
