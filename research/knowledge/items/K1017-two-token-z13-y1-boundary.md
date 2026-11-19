---
id: K1017
title: 2トークン残余ゲーム z=13・y=1境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z13 y1 boundary slice]
relations:
- type: depends_on
  target: K0832
  note: 単一トークンz=14閉形式、一般tail、height-only縮約を使用する
- type: depends_on
  target: K1016
  note: C子の評価にz=12・y=1境界切片を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z13-y1-boundary-20261119/report.md
  role: proof
  note: x外帰納と全R署名帯表による全称証明
- path: research/experiments/vertical-fiber-two-token-z13-y1-boundary-20261119/verify_z13_y1.py
  role: verifier
  note: 順序保持・降順正準化の二直接再帰、子アンカー、署名帯・mex・tail・height-only縮約の独立監査
- path: research/experiments/vertical-fiber-two-token-z13-y1-boundary-20261119/output/audit.json
  role: data
  note: 27,660,660照合・不一致0・独立プロセス3回実行でbyte-identical
- path: research/experiments/vertical-fiber-two-token-z13-y1-boundary-20261119/census_z13_y1.py
  role: data
  note: 有限センサスと候補導出（output/census.txt・2回実行byte-identical）
- path: research/log/2026-11-19-vertical-fiber-two-token-z13-y1-boundary.md
  role: log
  note: z=13,y=1切片の選定・導出・監査・構造則・接続
scope: >-
  κ=1残余ゲームH(R;(x,y);z)の2トークン族における固定高さz=13、y=1、
  全x>=1・全R>=0。Grundy値0/1/2を完全分類する。
evidence: >-
  xに関する外帰納。A子は同じz=13,y=1のx-1行、B子はK0832の単一トークンz=14公式、
  C子は1 xor K1016(z=12,y=1)で評価する。x=1では2つの除去手が同じ単一トークン子へ
  合流する。x<=15の個別署名帯とx>=16の偶奇別定常署名帯が全R>=1を互いに素に被覆し、
  各帯のmexが本文のT/P閉形式を与える。値2位置はx>=16でラダーO[1,z]と定常ピン
  z+2y=15、掃引帯O[pin,x+y+z]=O[15,29]、d=z格子点2y+(d+z)/2=15はx=14行で
  一般ラダー上端に一致する。値1は基底点z+1=14・帯開始z+2y+2=17・帯parity≡z (mod 2)、
  I帯はx偶数行のみtail R>=x+15へ接続する。tailはR>=x+15でH=(x+1) mod 2、
  R<=14(=z+1)はheight-only縮約single_token(x+1,13,R)。
  独立監査は27,660,660照合・不一致0・独立プロセス3回実行でbyte-identicalであり、
  全称性の根拠は外帰納と署名帯表である。
---

## 命題・範囲

K1017は抽象残余ゲームのz=13・y=1切片を全x>=1・全R>=0で分類する。値2位置はx<=13で高さのみ縮約と同じ偶奇ラダー（x偶数O[1,x+1]・x奇数O[1,x]、x<=14偶数行も同型）、x=15の掃引行でO[1,29]=O[1,13]∪O[15,29]、x>=16で{1,3,5,7,9,11,13,15}（pin=z+2y=15・奇数zラダーO[1,z]）に定着。値1位置はx奇数<=11で∅、x偶数<=12でI[x+2,∞)、x=13で{14}有限、x=14（d=z格子行）で{14}∪I[16,∞)、x=15で{14}有限、x偶数>=16で{14}∪O[17,x+14]∪I[x+15,∞)、x奇数>=17で{14}∪O[17,x+14]有限。tailはR>=x+15で(x+1) mod 2、R<=14はheight-only縮約single_token(x+1,13,R)。

## 現在の根拠と限界

全称性はx外帰納と全Rを覆うA/B/C署名帯表による。B子はK0832単一トークンz=14、C子はK1016のz=12,y=1全称定理。監査は二つの直接再帰、アンカー、署名帯、mex、tail、height-only縮約を有限範囲で照合するもので、全称証明そのものではない。行候補はcross-z監査log（d+z≡2 (mod 4)格子法則・安定域統一候補）の予言域（pin=15・掃引帯O[15,29]・帯開始17・帯parity奇・tail x+15）と全域一致している。z=13のy>=2、z>=14の一般分類、全高さを統合する2トークン値2位置の一般式、height-only縮約R<=z+1則の一般証明、標準二次元盤の固定幅・q点版安定化長は未解決。
