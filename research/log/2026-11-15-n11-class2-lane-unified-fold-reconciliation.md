# n11 class2-lane: unified fold reconciliation of the divergent chain heads (2026-11-15)

Long-term lane session. Three un-merged folds over the common 1109 baseline were found on main: the cost-68d chain head (solved 1117, 13 receipts: 7 cost-68d WIN7 + 6 warm band hygiene), the warm multiband batch-2 chain head (solved 1140, 31 WIN7 receipts), and this lane's six cost-70c warm batch-2 certificates (published, folded in neither head - the multiband2 fold deliberately deferred the cost-70c band to this lane). This session reconciled all 50 receipts in the sandbox (the execution environment bash/filesystem was unavailable for the whole session - recorded as an experiment fact; the authoritative Python chain fold is specified below for the next execution).

## Receipt reconciliation (50 receipts)

- Root identity: `root == child | 1<<bit` (BigInt) asserted for all 50 receipts; all passed.
- Root disjointness: the three groups are pairwise disjoint; the only intra-group duplicate is the known cross-child pair cost-71b bit-1 == cost-61d bit-22 (root `00000000000000803202000000400002`, canonical single certificate).
- Cross-lane batch-2 agreement: the two concurrent batch-2 lanes independently extracted 29 common roots (byte-verified by both) - a positive duplicate cross-check, not a conflict. This lane's unique additions are the six cost-70c warm certificates (bits 105/92/40/24/11/8; md5s and remote sizes recorded in the audit JSON); the multiband2 lane additionally certified cost-64b bit-40 and cost-61d bit-23.

## Marginal-union arithmetic and the 1154 prediction

From the published per-receipt marginal manifest hexes: cost-68d fold adds 8, multiband2 adds 31, cost-70c warm batch-2 adds 6 (greedy order 105, 92, 40, 24, 11, 8; each in the cost-70c sweep win7 list). The three hex sets are pairwise disjoint (verified), so the 50-receipt union covers exactly 45 manifest orbits over the 1109 baseline: predicted unified solved = 1109 + 45 = **1154**. This is a set-union prediction over published marginals, NOT a chain-head publication; the authoritative unified fold must reproduce the 1117 and 1140 endpoints byte-identically and fold all 50 receipts with the controls in the audit JSON.

## Unified fold specification (next execution)

1. runpy `recompute_frontier_cost68d_20261115.py` - assert the 1109 baseline and the 1117 endpoint.
2. runpy `recompute_frontier_warm_multiband2_20261115.py` - assert the 1140 endpoint.
3. Fold the 13 cost-68d-lane receipts (published order), then the 31 multiband2 receipts (published order), then the 6 cost-70c receipts (greedy order 105, 92, 40, 24, 11, 8).
4. Controls: solved 1154; set-equality `s_merged == s_1117 | s_1140 | covers(6)`; three-way root disjointness.
5. Publish `class-frontier-unified-merge-recompute-20261115.json` + ranking CSVs.

## Outstanding

- cost-69f sweep: completed on the parallel lane (9 WIN7-D10, raw batches only); certificates and fold pending - the next unified merge must fold them once published.
- cost-70c: WIN7 bits 3/42/86/103 remain uncertified.
- cost-65h/67b/68c warm candidates and the in-flight cost-65j sweep stay with the parallel lane.

Audit artifact: [class2-lane-unified-fold-reconciliation-20261115.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-unified-fold-reconciliation-20261115.json)

Interpretation guard: bookkeeping over published receipts; solved counts measure manifest coverage, not game-theoretic value. The 11x11 empty board, the two-stone root {49,60}, S2 {59,60}, class 2 and class 4 all remain UNKNOWN.

## Correction (post-push, same session)

The first version of this log and the audit JSON described the 1117 and 1140 heads as un-merged divergent forks. In fact the merged recompute `class-frontier-merged-recompute-after-multiband2-68dhyg-20261115.json` (commit 19bb2abc) was already on main before that push - the pre-push collision check filtered only for unified/reconcil commit messages and missed it. That recompute reproduces the 1140 head byte-identically and folds the 13 cost-68d/hygiene receipts on top, reaching the **merged chain head 1148/6699/528423/4969/392146** (44 of the 50 reconciled receipts folded; the third class-2 target S5 `00000000000000809102000000000000` narrows to 8 remaining orbits / 588 edge cost).

This is an independent confirmation of this session's reconciliation arithmetic: the cost-68d 8 marginal hexes are set-identical against the 1109 state (this audit) and the 1140 state (their fold), and the six cost-70c hexes are disjoint from all 39 folded hexes (re-verified here). The prediction is therefore unchanged and sharpened: **1154 = 1148 + 6**, pending only the fold of the six cost-70c warm batch-2 receipts. Fold spec and lesson recorded in the audit JSON.
