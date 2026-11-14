# 2026-11-14 class4-lane cost-79b (second cost-79 child): sterile (6th)

## Sweep

S6 `00000000020000003800400080000000` (cost-79, c1=0/c2=0/c4=3), the second
cost-79 S6 child of the best class-4 blocker-candidate S5
`00000000020000003800000080000000` (the first cost-79 child was swept sterile
the same day).

- **79/79 candidates REFUTED-D10, 0 WIN7, 0 capped** — **sterile child (6th**;
  both cost-79 children are sterile**)**. Frontier impact: none.
- 223,708,504 nodes total. Foreground batches 16+16+16+17+14, per-batch raw
  pushed to main (`class4-lane-cost79b-raw-batch1..5-20261114.jsonl`).
- Controls: pilot d6 5/5 = 5949; heaviest candidates 54/86/112 re-run fresh in
  a separate process, node-exact identical
  (10,957,509 / 8,543,804 / 8,510,688).
- Candidate enumeration: 79 legal moves re-derived independently by exact
  integer Bareiss (truelegal.py protocol; matches the published edge cost 79).
- Record: `output/class4-lane-cost79b-sweep-20261114.json`.

Interpretation guard: REFUTED-D10 is only the negation of a winner win within
depth 10 from each 7-stone root (loser to move). **No statement about deeper
play, the S5/S6 orbits, the two-stone root {49,60}, S2 {59,60}, or the 11x11
empty board — all remain UNKNOWN.**

## Next

- Cost-79 band is fully swept (both children sterile). Next cheapest unswept
  class-4 children: the cost-80 band
  (`00000000020000003800000180000000` c4=2,
  `00000000020000003800040080000000` c4=3,
  `00000000020000003800200080000000` c4=1).
- Frontier recomputation over the new WIN7 covers (cost-74b 6 + cost-78 2 +
  cost-78b 1 new; the sterile children leave the frontier unchanged) is still
  pending; pull the latest frontier receipt set from main first.
