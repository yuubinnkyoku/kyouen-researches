---
id: K0750
title: 5×19 の4行欠損クラス {0,1,2,4}（行0-2・行4 ≤5石・行3ちょうど6石）の極大安全配置は全8,378ケースで存在しない
kind: computation
status: computed
topics: [rectangles, variants, maximal-safe]
aliases: []
relations:
- type: depends_on
  target: K0740
  note: multi_deficient_runner（two_deficient_pair_runner_flat の DEF_ROWS 汎用版）による完全列挙（制御2種とも PASS）
- type: depends_on
  target: K0726
  note: blocker候補曲線census（7点円8本・8点円87本・行直線5本）
- type: depends_on
  target: K0749
  note: 同一機械・同一k-block分割による4行欠損クラス{0,1,2,3}完全否定の直接の後継
- type: supports
  target: K0332
  note: M_{5,7}=19 予想のうち4行欠損クラス{0,1,2,4}側の否定部
artifacts:
- path: research/experiments/five-row-q7-m19-20261110/scripts/multi_deficient_runner.ts
  role: source
  note: DEF_ROWS=[0,1,2,4] で実行（等価性制御1・陽性対照制御2はK0747と同一）
- path: research/log/2026-11-11-five-row-m19-5row-deficient-complete.md
  role: log
  note: 追記8・追記9: 4行欠損{0,1,2,4}全22スライス記録・完全完了宣言
---

# 5×19・4行欠損 {0,1,2,4} の完全完了: 全 8,378 S0 ケースで witness 0

5×19・q=7 の occupancy クラスのうち、行0-2と行4が ≤5 石・行3がちょうど6石の
4行欠損クラス（鏡映代表 {0,1,2,4}）について、行0の石列 S0 の全鏡映代表ケース
（計 8,378）を multi_deficient_runner で完全列挙した結果、
**どの S0 でも4行欠損 {0,1,2,4} の極大安全配置は存在しない**。

検証構造:
- 機械の制御（等価性 DEF_ROWS=[0,1] pair一致・陽性対照 5×18 witness再現）は
  K0747/K0749 と同一（PASS）。本クラスは同一機械の DEF_ROWS 差し替えのみで実行。
- k-block 境界は単一行・pair・5行欠損・4行欠損{0,1,2,3}クラスと完全一致:
  k=5 0..5831（5,832） / k=4 5832..7787（1,956） / k=3 7788..8276（489） /
  k=2 8277..8366（90） / k=1 8367..8376（10） / k=0 8377（1）。計 8,378。
- 全22スライス（idx 0..8377・gapless）で witness 0・leaves 0・
  census円数 95・代表総数 8,378 一致。
- ノードコスト: k=5帯 ~0.04-12k/case（最大 12,353 @ 601帯）、
  k=4帯 ~0.05-5.5k、k≤3帯 ~0.04-2.1k。{0,1,2,3} より一貫して軽い
  （非欠損行3が中央行でfillとblockerの干渉が強いと推定）。

帰結: 4行欠損3代表のうち2つ（{0,1,2,3}・{0,1,2,4}）が不存在で確定。
**残る未確定は4行欠損1代表（{0,1,3,4}）と3行欠損6鏡映代表のみ。**

限界:
- 4行欠損残り1代表・3行欠損6代表は未完了。それらの完了（または witness 発見）前に
  5×19 の occupancy 全解決・M_{5,7}=19 の確定はない。
- 機械の検証深度は K0740 記載の限界による（5×8 小盤全候補照合は未実施）。
- 本項目は有限計算結果であり全称命題ではない。
