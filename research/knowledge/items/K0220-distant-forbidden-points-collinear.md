---
id: K0220
title: 外点の禁止理由は遠方で直線だけに変わる
kind: proposition
status: proved
topics:
- maximum-safe
- geometry
aliases:
- B388
relations:
- type: depends_on
  target: K0026
  note: ''
artifacts:
- path: research/verification/round9-external-rays.md
  role: proof
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B388の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round9_external_rays.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/scripts/round9_external_rays.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: 有限安全Sを整数平面へ固定し、盤の外でも4点共円・共線だけで合法性を定める。r(S)はSの最小軸平行外接矩形からのChebyshev距離が最小の、追加可能な外点の距離。
evidence: 原文監査 SUPPORTED / general_proof
---

# 外点の禁止理由は遠方で直線だけに変わる

対象命題: 外点の禁止理由は遠方で直線だけに変わる。 全円の外接領域を越えた後に残る禁止直線の方向分布から、r(S)の実用的な上界を円全列挙より短く出せる。

適用文脈: 有限安全Sを整数平面へ固定し、盤の外でも4点共円・共線だけで合法性を定める。r(S)はSの最小軸平行外接矩形からのChebyshev距離が最小の、追加可能な外点の距離。

現在の結論: 三点真円は平方直径による有界領域に収まり、十分遠い格子外点を禁止するのは三点直線だけ。外部飽和半径の一般一様上界を証明したわけではない。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
