---
id: K1254
title: 非Miquelian反転平面（Suzuki–Tits）：弧は位数8で同じ7・位数32でより小さく、ゲームは勝敗が逆
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
- path: research/experiments/finite-field-kyouen-20261120/scripts/tits_build.py
  role: solver
  note: 一般の q=2^(2e+1) 用の Tits 反転平面構成（q=8,32 で検証）
- path: research/experiments/finite-field-kyouen-20261120/output/circles_tits_q32.txt
  role: data
  note: Suzuki–Tits 位数32 反転平面の 1,025 点 32,800 円
- path: research/experiments/finite-field-kyouen-20261120/output/grundy_tits_q8.txt
  role: data
  note: Suzuki–Tits 位数8 の完全 Grundy 計算の生出力（ROOT 0 0 = 後手勝ち）
- path: research/experiments/finite-field-kyouen-20261120/scripts/ag_board_export.py
  role: solver
  note: AG(2,q) 盤をアーク・センサス形式で書き出す
- path: research/experiments/finite-field-kyouen-20261120/output/grundy_ag_q8.txt
  role: data
  note: AG(2,8) 盤の完全 Grundy（ROOT 0 1 = 後手勝ち）
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
- 位数32の結果：`K(Tits) ≈ 14` に対し `K(Miquelian) ≥ 22`（同上の比較表）。

## 位数32（`q = 2^5`）での拡張：非Miquelian 盤はずっと制約が強い

同じ構成（`σ = 2^{e+1} = 8`）を `q = 32` で実行（`scripts/tits_build.py`、一般の `q` 用）：

```
q=32: Tits ovoid 1,025 点、円 32,800 = q(q²+1) ✓
      3-設計検証：全 524,800 対がちょうど 33 = (v−2)/(k−2) 個の円に載る ✓
```

**弧の探索**（同じ探索器・同じ予算で比較）：

| 盤 | 手法 | 結果 |
|---|---|---|
| **Suzuki–Tits(32)** | ILS（150試行×3000反復） | 13 |
| **Suzuki–Tits(32)** | ILS（500試行×4000反復） | **14** |
| Suzuki–Tits(32) | スワップ探索 k=15, 16, 20, 22 | すべて失敗（罰則 24, 33, 92, 136） |
| **Miquelian(32)** | ILS（150試行×3000反復） | **22** |

> **非Miquelian 盤ではずっと小さい**：位数32で `K(Tits) ≈ 14` に対し `K(Miquelian) ≥ 22`。
> 位数8では両者とも 7 で一致していたので、これは位数が上がって初めて現れる差である。

**解釈**：Miquelian 盤の大きな弧は「楕円二次曲面上の一般位置集合」という代数構造に支えられている
（K1250/K1252）。Tits ovoid は二次曲面ではないのでその構造が使えず、弧が小さくなる。
両盤は同じ `3-(1025,33,1)` 設計（パラメータ同一）なので、**設計のパラメータだけでは
弧の大きさは決まらない**ことがはっきりした。

上界は両盤とも ambient の `m(3,q) = q+1 = 33`（K1252）で、Tits 側には 19 の slack がある
（Miquelian 側は 11）。非Miquelian 盤で `K ≤ q` に相当する上界をどう示すかは未解決。

## ゲーム（共円ゲーム）は両盤で勝敗が逆になる

同じ位数8の2つの反転平面で、**共円ゲームの完全な Grundy 計算**（`grundy_full128.c`、
空盤から到達可能な全安全局面を列挙）を行った。

| 盤 | 安全局面数 | 空盤の Grundy 値 | 勝敗 |
|---|---:|---:|---|
| **Miquelian(8)** | 15,665,794 | **1** | **先手勝ち** |
| **Suzuki–Tits(8)** | 15,694,914 | **0** | **後手勝ち** |

> **最大弧サイズは両盤とも 7 なのに、空盤の勝敗は逆**。

- 安全局面数の差 `15,694,914 − 15,665,794 = 29,120` は、7-アーク数の差
  （`1,077,440 − 1,048,320 = 29,120`）と完全に一致する ✓（k ≤ 6 の層は両盤で同一）。
- したがって **ゲームの勝敗は 3-(65,9,1) という設計パラメータでは決まらず**、円の配置
  （＝ Miquelian か否か）に依存する。Miquelian 盤の「先手勝ち」は K1253 の系列
  （q=3,5,8 が先手勝ち、q=7,9 が後手勝ち）の一部だが、同じ位数8でも円配置が変わると
  後手勝ちになる例がここで初めて出た。
