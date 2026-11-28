# n11 nineteenth ladder-top escalation 2026-11-28

Execution kit of the escalation declared in
`research/log/2026-11-28-n11-nineteenth-ladder-top-escalation-declaration.md`
(publish-then-execute, declaration commit `b27b8f24`, single
owner).  Escalates the two remaining stage-1 keys of the class
20421 ladder-top selection against the canonical head of record
`3abecf8b...` (6,903 rows WIN 221 / LOSS 6,682; the eighteenth k03
adoption head); both keys verified fresh to the head by direct
cache scan before the declaration.

## Result

Declared order k04 -> k05, WIN-stop at the first WIN(1).

| key | stage-1 2M (published sixteenth kit `85edd462`) | 15M escalation | pair |
|---|---|---|---|
| k04 `1153062242096250880:540672` (s5 620742, legal 83) | UNKNOWN(0), nodes 2,000,000 | **WIN(1), nodes 6,877,739** (45.9% of budget), wall_s 37/36 | node-identical |
| k05 `1152921642046849024:68719477248` (s5 625899, legal 78) | UNKNOWN(0), nodes 2,000,000 | not escalated (WIN-stop fired at k04) | - |

The WIN-stop rule fired at k04 (WIN(1) at 15M, cold pair
node-identical); k05 stays at stage-1 2M UNKNOWN.  The declared
prediction (both keys resist at 15M) did NOT hold for k04: k04
resolved WIN(1) at 45.9% of budget; the measurement replaces the
prediction.

Calibration (after the declaration, before the runs): u01
`1153485622925590528:0` at 2M reproduces the published calibration
VALUES exactly (result 0, nodes 2,000,000, forbidden quadruples
95,670, wall_s 9; raw byte-identical to the published
sixteenth-kit calibration raw `05ce2090`); input csv byte-identical
(`52d79efc`).

Owner-union precheck (re-derived from the frozen graph on this
host, disclosed): k04 [18534, 18554, 19885, 20421] / k05
[18683, 18710, 20421]; the serving class 20421 is closure-ladder
rank 1 with unknown_now 2 before this Part (k05 is its last
cost-unknown child after k04 resolves).

## Claim status

This kit is escalation bookkeeping only: NO verdict is consumed.
The k04 WIN(1) row is single-implementation (jsreplay replica, cold
pair) and requires the C++ second-implementation scrutiny gate
plus a third-implementation corroboration before any adoption Part;
a k04 adoption would additionally require the standing WIN-side
flip-census review.  Class 20421 is NOT complete (k05 remains
stage-1 2M UNKNOWN).  The standard 11x11 empty board, all 19
central-reply roots, the two-stone root {60,27} and third moves
100/108 remain UNKNOWN.  Nodes are bookkeeping, never verdicts.

## Files

- `DECLARATION.md` - mirror of the published declaration
  (commit `b27b8f24`).
- `batch-summary.json` - machine-readable summary (schema
  `n11-nineteenth-ladder-top-escalation-summary-v1`).
- `k04.input.csv` / `k05.input.csv` / `cal-u01.input.csv` -
  byte-verified copies of the published sixteenth escalation kit's
  input files.
- `cal-u01-at2m.raw` - calibration raw.
- `at15m-k04-p1.raw` / `at15m-k04-p2.raw` - k04 15M cold pair,
  node-identical.
- `MANIFEST-sha256.txt` - sha256 of every kit file.
