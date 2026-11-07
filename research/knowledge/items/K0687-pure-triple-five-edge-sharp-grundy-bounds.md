---
id: K0687
title: 純三点残余辺が3本以下ならGrundyは1以下、4本以下で3以下、5本以下で5以下で全て鋭い
kind: proposition
status: proved
topics: [grundy, residual-games, geometry, variants]
aliases: []
relations:
- type: depends_on
  target: K0108
  note: 純三点残余族の通常ゲームと自由点のxor分離
- type: depends_on
  target: K0683
  note: 抽象三点禁止族の全型を指定有限整数点盤へ移せる
artifacts:
- path: research/experiments/pure-triple-few-edge-grundy-20261107/proof.md
  role: proof
  note: 所属cellの行和3による全称有限帰着、孤立点処理、鋭い達成例
- path: research/experiments/pure-triple-few-edge-grundy-20261107/audit.py
  role: verifier
  note: Venn行和生成と独立辺追加生成の全型集合一致、cell占有数mex
- path: research/experiments/pure-triple-few-edge-grundy-20261107/independent.cpp
  role: verifier
  note: 個別頂点占有subsetによる全527型の別根値計算
- path: research/experiments/pure-triple-few-edge-grundy-20261107/output/audit.json
  role: certificate
  note: h1..5の全型・度数・527型の個別一致・199922安全状態監査
- path: research/log/2026-11-07-pure-triple-spectra-and-incidence-bounds.md
  role: log
  note: 六点全数計算から、辺数による頂点無制限の定理へ進んだ経緯
scope: 任意個の合法点、極小残余禁止辺は全て三点集合、辺数h<=5、通常プレイ。自由点を任意個許す。標準全正方形盤での達成は含まない。
evidence: 辺所属cellの整数行和3への全称帰着。全527非同型核がVenn生成と辺追加生成で集合一致し、Python cell mexとC++個別subsetの199922安全状態で根値が型ごとに一致。
---

## 頂点数を制限しない鋭い上界

純三点辺の本数がh=1,2,3,4,5の場合、任意個の自由点を許した通常Grundyの鋭い上界は

\[
 \boxed{1,1,1,3,5.}
\]

従ってh≤3ならg≤1、h≤4ならg≤3、h≤5ならg≤5。
Grundy値2・3に必要な三点辺の最小本数は4、値4・5では5となる。

非孤立点は高々3h個で、辺への所属署名cellの点数a_sは各行の和が3になる整数解で表せる。
辺の置換で同型を除くとh=1..5の核数は **1,3,12,66,445**。
全527型を完全列挙し、核値と自由点のxor偶奇の両方を調べた。
頂点数の無限範囲はこの有限帰着と自由点のxor則によって保証する。

## 二方式生成と鋭さ

主生成は全所属署名の行和3を解く方式、別生成は小さい族へ新しい三点辺を追加する方式。
両方で全同型型が集合として一致した。
主ゲーム計算はcell占有数、別のC++は各頂点の占有subsetで、全527型・199922安全状態の根値が一致。

例えば次のマスク族が上界・最小本数を達成する。

|g|点数|辺数|辺mask|
|---:|---:|---:|---|
|2|6|4|19,21,38,56|
|3|7|4|37,73,14,112|
|4|8|5|67,21,22,152,224|
|5|9|5|176,261,38,56,448|

maskは頂点0を最下位bitとする。
g=4を六点で実現するにはK0686により七辺必要だが、点数を八個にすれば五辺で足りる。
点数最小と辺数最小は一致しない。

## 適用境界

[全称帰着・完全表・二生成法](../../experiments/pure-triple-few-edge-grundy-20261107/proof.md)を保存。
二点辺・四点辺が混じる族や、六本以上の鋭い上界には拡張しない。
K0683により達成型は有限整数点盤に移せるが、標準全正方形格子盤の達成ではない。
