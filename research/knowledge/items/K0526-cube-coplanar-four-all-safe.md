---
id: K0526
title: 2×2×2立方体の4点共面禁止版は全159安全局面を強解決し両ルール後手必勝
kind: proposition
status: proved
topics: [variants, geometry, grundy, maximal-safe, maximum-safe]
aliases: []
relations:
- type: depends_on
  target: K0002
  note: 通常Grundy値と終局の定義
- type: depends_on
  target: K0504
  note: 共面のみ4点禁止という別変種の定義
artifacts:
- path: research/experiments/cube-coplanar-q4-20261024/proof.md
  role: proof
  note: 有限完全分類と監査境界
- path: research/experiments/cube-coplanar-q4-20261024/verify.py
  role: verifier
  note: 排他的論理和と整数行列式の一致、および256状態全列挙
- path: research/experiments/cube-coplanar-q4-20261024/independent.cpp
  role: verifier
  note: 独立整数行列式生成と別実装の全局面再帰
- path: research/experiments/cube-coplanar-q4-20261024/results.json
  role: data
  note: Python完全列挙の層別Grundy・misère分布
- path: research/experiments/cube-coplanar-q4-20261024/independent-results.txt
  role: data
  note: C++独立完全列挙の出力
scope: 3次元2×2×2頂点盤、4点共面（退化含む）禁止の通常版とmisère版、全安全局面
solution:
  board: 2×2×2・共面4点禁止
  level: strong
  outcome: second-player-win
  classification: [root, first-moves, all-safe-win-loss, all-safe-grundy]
  coverage: 全159安全局面（通常版とmisère補助mex）
  conditions: 立方体の8頂点、4点共面のみ禁止、通常・misère別々
  verification: [exhaustive-enumeration, independent-enumeration]
  certificate: 256全ビット集合の有限完全列挙
  independent_check: 排他的論理和による幾何と直接整数行列式の独立一致
  note: 両版とも空盤後手勝ち。通常g(空)=0、全一石g=2。K=5、s=4
---

# 2×2×2・4点共面禁止版の完全解決

標準の共円・共線禁止や3次元の共球・共面5点禁止とは異なる。立方体8頂点で、任意の4点が同一実平面上にある配置を禁止する。

禁止4点組は12個、安全局面は159個。極大安全配置は4石24個と5石8個なので s=4, K=5。5石安全配置は各頂点vに対する {v,v⊕1,v⊕2,v⊕4,v⊕7} の8個のみ。

通常版の全一石局面はGrundy値2、空盤は0。misère補助mexも空盤0であり、両ルールとも後手必勝。通常／misère値の0↔1交換則には25局面の反例がある。

[全層の値、有限完全列挙の証明、独立検証器](../../experiments/cube-coplanar-q4-20261024/proof.md)。量化範囲は2×2×2の有限盤に限る。他の辺長や無限族へ外挿しない。
