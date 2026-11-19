---
id: K1020
title: 2トークン残余ゲーム z=15・y=1境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z15 y1 boundary slice]
relations:
- type: depends_on
  target: K0832
  note: 単一トークンz=16閉形式、一般tail、height-only縮約を使用する
- type: depends_on
  target: K1018
  note: C子の評価にz=14・y=1境界切片を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z15-y1-boundary-20261119/report.md
  role: proof
  note: x外帰納と全R署名帯表による全称証明
- path: research/experiments/vertical-fiber-two-token-z15-y1-boundary-20261119/verify_z15_y1.py
  role: verifier
  note: 順序保持・降順正準化の二直接再帰、子アンカー、署名帯・mex・tail・height-only縮約の独立監査
- path: research/experiments/vertical-fiber-two-token-z15-y1-boundary-20261119/output/audit.json
  role: data
  note: 27,661,600照合・不一致0・独立プロセス3回実行でbyte-identical
- path: research/experiments/vertical-fiber-two-token-z15-y1-boundary-20261119/census_z15_y1.py
  role: data
  note: 有限センサスと候補導出（output/census.txt・2回実行byte-identical）
- path: research/log/2026-11-19-vertical-fiber-two-token-z15-y1-boundary.md
  role: log
  note: z=15,y=1切片の選定・導出・監査・構造則・接続
scope: >-
  κ=1残余ゲームH(R;(x,y);z)の2トークン族における固定高さz=15、y=1、
  全x>=1・全R>=0。Grundy値0/1/2を完全分類する。
evidence: >-
  xに関する外帰納。A子は同じz=15,y=1のx-1行、B子はK0832の単一トークンz=16公式、
  C子は1 xor K1018(z=14,y=1)で評価する。x=1では2つの除去手が同じ単一トークン子へ
  合流する。x<=17の個別署名帯とx>=18の偶奇別定常署名帯が全R>=1を互いに素に被覆し、
  各帯のmexが本文のT/P閉形式を与える。値2位置はx>=18でラダーO[1,z]と定常ピン
  z+2y=17、掃引行x=z+y+1=17の掃引帯O[pin,x+y+z]=O[17,33]、d=z格子行x=16では
  格子ピン2y+(d+z)/2=17=x+1がプレーン偶ラダーO[1,x+1]に吸収される（奇数z型）。
  値1は基底点z+1=16（d=z-1行x=15に出現）・帯開始z+2y+2=19・帯parity≡z (mod 2)
  （奇）、I帯はx偶数行のみ、tailはR>=x+17でH=(x+1) mod 2、R<=16(=z+1)は
  height-only縮約single_token(x+1,15,R)。独立監査は27,661,600照合・不一致0・
  独立プロセス3回実行でbyte-identicalであり、全称性の根拠は外帰納と署名帯表である。
---

## 命題・範囲

K1020は抽象残余ゲームのz=15・y=1切片を全x>=1・全R>=0で分類する。値2位置はx<=15で高さのみ縮約と同じ偶奇ラダー（x偶数O[1,x+1]・x奇数O[1,x]、d=z格子行x=16も格子ピン17=x+1が一致するためプレーン偶ラダー表示）、x=z+y+1=17の掃引行でO[1,33]=O[1,z]∪O[17,33]、x>=18で{1,3,5,7,9,11,13,15,17}（pin=z+2y=17・奇数zラダーO[1,z]）に定着。値1位置はx奇数<=13で∅、x偶数<=14でI[x+2,∞)、x=15（d=z-1行・x奇）で{16}有限、x=16（d=z格子行）で{16}∪I[18,∞)、x=17（掃引行）で{16}有限、x偶数>=18で{16}∪O[19,x+16]∪I[x+17,∞)、x奇数>=19で{16}∪O[19,x+16]有限。tailはR>=x+17で(x+1) mod 2、R<=16はheight-only縮約single_token(x+1,15,R)。

## 現在の根拠と限界

全称性はx外帰納と全Rを覆うA/B/C署名帯表による。B子はK0832単一トークンz=16（初使用・アンカー6,480点照合済み）、C子はK1018のz=14,y=1全称定理。監査は二つの直接再帰、アンカー、署名帯、mex、tail、height-only縮約を有限範囲（V4..V8・V10はx<=3000・R<=x+30、V13は閉形式のみでx<=100000の固定seed散点）で照合するもので、全称証明そのものではない。行候補はcross-z監査log第5便の予言域（pin=17・掃引帯O[17,33]・帯開始19・帯parity奇・tail x+17・格子d=z行吸収型）と全域一致しており二重独立導出である。height-only縮約R<=z+1の有限観察はz=15のV14（x<=500・R<=16・8,500点）でz=4..15の12値に拡大した（一般証明は未解決）。z=15のy>=2、z>=16、全高さを統合する一般式、y=1横断2系列の「任意z」全称式化、標準二次元盤の固定幅・q点版安定化長は未解決。
