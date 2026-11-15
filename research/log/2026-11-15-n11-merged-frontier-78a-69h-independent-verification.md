# n11 merged frontier 78a+69h — independent merge verification of the resolved head fork

Date: 2026-11-15
Lane: class-2/4 frontier (n11 S2{59,60} milestone-5, s7-reuse experiment dir)
Status: COMPLETE (verification only; the canonical head was already published by the parallel lane)

## Context

The parallel cost-78a receipt fold (1219 → 1225, commit 1691d9bb) and the parallel cost-69h receipt fold (1219 → 1221, commit 3d2faf3b) both landed from the same cost-67c chain head 1219, leaving the canonical chain forked (noted in the cost-70d sweep log and K0783, commit 4e60e0ff). The parallel 69h lane then rebased its fold on the 78a head (commits aa6cdcf4..01877255), producing the rebased v2 69h head JSON (schema `n11-class-frontier-cost69h-receipts-recompute-20261115-v2`, git blob `d25eb3a00f73cf9ca34fc2816d28045c1e23f3ae`) and resolving the fork at the canonical head **1227/6620/522561/4890/386284**.

This lane independently re-derives that merged head with a **different method**: a single merged sequential replay of all 7 receipts from the 1219 fork state, rather than a rebase of one fold onto the other's head.

## Method (recompute_frontier_merged_cost78a_69h_20261115.py)

1. The cost-67c chain head 1219/6628/523173/4898/386896 is reproduced byte-identically by runpy (head JSON git blob `6d187f48…` re-asserted).
2. Both published branch head JSONs are asserted byte-identical to main by git blob sha: 78a `3938bb16…` (head 1225/6622/522699/4892/386422), 69h rebased v2 `d25eb3a0…` (head 1227/6620/522561/4890/386284). Both branch folds have separately been run to completion by their published fold scripts (each re-verifies every published input against main, re-derives the sweep audit from the raw batches, asserts the certificate bytes and root disjointness, and asserts its head JSON byte-identical to main).
3. The 7 receipt roots (5 cost-78a bits 36/20/29/8/109 + 2 cost-69h bits 58/96) are taken from the two blob-verified head JSONs; their covers() are re-computed with the chain-internal covers(); the 7 roots are asserted mutually disjoint raw-hex and D4-canonically (chain-internal canon()).
4. Chain A is re-derived exactly from the fork: per-bit marginals in publication order [36,20,29,8,109] equal the published per-bit records (6/5/5/5/5 marginal, 2/1/1/1/1 in-manifest), the cost-78a child orbit `00000000000000809102000000400000` closes at bit 36, head numbers 1225/6622/522699/4892/386422 reproduce, and s_1225 == s_1219 ∪ covers(5 roots). Chain B likewise ([58,96], child `0000000000000080120a000000200000` at bit 58, 1221/6626/523035/4896/386758 from the fork alone, historical-baseline agreement with the pre-rebase fold).
5. Branch additions: addA = 26 orbits, addB = 10 orbits, **raw overlap 0, covers-level overlap 0** — no cross-chain double coverage exists, so the two folds are fully additive.
6. The 7 receipts are re-added in one canonical sequential order (78a publication order, then 69h published order) with every per-bit marginal re-derived from the growing merged union; chain-A marginals reproduce their published values exactly and chain-B marginals show **zero deltas** vs their published values (i.e. the 78a fold does not disturb any 69h marginal); both child-orbit closures (bit 36, bit 58) occur exactly once.
7. The merged solved set satisfies s_merged == s_1225 ∪ s_1221 == s_1219 ∪ covers(7 roots); a reverse-order replay (69h first, then 78a) reproduces the identical set (commutativity control).
8. **Third-party agreement control**: the merged head numbers equal the parallel lane's rebased v2 head JSON numbers exactly — **1227/6620/522561/4890/386284**.

## Result

- Merged canonical head: **solved 1227 / unique remaining 6620 / sum remaining cost 522561 / open-classes S6 4890 / open-classes cost 386284**; remaining S5 orbits 175.
- Totals: 7 receipts, total marginal 36 (26 + 10), in-manifest marginal 8 (6 + 2), children closed by bit 36 (cost-78a child) and bit 58 (cost-69h child).
- Parent rows at the merged head: third coverable class-2 target `00000000000000809102000000000000` 2 rows / 143 (best coverable class-2); second coverable class-2 target `00000000000000801202000000200000` 31 rows / 2334; 69h parent2 `0000000000000080120a000000000000` 47 rows / 3455; 78a parent2 `00000000000000801202000100000000` 73 rows / 6065. Best class-4 blocker S5 `00000000020000003800000080000000` unchanged at 18 rows / 1460.
- Determinism: three consecutive runs of the merge script are byte-identical (head JSON md5 `bea292d0fed96c67fb707eb4c2165730`, ranking CSV md5 `f248573f9afd378dc3142bb36e488119`, top-candidates CSV md5 `43ceb46eecd84e9fc1c29407d34115ce`); stdout control lines identical.
- Environment note: running both published fold scripts in one process exceeds the sandbox memory limit (OOM at the 78a certificate-bytes verification); the merge therefore re-loads the two blob-verified head JSONs and re-derives both folds from the fork in a single 67c-chain reproduction (~10 s).

## Value

- Independent (third) verification of the resolved canonical head 1227/6620/522561/4890/386284 by a method disjoint from the parallel lane's rebase: single-order merged replay + union control + reverse-order commutativity + per-bit marginal re-derivation.
- Proof that the two folds are fully additive (raw and covers-level overlap 0; chain-B marginal deltas none), i.e. no orbit was double-counted when the fork was resolved.
- The head fork flagged in the cost-70d sweep log / K0783 is confirmed resolved; subsequent folds must rebase on 1227/6620/522561/4890/386284 (the parallel lane's rebased v2 head JSON numbers).

## Interpretation guard

Bookkeeping over published receipts. Solved counts measure manifest coverage, not the game-theoretic value of any position. REFUTED-D10 sweeps prove only the absence of WIN7-D10; WIN7 certificates prove a win within depth 10 from the individual 7-stone roots only. Closing the two child orbits removes those rows from their parents' remaining rows but does not solve any S5 parent. The standard 11x11 empty board, two-stone root {49,60}/{59,60}, S2 {59,60}, class 2 and class 4 remain **UNKNOWN**.

## Artifacts

- `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_merged_cost78a_69h_20261115.py` — the merge script (runpy 67c chain + 7-receipt merged replay).
- `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-merged-cost78a-69h-recompute-20261115.json` — merged head record (git blob sha `294c4ed3d9fb26143d54ef2e45d400d1068a41dd`).
- `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-s5-ranking-after-merged-cost78a-69h-20261115.csv` — S5 ranking at the merged head.
- `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-top-candidates-s6-after-merged-cost78a-69h-20261115.csv` — top candidates at the merged head.
- Parallel-lane artifacts (rebase): `class-frontier-cost69h-receipts-recompute-20261115.json` (v2, blob `d25eb3a0…`), rebased fold script, claim v4, and the appended 69h fold log.
