---
id: K0152
title: 共線数の主項定数を原始方向の収束級数で書ける
kind: proposition
status: proved
topics:
- geometry
aliases:
- B145
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
  note: B145の原文・定義（現在の結論は採用報告を優先）
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

# 共線数の主項定数を原始方向の収束級数で書ける

対象命題: 共線数の主項定数を原始方向の収束級数で書ける。 D_nの有限和から、方向ごとの寄与を重複なく整理して明示的な定数を得られる。次数の予想B141とは別に、係数を狙う。

適用文脈: 有限サイズの `F_n/n^6` の見かけの安定だけを根拠に次数を固定しない。ここでは `F_n=|Q_n|`、`C_n`を非共線の共円四点組数、`D_n`を共線四点組数とする。

現在の結論: 整数方向別の恒等式と一様誤差による漸近証明。B141の旧REFUTEDを訂正。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
