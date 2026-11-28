# 2026-11-28 n11 nineteenth ladder-top k04 WIN-row canonical adoption declaration

Single-owner declaration (publish-then-execute) for the canonical
adoption of the nineteenth class 20421 k04 WIN row
(`1153062242096250880:540672`, class 20421, s5 index 620742, legal
83, WIN(1) nodes 6,877,739 @15M) into the canonical head of record.
This lane is the declared owner of this Part; the adoption runs
only after this declaration is on main.

## Basis (all published and byte-verified)

- Three-implementation agreement (two-pillar COMPLETE, kits
  published in commit `b1f527eb`, completion `170cccd6`):
  - replica: `n11-nineteenth-ladder-top-escalation-20261128`
    (declaration `b27b8f24`, kit `73cf1b2f`) - k04 15M cold pair
    node-identical WIN(1) nodes 6,877,739.
  - C++ gate: `n11-nineteenth-ladder-top-k04-win-cppgate-20261128`
    (`855d50fc`/`b1f527eb`) - GATE-PASS `83,15000000,1,6877739`,
    anchors 3/3 node-exact (wall_s-only, cross-host), tamper 4/4
    fail-closed + clean control.
  - third impl: `n11-nineteenth-ladder-top-k04-thirdimpl-20261128`
    (`855d50fc`/`b1f527eb`) - CORROBORATION-PASS result 1,
    expansions 7,920,095 x2 identical.
- BASE head of record: `merged-exact-s5-chain-plus-eighteenth-k03-
  20261128.cache` sha256 `3abecf8b1da6735a0cf0719087b0f026e3a82648
  dce026b9c82aab106e23a023`, 6,903 rows WIN 221 / LOSS 6,682.
  Freshness: k04 absent from BASE by direct cache scan on this
  host before this declaration.

## Pre-registered plan and expected shape

- Expected merged shape: **6,904 rows WIN 222 / LOSS 6,682**
  (6,903+1 / 221+1 / 6,682+0), new head
  `merged-exact-s5-chain-plus-nineteenth-k04-20261128.cache`,
  increment `increment-nineteenth-k04-adoption-20261128.cache`
  (1 WIN row, nodes 6,877,739).
- Fail-closed maker (adaptation of the published eighteenth k03
  adoption maker
  `research/experiments/n11-eighteenth-ladder-top-k03-adoption-
  20261128/scripts/make_adoption_eighteenth_k03.py`, raw-fetch
  sha256 `6ca2967068130024b20c80355c914fd3774efcbc6ccad753a00bec
  45d71e3958`, byte-verified this session): G0 standing pins
  (merger `90711961`, policy `78655e94`, quarantine `81d23160`,
  BASE `3abecf8b`, gate source `9193f5b6` + headers `5976935d`/
  `2e36d694`), kit MANIFEST verification for all three source
  kits, G1 live gate re-run of the published gate_runner.sh on a
  scratch copy (expected `k04 GATE-PASS 83,15000000,1,6877739`,
  raw node-exact vs the published kit raw), G2 pillar re-parse
  (replica 15M pair, gate pair, third-impl pair result 1 /
  expansions 7,920,095), G3 freshness (k04 absent from BASE, no
  WIN/LOSS conflict), G4 quarantine-free + canonical-safe per
  s5_evidence_policy, G5 increment build, G6 merge x3
  byte-identical + shape gates. Maker x2 (run1/run2 kitout
  recursive diff byte-identical) + clean control.
- Disclosed maker adaptations (every replacement count-asserted,
  residues grepped, assertion chain unchanged): kit name, row
  constants (k04 key, nodes 6,877,739, legal 83, class index
  20421, s5 index 620742), BASE/OUT shapes (6,903/221/6682 ->
  6,904/222/6682), EXPECT_QUAD `83,15000000,1,6877739`,
  TI_EXP expansions 7,920,095, replica-raw path (the nineteenth
  escalation kit publishes its raws at the kit root, not in a
  `raws/` subdirectory), manifest/README strings.
- Tamper battery 5/5 fail-closed, each aborting before any output
  is written: T1 replica result flip, T2 third-impl expansions
  drift, T3 gate raw quad flip (caught by the G1 live re-run),
  T4 quarantine-key injection with a fully valid active registry
  entry (registry + maker QUAR_SHA re-pinned), T5 coherent
  freshness world (k04 row injected into BASE, BASE re-pinned
  incl. rows/win).
- Owner-union precheck for the WIN-side flip-census follow-up
  (SEPARATE declared Part): [18534, 18554, 19885, 20421] from the
  frozen graph in the nineteenth escalation Part; caveat:
  shared-owner pre-exclusion (other owner classes may already be
  excluded_now on BASE; the serving class 20421 is already
  excluded_now on BASE after the eighteenth k03 adoption reaudit).

## Amendment published in this same commit

- The k04 thirdimpl kit's `output/pillars-summary.json` is
  reschemad to the standing flat thirdimpl-summary v1 format
  (top-level result/expansions fields required by the maker's G2
  cross-check; the same amendment the eighteenth k03 Part needed,
  commit `7fe49b5e`). ALL VALUES unchanged; schema name unchanged
  (`n11-nineteenth-ladder-top-k04-thirdimpl-summary-v1`); the
  kit MANIFEST is republished accordingly. The published ti raws
  and the original published values are untouched.

## Claim status

Adoption bookkeeping only: NO verdict is consumed. Even after
adoption, the k04 row is cache bookkeeping. Class 20421 is NOT
complete (k05 `1152921642046849024:68719477248` remains stage-1
2M UNKNOWN; no closure-ladder exit is expected from this
adoption - the serving class 20421 stays in the ladder with 1
cost-unknown child). The standard 11x11 empty board, all 19
central-reply roots, the two-stone root {60,27} and third moves
100/108 remain UNKNOWN. Nodes/expansions are bookkeeping, never
verdicts. This lane runs without access to the user's computer
(scheduled task); publication is via the GitHub API only.
