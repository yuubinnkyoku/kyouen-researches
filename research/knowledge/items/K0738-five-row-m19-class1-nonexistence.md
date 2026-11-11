---
id: K0738
title: 5×19 の (5,6,6,6,6) 型・行1/行3欠損の極大安全配置は全8,378ケースで存在しない
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
  note: M_{5,7}=19 予想のうち単一行欠損クラスの行1/行3側の否定部
artifacts:
- path: research/experiments/five-row-q7-m19-20261110/scripts/slice_runner_class1.ts
  role: source
  note: クラス{1}（Y0=1）スライスrunner。行fill修正後の全スライスで使用
- path: research/log/2026-11-11-five-row-m19-class1-slices.md
  role: log
  note: 全スライス記録・k-block境界の厳密確定・完了宣言
---

# 5×19・クラス{1} の完全完了: 全 8,378 S0 ケースで witness 0

5×19・q=7・occupancy パターン (5,6,6,6,6)（行1が ≤5 石・他行ちょうど6石）の
極大安全配置を、行1の石列 S0 の全鏡映代表ケース（計 8,378）について
blocker-obligation-fill DFS（K0727・行fill修正後）で完全列挙した結果、
**どの S0 でも (5,6,6,6,6) 型の極大安全配置は存在しない**。
行鏡映 (y→4−y) により行3欠損クラスも同時に否定される。

検証構造:
- ケースは canonical 順で、k-block 境界は厳密に確定:
  k=5 0..5831（5,832） / k=4 5832..7787（1,956） / k=3 7788..8276（489） /
  k=2 8277..8366（90） / k=1 8367..8376（10） / k=0 8377（1）。計 8,378。
- 全スライス witness 0・leaves 0・census 円数 95・代表総数 8,378 一致。
- 2レーン並列leapfrogで進行し、overlap区間は両レーン独立実行で一致、
  末尾 idx 7995..8377 の383ケースは別実行による独立再検証で一致（二重検証）。

帰結: 5×19 の単一行欠損クラスのうち行1・行3側が完全否定された。
5×18 には witness が存在するため「証人はちょうど M−1 にのみ存在」パターンと整合し、
M_{5,7}=19 予想を補強する。

限界:
- クラス{0}/{4} は K0728、クラス{2} は K0739 で完了。単一行欠損は全位置で否定済み。
- 複数行欠損・他 occupancy パターンは未完了であり、これらの完了前に
  M_{5,7} の値は確定しない。本項目は有限計算結果であり全称命題ではない。
