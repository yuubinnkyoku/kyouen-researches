---
id: K0417
title: 19残存初手の共同S5証明計画は上界31,546・下界6,573で個別合計の約半分
kind: computation
status: computed
topics: [square-outcomes, search-methods, certificates, verification, provenance]
aliases: []
relations:
- type: depends_on
  target: K0415
  note: 19未確定初手軌道と中央応手f=60の候補root
- type: depends_on
  target: K0414
  note: 既知LOSS基準rootと32個の無料S4 LOSS class
- type: depends_on
  target: K0371
  note: 元先手固定の勝敗伝播規則（S1=AND・S4 LOSS=全S5子LOSS）
- type: depends_on
  target: K0372
  note: 独立Board・exact cache隔離・trusted leafの区別
artifacts:
- path: research/experiments/n11-joint-s5-proof-planning-20261012/README.md
  role: source
  note: 共同最適化の結果・方法・再現・限界
- path: research/experiments/n11-joint-s5-proof-planning-20261012/scripts/build_dependency_graph.py
  role: source
  note: 20 rootのS3/S4/S5依存グラフ構築（独立Board＋cache照合のみ）
- path: research/experiments/n11-joint-s5-proof-planning-20261012/scripts/optimize_s5_selection.py
  role: source
  note: 群別1選択肢・和集合最小の上界 heuristic と5種の下界
- path: research/experiments/n11-joint-s5-proof-planning-20261012/scripts/verify_plans.py
  role: verifier
  note: 全2,261 third手・全34,948到達S4の独立再計算（失敗0）
- path: research/experiments/n11-joint-s5-proof-planning-20261012/output/optimization-results.json
  role: data
  note: 個別19 rootと共同の上下界・共有削減・寄与統計
- path: research/experiments/n11-joint-s5-proof-planning-20261012/output/chosen-plans.json
  role: data
  note: 個別・共同の選択S4と要求S5集合（楽観的計画）
- path: research/experiments/n11-joint-s5-proof-planning-20261012/output/plan-verification.json
  role: certificate
  note: 独立再検証の通過記録（58.6秒、失敗0件）
scope: K0415の19未確定初手軌道の中央応手root各119 third手を、既存exact-S5 cache由来の既知LOSS S4または未知S5子集合付きS4で覆う有限選択問題。solver探索なし。
evidence: 2261 third手は選択肢集合が948種に重複し、有料群は869個。multi-start greedy＋再選択＋縮小の実行可能計画は共同31,546個の未知S5（個別最適化の合計63,118の50.02%削減）。element-only分数双対の下界6,573（grouped双対1,586.75、LP緩和双対728を上回る）。`LB <= UB` 表明と独立検証器の全件再計算が通過。最安の単独軌道は初手49で上界2,055。
---

19残存初手の中央応手rootをLOSS証明するのに必要な未確定exact-S5数は、root別に最適化した合計63,118に対し、19 root共同では実行可能計画31,546・有効下界6,573まで下がる。削減の主因はthird手群のroot間重複（2261手→948種）であり、重複群の統合は最適値を変えない。79群は既知LOSS S4で無料である。

この数は楽観的証明計画の規模であり、列挙した未知S5が将来すべてLOSSになる仮定に依存する。下界との差は閉じておらず、非中央応手の比較とWIN側証明の費用は未評価である。
