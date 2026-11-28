# n11 eighteenth ladder-top k03 WIN-row canonical adoption

Canonical adoption kit for the eighteenth class 20421 k03 WIN row
(`1155173441859489792:131072`, class 20421, s5_index 605961, legal 73,
WIN(1) nodes 5,266,012 @15M). Declared in
`research/log/2026-11-28-n11-eighteenth-ladder-top-k03-adoption-declaration.md`
(commit `7fe49b5e`, single owner, publish-then-execute, HEAD pin
`59143099`; the same commit published the thirdimpl summary reschema
amendment).

## New head of record

- `merged-exact-s5-chain-plus-eighteenth-k03-20261128.cache`
  sha256 `3abecf8b1da6735a0cf0719087b0f026e3a82648dce026b9c82aab106e23a023`,
  **6,903 rows WIN 221 / LOSS 6,682** (pre-registered shape exactly:
  6,902+1 / 220+1 / 6,682+0). Increment
  `increment-eighteenth-k03-adoption-20261128.cache` sha256 `c208891e...`
  (1 WIN row, nodes 5,266,012).
- BASE: `merged-exact-s5-chain-plus-seventeenth-k02-20261128.cache`
  sha256 `e56ca5ca...` (6,902 rows WIN 220 / LOSS 6,682), byte-fetched
  from main and pin-verified. Merger `90711961...` x3 byte-identical
  (merge-audit-run1/2/3.json).

## Verification chain (all live inside the fail-closed maker)

- G0 standing pins: merger `90711961`, quarantine `81d23160`,
  policy `78655e94`, BASE `e56ca5ca`, gate source `9193f5b6` +
  headers `5976935d`/`2e36d694` (gate binary as anchor-verified this
  session, zig 0.13.0, tarball pin `d45312e6`).
- Kit MANIFESTs verified for all three source kits (eighteenth
  escalation `88e825d5`, k03 cppgate `3549edde`, k03 thirdimpl
  `3549edde` with the summary reschema amendment `7fe49b5e`).
- G1 live gate re-run: k03 GATE-PASS `73,15000000,1,5266012`
  fresh-cold pair, raw node-exact vs the published kit raw.
- G2 pillar re-parse: replica 15M pair, gate pair, third-impl pair
  (result 1, expansions 6,039,011) all agree with the published rows.
- G3 freshness: k03 absent from BASE, no WIN/LOSS conflict.
- G4 quarantine-free + canonical-safe per s5_evidence_policy.
- G5/G6: increment build, merge x3 byte-identical, shape gates.
- Maker x2 (run1/run2) + clean control: kitout recursive diff clean
  (byte-identical).
- Tamper battery 5/5 fail-closed (see `output/tamper-battery-stdout.log`):
  T1 replica result flip, T2 third-impl expansions drift, T3 gate raw
  quad flip (caught by the G1 live re-run), T4 quarantine-key
  injection with fully valid active registry entry (registry + maker
  QUAR_SHA re-pinned), T5 coherent freshness world (k03 row injected
  into BASE, BASE re-pinned incl. rows/win). Every tamper run aborted
  before any output was written (kitout absent).

## Honest disclosures

- One kit fix was needed before the maker chain: the thirdimpl kit's
  `output/pillars-summary.json` was reschemad to the standing flat
  thirdimpl-summary v1 format (top-level result/expansions fields
  required by the maker's G2 cross-check); all VALUES unchanged;
  published as an amendment with the adoption declaration (commit
  `7fe49b5e`) and disclosed there.
- Maker = seventeenth k02 adoption maker (kit `859e2598`, script
  `c3cd7e1b`) mechanical adaptation (kit name, row constants, BASE/OUT
  shapes, raw file names at15m, budget 15000000, TI_EXPECT, class
  index 20421, comment/manifest strings; assertion chain unchanged;
  every replacement count-asserted, residues grepped - the 14
  remaining ancestor-name mentions are intentional lineage
  references).
- Class 20421 is NOT complete: k04 `1153062242096250880:540672`,
  k05 `1152921642046849024:68719477248` remain stage-1 2M UNKNOWN;
  no closure-ladder exit is expected from this adoption (serving
  class 20421 stays in the ladder with 2 cost-unknown children).
- The WIN-side flip-census/reaudit of the owner classes
  ([18136, 18143, 20128, 20421] precheck from the frozen graph, with the
  standing shared-owner pre-exclusion caveat) is a SEPARATE declared
  follow-up Part.
- This lane runs without access to the user's computer (scheduled
  task); publication is via the GitHub API only.

## Non-claims / status guard

- NO verdict consumed. The adopted row is cache bookkeeping only.
- The standard 11x11 empty board, the 19 central-reply roots,
  two-stone root {60,27}, third move {100,108}, and every closure
  class remain UNKNOWN. nodes are bookkeeping, never verdicts.

## Files

- `adoption-manifest.json` - machine-readable manifest (schema
  `n11-eighteenth-ladder-top-k03-win-adoption-manifest-v1`).
- `output/increment-eighteenth-k03-adoption-20261128.cache` - the
  1-row WIN increment.
- `output/merged/merged-exact-s5-chain-plus-eighteenth-k03-20261128.cache`
  - the new head of record (289,195 B).
- `output/merged/merge-audit-run{1,2,3}.json` - merger audits
  (byte-identical outputs).
- `output/tamper-battery-stdout.log` - honest tamper record.
- `scripts/make_adoption_eighteenth_k03.py` - the fail-closed maker.
- `MANIFEST-sha256.txt` - sha256 of every kit file.
