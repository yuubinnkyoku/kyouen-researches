---
id: K0217
title: 盤内では最小極大なのに盤外の広い帯まで塞ぐ
kind: question
status: open
topics:
- maximum-safe
- geometry
aliases:
- B385
relations:
- type: depends_on
  target: K0026
  note: ''
artifacts:
- path: research/verification/round16-dilation-exterior.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B385の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round16_first_appearance.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/scripts/round16_first_appearance.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: 有限安全Sを整数平面へ固定し、盤の外でも4点共円・共線だけで合法性を定める。r(S)はSの最小軸平行外接矩形からのChebyshev距離が最小の、追加可能な外点の距離。
evidence: 原文監査 PARTIAL / finite_evidence_and_partial_general_result
---

# 盤内では最小極大なのに盤外の広い帯まで塞ぐ

未確定の命題: 盤内では最小極大なのに盤外の広い帯まで塞ぐ。 s_nを達成するSのr(S)を任意に大きくできる。少数の直線束が外側でも効き続ける候補。

適用文脈: 有限安全Sを整数平面へ固定し、盤の外でも4点共円・共線だけで合法性を定める。r(S)はSの最小軸平行外接矩形からのChebyshev距離が最小の、追加可能な外点の距離。

現在の結論: 拡大後r=1は最大性・最小極大性・一石移動を保存せず、原文は未決着。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
