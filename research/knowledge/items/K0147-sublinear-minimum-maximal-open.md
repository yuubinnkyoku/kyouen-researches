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
- type: depends_on
  target: K0106
  note: 固定qの指数下界は対応する上界を与えない
- type: depends_on
  target: K0320
  note: 有限n=11..15の構成はo(n)の上界ではない
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
- path: research/saturation-20261003.md
  role: proof
  note: 直線被覆係数の改善と全固定qへの指数下界の拡張
- path: research/geometry-20261003.md
  role: proof
  note: §10の整数平方完成ノルム上界2(n-1)^6
- path: research/verification/scripts/saturation_20261003_verified.json
  role: data
  note: n=11..15のn-1石極大証人の独立検査
scope: 標準q=4正方形盤でn→∞の全系列についてs_n/n→0となるか。
evidence: 原文監査 PARTIAL / general_asymptotic_lower_exponent_proof
---

# 最小極大は線形より小さくなる

標準q=4の最小極大サイズについてs_n=o(n)かは未証明。任意のε>0に対する十分大きいnでの下界s_n>n^(2/3−ε)は証明済みだが、必要なのは線形未満の上界構成である。

最新の独立検査済み構成ではn=11..15にn−1石極大が存在する。s_11≤10<11は確定するが、有限のn−1例をs_n/n→0の証明と解釈しない。

直線被覆係数の改善・円の平方完成ノルム上界2(n−1)^6も下界側の改良であり、本問を閉じない。
