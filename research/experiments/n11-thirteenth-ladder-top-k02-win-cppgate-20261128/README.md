# n11 thirteenth ladder-top k02 WIN-row C++ scrutiny gate

Execution kit of the C++ second-implementation scrutiny gate for the
thirteenth ladder-top k02 escalation WIN row
(`1152922672837951488:65792`, class 16757, legal 72, s5_index 558553,
WIN(1) nodes 3,485,963 @15M, kit
`n11-thirteenth-ladder-top-k02-escalation-20261128`, commit
`3087c38b`), under the canonical head of record `beecb024...` (6,894
rows WIN 212 / LOSS 6,682; k02 verified fresh/absent by the selection
and escalation Parts).  Declared in
`research/log/2026-11-28-n11-thirteenth-ladder-top-k02-pillars-declaration.md`
(commit `177b1086`, single owner); the k02 target runs happened only
after that declaration was on main (anchors/build were scratch).

## Results

- **k02 GATE-PASS `72,15000000,1,3485963`** (fresh-cold pair
  node-identical, node-exact vs the published k02 escalation raw).
  Gate source `9193f5b6...` + headers `5976935d...`/`2e36d694...`
  (byte-fetched from the published tenth-cost k01k02 cppgate kit,
  sha256-verified against the standing pins), zig 0.13.0 (tarball
  pin `d45312e6...`), `-std=c++20 -O2`.
- Anchors (published-raw-pinned, all GATE-PASS, pair node-identical):
  anchor-at2m `98,2000000,0,2000000`, anchor-aj001
  `84,30000000,2,5156075`, anchor-af039 `89,30000000,2,19234232`;
  all six anchor raws byte-identical (sha256) to the published
  u03/u04 pillars kit raws (cross-host determinism byte-exact).
- Tamper battery 4/4 fail-closed (T1 wrong expected pin rc=43, T2
  raw nodes edit rc=42, T3 missing input rc=2, T4 gate-rows.json
  expected-pin flip caught by the summary gate G2 rc=1) + clean
  control re-PASS (SUMMARY-PASS).
- With the companion third-impl corroboration kit
  (`n11-thirteenth-ladder-top-k02-thirdimpl-20261128`,
  CORROBORATION-PASS, result 1, expansions 3,910,009 x2 identical),
  the two-pillar requirement for the k02 WIN row is COMPLETE.
  Both class 16757 keys (k01 `f1f5c49d`, k02 here) are now
  pillar-complete WIN rows: verdict-level WIN(1) agreement across
  all three implementations for the entire class.

## Honest disclosures

- The runner `scripts/gate_runner.sh` is byte-identical to the
  published u04 cppgate runner (sha256 `f2ebcc3e...`).  The summary
  generator `scripts/make_summary.py` is the k01 kit's generator
  with only the schema name updated (k01 kit commit `f1f5c49d`).
- The k02 input is byte-identical to the published k02 escalation
  kit input (sha256-pinned in input/gate-rows.json); anchor inputs
  are byte-identical to the published u03/u04 pillars kit inputs.
- No k02 adoption and no class 16757 adoption is performed by this
  Part.  NO verdict consumed.  No other key was run at any budget in
  this Part beyond k02 and the three pinned anchors.

## Files

- input/gate-rows.json (schema
  n11-thirteenth-ladder-top-k02-cppgate-rows-v1),
  input/k02.input.csv, input/anchor-*.input.csv,
  output/raw/*.out (k02 p1/p2 byte-identical), output/gate-status.log,
  output/tamper-battery-stdout.log, output/cppgate-summary.json
  (schema n11-thirteenth-ladder-top-k02-cppgate-summary-v1),
  scripts/gate_runner.sh, scripts/make_summary.py,
  MANIFEST-sha256.txt (sha256 of every published file, excluding
  itself).

## Status guard

Pillar bookkeeping only; NO verdict consumed; nodes are bookkeeping,
never evidence.  The standard 11x11 empty board, the two-stone root
{60,27} and its remaining third moves 100/108 stay UNKNOWN.
