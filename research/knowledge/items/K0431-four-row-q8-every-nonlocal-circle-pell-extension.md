---
id: K0431
title: 四行8点円の全ての非局所型は同じ傾きの無限Pell族へ延長する
kind: proposition
status: proved
topics: [geometry, rectangles, variants]
aliases: []
relations:
- type: generalizes
  target: K0317
  note: 特定のPell族の存在を、任意の非局所円からの無限延長へ強める
artifacts:
- path: research/experiments/fixed-width/reports/q48-all-nonlocal-pell-20261015.md
  role: proof
  note: ノルム8の平方判別式例外排除と無限Pell延長
- path: research/experiments/fixed-width/scripts/q48_all_nonlocal_pell_20261015.py
  role: verifier
  note: 既知5型を正規形へ戻し、Pell世代と整数行列式を監査
- path: research/experiments/fixed-width/output/q48_all_nonlocal_pell_20261015.txt
  role: data
  note: 15円・75個の行列式等の監査結果
scope: 標準整数格子の四連続行に各2点を持つ全8点円。局所型(1,3,3,1)を除く無界命題。
evidence: 任意の非局所円を正規形にすると QM²−PL²=8、P≥15。平方判別式補題からPQは非平方で、偶奇を保つPell変換を反復できる。正値・厳密増加性も保たれ、同じ既約傾きの相異なる円が無限に得られる。
---

非局所の増加弦長を上下反転で `0<a<b<c<d` とする。`s=(d+a)/2`, `v=(c-b)/2` の既約比 `A/B=s/v` と `g=gcd(A,3)` から、正整数 `L,M` と

`P=A²−B²`, `Q=(A²−9B²)/g²`, `QM²−PL²=8`

を得る。もし `PQ` が平方なら、平方自由部分で因数分解した `p(sM−rL)(sM+rL)=8` は `P=1` を強制する。しかし4行8点円では `A>3B` から `P≥15`。ゆえに `PQ` は非平方である。

通常のPell単元を二乗して偶奇を保つ行列変換を反復するとノルム8を保つ。`M/L` は `sqrt(P/Q)` へ減少し、弦長の正値・厳密増加性は元の円の不等式から保存される。最大弦長が無限に増えるため、同じ既約傾きの互いに異なる8点円が無限に存在する。

有限監査は既知5型の各3世代に限る。どの傾きが実現可能かの完全分類は未解決であり、有限円型列挙や安定化長から無界結論を導いてはいない。
