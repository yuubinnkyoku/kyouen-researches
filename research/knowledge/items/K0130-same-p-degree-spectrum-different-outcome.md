---
id: K0130
title: 同じP(S)の次数列・スペクトルでも勝敗が違う
kind: proposition
status: computed
topics:
- residual-games
- reconfiguration
aliases:
- B068
relations:
- type: depends_on
  target: K0108
  note: ''
artifacts:
- path: research/experiments/original-claims/reports/round34-b068-cospectral-opposite-games.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/archive/hypothesis-ledgers/hypothesis-bank-2026-09-27.md
  role: source
  note: B068の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round34_b068_verified.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/scripts/round34_b068_search.cpp
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/scripts/round34_b068_verify.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: 原文の指定有限盤・証人範囲
evidence: 原文監査 SUPPORTED / finite_cospectral_witness_pair
---

# 同じP(S)の次数列・スペクトルでも勝敗が違う

対象命題: 同じP(S)の次数列・スペクトルでも勝敗が違う。 3点以上の残余制約がない局面に限定して、P(S)が同スペクトルだがgの零非零が異なる組がある。

現在の結論: 6×6の二点残余のみの八頂点対は次数列・厳密特性多項式が同じでg=3対0。各256拡張と行列式を独立検算済み。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
