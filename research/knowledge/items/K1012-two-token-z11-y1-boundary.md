---
id: K1012
title: 2トークン残余ゲーム z=11・y=1境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z11 y1 boundary slice]
relations:
- type: depends_on
  target: K0832
  note: 単一トークンz=12閉形式、一般tail、Theorem Tを使用する
- type: depends_on
  target: K1003
  note: C子の評価にz=10・y=1境界切片を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z11-y1-boundary-20261119/report.md
  role: proof
  note: x外帰納と全R署名帯表による全称証明
- path: research/experiments/vertical-fiber-two-token-z11-y1-boundary-20261119/verify_z11_y1.py
  role: verifier
  note: 順序保持・正準化直接再帰、A/B/Cアンカー、署名帯・mex・tailの独立監査
- path: research/experiments/vertical-fiber-two-token-z11-y1-boundary-20261119/output/audit.json
  role: data
  note: 27,653,160比較点・不一致0・二回実行byte-identical
- path: research/log/2026-11-19-vertical-fiber-two-token-z11-y1-boundary.md
  role: log
  note: z=11,y=1切片の選定・証明・監査・次のy=2接続
scope: >-
  κ=1残余ゲームH(R;(x,y);z)の2トークン族における固定高さz=11、y=1、
  全x>=1・全R>=0。Grundy値0/1/2を完全分類する。
evidence: >-
  xに関する外帰納。A子は同じz=11,y=1のx-1切片、B子はK0832の単一トークンz=12公式、
  C子は1 xor K1003(z=10,y=1)で評価する。x=1ではA手がなく、二つの除去手は同じ
  単一トークン子へ合流する。x=1..14の個別署名帯とx>=15の偶奇別定常署名帯で全R>=1を
  被覆し、各帯のmexが本文のT/P閉形式を与える。一般tailはR>=x+13でH=(x+1) mod 2。
  独立監査は27,653,160比較点・不一致0・二回実行byte-identicalであり、全称性の根拠は
  外帰納と署名帯表である。
---

## 命題・範囲

K1012は抽象残余ゲームのz=11・y=1切片を全x>=1・全R>=0で分類する。値2位置はx<=12でO[1,x+1]、x=13でO[1,25]、x>=14で{1,3,5,7,9,11,13}。値1位置はx=1,3,5,7,9で空、x=2,4,6,8,10でI[x+2,∞)、x=11で{12}、x=12で{12}∪I[14,∞)、x=13で{12}、x>=14偶数で{12}∪O[15,x+13]∪I[x+14,∞)、x>=15奇数で{12}∪O[15,x+12]。tailはR>=x+13で(x+1) mod 2。

## 現在の根拠と限界

全称性はx外帰納と全Rを覆うA/B/C署名帯表による。B子はK0832単一トークンz=12、C子はK1003のz=10,y=1全称定理。監査は二つの直接再帰、アンカー、署名帯、mex、tailを有限範囲で照合するもので、全称証明そのものではない。z=11のy>=2、z>=12の一般分類、標準二次元盤の固定幅・q点版安定化長は未解決。
