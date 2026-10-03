---
id: K0144
title: 少数の代数曲線の和で漸近最適になる
kind: proposition
status: refuted
topics:
- maximum-safe
- geometry
aliases:
- B089
relations:
- type: depends_on
  target: K0026
  note: ''
artifacts:
- path: research/verification/round17-b089-bounded-degree.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/hypothesis-bank-2026-09-27.md
  role: source
  note: B089の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round17_b089_curves.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/scripts/round17_b089_curves.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: 本文の原文量化と現在の採用境界
evidence: 原文監査 REFUTED / general_asymptotic_refutation
---

# 少数の代数曲線の和で漸近最適になる

否定された命題: 少数の代数曲線の和で漸近最適になる。 定数個の二次または三次曲線上の点を選ぶ構成で、K_nとの差がo(n)になる。

現在の結論: 固定本数低次数曲線のo(n)上界と素数盤のK_n線形下界。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
