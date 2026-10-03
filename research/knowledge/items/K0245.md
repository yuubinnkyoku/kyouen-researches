---
id: K0245
title: 点数が固定の円が共円四点数の正の割合を担う
kind: proposition
status: proved
topics:
- geometry
- statistics
aliases:
- B475
relations: []
artifacts:
- path: research/verification/round13-four-point-circles.md
  role: proof
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B475の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/scripts/round13_asymptotic_checks.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: '起点: [個票08](verification/batch-08.md)。有限範囲の次数フィットは動機にとどめる。D_nを共線四点数、C_nを非共線共円四点数とする。'
evidence: 原文監査 SUPPORTED / general_proof_using_published_count
---

# 点数が固定の円が共円四点数の正の割合を担う

対象命題: 点数が固定の円が共円四点数の正の割合を担う。 ある定数m_0があり、盤内点数m_0以下の円からのC_nへの寄与のliminfが正になる。

適用文脈: 起点: [個票08](verification/batch-08.md)。有限範囲の次数フィットは動機にとどめる。D_nを共線四点数、C_nを非共線共円四点数とする。

現在の結論: 四点寄与で円を重み付けすると盤内格子点数は4へ集中し、Pr(点数≥5)=O_ε(n^(−11/29+ε))。円全体の完全整数点数ではない。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
