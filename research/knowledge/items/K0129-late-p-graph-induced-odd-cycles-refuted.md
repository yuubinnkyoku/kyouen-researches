---
id: K0129
title: 終盤のP(S)には大きな誘導奇サイクルがない
kind: proposition
status: refuted
topics:
- residual-games
- reconfiguration
aliases:
- B067
relations:
- type: depends_on
  target: K0108
  note: ''
artifacts:
- path: research/verification/round34-b067-induced-seven-cycle.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/hypothesis-bank-2026-09-27.md
  role: source
  note: B067の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round34_b067_verified.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/scripts/round34_b067_verify.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: 本文の原文量化と現在の採用境界
evidence: 原文監査 REFUTED / finite_counterexample_with_exact_height
---

# 終盤のP(S)には大きな誘導奇サイクルがない

否定された命題: 終盤のP(S)には大きな誘導奇サイクルがない。 `K(S)−|S|≤3` の局面で長さ7以上の誘導奇サイクルが現れない。円の交わり方から出る禁止構造の候補。

現在の結論: 4×4のh=3の局面で二点競合に弦なし誘導C7。全256拡張から真の高さを再計算し、旧K(S)バグの留保を解消した。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
