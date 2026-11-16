# N11 class-2 lane: cost64h verified receipt fold (2026-11-17)

## Result

The 23 cost64h WIN7-D10 receipts have been folded into the canonical S6 manifest. This is a bookkeeping fold of already verified certificates; it is not a new engine search and creates no new game verdict.

The fold starts from canonical head:

`1452/174/6396/506144/4669/370058`

and produces:

`1472/174/6376/504672/4649/368586`

Exactly 20 manifest S6 rows are newly closed. The 23 receipts have total marginal 111 D4 orbits, of which 20 are manifest rows. The fold affects 17 S5 parents, 42 parent-row incidences, and reduces aggregate parent-edge cost by 3,090.

The target S5 parent `00000000000000403800000008000000` goes from 18 open rows / edge cost 1,287 to 12 open rows / edge cost 872 (six rows and 415 edge-cost units removed). No S5 parent is fully closed by this fold.

## Evidence checks

- The independent fold pre-registration is pinned at blob `5074a8a0cbb75fcc91b5b999a3135fac06d42400`; its independent-agreement record is pinned at `9ab473ac0163755ddf541d8a9a5e44da304f8095`. The reproduced basis head, projected head, receipt list, parent deltas, demand histogram, and conflict census all agree.
- The certificate directory contains 23 `.cert` files. Every path, Git blob SHA-1, byte count, bit, and root header matches the fourth Python verification record. All 23 certificates independently pass; consumed-union missing/extra are both zero and terminal-stone range is [13,17].
- Aggregate certificate evidence: 29,053,047 bytes; 804,783 strategy rows; 1,755,168 visited states; 1,584,262 loser-reply edges; 280,569 terminals.
- The v17 full-row recheck covers all 64 cost64h candidates. All 64 are byte-identical in verdict and node count to the published v16 row: 23 WIN7-D10, 41 REFUTED-D10, zero capped, 47,017,565 candidate nodes. No fbt saturation occurred in this row.
- Cross-source verdict scan against cost66i and cost76c reports zero conflicts. A separate D4 root comparison also finds zero overlap between the 23 cost64h WIN roots and the nine cost66i WIN roots, and zero overlap with the two corrected cost76c WIN roots.

The 145-check audit is published in `class2-lane-cost64h-fold-audit-20261117.json`. It includes per-certificate path/blob/size/root/terminal/union checks and the fold projection checks.

## Canonical frontier deltas

| Metric | Before | After |
|---|---:|---:|
| Solved S6 rows in manifest | 1,452 | 1,472 |
| Remaining S5 orbits | 174 | 174 |
| Unique remaining S6 | 6,396 | 6,376 |
| Sum remaining edge cost | 506,144 | 504,672 |
| S6 demand by open classes | 4,669 | 4,649 |
| Open-class demand cost | 370,058 | 368,586 |

The remaining S5 orbit count is unchanged: this fold improves the frontier but does not close a five-stone parent.

## Cross-lane handoff

- cost76c remains v17-corrected at the historical head 1452: WIN7-D10 bits 61 and 99; bit 113 is REFUTED-D10. Bit 61 remains the primary certificate target. Its old marginal projection must be recomputed against head 1472 after certificate verification.
- cost66i now has all nine WIN7-D10 certificates extracted and independently verified. Its nine-receipt fold remains pending until cost76c is folded; then its marginals must be recomputed against the resulting head.
- The cost66i cross-source audit records bit 100 as agreeing with the cost64h REFUTED-D10 orbit (cost64h bit 103); this is agreement, not a WIN/REFUTED conflict.

## Published artifacts

- Generator: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/fold_cost64h_verified_receipts_20261117.py`
- Fold: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost64h-receipts-recompute-20261117.json`
- Audit: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost64h-fold-audit-20261117.json`
- Updated claims: cost64h v3, cost76c v5, cost66i v6.

The generator was added for full-checkout reproduction. In this run, the certificate bytes were matched to GitHub blob metadata and the independent verifier output, and the fold record was checked field-by-field against the preregistration in the execution harness; the Python generator and the repository's `check_cost64h_fold_receipt_agreement_20261116.py` were not executed locally.

## Interpretation guard

WIN7-D10 is a certificate for the individual seven-stone root. REFUTED-D10 is not a LOSS proof. This fold closes 20 S6 manifest rows but no S5 parent, no two-stone root, and no one-stone root. The standard 11×11 empty board remains **UNKNOWN**.
