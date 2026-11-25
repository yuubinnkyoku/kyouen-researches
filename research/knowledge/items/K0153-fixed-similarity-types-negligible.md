---
id: K0153
title: 固定個数の相似型では大盤の大半を覆えない
kind: proposition
status: proved
topics:
- geometry
aliases:
- B150
relations: []
artifacts:
- path: research/experiments/original-claims/reports/round4-collinear-asymptotic.md
  role: proof
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/archive/hypothesis-ledgers/hypothesis-bank-2026-09-27.md
  role: source
  note: B150の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round4_collinear_asymptotic.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/scripts/round4_collinear_asymptotic.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: 有限サイズの `F_n/n^6` の見かけの安定だけを根拠に次数を固定しない。ここでは `F_n=|Q_n|`、`C_n`を非共線の共円四点組数、`D_n`を共線四点組数とする。
evidence: 原文監査 SUPPORTED / general_proof
---

# 固定個数の相似型では大盤の大半を覆えない

対象命題: 固定個数の相似型では大盤の大半を覆えない。 どの固定有限テンプレート族を選んでも、それが生成する禁止四点組の割合は0へ近づく。B149の有限サイズでの圧縮と両立する。

適用文脈: 有限サイズの `F_n/n^6` の見かけの安定だけを根拠に次数を固定しない。ここでは `F_n=|Q_n|`、`C_n`を非共線の共円四点組数、`D_n`を共線四点組数とする。

現在の結論: 固定した有限個の相似型の寄与はO(n^4)、全非共線共円四点数はΘ(n^5)。固定型の寄与割合は0へ行く。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
