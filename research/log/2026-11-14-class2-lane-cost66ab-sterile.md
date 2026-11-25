# 2026-11-14 class2-lane cost-66a + cost-66b sweeps — 11th and 12th sterile children (all REFUTED-D10)

## Target and children

Best class-2 blocker S5 after the merged frontier recompute (656920d7) is
`00000000000000809082000000000000` (classes=3, 21 remaining S6 orbits, cost 1471).
The two cheapest unswept S6 children were the cost-66 pair, both demand c1=2,c2=2,c4=0:
`00000000000000809082000004000000` (66a) and `00000000000000809082000020000000` (66b).

## Sweep (both children)

- 66 legal candidates each, enumerated independently by `legal_candidates.py`
  (Bareiss 4x4); count bit-exact with the published s6_s7_edge_cost 66.
- Engine: `class4_child1_runner.ts` (v15 exact rules, close-first AND ordering at
  depth >= 8, cap 1e9, per-candidate full engine reset), chunked 8+8 per invocation,
  pilot d6 control 5,949 nodes (loss=false) in all 8 invocations per child.
- **cost-66a: 66 REFUTED-D10, 0 WIN7-D10, 0 capped, total 381,822,266 nodes.**
- **cost-66b: 66 REFUTED-D10, 0 WIN7-D10, 0 capped, total 347,082,667 nodes.**
  Terminal stone range [13,17] on every candidate of both sweeps.
- Heaviest candidates re-run fresh after each full sweep, node-exact identical:
  66a bits 41 / 18 / 114 (17.6M / 15.5M / 15.3M), 66b bits 88 / 67 / 42
  (15.2M / 14.9M / 14.4M).

## Interpretation

Both children are **sterile** (11th and 12th overall; for this class-2 target the
2nd and 3rd after cost-65b): no depth-10 WIN7 exists from any 7-stone root of
either child, so neither contributes WIN7 certificates and both must be covered
through other S6 parents' certificates. Frontier numbers are unchanged (no
receipts added); the cost-66 band of this target is now fully swept and the
cheapest unswept child moves to cost-67 `00000000000000809082020000000000`.

## Artifacts

- `output/class2-lane-cost66a-sweep-20261114.json`, `output/class2-lane-cost66b-sweep-20261114.json`
- `output/class2-lane-cost66a-raw-batch1..8-20261114.jsonl`
- `output/class2-lane-cost66b-raw-batch1..8-20261114.jsonl`

11x11 empty board, two-stone root {49,60}, S2 {59,60}, class 2 and class 4 all
remain UNKNOWN.
