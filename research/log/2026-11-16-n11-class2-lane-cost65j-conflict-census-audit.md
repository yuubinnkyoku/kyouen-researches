# n11 class-2 lane: cost-65j conflict census audit (2026-11-16)

## What was done
- Independently audited the conflict census of the cost-65j fold v2 record (schema n11-class-frontier-cost65j-receipts-20261116-v2): the claim that of the 65 candidate orbits of child `00000000000000809102000080000000` exactly four overlap the 718 folded roots at head 1410, all WIN7/WIN7 with zero WIN/LOSS conflicts (bits 25/79/91/101).
- Tools: the independent third implementation of the win2/win13/win4 audits (BigInt board, bit = y*11+x, D4 canonicalization over the 8 board transforms, exact integer det3/det4, K0868 survival-move convention), plus a full re-read of the 9 blob-pinned raw batch JSONLs from latest main and provenance fetches of the cost-72b / cost-69i receipt records and the warm-multiband2/unified-merge addition entries.
- The audit was run twice with identical results.

## Results (all checks pass)
- Legal candidate set re-enumerated from the survival rule: exactly the published 65 candidate bits (set equality). Square 97 is excluded because it is concyclic with child stones 31/49/71 - this is why no receipt root of this child contains stone 97 without also dropping stone 31.
- All 65 candidate roots occupy 65 distinct D4 orbits: no intra-sweep collision, so no WIN/REFUTED conflict is possible inside this sweep. The 17 WIN receipts occupy 17 distinct orbits and all 17 canonical hexes match the fold record (consolidated re-verification of the win13 and win4 audits).
- All four census overlaps verified as genuine D4-orbit identities: bit 25 is byte-identical to the cost-72b bit-31 receipt; bit 79's orbit is the cost-63a bit-97 cross-cover receipt; bit 91's orbit is the cost-72b bit-97 receipt; bit 101's orbit is the cost-69i bit-97 receipt. Each closer root: 7 stones, covers = 7, child canonical in covers, and every stone survival-legal against the other six.
- Raw batch re-read: 64 bit records, no duplicates, bit 113 absent (canonical identity transfer), verdicts 17 WIN7 / 47 REFUTED run / 0 capped, per-batch node sums equal to the fold-script pins, total 402,603,616 = 158,472,633 (WIN) + 244,130,983 (REFUTED run), pilots 5949 x7 + 3402 x2. The four census bits are loss:true in batches 3/5/6/7.
- Structural cause identified: the S5 parent `00000000000000809102000000000000` (stones 49/56/60/63/71) is setwise invariant under the vertical reflection (x,y)->(x,10-y) (which swaps 49<->71); the four overlaps are exactly the reflection images of the four zero-marginal 65f WIN candidates (31<->97, 79->35, 91->25, 101->13). The children themselves have trivial stabilizers, which is why all 65 candidate orbits are distinct.
- Proof-tier upgrade (no new computation): the folded-side counterparts of census bits 25/91/101 are certificate-backed WIN7 receipts (72b bit-31 md5 1ee298bcb02c41962aa1242dc1f805dc, 72b bit-97 md5 6ed0334c4c9540c39ce8cf839f900a18, 69i bit-97 md5 95707f643661f24bad14c3c01bcefefb); by D4 symmetry these certify the 65f receipt orbits too. Only the bit-79 orbit remains search-level on the folded side (cost-63a bit-97, unverified_win7_bits): extracting that one certificate would certificate-back all four census-overlap orbits.
- Cross-engine anchor: the 72b bit-31 v15 anchor count 13,884,751 equals the 65f bit-25 raw record exactly - the same root was searched twice (v15 as 65f bit-25, v16 as 72b bit-31 at 2,481,547 nodes), both WIN7.
- Scope: the exhaustive negative direction (no fifth overlap among the 718 folded roots) rests on the published fold script's runpy chain with byte-identical reproduction controls; this audit verifies the four positive overlaps, the intra-sweep disjointness, and both sides' verdict provenance.

## Observations for the parallel lane
- K0865 checker violation (computed: front-matter key, topic bookkeeping, roles primary output / secondary output / report) remains unfixed; it is the parallel lane's item (see the win13 audit log).
- The bit-79 orbit (root `00000002000000809102000800000000`, canon `00000000000080809102000080000000`) is the only census-overlap orbit without certificate backing on either side (65f bit-79 raw sweep + 63a bit-97 search-level). Certificate extraction for it would close the last gap; the 63a sweep record lists bit 97 in unverified_win7_bits.
- The S5 vertical-reflection stabilizer means every future receipt of any child of this S5 should be census-checked against the sigma-image family: the 65f/65j fold found all four overlaps this way, and the same mechanism will produce cross-cover opportunities for the remaining S5s of the 8012 family.

## Status
11x11 empty board / two-stone roots / S2 / class 1 / class 2 / class 4: all UNKNOWN. solved counts are manifest coverage bookkeeping, not game outcomes. REFUTED-D10 is not a LOSS proof. WIN7-D10 certificates prove a first-player win within depth 10 from the individual 7-stone roots only.

Output: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost65j-conflict-census-audit-20261116.json`
