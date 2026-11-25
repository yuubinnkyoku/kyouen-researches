---
id: K0739
title: 5×19 の (5,6,6,6,6) 型・行2欠損の極大安全配置は全8,378ケースで存在しない — 単一行欠損クラス完結
kind: computation
status: computed
topics: [rectangles, variants, maximal-safe]
aliases: []
relations:
- type: depends_on
  target: K0727
  note: blocker-obligation-fill DFS（sound+complete・行fill修正済み）による完全列挙
- type: depends_on
  target: K0726
  note: blocker候補曲線census（7点円8本・8点円87本・行直線5本）
- type: supports
  target: K0332
  note: M_{5,7}=19 予想のうち単一行欠損クラスの行2（中央行）側の否定部
artifacts:
- path: research/experiments/five-row-q7-m19-20261110/scripts/slice_runner_class2.ts
  role: source
  note: クラス{2}（Y0=2・中央行）スライスrunner。slice_runner_class1.ts の Y0 を 2 にした同一機械
- path: research/log/2026-11-11-five-row-m19-class2-slices.md
  role: log
  note: 全スライス記録・完了宣言・クラス{2}は行鏡映で自身と同値であることの記録
---

# 5×19・クラス{2} の完全完了: 全 8,378 S0 ケースで witness 0 — 単一行欠損クラス完結

5×19・q=7・occupancy パターン (5,6,6,6,6)（行2が ≤5 石・他行ちょうど6石）の
極大安全配置を、行2（中央行）の石列 S0 の全鏡映代表ケース（計 8,378）について
blocker-obligation-fill DFS（K0727）で完全列挙した結果、
**どの S0 でも (5,6,6,6,6) 型の極大安全配置は存在しない**。
行2は行鏡映で自身と同値のため、クラス{2}はこれで完結する。

検証構造:
- ケースは canonical 順で k-block 構成はクラス{0}/{1} と同一:
  k=5 5,832 / k=4 1,956 / k=3 489 / k=2 90 / k=1 10 / k=0 1、計 8,378。
- 全スライス witness 0・leaves 0・census 円数 95・代表総数 8,378 一致。
- 2レーン並列leapfrogで進行し、overlap区間（4604..5076・5147..5280・5294..5395・
  5414..5555・5574..5714・5739..6122・6225..6734・6918..7493）は両レーン独立実行で一致。
- 完了後、別セッション（長期レーン）が A13 相当（START=4160）から B18r 相当
  （START=6225）までの主要スライス12本を独自に再実行し、done数・nextIdx・
  witness 0・leaves 0 が記録と完全一致することを確認（第三の独立再検証）。

帰結: **5×19 の単一行欠損クラス（{0}≡{4}, {1}≡{3}, {2}）はすべて不存在で完結**。
(5,6,6,6,6) 型に限れば 5×19 に極大安全配置は存在しない。
witness は 5×18 にのみ存在し、M_{5,7}=19 予想を強く補強する。
ノードコストはクラス{0}/{1} の同帯域より一貫して軽い（中央行欠損は両側行fillが
blockerと干渉して早期矛盾するためと推定）。

限界:
- 複数行欠損クラス（≥2行が ≤5 石）・満杯30石以外の一般 occupancy パターンは
  未完了であり、これらの完了前に M_{5,7} の値は確定しない。
- 本項目は 5×19 の有限計算結果であり、M_{5,7} の全称命題ではない。
