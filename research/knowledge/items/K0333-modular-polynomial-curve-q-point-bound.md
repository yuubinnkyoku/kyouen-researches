---
id: K0333
title: 次数k≥2の剰余多項式グラフは直線高々k点・円高々2k点でq≥2k+1版が全点安全
kind: proposition
status: proved
topics: [geometry, variants, maximum-safe, residual-games]
aliases: []
relations:
- type: depends_on
  target: K0001
  note: 円または直線のq点を禁止するルール変種
artifacts:
- path: research/experiments/frontier-geometry-2026-10-05/proof.md
  role: proof
  note: 原始整数方程式・有限体根数による全称証明とk=2,3,4の鋭さ証人
- path: research/experiments/frontier-geometry-2026-10-05/verify_polynomial_curves.py
  role: verifier
  note: 原始整数の直線・円カタログと共有幾何coreによる独立有限支持検査
- path: research/experiments/frontier-geometry-2026-10-05/polynomial-curve-audit.json
  role: data
  note: 66多項式グラフ・13素数Q_pカタログ・次数3,4の明示整数証人
scope: 素数p、次数k≥2で最高次係数がpで非零の整数多項式f、P={(t,f(t) mod p):0≤t<p}の整数代表。q版ゲームの強解決はPだけを盤にした制限ゲーム。
evidence: 全称数学的証明。k=2,3,4の円上限は明示存在証人で鋭さも確定。
---

# 剰余多項式グラフの円・直線上限

Pと任意の実直線の交点は高々k点、任意の実円の交点は高々2k点。
三点を通る円を原始整数方程式A(x²+y²)+Bx+Cy+D=0に直してmod pで代入する。
A≠0なら非零の次数2k多項式、A=0なら非零で次数≤kとなるため根数上限が適用できる。
直線も同様。円がk+1点以上ならp∤Aであり、中心の既約共通分母にpは現れない。

従ってq≥2k+1ではP全体が安全であり、p×p盤のq点版に安全p点の明示構成を与える。
**Pのみを盤にした制限ゲーム**では全ての部分集合が安全、最大も最小極大もp。
Sからの手数L=p−|S|は固定され、通常二人版のGrundy値はL mod 2。
r人循環手番では、次がaなら最終着手者はL>0でa+L−1 mod r、着手不能手番はa+L mod r。
r人の勝者規則そのものは仮定しない。

円上限2kはk=2,3,4で鋭い。k=2のQ_pでは全奇素数p≥5で二つの完全対が四点円を作る。
k=3,p=3391の六点円、k=4,p=43の八点円の整数座標と方程式をartifactに保存し直接代入で検査した。
従ってこの三次数では全多項式グラフを安全と保証する閾値をq=2kへ下げられない。

全kでの鋭さ、標準q=4での剰余放物線等号問題、全p×p盤の最大や勝敗を確定した結果ではない。
有限カタログは一般証明の支持検査として区別する。
