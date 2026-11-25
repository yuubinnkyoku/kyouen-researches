# n11 class2 frontier union and cost-65e bit-107 parent lift

Date: 2026-11-15  
Inspected main head: `8a0f072e9c2afc8b805fd95df5557765149f44a4`

## A common frontier across three parallel receipt lanes

The cost-63a, cost-61e and cost-61f frontier outputs can be combined exactly. Their common base is the after-cost-61d state:

- 951 solved S6 positions in the manifest
- 6,896 unique S6 positions remaining
- total remaining edge cost 542,952
- open-class demand 5,166 S6 / 406,675 edges

The three marginal canonical-key sets are pairwise disjoint: cost-63a contributes 2 keys, cost-61e contributes 3, and cost-61f contributes 5 unique keys (the three cost-61f certificates list 7 marginal incidences, with overlap inside that lane). All ten keys occur in the 7,867-row S6 manifest, and their manifest costs sum to 660.

The combined state is therefore **961 solved / 6,886 remaining / 542,292 remaining cost / 5,156 open S6 / 406,015 open cost**. This is a set union of the three published recomputations, not a new replay of their certificate bodies.

## cost-65e bit-107: one more known S6 parent

The completed cost-65e sweep classified all 65 legal seventh moves: 21 WIN7-D10 candidates, 44 REFUTED-D10, 0 capped, 308,092,253 nodes. Its bit-107 certificate is a new WIN7 root:

- root `00000800000000809102000000800000`
- 18,930 rows
- 44/44 sub-roots PASS, consumed-row union 0 missing / 0 extra
- FBT drops 0
- SHA-256 `ac656690280ef9f2162936fcc48504902840ac1f24315aa3a9323c84a778c2e9`

An independent exact determinant implementation confirms the root is safe and has 44 legal opponent replies. Removing each of its seven stones and canonicalizing under D4 yields four S6 positions in the 7,867-row manifest. One is the cost-65e target parent itself, `00000000000000809102000000800000`, with edge cost 65 and class mask 2. It is not among the ten positions already counted in the three-lane union.

For the corresponding S5 target `00000000000000809102000000000000`, the published cost-63a frontier has 37 remaining children / cost 2,658. The cost-61e and cost-61f alternative frontiers both show 38 / 2,721, so those receipts do not change this target. The bit-107 certificate therefore reduces this S5 target locally to **36 children / cost 2,593**.

The other three manifest parents of bit-107 are listed in the machine-readable output but are not counted as new: their status against the baseline solved set has not been recomputed. Thus the safe global statement after bit-107 is a lower bound of **at least 962 solved S6**, at most 6,885 remaining, and at most 542,227 total remaining edge cost (open-class bounds 5,155 / 405,950). The exact global frontier after bit-107 remains to be recomputed.

## cost-61f certificates

The three cost-61f certificates (bits 23, 26, 99) have 26,256 / 30,764 / 26,575 rows and 47 / 49 / 45 sub-roots. A separate exact integer determinant implementation independently confirms the corresponding roots are safe and have exactly 47 / 49 / 45 legal replies. This checks root geometry and mobility, not the strategy rows themselves.

The completed cost-61f sweep was 61/61: 11 WIN7-D10, 50 REFUTED-D10, 0 capped, 45,925,702 v16 nodes. The cost-65e sweep used v15. Neither raw verdict class is promoted to a proof without the certificate checks above.

## Reproduction and limits

- `scripts/audit_frontier_union_cost65e_bit107_20261115.py`
- `output/frontier-union-cost65e-bit107-audit-20261115.json`

The script independently re-enumerates both legal candidate sets, re-aggregates all raw batches, composes the three frontier sets, and checks the cost-65e / cost-61f root geometry and D4 parent lifts. The certificate strategy rows are not independently replayed by this script; it relies on the published verifier results for their 44/44, 47/49/45 sub-root checks.

K0783 still contains the earlier cost-56a/cost-58b and partial cost-63a narrative. It was not edited here because the local repository and locked uv environment were unavailable to regenerate the knowledge views required by AGENTS.md. This log is an audit record, not a replacement for updating that knowledge item and rebuilding generated views.

## Interpretation guard

The S6 coverage figures are not a solved S5 blocker or a two-stone result. Standard 11×11 empty root, `{49,60}`, S2 `{59,60}`, class 2 and class 4 remain **UNKNOWN**.
