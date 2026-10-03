---
id: K0186
title: g=h≥3の局面に軌道サイズ1か2の勝ち手が常にあるか
kind: question
status: open
topics:
- grundy
aliases:
- B326
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
  note: B326の原文・定義（現在の結論は採用報告を優先）
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
scope: 標準通常版の全n・全安全S。hは最大残り手数、軌道はSのD4安定化群による。
evidence: 原文監査 PARTIAL / finite_complete_census_and_small_board_crosscheck
---

# g=h≥3の局面に軌道サイズ1か2の勝ち手が常にあるか

標準通常版の全正方形盤について、g(S)=h(S)≥3なら、SのD4安定化群による軌道サイズが1または2となる勝ち手が必ずあるかは未証明。hは終局0・非終局1+max(子h)の最大残り手数である。

7×7では条件を満たす58,123,224局面すべての安定化群の位数が1または2なので、勝ち手の軌道もサイズ1または2。4×4にも独立再帰による検算がある。

全盤への一般化は未解決。小軌道であることは軌道内の手が非同値であるという意味ではなく、misèreの補助mex値hとも混同しない。
