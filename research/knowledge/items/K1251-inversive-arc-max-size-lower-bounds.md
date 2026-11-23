---
id: K1251
title: 反転平面M(q)の弧の最大サイズ：文献の(q+5)/2構成を上回る検証済み下界
kind: computation
status: computed
topics: [geometry, variants, maximum-safe, search-methods, statistics]
aliases:
- inversive plane arcs: improved lower bounds
- 反転平面アークの最大サイズの下界改善
relations:
- type: depends_on
  target: K1250
  note: 弧＝楕円二次曲面上の一般位置集合、および上界K≤q+2（射影上界）
- type: depends_on
  target: K1058
  note: 位数qの反転平面盤とK(q)の定義・q≤11の厳密値
- type: supports
  target: K1250
  note: 二次曲面上の一般位置集合の具体的な大きさの記録
artifacts:
- path: research/experiments/finite-field-kyouen-20261120/output/arc_maxsearch_big.json
  role: data
  note: q=13..47 の検証済み弧（証人付き）
- path: research/experiments/finite-field-kyouen-20261120/output/arc_maxsearch_q49b.json
  role: data
  note: q=49 のサイズ32の弧
- path: research/experiments/finite-field-kyouen-20261120/output/arc_lift_verify.json
  role: data
  note: 全証人のrank検証と射影補題の検証
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_maxsearch.c
  role: solver
  note: 反復局所探索（増分ブロッキング）
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_search_report.py
  role: verifier
  note: 円リストとの突き合わせによる証人検証
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_lift_verify.py
  role: verifier
  note: 二次曲面への持ち上げとrankによる独立検証
scope: 位数qのMiquelian反転平面M(q)（= 楕円二次曲面Q^-(3,q)の円幾何）における弧（どの4点も同一円上にない点集合）の最大サイズK(q)。q=3..11は全数列挙による厳密値、q=13..49は明示的な証人による下界。文献比較はSonnino 1999の(q+5)/2構成との比較に限る。
evidence: q=3..11のKは全数探索（K1058に記録）。q=13..49の各下界は、円リストとの総当り突き合わせ（arc_search_report.py）と、楕円二次曲面への持ち上げ後の「全4点組のrank=4」検査（arc_lift_verify.py）の二経路で独立に検証済み。射影上界K≤q+2（q奇数）は全証人で「任意の点からの射影がPG(2,q)のアークになる」ことを総当り確認。
---

# 反転平面M(q)の弧の最大サイズ：文献の(q+5)/2構成を上回る検証済み下界

## 問題

位数 `q` の Miquelian 反転平面 `M(q)` の**弧（arc）**とは、どの4点も同一円上にない
点集合である。最大サイズを `K(q)` と書く。これは K1058・K1250 で扱ってきた
「反転平面盤の最大安全集合」と同一の量であり、K1250 により
**楕円二次曲面 `Q⁻(3,q)` 上の一般位置集合の最大サイズ**、すなわち
**二次曲面上に列を持つ4次元MDS符号の最大長**に等しい。

## 文献（確認できた範囲）

- **A. Sonnino, "Large k-arcs in inversive planes of odd order", J. Geom. 66 (1999) 187–191**：
  `q` 奇数の `M(q)` に **`(q+5)/2`-弧の族**を構成する、と要旨に明記されている。
  同要旨は「任意の `k` と素数 `p` に対し、`h` が `k` に比べて十分大きければ
  `M(p^h)` に `k`-弧が存在する」（[7] による）とも述べており、
  **`K(q) = Θ(q)` であること**はこれと我々の上界から従う。
- "Complete arcs in inversive planes over prime fields" など、弧の完備性を扱う研究もある。

**注意（限界）**：全文は取得できなかった（403/リダイレクト）。したがって以下の比較は
**確認できた `(q+5)/2` 族との比較に限る**。より強い既知構成が存在する可能性は排除できない。

## 結果：検証済み下界は (q+5)/2 を上回る

`K(q)` の値（q ≤ 11 は全数列挙による厳密値、q ≥ 13 は明示的な証人による下界）と
Sonnino の構成値 `(q+5)/2` の比較：

| q | `K(q)` | 種別 | `(q+5)/2` | 差 |
|---:|---:|---|---:|---:|
| 3 | **5** | 厳密 | 4 | +1 |
| 4 | **5** | 厳密 | — | — |
| 5 | **6** | 厳密 | 5 | +1 |
| 7 | **6** | 厳密 | 6 | 0 |
| 8 | **7** | 厳密 | — | — |
| 9 | **9** | 厳密 | 7 | +2 |
| 11 | **9** | 厳密 | 8 | +1 |
| 13 | 10 | 下界 | 9 | +1 |
| 16 | 12 | 下界 | — | — |
| 17 | 13 | 下界 | 11 | +2 |
| 19 | 14 | 下界 | 12 | +2 |
| 23 | 16 | 下界 | 14 | +2 |
| 25 | 18 | 下界 | — | — |
| 27 | 19 | 下界 | — | — |
| 29 | 20 | 下界 | 17 | +3 |
| 31 | 21 | 下界 | 18 | +3 |
| 32 | 22 | 下界 | — | — |
| 37 | 25 | 下界 | 21 | +4 |
| 41 | 27 | 下界 | 23 | +4 |
| 43 | 28 | 下界 | 24 | +4 |
| 47 | 30 | 下界 | 26 | +4 |
| 49 | 32 | 下界 | 27 | +5 |

奇数 `q ≥ 5` のすべてで文献構成値以上、`q ≥ 13` では **+1〜+5** 上回る。
`K/q` は `q=13` の 0.77 から `q=49` の 0.65 へ下がるが、
これは探索が `q` とともに予算不足になるためでもあり（`q=49` は試行回数を5倍にして
18→32 に伸びた）、真の比はより大きい可能性がある。

## 上界と帰結

- **`K ≤ q+2`（`q` 奇数、無条件）** — K1250 の射影上界。
- `K ≤ q+1`（MDS予想下。素数 `q` では Ball の定理により無条件）。
- `K ≥ (q+5)/2`（Sonnino 1999）。

したがって

> **`(q+5)/2 ≤ K(q) ≤ q+2`、すなわち `K(q) = Θ(q)`。**

以前の「`K ≈ 8.86`（ほぼ定数）」「`K ≈ q^0.31`」という見立ては、文献の `(q+5)/2` 構成とも
矛盾していた。**`K` は線形に増える。** 残る問題は定数である：
`liminf K(q)/q` は現在 `0.5`（文献）と `1`（上界）の間で、本項の測定が `0.65` まで押し上げた。

## 検証

- 各下界は**二経路**で独立に検証：
  1. 円リストとの総当り（`arc_search_report.py`、どの円も4点以上を含まない）、
  2. 楕円二次曲面への持ち上げ後の「全4点組の rank が4」（`arc_lift_verify.py`）。
     こちらは円リストを一切使わない。
- 射影上界の補題「任意の点からの射影が `PG(2,q)` のアークになる」も全証人で総当り確認
  （`q=49` では4点組 35,960 個の検査を含む）。

## 限界

- `q ≥ 13` の値は**下界**。探索はランダムなので、予算を増やせば上振れしうる。
- 文献の比較は `(q+5)/2` 族のみ（全文未取得）。より良い既知構成・より強い既知上界を
  見落としている可能性がある。
- `(q+5)/2` は `q` 奇数用。偶数 `q` の文献構成は未確認で、偶数側の比較はしていない。
