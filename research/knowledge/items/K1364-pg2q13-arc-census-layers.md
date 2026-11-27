---
id: K1364
title: "PG(2,13) のアーク国勢調査 m=4..7 の厳密値と s=2 錐の事前評価（完全錐は純Pythonでは非現実的）"
kind: computation
status: computed
topics: [grundy, geometry, variants]
aliases:
- PG(2,13) arc census layers m=4..7 exact counts
- PG(2,13) s=2 cone pre-assessment
relations:
- type: depends_on
  target: K1353
  note: 錐+二重計数法（三角形推移性と triple double counting）
- type: related
  target: K1359
  note: 同一手法の PG(2,9) s=2 完全スペクトル
- type: related
  target: K1363
  note: 同一手法の PG(2,8)/PG(2,11) s=2 完全スペクトルと次の一手（PG(2,13) 事前評価）への接続
artifacts:
- path: research/experiments/pg2q13-cone-preassessment-20261127/scripts/q13_cone_layers.py
  role: verifier
  note: 層別完全列挙 + 4ゲート fail-closed（rc=0 PASS）
- path: research/experiments/pg2q13-cone-preassessment-20261127/output/out_q13.json
  role: data
  note: T_m・N_m・両三角形一致・ゲート全 PASS
scope: PG(2,13)（183点）の s=2 ゲームに向けた錐の規模評価と、錐の m=4..7 層の完全列挙による PG(2,13) の m-アーク総数の厳密値。
evidence: 錐法（PGL(3,13) の三角形推移性）。各層は完全列挙（有限・全数）。T_m は2つの異なる三角形で完全一致（推移性の運用検証）。T_4=144 は三角形の3辺上を除く点数 183-3-36 と厳密一致。N_3*T_m/C(m,3) の整除ゲート全 PASS。盤公理は出版済みビルダの内部 assert で検証済み。
---

# PG(2,13) アーク国勢調査 m=4..7 と s=2 錐の事前評価

## 厳密値（層 m=4..7 の完全列挙による）

N_3 = 938,119。錐の各層 T_m（固定三角形 F を含む m-アーク数）と
二重計数 N_m = N_3·T_m/C(m,3):

| m | T_m | N_m |
|---:|---:|---:|
| 4 | 144 | 33,772,284 |
| 5 | 7,920 | 742,990,248 |
| 6 | 192,720 | 9,039,714,684 |
| 7 | 1,942,560 | 52,067,212,704 |

層成長は x55 → x24 → x10.1 と減速し、ピーク層は m=8..10 の >=10^7 規模と推定。

## 事前評価の結論

完全錐（全サイズ、最大 14）は 10^7〜10^8 局面規模と推定され、
**純 Python の単一コマンド実行（300s 上限）では非現実的**。
PG(2,13) s=2 の完全 Grundy スペクトルには C/bitset 移植が必要。
（q=11 の錐は 708,761 局面であったのに対し、q=13 は約2桁大きい。）

## 検証ゲート（fail-closed、全 PASS rc=0）

- G1: 盤公理（183点・183直線×14点・pair→line 一意）。
- G2: T_4 = 183-3-36 = 144（3辺上の点を除く数と厳密一致）。
- G3: 全 (m) で整除性 N_3·T_m % C(m,3) == 0。
- G4: 異なる2三角形で T_m 表が完全一致。

## 区別された主張

- m=4..7 の T_m・N_m は**有限完全列挙**による厳密値。
- m>=8 の層規模・完全錐総数は**推定**（未計測）。
- Grundy 分布は本項目では未計算（次の長期レーン課題）。
