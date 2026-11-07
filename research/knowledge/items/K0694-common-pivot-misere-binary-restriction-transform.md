---
id: K0694
title: 共通pivotのmisère補助値は0/1制限ゲームで変換でき、通常上界3の族にも値7が生じる
kind: proposition
status: proved
topics: [grundy, residual-games, geometry, variants]
aliases: []
relations:
- type: depends_on
  target: K0108
  note: 残余禁止族の継続ゲーム表現
- type: depends_on
  target: K0309
  note: 終局1のmisère補助mexと通常値との交換則の定義・境界
- type: depends_on
  target: K0692
  note: 通常rank三以下の共通pivot族の上界3と比較する
- type: depends_on
  target: K0683
  note: 純三点達成例の指定有限整数点盤への移送
artifacts:
- path: research/experiments/common-pivot-misere-bound-20261108/proof.md
  role: proof
  note: rank任意の二点辺付きpivot変換、自由二点の補助値周期2、純三点計算法
- path: research/experiments/common-pivot-misere-bound-20261108/audit.py
  role: verifier
  note: リンクグラフhと0/1制限ゲームtでの式、41662根の別C++比較
- path: research/experiments/common-pivot-misere-bound-20261108/independent.cpp
  role: verifier
  note: 通常・misère両方を占有subsetから直接計算
- path: research/experiments/common-pivot-misere-bound-20261108/output/audit.json
  role: certificate
  note: 3284481安全状態の全一致、純三点h4/h5と混合族h4/h5
- path: research/experiments/common-pivot-misere-bound-20261108/output/geometry.json
  role: certificate
  note: 22点と23点の整数座標盤、全禁止四点組、全安全補助値
- path: research/experiments/common-pivot-misere-bound-20261108/audit_induced.py
  role: verifier
  note: 十五点h6と十六点h7のリンク制限ゲーム計算と独立C++全占有subset
- path: research/experiments/common-pivot-misere-bound-20261108/output/induced_high_audit.json
  role: certificate
  note: 二点辺二本・三点辺十八本で(g,h)=(0,6),(1,7)の達成例と比較件数
- path: research/log/2026-11-08-common-pivot-misere-transform.md
  role: log
  note: 単純式の失敗から、0/1制限ゲームと大きいmisère値へ進んだ記録
scope: 全禁止辺が一点cを共有し二点辺が一つある任意rankの一点追加ゲーム。hは終局1の補助mex。適用例は純三点十/十一点h4/5とrank三以下の混合族十五/十六点h6/7。標準全正方形格子盤は対象外。
evidence: 外側点数の帰納による厳密変換、自由二点の周期2補題。全41658小族と追加四例を別C++で比較し、純三点二例は整数座標も検査。追加のh6/h7も別C++全占有subsetと一致。
---

hを終局で1、非終局で子のmexとするmisère補助値とする。
全辺がcを含み二点辺がある場合、c以外の合法点数の偶奇をp、
cへの手の後のゲームをLとする。
Lのうちh=0/1の局面だけを残した別の通常ゲームのGrundyをt(L)とすると、

|p|条件|現在のh|
|---:|---|---:|
|0|h(L)=1|2+t(L)|
|0|h(L)≠1|1|
|1|h(L)=0|2+t(L)|
|1|h(L)≠0|0|

rank・点数・辺数に上限のない厳密式である。
また任意の有限不偏ゲームに自由点を二個加えても補助値hは変わらない。
自由点一個についてh xor1を使うことはできない。

K0692の通常上界3はhに移らない。
全辺が頂点0を共有する純三点族
`7,13,49,97,515,517,521,529,545,577,641,769` は
十合法点で(g,h)=(1,4)、自由点付き十一合法点で(0,5)。
22点・23点の整数座標盤へ移し、全禁止四点組16170件と1839安全状態を検査した。
いずれも全禁止四点組が一つの未占有pivotを共有する。

さらに二点辺二本・三点辺十八本の共通pivot族で、
十五合法点の(g,h)=(0,6)、自由点付き十六合法点の(1,7)を得た。
リンクグラフのh=0/1制限ゲーム値tは4/5で、別C++全占有subsetとも一致。
K0683により37点・38点の整数点盤へ構成的に移せるが、
この二例には別の具体座標全数監査は付けていない。

全41662根・3284481安全状態で、リンクグラフのh/t計算と別C++生subset計算が一致。
rank三以下の共通pivot族で通常／misère交換則が破れる最少合法点数は七。
固定pivotラベルで150族、全て(g,h)=(2,1)で、リンクグラフはC6かP3二個の直和に限る。
単純な通常式の移植は失敗しており、当時の不一致記録もexperiment内に保持する。
[証明・再現・限界](../../experiments/common-pivot-misere-bound-20261108/proof.md)を参照。
hの全称有界性・非有界性、達成例の最少点数、世界初性は未確定。
hはSprague–Grundy不変量ではなく、直和xorや違法手を打った側が負けるルールへ移さない。
