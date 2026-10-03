---
id: K0124
title: 同じ残余ゲームを与える占有集合は交換でつながる
kind: proposition
status: refuted
topics:
- residual-games
- reconfiguration
aliases:
- B057
relations:
- type: depends_on
  target: K0108
  note: ''
artifacts:
- path: research/verification/round42-exact-residual-family-audit.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/hypothesis-bank-2026-09-27.md
  role: source
  note: B057の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round42_families_verified.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/scripts/round42_families_audit.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: 本文の原文量化と現在の採用境界
evidence: 原文監査 REFUTED / complete_exact_family_counterexample
---

# 同じ残余ゲームを与える占有集合は交換でつながる

否定された命題: 同じ残余ゲームを与える占有集合は交換でつながる。 固定n,kで同一のR(S)を与えるSの族が、安全な1点移動で連結になる。成立すれば冗長な石配置の自由度を整理できる。

現在の結論: 4×4四石・同一L/Rの完全族は二集合のみ。三石交換が必要、Rは連結な四点パス。全65536集合から抽出。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
