# Completion log: n11 nineteenth ladder-top k04 WIN pillars (cppgate + thirdimpl)

Completion of the Part declared in
`research/log/2026-11-28-n11-nineteenth-ladder-top-k04-pillars-declaration.md`
(declaration commit `855d50fc`, single owner, publish-then-execute).
Kits published in commit `b1f527eb` (26 files, two kits):

- `research/experiments/n11-nineteenth-ladder-top-k04-win-cppgate-20261128/`
- `research/experiments/n11-nineteenth-ladder-top-k04-thirdimpl-20261128/`

## C++ scrutiny gate (second implementation)

- Pinned source `kyouen_dfpn_root.cpp` `9193f5b6...` + headers
  `5976935d`/`2e36d694` (byte-verified raw CDN fetches from the
  published tenthcost k01k02 cppgate kit), zig 0.13.0 tarball pin
  `d45312e6...` verified, `-std=c++20 -O2`.
- **k04 GATE-PASS `83,15000000,1,6877739`**: fresh-cold pair
  node-exact against the published nineteenth escalation raws
  (WIN(1) at 15M), 2-pass determinism.
- Anchors 3/3 GATE-PASS: at2m `98,2000000,0,2000000`, aj001
  `84,30000000,2,5156075`, af039 `89,30000000,2,19234232`; the
  six anchor raws are node-exact against the published eighteenth
  k03 cppgate kit raws (wall_s-only difference, cross-host
  determinism).
- External tamper battery 4/4 fail-closed (T1 target-input G0,
  T2 anchor-input G0, T3 expected-row G2, T4 raw verdict flip G2;
  all inputs restored byte-identical, sha-verified) + clean
  control SUMMARY-PASS. make_summary fail-closed, schema
  `n11-nineteenth-ladder-top-k04-cppgate-summary-v1`.

## Third-implementation corroboration

- `third_impl.js` pin `08ea958f...` (byte-verified local copy),
  `--row=k04 --stones=5 --legal=83 --lo=1153062242096250880
  --hi=540672 --cap=400000000 --wallcap=260 --memo-power=22`:
  **result 1, expansions 7,920,095, nodes 4,544,365, quads 95,670,
  ttOverwrites 3,726,116, identical on both cold passes**
  (wall_s 26.04 / 26.13). **CORROBORATION-PASS**, schema
  `n11-nineteenth-ladder-top-k04-thirdimpl-summary-v1`.

## Two-pillar COMPLETE

Verdict-level WIN(1) agreement across all three implementations
(jsreplay replica escalation `73cf1b2f`, C++ gate, third
implementation) for the k04 row
`1153062242096250880:540672` (class 20421, s5 index 620742, legal
83, WIN(1) nodes 6,877,739 @15M). nodes/expansions are bookkeeping
and are not required to match across implementations.

## Status guard

Pillar bookkeeping only: **NO verdict consumed**. The k04 WIN(1)
row is NOT adopted by this Part; adoption requires a separate
single-owner declared Part (expected merged shape 6,903 -> 6,904
rows WIN 221 -> 222, increment, merger `90711961` x3, maker +
tamper), followed by the WIN-side flip-census/reaudit (owner
union [18534, 18554, 19885, 20421]; the serving class 20421 is
already excluded_now). Class 20421 is NOT complete (k05 remains
stage-1 2M UNKNOWN). The standard 11x11 empty board, all 19
central-reply roots, the two-stone root {60,27} and third moves
100/108 remain **UNKNOWN**. 11x11 is **UNKNOWN**.
