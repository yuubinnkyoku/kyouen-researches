---
id: K1324
title: "PG(2,8) の極大キャップの軌道 — hyperoval は単一軌道、極大 6-キャップは 3 軌道"
kind: computation
status: computed
topics: [geometry, maximal-safe]
aliases:
- PGL(3,8) orbits of maximal caps in PG(2,8)
- three classes of complete 6-arcs in PG(2,8)
- hyperovals of PG(2,8) form one orbit
relations:
- type: related
  target: K1323
  note: 円錐曲線レイヤー（conic k-キャップは各 k 単一軌道）と合わせた PG(2,8) の構造
- type: related
  target: K1300
  note: PG(2,8) のキャップ国勢調査（極大 6 は 2,060,352、10 は 32,704）
- type: related
  target: K1303
  note: PG(2,9) では完全アークがサイズごとに単一軌道だったのと対照的
artifacts:
- path: research/experiments/pg2q8-cap-game-20261125/report.md
  role: log
  note: 極大キャップ軌道の節を含む総括
- path: research/experiments/pg2q9-cap-game-20261125/scripts/orbit_bfs.c
  role: solver
  note: 128-bit マスクの軌道 BFS（probe 機能付き）
- path: research/experiments/pg2q8-cap-game-20261125/output/orbits_maximal.txt
  role: data
  note: hyperoval 単一軌道・極大 6-キャップ 3 軌道の結果
- path: research/experiments/pg2q8-cap-game-20261125/output/gens.txt
  role: data
  note: PGL(3,8) の生成元 8 個（73 点の置換）
scope: PG(2,8)（73 点、73 直線）上の極大キャップ（完全アーク）はサイズ 6 の 2,060,352 個と hyperoval（サイズ 10）32,704 個、および PGL(3,8) の作用。
evidence: GF(8)=GF(2)[x]/(x³+x+1) 上の PGL(3,8) 生成元 8 個（transvection・対角・座標置換）を 73 点の置換として構成。軌道 BFS（128-bit マスク）で、hyperoval {0,5,13,18,27,38,46,53,59,66} の軌道は 32,704 = 全 10-キャップ（単一軌道、固定群 504）。極大 6-キャップ {10,47,49,55,61,64} の軌道は 686,784。ランダムな極大 6-キャップ 4 個の軌道もすべて 686,784。probe 検査で 2 個は orbit1 に含まれ、2 個は含まれない → 少なくとも 2 軌道。全極大 6-キャップ数 2,060,352 = 3×686,784 なので、**ちょうど 3 軌道（各 686,784、固定群 24）**。|PGL(3,8)| = 16,482,816 = 686,784·24 = 32,704·504。
---

# PG(2,8) の極大キャップの軌道

## 結果

| 極大キャップ | 個数 | 軌道 | 固定群 |
|---|---:|---|---:|
| hyperoval (10) | 32,704 | **1 軌道**（32,704） | 504 |
| 6-キャップ | 2,060,352 | **3 軌道**（各 686,784） | 24 |

- hyperoval は PGL(3,8) の単一軌道。
- **極大 6-キャップは 3 個の軌道に分かれる**（各 686,784）。
  全個数 2,060,352 = 3×686,784 と、probe で 2 軌道以上を確認したことから、
  ちょうど 3 軌道。
- |PGL(3,8)| = 16,482,816 = 686,784·24 = 32,704·504。

## 方法

- GF(8) 上で PGL(3,8) の生成元 8 個を 73 点の置換として構成。
- 極大キャップを 1 個取り、128-bit マスクの軌道 BFS で軌道サイズを計算。
- 複数のランダム極大 6-キャップの軌道サイズと、orbit1 への probe 所属で軌道数を確認。

## 意味

- PG(2,9) では完全アークがサイズごとに単一軌道だったが、PG(2,8) の極大 6-キャップは
  3 類に分かれる（完全 6-アークの 3 型）。
- 円錐曲線レイヤー（K1323）と合わせ、PG(2,8) のキャップ構造の全体像に近づいた。
