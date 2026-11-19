---
id: K1047
title: 2トークン残余ゲーム z=14・y=5境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z14 y5 boundary slice]
relations:
- type: depends_on
  target: K0832
  note: 高さのみ縮約、Theorem T、単一トークン閉形式、一般tailを使用する
- type: depends_on
  target: K1031
  note: B子の評価にz=14・y=4境界切片を使用する
- type: depends_on
  target: K1045
  note: C子の評価に1 xor (z=13・y=5境界切片)を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z14-y5-boundary-20261119/report.md
  role: proof
  note: x外帰納と全Rを覆うA/B/C署名帯表による全称証明
- path: research/experiments/vertical-fiber-two-token-z14-y5-boundary-20261119/verify_z14_y5.py
  role: verifier
  note: 順序保持・降順正準化の二直接再帰、K1031/K1045子アンカー、署名帯・mex・低R縮約・tailの独立監査
- path: research/experiments/vertical-fiber-two-token-z14-y5-boundary-20261119/output/audit.json
  role: data
  note: 1,106,746照合・不一致0・二回実行byte-identicalの決定論的監査結果
- path: research/log/2026-11-19-vertical-fiber-two-token-z14-y5-boundary.md
  role: log
  note: 最新main確認、未解決切片の選定、証明・監査・次の課題
scope: >-
  κ=1残余ゲームH(R;(x,y);z)の2トークン族における固定高さz=14、y=5、
  全x>=5・全R>=0。Grundy値0/1/2を完全分類する。
evidence: >-
  xに関する外帰納。x=5では二つの等しいトークンの減少手が同じ(5,4);14
  多重集合子に合流し、K1031のx=5行を基底として使う。x>=6ではA子を帰納仮説、
  B子をK1031（z=14,y=4）、C子を1 xor K1045（z=13,y=5）で評価する。
  全R>=1のうち1<=R<=x+19はreport.mdの過渡行x=5..21と定常行x>=22偶数・
  x>=23奇数のA/B/C署名帯表が互いに素に被覆し、mex表から本文のT/Pが得られる。
  K0832からR<=15の高さのみ縮約とR>=x+20の一般tailも従う。独立監査は二直接再帰、
  子アンカー、署名帯、mex、低R、tail、散点を含む1,106,746照合で不一致0、
  二回実行byte-identical。有限監査は転写・実装照合であり、全称性はx外帰納と
  全R署名帯表による。
---

## 命題・範囲

全ての \(x\ge5\)、\(R\ge0\) について、\(H(R;(x,5);14)\) のGrundy値0/1/2を
report.mdの \(T(x),P(x)\) で完全分類する。低残容量は \(R\le15\) で単一トークン
\(x+5\) へ縮約し、高残容量は \(R\ge x+20\) で \((x+5)\bmod2\) となる。

## 現在の根拠と限界

全称性はx外帰納と全Rを覆うA/B/C署名帯表による。B子はK1031、C子はK1045の
全称定理であり、低R縮約・一般tailはK0832から従う。有限監査は二直接再帰・
子アンカー・署名帯・mex等の転写を照合するもので、証明そのものではない。

値1基底点は \(\{15,17,19,21,23\}=\{z+1,z+3,z+5,z+7,z+9\}\) で、y=5点仮説の
偶数高さ側の実例。pinは \(25=2y+z+1\)、掃引行は \(x=z+y+1=20\)、掃引帯は
\(O[25,39]\)。中間帯開始は \(z+2y+2=26\)。前倒し点21,23は
\(2y+(d+z)/2\)（\(d=x-y\)、\(d+z\equiv2\pmod4\)）で説明される。
z=14・y>=6、z>=15・y>=2、y>=2族の一般化、値1基底点y点仮説・d+z剰余格子の
一般証明、標準二次元盤の固定幅・q点版安定化長は未解決。
