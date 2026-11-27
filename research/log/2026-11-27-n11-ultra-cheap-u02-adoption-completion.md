# n11 ultra-cheap u02 WIN-row canonical adoption completion (2026-11-27)

Completion log of the adoption declared in
`research/log/2026-11-27-n11-ultra-cheap-u02-adoption-declaration.md`
(commit `6522b9b6`).  Kit:
`research/experiments/n11-ultra-cheap-u02-win-adoption-20261127/`
(commit `612cb3c2`, fetch-back 8/8 git-blob-sha identical including the
288,677-byte merged cache).

## Outcome

- **New head of record:
  `merged-exact-s5-chain-plus-ultra-cheap-u02-20261127.cache`**, sha256
  `82b525777843ecb44c3857b034f7a135284c2587b42dbaa94aa295b01adc7509`,
  **6,892 rows WIN 210 / LOSS 6,682** - exactly the pre-registered shape
  (6,891+1 / 209+1 / 6,682+0).
- Increment: 1 WIN row
  `s5verdict,1297036830121656320,131074,5,1,3167121`
  (increment sha256 `ef727442...`).
- BASE: `0ec4080d...` (u01 head, 6,891 rows WIN 209 / LOSS 6,682).
- MAKER-PASS x2 (all outputs byte-identical between runs); merger
  `90711961...` x3 byte-identical (merge-audit
  `b9ef4e04...` x3).

## Gates (all PASS, fail-closed)

G0 pins + 26-file kit MANIFEST self-verification; G1 live gate_runner
re-run on a scratch copy (`u02 GATE-PASS 80,15000000,1,3167121`, 2
fresh-cold C++ passes node-exact vs the published raws); G2 three-pillar
re-parse (replica cold pair byte-identical, C++ gate pair, third_impl
pair WIN(1) expansions 3,595,562 legal 80 clean); G3 freshness (u02
absent from BASE) + no duplicates + no WIN/LOSS conflicts; G4
quarantine-free + canonical-safe; G5/G6 increment + merge x3 +
shape check.

## Disclosures

- First maker run fail-closed on G0 ("missing MANIFEST"): the kitbuild
  fetch had skipped the published kits' own MANIFEST files; they were
  fetched and the passing runs executed.  No output was written by the
  failed run.
- The gate binary emits a zig glibc-version warning (host 2.41 vs
  provided 2.39); all rows ran to replay_done.

## Status guard

Adoption bookkeeping only: the adopted row is cache bookkeeping, NOT a
class closure, NOT a root verdict, transfers nothing.  The WIN-side
flip-census review of the u02 row's owner-class union (class 2251
completion would be Board-verified free_now at adoption time) is the
declared follow-up Part of this lane (u01 precedent
`n11-ultra-cheap-u01-adoption-reaudit-20261127`).  The standard 11x11
empty board, the two-stone root {60,27} and its remaining third moves
100/108 stay UNKNOWN.
