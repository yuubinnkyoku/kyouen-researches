---
id: K0230
title: q≥3の多数点円は、整数中心円の剰余類選択として最適に記述できる
kind: proposition
status: refuted
topics:
- geometry
aliases:
- B455
relations: []
artifacts:
- path: research/experiments/original-claims/reports/round11-residue-orbits.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/archive/hypothesis-ledgers/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B455の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round11_circle_records.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/scripts/round11_circle_records.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: '起点: [個票07・B131〜B137](../../log/claim-audit/batch-07.md)。分母に対する単調性は捨てる。半径が同じだが片側が0点という退化比較も除き、双方4格子点以上の円を主に扱う。'
evidence: 原文監査 REFUTED / general_impossibility
---

# q≥3の多数点円は、整数中心円の剰余類選択として最適に記述できる

否定された命題: q≥3の多数点円は、整数中心円の剰余類選択として最適に記述できる。 ある最良円族で、通分した二平方和表現の特定の一剰余類が、他の全剰余類より一貫して多い。

適用文脈: 起点: [個票07・B131〜B137](../../log/claim-audit/batch-07.md)。分母に対する単調性は捨てる。半径が同じだが片側が0点という退化比較も除き、双方4格子点以上の円を主に扱う。

現在の結論: q≥3の剰余類は90度回転の四個組をなし、単一剰余類だけを厳密最大とする原文の読みは不成立。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
