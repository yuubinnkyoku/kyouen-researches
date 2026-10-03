---
id: K0249
title: 最初の禁止は単発でなく同じ円・直線の束として現れる
kind: proposition
status: refuted
topics:
- geometry
- statistics
aliases:
- B479
relations: []
artifacts:
- path: research/verification/round13-poisson-limit.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B479の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/scripts/round13_asymptotic_checks.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: '起点: [個票08](verification/batch-08.md)。有限範囲の次数フィットは動機にとどめる。D_nを共線四点数、C_nを非共線共円四点数とする。'
evidence: 原文監査 REFUTED / general_asymptotic_refutation
---

# 最初の禁止は単発でなく同じ円・直線の束として現れる

否定された命題: 最初の禁止は単発でなく同じ円・直線の束として現れる。 B478の競合として、同尺度の極限は非自明な複合Poisson分布となり、複数の四点違反が同時に生まれる割合が残る。

適用文脈: 起点: [個票08](verification/batch-08.md)。有限範囲の次数フィットは動機にとどめる。D_nを共線四点数、C_nを非共線共円四点数とする。

現在の結論: λ_nが正の有限値へ行く同じ閾値尺度で、複数禁止を同曲線上に作る束の確率は0へ行く。有限nの五個・十五個束は非自明な複合Poisson極限を示さない。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
