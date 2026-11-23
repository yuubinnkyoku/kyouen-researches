---
id: K1254
title: 非Miquelian反転平面（Suzuki–Tits 位数8）の弧：最大値は Miquelian と同じ7
kind: proposition
status: proved
topics: [geometry, variants, maximum-safe]
aliases:
- Suzuki–Tits inversive plane arcs
- arcs in the non-Miquelian inversive plane of order 8
relations:
- type: related
  target: K1251
  note: Miquelian 側の同じ位数の値 K(8)=7 との比較
- type: depends_on
  target: K1250
  note: 反転平面＝3-(q²+1,q+1,1) 設計の弧という見方
artifacts:
- path: research/experiments/finite-field-kyouen-20261120/scripts/tits_ovoid_exponents.py
  role: solver
  note: PG(3,8) の Tits ovoid の座標形の同定（f = x^4+xy+y^6）
- path: research/experiments/finite-field-kyouen-20261120/scripts/tits_inversive_export.py
  role: solver
  note: Tits ovoid から 3-(65,9,1) 設計を構成し円リストを出力
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_census.c
  role: solver
  note: アーク・センサス（層サイズと K の厳密決定）
- path: research/experiments/finite-field-kyouen-20261120/output/circles_tits_q8.txt
  role: data
  note: Suzuki–Tits 位数8 反転平面の 65 点 520 円
- path: research/experiments/finite-field-kyouen-20261120/output/arc_census_tits_q8.txt
  role: data
  note: Suzuki–Tits 位数8 のアーク・センサス生出力（層サイズと K=7）
- path: research/experiments/finite-field-kyouen-20261120/scripts/tits_ovoid_search.py
  role: solver
  note: Tits ovoid の座標形の候補探索（3次以下。不発の記録）
scope: 位数8のSuzuki–Tits反転平面（Tits ovoid から作られる非Miquelian反転平面）の弧（どの4点も同一円上にない点集合）の最大サイズ
evidence: Tits ovoid O = {(1, x^4+xy+y^6, x, y)} ∪ {(0,1,0,0)} を F_8 上で構成し、全直線が2点以下（0本の違反）・平面上の9点切断が520個・全 C(65,3) 三点点が円上にちょうど1回（43,680/43,680）を機械確認。その後アーク・センサスを深さ10まで走らせ、層サイズと K を厳密に決定。
---

# 非Miquelian反転平面（Suzuki–Tits 位数8）の弧

## 構成

偶数位数の反転平面はすべて egglike（Dembowski）：`PG(3,q)` の ovoid の平面切断が円。
`q = 8` では ovoid は2種類ある：

- **楕円二次曲面**（Miquelian 反転平面 `M(8)`、円は平面切断）— K1058/K1250 の盤
- **Tits ovoid**（偶数の ovoid は `q = 2^{2e+1}` のときのみ非二次曲面が存在。`q = 2^3` が最小）
  `O = {(1, x^σ + xy + y^{σ+2}, x, y) : x,y ∈ F_8} ∪ {(0,1,0,0)}`, `σ = 4`（= x^4 + xy + y^6）

Tits ovoid から作られる **Suzuki–Tits 反転平面**は `3-(65,9,1)` 設計で、円は平面上の
9点切断 520 個（`= q(q²+1)`）。

**構成の機械検証**（`scripts/tits_inversive_export.py`）：

| 検証 | 結果 |
|---|---|
| ovoid の点数 | 65 = q²+1 ✓ |
| 全 4,745 直線が2点以下 | 違反 0 ✓ |
| 9点平面切断の個数 | 520 = q(q²+1) ✓ |
| 三点点の被覆 | `C(65,3) = 43,680` をちょうど1回ずつ ✓（3-設計公理） |

## 結果：最大弧サイズは 7（Miquelian と同じ）

アーク・センサス（アークのみを DFS で列挙）を深さ10まで実行（15,694,914 ノード、約20秒）：

```
k : #k-arcs
1 : 65
2 : 2,080
3 : 43,680
4 : 611,520          ( C(65,4) − 520·C(9,4) = 611,520 と一致 )
5 : 4,525,248
6 : 9,434,880
7 : 1,077,440
8 : 0                ← 8-アークは存在しない
```

> **`K(Suzuki–Tits, 8) = 7`**

**Miquelian 盤での値 `K(8) = 7`（K1058・全数列挙で厳密）と同じ**である。ただし 7-アークの
個数は異なる：Suzuki–Tits が **1,077,440**、Miquelian が **1,048,320**（`+29,120 = 2.78%`）。
層サイズも k ≤ 6 では両盤で一致し、k=7 で初めて差が出る。

## 位置づけ

- 反転平面の弧は Miquelian 盤（楕円二次曲面上の一般位置集合）でしか研究されていない
  （文献調査は K1251）。**非Miquelian 盤の弧の計算は本項が最初**。
- K1252 の上界 `K ≤ q` の証明は `Q⁻` が二次曲面であることを使うので **この盤には適用できない**。
  一方「弧＝`PG(3,q)` の n-アーク」という見方は任意の ovoid で成り立つので、
  ambient の `m(3,q) = q+1`（Casse–Glynn）から **`K ≤ q+1`** は無条件に成り立つ。
  位数8では `7 ≤ 9` で、まだ slack がある。
- 次の問い：Suzuki–Tits 位数32（`q = 2^5`、次に存在する位数）でも `K = 7` に対応する値
  （＝Miquelian の下界と同程度）になるか。全数列挙は不可（1025 点）なので探索になる。

## 限界

- ovoid の座標形の同定は `q=8` の全数（指数の総当り）による。一般の `q = 2^{2e+1}` では
  `σ = 2^{e+1}` の古典形を使えばよいが、本項では `q=8` のみ構成・検証した。
- 弧の計算は厳密（アーク・センサスが全アークを列挙）。ただし `K` の値はこの盤に固有の
  計算結果であり、一般の非Miquelian 盤への拡張は未検討。
