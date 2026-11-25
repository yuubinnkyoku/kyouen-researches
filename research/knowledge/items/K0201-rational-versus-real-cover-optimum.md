---
id: K0201
title: 有理点での最適重複被覆は実数点での最適値より小さい
kind: proposition
status: proved
topics:
- maximal-safe
- geometry
aliases:
- B354
relations:
- type: depends_on
  target: K0026
  note: ''
artifacts:
- path: research/experiments/original-claims/reports/round6-rational-orchard.md
  role: proof
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/archive/hypothesis-ledgers/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B354の原文・定義（現在の結論は採用報告を優先）
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
evidence: 原文監査 SUPPORTED / general_proof_using_published_theorems
---

# 有理点での最適重複被覆は実数点での最適値より小さい

対象命題: 有理点での最適重複被覆は実数点での最適値より小さい。 同じkで、安全性を保つ実数配置の最大bを有理座標では実現できないkが無限にある。

適用文脈: 起点: [個票04・B071〜B075](../../log/claim-audit/batch-04.md)。p中心の反転後にも「4点共円・共線なし」を要求する。一般の三点直線配置の構成が、そのまま使えるとは仮定しない。`δ(S,p)=C(|S|,2)−3b_S(p)`。

現在の結論: 反転・安全化補題、Green–TaoとMazurの適用条件を確認した一般証明。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
