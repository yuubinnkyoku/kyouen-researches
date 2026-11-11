---
id: K0728
title: 5×19 の (5,6,6,6,6) 型・行0/行4欠損の極大安全配置は全8,378ケースで存在しない
kind: computation
status: computed
topics: [rectangles, variants, maximal-safe]
aliases: []
relations:
- type: depends_on
  target: K0727
  note: blocker-obligation-fill DFS（sound+complete）による完全列挙
- type: depends_on
  target: K0726
  note: blocker候補曲線census（7点円8本・8点円87本・行直線5本）
- type: supports
  target: K0332
  note: M_{5,7}=19 予想のうち欠損行≤5石・単一行欠損の行0/行4側の否定部
artifacts:
- path: research/experiments/five-row-q7-m19-20261110/scripts/five_row_q7_blocker_dfs.ts
  role: source
  note: blocker-obligation-fill DFSの再現ソース
- path: research/experiments/five-row-q7-m19-20261110/scripts/slice_runner_class0.ts
  role: source
  note: 双方向スライスrunner
- path: research/log/2026-11-11-five-row-m19-class0-complete.md
  role: log
  note: 完走時のスライス記録・2レーン合流の検証
---

# 5×19・クラス{0} の完全完了: 全 8,378 S0 ケースで witness 0

5×19・q=7・occupancy パターン (5,6,6,6,6)（行0が ≤5 石・他行ちょうど6石）の
極大安全配置を、行0の石列 S0 の全鏡映代表ケース（k=0..5、計 8,378）について
blocker-obligation-fill DFS（K0727）で完全列挙した結果、
**どの S0 でも (5,6,6,6,6) 型の不足極大安全配置は存在しない**。
行鏡映 (y→4−y) により行4欠損クラスも同時に否定される。

検証構造:
- ケースは canonical 順（k=5 5,832 → k=4 1,956 → k=3 489 → k=2 90 → k=1 10 → k=0 1）。
  全スライスで witness 0・leaves 0・census 円数 95・代表総数 8,378 が一致。
- 完走は2つの独立レーン（順方向・逆方向）の合流で確認。
  重複区間（idx 1753..3378 を両レーンが独立実行、idx 4300..4383 を意図的再実行）は
  すべて結果一致であり、記録の整合性は二重検証されている。

帰結: 5×19 で (5,6,6,6,6) 型に限れば、欠損行が行0または行4の
単一行欠損クラスは完全否定された。5×18 には 29石の witness が存在するため、
「証人はちょうど M−1 にのみ存在」パターン（M_{4,7}=13、M_{5,6}(予想)=16 と同型）と
整合し、M_{5,7}=19 予想（19 ≤ M_{5,7} ≤ 158, K0332）を強く補強する。

限界:
- クラス{1}（行1欠損・行3と鏡映同値）は進行中（2026-11-11 時点で
  k=5 ブロックの idx 0..433 完了・全 witness 0、gap 395..416 を除く）。
- クラス{2}（行2欠損）と複数行欠損・他 occupancy パターンは未完了であり、
  これらの完了前に M_{5,7} の値は確定しない。
- 本項目は 5×19 の有限計算結果であり、M_{5,7} の全称命題ではない。
