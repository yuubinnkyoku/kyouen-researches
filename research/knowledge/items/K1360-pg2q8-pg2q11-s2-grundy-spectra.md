---
id: K1360
title: "PG(2,8)・PG(2,11) s=2 の完全 Grundy スペクトル — PG(2,11) は 59.9 億局面で最大 Grundy 3 が初出現"
kind: computation
status: computed
topics: [grundy, geometry, variants]
aliases:
- PG(2,8) s=2 complete Grundy spectrum
- PG(2,11) s=2 complete Grundy spectrum
relations:
- type: depends_on
  target: K1359
  note: 錐+二重計数法の PG(2,8)/PG(2,11) への適用
- type: related
  target: K1300
  note: s パラメータ表の PG(2,8) 行（定理経由値の計算的直接確認）
- type: related
  target: K1298
  note: 偶一様なら G=|S| mod 2（PG(2,8) で全サイズ確認）、混在なら G>=2（PG(2,11) は G=3 まで）
artifacts:
- path: research/experiments/pg2q-s2-cone-spectrum-family-20261127/scripts/pg2q9_cone_spectrum.py
  role: verifier
  note: q=3,4,8,9,11 対応本体（q<=4 素朴全 DP 較正込み）
- path: research/experiments/pg2q-s2-cone-spectrum-family-20261127/scripts/verify_pg2_general.py
  role: verifier
  note: q=8/9/11 共通検証バッテリー（gate 6 + tamper 5・rc=0 PASS）
- path: research/experiments/pg2q-s2-cone-spectrum-family-20261127/output/out_q8.json
  role: data
  note: PG(2,8) s=2 スペクトル
- path: research/experiments/pg2q-s2-cone-spectrum-family-20261127/output/out_q11.json
  role: data
  note: PG(2,11) s=2 スペクトル（初測定）
- path: research/experiments/pg2q-s2-cone-spectrum-family-20261127/output/audit_q8.json
  role: data
  note: q=8 ゲート/tamper レポート
- path: research/experiments/pg2q-s2-cone-spectrum-family-20261127/output/audit_q11.json
  role: data
  note: q=11 ゲート/tamper レポート
scope: PG(2,8)（73点）と PG(2,11)（133点）の s=2 共演ゲーム（各直線上高々2点・1手1点追加・追加不能が終局・通常プレイ）の全安全局面の Grundy 分布。
evidence: 錐+二重計数法（K1359 と同一・PGL(3,q) の非共線3点推移性）。PG(2,8) 錐 8,450 局面・PG(2,11) 錐 708,761 局面。PG(2,8) は出版国勢調査（総数 19,550,350・極大 2,060,352/32,704）と K1298 パリティ則 G=|S| mod 2 を bit-exact 再現。PG(2,11) は古典円錐曲線総数 160,930 = |PGL(3,11)|/|PGL(2,11)| との一致、完全 7/9/10/12-アークの軌道安定化群恒等式（21/1/60/1320）、3 つの異なる F での錐 T 表完全一致、環境リセット跨ぎの bit-exact 再現、子/mex 別実装監査、tamper 5/5 fail-closed。
---

# PG(2,8)・PG(2,11) s=2 の完全 Grundy スペクトル

## PG(2,8) s=2

総 19,550,350 局面（出版国勢調査一致）。極大 {6,10}（2,060,352/32,704）。
全サイズで **G = m mod 2**（K1298 の定理経由値の独立計算による直接確認）。
最大 G=1・Grundy(∅)=0。サイズ別分布 m=4..9 = 686,784 / 4,120,704 / 8,928,192 /
3,924,480 / 1,471,680 / 327,040 は新規。

## PG(2,11) s=2（初測定）

総 **5,989,752,243** 局面を錐 708,761 局面で完全決定。

| size | G=0 | G=1 | G=2 | G=3 |
|---:|---:|---:|---:|---:|
| 0 | 1 | | | |
| 1 | | 133 | | |
| 2 | 8,778 | | | |
| 3 | | 354,046 | | |
| 4 | 8,851,150 | | | |
| 5 | | 21,242,760 | 106,213,800 | |
| 6 | 293,858,180 | 123,916,100 | | 495,664,400 |
| 7 | 434,970,800 | 460,259,800 | 1,692,339,880 | |
| 8 | 884,229,885 | 1,168,351,800 | | |
| 9 | 212,427,600 | 70,809,200 | | |
| 10 | 14,161,840 | | | |
| 11 | | 1,931,160 | | |
| 12 | 160,930 | | | |

- **最大 Grundy 3**（サイズ 6 のみ）= PG 系列初の 3。**Grundy(∅)=0**。
- 極大 {7,8,9,10,12}・完全アーク 10,115,600 / 645,248,835 / 212,427,600 /
  3,540,460 / 160,930。**完全 12-アーク 160,930 は PG(2,11) の円錐曲線総数
  |PGL(3,11)|/|PGL(2,11)| と厳密一致**（奇 q の円錐曲線は完全アーク）。
- q=3,4,8,9,11 で Grundy(∅)=0 は不動。最大Gは q=8:1 → q=9:2 → q=11:3 と
  q の増大で非減少。
