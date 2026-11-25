---
id: K0134
title: B072に等号を達成する非自明な配置
kind: proposition
status: refuted
topics:
- maximal-safe
- geometry
aliases:
- B073
relations:
- type: depends_on
  target: K0026
  note: ''
artifacts:
- path: research/experiments/original-claims/reports/round45-cover-gap-and-sharp-overlap.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/archive/hypothesis-ledgers/hypothesis-bank-2026-09-27.md
  role: source
  note: B073の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round45_cover_verified.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: 本文の原文量化と現在の採用境界
evidence: 原文監査 REFUTED / general_impossibility_using_melchior_inequality
---

# B072に等号を達成する非自明な配置

否定された命題: B072に等号を達成する非自明な配置。 `|S|≥7` で、空点pを囲む三つ組族がSteiner三つ組系になる安全Sが、ある格子盤上に存在する。数え上げ上限が幾何で実現可能かを問う。

現在の結論: k≥4で反転後の通常直線数δ≥3。旧floor(k(k−1)/6)の等号はδ=0または1を要求し不可能。k≥7のSteiner等号候補も否定される。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
