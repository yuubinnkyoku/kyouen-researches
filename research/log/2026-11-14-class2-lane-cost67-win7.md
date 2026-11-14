# 2026-11-14 class2-lane cost-67 sweep — 4 WIN7-D10 (bits 18, 34, 101, 118) + 63 REFUTED

## Target and child

Best class-2 blocker S5 after the merged frontier recompute (656920d7) is
`00000000000000809082000000000000` (classes=3, 21 remaining S6 orbits, cost 1471).
After the cost-66a/66b sterile sweeps (44b3a0a1), the cheapest unswept S6 child is
`00000000000000809082020000000000`, s6_s7_edge_cost = 67, demand c1=2,c2=2,c4=0.

## Sweep

- 67 legal candidates enumerated independently by `legal_candidates.py` (Bareiss 4x4);
  count bit-exact with the published s6_s7_edge_cost 67.
- Engine: `class4_child1_runner.ts` (v15 exact rules, close-first AND at depth >= 8,
  cap 1e9, per-candidate full engine reset), chunked 8+8 per invocation, pilot d6
  control 5,949 nodes (loss=false) in all 8 invocations.
- **Result: 4 WIN7-D10 (bits 18, 34, 101, 118) + 63 REFUTED-D10, 0 capped,
  total 286,673,913 nodes.** Terminal stone range [13,17] on every candidate.
- Heaviest candidates bits 26 / 12 / 18 (17.6M / 16.7M / 11.9M nodes) and all four
  WIN7 bits re-run fresh after the full sweep: node-exact identical.

## WIN7 certificates (all four fully verified)

Blind extraction (repo-verbatim `class4_child1_cert_extractor_exact.ts`,
FBS=1<<20, probe96, empty kill table; driver `cert_driver67.ts` imports
extractBatch and passes {} so every pref=null; rows sorted -u before write):

| bit | root | rows | extraction nodes | fbt_drops | sub-roots | loser mobility |
|-----|------|------|------------------|-----------|-----------|----------------|
| 18  | 00000000000000809082020000040000 | 59,084 | 18,160,725 | 0 | 60/60 PASS | 60 |
| 34  | 00000000000000809082020400000000 | 35,817 | 8,247,409 | 0 | 51/51 PASS | 51 |
| 101 | 00000020000000809082020000000000 | 33,754 | 9,652,919 | 0 | 46/46 PASS | 46 |
| 118 | 00400000000000809082020000000000 | 29,636 | 7,372,037 | 0 | 45/45 PASS | 45 |

Independent verification with `verify_bit7_win7_cert.ts` (engine-free, exact
integer Bareiss 4x4): root-check stones=7 and loserMobility equal the independent
`legal_candidates.py` enumeration on every root; every sub-root PASS; the union of
consumed winner states over all sub-roots equals the certificate row set exactly
(0 missing / 0 extra, both directions). Terminal stone ranges [13,17].

All four roots are new: none is present in any published certificate directory
(checked against every class2-lane/class4-lane certificates listing on main), so
no cross-child reuse applies (unlike cost-78b bit48).

The bit-18 certificate is 2,135,683 bytes and exceeds the single-run transport
limit; it is pushed as `.cert.part1of2` + `.cert.part2of2` with a README in the
same directory (recombine with cat; concatenation md5 f14be4a4ddda33502b56556bb249af81).

## Artifacts

- `output/class2-lane-cost67-sweep-20261114.json` (sweep record)
- `output/class2-lane-cost67-raw-batch1..8-20261114.jsonl` (per-candidate raw)
- `output/class2-lane-cost67-certificates/n11_s7_*.cert` (+ parts + README for bit 18)
- `output/class2-lane-cost67-win7-certificates-20261114.json` (certificate record)
- `scripts/cert_driver67.ts` (blind-extraction driver, imports repo extractor verbatim)

11x11 empty board, two-stone root {49,60}, S2 {59,60}, class 2 and class 4 all
remain UNKNOWN; each WIN7 certificate proves only that its 7-stone root is a
winner-side win within depth 10.
