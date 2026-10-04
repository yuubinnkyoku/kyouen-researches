---
id: K0261
title: 3対3の安全配置は一方の行を平行移動しても安全な区間を多数持つ
kind: proposition
status: proved
topics:
- rectangles
- variants
aliases:
- B546
relations: []
artifacts:
- path: research/experiments/original-claims/reports/round4-fixed-width.md
  role: proof
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/archive/hypothesis-ledgers/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B546の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round4_fixed_width.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/scripts/round4_fixed_width.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: 盤は `{0,…,m−1}×{0,1}`。各行の占有集合をA,B、行内の異なる二点の和集合をΣ₂(A),Σ₂(B)とする。各行高々3点とペア和衝突回避という既知の記述を出発点にする。
evidence: 原文監査 SUPPORTED / general_proof
---

# 3対3の安全配置は一方の行を平行移動しても安全な区間を多数持つ

対象命題: 3対3の安全配置は一方の行を平行移動しても安全な区間を多数持つ。 固定A,Bで、許される整数ずらし量が互いに離れた3区間以上へ分かれる。

適用文脈: 盤は `{0,…,m−1}×{0,1}`。各行の占有集合をA,B、行内の異なる二点の和集合をΣ₂(A),Σ₂(B)とする。各行高々3点とペア和衝突回避という既知の記述を出発点にする。

現在の結論: 全固定幅の一様終局定理。必要な短い二行盤と区間証人も全数検査。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
