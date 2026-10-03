---
id: K0244
title: 共線数の有限サイズ補正を境界長とgcd和へ分けられる
kind: proposition
status: proved
topics:
- geometry
aliases:
- B473
relations: []
artifacts:
- path: research/verification/round4-collinear-asymptotic.md
  role: proof
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B473の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round4_collinear_asymptotic.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/scripts/round4_collinear_asymptotic.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: '起点: [個票08](verification/batch-08.md)。有限範囲の次数フィットは動機にとどめる。D_nを共線四点数、C_nを非共線共円四点数とする。'
evidence: 原文監査 SUPPORTED / general_proof
---

# 共線数の有限サイズ補正を境界長とgcd和へ分けられる

対象命題: 共線数の有限サイズ補正を境界長とgcd和へ分けられる。 主項の候補だけでなく、次項を `n^4` と対数・約数和の組合せで記述し、小盤の見かけの成長率の上昇を説明できる。

適用文脈: 起点: [個票08](verification/batch-08.md)。有限範囲の次数フィットは動機にとどめる。D_nを共線四点数、C_nを非共線共円四点数とする。

現在の結論: 共線D_nの主項は7ζ(2)/(60ζ(3))n^5、次項は−3/(4ζ(2))n^4 log n、剰余O(n^4)。旧F-Wのn6フィットを漸近定理にしない。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
