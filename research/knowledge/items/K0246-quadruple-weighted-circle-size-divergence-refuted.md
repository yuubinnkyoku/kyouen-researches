---
id: K0246
title: 四点寄与で重み付けすると円上点数は発散する
kind: proposition
status: refuted
topics:
- geometry
- statistics
aliases:
- B476
relations: []
artifacts:
- path: research/verification/round13-four-point-circles.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B476の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/scripts/round13_asymptotic_checks.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: '起点: [個票08](verification/batch-08.md)。有限範囲の次数フィットは動機にとどめる。D_nを共線四点数、C_nを非共線共円四点数とする。'
evidence: 原文監査 REFUTED / general_asymptotic_refutation
---

# 四点寄与で重み付けすると円上点数は発散する

否定された命題: 四点寄与で重み付けすると円上点数は発散する。 C_nの四点組を一様に選び、その円上の盤点数を測ると、任意の固定m以下である確率が0へ向かう。B475と競合する。

適用文脈: 起点: [個票08](verification/batch-08.md)。有限範囲の次数フィットは動機にとどめる。D_nを共線四点数、C_nを非共線共円四点数とする。

現在の結論: 四点重み付きの盤内点数平均は4へ収束、全ての固定モーメントの余分も0へ行くので発散説は偽。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
