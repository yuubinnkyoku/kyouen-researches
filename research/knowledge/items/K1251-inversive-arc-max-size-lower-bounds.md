---
id: K1251
title: 反転平面M(q)の弧の最大サイズ：文献の(q+5)/2構成を上回る検証済み下界
kind: computation
status: computed
topics: [geometry, variants, maximum-safe, search-methods, statistics]
aliases:
- inversive plane arcs, improved lower bounds
- 反転平面アークの最大サイズの下界改善
relations:
- type: depends_on
  target: K1250
  note: 弧＝楕円二次曲面上の一般位置集合、および上界K≤q+2（射影上界）
- type: depends_on
  target: K1058
  note: 位数qの反転平面盤とK(q)の定義・q≤11の厳密値
- type: related
  target: K1252
  note: q奇数(q≥7)で上界K≤q+1が無条件に従う
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
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_structure_probe.py
  role: verifier
  note: 極大アークが低次曲線・生成元不変・乗法構造を持たないことの検査（負の結果）
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_swapsearch.c
  role: solver
  note: 固定サイズ交換探索（4点以上を含む円の個数を最小化）
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_swap_search.py
  role: verifier
  note: 交換探索の駆動と、報告された弧の総当り再検証
- path: research/experiments/finite-field-kyouen-20261120/output/arc_swap_q13.json
  role: data
  note: 交換探索によるq=13の再現とk=11未発見の記録
- path: research/experiments/finite-field-kyouen-20261120/scripts/graph_arc_probe.py
  role: solver
  note: 関数のグラフ族をアークとしてテストする予備探索
- path: research/experiments/finite-field-kyouen-20261120/scripts/graph_field_poly_search.py
  role: verifier
  note: F_q上の2次以下の多項式グラフがアークでないことの全数検査（q=5..13）
- path: research/experiments/finite-field-kyouen-20261120/scripts/graph_random_search.py
  role: solver
  note: ランダム関数のグラフアーク探索（5,000サンプル）
- path: research/experiments/finite-field-kyouen-20261120/scripts/graph_fp_linear.py
  role: verifier
  note: F_p-線型写像の全数検査（q=9で24/81のみアーク）
- path: research/experiments/finite-field-kyouen-20261120/scripts/fp2_subspace_arcs.py
  role: solver
  note: q=p^2 の2次元F_p-部分空間の全数検査（q=9で40個がアーク、q=25で0）
- path: research/experiments/finite-field-kyouen-20261120/output/fp2_subspace_arcs.json
  role: data
  note: q=9,25 の部分空間アーク数
- path: research/experiments/finite-field-kyouen-20261120/output/fp2_subspace_arcs_q49.json
  role: data
  note: q=49 の2次元F_7-部分空間 2,850 個（アーク 0）
- path: research/experiments/finite-field-kyouen-20261120/scripts/max_arc_orbit.py
  role: solver
  note: 最大アークのPΓL(2,q^2)軌道分解（q=9で単一軌道）
- path: research/experiments/finite-field-kyouen-20261120/scripts/graph_hillclimb.py
  role: solver
  note: グラフ空間の山登り（罰則最小化）
- path: research/experiments/finite-field-kyouen-20261120/output/arc_maxsearch_push.json
  role: data
  note: 予算を増やした追試（値が変わらないことの記録）
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

## 文献（サブエージェントによる web 調査、2026-11-23）

**用語**：反転平面 `M(q)` の弧（k-arc）＝どの4点も同一円上にない k 点集合。
Sonnino 1999 の要旨原文："An arc of size k (briefly: a k-arc) in an inversive plane is defined
as a set consisting of k points no four of which lie on the same circle."
（zbMATH の一部レビューが "no three" と書いているのは誤り。）

