# class2-lane: cost-75e/60c fold row-level bookkeeping verification, chain completion (2026-11-16)

## What was done

- Independent third implementation re-verification of the two remaining fold steps of the current head chain: cost-75e (1405 -> 1407, 4 receipts) and cost-60c (1407 -> 1410, 1 receipt).
- Family membership at the D4-orbit level (full 116-superset canonical orbit set per parent), per-child edge-cost recomputation with the verified-det3 legality, receipt in-manifest marginal union vs lost-children comparison, head-total accounting.

## Results (cost-75e, 1405 -> 1407)

- Parents with published 1405 baselines: second_candidate_s5 6/439 -> 5/364 (1 lost row, 75) and cost70g_parent2 48/3885 -> 47/3803 (1 lost row, 82): both deltas exact. cost75e_parent2 (2 lost rows, 157) has no published per-parent baseline; cross-checked via head totals, marginal union and the was_row_of record.
- 2 unique lost children: 00000000040000809002000000000002 (cost 75 recomputed 75, 2 parents) and 00000000000000801202000000000201 (cost 82 recomputed 82, 2 parents); 4/4 family pairs pass.
- Receipts: 4/4 certified (bits 6/10/11/37; bits 11/37 zero in-manifest marginal); union of in-manifest marginals == the 2 lost children D4-canonically.
- Head accounting: 75+82 = 157 = 509457-509300; 2 children = 6443-6441. All checks PASS.

## Results (cost-60c, 1407 -> 1410)

- Four lift/shared parents lost 1-2 rows each (costs 60/59/72); no per-parent 1407 baselines are published for them - losses cross-checked via head totals, marginal union and the in_manifest_marginals was_row_of records. The four untouched parents byte-match the published 1407 records (5/364, 3/209, 10/698, 65/5316, 0 lost rows).
- 3 unique lost children: 00000000000000003800000008008020 (60 recomputed 60), 00000000000000801092200000000000 (59 recomputed 59), 00000000000000801292000000000000 (72 recomputed 72); each a row of exactly 2 parents; 6/6 family pairs pass.
- Receipt: 1/1 certified (bit 92); marginal union == the 3 lost children D4-canonically.
- Head accounting: 60+59+72 = 191 = 509300-509109; 3 children = 6441-6438. All checks PASS.

## Chain completion

- With the cost-65j row verification (commit a66f35c8), the entire 1405 -> 1419 chain is now third-implementation verified at the row level: 14 unique lost children, cost 157+191+635 = 983 = 509457-508474, rows 2+3+9 = 14 = 6443-6429, solved 1405+14 = 1419. Zero residual.
- Baseline-coverage gap recorded: future fold JSONs should publish per-parent rows_before/edge_cost_before for every affected parent (two gaps found this run).

## Observations for the parallel lane

- STERILE rows 65k/70j/74h remain open at 1419; the next neighbor candidate (cost 62 00000000000000801282020000000000) needs the 70j-row coverage pre-check before any sweep.
- The bit-79 orbit remains the weakest proof-tier link (uncertified on both sides); certificate extraction is the highest-priority engine target.
- K0865 checker violation (parallel lane item) untouched.

## Status

- 11x11 empty board, S2 {59,60}, class1/class2/class4 roots: **UNKNOWN** (unchanged; this verification asserts no game-theoretic values).
- head 1419 counts are manifest coverage bookkeeping only.

Output: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost75e-60c-fold-rowbookkeeping-verification-20261116.json`
