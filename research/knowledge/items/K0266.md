---
id: K0266
title: 7×7全最大配置の交換距離は5が最小で、最小対は八A–Bペア
kind: proposition
status: computed
topics:
- maximum-safe
- reconfiguration
aliases:
- Cycle7:d*
relations:
- type: depends_on
  target: K0051
  note: ''
artifacts:
- path: night-research/FINAL_SELECTION_THEOREM.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: results/maxsafe_exchange_n7.csv
  role: data
  note: 全16配置の交換検査
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: results/maxsafe_exchange_components_n6.csv
  role: data
  note: n6最大層の成分
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 7×7全最大配置の交換距離は5が最小で、最小対は八A–Bペア

全16最大配置のC(16,2)=120対を計算すると、d(S,T)=14−|S∩T|の最小は5、d≤4なし。d5の八対はA–B完全マッチングを作り、A側を中心ありとする同時D4では交換テンプレート一類。

一石交換グラフでは全16配置が孤立。n6最大11石464配置では296が一石交換を持ち、無向辺304、成分248（168単元,56二点,8五点,8七点,8十一点）。「全極大」の比較ではなく最大サイズ層の比較。
