# 2026-11-14 class4-lane cost-80c sweep: 8th sterile child (80/80 REFUTED-D10), cost-80 band fully swept

## Context

Third and final cost-80 S6 child of the best class-4 blocker-candidate S5
`00000000020000003800000080000000` (after-cost80b frontier: 18 orbit / cost 1460).
Same session as the cost-80 (child 1, sterile) and cost-80b (child 2,
1 WIN7 bit 50 with verified certificate) sweeps. An environment reset wiped the
local workspace between the cost-80b frontier push and this sweep; all tools
were re-fetched from main (commit-pinned raw) and the pilot control passes.

## Sweep (child: `00000000020000003800200080000000`, c4=1)

Protocol identical to cost-74a/b/75/78/78b/79/79b/80/80b: v15 engine verbatim,
per-candidate freshEngine, close-first AND at depth>=8, cap 1e9, depth 10
single-run, foreground batches 20+20+20+20 with per-batch JSONL durability.

- Enumeration: `legal_candidates.py` independently derives 80 legal candidates;
  matches the published edge cost 80.
- **Result: all 80 candidates REFUTED-D10. 0 WIN7, 0 capped, 220,291,094 nodes
  total, terminal [13,17].**
- Controls: pilot d6 4/4 at 5,949 nodes; heaviest bits 0/84/10
  (14,869,940 / 10,686,991 / 9,277,776 nodes) re-run fresh: node-exact identical.

Record: `output/class4-lane-cost80c-sweep-20261114.json` (md5 8bf38522391f1646e4f86d8e6ae6ac92),
raw batches `output/class4-lane-cost80c-raw-batch{1..4}-20261114.jsonl` (20 bits each).

## Interpretation

8th sterile child. No frontier receipts, so the after-cost80b frontier
(878 solved / 6969 unique remaining / sum 548122 / open 5209 / 409668) is
unchanged. **The cost-80 band of the class-4 target is now fully swept**:
child 1 sterile, child 2 closed for its covered orbits by the verified bit 50
certificate, child 3 sterile. The next cheapest unswept child of the class-4
target per the after-cost80b top-candidates CSV is cost-81
`00000000020000003800000080008000` (c4=3), then cost-82
`00000000020000003800000080000800` (c4=2) / `00000000020000003800000090000000` (c4=3).

## Guard

REFUTED-D10 is only the negation of a winner win within depth 10 from the
7-stone root (loser to move). No statement about deeper play, the S5/S6
orbits, the two-stone root {49,60}, S2 {59,60}, or the 11x11 empty board.
**11x11 remains UNKNOWN.**
