---
id: K0248
title: 無作為k点の最初の禁止数はPoisson型になる
kind: proposition
status: proved
topics:
- geometry
- statistics
aliases:
- B478
relations: []
artifacts:
- path: research/verification/round13-poisson-limit.md
  role: proof
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B478の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/scripts/round13_asymptotic_checks.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: '起点: [個票08](verification/batch-08.md)。有限範囲の次数フィットは動機にとどめる。D_nを共線四点数、C_nを非共線共円四点数とする。'
evidence: 原文監査 SUPPORTED / general_proof_using_published_count
---

# 無作為k点の最初の禁止数はPoisson型になる

対象命題: 無作為k点の最初の禁止数はPoisson型になる。 `E[含まれる禁止四点数]→λ∈(0,∞)`となるk=k(n)の尺度で、禁止数がPoisson(λ)へ収束する。

適用文脈: 起点: [個票08](verification/batch-08.md)。有限範囲の次数フィットは動機にとどめる。D_nを共線四点数、C_nを非共線共円四点数とする。

現在の結論: 一様k=k(n)点でλ_n=F_n(k)_4/(n²)_4→λ∈(0,∞)を仮定。k=Θ(n^(3/4))、Poisson(λ_n)への全変動誤差O(n^(−1/4))、安全確率→e^(−λ)。固定整数kの極限ではない。Poisson(λ)への同誤差率はλ_nの収束速度なしには主張しない。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
