# 2026-11-28 n11 sixteenth ladder-top escalation completion

Completion log for the stage-1 2M + 15M WIN-stop escalation of the
five keys selected by the sixteenth ladder-top selection (class
20421), declared single-owner publish-then-execute at `4d361b73`
(`research/log/2026-11-28-n11-sixteenth-ladder-top-escalation-declaration.md`),
kit published at `85edd462`
(`research/experiments/n11-sixteenth-ladder-top-escalation-20261128/`,
23 files, fetch-back 23/23 byte-identical at commit pin `85edd462`).

## Executed and measured

- Calibration u01 `1153485622925590528:0` @2M: result 0, nodes
  2,000,000, forbidden quadruples 95,670 - values identical to the
  published fifteenth escalation kit calibration (wall_s 10 vs 9
  host-difference); input csv byte-identical (`52d79efc`).
- Stage-1 2M cold pairs, all five keys: **UNKNOWN(0), nodes
  2,000,000, budget exhausted** - the pre-registered stage-1
  prediction held exactly; all pairs node-identical (wall_s 9-10).
- 15M escalation, declared order: **k01 `1155454779397246976:131072`
  (s5 528689, legal 76) resolved WIN(1) at nodes 5,273,778 (35.2%
  of budget), cold pair node-identical (wall_s 30/29)**.  The
  WIN-stop rule fired at k01; k02-k05 stay at stage-1 2M UNKNOWN.
- Owner-union precheck disclosed in the declaration and measured
  from the frozen graph `54f9c364` (k01 [15647, 16901, 20421] /
  k02 [16104, 16132, 16656, 20421] / k03 [18136, 18143, 20128,
  20421] / k04 [18534, 18554, 19885, 20421] / k05 [18683, 18710,
  20421]).
- Deviation from the declared plan: none.  Main HEAD at this
  completion-log push: `85edd462da702f08e48eb6c8d0dcfcf889be9e6a`.

## Next (not claimed here)

The k01 WIN(1) row is single-implementation (jsreplay replica).
Before any adoption Part it requires the C++ second-implementation
scrutiny gate (expected gate row `1,15000000,1,5273778` @15M cap,
fresh cold pair, anchors, tamper battery) plus a third-implementation
corroboration, then a fresh single-owner adoption declaration
(increment + merger + flip census/reaudit with the shared-owner
pre-exclusion caveat).  Class 20421 is NOT complete (k02-k05 remain
unknown).

## Claim status

Escalation bookkeeping only: NO verdict is claimed or consumed.  The
standard 11x11 empty board: UNKNOWN.  All 19 central-reply roots:
UNKNOWN.  Two-stone root {60,27}: UNKNOWN.  Third-move pair
{100,108}: UNKNOWN.  Every closure class (including 20421) stays
UNKNOWN.  Nodes, expansions and wall_s are bookkeeping, never
verdicts.
