---
id: K0175
title: J_5の最小応答拠点は対角の角ペアで表せない
kind: proposition
status: computed
topics:
- residual-games
- first-moves
aliases:
- B308
relations:
- type: depends_on
  target: K0108
  note: ''
artifacts:
- path: research/verification/round27-fixed-response-audit.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B308の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round27_pairing_verified.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round27_pairing_audited.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round27_response_graphs.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: '起点: [個票01・B011〜B020](verification/batch-01.md)。既知の連結性・完全マッチング・Aut=D4そのものは再提案しない。'
evidence: 原文監査 SUPPORTED / finite_complete_classification_and_witness
---

# J_5の最小応答拠点は対角の角ペアで表せない

対象命題: J_5の最小応答拠点は対角の角ペアで表せない。 どの初手にも隣接する拠点が必要な「全域支配」の最小解は、角だけを選ぶ方法とは異なる点を必要とする。

適用文脈: 起点: [個票01・B011〜B020](verification/batch-01.md)。既知の連結性・完全マッチング・Aut=D4そのものは再提案しない。

現在の結論: 全域支配数は8、最小集合18個。対角の四隅ペア二点は全域支配集合でない。閉近傍支配との混同を避ける。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
