---
id: K0265
title: 3w石の配置は行ごとに等差数列を置く構成で達成できる
kind: proposition
status: proved
topics:
- rectangles
- variants
aliases:
- B558
relations: []
artifacts:
- path: research/experiments/original-claims/reports/round8-ap-quadratic-prime.md
  role: proof
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/archive/hypothesis-ledgers/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B558の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round8_ap_prime.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/scripts/round8_ap_prime.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: この節の盤は `{0,…,m−1}×{0,…,w−1}`。個票09の小さい長方形での一致は動機にとどめ、周期性の証明を引き継がない。
evidence: 原文監査 SUPPORTED / general_proof
---

# 3w石の配置は行ごとに等差数列を置く構成で達成できる

対象命題: 3w石の配置は行ごとに等差数列を置く構成で達成できる。 行ごとの初項と公差を適切に選べば、mがwの二次以下の範囲で共円・共線をすべて回避できる。

適用文脈: この節の盤は `{0,…,m−1}×{0,…,w−1}`。個票09の小さい長方形での一致は動機にとどめ、周期性の証明を引き継がない。

現在の結論: 行ごとの素数公差の三点等差列で、全固定wに幅O(w²)の安全3w石構成がある。公差1の旧未証明候補とは別の証明済み構成。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
