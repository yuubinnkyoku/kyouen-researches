---
id: K1017
title: 2トークン残余ゲーム z=12・y=2境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z12 y2 boundary slice]
relations:
- type: depends_on
  target: K0832
  note: 単一トークン全z閉形式、一般tail、高さのみ縮約、Theorem Tを使用する
- type: depends_on
  target: K1016
  note: B子の評価にz=12,y=1境界切片を使用する
- type: depends_on
  target: K1013
  note: C子の評価にz=11,y=2境界切片を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z12-y2-boundary-20261119/report.md
  role: proof
  note: x外帰納と全R署名帯表による全称証明
- path: research/experiments/vertical-fiber-two-token-z12-y2-boundary-20261119/verify_z12_y2.py
  role: verifier
  note: 順序保持・降順正準化の二直接再帰、子アンカー、署名帯・mex・tail・高さのみ縮約の独立監査
- path: research/experiments/vertical-fiber-two-token-z12-y2-boundary-20261119/output/audit.json
  role: data
  note: 9,237,809照合・不一致0
- path: research/log/2026-11-19-vertical-fiber-two-token-z12-y2-boundary.md
  role: log
  note: z=12,y=2切片の導出・証明・監査・次のy=3接続
scope: >-
  κ=1残余ゲームH(R;(x,y);z)の2トークン族における固定高さz=12、y=2、
  全x>=2・全R>=0。Grundy値0/1/2を完全分類する。
evidence: >-
  xに関する外帰納。A子は同じz=12,y=2のx-1行、B子はK1016のz=12,y=1全称公式、
  C子は1 xor K1013のz=11,y=2全称公式で評価する。x=2では2つのトークン減少手が
  同じ(2,1);12子に合流する。x=2..16の個別署名帯とx>=17奇/x>=18偶の定常署名帯が
  全R>=1を被覆し、各帯のmexが本文のT/P閉形式を与える。定常値2位置は
  O[1,11]とpin=17=2y+z+[z偶]、掃引行はx=15=z+y+1で掃引帯O[17,29]。
  値1の基底点は{13,15}、帯開始は18=z+2y+2、tailはR>=x+15でH=(x+2) mod 2、
  R<=13は高さのみ縮約v_single(x+2,12,R)。独立監査は9,237,809照合・不一致0。
  全称性の根拠は外帰納と全R署名帯表であり、有限監査自体ではない。
---
