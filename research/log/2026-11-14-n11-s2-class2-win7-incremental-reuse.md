# 2026-11-14 S2 {59,60}: incremental class2-lane WIN7 reuse

Main snapshot: `b8e0427e8d7e8a460ac6fe55bde1ce6cac0f9d58`.

## Scope and method

The S2 {59,60} milestone-5 S6 worklist contains 7,867 D4-canonical six-stone rows, with total legal seventh-move candidate cost 615,497. The earlier reuse audit matched 4,052 baseline WIN7 receipts to 498 worklist parents. This pass adds four later class2-lane certificate manifests: cost-69c, cost-70b, cost-71, and cost-75.

For every new certificate root, the audit canonicalizes its seven-stone mask under D4, checks the seven-stone count, and independently checks exact safety using integer collinearity/cocircularity tests. It then deletes each occupied point, canonicalizes the resulting six-stone parent, and matches it against the full S6 worklist. Baseline WIN7 and LOSS7 receipt sets are checked for internal conflict and the new WIN7 roots are checked against the baseline LOSS7 set.

## Result

- New WIN7 roots: **23**, all distinct and exact-safe; no duplicate baseline WIN7 root and no conflict with baseline LOSS7.
- New parent-child incidences: **70** across **48** distinct S6 worklist parents.
- Five of those parents were already covered by the baseline. The incremental gain is therefore **43 new D4-canonical S6 worklist orbits**: 3 class-1, 35 class-2, and 5 class-3.
- Baseline parent coverage: 498. After union: **541**.
- Worklist rows not yet closed by this WIN7-reuse mechanism: 7,867 → **7,326**.
- Remaining legal seventh-move candidate cost: 615,497 total; 577,110 after baseline reuse; **573,835** after this pass. Incremental reduction: **3,275**.

The cost column is the number of legal seventh-move candidates associated with each S6 worklist row. It is not a search-node count, game distance, or a verdict for an unresolved root.

## Verification boundary

The audit rechecks geometry, D4 normalization, parent incidence, and conflicts. It does **not** re-run the 23 certificate bodies. Their WIN7 verdicts are reused from the already-published certificate manifests and verification logs. A WIN7 root is an original-first-player win; restoring any one removed point as the seventh move gives a winning move from the corresponding six-stone parent. This only closes the matched S6 worklist rows.

Reproduction:
- Script: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_incremental_class2_win7_reuse.py`
- Output: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-win7-reuse-incremental-20261114.json`

## Separate in-flight record

The latest main still contains cost-73a as an in-flight sweep. Its JSON says 64/73 candidates done (1 WIN7 bit 81, 63 REFUTED, 0 capped, 324,426,606 nodes) with 9 remaining, while the commit subject for the in-flight record says 57/73. The JSON arithmetic is internally consistent (1+63=64; 64+9=73), but the subject is stale by seven candidates. Raw batches A-H are not in the repository and certificate extraction is pending, so cost-73a is excluded from this reuse pass.

## Status

The S2 {59,60} root, two-stone root {49,60}, and standard 11×11 empty root remain **UNKNOWN**. This pass reduces the S6 worklist but does not close the 1,447-orbit S5 worklist or determine any of those roots.
