---
id: K0699
title: 純三点ゲームの通常値とmisère補助値2〜9の点数・辺数Pareto前線が確定し、8と9の最少合法点数は十と十一
kind: proposition
status: proved
topics: [grundy, residual-games, geometry, variants]
aliases: []
relations:
- type: depends_on
  target: K0687
  note: 七辺以下の全核と自由点偶奇の通常値・補助値の完全表
- type: depends_on
  target: K0686
  note: 純三点の低値2と3の点数下界
- type: depends_on
  target: K0690
  note: 任意rankでの合法点数と両値の二段差、および純三点h2とh3の点数下界
- type: depends_on
  target: K0683
  note: 達成族の指定有限整数点盤への実現
artifacts:
- path: research/experiments/minimum-grundy-eight-20261108/proof.md
  role: proof
  note: 点数下界・七辺全核・点数最小証人による未列挙全辺数の支配排除
- path: research/experiments/minimum-grundy-eight-20261108/catalog_both.py
  role: verifier
  note: 全58146核の両偶奇を集計し、全前線証人を残余再帰で再検査
- path: research/experiments/minimum-grundy-eight-20261108/output/pareto_both.json
  role: certificate
  note: 両値2〜9の全非支配組合せと各族の辺mask証人
- path: research/experiments/minimum-grundy-eight-20261108/verify.py
  role: verifier
  note: 点数最小g/h8と9を独立残余再帰・C++subset・整数座標盤で検査
- path: research/experiments/minimum-grundy-eight-20261108/output/audit_pruned.json
  role: certificate
  note: 十点八辺の両値8・十一点八辺の両値9、18/19点の整数盤と全四点組
- path: research/log/2026-11-08-pure-triple-edge-censuses-and-pareto-fronts.md
  role: log
  note: 有界探索から完全核表と全点数最適表へ至った経緯
scope: 任意有限点集合上の純三点極小禁止族。自由点を任意個許す。gは通常Grundy、hは終局1のmisère補助mex。合法点数nと異なる三点辺数eの同時最小化。標準全正方形格子盤と総盤点数・占有点数の最小化は含まない。
evidence: 七辺以下の全58146核と自由点偶奇116292根の独立比較済み全表を集計。各値の大域的点数下界を八辺以下で達成し、全八辺以上を支配関係で排除。八辺g/h8・9の証人を独立再帰と生subsetの1620安全状態、具体的整数盤で検査。
---

同じ値を実現する純三点族のうち、合法点数nと辺数eをどちらも悪化させず、
少なくとも片方を小さくできる族がない組合せは、以下で尽きる。

|値|通常gの(n,e)|補助hの(n,e)|
|---:|---|---|
|2|(6,4)|(6,4)|
|3|(7,4)|(7,4)|
|4|(6,7), (7,6), (8,5)|(6,7), (7,6), (9,5)|
|5|(7,7), (8,6), (9,5)|(7,7), (8,5)|
|6|(8,6)|(8,6)|
|7|(9,6)|(9,6)|
|8|(10,8), (11,7)|(10,8), (11,7)|
|9|(11,8), (12,7)|(11,8), (12,7)|

値8と9は、任意rankを許しても最少合法点数が **10,11**。
十点上の三点辺mask `11,22,42,70,73,137,266,529` は(g,h)=(8,8)、
一自由点を加えた十一点では(9,9)となり、点数下界を達成する。
一方、最少辺数7では両値8に十一点、両値9に十二点が必要。
従って点数最小と辺数最小を同時には達成できない。

全称性は、七辺以下の58,146核の完全表だけではなく、
全辺数に有効な点数下界と、それを八辺以下で達成する証人を組み合わせて保証する。
八辺以上の任意族は、同じ値の点数最小証人に支配されるか同じ(n,e)となる。
自由点はgのxor偶奇とhの二個周期で処理した。hにはxor合成を使わない。

値4・5では通常値と補助値で前線が異なり、単なる値の交換では得られない。
全証人と[証明・再現手順](../../experiments/minimum-grundy-eight-20261108/proof.md)を保存する。
十点・十一点の最適証人は18点・19点の具体的整数座標盤でも検査済み。
その総盤点数や占有八点の最小性、標準全正方形格子盤での達成、世界初性は未主張。
