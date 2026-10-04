---
id: K0242
title: 共線数の大きい傾きの尾部は一様に小さい
kind: proposition
status: proved
topics:
- geometry
aliases:
- B471
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
- path: research/archive/hypothesis-ledgers/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B471の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round4_collinear_asymptotic.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/scripts/round4_collinear_asymptotic.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: '起点: [個票08](../../log/claim-audit/batch-08.md)。有限範囲の次数フィットは動機にとどめる。D_nを共線四点数、C_nを非共線共円四点数とする。'
evidence: 原文監査 SUPPORTED / general_proof
---

# 共線数の大きい傾きの尾部は一様に小さい

対象命題: 共線数の大きい傾きの尾部は一様に小さい。 原始方向vの高さをH(v)=max(|v_x|,|v_y|)とすると、H(v)>hからの寄与は全n,hで `O(n^5/h)` に抑えられる。

適用文脈: 起点: [個票08](../../log/claim-audit/batch-08.md)。有限範囲の次数フィットは動機にとどめる。D_nを共線四点数、C_nを非共線共円四点数とする。

現在の結論: 高さh以上の原始方向に由来する共線四点数の尾部は一様に≤2n^5/h。有限方向近似の誤差を制御できる。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
