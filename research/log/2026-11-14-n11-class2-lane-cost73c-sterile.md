# 2026-11-14 n11 class2-lane cost-73c sweep: sterile

Long-term lane session 9, continuing directly after the cost-73b sterile sweep. S5 parent `00000000000000809082000000000000`, S6 child `00000000000000809082000000000080` (cost 73, demand c1=2,c2=2,c4=0).

## Sweep

- Candidates: 73 legal seventh moves via `legal_candidates.py` (Bareiss 4x4), bit-exact with the published edge cost.
- Engine: v15 verbatim, close-first AND, `--cap 1000000000`, depth 10 single-shot, 11 batches, 2 workers.
- Pilot d6 control: `loss=false` at exactly 5,949 nodes in all 11 invocations (identical control lines).
- Result: **73 REFUTED-D10, 0 WIN7-D10, 0 capped, 388,889,991 nodes** — **sterile** (16th sterile child overall, second in the cost-73 band).
- Fresh-rerun control: bits 120 (26,150,087), 32 (19,876,385), 67 (14,451,598) re-solved node-exactly after the sweep.
- Terminal stone range: [13,17] on all 73 candidates.

## Interpretation

No seventh move from this child gives a winner win within depth 10; the child is not decided and the frontier counts are unchanged. The child stays open in the worklist.

Raw batches: `../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost73c-raw-batch1..11-20261114.jsonl`. Record: `class2-lane-cost73c-sweep-20261114.json`.

## Status

11x11 empty root, two-stone root {49,60}, S2 {59,60}, class 2, class 4: **UNKNOWN**.
