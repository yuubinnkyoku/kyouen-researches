---
id: K0199
title: 共円回避を加えると欠損は超線形
kind: question
status: open
topics:
- maximal-safe
- geometry
aliases:
- B352
relations:
- type: depends_on
  target: K0026
  note: ''
artifacts:
- path: research/experiments/original-claims/reports/round6-rational-orchard.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/archive/hypothesis-ledgers/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B352の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round6_rational_orchard.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/scripts/round6_rational_orchard.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: '起点: [個票04・B071〜B075](../../log/claim-audit/batch-04.md)。p中心の反転後にも「4点共円・共線なし」を要求する。一般の三点直線配置の構成が、そのまま使えるとは仮定しない。`δ(S,p)=C(|S|,2)−3b_S(p)`。'
evidence: 原文監査 PARTIAL / partial_general_bound
---

# 共円回避を加えると欠損は超線形

未確定の命題: 共円回避を加えると欠損は超線形。 あるε>0,c>0があり、十分大きい安全Sで `δ(S,p)≥c k^(1+ε)`。普通直線だけの制約より強い損失を予想する。

適用文脈: 起点: [個票04・B071〜B075](../../log/claim-audit/batch-04.md)。p中心の反転後にも「4点共円・共線なし」を要求する。一般の三点直線配置の構成が、そのまま使えるとは仮定しない。`δ(S,p)=C(|S|,2)−3b_S(p)`。

現在の結論: δ>k(log log k)^ηは既証だが、原文の固定ε>0でδ≥k^(1+ε)には届かない。

採用境界: δ>k(log log k)^ηは固定冪k^(1+ε)の下界ではない。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。

## 2026-10-17 bounded advance

New finite evidence: exact min-delta tables for combined safe sets on 3x3 (k<=5), 4x4 (k<=7), 5x5 (k<=9): delta/k stays 0..2; no fixed-power superlinear trend at small scales. 4x4 collinear-only comparison: combined safety does not raise min deficit relative to collinear-only (k=7: 6 vs 15).

Scope clarification: board sizes at most 5x5; asymptotic exponents not estimable. Consistent with established linear lower bound.

Next steps: larger boards / rationality constraints investigation. Status remains open.

## 2026-10-17 bounded advance (round 2)

New finite evidence: exact bounded enumeration of combined-safe k-subsets on 6x6 and 7x7 for k up to 2n-1. 6x6: delta_min/k rises from ~0.43 at k=7 to 2.27 at k=11. 7x7: ~0.43 at k=7 to 3.00 at k=13. Values remain O(1) (coefficients <=3) over enumerated range; no evidence of fixed-power superlinear trend delta >= c k^(1+epsilon). Cross-check reproduced prior 3x3/4x4/5x5 values.

Scope clarification: p restricted to board points; k <= 2n-1 only; asymptotic exponents not estimable from n<=7. K0199 remains open.

Next steps: larger boards or off-board points; determine whether linear coefficient grows without bound. Status remains open.

統合監査（2026-10-20）: 上記2026-10-17の追記はローカル研究時点の報告であり、今回すべての探索・測定を再実行したものではない。再検証の範囲は `research/experiments/local-main-integration-20261020/README.md` に記す。既存の未解決性・量化の限界を維持する。