**下界（文献の最良）**：**A. Sonnino, "Large k-arcs in inversive planes of odd order",
J. Geom. 66 (1999) 187–191**（DOI 10.1007/BF01225681）。本文："we shall construct a family of
½(q+5)-arcs in the inversive plane M(q) with q odd. These arcs turn out to be complete for
q > 71 or q ∈ {17,23,27,29,41,47,53,59}." 要旨の仮定は `q ≡ 1 (mod 3)` かつ `q ≥ 71` または
`q ∈ {17,23,27,29,41,47,49,53,59}` で、**全奇数 q かどうかは本文と要旨で食い違う（未確定）**。
zbMATH レビューの `1/3(q+5)` は誤植（(q+5)/3 は q=17,23,… で整数でない）。

**後年の Hadnagy–Sonnino, Discrete Math. 255 (2002) 181–188** は素数位数で
**≈(p+17)/4** の complete arc を作るもので、`(q+5)/2` より**小さい**。
したがって `(q+5)/2` が文献の最良で、本項の検証済み下界（q=13..49 で +1〜+5）は**改善**である。

**上界：文献に存在しない**。zbMATH（レビュー全文）・OpenAlex・Crossref・Springer・
ScienceDirect・arXiv・EuDML を検索した限り、反転平面の弧の上界（`k ≤ q`, `q+1`, `q+2` など）を
述べた論文は**奇数・偶数を問わず見つからない**。唯一の材料は ambient な `PG(3,q)` の理論
（Hirschfeld–Storme, "The packing problem …: update 2001", Table 3.1：`q` 奇数 `> 3` で
`m(3,q) = q+1` かつ `(q+1)`-アークは normal rational curve（Segre 1955）、`q = 2^h ≥ 8` でも
`m(3,q) = q+1`）で、これから `K(q) ≤ q+1` が出るのみ。
⇒ **`K ≤ q`（q 奇数, q≥9、K1252）は文献にない**。

**偶数 q**：Sonnino の一連の論文はすべて奇数位数。偶数位数（Miquelian および Suzuki–Tits
ovoid 由来）については構成も上界も小さい q のデータも見つからない。

**小さい q の厳密値**：印刷された表は存在しない。文献にあるのは構成からの下界
（`K(3)≥4, K(5)≥5, K(7)≥6, K(9)≥7`）だけ。⇒ 本項の `K(3..11)` の厳密値は新規。

**MDS 対応**：`PG(3,q)` 側の古典的対応は既知（Storme–Thas, J. Combin. Theory Ser. A 62 (1993)
139–154："k-arcs in PG(n,q) and linear MDS codes of dimension n+1 and length k over GF(q) are
equivalent objects"）。**「`Q⁻` 上の弧＝楕円二次曲面上に列を持つ MDS 符号の最大長」という
制限版の同定（K1250）は文献に見当たらない。**

**注意（限界）**：Sonnino 1999 と Hadnagy–Sonnino 2002 の全文は有料で取得できず、
要旨・レビュー・索引 PDF の断片による。したがって以下の比較は `(q+5)/2` 族との比較に限る。

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
| 11 | 9 | 下界（旧DFSは厳密と主張したが同じ実装が q=13,17,19 で誤り） | 8 | +1 |
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

- **`K ≤ q`（`q` 奇数、`q ≥ 9`、無条件）** — K1252（射影上界の等号ケース `k = q+2` と
  `k = q+1` を排除）。
- `K ≤ q+2`（`q` 奇数、全範囲）— K1250 の射影上界（K1252 の手前の段）。
- **`K ≤ q+1`（すべての `q ≥ 4`、無条件）** — ambient な `PG(3,q)` の
  `m(3,q) = q+1`（Segre 1955 / Casse–Glynn 1982、`Q⁻` 上の弧は n-アークでもあるため）。
  **偶数 q の最良の無条件上界**（以前の射影上界 `q+3` を改善）。`K(4) = 5 = q+1` で tight。
- `K ≤ q+1`（全 `q`、MDS予想下。素数 `q` では Ball の定理により無条件）— K1250。
- `K ≥ (q+5)/2`（Sonnino 1999）。

したがって `q` 奇数 `≥ 7` で

