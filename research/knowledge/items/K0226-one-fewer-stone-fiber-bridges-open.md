---
id: K0226
title: 一石少ない中間配置を許すと同一残局族を少数の橋で結べる
kind: question
status: open
topics:
- residual-games
- reconfiguration
aliases:
- B448
relations:
- type: depends_on
  target: K0108
  note: ''
- type: depends_on
  target: K0301
  note: 四石配置対の三石Johnson交換橋は一般証明済み
artifacts:
- path: research/experiments/original-claims/reports/round42-exact-residual-family-audit.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/archive/hypothesis-ledgers/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B448の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round42_families_verified.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/scripts/round42_families_audit.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: '起点: [個票03・B057](../../log/claim-audit/batch-03.md)。ここでは同じk・同じラベル付きL・同じ極小残余族Rを持つ集合を一つの族とする。Rが空の場合でもLを省略しない。'
evidence: 原文監査 PARTIAL / general_four_stone_bridge_proof
---

# 一石少ない中間配置を許すと同一残局族を少数の橋で結べる

未確定の命題: 一石少ない中間配置を許すと同一残局族を少数の橋で結べる。 端点ではL,Rを保ち、中間は別残局を許したG_{k−1}上で、各成分間の接続に共通する小さい橋の型がある。

適用文脈: 起点: [個票03・B057](../../log/claim-audit/batch-03.md)。ここでは同じk・同じラベル付きL・同じ極小残余族Rを持つ集合を一つの族とする。Rが空の場合でもLを省略しない。

現在の結論: 安全四石対は、常に安全な三石層のJohnsonグラフを経由して接続でき、この部分はK0301としてprovedに分離した。k≥5を含む原文全体は未証明。

採用境界: 任意の安全四石配置対は常に安全な三石層のJohnsonグラフを通って結べる。k≥5の原文全体は未証明。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。

## 2026-10-17 bounded advance

New finite evidence: 4x4 census k=3..6: all split families under one-stone exchange merge through (k-1)-stone layer (k=4:32/32, k=5:146/146, k=6:44/44) with bridge lengths 2-3, 2-5, 2-6 (k-1)-stone vertices. 3x3 k=4: 17 split families all merged via 3-stone layer (2-4 vertices). Lower layer connected on tested boards.

Scope clarification: bridge length grows with k (max observed = k for k>=5), so uniform O(1) bound not established.

Next steps: test 5x5 and larger boards. Status remains open.

## 2026-10-17 bounded advance (round 3)

New finite evidence: 5x5 exact fiber-bridge census for k=4..9. Safe states by size: 1,25,300,2300,11824,37272,59192,35208,5172,100. Lower layer connected for sizes 3..8. Every same-(k,L,R) family split under one-stone exchange merges through (k-1)-stone layer: k=4 2/2 pairs (bridge 2); k=5 237/237 (2..5, mean 2.996); k=6 102,134/102,134 (2..6, mean 3.947); k=7 73,390/73,390 (2..7, mean 4.471); k=8 2,992/2,992 (2..8, mean 4.655); k=9 946/946 (2..9, mean 5.281). C++ exact census with Python cross-check for k=5.

Scope clarification: merging automatic due to lower-layer connectivity on tested board; nontrivial content is path length, not uniformly bounded (max grows with k). K0226 remains open; general statement for k>=5 unproved.

Next steps: test larger boards; compute Steiner total cost; seek uniform bound. Status remains open.

統合監査（2026-10-20）: 上記2026-10-17の追記はローカル研究時点の報告であり、今回すべての探索・測定を再実行したものではない。再検証の範囲は `research/experiments/local-main-integration-20261020/README.md` に記す。既存の未解決性・量化の限界を維持する。
