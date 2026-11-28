# n11 class-20421 k05 WIN-row canonical adoption

Canonical adoption kit for the class-20421 k05 WIN row
(`1152921642046849024:68719477248`, class 20421, s5 index 625899,
legal 78, WIN(1) nodes 2,007,513 @15M). Declared in
`research/log/2026-11-28-n11-class20421-k05-adoption-declaration.md`
(commit `cf6a21a6`, single owner, publish-then-execute).

## New head of record

- `merged-exact-s5-chain-plus-class20421-k05-20261128.cache`
  sha256 `e1a9cacc54abad5198e455ff53492310fabc28f5f89cf26363a7f3da7fe944de`,
  **6,905 rows WIN 223 / LOSS 6,682** (pre-registered shape
  exactly: 6,904+1 / 222+1 / 6,682+0). Increment
  `increment-class20421-k05-adoption-20261128.cache` sha256
  `6b525957...` (1 WIN row, nodes 2,007,513).
- BASE: `merged-exact-s5-chain-plus-nineteenth-k04-20261128.cache`
  sha256 `8cc87263...` (6,904 rows WIN 222 / LOSS 6,682),
  byte-verified against the published nineteenth k04 adoption kit
  output. Merger `90711961...` x3 byte-identical
  (merge-audit-run1/2/3.json).

## Verification chain (all live inside the fail-closed maker)

- G0 standing pins: merger `90711961`, quarantine `81d23160`,
  policy `78655e94`, BASE `8cc87263`, gate source `9193f5b6` +
  headers `5976935d`/`2e36d694` (gate binary as anchor-verified
  this session, zig 0.13.0, tarball pin `d45312e6`).
- Kit MANIFESTs verified for all three source kits (class20421-k05
  escalation `ddff08ce`/`9a87750e`, k05 cppgate
  `772c04bc`/`c34e82ee`, k05 thirdimpl `772c04bc`/`c34e82ee`,
  published directly in the flat thirdimpl-summary v1 format - no
  reschema amendment needed for this Part).
- G1 live gate re-run: k05 GATE-PASS `78,15000000,1,2007513`
  fresh-cold pair, raw node-exact vs the published kit raw.
- G2 pillar re-parse: replica 15M pair, gate pair, third-impl pair
  (result 1, expansions 2,292,427) all agree with the published
  rows.
- G3 freshness: k05 absent from BASE, no WIN/LOSS conflict.
- G4 quarantine-free + canonical-safe per s5_evidence_policy.
- G5/G6: increment build, merge x3 byte-identical, shape gates.
- Maker x2 (run1/run2) + clean control: kitout recursive diff
  clean (byte-identical).
- Tamper battery 5/5 fail-closed (see
  `output/tamper-battery-stdout.log`): T1 replica result flip
  (G2 replica pair mismatch), T2 third-impl expansions drift (G2
  third-impl pair mismatch), T3 gate raw quad flip (caught by the
  G1 live re-run), T4 quarantine-key injection with a fully valid
  active registry entry (registry + maker QUAR_SHA re-pinned; G4),
  T5 coherent freshness world (k05 row injected into BASE, BASE
  re-pinned incl. rows/win; G3). A disclosed pre-round without
  MANIFEST re-pins caught T1-T3 fail-closed at the kit MANIFEST
  gate; the repinned probes then reached their intended deeper
  gates. Every tamper run aborted before any output was written
  (kitout absent); all inputs restored byte-identical,
  sha-verified.

## Honest disclosures

- Maker = nineteenth k04 adoption maker (published in commit
  `a03e21ef`, byte-verified raw fetch this session) mechanical
  adaptation (kit name, row constants, BASE/OUT shapes, raw file
  names at15m, budget 15000000, TI_EXPECT, class index 20421,
  comment/manifest strings; assertion chain unchanged; every
  replacement count-asserted, residues grepped - the remaining
  nineteenth/k04 mentions are intentional lineage references and
  the BASE cache name).
- This adoption closes the last cost-unknown of the serving class
  20421 (unknown_now 1 -> 0 expected on the flip-census reaudit).
  Class 20421 is NOT complete until the separately declared
  WIN-side flip-census/reaudit measures the closure-ladder EXIT
  exactly (owner union [18683, 18710, 20421], with the standing
  shared-owner pre-exclusion caveat on the owner classes).
- The standard 11x11 empty board, all 19 central-reply roots, the
  two-stone root {60,27} and third moves 100/108 stay UNKNOWN.
  This lane runs without access to the user's computer
  (scheduled task); publication is via the GitHub API only.

## Files

- `adoption-manifest.json` - machine-readable adoption manifest
  (schema `n11-class20421-k05-win-adoption-manifest-v1`).
- `scripts/make_adoption_class20421_k05.py` - the fail-closed
  maker (adaptation of the published nineteenth k04 maker).
- `output/increment-class20421-k05-adoption-20261128.cache` - the
  fresh 1-row WIN increment.
- `output/merged/merged-exact-s5-chain-plus-class20421-k05-20261128.cache`
  - the new head of record (6,905 rows WIN 223 / LOSS 6,682).
- `output/merged/merge-audit-run{1,2,3}.json` - the three
  byte-identical merger audits.
- `output/tamper-battery-stdout.log` - the tamper battery outcome
  log (pre-round + 5/5 fail-closed + clean control).
- `MANIFEST-sha256.txt` - sha256 of every kit file.

## Status guard

Adoption bookkeeping only: NO verdict consumed. Even after
adoption, the k05 row is cache bookkeeping. Class 20421 is NOT
complete until the separately declared WIN-side flip-census
reaudit measures the ladder EXIT. The standard 11x11 empty board,
the 19 central-reply roots, the two-stone root {60,27} and third
moves 100/108 stay UNKNOWN. Nodes/expansions are bookkeeping,
never verdicts.
