# n11 nineteenth ladder-top k04 WIN-row canonical adoption

Canonical adoption kit for the nineteenth class 20421 k04 WIN row
(`1153062242096250880:540672`, class 20421, s5 index 620742, legal 83,
WIN(1) nodes 6,877,739 @15M). Declared in
`research/log/2026-11-28-n11-nineteenth-ladder-top-k04-adoption-declaration.md`
(commit `1043d552`, single owner, publish-then-execute; the same commit
published the k04 thirdimpl summary reschema amendment, values
unchanged).

## New head of record

- `merged-exact-s5-chain-plus-nineteenth-k04-20261128.cache`
  sha256 `8cc87263602898e632ad02cb7016322042d4d0a7d00ee0e860182c3be07a03f4`,
  **6,904 rows WIN 222 / LOSS 6,682** (pre-registered shape exactly:
  6,903+1 / 221+1 / 6,682+0). Increment
  `increment-nineteenth-k04-adoption-20261128.cache` sha256 `7cc20141...`
  (1 WIN row, nodes 6,877,739).
- BASE: `merged-exact-s5-chain-plus-eighteenth-k03-20261128.cache`
  sha256 `3abecf8b...` (6,903 rows WIN 221 / LOSS 6,682), byte-fetched
  from main and pin-verified. Merger `90711961...` x3 byte-identical
  (merge-audit-run1/2/3.json).

## Verification chain (all live inside the fail-closed maker)

- G0 standing pins: merger `90711961`, quarantine `81d23160`,
  policy `78655e94`, BASE `3abecf8b`, gate source `9193f5b6` +
  headers `5976935d`/`2e36d694` (gate binary as anchor-verified this
  session, zig 0.13.0, tarball pin `d45312e6`).
- Kit MANIFESTs verified for all three source kits (nineteenth
  escalation `73cf1b2f`, k04 cppgate `b1f527eb`, k04 thirdimpl
  `b1f527eb` with the summary reschema amendment `1043d552`).
- G1 live gate re-run: k04 GATE-PASS `83,15000000,1,6877739`
  fresh-cold pair, raw node-exact vs the published kit raw.
- G2 pillar re-parse: replica 15M pair, gate pair, third-impl pair
  (result 1, expansions 7,920,095) all agree with the published rows.
- G3 freshness: k04 absent from BASE, no WIN/LOSS conflict.
- G4 quarantine-free + canonical-safe per s5_evidence_policy.
- G5/G6: increment build, merge x3 byte-identical, shape gates.
- Maker x2 (run1/run2) + clean control: kitout recursive diff clean
  (byte-identical).
- Tamper battery 5/5 fail-closed (see
  `output/tamper-battery-stdout.log`): T1 replica result flip
  (G2 replica pair mismatch), T2 third-impl expansions drift (G2
  third-impl pair mismatch), T3 gate raw quad flip (caught by the
  G1 live re-run), T4 quarantine-key injection with a fully valid
  active registry entry (registry + maker QUAR_SHA re-pinned; G4),
  T5 coherent freshness world (k04 row injected into BASE, BASE
  re-pinned incl. rows/win; G3). A disclosed pre-round without
  MANIFEST re-pins caught T1-T3 fail-closed at the kit MANIFEST
  gate; the repinned probes then reached their intended deeper
  gates. Every tamper run aborted before any output was written
  (kitout absent); all inputs restored byte-identical,
  sha-verified.

## Honest disclosures

- The k04 thirdimpl kit's `output/pillars-summary.json` was
  reschemad to the standing flat thirdimpl-summary v1 format
  (top-level result/expansions fields required by the maker's G2
  cross-check; the same amendment the eighteenth k03 Part needed).
  ALL VALUES unchanged; published as an amendment with the adoption
  declaration (commit `1043d552`) and disclosed there.
- Maker = eighteenth k03 adoption maker (script raw-fetch sha256
  `6ca29670...`, byte-verified this session) mechanical adaptation
  (kit name, row constants, BASE/OUT shapes, raw file names at15m,
  budget 15000000, TI_EXPECT, class index 20421, comment/manifest
  strings; assertion chain unchanged; every replacement
  count-asserted, residues grepped - the remaining
  eighteenth/seventeenth mentions are intentional lineage
  references). One functional path adaptation: the nineteenth
  escalation kit publishes its raws at the kit root (no `raws/`
  subdirectory), so the replica-raw paths drop the `raws/` segment.
- Class 20421 is NOT complete: k05
  `1152921642046849024:68719477248` remains stage-1 2M UNKNOWN;
  no closure-ladder exit is expected from this adoption (the
  serving class 20421 is already excluded_now; it stays in the
  ladder with 1 cost-unknown child).
- The WIN-side flip-census/reaudit of the owner classes
  ([18534, 18554, 19885, 20421] precheck from the frozen graph,
  with the standing shared-owner pre-exclusion caveat) is a
  SEPARATE declared follow-up Part.
- This lane runs without access to the user's computer (scheduled
  task); publication is via the GitHub API only.

## Non-claims / status guard

- NO verdict consumed. The adopted row is cache bookkeeping only.
- The standard 11x11 empty board, the 19 central-reply roots,
  two-stone root {60,27}, third move {100,108}, and every closure
  class remain UNKNOWN. nodes are bookkeeping, never verdicts.

## Files

- `adoption-manifest.json` - machine-readable manifest (schema
  `n11-nineteenth-ladder-top-k04-win-adoption-manifest-v1`).
- `output/increment-nineteenth-k04-adoption-20261128.cache` - the
  1-row WIN increment.
- `output/merged/merged-exact-s5-chain-plus-nineteenth-k04-20261128.cache`
  - the new head of record (289,244 B).
- `output/merged/merge-audit-run{1,2,3}.json` - merger audits
  (byte-identical outputs).
- `output/tamper-battery-stdout.log` - honest tamper record.
- `scripts/make_adoption_nineteenth_k04.py` - the fail-closed maker
  (sha256 `64a1ebdf...`).
- `MANIFEST-sha256.txt` - sha256 of every kit file.
