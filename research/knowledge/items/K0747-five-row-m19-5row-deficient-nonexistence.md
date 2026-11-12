---
id: K0747
title: 5×19 の5行欠損クラス（全行 ≤5 石・occupancy 自由）の極大安全配置は全8,378ケースで存在しない
kind: computation
status: computed
topics: [rectangles, variants, maximal-safe]
aliases: []
relations:
- type: depends_on
  target: K0740
  note: two_deficient_pair_runner の DEF_ROWS 汎用版 multi_deficient_runner による完全列挙（等価性・陽性対照とも PASS）
- type: depends_on
  target: K0726
  note: blocker候補曲線census（7点円8本・8点円87本・行直線5本）
- type: depends_on
  target: K0745
  note: 満容量 (6,6,6,6,6) witness 実在との対比で occupancy クラス空間を分割
- type: supports
  target: K0332
  note: M_{5,7}=19 予想のうち5行欠損クラス側の否定部
artifacts:
- path: research/experiments/five-row-q7-m19-20261110/scripts/multi_deficient_runner.ts
  role: source
  note: DEF_ROWS 差し替え汎用機械（5/4/3行欠損クラスすべてに使用可・制御2種で検証済み）
- path: research/log/2026-11-11-five-row-m19-5row-deficient-complete.md
  role: log
  note: 全スライス記録・5行欠損完了宣言・4行欠損開始
---

# 5×19・5行欠損クラスの完全完了: 全 8,378 S0 ケースで witness 0

5×19・q=7 の occupancy クラスのうち、全5行が ≤5 石（occupancy 自由・合計 ≤25 石）
の5行欠損クラスについて、行0の石列 S0 の全鏡映代表ケース（計 8,378）を
multi_deficient_runner（K0740 pair 機械の DEF_ROWS 汎用版・探索順同一）で
完全列挙した結果、**どの S0 でも5行欠損の極大安全配置は存在しない**。
5行欠損は行鏡映で不変の単一クラスであり、鏡映による追加代表はない。

検証構造:
- 制御1（等価性）: DEF_ROWS=[0,1] で pair版スライスA1と決定的完全一致
  （done=117・max 28,488 @ idx 39・witness 0・leaves 0・nC=95）。
- 制御2（陽性対照）: 5×18・DEF_ROWS=[0]・S0={0,1,5,13,17} で既知第3 witness を
  17,829 ノードで完全再現・verify() PASS。石分岐・witness 検出の健全性を実証。
- k-block 境界は単一行・pair クラスと同一:
  k=5 0..5831（5,832） / k=4 5832..7787（1,956） / k=3 7788..8276（489） /
  k=2 8277..8366（90） / k=1 8367..8376（10） / k=0 8377（1）。計 8,378。
- 全スライス witness 0・leaves 0・census 円数 95・代表総数 8,378 一致。
  overlap 区間（3000..3367）は独立実行で一致（二重検証）。
- ノードコストは pair クラスより軽い（~0.5–1.5k/case・最大 ~8.6k）。

帰結: 5×19 の occupancy クラスのうち、満容量 (6,6,6,6,6) は witness 実在（K0745）し、
単一行・2行・5行欠損クラスは不存在が確定した。**残る未確定クラスは
4行欠損3代表（{0,1,2,3}/{0,1,2,4}/{0,1,3,4}）と3行欠損6鏡映代表のみ**である。
4行欠損 {0,1,2,3} は本機で探索開始済み（idx 0..323・全 witness 0）。

限界:
- 4行・3行欠損クラスは未完了。それらの完了（または witness 発見）前に
  5×19 の occupancy 全解決・M_{5,7}=19 の確定はない。
- 機械の検証深度は K0740 記載の限界による（5×8 小盤全候補照合は未実施）。
- 本項目は有限計算結果であり全称命題ではない。
