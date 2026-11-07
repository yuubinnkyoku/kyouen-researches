---
id: K0696
title: 二点辺付きrank三共通pivot族のmisère補助値は無界と予想する
kind: proposition
status: conjectured
topics: [grundy, residual-games, variants]
aliases: []
relations:
- type: depends_on
  target: K0694
  note: 二点辺付きpivot変換と自由二点の補助値周期2
- type: depends_on
  target: K0692
  note: 同じ対象の通常Grundyは全点数・全辺数で3以下
- type: depends_on
  target: K0683
  note: 各有限rank三族の指定有限整数点盤での実現
artifacts:
- path: research/experiments/common-pivot-misere-larger-values-20261108/proof.md
  role: proof
  note: 無界性をグラフh0/1制限ゲームへ帰着する証明と、有限Tなら上界T+4の条件付き証明
- path: research/experiments/common-pivot-misere-larger-values-20261108/verify.py
  role: verifier
  note: リンク値t6/7の再計算とh8/9の別C++全占有subset照合
- path: research/experiments/common-pivot-misere-larger-values-20261108/output/audit.json
  role: certificate
  note: 十九点h8・二十点h9の二根と790944安全状態の一致
- path: research/log/2026-11-08-misere-mobility-gap-and-larger-pivot-values.md
  role: log
  note: 値9までの有限証拠と無界性予想・同値帰着を分けた記録
scope: サイズ二/三の全極小残余辺が一点cを共有し、二点辺を少なくとも一つ含む有限一点追加ゲーム。点数・辺数は無制限。hは終局1のmisère補助mex。
evidence: K0694でh4..7、追加の独立C++検査でh8/9を達成。無界性そのものは未証明だが、Node-Kaylesのh0/1制限ゲームGrundy tの無界性と同値であることは証明済み。
---

## 予想

任意のBに対し、全二点/三点辺が一点cを共有し二点辺がある有限族で
**h>B** となるものが存在すると予想する。
同じ対象の通常GrundyはK0692により常に3以下。
hは直和のSprague–Grundy値ではなく、終局1のmisère補助mexである。

## 証明済みの同値帰着

有限グラフHのNode-Kaylesについて、h=0/1局面だけを残す通常ゲームの値をt(H)、
その全グラフにわたる上限をTとする。この予想は **T=∞と同値**。
さらに二点辺を要求しないrank三共通pivot族全体でのh無界性とも同値。

Tが有限なら、二点辺付き部分族の補助値上限は厳密にT+2、
rank三共通pivot族全体ではT+4以下となる。
T=∞ならmexの閉性から全てのt=sをグラフで達成でき、
二点辺付き部分族でh=2+sを作れるため、全非負整数hの達成も従う。
[同値と条件付き上界の証明](../../experiments/common-pivot-misere-larger-values-20261108/proof.md)を参照。

## 現在の有限証拠と限界

十九合法点・二点辺二本・三点辺三十本で(g,h)=(0,8)、
自由点付き二十合法点で(1,9)を別C++の790944安全状態でも確認した。
リンクに自由点を一つ加えたh=0のグラフではt=7なので **T≥7** は確定している。
K0683で53/54点の有限整数点盤へ構成的に移せるが、具体座標の別全数監査は未実施。

値9までの有限達成は、無界性や全非負整数の達成の証明ではない。
Tの有限上界、無限族の構成、予想の反例はいずれも未確定。
標準全正方形格子盤についての主張や世界初性は含めない。
