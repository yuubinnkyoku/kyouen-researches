---
id: K0999
title: 2トークン残余ゲーム z=8・y=9境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z8 y9 boundary slice]
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームのA/B/C再帰、Theorem T、高R tailを使用する
- type: depends_on
  target: K0996
  note: B子と対角基底にz=8,y=8境界切片を使用する
- type: depends_on
  target: K0976
  note: C子にz=7・全y>=4の全Grundy公式を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z8-y9-boundary-20261119/report.md
  role: proof
  note: x外帰納と全xを覆うA/B/C署名帯表による全称証明
- path: research/experiments/vertical-fiber-two-token-z8-y9-boundary-20261119/verify_z8_y9.py
  role: verifier
  note: 順序付き・正準化直接mex再帰、K0996/K0976アンカー、署名帯・mex・tailを独立監査する検証器
- path: research/experiments/vertical-fiber-two-token-z8-y9-boundary-20261119/output/audit.json
  role: data
  note: 8,207,476検査・不一致0・二方式・二回実行byte-identical
- path: research/log/2026-11-19-vertical-fiber-two-token-z8-y9-boundary.md
  role: log
  note: z=8,y=9の閉形式・外帰納証明・独立監査・限界
scope: >-
  κ=1残余ゲームH(R;(x,9);8)の2トークン族における固定高さz=8、y=9、全x>=9・全R>=0。Grundy値0/1/2を完全分類する。
evidence: >-
  xに関する外帰納。x=9では二つのトークン減少手が同一の(9,8)子へ合流する。x>=10ではA子を帰納仮説、B子をK0996、C子をK0976で評価する。1<=R<=x+17の全域をx=9..19の過渡署名帯とx>=20の定常署名帯で被覆し、K0832 Theorem Tのmex制約で閉じる。R>=x+18はK0832の一般tail H=(x+9) mod 2で閉じる。独立監査は8,207,476検査・不一致0・二方式・二回実行byte-identical。有限監査は証明の代わりではなく、全称性はx外帰納と署名表による。
---

## 命題・範囲

全 \(x\ge9,R\ge0\) について \(H(R;(x,9);8)\) のGrundy値0/1/2を完全分類する。値2位置・値1位置の閉形式と高R tailは証明報告に記載する。

## 現在の根拠と限界

全称性はx外帰納による。x=9ではA/B子がK0996の同一局面へ合流し、C子はK0976のz=7,y>=4公式に帰着する。x>=10ではAを帰納仮説、BをK0996、CをK0976で評価し、1<=R<=x+17の全域を署名帯表で覆う。R>=x+18はK0832の高R tailで閉じる。有限監査は二方式の直接再帰と署名表の独立照合であり、全称証明そのものとは区別する。

本項は抽象残余ゲームのz=8,y=9切片である。z=8のy>=10は一様閉形式K1000で全y>=9として全称証明され、z=8の2トークン族に未解決境界は残っていない。z=9のy>=9、z>=10の全Grundy分類、全高さを統合する2トークン値2位置の一般式、標準二次元盤の固定幅・q点版の真の安定化長は未解決。
