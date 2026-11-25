# 2026-11-14 class2-lane cost-65b sweep — 8th sterile child (all 65 REFUTED-D10)

## Target and child

Best class-2 blocker S5 after the cost-78b frontier recompute is
`00000000000000809082000000000000` (classes=3, 23 remaining S6 orbits, cost 1601).
Cheapest unswept S6 child (from the after-cost78b incidences, cross-checked against
every published sweep record on main): `00000000000000809082000000020000`,
s6_s7_edge_cost = 65, demand c1=1,c2=2,c4=0.

## Sweep

- 65 legal candidates enumerated independently by `legal_candidates.py` (Bareiss 4x4);
  count bit-exact with the published s6_s7_edge_cost 65.
- Engine: `class4_child1_runner.ts` (v15 exact rules, close-first AND ordering at
  depth >= 8, cap 1e9, per-candidate full engine reset).
- Pilot d6 control 5,949 nodes (loss=false) in all 6 runner invocations.
- **Result: 65 REFUTED-D10, 0 WIN7-D10, 0 capped, total 245,459,068 nodes.**
  Terminal stone range [13,17] on every candidate.
- Heaviest candidates bits 103 / 101 / 98 (11.6M / 10.3M / 9.0M nodes) re-run fresh
  after the full sweep: node-exact identical (245,459,068 total reproduced).

## Interpretation

**Sterile child** (8th overall, first for this class-2 target): no depth-10 WIN7
exists from any 7-stone root of this child, so it contributes no WIN7 certificates.
Its orbit must be covered through other S6 parents' certificates. Frontier numbers
are unchanged (no receipts added); this sweep removes the child from the candidate
pool for certificate-based closure.

## Artifacts

- `output/class2-lane-cost65b-sweep-20261114.json` (sweep record)
- `output/class2-lane-cost65b-raw-batch1..6-20261114.jsonl` (per-candidate raw)

Naming note: `class2-lane-cost65-*` was already taken by the old class-2 blocker's
child, so this child is recorded as cost-65b.

11x11 empty board, two-stone root {49,60}, S2 {59,60}, class 2 and class 4 all
remain UNKNOWN.
