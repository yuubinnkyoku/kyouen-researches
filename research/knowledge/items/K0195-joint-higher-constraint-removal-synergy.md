---
id: K0195
title: 高階制約を二つ同時に外したときだけ値が変わる
kind: proposition
status: computed
topics:
- residual-games
- reconfiguration
aliases:
- B346
relations:
- type: depends_on
  target: K0108
  note: ''
artifacts:
- path: research/experiments/original-claims/reports/round37-residual-original-witness-audit.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/archive/hypothesis-ledgers/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B346の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round37_residual_witnesses_verified.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/scripts/round37_residual_witness_audit.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: '起点: [個票03・B051〜B058](../../log/claim-audit/batch-03.md)、[個票04・B064〜B068](../../log/claim-audit/batch-04.md)。孤立点だけによる退化例は除いて考える。'
evidence: 原文監査 SUPPORTED / finite_pair_synergy_witness
---

# 高階制約を二つ同時に外したときだけ値が変わる

対象命題: 高階制約を二つ同時に外したときだけ値が変わる。 単独除去はいずれもgを保存するが、同時除去はP/Nを反転する局面がある。

適用文脈: 起点: [個票03・B051〜B058](../../log/claim-audit/batch-03.md)、[個票04・B064〜B068](../../log/claim-audit/batch-04.md)。孤立点だけによる退化例は除いて考える。

現在の結論: 3×3 S=[0,1,4]の極小三点辺二つは、各単独解除ならg0、双方解除だけg3。冗長辺を操作した見かけの効果ではない。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
