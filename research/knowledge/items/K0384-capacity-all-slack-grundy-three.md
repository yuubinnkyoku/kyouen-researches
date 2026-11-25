---
id: K0384
title: 全容量余裕の容量占有ゲームにおけるGrundy値の一様上界
kind: proposition
status: proved
topics:
- variants
- grundy
aliases: []
relations:
- type: generalizes
  target: K0358
  note: 余裕1のGrundy分類を任意の余裕へ拡張
artifacts:
- path: research/experiments/capacity-all-slack-20261010/README.md
  role: proof
  note: 全称の二重帰納、可換菱形補題、有限検証範囲
- path: research/experiments/capacity-all-slack-20261010/verify.py
  role: verifier
  note: 署名再帰と独立全列mexの422953局面照合
- path: research/experiments/capacity-all-slack-20261010/check_kernel.py
  role: verifier
  note: 別の上位核で337625形の偶奇余裕上界を照合
scope: 抽象容量占有ゲームの全1≤h<w,m≥1,r≥0、全安全局面。K0352の幾何条件を満たすd次元平行列盤にも適用。
evidence: 可換菱形と余裕・下位残量の二重帰納による全称数学的証明、2方式の有限検証
---

# 全容量余裕の一様Grundy上界3

`x_1≥...≥x_w`、`sum_{i≤h}x_i≤r` の容量占有ゲームで、`sigma=r−sum_{i≤h}x_i` とする。任意の安全局面について

- **sigma偶数**なら `g(x)∈{0,1}`。
- **sigma奇数**なら `g(x)∈{0,1,2,3}`。

よって **任意のh,w,m,rでg≤3**。奇数余裕の2/3は既存K0358の例で達成され、定数3は鋭い。`hm≤r` の自明領域は全列独立の偶奇式で含める。

証明は、上位h列の形`u`と下位残量`R`に分解し、偶数余裕のGrundyを`(R+theta(u)) mod2`、奇数余裕を`(R+a+1) mod2`または`2+(R mod2)`と分類する二重帰納。偶数余裕の異なる上位子が両方0/1を出すことは、上位二手の**可換菱形**（共通の二手後形）と奇数余裕署名の定義に矛盾する。全詳細はproof artifact。

署名を用いて上位形だけから全Grundyを厳密計算できる。有限検算は独立mexとの422,953局面照合、別の上位核との337,625形照合。有限検算と全称証明を区別する。

K0352にあった一般h≥4の`g≤3`未証明という限界は解消した。**標準2次元正方形盤のGrundyにこの容量上界を移してはならない**（K0352の幾何的容量縮約条件が必要）。
