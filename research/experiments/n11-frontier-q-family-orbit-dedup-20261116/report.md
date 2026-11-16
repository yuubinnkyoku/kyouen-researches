# Q family remaining S6→S7 D4 orbit dedup

## Target

Q parent: 00000000000000821082000000000000

The post-cost65j frontier ranking identifies Q as a class-1 own-closable S5 parent with 18 remaining S6 rows and 1,238 legal S6→S7 survival candidates. All 18 rows remain unswept; existing engine verdicts and transferred REFUTED-D10 counts are zero.

## Exact reduction

- 1,238 candidate occurrences reduce to **687 distinct D4 root orbits**.
- **551 duplicate occurrences are removed (44.507%)**.
- Every root orbit has either one or two Q-row owners: 136 single-owner roots and 551 two-owner roots.
- No S6 row has an intra-row D4 collision; all duplication is between different S6 rows.

The Q overlap graph has 152 of 153 possible row pairs. An exact maximum-weight perfect matching pairs all 18 rows into 9 pairs, each with four shared root orbits. The 9 primary roots form a minimum-size candidate cover; 27 additional roots are recorded as alternatives. If all nine primary roots were later proved WIN7-D10, they would cover all 18 rows. They are currently untested.

## Target comparison

| Family | Remaining S6 rows | Candidate occurrences | Unique D4 roots | Redundant | Reduction |
|---|---:|---:|---:|---:|---:|
| Q, class 1 | 18 | 1,238 | 687 | 551 | 44.507% |
| P, class 2 | 24 | 1,704 | 1,468 | 236 | 13.850% |
| class4 | 18 | 1,460 | 1,170 | 290 | 19.863% |
| audit-blocked | 10 | 698 | 613 | 85 | 12.178% |
| best-coverable | 3 | 209 | 206 | 3 | 1.435% |
| second-coverable | 5 | 364 | 354 | 10 | 2.747% |

Q has no candidate-root orbit overlap with P or the four coordinator top families. P overlaps the top families in 14 roots; the top four families have two internal cross-family overlaps. Across all six families, 5,673 candidate occurrences reduce to 4,482 unique D4 root orbits (20.994%).

The earlier full-family duplication percentages must not be applied directly to the remaining worklist: P's exact remaining subset saves 13.850%, while Q's saves 44.507%.

## Method and boundary

The audit reads the pinned head-1410 S6 worklist and the post-cost65j ranking/closability records. It independently re-enumerates survival candidates with exact integer determinants and canonicalizes every seven-stone root under all eight D4 symmetries. The candidate counts match the published edge costs row by row.

This is a search-plan reduction only. No engine search was run, no WIN7/REFUTED-D10 verdict was added, and no certificate was created. Q, P, S2 {59,60}, and the empty 11×11 board remain UNKNOWN.
