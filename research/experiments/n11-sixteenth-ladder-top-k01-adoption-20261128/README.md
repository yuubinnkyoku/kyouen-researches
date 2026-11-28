# n11 sixteenth ladder-top k01 WIN-row canonical adoption

Canonical adoption kit for the sixteenth class 20421 k01 WIN row
(`1155454779397246976:131072`, class 20421, s5_index 528689, legal 76,
WIN(1) nodes 5,273,778 @15M). Declared in
`research/log/2026-11-28-n11-sixteenth-ladder-top-k01-adoption-declaration.md`
(commit `e1618d8b`, single owner, publish-then-execute, HEAD pin
`fd960128`).

## New head of record

- `merged-exact-s5-chain-plus-sixteenth-k01-20261128.cache`
  sha256 `dbc1d9508dda61a353ba7b9ef60371bb28eb08cf8f4cd6d30122eafd6a72bc21`,
  **6,901 rows WIN 219 / LOSS 6,682** (pre-registered shape exactly:
  6,900+1 / 218+1 / 6,682+0). Increment
  `increment-sixteenth-k01-adoption-20261128.cache` sha256 `bb029422...`
  (1 WIN row).
- BASE: `merged-exact-s5-chain-plus-fifteenth-k02-20261128.cache`
  sha256 `58110025...` (6,900 rows WIN 218 / LOSS 6,682), byte-fetched
  from main and pin-verified. Merger `90711961...` x3 byte-identical
  (merge-audit-run1/2/3.json).

## Verification chain (all live inside the fail-closed maker)

- G0 standing pins: merger `90711961`, quarantine `81d23160`,
  policy `78655e94`, BASE `58110025`, gate source `9193f5b6` +
  headers `5976935d`/`2e36d694` (gate binary rebuilt this session
  with zig 0.13.0, tarball pin `d45312e6`).
- Kit MANIFESTs verified for all three source kits (sixteenth
  escalation `85edd462`, k01 cppgate `fd960128`, k01 thirdimpl
  `4eb639e6`).
- G1 live gate re-run: k01 GATE-PASS `76,15000000,1,5273778`
  fresh-cold pair, raw node-exact vs the published kit raw.
- G2 pillar re-parse: replica 15M pair, gate pair, third-impl pair
  (result 1, expansions 6,003,522) all agree with the published rows.
- G3 freshness: k01 absent from BASE, no WIN/LOSS conflict.
- G4 quarantine-free + canonical-safe per s5_evidence_policy.
- G5/G6: increment build, merge x3 byte-identical, shape gates.
- Maker x2 (run1/run2) + clean control: kitout recursive diff clean
  (byte-identical).
- Tamper battery 5/5 fail-closed (see `output/tamper-battery-stdout.log`):
  T1 replica result flip, T2 third-impl expansions drift, T3 gate raw
  quad flip (caught by the G1 live re-run), T4 quarantine-key
  injection with fully valid active registry entry (registry + maker
  QUAR_SHA re-pinned), T5 coherent freshness world (k01 row injected
  into BASE, BASE re-pinned incl. rows/win). Every tamper run aborted
  before any output was written.

## Honest disclosures

- The kit-fix commit `4eb639e6` replaced this lane's thirdimpl
  `output/pillars-summary.json` (first published in `fd960128` with a
  deviating schema: nested p1/p2, string result) with the lineage
  summary schema; the adoption maker G2 cross-check rejected the
  first summary fail-closed, no measured value changed (same two
  cold passes, same MANIFEST-pinned raws). The commit message of
  `4eb639e6` contains a truncated sha ("fd96028" for `fd960128`);
  the full sha is in the summary disclosure field.
- Maker = fifteenth k02 adoption maker (`26ff68dc`) mechanical
  adaptation (kit name, row constants, BASE/OUT shapes, raw file
  names at15m, budget 15000000, TI_EXPECT, class index 20421,
  comment/manifest strings; assertion chain unchanged).
- Class 20421 is NOT complete: k02 `1156299204327378944:131072`,
  k03 `1155173441859489792:131072`, k04 `1153062242096250880:540672`,
  k05 `1152921642046849024:68719477248` remain stage-1 2M UNKNOWN;
  no closure-ladder exit is expected from this adoption (serving
  class 20421 stays unknown_now with 4 cost-unknown children).
- The WIN-side flip-census/reaudit of the owner classes
  ([15647, 16901, 20421] precheck from the frozen graph, with the
  standing shared-owner pre-exclusion caveat) is a SEPARATE declared
  follow-up Part.

## Non-claims / status guard

- NO verdict consumed. The adopted row is cache bookkeeping only.
- The standard 11x11 empty board, the 19 central-reply roots,
  two-stone root {60,27}, third move {100,108}, and every closure
  class remain UNKNOWN. nodes are bookkeeping, never verdicts.

## Files

- `adoption-manifest.json` - machine-readable manifest (schema
  `n11-sixteenth-ladder-top-k01-win-adoption-manifest-v1`).
- `output/increment-sixteenth-k01-adoption-20261128.cache` - the
  1-row WIN increment.
- `output/merged/merged-exact-s5-chain-plus-sixteenth-k01-20261128.cache`
  - the new head of record (289,097 B).
- `output/merged/merge-audit-run{1,2,3}.json` - merger audits
  (byte-identical outputs).
- `output/tamper-battery-stdout.log` - honest tamper record.
- `scripts/make_adoption_sixteenth_k01.py` - the fail-closed maker.
- `MANIFEST-sha256.txt` - sha256 of every kit file.
