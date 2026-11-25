---
id: K0122
title: T*(S)に同じ偶奇の穴は開かない
kind: proposition
status: refuted
topics:
- strategy-length
- grundy
aliases:
- B031
relations:
- type: depends_on
  target: K0049
  note: ''
artifacts:
- path: research/experiments/original-claims/reports/round25-forced-length-holes.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/archive/hypothesis-ledgers/hypothesis-bank-2026-09-27.md
  role: source
  note: B031の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round25_forced_verified.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round25_forced_n6.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/scripts/round25_forced_lengths.cpp
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: 本文の原文量化と現在の採用境界
evidence: 原文監査 REFUTED / finite_counterexample_and_minimum_board_proof
---

# T*(S)に同じ偶奇の穴は開かない

否定された命題: T*(S)に同じ偶奇の穴は開かない。 `a,b∈T*(S),a<b` なら `a,a+2,…,b` がすべてT*(S)に入る。存在する終局サイズの穴と、戦略上の穴を分ける。

現在の結論: n6にT*={7,11}の局面があり、同偶奇の9が欠ける。旧n5のT*={6,7,9}は偶奇不変則と矛盾する無効な反例。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
