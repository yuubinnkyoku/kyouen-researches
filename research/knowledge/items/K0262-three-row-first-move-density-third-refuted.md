---
id: K0262
title: 部分勝ちとなる三行盤の勝ち初手密度は1/3へ近づく
kind: proposition
status: refuted
topics:
- rectangles
- variants
aliases:
- B555
relations: []
artifacts:
- path: research/experiments/original-claims/reports/round4-fixed-width.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/archive/hypothesis-ledgers/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B555の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round4_fixed_width.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/scripts/round4_fixed_width.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: この節の盤は `{0,…,m−1}×{0,…,w−1}`。個票09の小さい長方形での一致は動機にとどめ、周期性の証明を引き継がない。
evidence: 原文監査 REFUTED / general_impossibility
---

# 部分勝ちとなる三行盤の勝ち初手密度は1/3へ近づく

否定された命題: 部分勝ちとなる三行盤の勝ち初手密度は1/3へ近づく。 B554の点ごとの式より弱く、長さ方向にまばらな例外列だけが加わるという密度予想。

適用文脈: この節の盤は `{0,…,m−1}×{0,…,w−1}`。個票09の小さい長方形での一致は動機にとどめ、周期性の証明を引き継がない。

現在の結論: 標準三行盤は十分大mで全初手勝ち、勝ち初手密度は1。部分勝ち盤の密度が1/3へ行くという外挿は不成立。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
