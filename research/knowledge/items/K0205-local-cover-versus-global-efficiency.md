---
id: K0205
title: 点ごとの被覆上限は大きくても全面被覆は極端に非効率
kind: proposition
status: proved
topics:
- maximal-safe
- geometry
aliases:
- B360
relations:
- type: depends_on
  target: K0026
  note: ''
artifacts:
- path: research/verification/round5-cover-union.md
  role: proof
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B360の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round5_cover_union.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/scripts/round5_cover_union.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: '起点: [個票04・B071〜B075](verification/batch-04.md)。p中心の反転後にも「4点共円・共線なし」を要求する。一般の三点直線配置の構成が、そのまま使えるとは仮定しない。`δ(S,p)=C(|S|,2)−3b_S(p)`。'
evidence: 原文監査 SUPPORTED / infinite_witness_family
---

# 点ごとの被覆上限は大きくても全面被覆は極端に非効率

対象命題: 点ごとの被覆上限は大きくても全面被覆は極端に非効率。 bの最大値が同程度の二つの安全集合で、禁止点の和集合のサイズの比を任意に大きくできる。

適用文脈: 起点: [個票04・B071〜B075](verification/batch-04.md)。p中心の反転後にも「4点共円・共線なし」を要求する。一般の三点直線配置の構成が、そのまま使えるとは仮定しない。`δ(S,p)=C(|S|,2)−3b_S(p)`。

現在の結論: 同盤・同石数・双方bmax=Θ(k²)で禁止点和集合比が無界。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
