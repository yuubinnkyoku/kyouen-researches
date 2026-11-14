# 2026-11-14 n11 class2-lane cost-73b sweep: sterile

Long-term lane session 9. S5 parent `00000000000000809082000000000000`, S6 child `00000000000000809082000000000040` (cost 73, demand c1=2,c2=2,c4=0), the next-cheapest un-swept class-2 child after the after-cost71 frontier recompute. cost-73a (`...82000000000010`) is claimed in flight by the parallel lane and was not touched.

## Sweep

- Candidates: 73 legal seventh moves, independently enumerated with `legal_candidates.py` (Bareiss 4x4), bit-exact with the published edge cost.
- Engine: v15 verbatim (`class4_child1_runner.ts`), close-first AND, `--cap 1000000000`, depth 10 single-shot, 11 batches of <=7 candidates, 2 workers on the 2-core host.
- Pilot d6 control: `loss=false` at exactly 5,949 nodes in all 11 invocations.
- Result: **73 REFUTED-D10, 0 WIN7-D10, 0 capped, 376,649,033 nodes** — **sterile** (15th sterile child overall, first in the cost-73 band).
- Fresh-rerun control: heaviest bits 53 (20,428,367), 18 (19,812,446), 12 (12,332,047) re-solved node-exactly in a separate process after the sweep.
- Terminal stone range: [13,17] on all candidates except bit 19 ([15,17]).

## Interpretation

Sterile means no seventh move from this child gives a winner win within depth 10. It does not decide the child and does not change the frontier counts (no new WIN7 cover). The child stays open in the worklist.

Raw batches: `../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost73b-raw-batch1..11-20261114.jsonl`. Record: `class2-lane-cost73b-sweep-20261114.json`. Transport note: raw batches 1-5 were first pushed as a reconstruction that omitted `ms`/`andclose` and normalized bit 19's terminal range to [13,17]; batches 2-5 were re-pushed verbatim in the immediately following commit (batch1 was already verbatim). Use the second version of batches 2-5.

## Status

11x11 empty root, two-stone root {49,60}, S2 {59,60}, class 2, class 4: **UNKNOWN**.
