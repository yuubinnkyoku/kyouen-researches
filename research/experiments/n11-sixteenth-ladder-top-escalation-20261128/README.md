# n11 sixteenth ladder-top escalation 2026-11-28

Execution kit of the escalation declared in
`research/log/2026-11-28-n11-sixteenth-ladder-top-escalation-declaration.md`
(publish-then-execute, declaration commit `4d361b73`, single owner).
Escalates the five selected keys of the published sixteenth
ladder-top selection (class 20421 `1155173304420536320:131072`,
kit `b4e338aa`, completion `27829d8c`) against the canonical head
of record `58110025...` (6,900 rows WIN 218 / LOSS 6,682); all five
keys verified fresh to the head by the published selector.

## Result

Declared order k01 -> k05, WIN-stop at the first WIN(1).

| key | stage-1 2M | 15M escalation | pair |
|---|---|---|---|
| k01 `1155454779397246976:131072` (s5 528689, legal 76) | UNKNOWN(0), nodes 2,000,000 | **WIN(1), nodes 5,273,778** (35.2% of budget), wall_s 30/29 | node-identical |
| k02 `1156299204327378944:131072` (s5 543795, legal 73) | UNKNOWN(0), nodes 2,000,000 | not escalated (WIN-stop) | node-identical |
| k03 `1155173441859489792:131072` (s5 605961, legal 73) | UNKNOWN(0), nodes 2,000,000 | not escalated (WIN-stop) | node-identical |
| k04 `1153062242096250880:540672` (s5 620742, legal 83) | UNKNOWN(0), nodes 2,000,000 | not escalated (WIN-stop) | node-identical |
| k05 `1152921642046849024:68719477248` (s5 625899, legal 78) | UNKNOWN(0), nodes 2,000,000 | not escalated (WIN-stop) | node-identical |

The WIN-stop rule fired at k01 (WIN(1) at 15M); k02-k05 stay at
stage-1.  The stage-1 prediction (all five UNKNOWN with budget
exhaustion) held exactly.

Calibration (after the declaration, before the runs): u01
`1153485622925590528:0` at 2M reproduces the published fifteenth
escalation kit's calibration VALUES exactly (result 0, nodes
2,000,000, forbidden quadruples 95,670, wall_s 10 vs published 9
host-difference); the input csv is byte-identical to the published
calibration (`52d79efc`).

Owner-union precheck (disclosed in the declaration, derived from
the frozen graph `54f9c364`): k01 [15647, 16901, 20421] / k02
[16104, 16132, 16656, 20421] / k03 [18136, 18143, 20128, 20421] /
k04 [18534, 18554, 19885, 20421] / k05 [18683, 18710, 20421];
serving class 20421 is ladder rank 1 (unknown_now 5).

## Claim status

This kit is escalation bookkeeping only: NO verdict is consumed.
The k01 WIN(1) row is single-implementation (jsreplay replica, cold
pair) and requires the C++ second-implementation scrutiny gate plus
a third-implementation corroboration before any adoption Part; a
k01 adoption would additionally require the standing WIN-side
flip-census review.  Class 20421 is NOT complete (k02-k05 remain
unknown).  The standard 11x11 empty board, all 19 central-reply
roots, the two-stone root {60,27} and third moves 100/108 remain
UNKNOWN.

## Files

- `DECLARATION.md` - mirror of the published declaration
  (commit `4d361b73`).
- `batch-summary.json` - machine-readable summary (schema
  `n11-sixteenth-ladder-top-escalation-summary-v1`), head basis,
  runner pin (jsreplay sha256 `84585617...`), declared order,
  calibration, stage-1 and 15M results, WIN-stop firing, owner-union
  precheck, disclosures, status guard.
- `k01..k05.input.csv`, `cal-u01.input.csv` - probe input rows,
  byte-verified copies of the published sixteenth selection kit's
  input files and the published fifteenth calibration.
- `raws/cal-u01-at2m.raw` - calibration raw.
- `raws/at2m-k01..k05-p1/p2.raw` - stage-1 2M cold pairs (all
  node-identical within pair, wall_s 9-10).
- `raws/at15m-k01-p1/p2.raw` - k01 15M cold pair, node-identical
  (wall_s 30/29).
- `MANIFEST-sha256.txt` - sha256 of every kit file.
