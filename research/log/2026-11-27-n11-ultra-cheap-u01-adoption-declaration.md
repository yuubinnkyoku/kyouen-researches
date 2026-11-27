# n11 ultra-cheap u01 WIN-row canonical adoption: single-owner declaration

**Declaration (publish-then-execute).** This lane declares the canonical
adoption of the ultra-cheap u01 WIN row
(`1153485622925590528:0`, class 1849, legal 88, s5_index 81011,
nodes 4,893,014 bookkeeping), whose 3/3 pillars are complete and
published (replica cold pair: batch kit
`n11-ultra-cheap-batch-stage1-2m-20261127` commit `a99be0f8`; C++
scrutiny gate + third-implementation corroboration: pillars kit
`n11-ultra-cheap-u01-win-pillars-20261127` commit `8dab30d6`,
MANIFEST repairs `abbc1edb`).

## What this Part consumes

Exactly one row: u01 WIN(1).  BASE = canonical head of record
`1e2eeda2...` (6,890 rows WIN 208 / LOSS 6,682).  Pre-registered
merged shape: **6,891 rows WIN 209 / LOSS 6,682**
(`merged-exact-s5-chain-plus-ultra-cheap-u01-20261127.cache`).

## Maker protocol (eleventh single-row adoption template)

Fresh maker (structural descendant of the published eleventh k01
adoption maker), fail-closed gates:

- G0 pins: merger `90711961...`, policy `78655e94...`, quarantine
  `81d23160...`, BASE `1e2eeda2...`, gate source `9193f5b6...` +
  headers `5976935d...`/`2e36d694...`; both source kit MANIFESTs
  fully re-verified from byte-fetched copies.
- G1 (adapted, disclosed): this lane's pillar kit ships the runner +
  raws + tamper battery instead of a separate audit script, so G1 is a
  LIVE re-run of the published gate_runner.sh on a scratch copy (2
  fresh-cold C++ passes, quadruple `88,15000000,1,4893014`, raw
  node-exact vs published).  The gate binary is the one built this
  session by this lane from the sha-verified pinned source with zig
  0.13.0 (`d45312e6...`), `-std=c++20 -O3`; binary provenance is by
  this disclosure plus the live node-exact re-run, not by a rebuild
  inside the maker.
- G2: re-parse of all three pillars (replica 15M cold pair, C++ gate
  pair, third-impl pair).
- G3: freshness (u01 absent from BASE), duplicate-key check, WIN/LOSS
  conflict review vs BASE.
- G4: quarantine-free and canonical-safe per s5_evidence_policy.
- G5: increment + adoption-manifest.
- G6: merger 3 runs byte-identical with audits; merged shape exactly
  as pre-registered.

Three maker runs required byte-identical (increment, manifest, merged
cache, audits).

## Scope and non-scope

This Part advances the head of record by exactly this one row.  The
class 1849 completion (free_now at adoption time) is NOT claimed here:
the flip-census/reaudit review is the next follow-up Part (SZ/ninth/
tenth/eleventh precedent), under its own declaration.  NO root verdict
is consumed: the standard 11x11 empty board, all 19 central-reply
roots, the two-stone root {60,27} and its remaining third moves
100/108 stay UNKNOWN.  Nodes are bookkeeping, never evidence.

This lane runs without access to the user's computer (scheduled task);
publication via the GitHub API only.
