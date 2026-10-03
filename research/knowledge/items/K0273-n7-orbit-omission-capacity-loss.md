---
id: K0273
title: 7×7の軌道省略容量損失は5・6盤より強い
kind: proposition
status: computed
topics:
- maximum-safe
- geometry
aliases: []
relations:
- type: depends_on
  target: K0051
  note: ''
artifacts:
- path: night-research/FINAL_SELECTION_THEOREM.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: night-research/CYCLE24_N6_CAPACITY_CONTRAST.md
  role: source
  note: 六盤の完全制約最大
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: night-research/CYCLE25_N5_CAPACITY_CONTRAST.md
  role: source
  note: 五盤の完全制約最大
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: night-research/CYCLE26_N4_CAPACITY_CONTRAST.md
  role: source
  note: 四盤との比較
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 7×7の軌道省略容量損失は5・6盤より強い

各盤の最大安全層で軌道(0,2)または(1,2)を省くと、n5は最大9→8、n6は11→10、n7は14→12。n7両方省略は最大11。n7では両軌道が十三石でも必須。

n5中心なし56/100最大、n6の(2,2)なし104/464最大が残る一方、n7最大では(2,2)は全16で空。n7角四つは最大≤12、中心+(2,3)も最大12。各値は条件付き完全探索であり、相構造の一般全盤則にはしない。
