---
id: K0145
title: 10×10の最小極大は10石
kind: question
status: superseded
topics:
- maximal-safe
- geometry
aliases:
- B093
relations:
- type: depends_on
  target: K0026
  note: ''
artifacts:
- path: research/experiments/original-claims/reports/round56-ten-board-eight-stone-exclusion.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/archive/hypothesis-ledgers/hypothesis-bank-2026-09-27.md
  role: source
  note: B093の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/knowledge/items/K0034-n10-minimum-maximal-bounds.md
  role: source
  note: 九石全域排除により本問いを解消した現行命題
scope: 本文の原文量化と現在の採用境界
evidence: resolved_by_K0034_nine_stone_exhaustive_exclusion
---

# 10×10の最小極大は10石（問いは解消）

未確定の命題: 10×10の最小極大は10石。 `s_10=10`。古い不安全な10石例は証拠に使わず、独立した予想としてのみ残す。

**解消（2026-10-16）**: K0034 が九石の有無を全域完全列挙で決着。D4第一石代表15点の全探索で九石の極大安全集合は存在せず、十石証人（round49、および別途再発見された `13 50 56 59 63 68 77 83 85 98`）と合わせて s_10=10。経緯と証拠の詳細は research/experiments/n10-nine-stone-sat-20261016/ を参照。

採用境界: s9=9から十盤八石候補を全幅・初点0..4へ帰着し八石全域除外、九石も D4 代表15点の完全列挙で除外。s10=10。
