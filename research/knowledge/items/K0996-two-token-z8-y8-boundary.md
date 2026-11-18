---
id: K0996
title: 2トークン残余ゲーム z=8・y=8境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z8 y8 boundary slice]
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームのA/B/C再帰、Theorem T、高R tailを使用する
- type: depends_on
  target: K0995
  note: B子の評価にz=8,y=7境界切片を使用する
- type: depends_on
  target: K0976
  note: C子の評価にz=7,y>=4の全称公式を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z8-y8-boundary-20261119/report.md
  role: proof
  note: x外帰納と全xを覆うA/B/C署名帯表による全称証明
- path: research/experiments/vertical-fiber-two-token-z8-y8-boundary-20261119/verify_z8_y8.py
  role: verifier
  note: 順序付き・正準化直接mex再帰、K0995/K0976アンカー、署名帯・mex・tailを独立監査する検証器
- path: research/experiments/vertical-fiber-two-token-z8-y8-boundary-20261119/output/audit.json
  role: data
  note: 8,201,193検査・不一致0・二方式・二回実行byte-identical
- path: research/log/2026-11-19-vertical-fiber-two-token-z8-y8-boundary.md
  role: log
  note: 最新mainとの照合、z=8,y=8の閉形式・外帰納証明・独立監査・限界
scope: >-
  κ=1残余ゲームH(R;(x,y);z)の2トークン族における固定高さz=8、y=8、全x>=8・全R>=0。Grundy値0/1/2を完全分類する。
evidence: >-
  xに関する外帰納。x=8では二つのトークン減少手が同一の(x,7)子へ合流する。x>=9ではA子を帰納仮説、B子をK0995、C子をK0976で評価する。1<=R<=x+16の全域をx=8..18の過渡切片とx>=19の定常署名帯表で被覆し、K0832 Theorem Tのmex制約で閉じる。R>=x+17はK0832の一般tailで閉じる。独立監査は8,201,193検査・不一致0・二方式・二回実行byte-identical。有限監査は証明の代わりではなく、全称性はx外帰納と署名表による。
---

## 命題・範囲

\[
H(R;(x,8);8)\in\{0,1,2\}
\]
を全 \(x\ge8,R\ge0\) で分類する。値2位置と値1位置の完全な閉形式は対応する証明報告に記載する。

## 現在の根拠と限界

全称性はx外帰納による。x=8ではA/B子がK0995の同一局面へ合流し、C子はK0976に帰着する。x>=9ではAを帰納仮説、BをK0995、CをK0976で評価し、1<=R<=x+16の全域を署名帯表で覆う。R>=x+17はK0832の高R tailで閉じる。有限監査は二方式の直接再帰と署名表の独立照合であり、全称証明そのものとは区別する。

本項は抽象残余ゲームの固定切片である。z=8のy>=9、z=9のy>=8、z>=10の全Grundy分類、全高さを統合する2トークン値2位置の一般式、標準二次元盤の固定幅・q点版の真の安定化長は未解決。
