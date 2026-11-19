---
id: K1062
title: 2トークン残余ゲーム z=14・y>=6一様全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z14 uniform y-ge6 full grundy]
relations:
- type: depends_on
  target: K0832
  note: A/B/C再帰、単一トークン閉形式、一般tailを使用する
- type: depends_on
  target: K1047
  note: y=6基底行のB子をz=14,y=5全x定理で閉じる
- type: depends_on
  target: K1061
  note: 全y>=6行のC子をz=13一様全Grundy定理で閉じる
artifacts:
- path: research/experiments/vertical-fiber-two-token-z14-y-ge6-proof-20261120/report.md
  role: proof
  note: y強帰納・行内x外帰納と全R A/B/C署名帯表による全称証明
- path: research/experiments/vertical-fiber-two-token-z14-y-ge6-proof-20261120/verify_z14_y_ge6.py
  role: verifier
  note: 二直接再帰、K1047/K1061子アンカー、署名帯・mex、低R系、tailの独立監査
- path: research/experiments/vertical-fiber-two-token-z14-y-ge6-proof-20261120/output/audit.json
  role: data
  note: 1,852,619検査・不一致0・二回実行と別cwdでbyte-identical
- path: research/log/2026-11-20-vertical-fiber-two-token-z14-y-ge6-proof.md
  role: log
  note: 重複確認、式の導出、過渡セル、監査と次の未解決範囲
scope: >-
  κ=1残余ゲームH(R;(x,y);14)の2トークン族における固定高さz=14、
  全x>=y>=6・全R>=0。Grundy値0/1/2を本文と証明報告のT/P式で完全分類する。
evidence: >-
  yに関する強帰納と、各y行内のx外帰納。y=6のB子はK1047、全行のC子は
  1 xor K1061、y>=7のB子はy帰納仮定、A子はx帰納仮定で評価する。
  1<=R<=S+14（S=x+y）の全域をd=x-y別・parity別のA/B/C署名帯表で一意被覆し、
  mexを取る。R=0は終局、R>=S+15はK0832一般tailで閉じる。
  独立監査は1,852,619検査・不一致0・二回実行および別cwdでbyte-identical。
  有限監査は証明そのものではなく、全称性は二段帰納と記号的署名帯表による。
---
  
## 命題・範囲

全ての \(x\ge y\ge6\)、\(R\ge0\) について、\(H(R;(x,y);14)\) のGrundy値0/1/2を
report.mdの \(T(x,y),P(x,y)\) で完全分類する。低残容量は \(R\le20\) で単一トークン
\(S=x+y\) に一致し、高残容量は \(R\ge S+15\) で \(S\bmod2\) となる。

## 現在の根拠と限界

全称性はy強帰納・各行内x外帰納と、全Rを覆うA/B/C署名帯表による。
y=6のB子はK1047、C子はK1061、y>=7のB子は強帰納仮定、A子はx外帰納仮定。
低Rの \(R\le20\) 単一トークン一致は閉形式からの族固有の系であり、K0832の一般条件
\(R\le z+1=15\) を一般定理として拡張する主張ではない。最初の一様反例は
\((y,d,R)=(6,2,21)\) で、\(H(21;(8,6);14)=0\)、単一トークン値は2。
高R tailはK0832から従う。

値1基底点はd>=14で
\(\{15,17,\ldots,2y+13\}=\{z+1,z+3,\ldots,z+2y-1\}\) のちょうどy点。
定常pinは \(2y+z+1=2y+15\)、掃引行は \(d=z+1=15\)。
前倒し点 \(2y+(d+z)/2\) は \(d+z\equiv2\pmod4\) の格子に乗る。
過渡セルは \((6,0),(7,0),(6,1),(6,2),(6,3),(7,1),(7,3)\)。

z=15・y>=6はB=K1049、C=1 xor K1062で両子が揃い、次の一様化候補。
z>=16・y>=2の未解決切片、値1基底点y点仮説・pin格子の全z一般証明、
標準二次元盤の固定幅・q点版の真の安定化長は未解決。
