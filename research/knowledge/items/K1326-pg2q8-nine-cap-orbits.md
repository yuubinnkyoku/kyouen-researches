---
id: K1326
title: "PG(2,8) の 9-キャップは 2 個の PGL(3,8) 軌道（conic 32,704 / 非 conic 294,336）"
kind: computation
status: computed
topics: [geometry, maximum-safe]
aliases:
- two orbits of nine-caps in PG(2,8)
- non-conic nine-caps of PG(2,8) form one orbit
relations:
- type: related
  target: K1300
  note: PG(2,8) のキャップ国勢調査（9-キャップ 327,040、円錐曲線 32,704）
- type: related
  target: K1323
  note: 円錐曲線レイヤー（conic 9-キャップは単一軌道）
- type: related
  target: K1324
  note: 極大キャップ（6 と 10）の軌道分類
artifacts:
- path: research/experiments/pg2q8-cap-game-20261125/report.md
  role: log
  note: 9-キャップ軌道の節を含む総括
- path: research/experiments/pg2q9-cap-game-20261125/scripts/orbit_bfs.c
  role: solver
  note: 128-bit マスクの軌道 BFS
- path: research/experiments/pg2q8-cap-game-20261125/output/orbits9.txt
  role: data
  note: conic / 非 conic 9-キャップの軌道サイズと固定群
- path: research/experiments/pg2q8-cap-game-20261125/output/starts9.txt
  role: data
  note: 非 conic 9-キャップの開始マスク
scope: PG(2,8)（73 点、73 直線）上の 9-キャップ（どの直線とも高々 2 点の 9 点集合）327,040 個と PGL(3,8) の作用。
evidence: 9-キャップは 327,040 個（K1300 の国勢調査）。このうち円錐曲線（非退化二次形式の零点）は 32,704 = 8⁵−8² 個で単一軌道（固定群 PGL(2,8) = 504、K1323）。非 conic 9-キャップの例 {2,3,10,12,21,45,47,50,52} はキャップで、9 点すべてを通る二次形式が零形式のみ（conic でない）。PGL(3,8) 生成元 8 個（K1324 の gens.txt）による軌道 BFS で軌道サイズ 294,336 = 327,040 − 32,704（全非 conic 9-キャップ）→ **非 conic 9-キャップは単一軌道**（固定群 16,482,816/294,336 = 56）。よって 9-キャップはちょうど 2 軌道。付記として、極大 6-キャップの 3 類は外部点の secant 本数分布（{1:36, 2:24, 3:7}、nucleus 0）が一致し、この不変量では分離できない。**独立検証（5/5 PASS）** では盤の完全一致、非 conic 9-キャップの rank 6・kernel 0、37,449 個の二次形式の全列挙（32,704 conic）、独自生成元・Schreier 鎖で |PGL(3,8)| = 16,482,816、軌道 294,336（固定群 56）と 32,704（固定群 504）の集合的一致、独立 DFS 国勢調査（9-キャップ 327,040）を確認。**構造的対応** として、10-キャップ 32,704 個は「conic + その唯一の非割線点（nucleus）」で、conic ↔ 10-キャップは全単射。各 10-キャップの 10 個の 9-部分集合がちょうど全 9-キャップ 327,040 個を与え、非 conic 9-キャップは「hyperoval から conic 点を 1 個除いたもの」= 9 × 32,704 = 294,336。各非 conic 9-キャップは一意に 10-キャップへ延長でき、極大でない。
---

# PG(2,8) の 9-キャップは 2 軌道

## 結果

| 9-キャップ | 個数 | 軌道 | 固定群 |
|---|---:|---|---:|
| conic | 32,704 | 1 軌道 | 504 |
| 非 conic | 294,336 | 1 軌道 | 56 |

- 9-キャップ 327,040 = conic 32,704 + 非 conic 294,336。
- 非 conic 9-キャップは単一 PGL(3,8) 軌道（例 {2,3,10,12,21,45,47,50,52} の軌道が全個数と一致）。
- 付記: 極大 6-キャップ 3 類は secant 本数分布では区別できない（より細かい不変量が必要）。

## 方法

- 非 conic 9-キャップを 1 個取り、PGL(3,8) 生成元 8 個で軌道 BFS（128-bit マスク）。
- 軌道サイズを国勢調査の非 conic 個数と比較。
