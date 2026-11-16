# 2026-11-16: cost-64d WIN23 receipt-to-frontier marginal audit (third implementation)

## Scope

This is a structural audit of the published cost-64d sweep projection at canonical head 1419. It does not re-run the engine, verify the 23 WIN7-D10 certificates, or apply the fold.

Inputs were fetched from main at `d155647e02020f1fbff798b6fa229ed4cdb658c8` and pinned by Git blob SHA in the JSON output:
- the 6,438-row head-1410 remaining-S6 worklist;
- the completed cost-64d claim (64 legal candidates, 23 WIN7-D10 bits);
- the independent raw-sweep audit with per-receipt `marginal_in_manifest_1419` and per-parent projected losses.

## Independent method

For each of the 23 WIN bits, reconstruct the seven-stone root as child OR bit. Apply all eight D4 transformations independently to the root and to each of its seven one-stone deletions. Join the canonical six-stone deletions against the 6,438-row worklist.

A subtle accounting distinction matters: the worklist still contains rows whose `open_candidates_after_transfers` is zero because a WIN receipt is already scheduled for them. Such rows are real subset hits, but not new marginal closures. The audit therefore counts only rows with `open_candidates_after_transfers > 0` and compares every per-root set against the published marginal list.

## Results

- 6,438 worklist rows; 64 legal candidates; 23 WIN7-D10 roots.
- All 23 WIN roots have distinct D4 orbits.
- Before excluding already-scheduled rows: 20 unique subset-hit rows and 42 receipt-row edges.
- Four already-scheduled rows/edges are excluded from new marginals.
- New marginal union: **16 unique rows**, represented by **38 receipt-row edges**.
- Per-root coverage histogram: 10 roots cover one new row, 11 cover two, and 2 cover three.
- The 16 rows have **30 parent-row incidences**; this exactly matches the sum of `rows_lost` in the 13 published parent-projection records.
- Sum of per-parent projected edge-cost deltas: **−2,133**.
- Every one of the 23 independently reconstructed per-root marginal sets matches the published audit exactly; the swept child itself is in the new marginal union.
- The published projected head is 1435, but this is still a projection only. The canonical head remains 1419 until the chain reproduction and fold are actually applied.

The key correction is not a change to the 16-row result: counting all D4 subset hits naively gives 20 rows, because four were already scheduled. Filtering on the published open-after-transfer count reproduces the exact 16-row marginal union and 30 parent incidences without double counting.

## Boundary

The 23 WIN7-D10 verdicts concern their individual seven-stone roots only. REFUTED-D10 is not a LOSS proof. This audit establishes no value for either open S5 parent, the two-stone roots, S2, or the empty 11×11 board. All remain UNKNOWN. No frontier fold was applied.

## Reproduction

Run from the repository root:

`python research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost64d_marginals_third_20261116.py`

The script uses only the Python standard library. Machine-readable output: [class2-lane-cost64d-marginal-audit-third-20261116.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost64d-marginal-audit-third-20261116.json).
