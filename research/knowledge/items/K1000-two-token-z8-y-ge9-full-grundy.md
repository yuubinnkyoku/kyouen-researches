---
id: K1000
title: 2トークン残余ゲーム z=8・y>=9一様全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z8 uniform y>=9 full grundy]
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームのA/B/C再帰、Theorem T、一般tailを使用する
- type: depends_on
  target: K0996
  note: y=9行のB子の基底にz=8,y=8境界切片を使用する
- type: depends_on
  target: K0976
  note: C子の評価にz=7・全y>=4の全Grundy一様式を使用する
- type: generalizes
  target: K0999
  note: 本項の一様式のy=9特殊化はK0999の閉形式・署名帯表と完全一致する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z8-y-ge9-proof-20261119/report.md
  role: proof
  note: y強帰納と各行内x外帰納、(y,d)パラメトリックA/B/C署名帯表による全称証明
- path: research/experiments/vertical-fiber-two-token-z8-y-ge9-proof-20261119/verify_z8_y_ge9_proof.py
  role: verifier
  note: 順序付き・正準化直接mex再帰、K0996/K0976アンカー、K0995/K0996/K0999切片再生、署名帯・mex・tailを独立監査する検証器
- path: research/experiments/vertical-fiber-two-token-z8-y-ge9-proof-20261119/output/audit.json
  role: data
  note: 7,581,441検査・不一致0・二方式・二回実行byte-identical
- path: research/log/2026-11-19-vertical-fiber-two-token-z8-y-ge9-proof.md
  role: log
  note: z=8,y>=9の一様閉形式・二段帰納証明・独立監査・限界
scope: >-
  κ=1残余ゲームH(R;(x,y);8)の2トークン族における固定高さz=8、全x>=y>=9・全R>=0。Grundy値0/1/2を完全分類する。
evidence: >-
  y強帰納と各行内のx外帰納。y=9行ではB子をK0996、C子を1 xor K0976(z=7全y>=4一様式)で評価し、d=0でA=Bが合流してx外帰納が出発する。y>=10の行ではB子をy帰納仮定、A子をx帰納仮定、C子を同じくK0976で評価する。1<=R<=x+y+8の全域を(y,d)パラメトリックなd別署名帯表で被覆し、K0832 Theorem Tのmex制約で閉じる。R>=x+y+9はK0832の一般tailで閉じる。独立監査は7,581,441検査・不一致0・二方式・二回実行byte-identical。有限監査は証明の代わりではなく、全称性は二段帰納と署名表による。同一式はy=9のK0999、y=8のK0996、y=7のK0995の閉形式を有限全域で正確に再現し、y=5,6はエンジン直接照合で一致する。これによりz=8の2トークン族は全y>=1で全称分類済みとなる。
---

## 命題・範囲

全 \(x\ge y\ge9,R\ge0\) について \(H(R;(x,y);8)\) のGrundy値0/1/2を完全分類する。値2位置・値1位置の(x,y)パラメトリック閉形式（d=x−yと2yで表す）と高R tailは証明報告に記載する。

## 現在の根拠と限界

全称性はy強帰納と各行内x外帰納による。y=9行ではB子をK0996、C子を1 xor K0976で評価し、A子をx外帰納で評価する。d=0ではA=BがK0996の同一局面へ合流する。y>=10の行ではB子をy帰納仮定、A子をx帰納仮定、C子を同じくK0976で評価する。1<=R<=x+y+8の全域をd別のパラメトリック署名帯表で覆い、R>=x+y+9はK0832の一般tailで閉じる。有限監査は二方式の直接再帰、アンカー再構成と署名表の独立照合であり、全称証明そのものとは区別する。

本項は抽象残余ゲームのz=8,y>=9一様切片である。y<=4の行は本式の適用外の逸脱スライスで、各切片証明（K0983・K0984・K0986・K0987）が全称性を担い、y=5..8の行も各切片証明（K0991・K0993・K0995・K0996）による。z=9のy>=9、z>=10の全Grundy分類、全高さを統合する2トークン値2位置の一般式、標準二次元盤の固定幅・q点版の真の安定化長は未解決。
