---
id: K0703
title: 純三点共通pivot族は通常値0または1を固定して全misère補助値4以上を実現できる
kind: proposition
status: proved
topics:
- grundy
- residual-games
- geometry
- variants
aliases: []
relations:
- type: depends_on
  target: K0696
  note: リンク相互再帰Gmのh0・t=m・制限子値集合・自由点での低所属保存
- type: depends_on
  target: K0694
  note: 外側着手後のpaired補助値式と自由点付き純三点の式
- type: depends_on
  target: K0692
  note: 同じ純三点共通pivot族の通常値上界とリンク子値による初期g1
- type: depends_on
  target: K0683
  note: 各三点辺に一占有アンカーを置く指定有限整数点盤での実現
- type: depends_on
  target: K0704
  note: 自由点付加の補助値xor1は全有限ゲームに成立する一般補題
artifacts:
- path: research/experiments/common-pivot-misere-all-values-20261108/proof.md
  role: proof
  note: 低hリンク子の全t集合からpure根h=m+2と一自由点付きの値を導出
- path: research/experiments/common-pivot-misere-all-values-20261108/verify.py
  role: verifier
  note: リンクの相互再帰と全到達残余の性質Rを原始再帰で検査
- path: research/experiments/common-pivot-misere-all-values-20261108/output/dag_audit.json
  role: certificate
  note: m2..64のpure根と自由点付き根の式を独立ゲームDAGで照合
- path: research/experiments/common-pivot-misere-all-values-20261108/output/geometry.json
  role: certificate
  note: 十点g1/h4と十一点g0/h5の具体的22/23点整数盤も独立検査
- path: research/log/2026-11-08-misere-unboundedness-mutual-recursion.md
  role: log
  note: 二点辺なしのpure coneでも全高値を得た経緯
scope: 全極小残余禁止辺が三点集合で共通合法点cを持つ有限一点追加ゲーム。任意個の点・辺と自由点を許す。gは通常Grundy、hは終局1の補助mex。指定有限整数点盤への実現を含むが、標準全正方形格子盤は含まない。
evidence: 全m>=2のh0,t=mリンクGmの子制限値集合0..m-1と高h子の存在から、pure根の全子h集合0..m+1を導きh=m+2。通常根g1、一自由点付きg0と補助値xor1の特定式を別に導出。独立DAGと小型整数座標でも照合。
---


任意q≥4について、全て三点の残余辺が一つの合法点cを共有する有限族で

\[
(g,h)=(1,q)
\]

を実現できる。さらに同じクラスで通常値を0に固定しても、全q≥4を実現できる。
通常値はクラス全体で3以下だが、補助値hには一様上界がない。

K0696の相互再帰リンクG_m^0 (m≥2)の各辺uvを{c,u,v}へ置き換える。
リンクのhは0、低hの子は全て1で、その制限通常値集合は0..m−1。
高hの子も存在する。K0694のpaired式を外側着手後に適用すると、
初手後のh集合は、cへ置いた場合の0と、外側の1..m+1で尽きる。
根はh=m+2、通常値はg=1と決まる。
合法点数は5·2^(m−1)、三点辺数はm≥3で
5·2^(m−2)(5·2^(m−1)−m−5)。サイズ最小性は主張しない。

自由点一個を加えた根はg=0、補助値は(m+2) xor 1。
これは一自由点付加に対する一般補題K0704の特例であり、任意直和におけるh同士のxor合成とは区別する。
q→q xor 1は4以上の整数を置換するため、g=0でも全q≥4を実現する。

[全称帰納・pure根のmex・自由点式](../../experiments/common-pivot-misere-all-values-20261108/proof.md)を保存した。
小型例の十合法点(g,h)=(1,4)、十一合法点(0,5)は、22/23点の整数座標盤でも監査済み。
全qへの量化は帰納証明に基づき、有限計算からの外挿ではない。
標準全正方形格子盤、全ての小さいhの共通pivot最少点数、世界初性は未主張。
