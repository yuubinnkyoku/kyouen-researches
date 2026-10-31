---
id: K0580
title: 平面q点禁止ゲームは境界N=2q−2でも禁止曲線と全安全局面を完全分類できる
kind: proposition
status: proved
topics: [geometry, variants, grundy, first-moves, maximal-safe, strategy-length]
aliases: []
relations:
- type: depends_on
  target: K0578
  note: 一曲線の場合の偶奇則と整数格子実現構成を利用
- type: depends_on
  target: K0483
  note: 二禁止辺の通常Grundy閉公式
- type: depends_on
  target: K0579
  note: 二禁止辺のmisère交換則
artifacts:
- path: research/experiments/critical-short-board-20261031/proof.md
  role: proof
  note: q≥5で高々二担い手、q=4で高々三担い手、全局面値と整数実現の全称証明
- path: research/experiments/critical-short-board-20261031/verify.py
  role: verifier
  note: 4×4格子20878盤の完全列挙、91盤の全安全局面直接mex検査
scope: 相異なるN=2q−2個の実平面点、q≥4、共円・共線q点組禁止、通常・misèreの全安全局面
evidence: 二担い手の交差がちょうど2点となる幾何的な全称証明とK0483/K0579。q=4の三担い手は補集合の完全マッチングに帰着。4×4格子20878盤の整数行列式完全列挙で独立検査。
---

# 境界N=2q−2の全局面強解決

q=4なら禁止q点組数は **0,1,2,3,5,15** のいずれか。q≥5なら **0,2** または **$\binom mq$ ($q\le m\le2q-2$)** のいずれか。候補はすべて整数格子上で実現可能。

禁止組が一つの直線・円上のm点からなる場合、終局長は $L=N-m+q-1$ で固定し、$g(S)=(L-|S|)\bmod2,\ h(S)=1-g(S)$。禁止組なしならL=N。

二つの禁止組がある場合は、それぞれq点で共有点がちょうど2点。K0483とK0579により**全安全局面**の通常・misère値を閉公式で決定できる。空盤の(g,h)はq=4なら(2,2)、q≥5なら(0,1)。q=4の通常勝ち初手は二禁止組の固有部4点、misère勝ち初手は共有部2点。q=5のmisère勝ち初手は共有部2点のみ、q≥6なら全点がmisère勝ち初手。q≥5の通常勝ち初手はない。

三つの禁止組があるのはq=4に限り、各禁止組の補集合は互いに素な三つの二点集合。すべての極大安全集合は4点で、$g(S)=(4-|S|)\bmod2,\ h(S)=1-g(S)$。

異なる直線・円は高々2点しか共有できないことが分類の核心。全称証明、全候補の整数実現、独立検証の範囲はproof.mdに記録。これは未着手の小盤の結果であり、占有済みの大盤の残余点集合に無条件適用しない。