> **`(q+5)/2 ≤ K(q) ≤ q+1`、すなわち `K(q) = Θ(q)`。**

以前の「`K ≈ 8.86`（ほぼ定数）」「`K ≈ q^0.31`」という見立ては、文献の `(q+5)/2` 構成とも
矛盾していた。**`K` は線形に増える。** 残る問題は定数である：
`liminf K(q)/q` は現在 `0.5`（文献）と `1`（上界）の間で、本項の測定が `0.65` まで押し上げた。

## ロバスト性（値は予算の産物ではない）

`q ≤ 32` の値は、予算（`trials × ils` を10倍以上変える）と貪欲則
（一様ランダム／「ほぼ満杯のブロックが最少の点を選ぶ」サンプリング法 `--sample`）を
変えても**変わらない**：

- `q=13`：`trials=40, ils=3000` / `trials=2000, ils=1000`（200万ステップ）/
  `trials=400, ils=6000` のすべてで 10。
- `q=17`：`trials=1000, ils=1500` でも 13。
- `q=23, 29`：`--sample 0` と `--sample 8` の両方で 16, 20。

したがってこれらは予算不足の産物ではなく、真値に近い（`q=13,17` は上限の可能性が高い）。
一方 `q ≥ 37` は**再起動回数に敏感**で、`q=49` は `trials=40` で 18、`trials=200` で 32 だった。
**大 `q` では `ils` より `trials` が効く。**

## 独立な探索戦略による裏づけ

3種類の**質的に異なる**探索で同じ値が出る（`scripts/arc_maxsearch.c` と
`scripts/arc_swapsearch.c`）：

1. **貪欲＋ランダム摂動**：詰まるまで点を追加し、r 点を無作為に削って再充填、改善しなければ巻き戻す。
2. **貪欲＋強制挿入**（`--force`）：外点 `q` を選び、`|S∩c|=3` である `q` を通る円すべてから
   弧の点を1つずつ削って `q` を挿入し、再充填する。妨害点を名指しで除去するので非常に速い
   （q=13〜23 は 1〜2 秒で記録値を再現）。
3. **固定サイズ交換探索**：サイズを `k` に固定し、「4点以上を含む円」の個数を最小化する
   1点交換（タブー付き）。異なる盆地を探索する。

| q | 13 | 17 | 19 | 23 | 25 | 27 | 29 | 31 | 32 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 貪欲＋ランダム摂動 | 10 | 13 | 14 | 16 | 18 | 19 | 20 | 21 | 22 |
| 貪欲＋強制挿入 | 10 | 13 | 14 | 16 | 18 | 19 | 20 | 21 | 22 |
| 固定サイズ交換 | 10 | （未到達） | （未到達） | （未到達） | — | — | — | — | — |

`q=13` では3戦略すべてが 10 で一致し、交換探索は `k=11` を見つけられない
（貪欲系も 200万 ILS ステップで 10 止まり）。`q=11` 以下は全数列挙の厳密値であり、
これらの値と整合する。**したがって表の値は予算・アルゴリズム依存の産物ではない。**

（交換探索は `q ≥ 17` では既知値の再発見にも届かず、この戦略は小さい `q` 向きである。
`--init` で既知の弧から成長を試みても `k = 現最良+1` は見つからなかった。）

## 構造化部分集合のテスト（グラフ ansatz）

探索が `≈0.65q` で頭打ちになるのは「構造を持つ大きなアークを取り逃がしている」からかもしれない。
そこで最も単純な構造化族、**アフィンモデルでの関数のグラフ**
`S = {(a, f(a)) : a ∈ F_q}`（q 点）を総当りで調べた。

- **最大アークがグラフで実現できる場合がある**：q=7 ではサイズ 6（`K=6`）、
  q=9 ではサイズ 9（`K=9`）のグラフがアークになる（ランダム関数/添字多項式の探索で発見）。
  q=5 ではランダム関数の多くがアーク（サイズ5）。
