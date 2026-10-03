---
id: K0156
title: 長方形の例外初手は端からの距離で分類できる
kind: proposition
status: proved
topics:
- rectangles
- variants
aliases:
- B220
relations: []
artifacts:
- path: research/verification/round4-fixed-width.md
  role: proof
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/hypothesis-bank-2026-09-27.md
  role: source
  note: B220の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round4_fixed_width.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/scripts/round4_fixed_width.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: この節は同じ禁止ルールを`w×m`格子盤へ適用する。1×mの自明な固定手数ゲームを新発見候補として数えない。
evidence: 原文監査 SUPPORTED / general_proof
---

# 長方形の例外初手は端からの距離で分類できる

対象命題: 長方形の例外初手は端からの距離で分類できる。 固定幅wでは、十分長い盤のWは有限個の端パターンと内部の剰余パターンで記述できる。

適用文脈: この節は同じ禁止ルールを`w×m`格子盤へ適用する。1×mの自明な固定手数ゲームを新発見候補として数えない。

現在の結論: 全固定幅の一様終局定理。必要な短い二行盤と区間証人も全数検査。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
