---
id: K0107
title: 安全k石の一空点被覆はk≥4で二次上限から必ず1減る
kind: proposition
status: proved
topics:
- geometry
- maximal-safe
aliases: []
relations:
- type: depends_on
  target: K0001
  note: ''
- type: refutes
  target: K0134
  note: 本文の証明・証人が原文に与える帰結
artifacts:
- path: research/experiments/original-claims/reports/round45-cover-gap-and-sharp-overlap.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round45_cover_verified.json
  role: data
  note: 整数反転と全三点・四点の鋭さ証人
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 安全k石の一空点被覆はk≥4で二次上限から必ず1減る

b_S(p)は空点pを禁止するS内三点組数。三点族は異なる組の共通石が高々一つで、全kでb≤floor(k(k−1)/6)。p中心反転でb=t₃、δ=C(k,2)−3b=t₂。k≥4ではMelchiorのt₂≥3によりb≤floor(k(k−1)/6)−1。

安全六石T=[(4,4),(4,7),(4,8),(7,4),(10,4),(1,10)]を原点反転し1523080倍した整数証人はb=4、δ=3で改良上限を達成。大kでδ=3を達成するとは言わない。
