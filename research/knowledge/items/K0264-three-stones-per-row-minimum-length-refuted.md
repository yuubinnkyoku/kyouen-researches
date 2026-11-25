---
id: K0264
title: 各行3石を置ける最小長はw≥2で2w+1
kind: proposition
status: refuted
topics:
- rectangles
- variants
aliases:
- B557
relations: []
artifacts:
- path: research/experiments/original-claims/reports/round5-row-thresholds.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/archive/hypothesis-ledgers/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B557の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round5_row_thresholds.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/scripts/round5_row_thresholds.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/scripts/round5_row_triples.cpp
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: この節の盤は `{0,…,m−1}×{0,…,w−1}`。個票09の小さい長方形での一致は動機にとどめ、周期性の証明を引き継がない。
evidence: 原文監査 REFUTED / finite_exhaustion_and_witness
---

# 各行3石を置ける最小長はw≥2で2w+1

否定された命題: 各行3石を置ける最小長はw≥2で2w+1。 `m_*(w)=min{m:K_{w×m}=3w}`について、w=2,3の一致を一つの式にする。

適用文脈: この節の盤は `{0,…,m−1}×{0,…,w−1}`。個票09の小さい長方形での一致は動機にとどめ、周期性の証明を引き継がない。

現在の結論: w5のm11には各行三石の安全配置なし、m12に安全15石がある。従って全w≥2で最小長2w+1という公式は偽。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
