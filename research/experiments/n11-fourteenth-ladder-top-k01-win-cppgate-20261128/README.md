# n11 fourteenth ladder-top k01 WIN-row C++ scrutiny gate

Execution kit of the C++ second-implementation scrutiny gate for the
fourteenth ladder-top escalation k01 WIN row
(`6053401124017274880:0`, class 5804, legal 86, s5_index 198576,
WIN(1) nodes 4,360,661 @15M, kit
`n11-fourteenth-ladder-top-escalation-20261128`, commit `5c670bc6`),
under the canonical head of record `d772f73c...` (6,896 rows WIN 214 /
LOSS 6,682; k01 verified fresh/absent by the selection and escalation
Parts).  Declared in
`research/log/2026-11-28-n11-fourteenth-ladder-top-k01-pillars-declaration.md`
(commit `2215d322`, single owner); the k01 target runs happened only
after that declaration was on main (anchors/build were scratch).

## Results

- **k01 GATE-PASS `86,15000000,1,4360661`** (fresh-cold pair
  node-identical, node-exact vs the published escalation raw; wall_s
  8 each, host wall-clock only).  Gate source `9193f5b6...` + headers
  `5976935d...`/`2e36d694...` (byte-fetched from the published
  tenth-cost k01k02 cppgate kit, sha256-verified against the
  standing pins), zig 0.13.0 (tarball pin `d45312e6...`,
  sha256-verified this session), `-std=c++20 -O2` per the standing
  build recipe.
- Anchors (published-raw-pinned, all GATE-PASS, pair node-identical):
  anchor-at2m `98,2000000,0,2000000`, anchor-aj001
  `84,30000000,2,5156075`, anchor-af039 `89,30000000,2,19234232`.
  Anchor raws are byte-identical (sha256) to the published
  thirteenth kit raws except anchor-af039.p1, which differs only in
  wall_s (published 38 vs this host 39; host wall-clock only,
  node-exact) - cross-host determinism node-exact throughout.
- Tamper battery 4/4 fail-closed (T1 wrong expected pin rc=43, T2
  raw nodes edit rc=42, T3 missing input rc=2, T4 gate-rows.json
  expected-pin flip caught by the summary gate G2 rc=1) + clean
  control re-PASS (SUMMARY-PASS, byte-identical summary).
- With the companion third-impl corroboration kit
  (`n11-fourteenth-ladder-top-k01-thirdimpl-20261128`,
  CORROBORATION-PASS, result 1, expansions 5,009,747 x2 identical),
  the two-pillar requirement for the k01 WIN row is COMPLETE.
  Verdict-level WIN(1) agreement across all three implementations.
  Adoption remains a separate declared Part with the standing WIN-side
  flip-census review; class 5804 completion additionally requires
  k02/k03/k04 (still 2M UNKNOWN).

## Honest disclosures

- The runner `scripts/gate_runner.sh` is byte-identical to the
  published u04/thirteenth cppgate runner (sha256 `f2ebcc3e...`,
  comment block still names the u04 kit).  The summary generator
  `scripts/make_summary.py` is the thirteenth kit's generator with
  the schema string adapted to fourteenth (G0 input pins, G1 status
  log, G2 raw-vs-expected + pair determinism; fail-closed, writes
  nothing on failure).
- The k01 input is byte-identical to the published escalation kit
  input (sha256-pinned in input/gate-rows.json); anchor inputs are
  byte-identical to the published thirteenth kit inputs.
- No k01 adoption is performed by this Part.  NO verdict consumed.
