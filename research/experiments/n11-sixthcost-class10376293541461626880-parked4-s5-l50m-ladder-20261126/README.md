# n11-sixthcost-class10376293541461626880-parked4-s5-l50m-ladder-20261126 (checkpoint state: HALTED ON WIN at both started keys k13/k19 after full pre-registered stages; k20/k33 never started; verdicts NOT consumed)

Sixth-cost class `10376293541461626880:65536` (coverage {80, 84, 100, 108})
parked-4-keys S5 L50M ladder, the budget-raising continuation lane for the four
exclusive single-live-parent keys the fifth-resumption parent batch parked at
UNKNOWN@15M (k13 `1152921573327376384:536870912`, k19
`10376293541461626880:65664`, k20 `10376293541461626880:33619968`, k33
`12682136550675320832:65536`). Declared single-owner in
`research/log/2026-11-26-n11-sixthcost-class10376293541461626880-parked4-s5-l50m-ladder-single-owner.md`
(commit `9e042a5f`), protocol identical to the third-cost parked2 L50M precedent
(`research/experiments/n11-class1297036830122704896-parked2-s5-l50m-ladder-20261121/`).

## Method

- Budget raise 15,000,000 -> 50,000,000 on the identical exact-replay protocol:
  Node.js replica `jsreplay.js` (sha256
  `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`,
  published byte-clone in this kit), exact replay mode (order=count-asc,
  share_tt=0, fresh 2^22-entry PnTT per row, cold per-row solver), run TWICE per
  key with independent fresh solvers; identical (result, nodes) required; one
  budget-margin re-proof at 32,000,000 per resolved key; a voluntary third cold
  50,000,000 verification run for every WIN key (honestly labeled beyond the
  declared pair, the k02/k03/k04/k05/k08 precedent). Two keys processed
  concurrently (2 worker processes max on this 2-core host), per-key stages
  serial. wall_s is environment-dependent and never a verdict.
- Fresh-session gates before any ladder row was trusted: the four published
  two-target validation rows reproduce node-exact on this host (at2m x2:
  result 0 / nodes 2,000,000 / legal 98, 99; 15M rows: result 2 / nodes
  3,651,923 and 5,040,200 / legal 98, 99; this host wall_s 9/9/17/25 s), and
  per-key fresh 15M baseline runs must reproduce the parent batch's published
  parked baseline exactly (result 0, nodes 15,000,000). Both gates PASSed for
  both started keys BEFORE their 50M stages.
- NO merged cache increment is published by this lane under ANY outcome
  (declared no-consumption rule): the sixth-cost parent batch's own consumption
  gate reserves any increment for its full batch audit under the WIN/LOSS
  conflict policy. This lane records raw evidence and a fail-closed machine
  audit only.

## Results (machine-checked by scripts/audit_parked4_l50m.py halt branch; raws under output/raw/)

- Both started keys resolved **WIN(1)** inside the 50M budget, and the lane
  halted under stopping rule 1 exactly as declared: no further claimed-key
  STARTS. The first observed WIN was k19's l50m-run1 (both keys' base15m
  baselines had already started at 07:38:31Z, before any 50M result existed, so
  both started keys legitimately completed their full pre-registered stages
  base15m -> 50M pair -> 32M margin -> voluntary 50M run3-verify; k20 and k33
  were never started and remain parked@15M, claimable by a later lane.
- **k13 `1152921573327376384:536870912` (legal 95): WIN(1) in nodes 16,402,480**
  - identical on both independent cold 50M runs (`l50m-run1-*`, `l50m-run2-*`)
    AND on the 32M budget-margin re-proof (`l50m-margin-*`) AND on the
    voluntary third cold 50M verification run (`l50m-run3-verify-*`). The 15M
    park is explained: the proof needs ~1.09x the 15M budget.
- **k19 `10376293541461626880:65664` (legal 95): WIN(1) in nodes 15,379,062**
  - identical on both independent cold 50M runs AND on the 32M margin re-proof
    AND on the voluntary third cold 50M verification run. The 15M park is
    explained: the proof completes at ~1.025x the 15M budget.
- Determinism: every executed stage of every started key returned identical
  (result, nodes) across all its runs.
- Per the pre-registered stopping rules this lane consumes NO verdict, publishes
  NO cache row, makes NO class/root/board claim, and hands both WIN raws to
  scrutiny owners for the mandatory second-implementation re-verification
  (pinned C++ `cpp/solvers/kyouen_dfpn_root.cpp` sha256 `9193f5b6...`; no C++
  toolchain exists in this lane's sandbox, re-verified). The parent batch's
  other unconsumed rows (k01 LOSS, k02-k05/k08 WIN, k06/k07 LOSS, the
  fifth-resumption k09..k43 rows) are untouched by this lane.
- If-adopted scenario (recorded NOT-ADOPTED in `output/halt-audit.json`,
  computed on the frozen 3,384-class geometry over the chain head of record
  `6e49dd84`): adopting both WIN raws would move the sixth-cost class
  `10376293541461626880:65536` to hypothetical status WIN with unknown children
  100 -> 98 (0 WIN -> 2 WIN of 108; 58 shared unknown children remain outside
  this batch's claim in any case); the recorded global status changes under the
  hypothetical are enumerated in the halt-audit and NOT adopted. The root
  impact through the depth-2/depth-1 chain is NOT computed by this lane and
  belongs to the K0414/K0416-lineage owners.
- Honest environment disclosure: the first launch of the two voluntary run3
  verify runs was killed with the launching shell process when the launch
  command returned (truncated LOCAL header-only files, never published); the
  verify runs were re-executed fresh and cleanly to completion with the
  ladder-proven nohup launch pattern, and the published artifacts are those
  clean runs. The declared determinism pair and margin had already completed
  before the incident; no raw row was affected.

## Status guard

Scheduling and raw evidence only. The standard 11x11 empty board remains
UNKNOWN. The two-stone root {60,27} and its remaining third moves 100/108
remain UNKNOWN. Nodes, budgets, proxy values and solved counts are never
verdicts. These raw rows are solver-trusted evidence pending second-implementation
scrutiny; the sixth-cost class stays as the canonical chain has it (0 WIN /
8 LOSS / 100 UNKNOWN children on the head of record `6e49dd84`), an S5 WIN raw
is not a class-closure claim and not a route to the root certificate.
