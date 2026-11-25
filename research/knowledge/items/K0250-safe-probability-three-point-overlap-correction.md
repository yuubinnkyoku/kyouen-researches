---
id: K0250
title: 安全確率の最初の補正は三点共有の禁止ペアが決める
kind: proposition
status: proved
topics:
- geometry
- statistics
aliases:
- B480
relations: []
artifacts:
- path: research/experiments/original-claims/reports/round14-safety-correction.md
  role: proof
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/archive/hypothesis-ledgers/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B480の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round14_safety_correction.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/scripts/round14_safety_correction.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: '起点: [個票08](../../log/claim-audit/batch-08.md)。有限範囲の次数フィットは動機にとどめる。D_nを共線四点数、C_nを非共線共円四点数とする。'
evidence: 原文監査 SUPPORTED / general_asymptotic_expansion
---

# 安全確率の最初の補正は三点共有の禁止ペアが決める

対象命題: 安全確率の最初の補正は三点共有の禁止ペアが決める。 低密度の `log Pr(S安全)` を展開すると、単純な禁止数の平均の次に支配する項は、四点禁止どうしの三点共有数になる。

適用文脈: 起点: [個票08](../../log/claim-audit/batch-08.md)。有限範囲の次数フィットは動機にとどめる。D_nを共線四点数、C_nを非共線共円四点数とする。

現在の結論: k=Θ(n^(3/4))でlog Pr(安全)=−λ_n+[4ζ(3)/(45ζ(4))]k^5/n^4+O(n^(−3/8))。A3=10G5による補正は(2/5)A3(k/n²)^5で、単純なペア包含排除の係数を使わない。同曲線束をまとめた一様剰余評価を採用し、Poisson誤差率Θ(n^(−1/4))も鋭い。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
