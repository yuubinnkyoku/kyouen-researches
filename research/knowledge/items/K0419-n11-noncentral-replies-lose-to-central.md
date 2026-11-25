---
id: K0419
title: 初手49・38・16の非中央応手27・93は中央応手に楽観的S5数で約1.5倍劣る
kind: computation
status: computed
topics: [square-outcomes, search-methods, certificates, verification, provenance]
aliases: []
relations:
- type: depends_on
  target: K0417
  note: 中央応手の個別上界（49:2055・38:2155・16:2084）と共同上界31,546
artifacts:
- path: research/experiments/n11-proof-cost-comparison-20261012/scripts/build_alt_roots.py
  role: source
  note: 中央と同一index空間の非中央6 root構築（39.1秒）
- path: research/experiments/n11-proof-cost-comparison-20261012/scripts/compare_alt_replies.py
  role: source
  note: 個別最適化とjoint-swap共同再最適化
- path: research/experiments/n11-proof-cost-comparison-20261012/output/alt-roots-summary.json
  role: data
  note: 6 rootの到達S4・無料third・新規クラス数
- path: research/experiments/n11-proof-cost-comparison-20261012/output/alt-reply-comparison.json
  role: data
  note: 個別UB/LB・再利用率・重なり率・joint-swap差分
- path: research/experiments/n11-proof-cost-comparison-20261012/README.md
  role: source
  note: 証明戦略比較の全体記録（課題1〜5）
scope: 初手49・38・16の非中央応手27・93の二石root各119 third手。既存cache＋独立Boardのみでsolver探索なし。
evidence: 個別上界は3,152〜3,234で中央（2,055〜2,155）をすべて上回り、無料thirdも中央10に対し各2。S4再利用率は約1%、代替計画とK0417共同要求集合の重なりは0〜1個で共有効果なし。joint-swapは31,546に対し＋3,065〜＋3,349悪化し、相異なる群も948→1,007に増える。
---

有望3初手の非中央応手は、個別・共同・共有のいずれの指標でも中央応手に劣る。非中央への拡大は行わず、中央応手が支配的である。
