# n11 class2-lane: fresh-mirror reproduction of the merged 63h/63i fold (head 1369) and post-merge v10 audit re-run

- date: 2026-11-16
- lane: long-term (n11 = 11x11 weak-resolution support)
- status: 11x11 empty board / two-stone roots {49,60} and {59,60} / S2 {59,60} / class 1 / class 2 / class 4 all UNKNOWN; solved counts are manifest-coverage bookkeeping only, and REFUTED-D10 is not a LOSS proof.

## Fresh-mirror reproduction of the merged fold (published state only)

Goal: confirm that the new canonical head 1369/6479/512163/4749/375886 (landed in commit c3bd5b4f) is reproducible from published main artifacts alone, catching any 62a-style reproducibility gap immediately rather than in a later lane.

Procedure (everything fetched fresh; no local carry-over):

1. codeload zip of main at HEAD c3bd5b4f (3,322,548,506-byte zip, 5.3 GB extracted); the fresh mirror contains no tmp-* intermediates.
2. Published reconstruct chain run in dependency order, all PASS:
   reconstruct_tmp_cost84a_20261116.py (27s) -> cost83d (32s) -> cost83c (12s) -> cost83a (22s) -> cost69i (20s) -> cost62a (22s) -> cost58c (102s) -> cost63h (2s) -> cost63i (59s; the gap-fill script published in c3bd5b4f, 18 certificates fetched from raw CDN, tsverify + BigInt all PASS). Total ~5 min wall.
3. recompute_frontier_merged_cost63h_63i_20261116.py run in the fresh mirror: 122 published input files byte-verified against main by git blob sha; the runpy cascade re-derives the full fold chain from the reconstructed 1227 baseline (cost-70e/71c/70f/72c/... through the 58c, 63h, 63i folds) with all in-script CONTROLs PASS.

Results:

- The 3 merged outputs regenerate byte-identical to the published versions (cmp equal; md5 98dc696c7f68b93e66fa4cdd10b4e025 / edf1fc4b329884a25e8bd4b8e0e63b45 / e68f3266ef6f0dae98d2bffff98a2a72; git blob shas c3ff50364499014a7096151bd9893a6510386c05 / d065e54fe7defdafe76d7a1f3a8956cf1c706963 / 34067a180a254c032ce90b0594cf2f0ffd33d1a0).
- Intermediate heads reproduced with blobs equal to the published values: 63h head JSON 647498b995770ff87b12e868a5b89015c26be51e (6,852 B), 63i head JSON db0288f15f1538293e66146542a938c9ebf8b91c (16,455 B).
- Head summary 1369/6479/512163/4749/375886 with the published histogram; the reverse-order replay control re-confirmed the merged set is order-independent.

Conclusion: the merged fold and the published reconstruct chain are fully independently reproducible from main alone. No gap of the kind found earlier for cost-62a exists for cost-63i; the gap-fill script reconstruct_tmp_cost63i_20261116.py is itself verified from fresh state.

## Post-merge v10 audit re-run (claim reconciliation-field safety check)

The merged fold updated class2-lane-cost63h-inflight-20261115.json in place (added a content-preserving reconciliation section; existing fold records kept as the 1362-branch history). Both published audit implementations and the agreement script were re-run on the post-merge mirror:

- audit_published_chain_roots_independent_20261115.py (v10): AUDIT PASSED (pins 108 = 26+52+30; cumulative 650 roots / 639 D4 orbits / 11 twin pairs; canonical 1233..1362 exactly-once, mim 129; receipt records 527; geometry anomalies 0; child-closure heads 37).
- audit_published_chain_roots_second_independent_v10_20261115.py: AUDIT PASSED (pins 104 = 26+52+26; identical inventory numbers).
- audit_dual_implementation_agreement_20261115.py (v7): AGREEMENT CONFIRMED (all 9 endpoint pairs; the 58c/63h pair reports 30 heads / 650 roots / 639 orbits / 11 twins / canon 1233..1362 mim 129).

The reconciliation addition to the 63h claim JSON does not affect any published audit assertion (added keys only; all previously asserted fields unchanged).

## Resume state

- canonical head 1369 (class-frontier-merged-cost63h-63i-recompute-20261116.json, blob c3ff50364499014a7096151bd9893a6510386c05).
- cost-63j remains IN FLIGHT (parallel-lane claim class2-lane-cost63j-inflight-20261116.json, child 00000000040000003800000048000000, 1367 baseline): do not touch; when it lands, its fold must re-base onto the 1369 head.
- Next audit extension (v11, both implementations + agreement v8) should pin the 63i and merged-fold endpoints (head 1369) and add the 63i/merged pair.
- 11x11 empty board and all listed classes/roots remain UNKNOWN.
