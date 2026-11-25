# n11 class-2 lane: cost-63a sweep cross-cover premise audit (2026-11-16)

## What was done
- Audited the ten WIN7-D10 receipt roots of the cost-63a sweep (child `00000000000000809102000800000000`, schema n11-class2-lane-cost63a-sweep-20261114-v1) with the independent third implementation of the win2/win13/win4 audits (BigInt board, bit = y*11+x, D4 canonicalization over the 8 board transforms, exact integer det3/det4, K0868 survival-move convention).
- Purpose: verify the head-1410 closure premise of the 65f/65j fold child `00000000000000809102000080000000`, which the warm-multiband2/unified-merge fold attributed to the cost-63a bit-97 cross-cover receipt `00000002000000809102000800000000`.
- Checks: root reconstruction (child63a | 1<<bit) for all 10 win7_bits, K0868 survival legality, popcount 7, covers = 7 rows with child63a, membership of the 65f/65j child in every cover set, S5 parent relations, D4 orbit distinctness of the two children.
- The audit was run twice with identical results (deterministic recompute).

## Results (10/10 pass)
- All 10 root reconstructions exact; all 10 bits K0868 survival-legal; every root covers exactly 7 rows including child63a. Controls: S5 parent `00000000000000809102000000000000` (stones 49/56/60/63/71) is a subset of both children; child63a = S5 + bit 35, the 65f/65j child = S5 + bit 31; the two children are distinct D4 orbits (both canonical-self).
- Cross-cover premise exact: removing stone 35 from the bit-97 root leaves {49,56,60,63,71,97}, whose D4 canonical form is exactly the 65f/65j child. The bit-97 root covers both children; it is the only one of the ten 63a win7 roots that covers the 65f/65j child.
- Verification tiers pinned down: bit 97 is a search-level WIN7-D10 verdict (win7_bits, heaviest_bits 11,447,839 nodes; raw batch6) and sits in unverified_win7_bits of the certificates manifest - no certificate has been extracted for it, and the sweep's cross-engine/fresh-rerun controls cover bits 32/2/119/11, not bit 97. The single certificate-backed receipt of the family (bit 119, 28,509 rows) covers only the child63a orbit and does NOT cover the 65f/65j child.
- Consequence for the fold premise: within the WIN7-D10 receipt framework, the head-1410 "solved" bookkeeping of the 65f/65j child rests on the search-level bit-97 receipt; the certificate-backed coverage of the same child comes from the 17 head-1419 receipts of the 65f/65j folds, whose roots are all child+1 stone (child in every cover set; 13 of the 65f family certificate-backed per the win13 manifest, the 4 of the 65j family are fold-v2 receipt records).
- Certificate and sweep bodies are the publishing lane's records; this audit is structural only and does not re-run the engine remotely.

## Observations for the parallel lane
- If the child-closure chain is ever to be upgraded to fully certificate-backed at the head-1410 tier, the missing piece is a bit-97 certificate extraction (root `00000002000000809102000800000000`) - the only 63a win7 bit whose receipt closes the 65f/65j child. Alternatively, certificate-backed coverage already exists one fold later via the 65f/65j head-1419 receipts.
- K0865 checker violation (parallel lane's item) remains unfixed; see the win13 audit log.

## Status
11x11 empty board / two-stone roots / S2 / class 1 / class 2 / class 4: all UNKNOWN. solved counts are manifest coverage bookkeeping, not game outcomes. REFUTED-D10 is not a LOSS proof. WIN7-D10 certificates prove a first-player win within depth 10 from the individual 7-stone roots only; a search-level WIN7-D10 verdict is weaker than a certificate.

Output: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost63a-sweep-crosscover-premise-audit-20261116.json`
