# n11 fifteenth ladder-top k01 WIN-row C++ scrutiny gate

Execution kit of the C++ second-implementation scrutiny gate for the
fifteenth ladder-top escalation k01 WIN row
(`6053682324116078592:0`, class 5804, legal 82, s5_index 207094,
WIN(1) nodes 12,803,283 @15M, kit
`n11-fifteenth-ladder-top-escalation-20261128`, commit `a33217ca`,
log `73b1610f`), under the canonical head of record `a66f636e...`
(6,897 rows WIN 215 / LOSS 6,682; k01 verified fresh/absent by the
fifteenth selection and escalation Parts).  Declared in
`research/log/2026-11-28-n11-fifteenth-ladder-top-k01-pillars-declaration.md`
(commit `f3273401`, single owner); the k01 target runs happened only
after that declaration was on main (anchors/build were scratch).

## Results

- **k01 GATE-PASS `82,15000000,1,12803283`** (fresh-cold pair
  node-identical, node-exact vs the published escalation raw pair
  sha256 `29a8b80c...`/`ee4048d5...`; wall_s ~25 each, host
  wall-clock only).  Gate source `9193f5b6...` + headers
  `5976935d...`/`2e36d694...` (byte-fetched from the published
  tenth-cost k01k02 cppgate kit, sha256-verified against the
  standing pins), zig 0.13.0 (tarball pin `d45312e6...`,
  sha256-verified this session), `-std=c++20 -O2` per the standing
  build recipe.
- Anchors (published-raw-pinned, all GATE-PASS, pair node-identical):
  anchor-at2m `98,2000000,0,2000000`, anchor-aj001
  `84,30000000,2,5156075`, anchor-af039 `89,30000000,2,19234232`.
  Anchor raws are node-exact vs the published fourteenth kit raws;
  two differ only in wall_s (af039.p1 38 vs 39, aj001.p2 9 vs 10,
  host wall-clock only) - cross-host determinism node-exact
  throughout.
- Tamper battery 4/4 fail-closed (T1 wrong expected pin rc=43, T2
  raw nodes edit rc=42, T3 missing input rc=2, T4 gate-rows.json
  expected-pin flip caught by the summary gate G2 rc=1) + clean
  control re-PASS (SUMMARY-PASS, byte-identical summary
  `8ec7bdc3...`).
- With the companion third-impl corroboration kit
  (`n11-fifteenth-ladder-top-k01-thirdimpl-20261128`,
  CORROBORATION-PASS, result 1, expansions 15,077,486 x2 identical),
  the two-pillar requirement for the k01 WIN row is COMPLETE.
  Verdict-level WIN(1) agreement across all three implementations.
  Adoption remains a separate declared Part with the standing
  WIN-side flip-census review; class 5804 completion additionally
  requires k02/k03 (still 2M UNKNOWN).

## Honest disclosures

- The runner `scripts/gate_runner.sh` is byte-identical to the
  published u04/thirteenth/fourteenth cppgate runner (sha256
  `f2ebcc3e...`, comment block still names the ultra-cheap u04 kit).
  The summary generator `scripts/make_summary.py` is the fourteenth
  kit's generator with the schema/kit strings adapted to fifteenth
  (2-line diff; G0 input pins, G1 status log, G2 raw-vs-expected +
  pair determinism; fail-closed, writes nothing on failure).
- The k01 input is byte-identical to the published fifteenth
  escalation kit input (sha256-pinned in input/gate-rows.json);
  anchor inputs are byte-identical to the published fourteenth kit
  inputs.
- The first tamper-battery invocation in this session had an rc-echo
  bug (rc read after a `mv`, spuriously printing 0 for T2-T4); the
  battery was re-run cleanly with stdout captured
  (`output/tamper-battery-stdout.log`, 4/4 fail-closed + clean
  control).  The buggy first attempt is disclosed here and is not
  used as evidence.
- No k01 adoption is performed by this Part.  NO verdict consumed.
