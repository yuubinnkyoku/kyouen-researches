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
- path: research/experiments/original-claims/reports/round28-seven-board-original-verdicts.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/archive/hypothesis-ledgers/hypothesis-bank-2026-09-27.md
  role: source
  note: B021の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round28_n7_audited.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round28_n7_layers.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round28_n7_independent.json
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

## 2026-10-17 bounded advance

New finite evidence: saturation onsets recomputed/verified for n=2..7: sigma_2=2, sigma_3=4, sigma_4=2, sigma_5=3, sigma_6=3, sigma_7=4; uniformity (K0041) verified n=2..7 (deficit non-increasing, post-sigma saturation). No counterexample in range. n=8 attempt (K_8=15, memo 2^25) did not finish; no sigma_8 claim.

Scope clarification: hypothesis sigma_n<=4 for n>=4 holds for all computed n>=4 (n=4..7). n=8+ uncomputed.

Next steps: complete or extend n=8 enumeration; seek general proof. Status remains open.

統合監査（2026-10-20）: 上記2026-10-17の追記はローカル研究時点の報告であり、今回すべての探索・測定を再実行したものではない。再検証の範囲は `research/experiments/local-main-integration-20261020/README.md` に記す。既存の未解決性・量化の限界を維持する。
