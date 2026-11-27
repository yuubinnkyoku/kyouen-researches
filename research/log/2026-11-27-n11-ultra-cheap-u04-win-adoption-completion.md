# Completion: n11 ultra-cheap u04 WIN-row canonical adoption

Declaration `218634ca` -> kit `n11-ultra-cheap-u04-win-adoption-20261127`
(commits `ed1aab54` + merged cache `04b8c23a`, fetch-back 8/8
byte-identical vs MANIFEST-sha256).

## New head of record

**`merged-exact-s5-chain-plus-ultra-cheap-u04-20261127.cache`**,
sha256 `beecb024a648d0ddb29eaf261b09326f9412328cd09f85cb180ee2ffd9ed4544`,
**6,894 rows WIN 212 / LOSS 6,682** - exactly the pre-registered
shape (BASE `c5082866...` 6,893/211/6,682 + 1 WIN).

- Increment: 1 WIN row (u04 `1152921505747697664:1032`, class 23101),
  sha256 `c6344d3a...`.
- Merger `90711961...` x3 byte-identical (merge-audits
  `077e10bf...` x3).  Adoption manifest `3241759f...` (schema
  n11-ultra-cheap-u04-win-adoption-manifest-v1).
- **The ultra-cheap 4-key family (u01/u02/u03/u04) is now fully
  adopted** into the canonical chain.

## Maker gates (all PASS, fail-closed; x2 byte-identical)

G0 pins (merger/policy/quarantine/BASE/gate source+headers) + 3
published-kit MANIFEST self-verification; G1 LIVE re-run of the
published gate_runner.sh (scratch copy, 2 fresh-cold C++ passes,
node-exact vs published raws); G2 three-pillar re-parse (replica pair
`85,15000000,1,9149084`, C++ gate pair, third_impl pair expansions
10,728,035 + summary cross-check); G3 freshness (u04 absent from
BASE) + no duplicates + no WIN/LOSS conflicts; G4 quarantine-free +
canonical-safe; G5 increment; G6 merger x3 + shape.  Both maker runs
byte-identical (kitout recursive diff identical).

## Disclosures

- Two fail-closed maker aborts are recorded in-session (missing
  GATE_BIN env; stale gaterun scratch guard) - both caught by the
  maker's own gates before any output was written.
- Gate binary rebuilt from pinned source `9193f5b6...` (zig 0.13.0,
  pin `d45312e6...`), provenance disclosed in the declaration.

## Status guard

Adoption bookkeeping only; NO verdict consumed; the adopted row is
NOT a class closure, NOT a root verdict, transfers nothing.  The
WIN-side flip-census/reaudit of the u04 owner-class union (serving
class 23101 completion Board-verified free_now at adoption time) is
the declared follow-up Part.  The standard 11x11 empty board, the
two-stone root {60,27} and its remaining third moves 100/108 stay
UNKNOWN.
