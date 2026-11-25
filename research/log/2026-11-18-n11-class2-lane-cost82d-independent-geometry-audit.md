# n11 class2-lane cost82d: independent geometry recheck

Date: 2026-11-18

## Result

An independent Python implementation using the 24-term Leibniz expansion of the exact integer determinant of rows `[x²+y², x, y, 1]` re-enumerated the survival moves of S6 child `00000000020000003800000080000800` (stones 11, 31, 59, 60, 61, 89).

- The six-stone parent is safe: no forbidden four-subset among its 15 four-subsets.
- All 20 triples of the six stones were checked against all 115 empty cells.
- Derived legal survival candidates: **82**, exactly equal to the published claim list; missing 0, extra 0.
- The parent has only the identity D4 stabilizer; all 82 seven-stone child roots have distinct D4 canonical forms. No symmetry-based reduction is available within this candidate row.
- The 17 confirmation-root D4 canons independently match the census-v18 transfer map **17/17**.
- Determinant controls pass for a cocircular square, four collinear points, and a nonzero-determinant control.

The implementation is independent of the repository's Bareiss-based `legal_candidates.py` and of the v17 search engine. Reproduction script and JSON are published alongside this log.

## Interpretation boundary

The completed v17 sweep (separate raw-batch audit) reports 0 WIN7-D10, 82 REFUTED-D10, 0 capped. This geometry audit does not re-run that search. `REFUTED-D10` is not a LOSS proof.

The cost82d child is a historical STERILE reference in K0865's head-1410 census: its S5 parent has 18 historical STERILE S6 rows. The v17 sweep therefore revalidates an existing prediction; it does not add a new S6 row, reduce the frontier, close an S5 parent, or change the manifest head. By K0863, a STERILE row cannot be covered by a depth-10 WIN7 receipt, but this is not a game-theoretic LOSS statement.

The standard 11×11 empty board, two-stone roots `{49,60}` and `{59,60}`, S2 `{59,60}`, and classes 1/2/4 remain UNKNOWN.
