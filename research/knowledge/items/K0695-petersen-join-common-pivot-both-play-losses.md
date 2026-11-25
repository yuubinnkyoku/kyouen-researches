---
id: K0695
title: Petersen完全joinの共通pivot純三点族は全サイズで通常・misèreとも後手勝ちとなる
kind: proposition
status: proved
topics: [grundy, residual-games, geometry, variants]
aliases: []
relations:
- type: depends_on
  target: K0692
  note: 二点辺が生じた後の通常Grundy閉形式
- type: depends_on
  target: K0694
  note: misère補助値の二点辺付きpivot変換
- type: depends_on
  target: K0683
  note: 全kについて指定有限整数点盤に移す
artifacts:
- path: research/experiments/petersen-common-pivot-misere-family-20261108/proof.md
  role: proof
  note: KG5,2の全閉近傍子C6、joinと全初手証明、盤点数の式
- path: research/experiments/petersen-common-pivot-misere-family-20261108/verify.py
  role: verifier
  note: k1..5の全局所子検査、k1..2の別C++生subset、k1の整数座標幾何検査
- path: research/experiments/petersen-common-pivot-misere-family-20261108/output/audit.json
  role: certificate
  note: 通常・補助値の全子と二根、26点盤の全共円四点組と具体座標
- path: research/log/2026-11-08-common-pivot-misere-transform.md
  role: log
  note: misère変換からPetersenの全C6子を使う無限族へ進んだ記録
scope: 全k>=1、Petersenグラフk個の完全join H_kの各辺uvへ共通合法点cを加えた純三点禁止族。通常プレイと最後の合法手が負けるmisère比較版。初期安全局面のみの勝敗。
evidence: H_kの全Node-Kayles子がC6で(g,h)=(0,0)になる局所証明と、pivot族の全初手で通常値・補助値が非零となる証明。k1..2の全占有subsetとk1整数座標でも検査。
---

k≥1、H_kをPetersenグラフk個の完全joinとする。
合法点をcとH_kの10k頂点、三点辺を全{c,u,v} (uv∈E(H_k))とすると、

\[
 \boxed{(g,h)=(0,0)\quad\text{for all }k\ge1.}
\]

hは終局1のmisère補助mex。通常版とmisère版の両方で手番側負けとなる。
全三点辺は未占有cを共有する。
K0683により合法点10k+1、占有anchor数50k²−35k、総盤点数50k²−25k+1の
標準q4指定有限整数点盤に実現できる。全禁止四点組もcを共有する。

PetersenをKG(5,2)で表すと、どの閉近傍を消してもC6が残る。
完全joinの他成分も一手で消えるため、H_kの全Node-Kayles子はC6、根は(1,1)。
pivot族ではcへの手の子が(1,1)、全外側初手の子が(1,2)。
従ってどちらの子値集合にも0がなく、根は(0,0)。

[全称証明と独立検査](../../experiments/petersen-common-pivot-misere-family-20261108/proof.md)を参照。
有限監査はk1..5の全局所子、k1..2の生占有subset、k1の26点整数座標盤。
標準全正方形格子盤、全到達局面の強解決、最少点数、世界初性は未主張。
