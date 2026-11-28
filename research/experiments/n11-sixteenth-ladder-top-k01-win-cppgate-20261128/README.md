# n11 sixteenth ladder-top k01 WIN-row C++ scrutiny gate

Execution kit of the C++ second-implementation scrutiny gate for the
sixteenth class 20421 k01 WIN row (`1155454779397246976:131072`,
class 20421, legal 76, s5_index 528689, WIN(1) nodes 5,273,778 @15M,
sixteenth escalation kit `n11-sixteenth-ladder-top-escalation-20261128`,
declaration `4d361b73`, kit `85edd462`, completion log `775e1a6f`), under
the canonical head of record `58110025...` (6,900 rows WIN 218 / LOSS 6,682;
k01 verified fresh/absent from the head by the sixteenth escalation kit).
Declared in `research/log/2026-11-28-n11-sixteenth-ladder-top-k01-pillars-declaration.md`
(commit `60f4bac8`, single owner, publish-then-execute); the k01 target
runs happened only after that declaration was on main. The gate binary
and the three anchors were scratch-verified on this host before the
declaration (3/3 GATE-PASS, disclosed in the declaration, per the
standing thirteenth/fourteenth/fifteenth precedent).

## Results

- **k01 GATE-PASS `76,15000000,1,5273778`** (fresh-cold pair, two
  processes, 2-pass determinism; node-exact vs the published sixteenth
  escalation raw pair (jsreplay) nodes 5,273,778, result WIN(1);
  wall_s host wall-clock only). Gate source `9193f5b6...` + headers
  `5976935d...`/`2e36d694...` (standing pins, sha-verified on this
  host), zig 0.13.0 tarball pin `d45312e6...` (re-verified on
  download), `-std=c++20 -O2` per the standing build recipe.
- Anchors (published-raw-pinned, all GATE-PASS, pair
  node-identical): anchor-at2m `98,2000000,0,2000000`,
  anchor-aj001 `84,30000000,2,5156075`, anchor-af039
  `89,30000000,2,19234232`, with the published anchor input pins
  (`ecc0299b...`/`2f6daea5...`/`e51a3c9d...`, byte-verified).
- Tamper battery 4/4 fail-closed (T1 wrong expected pin rc=43, T2
  raw node edit rc=42, T3 missing input rc=2, T4 gate-rows.json
  expected-pin flip caught by the summary gate G2 rc=1) + clean
  control re-PASS (SUMMARY-PASS, byte-identical summary; all inputs
  restored byte-identical, sha-verified). The tamper T1/T2 lines
  remain in `output/gate-status.log` as the honest execution record.
- With the companion third-implementation corroboration kit
  (`n11-sixteenth-ladder-top-k01-thirdimpl-20261128`,
  CORROBORATION-PASS, result 1, expansions 6,003,522 x2 identical),
  the two-pillar requirement for the k01 WIN row is COMPLETE:
  verdict-level WIN(1) agreement across all three implementations
  (jsreplay replica, C++ gate, third implementation). Adoption
  remains a separate declared Part (canonical merge + flip-census/
  reaudit with owner-union precheck [15647, 16901, 20421]); class
  20421 is NOT complete (k02-k05 remain stage-1 2M UNKNOWN).

## Honest disclosures

- The runner `scripts/gate_runner.sh` is byte-identical to the
  published u04/thirteenth/fourteenth/fifteenth-k02 cppgate runner
  (sha256 `f2ebcc3e...`). The summary generator
  `scripts/make_summary.py` is the fifteenth k02 kit's generator with
  the kit-name/schema strings adapted to sixteenth k01 (schema
  `n11-sixteenth-ladder-top-k01-cppgate-summary-v1`).
- Anchor raws were produced pre-declaration (scratch) on this host
  and copied into this kit byte-identically; the k01 target raws were
  produced post-declaration. All four rows re-verified by the fresh
  summary generator (G0-G3) after the target run.
- No verdict consumed. NO interpretation of nodes/expansions as
  distance or solved count. The standard 11x11 empty board, the 19
  central-reply roots, two-stone root {60,27}, third move
  {100,108}, and every closure class remain UNKNOWN.

## Files

- `input/k01.input.csv` - byte-clone of the sixteenth escalation kit
  `k01.input.csv` (pin `6288b82f...`).
- `input/anchor-at2m.input.csv`, `input/anchor-aj001.input.csv`,
  `input/anchor-af039.input.csv` - byte-identical to the published
  anchor input pins.
- `input/gate-rows.json` - target/anchor rows, expected pins, gate
  source pins, escalation basis raw pins, head basis.
- `scripts/gate_runner.sh`, `scripts/make_summary.py` - runner and
  fail-closed summary generator.
- `output/gate-status.log` - honest per-row status (incl. tamper
  T1/T2 fail lines).
- `output/raw/*.out` - 8 cold-pass raws (k01 + 3 anchors, p1/p2).
- `output/cppgate-summary.json` - machine-readable summary
  (schema `n11-sixteenth-ladder-top-k01-cppgate-summary-v1`).
- `MANIFEST-sha256.txt` - sha256 of every kit file.
