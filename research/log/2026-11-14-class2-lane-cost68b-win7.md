# 2026-11-14 class2-lane cost-68b sweep + WIN7 certificates + after-cost68b frontier recompute

## Sweep (S6 child 00000000000000809082000040000000, cost 68, c1=2,c2=2,c4=0)

Named cost-68b: class2-lane-cost68-* belongs to the old class-2 blocker's child
(00000000000000801a02000080000000); this child belongs to the current target
S5 00000000000000809082000000000000 and is its cheapest unswept child after the
after-cost67 recompute.

- 68 legal candidates (legal_candidates.py, Bareiss 4x4), bit-exact with the edge cost.
- **Result: 2 WIN7-D10 (bits 23, 118) + 66 REFUTED-D10, 0 capped, 323,716,265 nodes**;
  terminal range [13,17] everywhere; pilot d6 5,949 nodes in all 8 invocations.
- An execution-environment reset occurred after batch 4; the deterministic rerun
  reproduced every earlier batch node-exact (bit23: 5,693,395 nodes identical
  pre/post reset) — a further cross-restart reproducibility datapoint.
- Heaviest bits 18/112/33 (16.5M/12.6M/12.5M) and both WIN7 bits re-run fresh:
  node-exact identical.

## WIN7 certificates (both fully verified)

Blind extraction (repo-verbatim extractor_exact, FBS=1<<20, probe96, empty kill
table via cert_driver67.ts; rows sorted -u):

| bit | root | rows | extraction nodes | fbt_drops | sub-roots | loser mobility |
|-----|------|------|------------------|-----------|-----------|----------------|
| 23  | 00000000000000809082000040800000 | 30,623 | 8,447,296 | 0 | 49/49 PASS | 49 |
| 118 | 00400000000000809082000040000000 | 33,285 | 11,292,258 | 0 | 52/52 PASS | 52 |

Independent verification (verify_bit7_win7_cert.ts, engine-free Bareiss 4x4):
root-check loserMobility = independent enumeration; all sub-roots PASS; union of
consumed winner states = certificate row set exactly (0/0 both directions).
Both roots are absent from all 149 roots in published WIN7 records on main
(no cross-child reuse).

## Frontier after cost-68b (recompute_frontier_cost68b_20261114.py)

Direct extension of the after-cost67 script: all staged controls reproduce the
published frontiers exactly (asserted, including after-cost67 898/6949/546687/5202/409163),
then the cost-68b receipt (2 WIN7) is added. Two runs byte-identical.

- solved_s6_in_manifest: **903** (898 + 5 in-manifest marginals)
- unique_remaining_s6: **6,944** / sum_remaining_cost: **546,334**
- open: **5,201 / 409,091**
- cost-68b addition: 13 covers / 11 marginal / 5 in-manifest
- best class-2 S5 00000000000000809082000000000000: **18 -> 16 orbits, cost 1,260 -> 1,123**
- best class-4 (18/1,460) unchanged

## Artifacts

- `output/class2-lane-cost68b-sweep-20261114.json` + raw batch1..8
- `output/class2-lane-cost68b-certificates/n11_s7_*.cert` (2)
- `output/class2-lane-cost68b-win7-certificates-20261114.json`
- `scripts/recompute_frontier_cost68b_20261114.py`
- `output/class-frontier-cost68b-recompute-20261114.json`, ranking + top-candidates CSVs

11x11 empty board, two-stone root {49,60}, S2 {59,60}, class 2 and class 4 all
remain UNKNOWN.
