# n11 fifteenth ladder-top class 5804 batch escalation (2026-11-28)

Execution kit of the escalation declared in
`research/log/2026-11-28-n11-fifteenth-ladder-top-escalation-declaration.md`
(publish-then-execute, declaration commit `8340f669`, amendment `c8eed460`,
single owner). Selected by the published fifteenth ladder-top selection kit
(`research/experiments/n11-fifteenth-ladder-top-selection-20261128/`,
commit `6f6deac0`, log `7da320b9`): ladder-top class 5804, exactly 3
remaining unknown S5 keys, against the canonical head of record
`a66f636e...` (6,897 rows WIN 215 / LOSS 6,682).

Declaration amendment note: the initial declaration commit `8340f669`
mis-stated the class-5804 parenthetical key string; amendment
`c8eed460` corrected it to the three selection-kit keys and was
published BEFORE any stage-1 run of this Part was executed. Scope,
key set, method and order are unchanged by the amendment.

## Result

Declared order: k01, k02, k03; stage-1 2M cold pair each, then
15M escalation under the WIN-stop rule.

| key | stage-1 2M | 15M escalation | pair |
|---|---|---|---|
| k01 `6053682324116078592:0` (s5_index 207094, legal 82) | UNKNOWN(0), nodes 2,000,000 | **WIN(1), nodes 12,803,283**, wall_s 70/69 | node-identical (2M and 15M) |
| k02 `6052837899185946628:128` (s5_index 212115, legal 87) | UNKNOWN(0), nodes 2,000,000 | suppressed (WIN-stop) | node-identical (wall_s 9 vs 8) |
| k03 `6053400849139367936:128` (s5_index 212536, legal 92) | UNKNOWN(0), nodes 2,000,000 | suppressed (WIN-stop) | byte-identical (2M) |

The WIN-stop rule fired on k01's WIN(1) at 15M: k02/k03
escalations were suppressed and they stay stage-1 2M UNKNOWN. No
other key was run at any higher budget in this Part. k01 is the
key that stayed 2M UNKNOWN as the fourteenth batch's k02; its
first resolution is this Part's 15M WIN(1).

Calibration (pre-declaration, disclosed in the declaration): u01
`1153485622925590528:0` at 2M reproduces the published fourteenth
escalation kit's calibration raw values exactly (result 0, nodes
2,000,000, forbidden quadruples 95,670, wall_s 9); only stdout
footer line ordering differs (host buffering), so the raw file
sha differs from the fourteenth kit's raw while all values are
identical.

## Claim status

This kit is batch bookkeeping only: NO verdict is consumed. The
k01 WIN row is single-implementation (jsreplay replica, cold
pair) and requires the C++ second-implementation scrutiny gate
plus a third-implementation corroboration before any adoption
Part; a k01 adoption would additionally require the standing
WIN-side flip-census review. Class 5804 is NOT complete (k02/k03
remain unknown), so no free_now flip is claimed here. 11x11
empty board remains UNKNOWN.

## Files

- `batch-summary.json` - machine-readable summary (schema
  `n11-fifteenth-ladder-top-escalation-summary-v1`), head basis,
  runner pin (jsreplay sha256 `84585617...`), declared order,
  stage-1/15M results, WIN-stop firing, calibration, disclosures,
  status guard.
- `k01-k03.input.csv`, `cal-u01.input.csv` - probe input rows;
  the three key CSVs are byte-identical to the fifteenth
  selection kit's `input/` files.
- `raws/cal-u01-at2m.raw` - calibration raw (host footer order;
  values identical to the fourteenth kit's calibration).
- `raws/at2m-kXX-p1/p2.raw` - stage-1 2M cold pairs.
- `raws/at15m-k01-p1/p2.raw` - 15M escalation cold pair,
  node-identical (wall_s 70 vs 69).
- `MANIFEST-sha256.txt` - sha256 of every kit file.
