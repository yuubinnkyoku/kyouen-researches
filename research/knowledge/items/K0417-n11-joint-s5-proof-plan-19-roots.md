---
id: K0417
title: 19残存初手の共同S5計画は夜間層別13の反映で上界31,774・整数下界6,585
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
- path: research/experiments/n11-s5-s6-quotient-20261013/scripts/repair_plan.py
  role: source
  note: 独立終局二局面の追加後、WIN子S4の排除・選択修復・全選択境界の検算
- path: research/experiments/n11-s5-s6-quotient-20261013/output/repaired-joint-plan.json
  role: data
  note: 現行19-root全2261手の選択応手・要求31636・独立検証結果
scope: 旧cacheとK0423の独立終局二局面を反映した、K0415の19未確定初手軌道の中央応手root各119 third手を、既存exact-S5 cache由来の既知LOSS S4または未知S5子集合付きS4で覆う有限選択問題。計画部分はsolver探索なし。二局面追加の終局証明はK0423。
evidence: 現行修復は19 root・2,261 third全手・349選択S4の完全S5境界を独立再計算して通過。旧計画要求209644がWINと証明されたため2 S4を排除し5選択を修復、558600 LOSSは費用から除外。現行要求31,636、厳密双対91145221/13860から整数下界6,577（K0418）。旧cacheでの履歴として2261 third手は選択肢集合が948種に重複し、有料群は869個。multi-start greedy＋再選択＋縮小の実行可能計画は共同31,546個の未知S5（個別最適化の合計63,118の50.02%削減）。element-only分数双対の下界6,573（grouped双対1,586.75、LP緩和双対728を上回る）。`LB <= UB` 表明と独立検証器の全件再計算が通過。最安の単独軌道は初手49で上界2,055。
---

## 現行計画（独立終局パイロット後）

K0423により、旧31,546要求集合の209644は元先手WIN、558600はLOSSと独立証明された。
旧選択のまま全要求をLOSS化することは不可能となり、S4クラス5687・5690を排除した。
初手5のthird59/61/115、初手49のthird55/65の5選択を修復した現行計画は31,636未確定S5。
全19 root・2,261合法third・349相異なる選択S4の完全S5境界を独立整数幾何と明示cacheで再検査し、既知WINを要求していないことを確認した。

現行の整数下界はK0418の6,577。旧31,546／6,574は旧cacheインスタンスの履歴値として保持し、現在の上下界には用いない。
残り31,636が全てLOSSとなることは未証明で、計画は依然楽観的。既存cache葉はsolver-trusted、追加二局面だけはtrusted葉0の終局DAG。

## 夜間バッチ反映（2026-10-14・K0424）

夜間適応探索で9局面の新規厳密判定（LOSS 3・WIN 6）をtrusted葉0の終局DAGで獲得し、
6段階の計画更新を経た現行値は上界31,774・下界6,585・層別13（6W+7L）・除外S4 17件。
K0423時点の31,636／6,577は本項目の履歴値として保持し、現在の上下界には用いない。
詳細はK0424と `research/experiments/n11-night-plan-update6-20261014/` を参照。

## 旧cacheインスタンスの履歴

19残存初手の中央応手rootをLOSS証明するのに必要な未確定exact-S5数は、root別に最適化した合計63,118に対し、19 root共同では実行可能計画31,546・有効下界6,573まで下がる。削減の主因はthird手群のroot間重複（2261手→948種）であり、重複群の統合は最適値を変えない。79群は既知LOSS S4で無料である。

この数は楽観的証明計画の規模であり、列挙した未知S5が将来すべてLOSSになる仮定に依存する。下界との差は閉じておらず、非中央応手の比較とWIN側証明の費用は未評価である。