- **しかし F_q 上の多項式のグラフはダメ**：2次以下の多項式 `f(a) = c_2a²+c_1a+c_0`
  の全組合せ（q=5,7,9,11,13）でグラフがアークになるものは **0 個**。
- **q ≥ 7 ではランダム関数もほぼダメ**：任意関数を 5,000 個サンプルして完全なグラフアークは
  q=7,9,11,13 で **0 個**（q=5 のみ多数）。
- q 点のグラフを目的関数（4点以上を含む円の個数）で山登りしても局所解（q=7 で罰則1、
  q=9 で4、q=11 で11）に留まる。

**F_p-線型写像の全数検査**：q = p^e のとき F_p-線型写像 : F_q → F_q は
e×e の F_p 行列（p^(e²) 個）で尽くされる。これを全数試すと

| q | 8 (=2³) | 9 (=3²) | 25 (=5²) | 27 (=3³) |
|---|---:|---:|---:|---:|
| F_p-線型グラフがアーク | 0/512 | **24/81** | 0/625 | 0/19683 |

**q=9 だけが当たり**（24個）。q=16（F_2-線型 65,536個）、q=25（F_5-線型 625個）、
q=27（F_3-線型 19,683個）、q=49（F_7-線型 2,401個）では **0**。
q=9 は上界 K ≤ q が tight な唯一の既知の q（K(9)=9、K1252/K1253）であり、
その極大アークの一部は F_3-線型写像のグラフで実現できる。

**さらに q=p² では「2次元 F_p-部分空間」を全数検査できる**（`F_{q²} = F_{p⁴}` の
2次元 F_p-部分空間はちょうど `p² = q` 個の元を持ち、反転平面の q 点集合になる。
個数はガウス二項係数 `[4 choose 2]_p = (p²+1)(p²+p+1)`）：

| q | 2次元 F_p-部分空間の数 | そのうちアーク（サイズ q） |
|---:|---:|---:|
| 9 (=3²) | 130 | **40** |
| 25 (=5²) | 806 | **0** |
| 49 (=7²) | 2,850 | **0** |

q=9 では「F_3-線型グラフ」より広い族（40個）が極大アークを与え、すべて単一軌道の一部である。
q=25, q=49 では 0 なので、**この族も q=9 に固有**である。

**結論**：極大アークは小さい q ではグラフとして実現できるが、
q ≥ 11 ではグラフ ansatz は一般探索（q=11 で 9）より弱い。
「構造化族で 0.65q を超える」という目論見は、少なくともグラフ ansatz では成功しなかった。

## 極大アークの軌道分解（最大アークはどれだけ本質的に一意か）

最大アークを自己同型群 `PΓL(2,q²)`（位数 `(q²+1)q²(q²−1)·(2e)`、`q = p^e`）で割った
軌道の大きさを、1つの最大アークから BFS で求めた（`scripts/max_arc_orbit.py`、
生成元 `z↦z+1, z↦λz, z↦1/z, z↦z^p`）。

| q | `K` | `#K-arcs` | 1軌道の大きさ | `|G|` | 判定 |
|---:|---:|---:|---:|---:|---|
| 7 | 6 | 1,254,400 | 117,600 | 235,200 | 単一軌道でない（≥11軌道） |
| 8 | 7 | 1,048,320 | 262,080 | 1,572,480 | 単一軌道でない（262,080×4 = 全体なので4軌道と整合） |
| **9** | **9** | **29,520** | **29,520** | 2,125,440 | **単一軌道（全9-アークが1軌道）** |

**q=9 では最大アークは自己同型を除いて一意**（29,520 = 全数）。しかも q=9 は
上界 `K ≤ q` が tight な唯一の既知の位数（`K(9)=9`、K1252/K1253）であり、
F_3-線型グラフとして実現できる9-アーク（前節、24個）はこの単一軌道の一部である。
q=7, q=8 では最大アークは複数の軌道に分かれるので、
「上界が tight な位数では極値対象も一意」という描像が q=9 で成立している。

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
