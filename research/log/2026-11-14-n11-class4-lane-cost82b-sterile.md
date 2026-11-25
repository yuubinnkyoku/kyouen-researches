# 2026-11-14 n11 class4-lane cost-82b sweep: sterile (18th observed)

Long-term lane session 11. The parallel class2-lane session 10 had the class-2 target's cost-74 child in flight, so this session took the cheapest unswept class-4 child: second child of the cost-82 band. S5 parent `00000000020000003800000080000000`, S6 child `00000000020000003800000090000000` (cost 82, demand c1=0,c2=0,c4=3).

## Sweep

- Candidates: 82 legal seventh moves via `legal_candidates.py` (Bareiss 4x4), bit-exact with the published edge cost 82 (after-cost73d CSV row).
- Engine: v15 verbatim (`class4_child1_runner.ts`), close-first AND at depth>=8, `--cap 1000000000`, depth 10 single-shot, 11 foreground batches of 8 bits.
- Pilot d6 control: `loss=false` at exactly 5,949 nodes in all 11 batch invocations.
- Result: **82 REFUTED-D10, 0 WIN7, 0 capped, 267,697,535 nodes**.
- Fresh-rerun control: heaviest candidates 54 (13,806,833), 7 (11,259,120), 2 (9,262,419) re-solved node-exactly in a separate process after the sweep.
- Terminal stone range: [13,17] on all 82 candidates.

## Interpretation

This child is WIN7-D10-sterile: no 7-stone root extending this S6 child admits a winner win within depth 10. Its c4=3 demand can therefore only be covered through certificates rooted in other S6 parents (cross-child reuse). The frontier is unchanged by a sterile sweep. This is the 18th sterile child observed in the class-2/class-4 lane campaigns.

REFUTED-D10 is only the negation of a winner win within depth 10 from the 7-stone root (loser to move). It is NOT a statement about deeper play, the S5/S6 orbits, the two-stone root {49,60}, S2 {59,60}, or the 11x11 empty board.

Raw batches: `../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class4-lane-cost82b-raw-batch1..11-20261114.jsonl`. Record: `class4-lane-cost82b-sweep-20261114.json`. Claim: `class4-lane-cost82b-inflight-20261114.json` (status updated to complete).

## Status

11x11 empty root, two-stone root {49,60}, S2 {59,60}, class 2, class 4: **UNKNOWN**.
