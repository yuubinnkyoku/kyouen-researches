# n11 seventeenth ladder-top k02 WIN-row canonical adoption

Canonical adoption kit for the seventeenth class 20421 k02 WIN row
(`1156299204327378944:131072`, class 20421, s5_index 543795, legal 73,
WIN(1) nodes 4,997,146 @15M). Declared in
`research/log/2026-11-28-n11-seventeenth-ladder-top-k02-adoption-declaration.md`
(commit `d9f75b8b`, single owner, publish-then-execute, HEAD pin
`4bdb6770`).

## New head of record

- `merged-exact-s5-chain-plus-seventeenth-k02-20261128.cache`
  sha256 `dbc1d9508dda61a353ba7b9ef60371bb28eb08cf8f4cd6d30122eafd6a72bc21`,
  **6,901 rows WIN 219 / LOSS 6,682** (pre-registered shape exactly:
  6,900+1 / 218+1 / 6,682+0). Increment
  `increment-seventeenth-k02-adoption-20261128.cache` sha256 `11b8669c...`
  (1 WIN row).
- BASE: `merged-exact-s5-chain-plus-sixteenth-k01-20261128.cache`
  sha256 `dbc1d950...` (6,901 rows WIN 219 / LOSS 6,682), byte-fetched
  from main and pin-verified. Merger `90711961...` x3 byte-identical
  (merge-audit-run1/2/3.json).

## Verification chain (all live inside the fail-closed maker)

- G0 standing pins: merger `90711961`, quarantine `81d23160`,
  policy `78655e94`, BASE `dbc1d950`, gate source `9193f5b6` +
  headers `5976935d`/`2e36d694` (gate binary rebuilt this session
  with zig 0.13.0, tarball pin `d45312e6`).
- Kit MANIFESTs verified for all three source kits (seventeenth
  escalation `bd63d669`, k02 cppgate `4bdb6770`, k02 thirdimpl
  `4bdb6770`).
- G1 live gate re-run: k02 GATE-PASS `73,15000000,1,4997146`
  fresh-cold pair, raw node-exact vs the published kit raw.
- G2 pillar re-parse: replica 15M pair, gate pair, third-impl pair
  (result 1, expansions 5,731,617) all agree with the published rows.
- G3 freshness: k02 absent from BASE, no WIN/LOSS conflict.
- G4 quarantine-free + canonical-safe per s5_evidence_policy.
- G5/G6: increment build, merge x3 byte-identical, shape gates.
- Maker x2 (run1/run2) + clean control: kitout recursive diff clean
  (byte-identical).
- Tamper battery 5/5 fail-closed (see `output/tamper-battery-stdout.log`):
  T1 replica result flip, T2 third-impl expansions drift, T3 gate raw
  quad flip (caught by the G1 live re-run), T4 quarantine-key
  injection with fully valid active registry entry (registry + maker
  QUAR_SHA re-pinned), T5 coherent freshness world (k02 row injected
  into BASE, BASE re-pinned incl. rows/win). Every tamper run aborted
  before any output was written.

## Honest disclosures

- No kit fixes were needed this time; all three source kits passed
  the maker's MANIFEST verification on first attempt (33/33 files
  byte-fetched from main and sha-verified).
- Maker = sixteenth k01 adoption maker (`d555c1d6`) mechanical
  adaptation (kit name, row constants, BASE/OUT shapes, raw file
  names at15m, budget 15000000, TI_EXPECT, class index 20421,
  comment/manifest strings; assertion chain unchanged).
- Class 20421 is NOT complete: k03 `1155173441859489792:131072`,
  k04 `1153062242096250880:540672`,
  k05 `1152921642046849024:68719477248` remain stage-1 2M UNKNOWN;
  no closure-ladder exit is expected from this adoption (serving
  class 20421 stays unknown_now with 3 cost-unknown children).
- The WIN-side flip-census/reaudit of the owner classes
  ([16104, 16132, 16656, 20421] precheck from the frozen graph, with the
  standing shared-owner pre-exclusion caveat) is a SEPARATE declared
  follow-up Part.

## Non-claims / status guard

- NO verdict consumed. The adopted row is cache bookkeeping only.
- The standard 11x11 empty board, the 19 central-reply roots,
  two-stone root {60,27}, third move {100,108}, and every closure
  class remain UNKNOWN. nodes are bookkeeping, never verdicts.

## Files

- `adoption-manifest.json` - machine-readable manifest (schema
  `n11-seventeenth-ladder-top-k02-win-adoption-manifest-v1`).
- `output/increment-seventeenth-k02-adoption-20261128.cache` - the
  1-row WIN increment.
- `output/merged/merged-exact-s5-chain-plus-seventeenth-k02-20261128.cache`
  - the new head of record (289,146 B).
- `output/merged/merge-audit-run{1,2,3}.json` - merger audits
  (byte-identical outputs).
- `output/tamper-battery-stdout.log` - honest tamper record.
- `scripts/make_adoption_seventeenth_k02.py` - the fail-closed maker.
- `MANIFEST-sha256.txt` - sha256 of every kit file.
