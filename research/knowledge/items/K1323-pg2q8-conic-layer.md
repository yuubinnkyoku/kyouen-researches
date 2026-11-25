---
id: K1323
title: "PG(2,8) の円錐曲線レイヤー — 各 k で単一 PGL(2,8) 軌道、Grundy は k mod 2"
kind: computation
status: computed
topics: [geometry, grundy, maximal-safe]
aliases:
- conic layer of PG(2,8)
- all k-subsets of a conic in PG(2,8) are equivalent
relations:
- type: related
  target: K1321
  note: PG(2,9) の円錐曲線レイヤー（k=4,5,6 で複数類があるのと対照的）
- type: related
  target: K1298
  note: パリティ特性定理（極大拡大がすべて偶数 → Grundy=(10−k) mod 2）
- type: related
  target: K1300
  note: PG(2,8) のキャップ・ゲーム（極大 6/10、両方偶数）
- type: related
  target: K1303
  note: 円錐曲線（9-キャップ）は単一軌道、固定群 PGL(2,8)
artifacts:
- path: research/experiments/pg2q8-cap-game-20261125/report.md
  role: log
  note: 円錐曲線レイヤーの節を含む総括
- path: research/experiments/pg2q8-cap-game-20261125/scripts/conic_layer_q8.py
  role: solver
  note: GF(8) 上の円錐曲線同定・パラメータ化・PGL(2,8) 軌道・アップセット DP
- path: research/experiments/pg2q8-cap-game-20261125/output/conic_layer_q8.json
  role: data
  note: k 別の軌道・代表・極大拡大サイズ・Grundy 値
scope: PG(2,8)（73 点、73 直線）の円錐曲線（9-キャップ）上の k-部分集合（k=3..8）がなすキャップと PGL(3,8)（円錐曲線上では PGL(2,8)）の作用、通常プレイ共演ゲームの Grundy 値。
evidence: 5-キャップ {10,16,29,47,48} を通る一意な非退化二次形式 Q = x²+3y²+4z²+4xy+5xz+7yz（行列 [[1,4,5],[4,3,7],[5,7,4]]、det=3）の零点 9 個を円錐曲線とする。円錐曲線は 32,704 = 8⁵−8² 個で単一軌道、固定群 PGL(2,8)（位数 504）。PGL(2,8) の 9 点上の k-部分集合への軌道は k=3..8 の各 k で単一（サイズ 84, 126, 126, 84, 36, 9 = C(9,k)）。各類代表のアップセット完全 DP で Grundy は 1, 0, 1, 0, 1, 0。極大拡大はすべて 6-キャップか 10-キャップ（hyperoval）で偶数なので、K1298 の定理より全 conic k-キャップで Grundy = k mod 2。アップセットは 8,450 / 646 / 66 / 16 / 8 / 4 局面。
---

# PG(2,8) の円錐曲線レイヤー

## 結果

| k | 1 円錐曲線あたりの類 | 類サイズ（=C(9,k)） | 極大拡大サイズ | Grundy |
|---:|---|---:|---|---:|
| 3 | 1 | 84 | 6, 10 | 1 |
| 4 | 1 | 126 | 6, 10 | 0 |
| 5 | 1 | 126 | 6, 10 | 1 |
| 6 | 1 | 84 | 10 | 0 |
| 7 | 1 | 36 | 10 | 1 |
| 8 | 1 | 9 | 10 | 0 |

- **PG(2,8) では各 k で円錐曲線上の k-部分集合は単一 PGL(2,8) 軌道**
  （PGL(2,9) で k=4,5,6 に複数類があったのと対照的）。
- 極大拡大はすべて偶数（6-キャップまたは hyperoval 10-キャップ）なので、
  K1298 の定理より **全 conic k-キャップで Grundy = k mod 2**。

## 方法

- GF(8)=GF(2)[x]/(x³+x+1) 上で 5-キャップを通る一意な非退化二次形式を求め、
  零点 9 個を円錐曲線とする。
- 円錐曲線を 1 点 P0 と P0 を通らない直線 L でパラメータ化（L の射影座標）。
- PGL(2,8) を PG(1,8) の 9 点に作用させ、k-部分集合の軌道を全数計算。
- 各類代表のアップセット完全 DP で Grundy と極大拡大サイズを計算。

## 意味

- q=8 の円錐曲線レイヤーは「各 k 単一軌道・パリティ一様」という最もきれいな形。
- q=9 との違い（k=4,5,6 の複数類、混在パリティ）は q の偶奇・群作用の違いを反映。
