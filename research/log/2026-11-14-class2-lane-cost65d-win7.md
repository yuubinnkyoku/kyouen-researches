# 2026-11-14 class2-lane cost-65d sweep — 1 WIN7-D10, certificate verified, frontier 881→884

## Target and child

Third cheapest unswept S6 child of the best class-2 blocker S5
`00000000000000809082000000000000` (after cost-65b sterile and cost-65c): S6 child
`00000000000000809082000010000000`, s6_s7_edge_cost = 65, demand c1=2,c2=2,c4=0.

## Sweep

- 65 legal candidates (`legal_candidates.py`, Bareiss 4x4), bit-exact with edge cost 65.
- Engine: `class4_child1_runner.ts` (v15 exact rules, close-first AND at d>=8, cap 1e9).
- Pilot d6 control 5,949 nodes in all 5 runner invocations.
- **Result: 1 WIN7-D10 (bit 103) + 64 REFUTED-D10, 0 capped, total 303,655,732 nodes.**
  Terminal range [13,17] everywhere. Heaviest bits 18 / 42 / 10 and the WIN7 bit
  re-run fresh after the sweep: node-exact identical.

## Certificate (fully verified, root new — no cross-child reuse)

Blind extraction (`class4_child1_cert_extractor_exact.ts`, FBS=1<<20, probe96, empty
kill table): fbt_drops = 0, fatal = null.

- root `00000080000000809082000010000000`, 36,916 rows, 11,294,025 extraction nodes,
  loser mobility 49, **49/49 sub-roots PASS**, consumed-union equality both
  directions (0/0), terminal range [13,17].
- Independent verification: `verify_bit7_win7_cert.ts` (engine-free, exact Bareiss 4x4).

## Frontier after cost-65d (recompute_frontier_cost65d.py)

Staged controls: after-cost78b (875/6972/548362/5212/409908) and after-cost65c
(881/6966/547927/5210/409767) reproduced exactly; sterile sweeps class4 cost-79/79b/80
and class2 cost-65b control-confirmed. cost-65d addition: 7 covers / 6 marginal /
**3 in-manifest** (including the swept child itself).

- **solved_s6_in_manifest 881 → 884**
- **unique_remaining_s6 6966 → 6963, sum 547927 → 547712**
- **open 5210/409767 → 5209/409691**
- best class-2 S5 `00000000000000809082000000000000`: **22 → 21 orbits, 1536 → 1471 cost**
- best class-4 unchanged (19/1540).

Re-run byte-identical; ranking + top-candidates CSVs regenerated (after-cost65d).

Note: one mid-sweep execution reset lost two local batches (36 candidates, all
REFUTED, no WIN7 among them in the lost portion); they were deterministically re-run
with node-exact identical results before the record was finalised, and every batch was
pushed to main immediately after completion this time.

## Artifacts

- `output/class2-lane-cost65d-sweep-20261114.json` + raw batches 1..5
- `output/class2-lane-cost65d-win7-certificates-20261114.json` +
  `output/class2-lane-cost65d-certificates/n11_s7_00000080000000809082000010000000.cert`
- `scripts/recompute_frontier_cost65d.py`,
  `output/class2-lane-cost65d-frontier-recompute-20261114.json`,
  `output/class-frontier-s5-ranking-after-cost65d.csv`,
  `output/class-frontier-top-candidates-s6-after-cost65d.csv`

11x11 empty board, two-stone root {49,60}, S2 {59,60}, class 2 and class 4 all
remain UNKNOWN (the WIN7 certificate proves a win within depth 10 from one
7-stone root only).
