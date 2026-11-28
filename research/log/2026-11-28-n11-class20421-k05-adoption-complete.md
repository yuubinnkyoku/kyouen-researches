# 2026-11-28 n11 class-20421 k05 WIN-row canonical adoption complete

Completion log for the canonical adoption of the class-20421 k05
WIN row (`1152921642046849024:68719477248`, class 20421, s5 index
625899, legal 78, WIN(1) nodes 2,007,513 @15M), declared in
`research/log/2026-11-28-n11-class20421-k05-adoption-declaration.md`
(commit `cf6a21a6`, publish-then-execute, single owner), executed
after publication on main.

## New head of record

- `merged-exact-s5-chain-plus-class20421-k05-20261128.cache`
  sha256 `e1a9cacc54abad5198e455ff53492310fabc28f5f89cf26363a7f3da7fe944de`,
  **6,905 rows WIN 223 / LOSS 6,682** (pre-registered shape
  exactly: 6,904+1 / 222+1 / 6,682+0; BASE `8cc87263...`
  6,904/222/6,682 + 1 fresh WIN row). Increment
  `increment-class20421-k05-adoption-20261128.cache` sha256
  `6b525957...`.

## Verification

- Fail-closed maker (adaptation of the published nineteenth k04
  adoption maker, commit `a03e21ef`; every replacement
  count-asserted): G0 standing pins all byte-verified; kit
  MANIFESTs verified for all three source kits; G1 live gate
  re-run GATE-PASS `78,15000000,1,2007513` raw node-exact; G2
  pillar re-parse 3-impl agreement (replica pair, gate pair,
  third-impl pair result 1 expansions 2,292,427); G3 freshness
  (k05 absent from BASE, no conflict); G4 quarantine-free +
  canonical-safe; G5/G6 increment + merge x3 byte-identical +
  shape gates. Maker x2 kitout recursive diff byte-identical +
  clean control MAKER-PASS.
- Tamper battery 5/5 fail-closed at the intended gates (T1 G2
  replica pair, T2 G2 third-impl pair, T3 G1 live re-run, T4 G4
  quarantined key with fully valid active registry entry and
  QUAR_SHA re-pin, T5 G3 coherent freshness world with BASE
  re-pin incl. rows/win), each aborting before any output was
  written; disclosed pre-round (no MANIFEST re-pins) caught T1-T3
  at the kit MANIFEST gate; all inputs restored byte-identical.
- Kit `research/experiments/n11-class20421-k05-adoption-20261128/`
  (commit `fdf1ed8b`, fix `ac6bd717`), fetch-back 10/10
  byte-identical commit-pinned raw CDN.

## Honest disclosure

- The first push of the merged head cache (`fdf1ed8b`) was
  silently truncated to 63,967 bytes by the ~64KB single-read
  limit of the publication tooling. The fetch-back check caught
  it (9/10 + 1 truncated), and commit `ac6bd717` republished the
  full 289,298-byte cache, fetch-back byte-identical to the
  maker x2 output (sha256 `e1a9cacc...`). The canonical head of
  record is the full-size file; no other kit file was affected
  (all others <60KB and fetch-back-verified in the same round).

## Status guard

NO verdict consumed. The k05 row is cache bookkeeping. This
adoption closes the last cost-unknown child of the serving class
20421; class 20421 is NOT complete until the separately declared
WIN-side flip-census/reaudit measures the closure-ladder EXIT
exactly (owner union [18683, 18710, 20421]; expected flips and
the unknown_now 1 -> 0 EXIT to be measured, not assumed; naive
2-flip expectations carry the standing caveat). The standard
11x11 empty board, all 19 central-reply roots, the two-stone
root {60,27} and third moves 100/108 remain UNKNOWN.
Nodes/expansions are bookkeeping, never verdicts. This lane runs
without access to the user's computer (scheduled task);
publication is via the GitHub API only.
