# n11 thirteenth ladder-top k01 WIN-row C++ scrutiny gate

Execution kit of the C++ second-implementation scrutiny gate for the
thirteenth ladder-top escalation k01 WIN row
(`1153204147814662144:65536`, class 16757, legal 72, s5_index 556117,
WIN(1) nodes 2,678,305 @15M, kit
`n11-thirteenth-ladder-top-escalation-20261128`, commit `12d8359c`),
under the canonical head of record `beecb024...` (6,894 rows WIN 212 /
LOSS 6,682; k01 verified fresh/absent by the selection and escalation
Parts).  Declared in
`research/log/2026-11-28-n11-thirteenth-ladder-top-k01-pillars-declaration.md`
(commit `c3cb9f7e`, single owner); the k01 target runs happened only
after that declaration was on main (anchors/build were scratch).

## Results

- **k01 GATE-PASS `72,15000000,1,2678305`** (fresh-cold pair
  node-identical, node-exact vs the published escalation raw; wall_s
  5 each, host wall-clock only).  Gate source `9193f5b6...` + headers
  `5976935d...`/`2e36d694...` (byte-fetched from the published
  tenth-cost k01k02 cppgate kit, sha256-verified against the
  standing pins), zig 0.13.0 (tarball pin `d45312e6...`,
  sha256-verified this session), `-std=c++20 -O2` per the standing
  build recipe.
- Anchors (published-raw-pinned, all GATE-PASS, pair node-identical):
  anchor-at2m `98,2000000,0,2000000`, anchor-aj001
  `84,30000000,2,5156075`, anchor-af039 `89,30000000,2,19234232`.
  All six anchor raws are byte-identical (sha256) to the published
  u03/u04 pillars kit raws: cross-host determinism byte-exact.
- Tamper battery 4/4 fail-closed (T1 wrong expected pin rc=43, T2
  raw nodes edit rc=42, T3 missing input rc=2, T4 gate-rows.json
  expected-pin flip caught by the summary gate G2 rc=1) + clean
  control re-PASS (SUMMARY-PASS, byte-identical summary).
- With the companion third-impl corroboration kit
  (`n11-thirteenth-ladder-top-k01-thirdimpl-20261128`,
  CORROBORATION-PASS, result 1, expansions 3,024,529 x2 identical),
  the two-pillar requirement for the k01 WIN row is COMPLETE.
  Verdict-level WIN(1) agreement across all three implementations.
  Adoption remains a separate declared Part with the standing WIN-side
  flip-census review; class 16757 completion additionally requires
  k02 (still 2M UNKNOWN).

## Honest disclosures

- The runner `scripts/gate_runner.sh` is byte-identical to the
  published u04 cppgate runner (sha256 `f2ebcc3e...`, comment block
  still names the u04 kit).  The summary generator
  `scripts/make_summary.py` is fresh for this kit (G0 input pins,
  G1 status log, G2 raw-vs-expected + pair determinism; fail-closed,
  writes nothing on failure).  One transcription typo in an anchor
  input pin was caught by G0 before any publication and corrected.
- The k01 input is byte-identical to the published escalation kit
  input (sha256-pinned in input/gate-rows.json); anchor inputs are
  byte-identical to the published u03/u04 pillars kit inputs.
- No k01 adoption is performed by this Part.  NO verdict consumed.
  No other key was run at any budget in this Part beyond k01 and the
  three pinned anchors.

## Files

- input/gate-rows.json - machine pin of the target, anchors, gate
  source, escalation basis and head basis (schema
  n11-thirteenth-ladder-top-k01-cppgate-rows-v1).
- input/k01.input.csv, input/anchor-*.input.csv - probe inputs.
- output/raw/*.out - the eight fresh-cold gate raws (k01 p1/p2
  byte-identical).
- output/gate-status.log - runner status lines.
- output/tamper-battery-stdout.log - the 4/4 fail-closed battery.
- output/cppgate-summary.json - machine summary (schema
  n11-thirteenth-ladder-top-k01-cppgate-summary-v1).
- scripts/gate_runner.sh, scripts/make_summary.py.
- MANIFEST-sha256.txt - sha256 of every published file (excluding
  itself).

## Status guard

Pillar bookkeeping only; NO verdict consumed; nodes are bookkeeping,
never evidence.  The standard 11x11 empty board, the two-stone root
{60,27} and its remaining third moves 100/108 stay UNKNOWN.
