---
id: K0135
title: 幾何によりB072より厳しい線形上限がある
kind: proposition
status: refuted
topics:
- maximal-safe
- geometry
aliases:
- B074
relations:
- type: depends_on
  target: K0026
  note: ''
artifacts:
- path: research/verification/round5-quadratic-cover.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/hypothesis-bank-2026-09-27.md
  role: source
  note: B074の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round5_quadratic_cover.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/scripts/round5_quadratic_cover.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: 本文の原文量化と現在の採用境界
evidence: 原文監査 REFUTED / infinite_counterexample_family
---

# 幾何によりB072より厳しい線形上限がある

否定された命題: 幾何によりB072より厳しい線形上限がある。 全安全Sと空点pに対して `b_S(p)≤C|S|` となる絶対定数Cがある。B073の大規模な延長と競合する。

現在の結論: 安全格子の無限族でb/k→∞、絶対定数の線形上界を反証。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
