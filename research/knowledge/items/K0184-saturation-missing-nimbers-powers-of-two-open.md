---
id: K0184
title: 飽和開始層で欠ける正のnimberは2の冪だけ
kind: question
status: open
topics:
- grundy
aliases:
- B322
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
- path: research/archive/hypothesis-ledgers/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B322の原文・定義（現在の結論は採用報告を優先）
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
scope: '起点: [個票02・B025〜B030](../../log/claim-audit/batch-02.md)。飽和開始の次層以降が埋まるというmexの直接帰結は新仮説に数えない。'
evidence: 原文監査 PARTIAL / finite_complete_classification
---

# 飽和開始層で欠ける正のnimberは2の冪だけ

未確定の命題: 飽和開始層で欠ける正のnimberは2の冪だけ。 n=4の1,4、n=6の4という穴を、xorの二進構造に結びつける候補。

適用文脈: 起点: [個票02・B025〜B030](../../log/claim-audit/batch-02.md)。飽和開始の次層以降が埋まるというmexの直接帰結は新仮説に数えない。

現在の結論: n7飽和開始k4には正の穴がない。全盤で穴が二冪だけという一般則は未証明。

採用境界: 7×7までの一石・飽和・J・空盤WFTを完全検査したが、原文の無界全称は未証明。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。

## 2026-10-17 bounded advance

New finite evidence: n=2..7 saturation-start missing positive nimbers all powers of two (n=4->{1,4}, n=6->{4}, others vacuous). Layer histograms recorded. Machine-readable recomputation in research/experiments/local-main-integration-20261020/source/K0184_calc.json.

Scope clarification: finite-case evidence only; no n>=8 complete saturation data.

Next steps: obtain n>=8 saturation-start histograms. Status remains open.

統合監査（2026-10-20）: 上記2026-10-17の追記はローカル研究時点の報告であり、今回すべての探索・測定を再実行したものではない。再検証の範囲は `research/experiments/local-main-integration-20261020/README.md` に記す。既存の未解決性・量化の限界を維持する。
