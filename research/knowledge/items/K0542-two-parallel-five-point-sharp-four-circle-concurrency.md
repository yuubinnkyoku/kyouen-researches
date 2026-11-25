---
id: K0542
title: 二平行線の各2〜5指定点を二点ずつ通る線外一点共通円の最大数を鋭く分類できる
kind: proposition
status: proved
topics: [geometry, variants, certificates]
aliases: []
relations: []
artifacts:
- path: research/experiments/two-parallel-five-point-concurrency-20261024/proof.md
  role: proof
  note: 五円のC5共有構造から黄金比型へ帰着し負の線間距離二乗で全称排除、四円明示例
- path: research/experiments/two-parallel-five-point-concurrency-20261024/verify.py
  role: verifier
  note: 標準ライブラリの有理係数多項式による16恒等式の独立展開と改変拒否
- path: research/experiments/two-parallel-five-point-concurrency-20261024/witness.cpp
  role: verifier
  note: 全点整数の鋭さの例を含む2例を独立整数演算し候補9円・6円のうち4円ずつが通ることを確認
- path: research/experiments/two-parallel-five-point-concurrency-20261024/audit.json
  role: data
  note: 恒等式・改変拒否・相異なる四円の係数組と全16サイズの達成例の検査receipt
scope: 相異なる二本の平行直線の各線に高々5個の異なる実数位置の指定点、両線上にない一点P、Pと各線の指定点2点ずつを通る異なる実円。
evidence: 五円の接続等号条件と二つの三次式の恒等式による全称証明。上限4の実現例を厳密有理数・整数計算で独立確認。
---

# 二平行線・各5点以下の共通点円は高々4本で鋭い

二本の平行線それぞれに高々5点を指定する。両線の外の一点Pを通り、各線の指定点を2点ずつ通る円は高々4本。
同和弦energyへの条件は不要であり、4本を実現する配置がある。

指定点数nB,nCが各2〜5の場合の正確な最大数は次の表となる。
上限個数としても、ちょうどその指定点数としても同じ。全欄を整数座標で実現できる。

|nB＼nC|2|3|4|5|
|---|---:|---:|---:|---:|
|2|1|1|1|1|
|3|1|1|2|2|
|4|1|2|2|3|
|5|1|2|3|4|

五円があるなら両線の共有点グラフは互いに補となるC5。
弦和から一方の高さを他方の一次式で表し、二つの小行列式だけでα²−α−1=0の型へ帰着する。
全円を通る点が要求する線間距離の二乗は
`−(α+1)[z²+(α−1)z+1]`。
α+1=α²>0、括弧内は平方に(α²+1)/4を足したものなので常に負となり、五円を排除する。

鋭さの整数例：x=0に高さ{−20,−10,0,5,20}、x=10に{−15,−10,−5,0,10}。
整数点P=(12,−4)は相異なる4円を共有する。別途、同和弦energy6・線間隔√71の例もある。
小さい点数の上界は共有円対数の凸性で証明し、この一つの整数例の部分集合だけで全16欄の下界を達成する。

各線6指定点以上への拡張は主張しない。K0541で用いるE≥13の場合の3円上界とは範囲が異なり、
無条件に3円へ強めることはこの明示例により不可能。
