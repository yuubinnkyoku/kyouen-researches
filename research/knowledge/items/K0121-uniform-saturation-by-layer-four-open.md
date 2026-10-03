---
id: K0121
title: 飽和開始は4石以内
kind: question
status: open
topics:
- grundy
aliases:
- B021
relations:
- type: depends_on
  target: K0002
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
- path: research/hypothesis-bank-2026-09-27.md
  role: source
  note: B021の原文・定義（現在の結論は採用報告を優先）
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
scope: '`M_n(k)=max_{|S|=k}g(S)`、`σ_n=min{k:M_n(k)=K_n−k}`。上限と、一度等号なら後続層でも等号になることは既存結果であり、ここでは新規扱いしない。'
evidence: 原文監査 PARTIAL / finite_complete_classification
---

# 飽和開始は4石以内

未確定の命題: 飽和開始は4石以内。 `n≥4`で `σ_n≤4`。大きいnimberを作る核は盤サイズによらず少数の石で足りるかもしれない。

適用文脈: `M_n(k)=max_{|S|=k}g(S)`、`σ_n=min{k:M_n(k)=K_n−k}`。上限と、一度等号なら後続層でも等号になることは既存結果であり、ここでは新規扱いしない。

現在の結論: σ4=2、σ5=σ6=3、σ7=4は全数確認。全nでσn≤4とは証明していない。

採用境界: 7×7までの一石・飽和・J・空盤WFTを完全検査したが、原文の無界全称は未証明。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
