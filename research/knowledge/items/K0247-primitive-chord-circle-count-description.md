---
id: K0247
title: 円を半径でなく弦の原始型で分解すると重複の少ない式が得られる
kind: proposition
status: proved
topics:
- geometry
- statistics
aliases:
- B477
relations: []
artifacts:
- path: research/experiments/original-claims/reports/round15-standard-chord.md
  role: proof
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/archive/hypothesis-ledgers/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B477の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round15_standard_chord.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/scripts/round15_standard_chord.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: '起点: [個票08](../../log/claim-audit/batch-08.md)。有限範囲の次数フィットは動機にとどめる。D_nを共線四点数、C_nを非共線共円四点数とする。'
evidence: 原文監査 SUPPORTED / general_identity
---

# 円を半径でなく弦の原始型で分解すると重複の少ない式が得られる

対象命題: 円を半径でなく弦の原始型で分解すると重複の少ない式が得られる。 一本の標準弦を各四点組へ一意に割り当てることで、円中心分母の和を扱いやすい算術和に変換できる。

適用文脈: 起点: [個票08](../../log/claim-audit/batch-08.md)。有限範囲の次数フィットは動機にとどめる。D_nを共線四点数、C_nを非共線共円四点数とする。

現在の結論: 標準弦の原始方向・整数内積・既約分数による重複なし計数。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
