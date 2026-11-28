# n11 fifteenth ladder-top k03 WIN-row C++ scrutiny gate

Execution kit of the C++ second-implementation scrutiny gate for the
fifteenth class 5804 k03 WIN row (`6053400849139367936:128`,
class 5804, legal 92, s5_index 212536, WIN(1) nodes 3,364,655 @15M,
kit `n11-fifteenth-ladder-top-k02k03-reescalation-20261128`,
declaration `88a24418`, kit+log `09358acd`), under the canonical head
of record `b5f322dd...` (6,898 rows WIN 216 / LOSS 6,682; k03 verified
fresh/absent from the head by the re-escalation Part). Declared in
`research/log/2026-11-28-n11-fifteenth-ladder-top-k03-pillars-declaration.md`
(commit `24194a4f`, single owner); the k03 target runs happened only
after that declaration was on main (anchors/build were scratch).

## Results

- **k03 GATE-PASS `92,15000000,1,3364655`** (fresh-cold pair
  byte-identical, sha256 `8f78e200...` x2; node-exact vs the
  published re-escalation raw pair sha256 `58f2ad9d...` x2,
  byte-identical pair; wall_s 6/6, host wall-clock only). Gate source
  `9193f5b6...` + headers `5976935d...`/`2e36d694...` (byte-fetched
  from the published tenth-cost k01k02 cppgate kit, sha256-verified
  against the standing pins), zig 0.13.0 (tarball pin `d45312e6...`,
  sha-verified this session), `-std=c++20 -O2` per the standing build
  recipe.
- Anchors (published-raw-pinned, all GATE-PASS, pair node-identical):
  anchor-at2m `98,2000000,0,2000000`, anchor-aj001
  `84,30000000,2,5156075`, anchor-af039 `89,30000000,2,19234232`.
  Anchor raws are byte-identical to the published fifteenth k01
  cppgate kit raws (sha256 `aa295618...` x2 / `54f261f6...` /
  `7fa3a106...` / `cfa72d66...` x2), wall_s included - cross-host
  determinism byte-exact on all six anchor raws.
- Tamper battery 4/4 fail-closed (T1 wrong expected pin rc=43, T2
  raw nodes edit rc=42, T3 missing input rc=2, T4 gate-rows.json
  expected-pin flip caught by the summary gate G2 rc=1) + clean
  control re-PASS (SUMMARY-PASS, byte-identical summary; input
  restored byte-identical, sha-verified).
- With the companion third-impl corroboration kit
  (`n11-fifteenth-ladder-top-k03-thirdimpl-20261128`,
  CORROBORATION-PASS, result 1, expansions 3,906,063 x2 identical),
  the two-pillar requirement for the k03 WIN row is COMPLETE.
  Verdict-level WIN(1) agreement across all three implementations.
  Adoption remains a separate declared Part with the standing
  WIN-side flip-census review; class 5804 is NOT complete (k02
  remains 15M UNKNOWN).

## Honest disclosures

- The runner `scripts/gate_runner.sh` is byte-identical to the
  published u04/thirteenth/fourteenth/fifteenth-k01 cppgate runner
  (sha256 `f2ebcc3e...`, comment block still names the ultra-cheap
  u04 kit). The summary generator `scripts/make_summary.py` is the
  fifteenth k01 kit's generator with the schema string and one
  comment line adapted to k03 (2-line diff, sha256 `2f1f6938...`;
  G0 input pins, G1 status log, G2 raw-vs-expected + pair
  determinism; fail-closed, writes nothing on failure).
- The k03 input is byte-identical to the published re-escalation kit
  input (sha256 `cad75b29...`, pinned in input/gate-rows.json);
  anchor inputs are byte-identical to the published fifteenth k01
  cppgate kit inputs.
- The first tamper-battery invocation captured the runner's
  "missing input" line with stderr discarded (T3 rc=2 still
  verified); the battery was re-run with stdout+stderr captured
  (`output/tamper-battery-stdout.log`, 4/4 fail-closed + clean
  control). The first attempt is disclosed here and is not used as
  evidence.
- No k03 adoption is performed by this Part. NO verdict consumed.
  The standard 11x11 empty board, all 19 central-reply roots, the
  two-stone root {60,27} and its remaining third moves 100/108 stay
  UNKNOWN.
