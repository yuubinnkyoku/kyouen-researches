# 2026-11-14 n11 class4-lane cost-86c sweep: sterile (21st observed)

Long-term lane session 11, continued. Third child of the cost-86 band. S5 parent `00000000020000003800000080000000`, S6 child `00000000020000003800000280000000` (cost 86, demand c1=0,c2=0,c4=3).

## Sweep

- Candidates: 86 legal seventh moves via `legal_candidates.py` (Bareiss 4x4), bit-exact with the published edge cost 86.
- Engine: v15 verbatim (`class4_child1_runner.ts`), close-first AND at depth>=8, `--cap 1000000000`, depth 10 single-shot, 15 foreground batches (7 then 6 bits).
- Pilot d6 control: `loss=false` at exactly 5,949 nodes in all 15 batch invocations.
- Result: **86 REFUTED-D10, 0 WIN7, 0 capped, 301,085,672 nodes**.
- Fresh-rerun control: heaviest candidates 112 (17,148,495), 82 (13,985,873), 113 (11,132,780) re-solved node-exactly in a separate process after the sweep.
- Cross-restart reproduction: an environment reset wiped the local workspace after batch 7; the deterministic re-run reproduced batch 7 node-exactly (4,919,936/5,558,579/5,244,191/2,558,561/2,556,893/1,196,390) and the sweep continued from there.
- Terminal stone range: [13,17] on all 86 candidates.

## Interpretation

This child is WIN7-D10-sterile: no 7-stone root extending this S6 child admits a winner win within depth 10. Its c4=3 demand can therefore only be covered through certificates rooted in other S6 parents (cross-child reuse). The frontier is unchanged by a sterile sweep. This is the 21st sterile child observed in the class-2/class-4 lane campaigns; the cost-86 band has 2 children left (`00000000020000003800100080000000`, `00000000020000003840000080000000`), plus cost-84 (parallel lane, in flight) and cost-87 `00000000020000003800000080000004`.

REFUTED-D10 is only the negation of a winner win within depth 10 from the 7-stone root (loser to move). It is NOT a statement about deeper play, the S5/S6 orbits, the two-stone root {49,60}, S2 {59,60}, or the 11x11 empty board.

Raw batches: `../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class4-lane-cost86c-raw-batch1..15-20261114.jsonl`. Record: `class4-lane-cost86c-sweep-20261114.json`. Claim: `class4-lane-cost86c-inflight-20261114.json` (status updated to complete).

## Status

11x11 empty root, two-stone root {49,60}, S2 {59,60}, class 2, class 4: **UNKNOWN**.
