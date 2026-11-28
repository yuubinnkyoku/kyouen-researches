# 2026-11-28 n11 class-20421 k05 WIN-row canonical adoption declaration

Single-owner declaration (publish-then-execute) for the canonical
adoption of the class-20421 k05 WIN row
(`1152921642046849024:68719477248`, class 20421, s5 index 625899,
legal 78, WIN(1) nodes 2,007,513 @15M) into the canonical head of
record. This lane is the declared owner of this Part; the adoption
runs only after this declaration is on main.

## Basis (all published and byte-verified)

- Three-implementation agreement (two-pillar COMPLETE, kits
  published in commit `c34e82ee`, completion `a19c79c3`):
  - replica: `n11-class20421-k05-escalation-20261128`
    (declaration `ddff08ce`, kit `9a87750e`) - k05 15M cold pair
    node-identical WIN(1) nodes 2,007,513.
  - C++ gate: `n11-class20421-k05-win-cppgate-20261128`
    (`772c04bc`/`c34e82ee`) - GATE-PASS `78,15000000,1,2007513`,
    anchors 3/3 node-exact vs the published nineteenth k04
    cppgate kit raws (wall_s-only, cross-host), tamper 4/4
    fail-closed + clean control.
  - third impl: `n11-class20421-k05-thirdimpl-20261128`
    (`772c04bc`/`c34e82ee`) - CORROBORATION-PASS result 1,
    expansions 2,292,427 x2 identical (published directly in the
    standing flat thirdimpl-summary v1 format; no reschema
    amendment is needed for this Part).
- BASE head of record: `merged-exact-s5-chain-plus-nineteenth-k04-
  20261128.cache` sha256 `8cc87263602898e632ad02cb7016322042d4d0a7d
  00ee0e860182c3be07a03f4`, 6,904 rows WIN 222 / LOSS 6,682.
  Freshness: k05 absent from BASE by direct cache scan on this
  host before this declaration.

## Pre-registered plan and expected shape

- Expected merged shape: **6,905 rows WIN 223 / LOSS 6,682**
  (6,904+1 / 222+1 / 6,682+0), new head
  `merged-exact-s5-chain-plus-class20421-k05-20261128.cache`,
  increment `increment-class20421-k05-adoption-20261128.cache`
  (1 WIN row, nodes 2,007,513).
- Fail-closed maker (adaptation of the published nineteenth k04
  adoption maker
  `research/experiments/n11-nineteenth-ladder-top-k04-adoption-
  20261128/scripts/make_adoption_nineteenth_k04.py`, published in
  commit `a03e21ef`, byte-verified raw fetch this session): G0
  standing pins (merger `90711961`, policy `78655e94`, quarantine
  `81d23160`, BASE `8cc87263`, gate source `9193f5b6` + headers
  `5976935d`/`2e36d694`), kit MANIFEST verification for all
  three source kits, G1 live gate re-run of the published
  gate_runner.sh on a scratch copy (expected
  `k05 GATE-PASS 78,15000000,1,2007513`, raw node-exact vs the
  published kit raw), G2 pillar re-parse (replica 15M pair, gate
  pair, third-impl pair result 1 / expansions 2,292,427), G3
  freshness (k05 absent from BASE, no WIN/LOSS conflict), G4
  quarantine-free + canonical-safe per s5_evidence_policy, G5
  increment build, G6 merge x3 byte-identical + shape gates.
  Maker x2 (run1/run2 kitout recursive diff byte-identical) +
  clean control.
- Disclosed maker adaptations (every replacement count-asserted,
  residues grepped, assertion chain unchanged): kit name, row
  constants (k05 key, nodes 2,007,513, legal 78, class index
  20421, s5 index 625899), BASE/OUT shapes (6,904/222/6682 ->
  6,905/223/6682), EXPECT_QUAD `78,15000000,1,2007513`,
  TI_EXP expansions 2,292,427 (replica-raw paths already at the
  kit root in both the nineteenth and this escalation kit),
  manifest/README strings.
- Tamper battery 5/5 fail-closed, each aborting before any output
  is written: T1 replica result flip, T2 third-impl expansions
  drift, T3 gate raw quad flip (caught by the G1 live re-run),
  T4 quarantine-key injection with a fully valid active registry
  entry (registry + maker QUAR_SHA re-pinned), T5 coherent
  freshness world (k05 row injected into BASE, BASE re-pinned
  incl. rows/win).
- Owner-union precheck for the WIN-side flip-census follow-up
  (SEPARATE declared Part): [18683, 18710, 20421] re-derived
  from the frozen graph in the class20421-k05 escalation Part;
  caveat: shared-owner pre-exclusion (other owner classes may
  already be excluded_now on BASE; the serving class 20421 is
  already excluded_now on BASE). This adoption is expected to
  close the last cost-unknown of the serving class 20421
  (unknown_now 1 -> 0), so the follow-up reaudit measures the
  class-20421 closure-ladder EXIT.

## Claim status

Adoption bookkeeping only: NO verdict is consumed. Even after
adoption, the k05 row is cache bookkeeping. Class 20421 is NOT
complete until the separately declared WIN-side flip-census
reaudit measures the ladder EXIT and its flips exactly. The
standard 11x11 empty board, all 19 central-reply roots, the
two-stone root {60,27} and third moves 100/108 remain UNKNOWN.
Nodes/expansions are bookkeeping, never verdicts. This lane runs
without access to the user's computer (scheduled task);
publication is via the GitHub API only.
