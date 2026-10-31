---
id: K0585
title: N=2q+1の二担い手12型は定数状態で強解決でき空盤と全初手を無界qで分類できる
kind: proposition
status: proved
topics: [geometry, variants, grundy, residual-games, first-moves]
aliases: []
relations:
- type: depends_on
  target: K0584
  note: 二担い手領域とN=2q+1の12型幾何分類
- type: depends_on
  target: K0002
  note: 通常Grundy値とmisère補助mex値の定義
artifacts:
- path: research/experiments/short-board-2qplus1-periodic-20261031/proof.md
  role: proof
  note: 3476個の有限mex恒等式を無界帰納法へ接続する証明、12型の空盤と全初手
- path: research/experiments/short-board-2qplus1-periodic-20261031/verify.py
  role: verifier
  note: 有限状態証明書とq=8,9,12,25,60の241080圧縮局面の独立照合
scope: q≥8、N=2q+1平面q点共円・共線禁止ゲームの二担い手12型、通常・misère二人ゲームの全安全局面
evidence: 3476個の局所mex恒等式と残容量偶奇射影の数学的帰納法による計算機援用全称証明、241080圧縮局面の独立照合
---

# 二担い手12型の無界Grundy値

K0584 の二担い手12型を (a,b,c,z)=(|A|−q,|B|−q,|A∩B|,N−|A∪B|) で表す（a≥b）。全安全局面の残容量 (u,v,T,E) に対して

\[
(g,h)(u,v,T,E)=(g,h)(p(u),p(v),T,E),
\quad p(n)=n\ (n\le5),\quad p(n)=4+(n\bmod2)\ (n\ge6).
\]

12型の有効な有限表は合計1936状態。占有数が与えられれば通常・misèreの値と勝ち初手を O(1) で判定できる。

**空盤**：任意の q≥8 について (a,b)=(0,0),(1,1),(2,0) の7型では (g,h)=(1,0)、(1,0),(2,1),(3,0) の5型では (0,1)。いずれも全初手の子の値は同一で、前者では (0,1)、後者では (1,0)。したがって通常版・misère版の勝ち初手はそれぞれ全点か空集合で、両版で逆になる。

全安全局面で h=τ(g)（0と1交換）は12型のうち (1,1,2,1)、(2,1,2,0) だけで破れる。q=8で前者の占有数 (0,5,0,0)、後者の (1,5,0,0) はどちらも (g,h)=(0,0)。

**証拠の範囲**：3,476個の有限mex恒等式の厳密検査と、u,v≥8 の遷移が6・7代表に一致することを用いた無界帰納法による計算機援用証明。別方式の再帰で241,080圧縮局面を照合し不一致0。Lean形式検証は未実施。一般の大盤残局へ無条件には適用しない。
