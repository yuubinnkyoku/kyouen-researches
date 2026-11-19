---
id: K1048
title: 2トークン残余ゲーム z=15・y=4境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z15 y4 boundary slice]
relations:
- type: depends_on
  target: K0832
  note: 高さのみ縮約、Theorem T、単一トークン閉形式、一般tailを使用する
- type: depends_on
  target: K1034
  note: B子の評価とx=4帰納基底にz=15・y=3境界切片を使用する
- type: depends_on
  target: K1031
  note: C子の評価に1 xor (z=14・y=4境界切片)を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z15-y4-boundary-20261120/report.md
  role: proof
  note: x外帰納と全Rを覆うA/B/C署名帯表による全称証明
- path: research/experiments/vertical-fiber-two-token-z15-y4-boundary-20261120/verify_z15_y4.py
  role: verifier
  note: 順序保持・降順正準化の二直接再帰、K1034/K1031子アンカー、署名帯・mex・低R縮約・tailの独立監査
- path: research/experiments/vertical-fiber-two-token-z15-y4-boundary-20261120/output/audit.json
  role: data
  note: 2,128,617照合・不一致0・二回実行byte-identicalの決定論的監査結果
- path: research/log/2026-11-20-vertical-fiber-two-token-z15-y4-boundary.md
  role: log
  note: 最新main確認、未解決範囲との照合、証明・監査・次の課題
scope: >-
  κ=1残余ゲームH(R;(x,y);z)の2トークン族における固定高さz=15、y=4、
  全x>=4・全R>=0。Grundy値0/1/2を完全分類する。
evidence: >-
  xに関する外帰納。x=4ではA/B子が同じ(4,3);15多重集合子に合流し、
  K1034のx=4行を基底として使う。x>=5ではA子を帰納仮説、B子をK1034
  （z=15,y=3）、C子を1 xor K1031（z=14,y=4）で評価する。全R>=1のうち
  1<=R<=x+19はreport.mdの過渡行x=4..21と定常行x>=23奇数/x>=22偶数の
  A/B/C署名帯表が互いに素に被覆し、mex表からT/Pが得られる。K0832から
  R<=16の高さのみ縮約とR>=x+20の一般tailも従う。独立監査は二直接再帰、
  子アンカー、署名帯、mex、低R、tail、散点を含む2,128,617照合で不一致0、
  二回実行byte-identical。有限監査は転写・実装照合であり、全称性は
  x外帰納と全R署名帯表による。
---

## 命題・範囲

全ての x≥4、R≥0 について、H(R;(x,4);15)のGrundy値0/1/2をreport.mdのT(x),P(x)で完全分類する。低残容量はR≤16で単一トークンx+4へ縮約し、高残容量はR≥x+20で(x+4) mod 2となる。

## 現在の根拠と限界

全称性はx外帰納と全Rを覆うA/B/C署名帯表による。B子はK1034、C子はK1031の全称定理であり、低R縮約・一般tailはK0832から従う。有限監査は二直接再帰・子アンカー・署名帯・mex等の転写を照合するもので、証明そのものではない。

値1基底点は{16,18,20,22}={z+1,z+3,z+5,z+7}でy=4点仮説の4点型。定常pinは23=2y+z、掃引行はx=z+y+1=20、掃引帯はO[23,39]。前倒し点21はd+z≡2 (mod 4)の格子式2y+(d+z)/2と一致する。

z=15・y>=6、z=14・y>=6、z>=16・y>=2、y>=2族の一般化、値1基底点y点仮説・d+z剰余格子の一般証明、標準二次元盤の固定幅・q点安定化長は未解決.