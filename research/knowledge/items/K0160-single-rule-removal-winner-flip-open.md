---
id: K0160
title: 禁止四点組一つを外すだけで空盤勝者が反転する
kind: question
status: open
topics:
- variants
aliases:
- B251
relations: []
artifacts:
- path: research/experiments/original-claims/reports/round32-b251-seven-board-exclusion.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/archive/hypothesis-ledgers/hypothesis-bank-2026-09-27.md
  role: source
  note: B251の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round32_b251_n7_audited.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round32_standard_pn_verified.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round32_b251_n7_geometry.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: この節では盤点を固定して禁止4点族だけを変える。標準版での局面ラベルをそのまま流用しない。
evidence: 原文監査 PARTIAL / finite_exhaustion
---

# 禁止四点組一つを外すだけで空盤勝者が反転する

未確定の命題: 禁止四点組一つを外すだけで空盤勝者が反転する。 ある正方形盤とe∈Q_nで、禁止をeだけ解除したゲームのP/Nが標準版と逆になる。

適用文脈: この節では盤点を固定して禁止4点族だけを変える。標準版での局面ラベルをそのまま流用しない。

現在の結論: n≤7では単一禁止四点解除による勝者反転を全域除外。n7全6364解除・935軌道を二方式検算したが、n≥8の存在証人はない。存在命題は未解決。

採用境界: 7×7全6364単独解除を935軌道・二方式で除外。共有標準表全179810350局面の証明条件も検算。存在証人はn≥8。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
