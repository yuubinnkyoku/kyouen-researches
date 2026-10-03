---
id: K0185
title: 天井達成局面は合法手数の小さい余裕で作れる
kind: question
status: open
topics:
- grundy
aliases:
- B325
relations:
- type: depends_on
  target: K0002
  note: ''
artifacts:
- path: research/verification/round30-ceiling-orbit-finite-audit.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B325の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round30_ceiling_audited.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round30_n7_ceiling.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/scripts/round30_ceiling_orbits.cpp
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: 標準通常版、hは最大残り手数。h→∞となる族に共通の絶対定数Cの存在を問う。
evidence: 原文監査 PARTIAL / finite_complete_census_and_small_board_crosscheck
---

# 天井達成局面は合法手数の小さい余裕で作れる

標準通常版の正方形盤で、最大残り手数h(S)を無限に大きくしながらg(S)=h(S)、|L(S)|≤h(S)+Cを満たす絶対定数C付きの局面族があるかは未証明。

7×7の全179,810,350安全局面を用いた有限監査では、g=hにおけるh=0..10の最小余裕|L|−hは0,0,1,1,2,2,4,5,9,17,28。4×4では別実装の再帰で一致した。

有限盤で余裕が増えたことは、固定余裕の無限族の不存在証明ではない。ここでhは終局0・非終局1+max(子h)であり、misèreの終局1から始める補助mex値とは異なる。
