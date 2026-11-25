# N11 class2 cost-69b raw sweep audit (2026-11-14)

Latest main at audit start: `bb1de7077a49a611b8494b12892eb63203bc4d68`.

Read `AGENTS.md`, `research/knowledge/README.md`, K0023, K0105, K0329, the cost-69a/cost-69b lane logs, the cost-69b summary JSON, and all five raw JSONL files named by that summary.

## Independent candidate-set check

Target S6 child: `00000000000000809082000000400000`.

- Occupied cells (0-based): `[22, 49, 55, 60, 63, 71]`.
- All 15 existing four-stone subsets have nonzero exact Bareiss determinant; the six-stone parent is safe.
- Re-enumerating every empty cell with exact 4x4 Bareiss determinants gives **46 blocked / 69 legal** seventh-stone candidates.
- The union of candidate bits in committed raw batches A-D is **exactly equal** to this independently re-derived 69-element set: 69 records, 69 distinct bits, no missing or extra candidate.

## Raw batch accounting

| Raw file | Candidate rows | pilot_d6 rows |
|---|---:|---:|
| batch A | 6 | 1 |
| batch B | 18 | 1 |
| batch C | 18 | 1 |
| batch D | 27 | 1 |
| **Total** | **69** | **4** |

All 69 candidate rows have `loss=false`, `capped=false`, and `andclose=true`. Their node counts sum to **305,754,861**, exactly matching the summary JSON. The union terminal range is [13,17]; bit 75 alone has [15,17], while every other candidate has [13,17].

## Determinism check

The separate rerun file contains bits 68, 119, and 41. Each matches the original candidate record exactly on `loss`, `capped`, and node count:

| Bit | Original nodes | Rerun nodes |
|---:|---:|---:|
| 68 | 15,565,883 | 15,565,883 |
| 119 | 11,048,413 | 11,048,413 |
| 41 | 10,780,096 | 10,780,096 |

The rerun sum is 37,394,392, equal to the sum of those three original records.

## Provenance gap

The summary JSON reports `pilot_d6_controls: 5`, and the sweep log says the control passed in all five batch invocations. However, the five committed raw files contain only **four** pilot records: one in each of batches A-D and none in the three-row determinism rerun. The log explains that batch B was accidentally executed twice and the pushed batch-B file is the deduplicated copy. The fifth invocation's pilot line is therefore not present in the committed raw set and cannot be independently checked from the listed artifacts. This does not affect the 69 candidate records, their exact candidate-set coverage, or the candidate-node sum; it narrows only the reproducibility claim for the fifth pilot control.

## Interpretation boundary

The runner's own output contract defines `loss=true` as a WIN7-within-depth candidate, while `loss=false && !capped` means only that no such win was found within the depth limit. Thus these 69 rows are not game-theoretic LOSS proofs for the S6 child, its S5 parent, either two-stone root, or the empty board. The sterile sweep contributes no new WIN7 certificate and no frontier cover.

K0023 and K0105 remain unchanged: the standard 11x11 empty-board winner is **UNKNOWN**. The two-stone roots {49,60} and {59,60}, and the class-2 blocker, also remain UNKNOWN.
