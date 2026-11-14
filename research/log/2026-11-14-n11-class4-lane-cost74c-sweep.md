# 2026-11-14 n11 class4-lane cost-74c sweep: sterile (74 REFUTED-D10)

Long-term lane session 9 continuation, after the cost-73d WIN7 and the frontier recompute (solved 920 / remaining 6,927). Best class-4 blocker-candidate S5 `00000000020000003800000080000000` (remaining 18 orbits, cost 1,460). S6 child `00000000020000003800000088000000` (cost 74, demand c1=0,c2=1,c4=2), the next cheapest unswept S6 child after the sterile cost-73 / 74a / 75 / 79 / 79b / 80 / 80c / 81 / 82a sweeps and the WIN7-solved 74b / 78 / 78b / 80b children.

## Sweep

- Claim pushed before the run: `class4-lane-cost74c-inflight-20261114.json` (74 candidate bits from `legal_candidates.py`, bit-exact with the published edge cost 74).
- Engine: v15 verbatim (`class4_child1_runner.ts`), close-first AND (depth>=8), `--cap 1000000000`, depth 10 single-shot, 11 batches (batches 1-10 as two parallel workers, batch 11 single-process).
- Pilot d6 control: `loss=false` at exactly 5,949 nodes in all 21 invocations.
- Result: **74 REFUTED-D10, 0 WIN7-D10, 0 capped, 250,407,651 nodes** — sterile child (18th sterile child on this lane).
- Fresh-rerun control: heaviest bits 116 (14,575,690), 88 (12,807,343), 4 (10,148,083) re-solved node-exactly in a separate single-process run after the sweep.
- Terminal stone range: [13,17] on all 74 candidates.

## Interpretation

No depth<=10 winner win exists from any of the 74 7-stone roots of this child. The child's c2=1/c4=2 demand can therefore only be covered through other roots' certificates. This is a bookkeeping fact about one S6 child; it does not decide the S5 parent orbit, any larger root, or the class-4 lane. Remaining unswept children of this S5 after cost-74c: cost-82b (`...90000000`), cost-84 (`...80000400`), cost-86 (5 children), cost-87 (`...80000004`) per the after-cost73d top-candidates CSV.

Raw batches: `../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class4-lane-cost74c-raw-batch1..11-20261114.jsonl` + `class4-lane-cost74c-determinism-rerun-20261114.jsonl`. Record: `class4-lane-cost74c-sweep-20261114.json`.

## Status

11x11 empty root, two-stone root {49,60}, S2 {59,60}, class 2, class 4: **UNKNOWN**.
