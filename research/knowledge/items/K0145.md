---
id: K0145
title: 10×10の最小極大は10石
kind: question
status: open
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
- path: research/verification/round56-ten-board-eight-stone-exclusion.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/hypothesis-bank-2026-09-27.md
  role: source
  note: B093の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: 本文の原文量化と現在の採用境界
evidence: 原文監査 PARTIAL / complete_eight_stone_prefix_suffix_exclusion_and_ten_stone_witness
---

# 10×10の最小極大は10石

未確定の命題: 10×10の最小極大は10石。 `s_10=10`。古い不安全な10石例は証拠に使わず、独立した予想としてのみ残す。

現在の結論: s10の現在範囲は9..10。八石全域を除外し十石証人を検算済みだが、九石の有無は未決。

採用境界: s9=9から十盤八石候補を全幅・初点0..4へ帰着。旧完了接頭部と今回全五再開部分を接続し八石全域除外、s10∈[9,10]。九石の有無が未決。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
