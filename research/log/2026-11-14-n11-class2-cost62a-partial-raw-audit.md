# n11 class2-lane cost-62a: partial raw sweep audit (32/62)

Audit base: `main` = `483fc4b53a5b871181b420cb8ff32cca8c6e5095`.

The current class2/class4 claims, the cost-62a claim JSON, and raw batches 1–4 were checked against the 62-bit candidate list in the claim.

## Raw-record reconciliation

- Claimed legal candidates: 62
- Published raw candidates: 32 across batches 1–4
- Distinct candidate bits: 32
- Duplicate bits: 0
- Unexpected bits: 0
- Not yet present in raw batches: 30
- Pilot controls: 4; all `loss=false`, uncapped, exactly 5,949 nodes
- Candidate nodes: **108,012,447**
- Candidate rows: all uncapped, all terminal ranges [13,17]

The four WIN7-D10 search candidates are:

| bit | 7-stone root | nodes |
|---:|---|---:|
| 1 | `00000000000000809102000001000002` | 11,849,776 |
| 11 | `00000000000000809102000001000800` | 2,557,437 |
| 32 | `00000000000000809102000101000000` | 7,975,993 |
| 66 | `00000000000000849102000001000000` | 3,444,804 |

Here `loss=true` means the 7th-stone player has a depth-10 win in the runner's WIN7 orientation. These are search verdicts, not yet independent certificate verifications.

## Root and symmetry checks

Each of the four 7-stone roots was independently checked with the exact integer 3x3 determinant form of the cocircularity test:

- 7 stones per root
- 35 four-point subsets per root
- 0 zero determinants in every root
- minimum absolute determinant 6

All 62 legal candidate roots were also canonicalized under the eight D4 transformations of the 11x11 square. The 62 canonical keys are all distinct, so none of the four WIN7 candidates can be merged with another candidate by board symmetry.

## Interpretation and next work

The target S5 is `00000000000000809102000000000000` (40 remaining S6 orbits, total seventh-move edge cost 2,850). Its cost-62 child is `00000000000000809102000001000000`. The first 32 of its 62 legal seventh moves have now been searched; 30 remain.

The four WIN7 candidates need full strategy extraction and independent certificate verification before their S6 parents can be credited as secured. Until then, they do not close the target S5 or any two-stone root.

These batches were produced by the v15 runner, whose claim records the 5,949-node pilot. The v16 unsigned-key repair was added later as a separate runner to avoid mixing in-flight v15 data with new node counts. The v15 memo-key defect disables transposition reuse for roots carrying a high bit in a 32-bit word; it does not turn a completed uncapped search into a proof of LOSS or change the meaning of `loss=true`. Do not merge v16 batches into this v15 claim.

The earlier best class2 S5 `00000000000000809082000000000000` remains receipt-unclosable within the WIN7-D10 receipt framework, not proven LOSS. The current cost-62a target is the next coverable class2 target.

## Status

No certificate body has yet been added for these four roots. The cost-62a sweep remains **in flight** at 32/62 candidates. Standard 11x11 empty root, two-stone root `{49,60}`, S2 `{59,60}`, class 2, and class 4 remain **UNKNOWN**.
