---
id: K0256
title: 最小反転解除族は共有する三点を持つ
kind: proposition
status: refuted
topics:
- variants
aliases:
- B523
relations: []
artifacts:
- path: research/experiments/original-claims/reports/round35-empty-intersection-minimum.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/archive/hypothesis-ledgers/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B523の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round35_minimum_family_verified.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round35_empty_intersection_search.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/scripts/round35_empty_intersection_search.cpp
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: '起点: [個票10・B251〜B259](../../log/claim-audit/batch-10.md)。4×4の全単独解除とペアの一部標本が不変という範囲だけを使う。'
evidence: 原文監査 REFUTED / cardinality_minimum_counterexample
---

# 最小反転解除族は共有する三点を持つ

否定された命題: 最小反転解除族は共有する三点を持つ。 小盤の最小族は、同じ三点に対する複数の補完候補をまとめて解禁する形になる。

適用文脈: 起点: [個票10・B251〜B259](../../log/claim-audit/batch-10.md)。4×4の全単独解除とペアの一部標本が不変という範囲だけを使う。

現在の結論: 基数最小三禁止解除族に共通点のない証人があり、共通三点必須説は偽。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
