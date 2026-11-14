# 2026-11-14 class2-lane cost-69a sweep — 3 WIN7-D10 (bits 48, 70, 103) + 66 REFUTED

## Target and child

Cheapest unswept S6 child of the class-2 target S5 00000000000000809082000000000000
after the after-cost68b recompute: `00000000000000809082000000000400`,
s6_s7_edge_cost = 69, demand c1=2,c2=2,c4=0.

## Sweep

- 69 legal candidates (legal_candidates.py, Bareiss 4x4), bit-exact with the edge cost.
- **Result: 3 WIN7-D10 (bits 48, 70, 103) + 66 REFUTED-D10, 0 capped, 360,149,635 nodes**;
  terminal range [13,17] everywhere; pilot d6 5,949 nodes in all 8 invocations.
- Heaviest bits 68/53/117 (16.8M/12.6M/12.2M) and all three WIN7 bits re-run fresh:
  node-exact identical.

## WIN7 certificates (all three fully verified)

Blind extraction (repo-verbatim extractor_exact, FBS=1<<20, probe96, empty kill
table via cert_driver67.ts; rows sorted -u):

| bit | root | rows | extraction nodes | fbt_drops | sub-roots | loser mobility |
|-----|------|------|------------------|-----------|-----------|----------------|
| 48  | 00000000000000809083000000000400 | 42,596 | 13,368,996 | 0 | 54/54 PASS | 54 |
| 70  | 00000000000000c09082000000000400 | 36,472 | 10,623,218 | 0 | 51/51 PASS | 51 |
| 103 | 00000080000000809082000000000400 | 29,047 | 8,466,041 | 0 | 48/48 PASS | 48 |

Independent verification (verify_bit7_win7_cert.ts, engine-free Bareiss 4x4):
root-check loserMobility = independent enumeration; all sub-roots PASS; union of
consumed winner states = certificate row set exactly (0/0 both directions).
All three roots are absent from all 149 roots in published WIN7 records
(no cross-child reuse).

The bit-48 certificate (1,542,354 bytes) exceeds the single-run transport limit
and is pushed as `.cert.part1of2` + `.cert.part2of2` (recombine with cat;
concatenation md5 24997fa018e2c89cbcd65b3a006c8183, sha256
aaf8ccc8aa119c7490497e14561c0d956a5c41766f8fd228992b473e1cb43160).

## Artifacts

- `output/class2-lane-cost69a-sweep-20261114.json` + raw batch1..8
- `output/class2-lane-cost69a-certificates/n11_s7_*.cert` (+ parts for bit 48)
- `output/class2-lane-cost69a-win7-certificates-20261114.json`

11x11 empty board, two-stone root {49,60}, S2 {59,60}, class 2 and class 4 all
remain UNKNOWN; each WIN7 certificate proves only that its 7-stone root is a
winner-side win within depth 10.
