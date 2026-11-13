# 2026-11-14 cost-60証明書込みfrontier完全再計算（第20セッション続き3）

- **正式frontier更新**: `scripts/recompute_frontier_cost60.py`
 （recompute_frontier_full.pyの論理 + 検証済みcost-60証明書19rootのcovers）。
  段階制御: after-batch3（690/7156/561764/5373/421771）を同一入力から
  **assertで再現**してからcost-60 coversを追加。
- cost-60効果: covers 111・marginal 110・**manifest内 +34**（見積りと完全一致）。
- **frontier after cost60**: solved_s6_in_manifest **724**・unique_remaining **7122**・
  sum_cost **559294**・open 5339/419301。
  **best class-2 blocker S5 `00000000000000003802000008000000` が 32→17 orbit・
  cost 2206→1168 に半減**（class-2 laneへの単一sweepの効果としては最大級）。
  best class-4 `00000000020000003800000080000000` は24/1934不変。
- 成果物: `output/class2-lane-cost60-frontier-recompute-20261114.json`（4ccc218f）・
  `output/class-frontier-s5-ranking-after-cost60.csv`（ab2338c4）・
  スクリプト（fb10e486）。制御は全て再現（690/7156/561764/5373/421771）。
- 解釈ガード: 本再計算は公表レシート上のbookkeeping。計上された全coverは
  独立検証済み証明書由来。REFUTED-D10は深さ10以内のWIN7の否定のみ。
  **11×11空盤・二石root {49,60}・S2 {59,60}・class 2・class 4 はいずれも UNKNOWN**。
- レジューム: (1) 次のclass-2 lane候補はbest class-2 blocker自身
  `00000000000000003802000008000000`（17 orbit・cost 1168 — ただしS5そのものの
  sweepではなく残17 orbitのS6 child選定が先）またはranking上位から、
  (2) cost-74 class-4 2件。並走レーンの最新mainを取り直してから。
