---
id: K0191
title: 二点競合が森なら一つの三点制約によるnimber差は3以下
kind: proposition
status: refuted
topics:
- residual-games
- reconfiguration
aliases:
- B342
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
  note: B342の原文・定義（現在の結論は採用報告を優先）
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
evidence: 原文監査 REFUTED / finite_counterexample_with_forest_and_single_deletion
---

# 二点競合が森なら一つの三点制約によるnimber差は3以下

否定された命題: 二点競合が森なら一つの三点制約によるnimber差は3以下。 B341の強い影響が起きるためには、二点競合のサイクルが必要という限定版。

適用文脈: 起点: [個票03・B051〜B058](../../log/claim-audit/batch-03.md)、[個票04・B064〜B068](../../log/claim-audit/batch-04.md)。孤立点だけによる退化例は除いて考える。

現在の結論: 4×4 S=[0,2]のPは五辺マッチング。極小三点辺[1,10,12]のみ解除してg5→0、差5>3。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
