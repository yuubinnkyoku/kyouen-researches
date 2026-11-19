---
id: K1014
title: 2トークン残余ゲーム z=11・y=3境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z11 y3 boundary slice]
relations:
- type: depends_on
  target: K0832
  note: 高さのみ縮約、Theorem T、一般tail、単一トークン全z公式を使用する
- type: depends_on
  target: K1013
  note: B子の評価にz=11,y=2境界切片を使用する
- type: depends_on
  target: K1005
  note: C子の評価にz=10,y=3境界切片を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z11-y3-boundary-20261119/report.md
  role: proof
  note: x外帰納と全R署名帯表による全称証明
- path: research/experiments/vertical-fiber-two-token-z11-y3-boundary-20261119/verify_z11_y3.py
  role: verifier
  note: 順序保持・正準化の2直接再帰、署名帯・mex・高さのみ縮約・tailの独立監査
- path: research/experiments/vertical-fiber-two-token-z11-y3-boundary-20261119/output/audit.json
  role: data
  note: x=3..300・49,915点の二再帰照合、不一致0、二回実行byte-identical
- path: research/log/2026-11-19-vertical-fiber-two-token-z11-y3-boundary.md
  role: log
  note: z=11,y=3切片の選定・証明・監査・次のy=4接続
scope: >-
  κ=1残余ゲームH(R;(x,y);z)の2トークン族における固定高さz=11、y=3、
  全x>=3・全R>=0。Grundy値0/1/2を完全分類する。
evidence: >-
  xに関する外帰納。x>=4ではA子を帰納仮説、B子をK1013のz=11,y=2公式、
  C子をK1005のz=10,y=3公式で評価する。x=3では二つのトークン減少手が同じ
  (2,3);11子へ合流する。x=3..16の個別署名帯とx>=17の偶奇別署名帯で
  全R>=1を被覆し、Theorem Tのmex規則で閉じる。R<=12は高さのみ縮約で
  v_single(x+3,11,R)に一致し、tailはR>=x+15でH=(x+3) mod 2。
  独立有限監査は49,915点の二再帰照合・不一致0であり、全称性の根拠は
  外帰納と署名帯表である。
---

## 命題・範囲

K1014は抽象残余ゲームのz=11・y=3切片を全x>=3・全R>=0で分類する。
値2位置はx=3で{1,3,5}、x=4,5で{1,3,5,7}、x=6,7で{1,3,5,7,9}、
x=8で{1,3,5,7,9,11,13}、x=9で{1,3,5,7,9,11}、x=10で
{1,3,5,7,9,11,15}、x=11..13で{1,3,5,7,9,11}、x=14で
{1,3,5,7,9,11,17}、x=15で{1,3,5,7,9,11}∪O[17,29]、
x>=16で{1,3,5,7,9,11,17}に定着する。値1位置とtailは証明報告の閉形式どおり。

## 現在の根拠と限界

全称性はx外帰納と全Rを覆うA/B/C署名帯表による。B子はK1013、
C子はK1005の全称定理。監査は二つの直接再帰、署名帯、mex、高さのみ縮約、
tailを有限範囲で照合するもので、全称証明そのものではない。
z=11のy>=4、z>=12の一般分類、標準二次元盤の固定幅・q点安定化長は未解決。
