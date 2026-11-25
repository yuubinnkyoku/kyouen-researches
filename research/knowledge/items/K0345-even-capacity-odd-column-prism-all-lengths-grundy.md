---
id: K0345
title: 偶数ペア容量・奇数列の三次元盤は任意長で全Grundy閉公式を持つ
kind: proposition
status: proved
topics: [variants, geometry, grundy]
aliases: []
relations:
- type: depends_on
  target: K0340
  note: 三次元平行列の安全性を全ペア容量へ縮約する
- type: generalizes
  target: K0341
  note: 偶数r長盤の空盤Grundy0を任意長・全安全局面の閉公式へ強化する
artifacts:
- path: research/experiments/prism-followup-20261005/even-capacity-proof.md
  role: proof
  note: 候補値への各合法手がxor1/2/3となる全称mex証明
- path: research/experiments/prism-followup-20261005/even_capacity_verify.py
  role: verifier
  note: 独立ラベル付き全状態mexと共有占有数DP、適用外反例の監査
- path: research/experiments/prism-followup-20261005/even-capacity-output.json
  role: data
  note: 明示パラメータの完全有限検算。全称命題の根拠は証明artifact
scope: 奇数w≥3、偶数r≥2、任意の共通列長m≥1の全ペア容量占有ゲーム。三次元幾何への移送にはq=r+1>2wと底面の非共線条件を要する。
evidence: 全称mex証明と独立ラベル付き占有数の有限完全検算。
---

# 偶数ペア容量・奇数列の全長Grundy閉公式

K0340の三次元平行列変種で、wが奇数、qが奇数、q>2w、任意のm≥1とする。
r=q−1、c=r−mとし、安全集合の列占有数xを降順に見て最大をa、二番目をb
（重複込み）とすると、

```
b<c:    g(x)=(Σx+m) mod2.
b≥c:    g(x)=2((a−b) mod2)+((Σx−a) mod2).
```

より一般に、これは任意の奇数w≥3・偶数r≥2・m≥1について
全ペア条件x_i+x_j≤rを満たす抽象占有ゲームの全称式である。
b≥c領域では合法手が候補値のxor1/2/3へ移り、候補値未満の全値へ常に移れる。
b<c領域では列端に達するまでの偶奇候補を使い、領域境界を含むmexを証明した。
有限検算からの外挿ではない。

空盤はm<rならGrundy m mod2、m≥rならGrundy0。
従って空盤勝敗・Grundyの真の安定化長は正確にr=q−1である。
幾何条件の下ではr=2k≥2w≥6となり、m≤kでは全Grundy0/1、m≥k+1では
最大Grundy値が正確に3。後者の存在証人は
(k,k−1,k−2,k−1,...,k−1)である。全式により任意長で上限3を持つ。

m≥rでは後半だけになり、rとmが式から消える。
K0341の奇数r長盤公式と合わせて、奇数列の三次元長盤の全Grundyは
容量の両偶奇で閉公式となる。

ラベル付き列の独立完全mexと既存ソート占有数DPを別々に照合した。
保存した有限検算は実装確認であり、無界主張の根拠は上記全称mex証明である。
偶数列数、奇数容量には適用外反例を保存した。
二次元標準盤のGrundy上限と11×11勝敗はこの式の対象外である。
