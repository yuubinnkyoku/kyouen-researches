---
id: K0123
title: 2点制約だけの対称P局面は対合証明を持つ
kind: proposition
status: refuted
topics:
- residual-games
- reconfiguration
aliases:
- B047
relations:
- type: depends_on
  target: K0108
  note: ''
artifacts:
- path: research/experiments/original-claims/reports/round31-b047-odd-cycle-counterexample.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/archive/hypothesis-ledgers/hypothesis-bank-2026-09-27.md
  role: source
  note: B047の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round31_b047_odd_cycle.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/scripts/round31_b047_odd_cycle.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: 本文の原文量化と現在の採用境界
evidence: 原文監査 REFUTED / finite_counterexample_with_exact_residual_game
---

# 2点制約だけの対称P局面は対合証明を持つ

否定された命題: 2点制約だけの対称P局面は対合証明を持つ。 R(S)が2点集合のみで、P(S)が頂点推移的かつg(S)=0なら、固定ペア応答でPを証明できる。

現在の結論: 5×5安全六石から二点制約だけの残余C5を実現。頂点推移的Pで合法五点なので固定点なし応答対合は不可能。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