- K1253 の解析（3重推移性による `g0 = mex{g1}` の還元、4点局面の拡大の Grundy 値が鍵）
  は設計のパラメータだけを使わないので、この違いを原理的に扱える枠組みである。

**データ**：`output/grundy_tits_q8.txt`（`SAFE 15694914`, `ROOT 0 0`, `SIZE` 行）。

### 位数8の3つの盤の比較

同じ位数8で、別の構造を持つ盤も計算した（AG(2,q) 盤＝4点共線と4点共円をブロック、
`scripts/ag_board_export.py` で書き出し）。

| 盤 | 点 | ブロック | 安全局面数 | 空盤の Grundy 値 | 勝敗 |
|---|---:|---:|---:|---:|---|
| Miquelian 反転平面 | 65 | 520 | 15,665,794 | **1** | **先手勝ち** |
| Suzuki–Tits 反転平面 | 65 | 520 | 15,694,914 | **0** | **後手勝ち** |
| AG(2,8) 盤 | 64 | 548 | 10,892,513 | **0** | **後手勝ち** |

**3つの盤のうち先手勝ちは Miquelian 反転平面だけ**。Miquelian と Suzuki–Tits は
同じ `3-(65,9,1)` 設計パラメータを持ち、最大弧サイズも同じ 7 なのに勝敗が逆で、
ゲームの勝敗が**設計のパラメータではなく円の配置で決まる**ことがはっきりした。
（AG 盤は3-設計ですらない別のハイパーグラフなので、後手勝ちなのは独立な情報。）

**どの段で差が付くか**：K1253 の枠組み（3重推移性による還元）を3盤で使うと、
小さい局面の代表値（点番号 `{0}`, `{0,1}`, `{0,1,2}` の Grundy 値）が

| 盤 | `g₃`（3点局面） | `g₂` | `g₁` | `g₀` | 勝敗 |
|---|---:|---:|---:|---:|---|
| Miquelian(8) | **0** | 1 | 0 | 1 | 先手 |
| Suzuki–Tits(8) | **2** | 0 | 1 | 0 | 後手 |
| AG(2,8) | **1** | 0 | 1 | 0 | 後手 |

となり、差は**3点局面の Grundy 値**（0 / 2 / 1）に現れる。Miquelian 盤は
`PΓL(2,q²)` が鋭く3重推移的なので3点局面は単一軌道で値が1つに決まるが、
Suzuki–Tits 盤（Suzuki 群 `Sz(q)` は2重推移的だが3重推移的でない）と AG 盤では
3点局面が複数軌道に分かれ、代表の取り方で値が変わりうる。ただし全体の `g₀` は
（1点局面が推移的なので）代表値から決まる。

完全な Grundy 分布（`GRUNDY` 行）：

| 盤 | 値0 | 値1 | 値2 | 値3 |
|---|---:|---:|---:|---:|
| Miquelian(8) | 5,355,233 | 6,379,361 | 3,931,200 | — |
| Suzuki–Tits(8) | 6,067,777 | 5,193,617 | 4,324,320 | 109,200 |
| AG(2,8) | 6,808,257 | 3,481,920 | 602,336 | — |

Suzuki–Tits 盤だけ Grundy 値 3 が現れる（109,200 局面）のも特徴的である。

## 限界

- ovoid の座標形の同定は `q=8` の全数（指数の総当り）による。一般の `q = 2^{2e+1}` では
  `σ = 2^{e+1}` の古典形を使えばよいが、本項では `q=8` のみ構成・検証した。
- 弧の計算は厳密（アーク・センサスが全アークを列挙）。ただし `K` の値はこの盤に固有の
  計算結果であり、一般の非Miquelian 盤への拡張は未検討。

## 付記：AG(2,8) 盤の最大弧は 8

AG 盤のアーク・センサス（同じプログラム）で層サイズが

```
1:64  2:2016  3:41664  4:551936  5:3813376  6:6422528  7:57344  8:3584  9:0
```

となり、**`K(AG(2,8)) = 8`**（8-アーク 3,584 個、9-アークなし）。K1058 の AG 表の
値 8 がアーク・センサスで独立に確認できた。反転平面（Miquelian）の `K(8) = 7` より
1 大きいが、AG 盤は禁止集合族が異なる（`K1058` §10co・本項目の円族比較）ので矛盾しない。
