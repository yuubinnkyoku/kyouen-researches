---
id: K0148
title: 最小極大の指数は2/3
kind: question
status: open
topics:
- maximal-safe
- geometry
aliases:
- B096
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
  note: B096の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: 本文の原文量化と現在の採用境界
evidence: 原文監査 PARTIAL / general_asymptotic_lower_exponent_proof
---

# 最小極大の指数は2/3

未確定の命題: 最小極大の指数は2/3。 `s_n=n^(2/3+o(1))`。通常の空点を覆う三つ組の個数と、必要な被覆点数n²のつり合いに着想を得た尺度候補。

現在の結論: s_n>n^(2/3−ε)は全ε>0・十分大nで成立。指数の等号s_n=n^(2/3+o(1))は対応上界がなく未確定。

採用境界: 原始方向別に直線被覆O(n k^(3/2))、三点真円の整数係数と約数上界でR(n)=n^o(1)。全ε>0でs_n>n^(2/3−ε)を証明。対応する上界・s_n=o(n)は未証明。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
