---
id: K0263
title: 三行盤で周期が続いても勝ち初手集合の幾何は非周期になる
kind: proposition
status: refuted
topics:
- rectangles
- variants
aliases:
- B556
relations: []
artifacts:
- path: research/verification/round4-fixed-width.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B556の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round4_fixed_width.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/scripts/round4_fixed_width.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: この節の盤は `{0,…,m−1}×{0,…,w−1}`。個票09の小さい長方形での一致は動機にとどめ、周期性の証明を引き継がない。
evidence: 原文監査 REFUTED / general_impossibility
---

# 三行盤で周期が続いても勝ち初手集合の幾何は非周期になる

否定された命題: 三行盤で周期が続いても勝ち初手集合の幾何は非周期になる。 空盤gは同じ3周期だが、Wの端パターン・内部剰余パターンの記述には成長する数の例外が必要になる。

適用文脈: この節の盤は `{0,…,m−1}×{0,…,w−1}`。個票09の小さい長方形での一致は動機にとどめ、周期性の証明を引き継がない。

現在の結論: 標準三行盤は十分大mで全初手勝ちになるため、原文の最終非周期性はない。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
