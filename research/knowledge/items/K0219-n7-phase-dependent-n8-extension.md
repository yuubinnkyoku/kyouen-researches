---
id: K0219
title: 7×7最大配置の一方の相だけが少ない再配置で8×8最大へ届く
kind: proposition
status: computed
topics:
- maximum-safe
- geometry
aliases:
- B387
relations:
- type: depends_on
  target: K0026
  note: ''
artifacts:
- path: research/verification/round9-n7-n8-overlap.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B387の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round9_n7_n8_overlap.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round9_n7_n8_phase.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/scripts/round9_n7_n8_overlap.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: 有限安全Sを整数平面へ固定し、盤の外でも4点共円・共線だけで合法性を定める。r(S)はSの最小軸平行外接矩形からのChebyshev距離が最小の、追加可能な外点の距離。
evidence: 原文監査 SUPPORTED / finite_exhaustion_and_witness
---

# 7×7最大配置の一方の相だけが少ない再配置で8×8最大へ届く

対象命題: 7×7最大配置の一方の相だけが少ない再配置で8×8最大へ届く。 元集合との共通部分を最大化したとき、A型とB型で最小必要除去数が異なる。

適用文脈: 有限安全Sを整数平面へ固定し、盤の外でも4点共円・共線だけで合法性を定める。r(S)はSの最小軸平行外接矩形からのChebyshev距離が最小の、追加可能な外点の距離。

現在の結論: 全16最大配置・全埋込みでA相最小除去1、B相2。既知K8=15へ達する再配置である。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
