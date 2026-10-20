---
id: K0148
title: 最小極大の指数は2/3
kind: question
status: open
topics:
- maximal-safe
- geometry
aliases:
- B096
relations:
- type: depends_on
  target: K0026
  note: ''
- type: depends_on
  target: K0106
  note: 固定qの指数下界は対応する上界を与えない
artifacts:
- path: research/experiments/original-claims/reports/round52-general-saturation-exponent-lower-bound.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/archive/hypothesis-ledgers/hypothesis-bank-2026-09-27.md
  role: source
  note: B096の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/saturation/reports/saturation-20261003.md
  role: proof
  note: 直線被覆係数の改善と全固定qへの指数下界の拡張
- path: research/experiments/geometry/reports/geometry-20261003.md
  role: proof
  note: §10の整数平方完成ノルム上界2(n-1)^6
scope: 標準q=4の漸近指数の等号。全固定qへの下界拡張とは別。
evidence: 原文監査 PARTIAL / general_asymptotic_lower_exponent_proof
---

# 最小極大の指数は2/3

標準q=4でs_n=n^(2/3+o(1))かは未確定。下界liminf log(s_n)/log n≥2/3は一般証明済みで、全固定q≥4にも拡張された。等号には対応する上界が必要である。

最新成果は直線被覆の係数と円の整数平方完成ノルム上界を改善する。円も禁止する標準版へline-only版の主定数を移せず、これらから指数2/3の上界も出ない。

## 2026-10-17 bounded advance

New finite evidence: n=11,k=8 exact search incomplete (307,355,289 nodes, 300.85s, found=false). Power-law fit on n=2..10 gives alpha~0.6694 but unstable (n>=6 gives 1.0). Construction upper bounds n=11..15 fit alpha~1.0848. Cumulative exponents fluctuate around 2/3 without convergence.

Scope clarification: small-n data neither support nor refute s_n=n^(2/3+o(1)); s_11 remains 8<=s_11<=10.

Next steps: complete 11x11 k=8/k=9 exclusions or construct O(n^(2/3)) sets for larger n. Status remains open.

## 2026-10-17 bounded advance (round 2)

New finite evidence: longer exact maximal-safe-set search on 11x11 for k=8 and k=9. k=8: 696,706,588 nodes in 300.405 s, found=false, complete=false. k=9: 489,846,461 nodes in 300.043 s, found=false, complete=false. Extends earlier bounded evidence (~41.0M nodes for k=8, ~16.2M for k=9) by roughly 17x and 30x.

Scope clarification: incomplete runs do not establish nonexistence. s_11 remains in range 8 <= s_11 <= 10; monotonicity from n=10 to n=11 remains undecided. No status change justified.

Next steps: further exact enumeration or proof of nonexistence for 8/9-stone maximals on 11x11. Status remains open.

統合監査（2026-10-20）: 上記2026-10-17の追記はローカル研究時点の報告であり、今回すべての探索・測定を再実行したものではない。再検証の範囲は `research/experiments/local-main-integration-20261020/README.md` に記す。既存の未解決性・量化の限界を維持する。
