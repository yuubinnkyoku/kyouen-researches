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
- type: depends_on
  target: K0106
  note: 固定qの指数下界は対応する上界を与えない
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
- path: research/saturation-20261003.md
  role: proof
  note: 直線被覆係数の改善と全固定qへの指数下界の拡張
- path: research/geometry-20261003.md
  role: proof
  note: §10の整数平方完成ノルム上界2(n-1)^6
scope: 標準q=4の漸近指数の等号。全固定qへの下界拡張とは別。
evidence: 原文監査 PARTIAL / general_asymptotic_lower_exponent_proof
---

# 最小極大の指数は2/3

標準q=4でs_n=n^(2/3+o(1))かは未確定。下界liminf log(s_n)/log n≥2/3は一般証明済みで、全固定q≥4にも拡張された。等号には対応する上界が必要である。

最新成果は直線被覆の係数と円の整数平方完成ノルム上界を改善する。円も禁止する標準版へline-only版の主定数を移せず、これらから指数2/3の上界も出ない。
