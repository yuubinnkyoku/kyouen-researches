# n11 class-2 lane: cost-65f win2 bits 20/21 structural audit + sweep candidate convention determination (2026-11-16)

## What was done
- Independently re-implemented the S6->S7 sweep-candidate arithmetic in TypeScript (BigInt board, bit = y*11+x, D4 canonicalization over the 8 board transforms, exact integer det3/det4).
- Audited the two cost-65f WIN7-D10 receipts bits 20/21 of child `00000000000000809102000080000000` - the receipts that closed the two cost-64 manifest rows in the cost-65j fold v2.
- Determined and cross-verified the published `own_candidates` (edge cost) convention on the child, on all 17 fold-v2 receipt bits, and on a 42-strata sample of the 6,438-row remaining-worklist-1410 cost column.

## Sweep candidate convention (determined)
A legal candidate is an empty cell on no common circle AND no common line with any 3 of the 6 stones (det4(a,b,c,cell) != 0 for all triples, degenerate triples included). The sweep enumerates survival moves; edge cost = count of such cells. Evidence:
- 65f child: completing 50, survival 65 = published edge cost 65.
- All 17 fold-v2 receipt bits are survival cells (including bits 20/21).
- 42 cost strata of the worklist: 42/42 match `115 - completing_inclusive`. The circle-only variant fails on 9 of the 42 rows (always survival overcounted); the inclusive rule fixes all 9 - so lines count as degenerate completing configurations.
- Consequence: the whole worklist cost column is independently re-derivable from stone positions alone with exact integer arithmetic.

## bits 20/21 structural results
- Root reconstruction exact (child | 1<<bit), D4 canonical hex matches, each root covers exactly 7 rows including the child, all marginal hexes present in covers.
- bit20 root covers `00000000000000003800000008003000`; bit21 root covers `00000000000000003800000008002002` - both are cost-64 rows of the fold v2 CLOSED9, independently confirming the manifest's claim and the fold v2 application audit's C3 (commit 72d18d2c).
- Certificate bodies (43,119 / 50,284 rows, part1of2/part2of2, BigInt union 0/0 + Bareiss 52/52) were double-verified by the parallel lane; this audit is structural only and does not re-run the engine remotely.

## Corrections recorded
- An earlier probe in this lane mis-took the circle-completing set as the legal set and flagged bits 20/21 as illegal; the determined convention is the complement (survival moves). The published fold audit C2 (17/17 PASS) is consistent with the survival convention and stands.

## Status
11x11 empty board / two-stone roots / S2 / class 1 / class 2 / class 4: all UNKNOWN. solved/manifest counts are coverage bookkeeping, not game outcomes. REFUTED-D10 is not a LOSS proof.

Output: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost65f-win2-structural-audit-20261116.json`