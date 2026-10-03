---
id: K0258
title: 一つの真円の制約を全部解除しても4×4の空盤勝者は変わらない
kind: proposition
status: refuted
topics:
- variants
aliases:
- B525
relations: []
artifacts:
- path: research/verification/round22-b252-one-circle-versus-scattered.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B525の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round22_b252_verified.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round22_b252_n4_all_geometry.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round22_b252_n4_all_scan.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: '起点: [個票10・B251〜B259](verification/batch-10.md)。4×4の全単独解除とペアの一部標本が不変という範囲だけを使う。'
evidence: 原文監査 REFUTED / finite_whole_circle_counterexample
---

# 一つの真円の制約を全部解除しても4×4の空盤勝者は変わらない

否定された命題: 一つの真円の制約を全部解除しても4×4の空盤勝者は変わらない。 四点単独より大きい解除でも同じ円の束なら頑健という候補。

適用文脈: 起点: [個票10・B251〜B259](verification/batch-10.md)。4×4の全単独解除とペアの一部標本が不変という範囲だけを使う。

現在の結論: 4×4中央八点真円の全70禁止を解除するとg0→1。単独四点解除の結果と丸ごと円解除を混同しない。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
