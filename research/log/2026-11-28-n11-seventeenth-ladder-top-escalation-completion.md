# 2026-11-28 n11 seventeenth ladder-top escalation completion

Completion log for the 15M WIN-stop escalation of the four
remaining keys of the sixteenth ladder-top selection (class
20421), declared single-owner publish-then-execute at `207339c8`
(`research/log/2026-11-28-n11-seventeenth-ladder-top-escalation-declaration.md`),
kit
`research/experiments/n11-seventeenth-ladder-top-escalation-20261128/`
(12 files).

## Executed and measured

- Calibration u01 `1153485622925590528:0` @2M: result 0, nodes
  2,000,000, forbidden quadruples 95,670, wall_s 9 - values
  identical to the published sixteenth/fifteenth escalation kit
  calibration; input csv byte-identical (`52d79efc`).
- 15M escalation, declared order k02 -> k05: **k02
  `1156299204327378944:131072` (s5 543795, legal 73) resolved
  WIN(1) at nodes 4,997,146 (33.3% of budget), cold pair
  node-identical (wall_s 24/25)**.  The WIN-stop rule fired at
  k02; k03-k05 stay at their published stage-1 2M UNKNOWN(0)
  (sixteenth escalation kit `85edd462`, not re-run here per the
  declaration).
- Owner-union precheck re-derived on this host from the frozen
  graph `54f9c364` and identical to the published sixteenth
  precheck (k02 [16104, 16132, 16656, 20421] / k03 [18136, 18143,
  20128, 20421] / k04 [18534, 18554, 19885, 20421] / k05
  [18683, 18710, 20421]).
- Freshness to the current head `dbc1d950...` (6,901 rows WIN 219
  / LOSS 6,682) measured on this host: the only head delta since
  the published selector run is the adopted k01 WIN row; k02-k05
  are fresh (no k02-k05 key appears in the head).
- Deviation from the declared plan: none.  Main HEAD at this
  completion-log push: see the commit pin of this log.

## Next (not claimed here)

The k02 WIN(1) row is single-implementation (jsreplay replica).
Before any adoption Part it requires the C++ second-implementation
scrutiny gate (fresh cold pair at the 15M cap, anchors, tamper
battery) plus a third-implementation corroboration, then a fresh
single-owner adoption declaration (increment + merger + flip
census/reaudit with the shared-owner pre-exclusion caveat; owner
union k02 [16104, 16132, 16656, 20421]).  Class 20421 is NOT
complete (k03-k05 remain unknown).

## Claim status

Escalation bookkeeping only: NO verdict is claimed or consumed.
The standard 11x11 empty board: UNKNOWN.  All 19 central-reply
roots: UNKNOWN.  Two-stone root {60,27}: UNKNOWN.  Third-move
pair {100,108}: UNKNOWN.  Every closure class (including 20421)
stays UNKNOWN.  Nodes, expansions and wall_s are bookkeeping,
never verdicts.
