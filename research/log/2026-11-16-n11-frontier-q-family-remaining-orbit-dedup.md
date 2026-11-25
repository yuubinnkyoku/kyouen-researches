# n11 frontier: Q family remaining-root orbit dedup and 9-pair candidate cover (2026-11-16)

The newest main already contains the Q full-family and P full-family orbit measurements. Their full-family percentages do not determine the work actually left in the current frontier. The remaining subsets give a sharper answer.

## Result

The cheapest any-class own-closable parent is Q, class 1:

- S5 parent 00000000000000821082000000000000
- 18 remaining S6 rows, 1,238 survival candidates
- all 18 rows unswept; zero engine WIN7, zero engine REFUTED-D10, zero transferred REFUTED-D10
- exact D4 dedup: **687 root orbits**, removing 551 repeated candidate occurrences (**44.507%**)

Every Q root orbit has one or two S6-row owners (136 single, 551 double). The row-overlap graph has 152/153 edges. An exact maximum-weight matching gives nine disjoint row pairs, each with four shared root options: 36 alternatives in total. One primary root per pair gives a 9-root candidate cover of all 18 rows. This is the minimum possible candidate-cover size because no root has more than two Q-row owners; it is not a claim that any of those roots is WIN7.

## Why Q takes priority over P

P is the best own-closable class-2 parent, but its exact remaining subset is 24 rows / 1,704 candidates → 1,468 D4 roots, only 13.850% internal dedup. Q is smaller before dedup and substantially smaller after dedup.

The new Q set is disjoint from P and all four current top-family candidate sets. P has 14 overlaps with those top families; the top families have two internal overlaps. Across Q, P, and the four top families, 5,673 candidate occurrences become 4,482 unique root orbits (20.994% fewer).

This refines the full-family observations in commits be91d324 (Q) and 665cc6e1 (P): Q's remaining-subset saving is 44.507%; P's is 13.850%. Full-family rates should not be substituted for remaining-subset rates.

## Artifacts

- `research/experiments/n11-frontier-q-family-orbit-dedup-20261116/verify.py`: stdlib verifier; exact Bareiss 4×4 determinant, D4 canonicalization, row-by-row cost controls, maximum-weight matching.
- `output/q-family-canonical-root-worklist.csv`: 687 canonical roots with owner mappings and seed priority.
- `output/q-family-pair-cover-seed.csv`: 36 alternatives across nine matched row pairs; nine marked primary.
- `output/cross-family-overlaps.csv`: 16 cross-family shared root orbits.
- `output/audit.json`: pinned inputs and all controls.

## Next action

Prioritize Q's 687-root canonical worklist. Search the nine primary roots first only as an initial probe; if a primary is REFUTED-D10, continue with its three alternatives and then the remaining shared/single-owner roots. Keep per-family seen-orbit tables; Q needs no global cache interaction with the current P/top4 set.

No long engine job was started in this run. This was a deterministic structural audit only. No WIN/LOSS verdict or certificate was produced.

**Q, P, S2 {59,60}, and the standard 11×11 empty board remain UNKNOWN.**
