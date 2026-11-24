---
id: K1305
title: "PG(2,9) の 5-キャップは 3 個の PGL(3,9) 軌道に分かれ、すべて Grundy 1"
kind: computation
status: computed
topics: [geometry, grundy, maximal-safe]
aliases:
- three orbits of five-caps in PG(2,9)
- all five-caps of PG(2,9) have Grundy 1
- frame stabilizer S4 orbit method
relations:
- type: related
  target: K1304
  note: 3-, 4-キャップは単一軌道（G=1, 0）。5-キャップは 3 軌道で全て G=1
- type: related
  target: K1303
  note: 完全アークの単一軌道分類と合わせた小キャップの軌道構造
- type: related
  target: K1300
  note: PG(2,9) のキャップ国勢調査（5-キャップ 14,859,936）
- type: related
  target: K1298
  note: パリティ特性定理と Grundy の自己同型不変性
artifacts:
- path: research/experiments/pg2q9-cap-game-20261125/report.md
  role: log
  note: 5-キャップ軌道と Grundy の総括
- path: research/experiments/pg2q9-cap-game-20261125/scripts/cap5_orbits_s4.py
  role: solver
  note: フレーム固定群 S4 の作用と軌道・Grundy の計算
- path: research/experiments/pg2q9-cap-game-20261125/output/cap5_orbits.json
  role: data
  note: 3 軌道のサイズ・固定群・代表・Grundy 値
scope: PG(2,9)（91 点、91 直線）上の 5-キャップ（どの直線とも高々 2 点）14,859,936 個と PGL(3,9) の作用、通常プレイ共演ゲームの Grundy 値。
evidence: 5-キャップ 14,859,936 = 2^5·3^6·7²·13 は |PGL(3,9)| = 42,456,960 = 2^7·3^6·5·7·13 を割り切れないので単一軌道ではない。すべての 5-キャップは 4-キャップ（単一軌道、K1304）を含み、4-キャップの固定群は S4（24 個の射影変換を GF(9) 上で構成）。固定フレーム {0,1,10,20} を含む 42 個の 5-キャップ上の S4 軌道はサイズ 24, 6, 12。軌道・固定群定理より PGL 軌道サイズは 1,769,040·s/5 = 8,491,392 / 2,122,848 / 4,245,696（合計 14,859,936、固定群の位数 5/20/10）。各軌道の代表 {0,1,10,20,31}, {0,1,10,20,41}, {0,1,10,20,42} のアップセット完全 DP（132/132/128 局面）で Grundy はすべて 1。Grundy は自己同型不変なので **全 5-キャップが Grundy 1**。
---

# PG(2,9) の 5-キャップの軌道と Grundy 値

## 結果

| S4 軌道サイズ | PGL 軌道サイズ | 固定群 | 代表 | Grundy |
|---:|---:|---:|---|---:|
| 24 | 8,491,392 | 5 | {0,1,10,20,31} | 1 |
| 12 | 4,245,696 | 10 | {0,1,10,20,42} | 1 |
| 6 | 2,122,848 | 20 | {0,1,10,20,41} | 1 |

- **5-キャップはちょうど 3 個の PGL(3,9) 軌道に分かれる**（合計 14,859,936）。
- **どの軌道の Grundy も 1** なので、**全 5-キャップが Grundy 1**。

## 方法（フレーム固定群 S4 の利用）

- 全 5-キャップは 4-キャップを含み、4-キャップは単一軌道（K1304）。
- 固定フレーム {0,1,10,20} の固定群は S4（GF(9) 上で 24 個の射影変換を構成）。
- フレームを含む 42 個の 5-キャップ上の S4 軌道（24, 6, 12）が PGL 軌道に対応。
  軌道・固定群定理より PGL 軌道サイズ = 1,769,040·s/5。
- 各軌道の代表のアップセット DP で Grundy を計算。

## 意味

- 3-, 4-, 5-キャップの全局面（110,565 + 1,769,040 + 14,859,936）の Grundy が
  orbit 不変性で厳密に確定: それぞれ 1, 0, 1。
- 全 PGL 軌道分解を 42 個の小対象の S4 軌道に落とす高速化は、より大きな盤への
  応用が期待できる。
