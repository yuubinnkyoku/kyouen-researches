---
id: K0193
title: 木の競合グラフで効く三点制約には最小の接続型がある
kind: question
status: open
topics:
- residual-games
- reconfiguration
aliases:
- B344
relations:
- type: depends_on
  target: K0108
  note: ''
artifacts:
- path: research/verification/round44-three-stone-cliques-and-tree-minima.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B344の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round44_tree_clique_verified.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/scripts/round44_tree_and_clique.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: '起点: [個票03・B051〜B058](verification/batch-03.md)、[個票04・B064〜B068](verification/batch-04.md)。孤立点だけによる退化例は除いて考える。'
evidence: 原文監査 PARTIAL / minimum_connecting_tree_classification
---

# 木の競合グラフで効く三点制約には最小の接続型がある

未確定の命題: 木の競合グラフで効く三点制約には最小の接続型がある。 三点が木のどこに位置するかを、分岐点までの距離の偶奇と共有パスで分類できる。

適用文脈: 起点: [個票03・B051〜B058](verification/batch-03.md)、[個票04・B064〜B068](verification/batch-04.md)。孤立点だけによる退化例は除いて考える。

現在の結論: 効く三点辺の最小接続木はK1,3と三葉上の三点辺で格子実現済み。より大きな木の距離偶奇による分類は未完成。

採用境界: 効く三点辺の最小接続木はK1,3・三葉上の辺、格子実現を検算。大きな木の距離偶奇による一般分類は未証明。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
