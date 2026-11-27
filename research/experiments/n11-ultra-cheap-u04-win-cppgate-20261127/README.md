# n11 ultra-cheap u04 WIN-row C++ scrutiny gate (the last open pillar)

Execution kit of the C++ second-implementation scrutiny gate for the u04
escalation WIN row (`1152921505747697664:1032`, class 23101, legal 85,
s5 index 745184, WIN(1) nodes 9,149,084 @15M, kit
`n11-ultra-cheap-u04-escalation-15m-20261127`, commit `24c5b85f`),
under the canonical head of record `c5082866...` (6,893 rows WIN 211 /
LOSS 6,682; u04 verified fresh/absent by the escalation Part).

This Part closes the pillar that the published third-impl kit
`n11-ultra-cheap-u04-thirdimpl-20261127` (commit `2691ac04`,
CORROBORATION-PASS, expansions 10,728,035 x2 identical) had to leave
OPEN because that execution environment had no C/C++ toolchain.

## Results

- **u04 GATE-PASS `85,15000000,1,9149084`** (fresh-cold pair
  node-identical, node-exact vs the published escalation raw; wall_s
  17 vs 18, host wall-clock only).  Gate source
  `9193f5b6...` + headers `5976935d...`/`2e36d694...`
  (byte-fetched from the published tenth-cost k01k02 cppgate kit and
  sha256-verified against the standing pins), zig 0.13.0 (tarball pin
  `d45312e6...`), `-std=c++20` per the standing build recipe.
- Anchors (published-raw-pinned, all GATE-PASS, pair node-identical):
  anchor-at2m `98,2000000,0,2000000`, anchor-aj001
  `84,30000000,2,5156075`, anchor-af039 `89,30000000,2,19234232`
  (af039 pair wall_s 38 vs 37).  The anchor raws reproduce the
  published u03 pillars kit raw sha256 values exactly (cross-host
  determinism).
- Tamper battery 4/4 fail-closed (T1 wrong expected pin rc=43, T2
  raw nodes edit rc=42, T3 missing input rc=2, T4 gate-rows.json
  expected-pin flip caught by the summary gate G1 rc=1) + clean
  control re-PASS.
- **Two-pillar requirement for the u04 WIN row is now COMPLETE**
  (escalation replica + C++ gate here + published third-impl
  corroboration).  Verdict-level WIN(1) agreement across all three
  implementations.  Adoption remains a separate declared Part with
  the standing WIN-side flip-census review.

## Honest disclosures

- The runner `scripts/gate_runner.sh` is a comment-block-only
  transform of the published u03 pillars runner (code region
  machine-verified identical).  The summary generator
  `scripts/make_summary.py` is fresh for this kit (G0 input pins,
  G1 status-log, G2 raw-vs-expected + pair determinism, G3 anchor
  cross-kit raw sha pins, G4 third-impl kit cross-pin fetched from
  main; fail-closed, writes nothing on failure).
- Execution preceded declaration publication within this single
  session (the environment unexpectedly had a usable toolchain this
  time; the build/run was treated as scratch until all anchors
  passed).  All pinned expectations come from the published
  escalation raw and the kit fails closed on disagreement, so the
  post-hoc declaration cannot mask any outcome.  No other key was
  run at any budget in this Part.
- The u04 input is byte-verified against the published escalation
  kit input; anchor inputs are byte-identical to the published u03
  pillars kit inputs (sha256-pinned in input/gate-rows.json).
- No u04 adoption is performed by this Part.  A u04 canonical
  adoption additionally requires the standing WIN-side flip-census
  review (serving class 23101 completion must be Board-verified
  free_now at adoption time).

## Files

- input/gate-rows.json - machine pin of the target, anchors, gate
  source, head basis and third-impl kit cross-pin (schema
  n11-ultra-cheap-u04-win-cppgate-rows-v1).
- input/u04.input.csv, input/anchor-*.input.csv - probe inputs.
- output/raw/*.out - the eight fresh-cold gate raws.
- output/gate-status.log - runner status lines.
- output/tamper-battery-stdout.log - the 4/4 fail-closed battery.
- output/cppgate-summary.json - machine summary (schema
  n11-ultra-cheap-u04-win-cppgate-summary-v1).
- scripts/gate_runner.sh, scripts/make_summary.py.
- MANIFEST-sha256.txt - sha256 of every published file (excluding
  itself).

## Status guard

Pillar bookkeeping only; NO verdict consumed; nodes are bookkeeping,
never evidence.  The standard 11x11 empty board, the two-stone root
{60,27} and its remaining third moves 100/108 stay UNKNOWN.
