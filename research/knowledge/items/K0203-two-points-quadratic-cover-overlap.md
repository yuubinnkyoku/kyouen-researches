---
id: K0203
title: 二つの空点で同時に二次的な重複被覆を持つ
kind: proposition
status: proved
topics:
- maximal-safe
- geometry
aliases:
- B356
relations:
- type: depends_on
  target: K0026
  note: ''
artifacts:
- path: research/experiments/original-claims/reports/round5-quadratic-cover.md
  role: proof
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/archive/hypothesis-ledgers/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B356の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round5_quadratic_cover.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/scripts/round5_quadratic_cover.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: '起点: [個票04・B071〜B075](../../log/claim-audit/batch-04.md)。p中心の反転後にも「4点共円・共線なし」を要求する。一般の三点直線配置の構成が、そのまま使えるとは仮定しない。`δ(S,p)=C(|S|,2)−3b_S(p)`。'
evidence: 原文監査 SUPPORTED / infinite_witness_family
---

# 二つの空点で同時に二次的な重複被覆を持つ

対象命題: 二つの空点で同時に二次的な重複被覆を持つ。 異なるp,qに対し `b_S(p),b_S(q)≥c k²`を、固定c>0で無限族として実現できる。

適用文脈: 起点: [個票04・B071〜B075](../../log/claim-audit/batch-04.md)。p中心の反転後にも「4点共円・共線なし」を要求する。一般の三点直線配置の構成が、そのまま使えるとは仮定しない。`δ(S,p)=C(|S|,2)−3b_S(p)`。

現在の結論: 安全二コピーの合併補題で二空点の固定二次下界。round24は別証明。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
