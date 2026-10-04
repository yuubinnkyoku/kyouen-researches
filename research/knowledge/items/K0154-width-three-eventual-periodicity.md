---
id: K0154
title: 幅3で既に最終周期性が破れる
kind: proposition
status: refuted
topics:
- rectangles
- variants
aliases:
- B213
relations: []
artifacts:
- path: research/experiments/original-claims/reports/round4-fixed-width.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/archive/hypothesis-ledgers/hypothesis-bank-2026-09-27.md
  role: source
  note: B213の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round4_fixed_width.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/scripts/round4_fixed_width.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: この節は同じ禁止ルールを`w×m`格子盤へ適用する。1×mの自明な固定手数ゲームを新発見候補として数えない。
evidence: 原文監査 REFUTED / general_impossibility
---

# 幅3で既に最終周期性が破れる

否定された命題: 幅3で既に最終周期性が破れる。 B212への競合候補として、3×mの勝敗またはnimber列が最終周期的ではない。

適用文脈: この節は同じ禁止ルールを`w×m`格子盤へ適用する。1×mの自明な固定手数ゲームを新発見候補として数えない。

現在の結論: 固定幅の全極大サイズ3w・全局面偶奇式により、原文の無限量化を除外。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
