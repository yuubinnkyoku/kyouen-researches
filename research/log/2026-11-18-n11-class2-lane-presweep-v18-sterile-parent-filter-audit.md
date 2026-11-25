# n11 class2-lane: v18 target pool is entirely STERILE-parent filtered

Date: 2026-11-18

## Finding

The v18 presweep selector's remaining pool contains only **9 rows**, and all 9 belong to S5 parent `00000000020000003800000080000000`. The head-1410 K0865 census classifies this parent as `all_remaining_sterile`: 18 remaining S6 rows, all 18 in the STERILE registry, total edge cost 1,460.

The v18-selected cost82d row and its runner-up cost82b are both in that STERILE parent and in the STERILE row registry. After applying the K0865/K0863 filter, the v18 pool has **0 eligible rows**. The v18 selection policy excludes 21 class2-lane sweeps but does not apply the STERILE-parent census.

This explains why cost82d was a historical-row revalidation rather than new closure progress. The v17 82/82 REFUTED-D10 sweep confirms one old STERILE prediction; it does not create a certificate or reduce the frontier. The next v18 runner-up cost82b is likewise already a historical STERILE row. It should not be launched as a D10 receipt-closure target.

## Coordinator correction

Rebuild the target census from the current head-1473 worklist, applying the K0865/K0863 STERILE-parent exclusions before ranking. The 3 all-remaining-sterile parents should not be offered as D10 receipt-closure targets. Partial-STERILE parents require separate treatment: they cannot be fully closed by D10 receipts while a STERILE child remains, but their non-STERILE rows may still have cross-cover value. Historical cross-version revalidation should be explicitly labelled as revalidation, not as a new closure attempt.

This log does not create a game verdict and does not change the manifest head. The 11x11 empty board, both two-stone roots, S2 {59,60}, and classes 1/2/4 remain UNKNOWN.
