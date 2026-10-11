---
id: K0399
title: 90度回転対称点集合の任意q点共円・共線数の法4公式
kind: proposition
status: proved
topics:
- geometry
- statistics
aliases: []
relations: []
artifacts:
- path: research/experiments/geometry/reports/quarter-turn-q-general-congruences-20261011.md
  role: proof
  note: 全称証明と有限検算の範囲
- path: research/experiments/geometry/scripts/quarter_turn_q_verify.py
  role: verifier
  note: 554条件の独立整数行列式照合
- path: research/experiments/geometry/output/quarter_turn_q_20261011.json
  role: data
  note: 5×5盤q=4..8の完全列挙結果
---

## 命題・範囲

任意の有限90度回転対称な平面点集合P、任意のq≥4について、q点共円組・q点共線組の個数は半回転不変組の個数に法4で一致する。中心からの半径sの対蹠点対数をa_s、中心を通る直線Lの対蹠点対数をb_L、中心の占有をδとすると、偶数q=2kでは共円組数≡Σ_s C(a_s,k)、共線組数≡Σ_L C(b_L,k) (mod4)。奇数q=2k+1では共円組数≡0、共線組数≡δΣ_L C(b_L,k) (mod4)。共線組数は常に偶数で、共円組数は4∤qなら偶数。q=4kでは、各半径の90度軌道数c_s=a_s/2を用い共円組数≡Σ_s C(c_s,k) (mod2)。

## 現在の根拠と限界

群作用の軌道長1,2,4の分類と、半回転固定の共円・共線組が対蹠点対からなることを使う数学的全称証明。整数行列式による554条件の独立有限検算は補助的根拠。既存q=4の四点版をq≥4へ一般化。勝敗やGrundy数を主張しない。
