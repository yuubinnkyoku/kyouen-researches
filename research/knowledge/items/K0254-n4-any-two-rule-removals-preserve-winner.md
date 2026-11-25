---
id: K0254
title: 4×4はどの二つの禁止四点を同時解除しても後手勝ち
kind: proposition
status: computed
topics:
- variants
aliases:
- B521
relations: []
artifacts:
- path: research/experiments/original-claims/reports/round19-rule-removal-audit.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/archive/hypothesis-ledgers/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B521の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round19_rule_certificates.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round19_rule_pair_lower.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/scripts/round19_rule_certificates.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: '起点: [個票10・B251〜B259](../../log/claim-audit/batch-10.md)。4×4の全単独解除とペアの一部標本が不変という範囲だけを使う。'
evidence: 原文監査 SUPPORTED / finite_complete_exhaustion
---

# 4×4はどの二つの禁止四点を同時解除しても後手勝ち

対象命題: 4×4はどの二つの禁止四点を同時解除しても後手勝ち。 前回の960ペア標本を全ペアへ強めた有限命題。

適用文脈: 起点: [個票10・B251〜B259](../../log/claim-audit/batch-10.md)。4×4の全単独解除とペアの一部標本が不変という範囲だけを使う。

現在の結論: 4×4全18721二禁止同時解除（2554 D4軌道）は空盤P。特定解除族の真部分集合だけの検査ではない。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
