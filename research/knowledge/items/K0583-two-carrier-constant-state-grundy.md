---
id: K0583
title: N=2q・q≥7の二担い手七型は定数状態で全局面強解決でき空盤の通常・misère値も無界に確定する
kind: proposition
status: proved
topics: [geometry, variants, grundy, residual-games, first-moves]
aliases: []
relations:
- type: depends_on
  target: K0582
  note: 二担い手七型の幾何分類と四群の容量再帰
- type: depends_on
  target: K0002
  note: 通常Grundyとmisère補助mexの定義
artifacts:
- path: research/experiments/short-board-2q-periodic-20261031/proof.md
  role: proof
  note: 残容量の偶奇縮約、1723局所恒等式を基底とする無界帰納法
- path: research/experiments/short-board-2q-periodic-20261031/verify.py
  role: verifier
  note: 有限状態証明書と別表現による119317圧縮局面の独立再帰照合
scope: q≥7、N=2q平面q点禁止ゲームの二担い手七型、通常・misère二人ゲームの全安全局面
evidence: 6×6残容量表の1723個の局所mex恒等式を厳密検査し、偶奇代表への遷移不変性から全称帰納法で証明。別の既占有数再帰をq=7,8,12,25,60の119317状態で照合。
---

# 二担い手七型の無界Grundy閉公式（有限表）

K0582 の七型で担い手点数を q+α、q+β、共有点数を c、外部点数を z とする。A/B 固有点、共有点、外部点の既占有数を (i,j,t,e) と置き、u=q-1-i-t、v=q-1-j-t、T=c-t、E=z-e とする。

**全称定理**：すべての安全局面で (g,h) は u,v をそれぞれ p(n)=n (n≤5)、p(n)=4+(n mod 2) (n≥6) に置換しても変わらない。各型の u,v≤5 の有限表をmexで一度構成すれば、全局面の値と勝ち手を定数時間で決められる（占有数が与えられた場合）。各型最大324表要素。

空盤の (g,h) は、**任意の q≥7** について、型 IV・V が (1,0)、型 I・II・III・VI・VII が (0,1)。これは K0582 の有限 q 観測を全称的に確定したもの。

全局面の交換則 h=τ(g)（0↔1交換、2以上固定）は I–V・VII で成立し、VI では不成立。例えば q=7・VI型の固有点占有数 (i,j)=(0,4)、共有点占有数 t=0 の安全局面は (g,h)=(0,0)。

**証拠の範囲**：1723個の有限状態mex恒等式を再計算する検証器と、無界変数を偶奇代表へ落とす数学的帰納法による計算機援用証明。q=7,8,12,25,60 の119317圧縮局面で独立した既占有数再帰と一致した。Leanによる形式検証は未実施。幾何的な二担い手型でない一般の残局へ無条件には適用しない。
