# n11 thirteenth ladder-top class 16757 batch escalation (2026-11-28)

Execution kit of the escalation declared in
`research/log/2026-11-28-n11-thirteenth-ladder-top-escalation-declaration.md`
(publish-then-execute, declaration commit `07003c2a`, single owner).
Selected by the published thirteenth ladder-top selection kit
(`research/experiments/n11-thirteenth-ladder-top-selection-20261128/`,
commit `fa4e6cb2`, log `2ca98e1c`): class 16757
(`1153204079095185408:65536`), exactly 2 remaining unknown S5 keys,
against the canonical head of record `beecb024...` (6,894 rows
WIN 212 / LOSS 6,682).

## Result

Declared order: k01 then k02, stage-1 2M cold pair each, then 15M
escalation under the WIN-stop rule.

| key | stage-1 2M | 15M escalation | pair byte-identical |
|---|---|---|---|
| k01 `1153204147814662144:65536` (s5_index 556117, legal 72) | UNKNOWN(0), nodes 2,000,000 | **WIN(1), nodes 2,678,305**, wall_s 12 | yes (2M and 15M) |
| k02 `1152922672837951488:65792` (s5_index 558553, legal 72) | UNKNOWN(0), nodes 2,000,000 | suppressed (WIN-stop) | yes (2M) |

The WIN-stop rule fired on k01's WIN(1) at 15M: k02's escalation was
suppressed and k02 stays stage-1 2M UNKNOWN. No other key was run at
any budget in this Part.

## Claim status

This kit is batch bookkeeping only: NO verdict is consumed. The k01
WIN row is single-implementation (jsreplay replica, cold pair) and
requires the C++ second-implementation scrutiny gate plus a
third-implementation corroboration before any adoption Part; a k01
adoption would additionally require the standing WIN-side flip-census
review. Class 16757 is NOT complete (k02 remains unknown), so no
free_now flip is claimed here. 11x11 empty board remains UNKNOWN.

## Files

- `batch-summary.json` - machine-readable summary (schema
  `n11-thirteenth-ladder-top-escalation-summary-v1`), head basis,
  runner pin, declared order, stage-1/15M results, WIN-stop firing,
  calibration, disclosures, status guard.
- `k01.input.csv` / `k02.input.csv` - probe input rows from the
  selection kit (identical bytes to that kit's `input/` files).
- `raws/at2m-k01-p1.raw`, `at2m-k01-p2.raw` - stage-1 2M cold pair,
  byte-identical (WIN-stop gate input).
- `raws/at2m-k02-p1.raw`, `at2m-k02-p2.raw` - stage-1 2M cold pair,
  byte-identical.
- `raws/at15m-k01-p1.raw`, `at15m-k01-p2.raw` - 15M escalation cold
  pair, fully byte-identical including wall_s 12.
- `raws/cal-u01-at2m.raw` - pre-declaration calibration (u01 at 2M,
  disclosed in the declaration), values identical to the published
  u03/u04 escalation kits' calibration raws.
- `MANIFEST-sha256.txt` - sha256 of every file in this kit.

## Inputs (published elsewhere)

jsreplay runner sha256
`845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`,
invoked as `node jsreplay.js --exact-replay=<input.csv>
--exact-replay-budget=<N> --only=5 --memo=22`; head of record
`beecb024...`; all selection-kit dependency pins are inherited
unchanged from commit `fa4e6cb2`.
