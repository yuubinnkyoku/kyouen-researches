---
id: K0137
title: 極大なのにすべての空点が二重以上に禁止される
kind: proposition
status: computed
topics:
- maximal-safe
- geometry
aliases:
- B077
relations:
- type: depends_on
  target: K0026
  note: ''
artifacts:
- path: research/experiments/original-claims/reports/round47-private-cover-and-global-minima.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/archive/hypothesis-ledgers/hypothesis-bank-2026-09-27.md
  role: source
  note: B077の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: 原文の指定有限盤・証人範囲
evidence: 原文監査 SUPPORTED / finite_witness_and_general_minimum_stone_count_proof
---

# 極大なのにすべての空点が二重以上に禁止される

対象命題: 極大なのにすべての空点が二重以上に禁止される。 `min_{p∉S}b_S(p)≥2` の安全極大集合がある。極大性に「唯一の理由で塞がる点」が必ずあるわけではない可能性。

現在の結論: 4×4の全空点二重以上六石証人・完全一重被覆五石証人を独立検算。曲線上界と残る小盤の全域検査で最小石数6/5、最小盤4を証明。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
