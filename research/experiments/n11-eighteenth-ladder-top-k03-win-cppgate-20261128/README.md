# n11 eighteenth ladder-top k03 WIN cppgate

Execution kit of the C++ second-implementation scrutiny gate for
the eighteenth class 20421 k03 WIN row
(`1155173441859489792:131072`, class 20421, legal 73, s5_index
605961, WIN(1) nodes 5,266,012 @15M, eighteenth escalation kit
`88e825d5`), declared in
`research/log/2026-11-28-n11-eighteenth-ladder-top-k03-pillars-declaration.md`
(commit `26143236`, single owner, publish-then-execute), against
the canonical head of record `e56ca5ca...` (6,902 rows WIN 220 /
LOSS 6,682; target absent from the head, host-measured 0 rows).

## Result

GATE-PASS `73,15000000,1,5266012` - the fresh-cold C++ pair is
node-exact against the published eighteenth escalation raw (k03
WIN(1) at 15M) on (legal, budget, result, nodes), with 2-pass
determinism. Anchors 3/3: at2m `98,2000000,0,2000000`, aj001
`84,30000000,2,5156075`, af039 `89,30000000,2,19234232` (anchor
inputs byte-identical to the published seventeenth k02 gate kit
pins, disclosed in the declaration).

- G0 input pins: k03 `ff63ed29...` (byte-clone of the published
  eighteenth escalation kit input) + 3 anchor pins.
- G1 status log sanity: GATE-PASS lines for k03 and all anchors.
- G2 raw-vs-expected + fresh-cold pair determinism on all four
  rows.
- G3 anchor raw sha cross-kit pins (in gate-rows.json).
- Tamper battery 4/4 fail-closed (T1 wrong expected pin rc=43,
  T2 raw node edit rc=42, T3 missing input rc=2, T4
  gate-rows.json expected-pin flip caught by the summary gate G2
  rc=1) + clean control re-PASS (SUMMARY-PASS, byte-identical
  summary; all inputs restored byte-identical, sha-verified).
  The tamper T1/T2 lines remain in `output/gate-status.log` as
  the honest execution record; the full battery stdout is
  published as `output/tamper-battery-stdout.log`.
- With the companion third-implementation corroboration kit
  (`n11-eighteenth-ladder-top-k03-thirdimpl-20261128`,
  CORROBORATION-PASS, result 1, expansions 6,039,011 x2
  identical), the two-pillar requirement for the k03 WIN row is
  COMPLETE: verdict-level WIN(1) agreement across all three
  implementations (jsreplay replica, C++ gate, third
  implementation). Adoption remains a separate declared Part
  (canonical merge + flip-census/reaudit with owner-union
  precheck [18136, 18143, 20128, 20421]); class 20421 is NOT
  complete (k04-k05 remain stage-1 2M UNKNOWN).

## Honest disclosures

- The gate binary is the pinned-source zig 0.13.0 build (source
  `9193f5b6`/`5976935d`/`2e36d694`, tarball pin `d45312e6`);
  it is re-verified here by the anchor rows' expected quads
  before the target row runs.
- The anchors are byte-identical to the published seventeenth
  k02 gate kit pins (re-fetched this session, sha-verified), and
  their raw quads reproduce the published expected values.
- This lane runs without access to the user's computer
  (scheduled task); publication is via the GitHub API only.

## Files

- `input/` - k03.input.csv (published escalation input pin) +
  3 anchor inputs + gate-rows.json (kit schema
  `n11-eighteenth-ladder-top-k03-cppgate-rows-v1`).
- `scripts/gate_runner.sh` - the gate runner (machine-identical
  to the published seventeenth k02 runner; only the comment
  block differs).
- `scripts/make_summary.py` - the fail-closed summary maker
  (machine-identical to the published seventeenth k02 maker
  except docstring and schema name).
- `output/gate-status.log` - honest per-row status (incl. tamper
  T1/T2 fail lines).
- `output/raw/*.out` - 8 cold-pass raws (k03 + 3 anchors, p1/p2).
- `output/cppgate-summary.json` - machine-readable summary
  (schema `n11-eighteenth-ladder-top-k03-cppgate-summary-v1`).
- `output/tamper-battery-stdout.log` - the full tamper battery
  stdout (4/4 fail-closed + clean control).
- `MANIFEST-sha256.txt` - sha256 of every kit file.

## Status guard

Pillar bookkeeping only: NO verdict consumed. Even with the
two-pillar COMPLETE, the k03 WIN(1) row is NOT adopted by this
kit; adoption requires a separate single-owner declaration.
Class 20421 is NOT complete (k04-k05 remain stage-1 2M UNKNOWN).
The standard 11x11 empty board, the 19 central-reply roots, the
two-stone root {60,27} and third moves 100/108 stay UNKNOWN.
Nodes/expansions are bookkeeping, never verdicts.
