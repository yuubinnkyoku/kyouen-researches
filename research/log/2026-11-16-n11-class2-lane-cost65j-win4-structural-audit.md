# n11 class-2 lane: cost-65j win4 structural audit (2026-11-16)

## What was done
- Audited the four cost-65j WIN7-D10 certificate receipts bits 112/116/118/119 of child `00000000000000809102000080000000` published in the cost-65j fold v2 receipts recompute record (schema n11-class2-lane-cost65j-receipts-recompute-20261116-v2) with the independent third implementation of the win2/win13 audits (BigInt board, bit = y*11+x, D4 canonicalization over the 8 board transforms, exact integer det3/det4, K0868 survival-move convention).
- Checks per bit: root reconstruction (child | 1<<bit), published canonical match, K0868 survival legality, popcount 7, covers recomputed as canon(root ^ 1<<s) for each stone, child in covers, the fold-v2 marginal_manifest / marginal_non_manifest hexes checked against covers, and covers cross-classified against the 6,438-row remaining-worklist-1410 (categories sterile / transfer_partial / win_pending / win_receipt_scheduled / unswept).
- The audit was run twice with identical results (deterministic recompute; same controls and per-bit outputs).

## Results (4/4 pass)
- All four root reconstructions exact; all four published canonical hexes match recomputation - all four played roots are non-canonical, in the same 8112 family as win13 bits 91/101/109 (00000000020000811202000000000100 / 00000000020000811202000000000010 / 00000000020000811202000000000004 / 00000000020000811202000000000002).
- All four bits are K0868 survival-legal; each root covers exactly 7 rows including the child. Controls: S5 parent subset of child, child survival count 65, worklist 6,438 rows, 9 win_receipt_scheduled rows.
- Scheduled-row closure exact: bit 112 closes `00000000010000003800000008080000` (74), bit 116 closes `00000000000000003800100008080000` (76), bit 118 closes `00000000000000003800000008480000` (71); bit 119 covers no scheduled row (zero-marginal, as recorded in totals.zero_mim_receipts of the fold-v2 record).
- Union check: the union of the 65j scheduled hits equals exactly the three rows the 65f win13 audit left open. The nine scheduled rows of the child are therefore fully partitioned: 6 by 65f, 3 by 65j. Together with the win13 audit (commit 74076854), all 17 head-1419 WIN receipts of this child are now structurally verified by the third implementation.
- Fold-v2 marginal basis confirmed: for bits 112/116/118 the covers intersect worklist-1410 in exactly the single scheduled row, and the four marginal_non_manifest hexes per bit (e.g. bit 112: `00000000020000011202000000000100`) are not worklist-1410 rows. The fold-v2 record's "marginal" is the corpus-wide open-row census, not worklist-1410, consistent with the win13 audit's measurements.
- Certificate bodies are the publishing lane's records; this audit is structural only and does not re-run the engine remotely.

## Observations for the parallel lane
- K0865 checker violation (computed: front-matter key, topic bookkeeping, roles primary output / secondary output / report) remains unfixed; it is the parallel lane's item (see the win13 audit log).
- Premise already recorded in the fold-v2 record: child `00000000000000809102000080000000` itself was already solved at head-1410 (cost-63a bit-97 cross-cover receipt, warm-multiband2/unified-merge fold); the 65f/65j folds' value is the closure of the nine scheduled rows, now fully verified and partitioned 6+3.

## Status
11x11 empty board / two-stone roots / S2 / class 1 / class 2 / class 4: all UNKNOWN. solved counts are manifest coverage bookkeeping, not game outcomes. REFUTED-D10 is not a LOSS proof. WIN7-D10 certificates prove a first-player win within depth 10 from the individual 7-stone roots only.

Output: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost65j-win4-structural-audit-20261116.json`
