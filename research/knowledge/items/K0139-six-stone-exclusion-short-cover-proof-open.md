---
id: K0139
title: 六石非存在は三つ組の共起だけで短く説明できる
kind: question
status: open
topics:
- maximal-safe
- geometry
aliases:
- B079
relations:
- type: depends_on
  target: K0026
  note: ''
artifacts:
- path: research/verification/round48-six-stone-cover-incidence.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/hypothesis-bank-2026-09-27.md
  role: source
  note: B079の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: 本文の原文量化と現在の採用境界
evidence: 原文監査 PARTIAL / exact_geometric_cover_incidence_maximization
---

# 六石非存在は三つ組の共起だけで短く説明できる

未確定の命題: 六石非存在は三つ組の共起だけで短く説明できる。 10×10の安全6点集合が全面を塞げないことを、三つ組ごとの補完数と交差制約の有限個の不等式で示せる。全局面の列挙に依存しない証明候補。

現在の結論: 10×10六石の重複込み補完総数の全安全集合最大は85<必要94。しかし85上界の採用根拠は完全最適化であり、非列挙の短い構造証明は未完成。

採用境界: 十盤六石の重複被覆総数は全安全集合最大85<必要94、等号証人を独立検算。上界は完全最適化に依存し、原文の短い非列挙証明は未達。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
