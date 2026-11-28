# n11 twentieth ladder-top k01 WIN-row canonical adoption

Canonical adoption kit for the twentieth ladder-top k01 WIN row
(`10376293541479448576:68719476736`, class 34269, s5 index 38891,
legal 87, WIN(1) nodes 10,752,246 @15M). Declared in
`research/log/2026-11-28-n11-twentieth-ladder-top-k01-adoption-declaration.md`
(commit `35f902c6`, single owner, publish-then-execute).

## New head of record

- `merged-exact-s5-chain-plus-twentieth-k01-20261128.cache`
  sha256 `1f1430f3ef808af78b4919a0aea97b2d5075957603ecc4668ad21b3407a63faa`,
  **6,906 rows WIN 224 / LOSS 6,682** (pre-registered shape
  exactly: 6,905+1 / 223+1 / 6,682+0). Increment
  `increment-twentieth-ladder-top-k01-adoption-20261128.cache` sha256
  `57c5314a931c53bd07d3cf8b0a79f8a3d67157e930285038a19fe653e05a9586`
  (1 WIN row, nodes 10,752,246).
- BASE: `merged-exact-s5-chain-plus-class20421-k05-20261128.cache`
  sha256 `e1a9cacc54abad5198e455ff53492310fabc28f5f89cf26363a7f3da7fe944de`
  (6,905 rows WIN 223 / LOSS 6,682), byte-verified against the
  published class20421 k05 adoption kit output. Merger
  `907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a`
  x3 byte-identical (merge-audit-run1/2/3.json).

## Verification chain (all live inside the fail-closed maker)

- G0 standing pins: merger `90711961`, quarantine `81d23160`,
  policy `78655e94`, BASE `e1a9cacc`, gate source `9193f5b6` +
  headers (gate binary anchor-verified this session, zig 0.13.0,
  tarball pin `d45312e6`).
- Kit MANIFESTs verified for all three source kits (twentieth
  escalation `f04f1fe2`/`44290797`, k01 cppgate
  `c96649db`/`dd9c751a`, k01 thirdimpl `c96649db`/`dd9c751a`,
  published directly in the flat thirdimpl-summary v1 format - no
  reschema amendment needed for this Part).
- G1 live gate re-run: k01 GATE-PASS `87,15000000,1,10752246`
  fresh-cold pair, raw node-exact vs the published kit raw.
- G2 pillar re-parse: replica 15M pair (WIN(1) nodes 10,752,246),
  gate pair, third-impl pair (result 1, expansions 12,569,497)
  all agree with the published rows.
- G3 freshness: k01 absent from BASE, no WIN/LOSS conflict.
- G4 quarantine-free + canonical-safe per s5_evidence_policy.
- G5/G6: increment build, merge x3 byte-identical, shape gates.
- Maker x2 (run1/run2) + clean control: kitout recursive diff
  clean (byte-identical).
- Tamper battery 5/5 fail-closed (see
  `output/tamper-battery-stdout.log`): T1 replica result flip
  (G2 replica pair mismatch), T2 third-impl expansions drift (G2
  third-impl pair mismatch), T3 gate raw flip (caught by the G1
  live re-run), T4 quarantine-key injection with a fully valid
  active registry entry (registry + maker QUAR_SHA re-pinned; G4;
  malformed-entry attempts were themselves caught by the registry
  validation), T5 coherent freshness world (k01 row injected into
  BASE, BASE re-pinned incl. rows/win; G3). Every tamper run
  aborted before any output was written; all inputs restored
  byte-identical, sha-verified.

## Honest disclosures

- Maker = class20421 k05 adoption maker (published in commit
  `fdf1ed8b`, byte-verified raw fetch this session) mechanical
  adaptation (kit name, row constants, BASE/OUT shapes, raw file
  names, budget 15000000, TI_EXPECT, class index 34269,
  comment/manifest strings; assertion chain unchanged; every
  replacement count-asserted, residues grepped - the remaining
  k05/class20421 mentions are intentional lineage references and
  the BASE cache name).
- One post-battery correction: the increment header comment
  inherited a stale k05 string ('adopted node total 2,007,513')
  and was corrected to the k01 value 10,752,246 before
  publication (the data row was always correct; merged head sha
  unchanged `1f1430f3...`; maker re-run x2 byte-identical, new
  increment sha `57c5314a...`). Recorded in the tamper battery
  log.
- This adoption resolves one cost-unknown of the serving class
  34269 (unknown_now 11 -> 10 expected on the flip-census
  reaudit; ladder stay expected, NO class exit). Class 34269 is
  NOT complete; the separately declared WIN-side flip-census
  reaudit measures the k01 owner-class flips exactly (owner
  union precheck [769, 34269], with the standing shared-owner
  pre-exclusion caveat on the owner classes).
- The standard 11x11 empty board, all 19 central-reply roots, the
  two-stone root {60,27} and third moves 100/108 stay UNKNOWN.
  This lane runs without access to the user's computer
  (scheduled task); publication is via the GitHub API only.

## Files

- `adoption-manifest.json` - machine-readable adoption manifest
  (schema `n11-twentieth-ladder-top-k01-win-adoption-manifest-v1`).
- `scripts/make_adoption_twentieth_k01.py` - the fail-closed
  maker (adaptation of the published class20421 k05 maker).
- `output/increment-twentieth-ladder-top-k01-adoption-20261128.cache` -
  the fresh 1-row WIN increment.
- `output/merged/merged-exact-s5-chain-plus-twentieth-k01-20261128.cache`
  - the new head of record (6,906 rows WIN 224 / LOSS 6,682).
- `output/merged/merge-audit-run{1,2,3}.json` - the three
  byte-identical merger audits.
- `output/tamper-battery-stdout.log` - the tamper battery outcome
  log (pre-round + 5/5 fail-closed + clean control).
- `MANIFEST-sha256.txt` - sha256 of every kit file.

## Status guard

Adoption bookkeeping only: NO verdict consumed. Even after
adoption, the k01 row is cache bookkeeping. Class 34269 is NOT
complete until the separately declared WIN-side flip-census
reaudit measures its ladder position. The standard 11x11 empty
board, the 19 central-reply roots, the two-stone root {60,27} and
third moves 100/108 stay UNKNOWN. Nodes/expansions are bookkeeping,
never verdicts.
