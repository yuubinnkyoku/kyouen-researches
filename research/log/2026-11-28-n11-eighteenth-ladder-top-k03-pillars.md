# Completion log: n11 eighteenth ladder-top k03 WIN pillars

Completion of the Part declared in
`research/log/2026-11-28-n11-eighteenth-ladder-top-k03-pillars-declaration.md`
(declaration commit `26143236`, single owner, publish-then-execute).
Kits (commit `3549edde`):
`research/experiments/n11-eighteenth-ladder-top-k03-win-cppgate-20261128/`
and `research/experiments/n11-eighteenth-ladder-top-k03-thirdimpl-20261128/`
(fetch-back byte-identical against each kit MANIFEST-sha256 via
commit-pinned raw CDN + sha256).

## Result: two-pillar requirement COMPLETE for the k03 WIN row

- **Pillar 1 (C++ scrutiny gate): GATE-PASS
  `73,15000000,1,5266012`** - fresh-cold C++ pair node-exact
  against the published eighteenth escalation raw (k03 WIN(1) at
  15M, jsreplay replica), 2-pass determinism. Anchors 3/3 (at2m
  `98,2000000,0,2000000`, aj001 `84,30000000,2,5156075`, af039
  `89,30000000,2,19234232`, input pins byte-identical to the
  published seventeenth k02 gate kit). Gate binary: pinned source
  `9193f5b6`/`5976935d`/`2e36d694`, zig 0.13.0 (tarball pin
  `d45312e6`), anchor-verified before the target row.
  Tamper battery 4/4 fail-closed (T1 wrong expected pin rc=43,
  T2 raw node edit rc=42, T3 missing input rc=2, T4 gate-rows
  expected flip caught by summary gate G2 rc=1) + clean control
  re-PASS byte-identical.
- **Pillar 2 (third implementation): CORROBORATION-PASS** -
  `third_impl.js` (`08ea958f...`, pinned standing third
  implementation) with `--row=k03 --stones=5 --legal=73
  --lo=1155173441859489792 --hi=131072 --cap=400000000
  --wallcap=260 --memo-power=22`: result 1, expansions 6,039,011,
  nodes 3,524,008, quads 95,670, ttOverwrites 1,865,863,
  identical on both cold passes (wall_s 18.29/17.77).
- **Verdict-level WIN(1) agreement across all three
  implementations** (jsreplay replica, C++ gate, third
  implementation) for k03 `1155173441859489792:131072`
  (class 20421, s5_index 605961, legal 73).

## Status guard / next

Pillar bookkeeping only: NO verdict is consumed. The k03 WIN(1)
row is NOT adopted by this Part; adoption requires a separate
single-owner declaration (canonical increment + merger + tamper
battery + WIN-side flip-census/reaudit with the shared-owner
pre-exclusion caveat; owner union k03 [18136, 18143, 20128,
20421]). Class 20421 is NOT complete (k04-k05 remain stage-1 2M
UNKNOWN). The standard 11x11 empty board, the 19 central-reply
roots, the two-stone root {60,27} and its remaining third moves
100/108 stay UNKNOWN. Nodes, expansions and wall_s are
bookkeeping, never verdicts.
