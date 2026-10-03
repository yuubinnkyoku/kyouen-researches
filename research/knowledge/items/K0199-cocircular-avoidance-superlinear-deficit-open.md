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
- path: research/verification/round6-rational-orchard.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B352の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round6_rational_orchard.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/scripts/round6_rational_orchard.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: '起点: [個票04・B071〜B075](verification/batch-04.md)。p中心の反転後にも「4点共円・共線なし」を要求する。一般の三点直線配置の構成が、そのまま使えるとは仮定しない。`δ(S,p)=C(|S|,2)−3b_S(p)`。'
evidence: 原文監査 PARTIAL / partial_general_bound
---

# 共円回避を加えると欠損は超線形

未確定の命題: 共円回避を加えると欠損は超線形。 あるε>0,c>0があり、十分大きい安全Sで `δ(S,p)≥c k^(1+ε)`。普通直線だけの制約より強い損失を予想する。

適用文脈: 起点: [個票04・B071〜B075](verification/batch-04.md)。p中心の反転後にも「4点共円・共線なし」を要求する。一般の三点直線配置の構成が、そのまま使えるとは仮定しない。`δ(S,p)=C(|S|,2)−3b_S(p)`。

現在の結論: δ>k(log log k)^ηは既証だが、原文の固定ε>0でδ≥k^(1+ε)には届かない。

採用境界: δ>k(log log k)^ηは固定冪k^(1+ε)の下界ではない。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
