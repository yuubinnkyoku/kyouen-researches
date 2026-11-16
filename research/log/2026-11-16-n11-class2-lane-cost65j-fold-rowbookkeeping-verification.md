# class2-lane: cost-65j fold row-level bookkeeping verification (2026-11-16)

## What was done

- Independent third implementation re-verification of the current head's final fold step (cost-65j, 1410 -> 1419): all 9 affected parents, all 18 parent-child row losses, all 9 unique lost children, and the 17 receipts' in-manifest marginals.
- Family membership verified at the D4-orbit level (each parent's full 116-superset canonical orbit set enumerated; each child's canonical form checked for membership).
- Each lost child's edge cost independently recomputed with the verified-det3 survival legality (65f control: re-enumerates to 65).

## Results

- All 9 parents: popcount 5, rows delta == lost-row count, edge-cost delta == lost-cost sum (133/64/635/71/74/76/69/74/74).
- All 9 unique lost children: popcount 6, every child is a row of exactly two parents (18 parent-rows), every recomputed legal-candidate count equals the listed cost (64/69/64/71/74/76/69/74/74).
- Family membership: 18/18 pairs pass at the orbit level; in 5 pairs the canonical child contains the parent only via a D4 image (manifest rows are canonical representatives).
- Receipts: union of the 17 receipts' marginal_manifest_hexes equals the 9 lost children D4-canonically (e.g. bit-4's 00000000000000043800000008002000 vs manifest row 0000000000000043800000008002000).
- Global accounting: unique child cost sum 635 == head sum_remaining_cost delta (509109-508474); parent-row sum 1270 == 2x635; solved delta 1410+9=1419.
- All checks PASS. The current head 1419/174/6429/508474/4702/372388 is now third-implementation verified at the row level for its final fold.

## Observations for the parallel lane

- The census-overlap bit-79 orbit is uncertified on BOTH sides: the 65f-side receipt (00000000000080809102000080000000) is among the 13 uncertified cost-65f receipts (blob-pinned raw records), and the 63a-side root (00000002000000809102000080000000's twin 00000002000000809102000800000000) remains search-level. Certificate extraction for the bit-79 orbit is the weakest proof-tier link among the four census overlaps - highest-priority engine certificate target.
- Zero in-manifest-marginal receipts: bits 15/23/25/66/79/91/101/119 (folded for root-coverage completeness, no remaining-row value at 1410).
- K0865 checker violation (parallel lane item) remains unfixed; not touched here.

## Status

- 11x11 empty board, S2 {59,60}, class1/class2/class4 roots: **UNKNOWN** (unchanged; this verification asserts no game-theoretic values).
- head 1419 counts are manifest coverage bookkeeping only.

Output: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost65j-fold-rowbookkeeping-verification-20261116.json`
