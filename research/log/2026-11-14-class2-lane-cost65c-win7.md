# 2026-11-14 class2-lane cost-65c sweep — 3 WIN7-D10, certificates verified, frontier 875→881

## Target and child

Second cheapest unswept S6 child of the best class-2 blocker S5
`00000000000000809082000000000000` (after cost-65b): S6 child
`00000000000000809082000000200000`, s6_s7_edge_cost = 65, demand c1=2,c2=2,c4=0.

## Sweep

- 65 legal candidates (`legal_candidates.py`, Bareiss 4x4), bit-exact with edge cost 65.
- Engine: `class4_child1_runner.ts` (v15 exact rules, close-first AND at d>=8, cap 1e9).
- Pilot d6 control 5,949 nodes in all 5 runner invocations.
- **Result: 3 WIN7-D10 (bits 9, 48, 70) + 62 REFUTED-D10, 0 capped,
  total 221,652,686 nodes.** Terminal range [13,17] everywhere.
- Heaviest bits 6 / 116 / 75 and all three WIN7 bits re-run fresh after the sweep:
  node-exact identical.

## Certificates (all three fully verified, all roots new — no cross-child reuse)

Blind extraction with `class4_child1_cert_extractor_exact.ts` (FBS=1<<20, probe96,
empty kill table): fbt_drops = 0, fatal = null on every batch.

| bit | root | rows | extraction nodes | loser mobility | sub-roots | union missing/extra |
|-----|------|------|------------------|----------------|-----------|---------------------|
| 9  | 00000000000000809082000000200200 | 38,363 | 6,339,815  | 57 | 57/57 PASS | 0/0 |
| 48 | 00000000000000809083000000200000 | 36,237 | 10,365,300 | 49 | 49/49 PASS | 0/0 |
| 70 | 00000000000000c09082000000200000 | 31,979 | 6,987,638  | 52 | 52/52 PASS | 0/0 |

Independent verification: `verify_bit7_win7_cert.ts` (engine-free, exact Bareiss 4x4),
root-check (7 stones, no 4 concyclic, loser mobility = independent enumeration) plus
every loser first-move sub-root; the consumed winner-state union equals the row set
exactly in both directions. Terminal range [13,17] on all sub-roots.

## Sterile-count note

The parallel class4 lane completed the cost-80 band (cost-80c sterile) around the
same time as this session's cost-65b; together with class4 cost-73/74a/75/79/79b/80
and class2 cost-65b the sterile-child count is now 9 (the cost-65b log's "8th" and
the cost-80c log's "8th" were written concurrently against the same prior set of 7).

## Frontier after cost-65c (recompute_frontier_cost65c.py)

Staged control: after-cost78b (875 / 6972 / 548362 / 5212 / 409908) reproduced exactly;
sterile sweeps class4 cost-79, cost-79b, cost-80 and class2 cost-65b control-confirmed
(0 WIN7, 0 capped each). cost-65c addition: 18 covers / 15 marginal / **6 in-manifest**
(including the swept child itself).

- **solved_s6_in_manifest 875 → 881**
- **unique_remaining_s6 6972 → 6966, sum 548362 → 547927**
- **open 5212/409908 → 5210/409767**
- best class-2 S5 `00000000000000809082000000000000`: **23 → 22 orbits, 1601 → 1536 cost**
- best class-4 unchanged (19/1540).

Re-run byte-identical; ranking + top-candidates CSVs regenerated (after-cost65c).

## Artifacts

- `output/class2-lane-cost65c-sweep-20261114.json` + raw batches 1..5
- `output/class2-lane-cost65c-win7-certificates-20261114.json` +
  `output/class2-lane-cost65c-certificates/n11_s7_*.cert` (3 files)
- `scripts/recompute_frontier_cost65c.py`,
  `output/class2-lane-cost65c-frontier-recompute-20261114.json`,
  `output/class-frontier-s5-ranking-after-cost65c.csv`,
  `output/class-frontier-top-candidates-s6-after-cost65c.csv`

11x11 empty board, two-stone root {49,60}, S2 {59,60}, class 2 and class 4 all
remain UNKNOWN (each WIN7 certificate proves a win within depth 10 from one
7-stone root only).
