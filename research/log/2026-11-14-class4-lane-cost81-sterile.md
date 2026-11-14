# 2026-11-14 class4-lane cost-81 sweep: 9th sterile child (81/81 REFUTED-D10)

## Context

Cheapest unswept S6 child of the best class-4 blocker-candidate S5
`00000000020000003800000080000000` after the cost-80 band was fully swept
(same session: cost-80 child 1 sterile, cost-80b child 2 with 1 WIN7 bit 50
certificate, cost-80c child 3 sterile; after-cost80b frontier 878 solved /
6969 unique remaining / 18 orbit / 1460).

## Sweep (child: `00000000020000003800000080008000`, c4=3)

Protocol identical to the whole cost-74..80c series: v15 engine verbatim,
per-candidate freshEngine, close-first AND at depth>=8, cap 1e9, depth 10
single-run, foreground batches 20+20+20+21 with per-batch JSONL durability.

- Enumeration: `legal_candidates.py` independently derives 81 legal candidates;
  matches the published edge cost 81.
- **Result: all 81 candidates REFUTED-D10. 0 WIN7, 0 capped, 325,836,995 nodes
  total, terminal [13,17].**
- Controls: pilot d6 4/4 at 5,949 nodes; heaviest bits 54/103/7
  (16,943,798 / 10,401,395 / 9,989,449 nodes) re-run fresh: node-exact identical.

Record: `output/class4-lane-cost81-sweep-20261114.json`,
raw batches `output/class4-lane-cost81-raw-batch{1..4}-20261114.jsonl`.

## Interpretation

9th sterile child; no frontier receipts, after-cost80b frontier unchanged.
Next cheapest unswept children of the class-4 target per the after-cost80b
top-candidates CSV: cost-82 `00000000020000003800000080000800` (c4=2) and
`00000000020000003800000090000000` (c4=3), then cost-84
`00000000020000003800000080000400` (c4=3).

## Guard

REFUTED-D10 is only the negation of a winner win within depth 10 from the
7-stone root (loser to move). No statement about deeper play, the S5/S6
orbits, the two-stone root {49,60}, S2 {59,60}, or the 11x11 empty board.
**11x11 remains UNKNOWN.**
