---
id: K0218
title: 7×7最大配置を8×8の15石へ変えるには元の石を2個以上捨てる必要がある
kind: proposition
status: refuted
topics:
- maximum-safe
- geometry
aliases:
- B386
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
  note: B386の原文・定義（現在の結論は採用報告を優先）
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
evidence: 原文監査 REFUTED / finite_counterexample
---

# 7×7最大配置を8×8の15石へ変えるには元の石を2個以上捨てる必要がある

否定された命題: 7×7最大配置を8×8の15石へ変えるには元の石を2個以上捨てる必要がある。 1個除去・2個追加では届かない。単にそのまま追加不能という既知結果より強い。

適用文脈: 有限安全Sを整数平面へ固定し、盤の外でも4点共円・共線だけで合法性を定める。r(S)はSの最小軸平行外接矩形からのChebyshev距離が最小の、追加可能な外点の距離。

現在の結論: 7×7 A相の最大配置から一石除去・二石追加で8×8安全15石。元石の除去が少なくとも二つ必要という全称を反証。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
