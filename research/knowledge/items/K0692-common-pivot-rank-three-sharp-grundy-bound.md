---
id: K0692
title: 全残余辺が一点を共有するrank三以下のゲームは辺数無制限でもGrundy3以下
kind: proposition
status: proved
topics: [grundy, residual-games, geometry, variants]
aliases: []
relations:
- type: depends_on
  target: K0002
  note: mexとGrundyの定義
- type: depends_on
  target: K0108
  note: 全残余族と自由点のxor分離
- type: depends_on
  target: K0683
  note: rank三以下の達成例を指定有限整数点盤に移す
- type: depends_on
  target: K0686
  note: 純三点でg2とg3に必要な最少点数の下界
- type: depends_on
  target: K0687
  note: 純三点のg2とg3に必要な最少辺数の下界
artifacts:
- path: research/experiments/common-pivot-residual-game-20261108/proof.md
  role: proof
  note: 二点辺がある場合のrank任意閉形式と、純三点のリンクグラフ帰着
- path: research/experiments/common-pivot-residual-game-20261108/audit.py
  role: verifier
  note: 全小共通pivot族の閉形式をC++個別占有subsetで型ごとに比較
- path: research/experiments/common-pivot-residual-game-20261108/output/audit.json
  role: data
  note: 完全小型比較、鋭いg3達成例、rank四のg4反例
- path: research/log/2026-11-08-common-pivot-rank-boundary.md
  role: log
  note: 小型観測からrank境界の反例と全称閉形式へ進んだ経緯
scope: 一点追加通常ゲーム、サイズ二または三の全極小残余禁止辺が一点cを共有。点数・辺数・自由点数は無制限。別の閉形式はrank任意で共通pivotと二点辺がある場合。
evidence: 外側着手後も二点辺が残る場合のmex帰納による閉形式、純三点ではリンクグラフの非孤立点への一手で二点辺が生じること。有限小型全族で別C++ subset計算と照合。
---

全残余禁止辺が二点または三点集合で、一つの点cを共有するなら
**Grundyは3以下**。辺数・点数・自由点数は制限しない。
さらに合法点数nが奇数ならg∈{0,1,2}、偶数ならg∈{0,1,3}。
四点の辺mask族 `3,13` がg=3を達成するため鋭い。
純三点でも七点の族 `7,13,49,97` がg=2、自由点付き八点族がg=3。
純三点・共通pivotに限れば、g2とg3の最少点数は7と8、最少辺数はともに4。

より一般にrank任意で、全辺がcを含み、二点辺が一つある場合は閉形式を持つ。
c以外の現在合法点数の偶奇をp、cへの手のGrundyをaとすると、

|p|条件|現在のg|
|---:|---|---:|
|0|a=0|2|
|0|a≠0|0|
|1|a=1|3|
|1|a≠1|1|

二点辺の外側点への手でcが不合法となり、残り全点が自由になることを用い、
外側点数に関する帰納で証明する。
純三点・二点辺なしの場合は、三点辺からcを除いたリンクグラフを使う。
非孤立外側点への手では必ず二点辺が生じるため、初手値の集合に上の式が使え、
mexは3以下となる。リンクグラフのGrundy計算を高速化したとは主張しない。

rank四にまで広げると、七点の純四点族 `75,83,101,43,105,51` は
全辺が頂点0を共有するがg=4となる。
共通一点だけでrank任意のg≤3を保証することはできない。
このrank四反例そのものは、共通三点から強制される四点辺mask27が欠けるため、
K0683の閉包障害により標準q4の正確な残余族としては幾何実現できない。

式の有限監査は外側0..6点の全41658共通pivot族と追加四証人。
別C++占有subset DPの3279792安全状態で全根値が一致した。

[全称証明・厳密式・有限監査](../../experiments/common-pivot-residual-game-20261108/proof.md)を参照。
K0683によりrank三以下の達成例は有限整数点盤に実現できる。
標準全正方形格子盤での達成と世界初性は主張しない。
