# n11 class-2 lane: cost-65f win13 structural audit (2026-11-16)

## What was done
- Audited all 13 cost-65f WIN7-D10 certificates of child `00000000000000809102000080000000` published in the win13 manifest (schema n11-class2-lane-cost65f-win13-certificates-20261116-v1) with the independent third implementation of the win2 audit (BigInt board, bit = y*11+x, D4 canonicalization over the 8 board transforms, exact integer det3/det4, K0868 survival-move convention).
- Checks per bit: root reconstruction (child | 1<<bit), published d4_canonical_hex match, K0868 survival legality, popcount 7, covers recomputed as canon(root ^ 1<<s) for each stone, child in covers, and covers cross-classified against the 6,438-row remaining-worklist-1410 (categories sterile / transfer_partial / win_pending / win_receipt_scheduled / unswept).
- The audit was run twice with identical results (deterministic recompute; same controls and per-bit outputs).

## Results (13/13 pass)
- All 13 root reconstructions exact; all 13 published D4 canonical hexes match recomputation, including the three non-trivial ones (bits 91/101/109 played roots are not canonical: 00000000020000811202000020000000 / 00000000020000811202000000080000 / 00000000020000811202000000000800).
- All 13 bits are K0868 survival-legal; each root covers exactly 7 rows including the child. Controls: S5 parent subset of child, child survival count 65, worklist 6,438 rows, 9 win_receipt_scheduled rows.
- Marginal classification exact: the six marginal-in-manifest receipts bits 4/18/20/21/28/109 each cover exactly one of the nine win_receipt_scheduled rows - bits 20/21 the two cost-64 rows (consistent with the win2 audit), bit 4 `00000000000000043800000008002000` (74), bit 18 `00000000000000003800000408002000` (74), bit 28 `00000000000000003800400008002000` (69), bit 109 `00000000000000003800000008002200` (69).
- The seven zero-marginal receipts bits 15/23/25/66/79/91/101 cover no scheduled row; in fact their covers intersect the worklist-1410 in no row at all.
- The remaining three scheduled rows (`00000000000000003800000008480000` 71, `00000000000000003800100008080000` 76, `00000000010000003800000008080000` 74) are not covered by any 65f root, consistent with the manifest's attribution of their closure to the four cost-65j certificates (manifest d4981d7e).
- Certificate bodies (587,837 rows total, BigInt union 0/0 and Bareiss all-pass per manifest) are the publishing lane's records; this audit is structural only and does not re-run the engine remotely.

## Observations for the parallel lane
- K0865 (head-1410 census, parallel lane's item) appears to violate the current knowledge checker on three counts: a `computed:` front-matter field (not in the allowed key set id/title/kind/status/topics/aliases/relations/artifacts/scope/evidence/solution), topic `bookkeeping` (not in VOCABULARY.yaml), and artifact roles `primary output` / `secondary output` / `report` (not in the allowed role set). K0866/K0867 and the schema-fixed K0868 are conformant by the same static check. Recorded here only; not modified by this lane since the item belongs to the parallel lane.

## Status
11x11 empty board / two-stone roots / S2 / class 1 / class 2 / class 4: all UNKNOWN. solved counts are manifest coverage bookkeeping, not game outcomes. REFUTED-D10 is not a LOSS proof. WIN7-D10 certificates prove a first-player win within depth 10 from the individual 7-stone roots only.

Output: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost65f-win13-structural-audit-20261116.json`
