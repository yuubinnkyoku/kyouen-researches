---
id: K0125
title: 三石局面のP(S)の彩色数は3以下
kind: proposition
status: refuted
topics:
- residual-games
- reconfiguration
aliases:
- B062
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
- path: research/hypothesis-bank-2026-09-27.md
  role: source
  note: B062の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round44_tree_clique_verified.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/scripts/round44_tree_and_clique.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: 本文の原文量化と現在の採用境界
evidence: 原文監査 REFUTED / infinite_clique_family_and_minimum_board_counterexample
---

# 三石局面のP(S)の彩色数は3以下

否定された命題: 三石局面のP(S)の彩色数は3以下。 Sの3組の石ペアに由来する競合辺の幾何が、任意グラフより強い彩色制約を持つかもしれない。

現在の結論: 三石の標準整数盤に任意大のK4Mを実現、彩色数は無界。4×4初例は厳密χ6、全n≤3三石は三色で最小盤4。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
