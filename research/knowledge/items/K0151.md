---
id: K0151
title: 非共線共円四点組はn^(4+o(1))
kind: proposition
status: refuted
topics:
- geometry
aliases:
- B142
relations: []
artifacts:
- path: research/verification/round17-original-scope-audit.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/hypothesis-bank-2026-09-27.md
  role: source
  note: B142の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: 有限サイズの `F_n/n^6` の見かけの安定だけを根拠に次数を固定しない。ここでは `F_n=|Q_n|`、`C_n`を非共線の共円四点組数、`D_n`を共線四点組数とする。
evidence: 原文監査 REFUTED / general_asymptotic_refutation_using_published_theorem
---

# 非共線共円四点組はn^(4+o(1))

否定された命題: 非共線共円四点組はn^(4+o(1))。 `C_n=n^(4+o(1))`。円の格子算術による約数的増加が、独立な自由度の一つより小さい可能性。

適用文脈: 有限サイズの `F_n/n^6` の見かけの安定だけを根拠に次数を固定しない。ここでは `F_n=|Q_n|`、`C_n`を非共線の共円四点組数、`D_n`を共線四点組数とする。

現在の結論: 公刊定理を採用した非共線共円四点数C_n=Θ(n^5)が反証根拠。旧Θ(n^6)主張を復活させない。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
