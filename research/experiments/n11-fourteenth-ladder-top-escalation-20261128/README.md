# n11 fourteenth ladder-top class 5804 batch escalation (2026-11-28)

Execution kit of the escalation declared in
`research/log/2026-11-28-n11-fourteenth-ladder-top-escalation-declaration.md`
(publish-then-execute, declaration commit `86a8b791`, single owner).
Selected by the published fourteenth ladder-top selection kit
(`research/experiments/n11-fourteenth-ladder-top-selection-20261128/`,
commit `a85f9c20`, log `0d251e82`): class 5804
(`6053400849139367936:0`), exactly 4 remaining unknown S5 keys,
against the canonical head of record `d772f73c...` (6,896 rows
WIN 214 / LOSS 6,682).

## Result

Declared order: k01, k02, k03, k04; stage-1 2M cold pair each, then
15M escalation under the WIN-stop rule.

| key | stage-1 2M | 15M escalation | pair |
|---|---|---|---|
| k01 `6053401124017274880:0` (s5_index 198576, legal 86) | UNKNOWN(0), nodes 2,000,000 | **WIN(1), nodes 4,360,661**, wall_s 20 | byte-identical (2M and 15M) |
| k02 `6053682324116078592:0` (s5_index 207094, legal 82) | UNKNOWN(0), nodes 2,000,000 | suppressed (WIN-stop) | byte-identical (2M) |
| k03 `6052837899185946628:128` (s5_index 212115, legal 87) | UNKNOWN(0), nodes 2,000,000 | suppressed (WIN-stop) | byte-identical (2M) |
| k04 `6053400849139367936:128` (s5_index 212536, legal 92) | UNKNOWN(0), nodes 2,000,000 | suppressed (WIN-stop) | node-identical (wall_s 9 vs 8) |

The WIN-stop rule fired on k01's WIN(1) at 15M: k02/k03/k04
escalations were suppressed and they stay stage-1 2M UNKNOWN. No
other key was run at any higher budget in this Part.

Calibration (pre-declaration, disclosed in the declaration): u01
`1153485622925590528:0` at 2M reproduces the published thirteenth
escalation kit's calibration raw values exactly (result 0, nodes
2,000,000, forbidden quadruples 95,670, wall_s 9); only stdout footer
line ordering differs (host buffering).

## Claim status

This kit is batch bookkeeping only: NO verdict is consumed. The k01
WIN row is single-implementation (jsreplay replica, cold pair) and
requires the C++ second-implementation scrutiny gate plus a
third-implementation corroboration before any adoption Part; a k01
adoption would additionally require the standing WIN-side flip-census
review. Class 5804 is NOT complete (k02/k03/k04 remain unknown), so
no free_now flip is claimed here. 11x11 empty board remains UNKNOWN.

## Files

- `batch-summary.json` - machine-readable summary (schema
  `n11-fourteenth-ladder-top-escalation-summary-v1`), head basis,
  runner pin (jsreplay sha256 `84585617...`), declared order,
  stage-1/15M results, WIN-stop firing, calibration, disclosures,
  status guard.
- `k01-k04.input.csv` - probe input rows, byte-identical to the
  selection kit's `input/` files.
- `cal-u01.input.csv` + `raws/cal-u01-at2m.raw` - calibration.
- `raws/at2m-kXX-p1/p2.raw` - stage-1 2M cold pairs.
- `raws/at15m-k01-p1/p2.raw` - 15M escalation cold pair, fully
  byte-identical (wall_s 20 both).
- `MANIFEST-sha256.txt` - sha256 of every kit file.
