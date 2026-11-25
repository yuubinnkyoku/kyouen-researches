---
id: K0741
title: 5×19 の (5,6,6,6,6) 型・2行欠損 pair {0,1}/{3,4} の極大安全配置は全8,378ケースで存在しない
kind: computation
status: computed
topics: [rectangles, variants, maximal-safe]
aliases: []
relations:
- type: depends_on
  target: K0740
  note: two_deficient_pair_runner（ハイブリッド blocker-fill DFS・等価検証済み flat 版）による完全列挙
- type: depends_on
  target: K0726
  note: blocker候補曲線census（7点円8本・8点円87本・行直線5本）
- type: supports
  target: K0332
  note: M_{5,7}=19 予想のうち2行欠損クラス pair {0,1}/{3,4} 側の否定部
artifacts:
- path: research/experiments/five-row-q7-m19-20261110/scripts/two_deficient_pair_runner_flat.ts
  role: source
  note: 等価検証済み flat 版 runner（Y0=0, Y1=1）
- path: research/log/2026-11-11-five-row-multi-deficient-machine.md
  role: log
  note: 全スライス記録・pair {0,1} 完了宣言（続き1–7）
---

# 5×19・pair {0,1} の完全完了: 全 8,378 S0 ケースで witness 0

5×19・q=7・occupancy パターン (5,6,6,6,6) のうち行0・行1がともに ≤5 石
（他行ちょうど6石）の2行欠損クラスについて、行0の石列 S0 の全鏡映代表ケース
（計 8,378）を two_deficient_pair_runner（K0740・ハイブリッド blocker-fill DFS）で
完全列挙した結果、**どの S0 でも (5,6,6,6,6) 型の2行欠損極大安全配置は存在しない**。
行鏡映 (y→4−y) により pair {3,4} も同時に否定される。

検証構造:
- k-block 境界は単一行クラス（K0738）と同一:
  k=5 0..5831（5,832） / k=4 5832..7787（1,956） / k=3 7788..8276（489） /
  k=2 8277..8366（90） / k=1 8367..8376（10） / k=0 8377（1）。計 8,378。
- 全スライス witness 0・leaves 0・census 円数 95・代表総数 8,378 一致。
- 2レーン並列leapfrogで進行、overlap区間は独立実行で一致（二重検証）。
  5×18 での第3 witness 発見（K0740 の陽性対照）が witness 検出の健全性を裏付ける。

帰結: 2行欠損クラス6代表（{0,1}≡{3,4}, {0,2}≡{2,4}, {1,2}≡{2,3},
{0,3}≡{1,4}, {1,3}, {0,4}）のうち最初の1つが完全否定された。
5×18 には witness が存在し5×19 には存在しないことは
「証人はちょうど M−1 にのみ存在」パターンと整合し、M_{5,7}=19 予想を補強する。

限界:
- 残り5ペアクラス代表は未完了。単一行欠損（K0728/K0738/K0739）との差分は
  欠損行 Y1 の「石/空+blocker」分岐のみで、機械の検証深度は K0740 記載の限界による。
- 非行欠損の一般極大配置の不在は未解決であり、これらの完了前に M_{5,7} の値は
  確定しない。本項目は有限計算結果であり全称命題ではない。
