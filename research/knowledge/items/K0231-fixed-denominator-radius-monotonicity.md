---
id: K0231
title: 分母qを固定した最良点数は半径の単調増加だけでは達成できない
kind: proposition
status: proved
topics:
- geometry
aliases:
- B456
relations: []
artifacts:
- path: research/verification/round11-circle-records.md
  role: proof
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B456の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round11_circle_records.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/scripts/round11_circle_records.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: '起点: [個票07・B131〜B137](verification/batch-07.md)。分母に対する単調性は捨てる。半径が同じだが片側が0点という退化比較も除き、双方4格子点以上の円を主に扱う。'
evidence: 原文監査 SUPPORTED / general_proof
---

# 分母qを固定した最良点数は半径の単調増加だけでは達成できない

対象命題: 分母qを固定した最良点数は半径の単調増加だけでは達成できない。 無限に多くの半径閾値で、既存最良円の整数拡大とは異なる算術型が必要になる。

適用文脈: 起点: [個票07・B131〜B137](verification/batch-07.md)。分母に対する単調性は捨てる。半径が同じだが片側が0点という退化比較も除き、双方4格子点以上の円を主に扱う。

現在の結論: 固定分母の記録円に必要な平方類が無限。過去の最良円の整数拡大を除外。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
