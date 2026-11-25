# 2026-11-14 n11 class2-lane cost-73d sweep: 1 WIN7-D10 (bit 48), certificate verified

Long-term lane session 9, after the sterile cost-73b and cost-73c sweeps. S5 parent `00000000000000809082000000000000`, S6 child `00000000000000809082000000004000` (cost 73, demand c1=2,c2=2,c4=0).

## Sweep

- Candidates: 73 legal seventh moves via `legal_candidates.py` (Bareiss 4x4), bit-exact with the published edge cost.
- Engine: v15 verbatim, close-first AND, `--cap 1000000000`, depth 10 single-shot, 11 batches, 2 workers.
- Pilot d6 control: `loss=false` at exactly 5,949 nodes in all 11 invocations.
- Result: **1 WIN7-D10 (bit 48) + 72 REFUTED-D10, 0 capped, 425,731,649 nodes**.
- Fresh-rerun control: bits 100 (24,766,290), 1 (18,482,571), and the WIN7 bit 48 (17,214,413) re-solved node-exactly after the sweep.
- Cross-restart reproduction: an environment reset wiped the local workspace after batch 6; the deterministic rerun reproduced batches 1-6 node-exactly (including WIN7 bit 48) and the sweep was completed from there.
- Terminal stone range: [13,17] on all 73 candidates.

## WIN7 certificate (root `00000000000000809083000000004000`)

- Extraction: repo-verbatim `class4_child1_cert_extractor_exact.ts`, blind (empty kill table), single batch over all 59 loser first-moves; 66,680 rows; extraction 25,261,945 nodes; fbt_drops=0; fatal=null.
- Verification: `verify_bit7_win7_cert.ts` root-check PASS (7 stones, loserMobility 59 = independent enumeration); **59/59 sub-roots PASS**; **union of consumed winner states equals the full row set exactly (0 missing / 0 extra)**; per-sub-root terminal ranges within [13,17].
- The root hex `00000000000000809083000000004000` is not present in any of the 21 published win7-certificates records on main (class2-lane cost-58 through cost-75 and class4-lane cost-74b/78/78b/80b checked by grep at push time): no cross-child reuse, a new distinct WIN7 root.

## Interpretation

The 7-stone root `00000000000000809083000000004000` is a WIN for the original first player within depth 10. This certifies the parent S6 `00000000000000809082000000004000` as covered (player to move loses), for the frontier accounting. It does not decide the S5 parent orbit or any larger root.

Raw batches: `../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost73d-raw-batch1..11-20261114.jsonl`. Record: `class2-lane-cost73d-sweep-20261114.json`. Certificate parts: `class2-lane-cost73d-certificates/`.

## Status

11x11 empty root, two-stone root {49,60}, S2 {59,60}, class 2, class 4: **UNKNOWN**.
