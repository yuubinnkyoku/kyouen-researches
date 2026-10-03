---
id: K0041
title: Grundy天井・欠損単調性と一度の飽和による全後続層飽和
kind: proposition
status: proved
topics:
- grundy
aliases: []
relations:
- type: depends_on
  target: K0002
  note: ''
- type: depends_on
  target: K0026
  note: ''
artifacts:
- path: night-research/CYCLE5_GRUNDY_STRUCTURE.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: night-research/verify_saturation.py
  role: verifier
  note: mex上界と全小盤分布の照合
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# Grundy天井・欠損単調性と一度の飽和による全後続層飽和

全有限安全石置きゲームでg(S)≤K(S)−|S|≤K_n−|S|。M_n(k)=max_{|S|=k}g(S)、D_n(k)=K_n−k−M_n(k)は非増加。一つの層でM_n(k)=K_n−kなら全後続層でも等号が続く。

天井達成局面の子は0..g−1の各値を実現するmexと高さ上界を持ち、飽和鎖がある。小盤の開始層σ_4=2、σ_5=σ_6=3は有限の独立内容で、後続単位傾斜自体は定理の帰結。
