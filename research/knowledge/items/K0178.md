---
id: K0178
title: 後手勝ち正方形盤のJ_nには完全マッチングまたは一頂点だけ余すマッチングがある
kind: proposition
status: refuted
topics:
- residual-games
- first-moves
aliases:
- B313
relations:
- type: depends_on
  target: K0108
  note: ''
artifacts:
- path: research/verification/round28-seven-board-original-verdicts.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B313の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round28_n7_audited.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round28_n7_layers.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round28_n7_independent.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: '起点: [個票01](verification/batch-01.md)。拠点自身への初手にも返せるよう、閉近傍による支配と全域支配を分ける。'
evidence: 原文監査 REFUTED / finite_counterexample_and_complete_verification
---

# 後手勝ち正方形盤のJ_nには完全マッチングまたは一頂点だけ余すマッチングがある

否定された命題: 後手勝ち正方形盤のJ_nには完全マッチングまたは一頂点だけ余すマッチングがある。 偶数nでは全頂点、奇数nではn²−1頂点を覆える。

適用文脈: 起点: [個票01](verification/batch-01.md)。拠点自身への初手にも返せるよう、閉近傍による支配と全域支配を分ける。

現在の結論: J7の四隅は唯一の隣接先が中央24。最大マッチング23辺であり、48頂点を覆う24辺近完全マッチングはない。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
