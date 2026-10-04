---
id: K0215
title: 7×7最大配置の最初の合法外点はD4軌道で少数型になる
kind: proposition
status: computed
topics:
- maximum-safe
- geometry
aliases:
- B382
relations:
- type: depends_on
  target: K0026
  note: ''
artifacts:
- path: research/experiments/original-claims/reports/round9-n7-outer-patterns.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/archive/hypothesis-ledgers/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B382の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round9_n7_outer_patterns.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/scripts/round9_n7_outer_patterns.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: 有限安全Sを整数平面へ固定し、盤の外でも4点共円・共線だけで合法性を定める。r(S)はSの最小軸平行外接矩形からのChebyshev距離が最小の、追加可能な外点の距離。
evidence: 原文監査 SUPPORTED / finite_complete_classification
---

# 7×7最大配置の最初の合法外点はD4軌道で少数型になる

対象命題: 7×7最大配置の最初の合法外点はD4軌道で少数型になる。 A相・B相ごとに外接矩形からの位置を分類すると、半径2の外周上の固定した短いパターンで記述できる。

適用文脈: 有限安全Sを整数平面へ固定し、盤の外でも4点共円・共線だけで合法性を定める。r(S)はSの最小軸平行外接矩形からのChebyshev距離が最小の、追加可能な外点の距離。

現在の結論: 既存全16最大配置の全外点を二方式で照合し、最初の半径2の型を分類。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
