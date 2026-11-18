# 2026-11-18 N11 cost-16 parent rank-27 構造 preread

## 結果

31行のcost-16 parent `00000000000000003800000008001000` について、membership順位27位の7石rootを加えたときの新規組合せ構造を全数再導出した。

- rank-27 root: `00000000000100003820000008001000`
- 追加される被覆行: `{12,18}`
- rank-26 root: `00000000000000801202000000101002`、行 `{5,16}`
- rank-27 rootは行12を新規に覆い、既存上位26 rootのうち13本が行18を覆う（行18ハブの再出現）。

### 新規組合せ census

| 新規組合せ | b_only | zero | disjoint | 全数 |
|---|---:|---:|---:|---:|
| 2 root | 13 | 0 | 13 | 26 |
| 3 root | 201 | 86 | 38 | 325 |
| 4 root | 588 | 1,990 | 22 | 2,600 |
| 5 root | 309 | 14,641 | 0 | 14,950 |

分類は、いずれかの行が3回以上現れる、または2回現れる行が2本以上ならzero、2回現れる行がちょうど1本ならb_only、重複行がなければdisjointとした。

### quintの構造

新規b_only quintは309本。二重行の内訳は次のとおり。

| 二重行 | quint数 |
|---|---:|
| 18 | 233 |
| 15 | 38 |
| 19 | 38 |

**309本すべてについて、5個の4-subsetは b_only 3本・disjoint 2本・zero 0本**だった。k=26で確定した「b_only quintが3つのb_only quadと2つのdisjoint quadを持つ」構造が、k=27でもそのまま成立する。

新規disjoint quadは22本で、各4-rootの8つの被覆行はすべて相異なる。新規disjoint quintは0本。

## k=26回帰

同じ独立実装でk=26も再計算し、既刊k26 JSONの新規pair/quad、全triple/quint census、二重行ヒストグラムに一致した。k26の全quint censusは b_only 1,872 / zero 63,908 / disjoint 0、二重行は18:1,121、15:379、19:372。rank-26追加分のquintは b_only 1,872 / zero 10,778 / disjoint 0。

## 検査方法

- 固定入力: aggregate blob `31bdefdb2e2cc90b706cbb8090e98eb5eece4d87`、k26 result blob `1841a281ff604e7f677b8c7772a7312f6f9da5e1`
- 27 rootの行集合を入力から取得し、Mapによる行重複数分類と、行ごとのroot bitmask/popcount分類を全17,901組で照合
- k26は新規組合せと全C(26,3)/C(26,5)の全数を回帰照合
- 15項目すべてPASS

独立Python計算でも、同じ27個の行ペアからk26/k27の全census、二重行分布、309 quintの4-subset構造が一致した。公開した再現スクリプトは固定blob SHA-1を検査してから同じ計算を行う。なお、この実行では公開スクリプト自体をリポジトリcheckout上で起動してはいない。

## 次の計算に必要な項

k=27の完全な生存値を得るには、今回特定した新規項を実際に計算する必要がある。

- 22 disjoint quad: `j4_A` と `j4_B` の寄与
- 309 b_only quint: `j5_B` の寄与
- 14,641 zero quintは構造的ゼロとして計算値を持たせない

これはk=27の包含排除計算の準備であり、探索コスト・WIN/LOSS verdict・ゲーム理論的値ではない。長時間探索やPm計算は今回起動していない。

**標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4は引き続きUNKNOWN。**
