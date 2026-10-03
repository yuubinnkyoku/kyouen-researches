---
id: K0257
title: 共通点を一つも持たない最小反転解除族がある
kind: proposition
status: computed
topics:
- variants
aliases:
- B524
relations: []
artifacts:
- path: research/verification/round35-empty-intersection-minimum.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B524の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round35_minimum_family_verified.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round35_empty_intersection_search.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/scripts/round35_empty_intersection_search.cpp
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: '起点: [個票10・B251〜B259](verification/batch-10.md)。4×4の全単独解除とペアの一部標本が不変という範囲だけを使う。'
evidence: 原文監査 SUPPORTED / finite_witness_and_cardinality_minimum_proof
---

# 共通点を一つも持たない最小反転解除族がある

対象命題: 共通点を一つも持たない最小反転解除族がある。 B523の一般化には限界があり、離れた制約の解除が相乗的に勝敗を変える。

適用文脈: 起点: [個票10・B251〜B259](verification/batch-10.md)。4×4の全単独解除とペアの一部標本が不変という範囲だけを使う。

現在の結論: 4×4三組反転解除族の共通部分が空。全八部分族の全安全mexを独立照合、全単独・全ペア不反転と合わせ基数最小3。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
