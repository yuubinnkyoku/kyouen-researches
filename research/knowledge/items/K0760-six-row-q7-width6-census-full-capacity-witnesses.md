---
id: K0760
title: "6×m（q=7）危険曲線censusと満容量36石witness — 幅6 occupancyプログラムのseed"
kind: computation
status: computed
topics: [rectangles, variants, maximal-safe, verification]
aliases: []
scope: "6×m整数格子・q=7（共円・共線7石禁止）・m∈{13,16,19,22,25,28,31,34,40,46,52,58,64,70}のcensus、m∈{19,25,31,40,46,52,58}の満容量witness"
evidence: "chord/center完全census（2重制御検証）と、満容量36石witnessの独立2経路検証（すべて厳密整数演算）"
relations:
- type: depends_on
  target: K0726
  note: 5×19危険曲線census（95本）を同じ機械で完全再現する制御として使用
- type: depends_on
  target: K0745
  note: 満容量witness構成・2経路検証の方法を幅6に拡張
- type: supports
  target: K0332
  note: 安定化長 M_{6,7}（幅6版）が空振りでないことの計算的支持
artifacts:
- path: research/experiments/six-row-q7-width6-20261112/scripts/six_row_q7_census_witness.ts
  role: source
  note: census・制御・witness探索・独立検証の完全再現スクリプト（バッチ実行の手順は冒頭に記載）
- path: research/experiments/six-row-q7-width6-20261112/output/six_row_q7_census_witness.json
  role: data
  note: census表・span分布・witness 7件・検証結果
- path: research/log/2026-11-12-six-row-q7-width6-seed.md
  role: log
  note: 手法・バグ教訓4件・レジューム候補
---

## 命題（計算された事実）

6×m整数格子・q=7（7石の共円・共線禁止）において:

1. **危険曲線census（完全列挙）**: m ∈ {13,16,19,22,25,28,31,34,40,46,52,58,64,70}
   の各々で、7点以上の格子点を含む円は 116/176/244/316/388/468/548/626/782/
   938/1126/1314/1530/1758 本。すべて7点円または8点円であり、**9点以上の円は
   m≤70 では1本も存在しない**。7点以上の直線は行直線6本のみ
   （非水平直線は6行と高々6点で交わる）。
   5×19 では全8点円がちょうど4行を跨ったのに対し、幅6のcensus円は
   4・5・6行を跨る（6×19: span4=48・span5=126・span6=70）。
2. **満容量witnessの実在（独立検証済み）**: m ∈ {19,25,31,40,46,52,58} の
   各々で、行占有 (6,6,6,6,6,6)・36石の安全極大配置が存在する
   （witnessはartifact参照・列鏡映canonical形）。
   極大性は証明（各行ちょうど6石・m≥7 のため追加石は7点共線）。
   安全性は2つの独立経路（危険円census上の石数、石3つ組外心列挙による
   円石数最大値）で検証し、すべて厳密整数演算である。

## 根拠

- census機械はchord法（円は各行と≤2点交わるため、≥7点円は同列和の
  2点ペアを≥2行持ち、中心x=s/2から中心yを厳密整数で解く）で完全。
- 制御1: 5×19 で K0726 の95本（7点:8・8点:87）を完全再現、K0745 W1 の
  worst円石数5を再現。制御2: 6×13 で独立手法（3点外心brute-force）と
  circle set が完全一致。
- witness探索は mulberry32 seed 20261112+7m・200サンプル。
  安全率は m=19: 147/200 から m≥46: ほぼ 200/200 へ上昇
  （36石固定でm増につれ違反が稀になる観測）。

## 限界・スコープ

- すべて有限計算事実であり、M_{6,7}（6×m の全極大安全配置が満容量36石と
  なる最小m・K0332の幅6版）の決定ではない。M_{6,7} の確定には
  欠損行クラスの不在を完全列挙するキャンペーン（5×19 の
  K0738〜K0759 に対応）が必要で未着手。
- m>70 のcensus、9点円の出現有無、総数の漸近則（m≤70 では概ね線形 ~26/m）、
  K0072 mod9補題の幅6版は未解析。
- 実装教訓（census符号・32bitビットマスク打ち切り・行毎鏡映の混合・
  key正規化欠落の4件）は log に記録済み。
