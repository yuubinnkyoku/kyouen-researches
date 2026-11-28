# n11 fifteenth ladder-top k02 WIN-row C++ scrutiny gate

Execution kit of the C++ second-implementation scrutiny gate for the
fifteenth class 5804 k02 WIN row (`6052837899185946628:128`,
class 5804, legal 87, s5_index 212115, WIN(1) nodes 18,247,029 @50M,
L50M escalation kit `n11-fifteenth-ladder-top-k02-l50m-escalation-20261128`,
declaration `5cc8e1fb`, kit+log `48ea76d8`), under the canonical head
of record `3a527d39...` (6,899 rows WIN 217 / LOSS 6,682; k02 verified
absent from the head by the L50M escalation Part). Declared in
`research/log/2026-11-28-n11-fifteenth-ladder-top-k02-pillars-declaration.md`
(commit `66bb19d1`, single owner); the k02 target runs happened only
after that declaration was on main (gate binary and anchors were
scratch-verified on this host in the published k01/k03 pillar kits).

## Results

- **k02 GATE-PASS `87,50000000,1,18247029`** (fresh-cold pair,
  2-pass determinism; node-exact vs the published L50M raw pair
  (jsreplay) nodes 18,247,029, result WIN(1); wall_s host
  wall-clock only). Gate source `9193f5b6...` + headers
  `5976935d...`/`2e36d694...` (the standing pins, sha-verified),
  zig 0.13.0 (tarball pin `d45312e6...`), `-std=c++20 -O2` per the
  standing build recipe; the gate binary was rebuilt and
  scratch-verified in the published k03 pillar session on this
  host and re-verified here.
- Anchors (published-raw-pinned, all GATE-PASS, pair
  node-identical): anchor-at2m `98,2000000,0,2000000`,
  anchor-aj001 `84,30000000,2,5156075`, anchor-af039
  `89,30000000,2,19234232`, with the published anchor input pins
  (`ecc0299b...`/`2f6daea5...`/`e51a3c9d...`).
- Tamper battery 4/4 fail-closed (T1 wrong expected pin rc=43, T2
  raw nodes edit rc=42, T3 missing input rc=2, T4 gate-rows.json
  expected-pin flip caught by the summary gate G2 rc=1) + clean
  control re-PASS (SUMMARY-PASS, byte-identical summary; input
  restored byte-identical, sha-verified).
- With the companion third-implementation corroboration kit
  (`n11-fifteenth-ladder-top-k02-thirdimpl-20261128`,
  CORROBORATION-PASS, result 1, expansions 21,587,934 x2
  identical), the two-pillar requirement for the k02 WIN row is
  COMPLETE. Verdict-level WIN(1) agreement across all three
  implementations. Adoption remains a separate declared Part with
  the standing WIN-side flip-census review; class 5804 is NOT
  complete until the k02 adoption Part.

## Honest disclosures

- The runner `scripts/gate_runner.sh` is byte-identical to the
  published u04/thirteenth/fourteenth/fifteenth-k01/k03 cppgate
  runner (sha256 `f2ebcc3e...`). The summary generator
  `scripts/make_summary.py` is the k03 kit's generator with the
  schema string and one comment line adapted to k02 (sha256
  `5fb2c511...`; G0 input pins, G1 status log, G2 raw-vs-expected
  + pair determinism; fail-closed, writes nothing on failure).
- The k02 input is byte-identical to the published L50M escalation
  kit input (sha256 `fda5d01d...`, pinned in input/gate-rows.json);
  anchor inputs are byte-identical to the published fifteenth k01
  cppgate kit inputs.
- No k02 adoption is performed by this Part. NO verdict consumed.
  The standard 11x11 empty board, all 19 central-reply roots, the
  two-stone root {60,27} and its remaining third moves 100/108
  stay UNKNOWN.
