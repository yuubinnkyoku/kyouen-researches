---
id: K0196
title: 残余四点制約が効く最小局面は三点制約の例と別型
kind: proposition
status: proved
topics:
- residual-games
- reconfiguration
aliases:
- B349
relations:
- type: depends_on
  target: K0108
  note: ''
artifacts:
- path: research/experiments/original-claims/reports/round40-b349-minimum-four-edge-classification.md
  role: proof
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/archive/hypothesis-ledgers/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B349の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round40_classification_verified.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: '起点: [個票03・B051〜B058](../../log/claim-audit/batch-03.md)、[個票04・B064〜B068](../../log/claim-audit/batch-04.md)。孤立点だけによる退化例は除いて考える。'
evidence: 原文監査 SUPPORTED / general_minimum_classification_and_finite_realizations
---

# 残余四点制約が効く最小局面は三点制約の例と別型

対象命題: 残余四点制約が効く最小局面は三点制約の例と別型。 全三点制約を含めた近似でも値を外す最小|L|の局面を、有限個の抽象ハイパーグラフで分類できる。

適用文脈: 起点: [個票03・B051〜B058](../../log/claim-audit/batch-03.md)、[個票04・B064〜B068](../../log/claim-audit/batch-04.md)。孤立点だけによる退化例は除いて考える。

現在の結論: 二点競合ありで効く四点辺の最小合法点数は5、抽象九型を全分類し全型を整数格子で実現。競合なしも許すなら最小4・単独四点辺一型。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
