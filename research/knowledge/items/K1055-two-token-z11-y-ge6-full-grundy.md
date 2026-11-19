---
id: K1055
title: 2トークン残余ゲーム z=11・y>=6一様全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z11 uniform y-ge6 full grundy]
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームのA/B/C再帰、Theorem T、一般tailを使用する
- type: depends_on
  target: K1037
  note: y=6行のB子の基底にz=11,y=5境界切片(全x)を使用する
- type: depends_on
  target: K1002
  note: C子の評価にz=10・全x>=y>=6の全Grundy一様式(proved)を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z11-y-ge6-proof-20261119/report.md
  role: proof
  note: y強帰納と各行内x外帰納、(y,d)パラメトリックA/B/C署名帯表による全称証明
- path: research/experiments/vertical-fiber-two-token-z11-y-ge6-proof-20261119/bands.py
  role: verifier
  note: 署名帯表の正本実装（クラス別・parity別、閉形式値やエンジンを呼ばない独立アーティファクト）
- path: research/experiments/vertical-fiber-two-token-z11-y-ge6-proof-20261119/verify_z11_y_ge6_proof.py
  role: verifier
  note: 二直接mex再帰・K1037/K1002子アンカー・署名帯・mex・Theorem T・高さのみ縮約・tail・決定的散点の独立監査
- path: research/experiments/vertical-fiber-two-token-z11-y-ge6-proof-20261119/output/audit.json
  role: data
  note: 1,687,185検査・不一致0・二回実行・別プロセス別cwd byte-identical
- path: research/log/2026-11-19-vertical-fiber-two-token-z11-y-ge6-proof.md
  role: log
  note: 導出過程・d=13/d=11のA子影署名の同定・監査・限界
scope: >-
  κ=1残余ゲームH(R;(x,y);11)の2トークン族における固定高さz=11、全x>=y>=6・全R>=0。
  Grundy値0/1/2を完全分類する。
evidence: >-
  y強帰納と各行内のx外帰納。y=6行ではB子をK1037（z=11,y=5切片）で、C子を
  1 xor K1002（z=10一様式・proved）で評価し、d=0でA=Bが合流してx外帰納が出発する。
  y>=7の行ではB子をy帰納仮定、A子をx帰納仮定、C子を同じくK1002で評価する。
  1<=R<=x+y+11の全域を(y,d)パラメトリックなd別署名帯表で被覆し、K0832 Theorem Tの
  mex制約で閉じる。R>=x+y+12はK0832の一般tailで閉じる。独立監査は1,687,185検査・
  不一致0・二方式・二回実行byte-identical。有限監査は証明の代わりではなく、
  全称性は二段帰納と署名表による。
---

## 命題・範囲

全 \(x\ge y\ge6,R\ge0\) について \(H(R;(x,y);11)\) のGrundy値0/1/2を完全分類する。値2位置は基本ラダー{1,3,...,11}に前倒し格子点（d=3:2y+7、d=7:2y+9、d=11:2y+11、いずれもd+z≡2 (mod 4)の格子式2y+(d+z)/2でd=11は定常pin 2y+zに一致）、掃引帯d=12のO[2y+11,S+11]、d>=13の定常pin 2y+11。値1位置はd別に5区分（偶d段階帯E[12,2y+4+2⌈d/4⌉]、d=12と偶d>=14のE[12,2y+10]、偶d>=14の奇帯O[2y+13,S+11]、奇d<=11の偶全域E[12,S+11]と奇帯O[2y+7+2⌊(d+1)/4⌋,S+10]、奇d>=13のE[12,2y+10]とO[2y+13,S+10]）。tailはR>=x+y+12で(x+y) mod 2。署名帯ではd=11の偶末尾が「023」、d=13が「12」、d>=15が「1」で、いずれもA子（d-1列）とC子（z=10掃引行）の値域から導出される。完全な式は証明報告を正本とする。

## 現在の根拠と限界

全称性はy強帰納と各行内x外帰納による。y=6行のB子はK1037で、d>=12ではK1037のx>=18定常行（値2={1,3,...,11,21}、値1={12,14,16,18,20}∪O[23,x+17]、tail x+17）が本項の帯表と原文一致し、d=1..11はK1037の遷移セル12個の有限解析で一致する。(y,d)=(6,0)はA=B合流の縮退セル（K1037のh=z行x=6の奇ラダーO[1,15]が偶行14,16に値2を供給し署名は[12,16]:02）。C子は全行でK1002（proved）。y>=7の行ではB子をy帰納仮定、A子をx帰納仮定で評価する。1<=R<=S+11の全域をd別のパラメトリック署名帯表で覆い、R>=S+12はK0832の一般tailで閉じる。有限監査（1,687,185検査・不一致0・別プロセス別cwd二回実行byte-identical）は証明そのものではなく独立実装照合であり、全称証明と区別する。

z=10の一様化（K1011）はy=9まで3切片（K1008..K1010）を要したが、z=11では基底アンカー切片（y=5）が直上のy=6から一様族に入るためy>=6で直ちに一様化する。値1基底点{z+1,z+3,...,z+2y-1}はy点仮説の第7例（y=6では{12,14,16,18,20,22}）。これによりz=11はy=1..3切片（K1012..K1014）、y=4（K1015）、y=5（K1037）と本項の併せ技で2トークン族で初めて全y>=1が全称分類済みの高さとなった。奇数z族（z=9,13,15の既出版と本項）共通のラダーO[1,z]・前倒し格子d=z-8+4k・pin 2y+z・掃引行d=z+1・定常d>=z+2構造の統一式、d=z+2のA子影署名の一般化、z>=12の全Grundy分類、値1基底点y点仮説の一般証明、標準二次元盤の固定幅・q点版の真の安定化長は未解決。標準二次元盤へ直接転送する結果ではない。
