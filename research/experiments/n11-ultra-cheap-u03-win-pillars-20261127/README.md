# n11 ultra-cheap u03 WIN-row pillars (C++ scrutiny gate + third-implementation corroboration)

Execution kit of the pillars declared in
`research/log/2026-11-27-n11-ultra-cheap-u03-win-pillars-declaration.md`
(publish-then-execute, declaration commit `693fecf7`), for the u03
escalation WIN row (`1153202979851993088:272`, class 16371, legal 78,
s5 index 550879, WIN(1) nodes 2,909,040 @15M, kit
`n11-ultra-cheap-u03-escalation-15m-20261127`, commit `36f0cd2c`),
under the canonical head of record `82b52577...` (6,892 rows WIN 210 /
LOSS 6,682; u03 verified fresh/absent).

## Results

- **C++ second-implementation scrutiny gate: u03 GATE-PASS
  `78,15000000,1,2909040`** (fresh-cold pair byte-identical,
  node-exact vs the published escalation raw).  Gate source
  `9193f5b6...` + headers `5976935d...`/`2e36d694...`
  (byte-verified against the published u02 pillars kit), zig 0.13.0
  (tarball pin `d45312e6...`).
- Anchors (published-raw-pinned, all GATE-PASS): anchor-at2m
  `98,2000000,0,2000000` (pair byte-identical), anchor-aj001
  `84,30000000,2,5156075` (pair byte-identical), anchor-af039
  `89,30000000,2,19234232` (pair node-identical; wall_s 38 vs 39,
  host wall-clock only).
- **Third-implementation corroboration: CORROBORATION-PASS** -
  third_impl.js `08ea958f...`, `--cap=400000000 --wallcap=260
  --memo-power=22`, two independent cold passes, **result 1 (WIN),
  expansions 3,305,845 on both passes** (all fields identical except
  wall_s 9.88 vs 9.97).  Verdict-level WIN(1) agreement across all
  three implementations (replica escalation, C++ gate, third_impl).
- Tamper battery 4/4 fail-closed (T1 wrong expected pin rc=43, T2 raw
  nodes edit rc=42, T3 missing input rc=2, T4 third_impl legal
  mismatch rc=1 - third_impl's own GATE_FAIL exit code).

## Honest disclosures

- The runner `scripts/gate_runner.sh` is a comment-block-only
  transform of the published u02 pillars runner (code region
  machine-verified identical; only the naming comment differs).
- T4's auxiliary python checker crashed on third_impl's unexpected
  error-message format, but the recorded rc=1 is third_impl's own
  GATE_FAIL exit code, re-verified directly
  (`third,...,GATE_FAIL,"legal count mismatch: derived=78
  declared=79"`, exit 1).
- No u03 adoption is performed by this Part.  A u03 canonical
  adoption additionally requires the standing WIN-side flip-census
  review (class 16371 completion would be Board-verified free_now at
  adoption time).

## Files

- input/gate-rows.json - machine pin of the target, anchors and head
  basis (schema n11-ultra-cheap-u03-win-pillars-rows-v1).
- input/u03.input.csv, input/anchor-*.input.csv - probe inputs
  (u03 byte-verified against the published batch kit input).
- output/raw/*.out - the eight fresh-cold gate raws.
- output/gate-status.log - runner status lines.
- output/ti/u03.p1.txt, output/ti/u03.p2.txt - the third_impl pair.
- output/tamper-battery-stdout.log - the 4/4 fail-closed battery.
- output/pillars-summary.json - machine summary (schema
  n11-ultra-cheap-u03-win-pillars-summary-v1).
- scripts/gate_runner.sh - the gate runner.
- MANIFEST-sha256.txt - sha256 of every published file (excluding
  itself).

## Status guard

Pillar bookkeeping only; NO verdict consumed; nodes/expansions are
bookkeeping, never evidence.  The standard 11x11 empty board, the
two-stone root {60,27} and its remaining third moves 100/108 stay
UNKNOWN.
