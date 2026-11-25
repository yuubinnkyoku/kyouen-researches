---
id: K0172
title: J_5の完全マッチングにはD4不変なものがない
kind: proposition
status: computed
topics:
- residual-games
- first-moves
aliases:
- B305
relations:
- type: depends_on
  target: K0108
  note: ''
artifacts:
- path: research/experiments/original-claims/reports/round27-fixed-response-audit.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/archive/hypothesis-ledgers/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B305の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round27_pairing_verified.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round27_pairing_audited.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round27_response_graphs.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: '起点: [個票01・B011〜B020](../../log/claim-audit/batch-01.md)。既知の連結性・完全マッチング・Aut=D4そのものは再提案しない。'
evidence: 原文監査 SUPPORTED / finite_complete_classification_and_witness
---

# J_5の完全マッチングにはD4不変なものがない

対象命題: J_5の完全マッチングにはD4不変なものがない。 全盤の対称性を保つ単一の応答表は作れず、ペアを選ぶ段階で向きを選ぶ必要がある。

適用文脈: 起点: [個票01・B011〜B020](../../log/claim-audit/batch-01.md)。既知の連結性・完全マッチング・Aut=D4そのものは再提案しない。

現在の結論: 完全マッチングは正確に二つで、いずれもD4不変ではない。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
