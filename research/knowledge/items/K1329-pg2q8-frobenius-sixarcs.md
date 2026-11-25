---
id: K1329
title: "PG(2,8) の極大 6-キャップ 3 類は Frobenius で巡回置換され、PΓL(3,8) で単一軌道"
kind: computation
status: computed
topics: [geometry, maximum-safe]
aliases:
- Frobenius cyclically permutes the three classes of complete 6-arcs in PG(2,8)
- PGammaL(3,8) is transitive on maximal 6-caps
relations:
- type: related
  target: K1324
  note: 極大 6-キャップが PGL(3,8) の 3 軌道（各 686,784）に分かれる
- type: related
  target: K1327
  note: 全キャップ軌道分類。3 類は局所不変量で区別できなかった
- type: related
  target: K1323
  note: PG(2,8) の円錐曲線・極大キャップの構造
artifacts:
- path: research/experiments/pg2q8-cap-game-20261125/output/frob_probes.txt
  role: data
  note: Frobenius 像と 3 代表のマスク
- path: research/experiments/pg2q9-cap-game-20261125/scripts/orbit_bfs.c
  role: solver
  note: probe 機能付きの軌道 BFS
- path: research/log/2026-11-26-pg2q8-frobenius-sixarcs.md
  role: log
  note: 巡回置換の発見と検証の記録
scope: PG(2,8)（73 点、73 直線）上の極大 6-キャップ 2,060,352 個。PGL(3,8) の 3 軌道と Frobenius 自己同型（PΓL(3,8)）の作用。
evidence: PGL(3,8) の 3 軌道の代表を A={10,47,49,55,61,64}, B={17,27,30,44,52,70}, C={8,48,50,51,58,61} とする。Frobenius φ(x,y,z)=(x²,y²,z²) を座標に適用すると φ(A)={10,28,31,59,65,67}, φ²(A)={10,29,33,37,43,46}。probe 付き軌道 BFS で φ(A) は C の PGL 軌道に、φ²(A) は B の PGL 軌道に属することを確認（φ³=id より φ(C)∈B, φ(B)∈A）。よって Frobenius は 3 類を A→C→B→A と巡回置換し、**PΓL(3,8) は極大 6-キャップ全体（2,060,352）に推移的**（PΓL 位数 3·16,482,816 = 49,448,448、固定群 24）。3 類が secant/tangent/external 統計・固定群作用で一致したのは、それらが半線型同値だからである。
---

# Frobenius による 6-アーク 3 類の巡回置換

## 結果

- PGL(3,8) の 3 軌道 A, B, C（各 686,784）は、Frobenius 自己同型
  `φ: (x,y,z) ↦ (x²,y²,z²)` により **A → C → B → A** と巡回置換される。
- したがって **PΓL(3,8) = PGL(3,8) ⋊ C3 は極大 6-キャップ 2,060,352 個に推移的**
  （単一 PΓL 軌道、固定群 24）。
- 3 類が secant/tangent/external 統計・固定群の平面作用で一致していたのは、
  それらが **半線型同値**（Frobenius で移り合う）だからである。

## 方法

- 3 代表 A, B, C と φ(A), φ²(A) の 128-bit マスクを作る。
- probe 付き軌道 BFS で、φ(A) が C の軌道に、φ²(A) が B の軌道に属することを確認。
- φ³ = id より残りも従う。
