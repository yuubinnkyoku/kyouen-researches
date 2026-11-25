> **研究履歴**：本文の判定・数値・計画は記録時点のものです。現在の結論・未解決・検証境界の唯一の正本は[knowledge](../../knowledge/README.md)です。この資料を現在知識の正本として並行更新しません。

# Cycle 15 verification — independent Python recompute

Script: inline TargetSearch via `../../experiments/structural-discovery/scripts/cycle8_exists_k.py` + `build_triples(7)`.
Quads n=7 = 6364 (matches).

| claim | method | result |
|---|---|---|
| max on mandatory skeleton (forbid center,(0,3),(2,3),(2,2)) @14 | target DFS | **unsat** (1,046,567 nodes) |
| skeleton @13 exists | target DFS | **found** witness |
| M∪{center} forbid B∪(2,2) @14 | target DFS forced center | **found** |

Agrees with COMPLETE C++ maxima in `CYCLE15_CAPACITY_DECOMPOSITION.md`
(skeleton max=13; M+center max=14 with 8 sets).

## Skeleton K=13 witness (Python)

Cells: (0,0),(1,0),(2,0),(2,1),(3,1),(6,1),(5,2),(6,2),(1,4),(0,5),(0,6),(4,6),(6,6)
— all in mandatory orbits; no center / no (0,3)/(2,3)/(2,2).
