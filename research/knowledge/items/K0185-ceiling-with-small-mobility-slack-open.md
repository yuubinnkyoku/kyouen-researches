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
- path: research/experiments/original-claims/reports/round30-ceiling-orbit-finite-audit.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/archive/hypothesis-ledgers/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B325の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round30_ceiling_audited.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round30_n7_ceiling.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/scripts/round30_ceiling_orbits.cpp
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

## 2026-10-17 bounded advance

New finite evidence: independent enumeration for n=2,3,4 validates procedure (n=4 matches ceil_n4.json: min slack 0,0,1,2,6,9 for h=0..5). n=2: 15 states, K=3; n=3: 298 states, K=5. Larger-case data n=5..7 as previously. Ceiling counts: n=2 10, n=3 168, n=4 4,434.

Scope clarification: fixed finite boards cannot decide K0185 (h->infinity requires unbounded boards).

Next steps: seek unbounded-board arguments or asymptotic constructions. Status remains open.

統合監査（2026-10-20）: 上記2026-10-17の追記はローカル研究時点の報告であり、今回すべての探索・測定を再実行したものではない。再検証の範囲は `research/experiments/local-main-integration-20261020/README.md` に記す。既存の未解決性・量化の限界を維持する。
