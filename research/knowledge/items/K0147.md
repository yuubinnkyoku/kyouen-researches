---
id: K0147
title: 最小極大は線形より小さくなる
kind: question
status: open
topics:
- maximal-safe
- geometry
aliases:
- B095
relations:
- type: depends_on
  target: K0026
  note: ''
artifacts:
- path: research/verification/round52-general-saturation-exponent-lower-bound.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/hypothesis-bank-2026-09-27.md
  role: source
  note: B095の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: 本文の原文量化と現在の採用境界
evidence: 原文監査 PARTIAL / general_asymptotic_lower_exponent_proof
---

# 最小極大は線形より小さくなる

未確定の命題: 最小極大は線形より小さくなる。 `s_n/n→0`。小盤の `s_n≈n` は過渡現象で、三つ組の被覆能力が大盤で勝るかもしれない。

現在の結論: 下界liminf log(s_n)/log n≥2/3は一般証明済み。s_n=o(n)には上界が必要で、これは未証明。

採用境界: 原始方向別に直線被覆O(n k^(3/2))、三点真円の整数係数と約数上界でR(n)=n^o(1)。全ε>0でs_n>n^(2/3−ε)を証明。対応する上界・s_n=o(n)は未証明。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
