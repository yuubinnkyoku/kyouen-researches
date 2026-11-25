---
id: K1018
title: 2トークン残余ゲーム z=14・y=1境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z14 y1 boundary slice]
relations:
- type: depends_on
  target: K0832
  note: 単一トークンz=15閉形式、一般tail、height-only縮約を使用する
- type: depends_on
  target: K1017
  note: C子の評価にz=13・y=1境界切片を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z14-y1-boundary-20261119/report.md
  role: proof
  note: x外帰納と全R署名帯表による全称証明
- path: research/experiments/vertical-fiber-two-token-z14-y1-boundary-20261119/verify_z14_y1.py
  role: verifier
  note: 順序保持・降順正準化の二直接再帰、子アンカー、署名帯・mex・tail・height-only縮約の独立監査
- path: research/experiments/vertical-fiber-two-token-z14-y1-boundary-20261119/output/audit.json
  role: data
  note: 27,661,160照合・不一致0・独立プロセス3回実行でbyte-identical
- path: research/experiments/vertical-fiber-two-token-z14-y1-boundary-20261119/census_z14_y1.py
  role: data
  note: 有限センサスと候補導出（output/census.txt・2回実行byte-identical）
- path: research/log/2026-11-19-vertical-fiber-two-token-z14-y1-boundary.md
  role: log
  note: z=14,y=1切片の選定・導出・監査・構造則・接続
scope: >-
  κ=1残余ゲームH(R;(x,y);z)の2トークン族における固定高さz=14、y=1、
  全x>=1・全R>=0。Grundy値0/1/2を完全分類する。
evidence: >-
  xに関する外帰納。A子は同じz=14,y=1のx-1行、B子はK0832の単一トークンz=15公式、
  C子は1 xor K1017(z=13,y=1)で評価する。x=1では2つの除去手が同じ単一トークン子へ
  合流する。x<=17の個別署名帯とx>=18の偶奇別定常署名帯が全R>=1を互いに素に被覆し、
  各帯のmexが本文のT/P閉形式を与える。値2位置はx>=17でラダーO[1,z-1]と定常ピン
  z+2y+1=17、掃引帯O[pin,x+y+z]=O[17,31]、h=z行x=13の拡張ラダーO[1,15]（d=12格子
  ピン2y+(d+z)/2=15と一致）。値1は基底点z+1=15・帯開始z+2y+2=18・帯parity≡z (mod 2)
  （偶）、I帯はx偶数行のみ、tailはR>=x+16でH=(x+1) mod 2、R<=15(=z+1)はheight-only縮約
  single_token(x+1,14,R)。独立監査は27,661,160照合・不一致0・独立プロセス3回実行で
  byte-identicalであり、全称性の根拠は外帰納と署名帯表である。
---
