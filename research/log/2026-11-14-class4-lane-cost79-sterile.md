# 2026-11-14 class4-lane cost-79: sterile child (5th)

## Sweep

S6 `00000000020000003800000880000000` (cost-79, c1=0/c2=0/c4=2 demand), the
next cheapest unswept S6 child of the best class-4 blocker-candidate S5
`00000000020000003800000080000000` after cost-73/74a/74b/75/78/78b.

- **79/79 candidates REFUTED-D10, 0 WIN7, 0 capped** — **sterile child (5th)**.
  Frontier impact: none (its c4=2 demand must be covered through other roots'
  certificates).
- 270,231,378 nodes total. Foreground batches 16+16+16+17+14, per-batch raw
  pushed to main (`class4-lane-cost79-raw-batch1..5-20261114.jsonl`).
- Controls: pilot d6 5/5 = 5949; heaviest candidates 106/7/16 re-run fresh in a
  separate process, node-exact identical (13,194,282 / 9,773,998 / 9,752,125).
- Candidate enumeration: 79 legal moves re-derived independently by exact
  integer Bareiss (truelegal.py protocol; matches the published edge cost 79).
- Record: `output/class4-lane-cost79-sweep-20261114.json`.

Interpretation guard: REFUTED-D10 is only the negation of a winner win within
depth 10 from each 7-stone root (loser to move). **No statement about deeper
play, the S5/S6 orbits, the two-stone root {49,60}, S2 {59,60}, or the 11x11
empty board — all remain UNKNOWN.**

## Next

- Remaining cheapest unswept class-4 children per the after-cost63 ranking:
  cost-79 `00000000020000003800400080000000` (c4=3), then the cost-80 band
  (three children).
- Frontier recomputation over the new WIN7 covers (cost-74b 6 + cost-78 2 +
  cost-78b 1 new) is still pending; pull the latest frontier receipt set from
  main first.
