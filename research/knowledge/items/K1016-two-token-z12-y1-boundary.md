---
id: K1016
title: 2トークン残余ゲーム z=12・y=1境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z12 y1 boundary slice]
relations:
- type: depends_on
  target: K0832
  note: 単一トークンz=13閉形式、一般tail、高さのみ縮約、Theorem Tを使用する
- type: depends_on
  target: K1012
  note: C子の評価にz=11・y=1境界切片を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z12-y1-boundary-20261119/report.md
  role: proof
  note: x外帰納と全R署名帯表による全称証明
- path: research/experiments/vertical-fiber-two-token-z12-y1-boundary-20261119/verify_z12_y1.py
  role: verifier
  note: 順序保持・降順正準化の二直接再帰、子アンカー、署名帯・mex・tail・高さのみ縮約の独立監査
- path: research/experiments/vertical-fiber-two-token-z12-y1-boundary-20261119/output/audit.json
  role: data
  note: 27,660,160照合・不一致0・独立プロセス3回実行でbyte-identical
- path: research/experiments/vertical-fiber-two-token-z12-y1-boundary-20261119/census_z12_y1.py
  role: data
  note: 有限センサスと候補導出（output/census.txt・2回実行byte-identical）
- path: research/log/2026-11-19-vertical-fiber-two-token-z12-y1-boundary.md
  role: log
  note: z=12,y=1切片の選定・導出・監査・次のy=2接続
scope: >-
  κ=1残余ゲームH(R;(x,y);z)の2トークン族における固定高さz=12、y=1、
  全x>=1・全R>=0。Grundy値0/1/2を完全分類する。
evidence: >-
  xに関する外帰納。A子は同じz=12,y=1のx-1切片、B子はK0832の単一トークンz=13公式、
  C子は1 xor K1012(z=11,y=1)で評価する。x=1では2つの除去手が同じ単一トークン子へ
  合流する。x=1..15の個別署名帯とx>=16の偶奇別定常署名帯が全R>=1を互いに素に被覆し、
  各帯のmexが本文のT/P閉形式を与える。値2位置はx>=15でラダーO[1,11]と定常ピン
  2y+z+[z偶]=15、掃引帯O[15,27]=O[pin,x+y+z]、x=z-1行の前倒し点z+1=13。
  tailはR>=x+14でH=(x+1) mod 2、R<=13は高さのみ縮約v_single(x+1,12,R)。
  独立監査は27,660,160照合・不一致0・独立プロセス3回実行でbyte-identicalであり、
  全称性の根拠は外帰納と署名帯表である。
---

## 命題・範囲

K1016は抽象残余ゲームのz=12・y=1切片を全x>=1・全R>=0で分類する。値2位置はx<=9で高さのみ縮約ラダー、x=10でO[1,11]、x=11でO[1,13]（前倒し点z+1=13はx=z-1行にのみ現れる）、x=12,13でO[1,11]、x=14の掃引行でO[1,11]∪O[15,27]、x>=15で{1,3,5,7,9,11,15}（pin=2y+z+[z偶]=15）に定着。値1位置はx=2,4,6,8,10のI[x+2,∞)、x=12のI[13,∞)、x=13の{13}有限、x>=14偶数の{13}∪E[16,x+12]∪I[x+14,∞)、x>=15奇数の{13}∪E[16,x+13]。tailはR>=x+14で(x+1) mod 2。

## 現在の根拠と限界

全称性はx外帰納と全Rを覆うA/B/C署名帯表による。B子はK0832単一トークンz=13、C子はK1012のz=11,y=1全称定理。監査は二つの直接再帰、アンカー、署名帯、mex、tail、高さのみ縮約を有限範囲で照合するもので、全称証明そのものではない。行候補は同日の別レーンによるz横断有限監査（第1便: d+z≡2 (mod 4)格子法則・安定域統一候補・149,142アンカー点、第2便追記: 出版子のみによるA/B/C mex整合2,083,000点+固定seed散点25,000点）と独立に全行一致しており、二重独立導出となっている。z=12のy>=2、z>=13の一般分類、全高さを統合する2トークン値2位置の一般式、標準二次元盤の固定幅・q点版安定化長は未解決。
