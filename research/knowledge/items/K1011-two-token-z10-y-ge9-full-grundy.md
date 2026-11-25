---
id: K1011
title: 2トークン残余ゲーム z=10・y>=9一様全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z10 uniform y-ge9 full grundy]
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームのA/B/C再帰、Theorem T、一般tailを使用する
- type: depends_on
  target: K1010
  note: y=9行のB子の基底にz=10,y=8境界切片を使用する
- type: depends_on
  target: K1001
  note: C子の評価にz=9・全y>=9の全Grundy一様式を使用する
- type: supports
  target: K1002
  note: K1002のy>=9領域を全称証明し、K1002全体のproved昇格を完成させる
artifacts:
- path: research/experiments/vertical-fiber-two-token-z10-y-ge9-proof-20261119/report.md
  role: proof
  note: y強帰納と各行内x外帰納、(y,d)パラメトリックA/B/C署名帯表による全称証明
- path: research/experiments/vertical-fiber-two-token-z10-y-ge9-proof-20261119/verify_z10_y_ge9_proof.py
  role: verifier
  note: 順序付き・正準化直接mex再帰、K1010/K1001アンカー、双転写・census恒等、y=8行再生・y=6..8照合・署名帯・mex・tail独立監査
- path: research/experiments/vertical-fiber-two-token-z10-y-ge9-proof-20261119/output/audit.json
  role: data
  note: 7,657,856検査・不一致0・二方式・二回実行byte-identical
- path: research/log/2026-11-19-vertical-fiber-two-token-z10-y-ge9-proof.md
  role: log
  note: z=10,y>=9の一様閉形式・二段帰納証明・独立監査・K1002昇格・限界
scope: >-
  κ=1残余ゲームH(R;(x,y);10)の2トークン族における固定高さz=10、全x>=y>=9・全R>=0。
  Grundy値0/1/2を完全分類する。分類式はK1002の一様式（y>=6）のy>=9制限に一致する。
evidence: >-
  y強帰納と各行内のx外帰納。y=9行ではB子をK1010、C子を1 xor K1001(z=9全y>=9一様式)
  で評価し、d=0でA=Bが合流してx外帰納が出発する。y>=10の行ではB子をy帰納仮定、
  A子をx帰納仮定、C子を同じくK1001で評価する。1<=R<=x+y+10の全域を(y,d)パラメ
  トリックなd別署名帯表で被覆し、K0832 Theorem Tのmex制約で閉じる。R>=x+y+11は
  K0832の一般tailで閉じる。独立監査は7,657,856検査・不一致0・二方式・二回実行
  byte-identical。有限監査は証明の代わりではなく、全称性は二段帰納と署名表による。
  K1010のy=8行閉形式は双転写恒等（57,135点）と公式再生（55,670点）で、K1002候補
  のcensus転写とは恒等（54,315点）で確認した。y=6..8行はエンジン直接照合で一致し、
  これによりK1002は全x>=y>=6・全R>=0で証明完了（proved昇格）、z=10族はy=1..5の
  各切片定理（K1003..K1007）と併せ全y>=1で全称分類済みとなる。
---

## 命題・範囲

全 \(x\ge y\ge9,R\ge0\) について \(H(R;(x,y);10)\) のGrundy値0/1/2を完全分類する。値2位置は基本ラダー{1,3,5,7,9}にd=0,4,8の前倒し点2y+5,2y+7,2y+9、d=11の掃引帯O[2y+11,S+10]、d>=12の定常点2y+11を加えた集合。値1位置はdの偶奇と過渡帯で4区分され、tailは \(R\ge x+y+11\) で \((x+y)\bmod2\)。完全な式は証明報告を正本とする。

## 現在の根拠と限界

全称性はy強帰納と各行内x外帰納による。y=9行ではB子をK1010、C子を1 xor K1001で評価し、A子を行内x外帰納で評価する。d=0ではA=BがK1010の同一局面へ合流する。y>=10の行ではB子をy帰納仮定、A子をx帰納仮定、C子を同じくK1001で評価する。1<=R<=x+y+10の全域をd別のパラメトリック署名帯表で覆い、R>=x+y+11はK0832の一般tailで閉じる。有限監査は二方式の直接再帰、アンカー再構成、双転写恒等、K1002census転写恒等、署名表の独立照合であり、全称証明そのものとは区別する。

本項によりK1002の主張域y>=6のうち未証明だったy>=9の中間帯12<=R<=S+10が閉じ、K1002は全x>=y>=6・全R>=0でprovedに昇格した（y=6..8はK1008・K1009・K1010の切片定理と恒等、R<=11は高さのみ縮約、R>=S+11は一般tail）。あわせてz=10の2トークン族はy=1..5切片・y=6..8切片・本項の併せ技で全y>=1で全称分類済みとなる。z>=11の全Grundy分類、全高さを統合する2トークン値2位置の一般式、標準二次元盤の固定幅・q点版の真の安定化長は未解決。標準二次元盤へ直接転送する結果ではない。
