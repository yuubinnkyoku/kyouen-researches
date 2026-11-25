---
id: K1065
title: 2トークン残余ゲーム z=15・y>=6一様全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z15 uniform y-ge6 full grundy]
relations:
- type: depends_on
  target: K0832
  note: A/B/C再帰、単一トークン閉形式、一般tailを使用する
- type: depends_on
  target: K1049
  note: y=6基底行のB子をz=15,y=5全x定理で閉じる
- type: depends_on
  target: K1062
  note: 全y>=6行のC子をz=14一様全Grundy定理で閉じる
artifacts:
- path: research/experiments/vertical-fiber-two-token-z15-y-ge6-proof-20261120/report.md
  role: proof
  note: y強帰納・行内d外帰納と全R A/B/C署名帯表による全称証明
- path: research/experiments/vertical-fiber-two-token-z15-y-ge6-proof-20261120/verify_z15_y_ge6.py
  role: verifier
  note: 二直接再帰、K1049/K1062子アンカー、署名帯・mex、低R縮約、tailの独立監査
- path: research/experiments/vertical-fiber-two-token-z15-y-ge6-proof-20261120/output/audit.json
  role: data
  note: 1,973,080検査・不一致0・二回実行と別cwdでbyte-identical
- path: research/log/2026-11-20-vertical-fiber-two-token-z15-y-ge6-proof.md
  role: log
  note: 重複確認、式の導出、過渡セル、監査と次の未解決範囲
scope: >-
  κ=1残余ゲームH(R;(x,y);15)の2トークン族における固定高さz=15、
  全x>=y>=6・全R>=0。Grundy値0/1/2を本文と証明報告のT/P式で完全分類する。
evidence: >-
  yに関する強帰納と、各y行内のd=x-y外帰納。y=6のB子はK1049、全行のC子は
  1 xor K1062、y>=7のB子はy帰納仮定、A子はd外帰納仮定で評価する。
  1<=R<=S+15（S=x+y）の全域を縮退セル・偶奇別の記号的A/B/C署名帯表で一意被覆し、
  mexを取る。R=0は終局、R>=S+16はK0832一般tailで閉じる。
  独立監査は1,973,080検査・不一致0・二回実行および別cwdでbyte-identical。
  有限監査は証明そのものではなく、全称性は二段帰納と記号的署名帯表による。
---

## 命題・範囲

全ての \(x\ge y\ge6\)、\(R\ge0\) について、\(H(R;(x,y);15)\) のGrundy値0/1/2を
report.mdの \(T(x,y),P(x,y)\) で完全分類する。低残容量は \(R\le21\) で単一トークン
\(S=x+y\) に一致し、高残容量は \(R\ge S+16\) で \(S\bmod2\) となる。

## 現在の根拠と限界

全称性はy強帰納・各行内d外帰納と、全Rを覆うA/B/C署名帯表による。
y=6のB子はK1049、C子はK1062、y>=7のB子は強帰納仮定、A子はd外帰納仮定。
低Rの \(R\le21\) 単一トークン一致は閉形式からの族固有の系であり、K0832の一般条件
\(R\le z+1=16\) を一般定理として拡張する主張ではない。tailはK0832から従う。
値1基底点はd>=13で \(\{16,18,\ldots,2y+14\}=\{z+1,z+3,\ldots,z+2y-1\}\)
のちょうどy点。値2の前倒し点はd+z≡2 (mod 4)、掃引行はd=16、定常pinは2y+z=2y+15。

z=16・y>=6の基底B子、全高さを統合する2トークン一般式、値1基底点y点仮説の全z一般証明、
前倒し格子の一般証明、標準二次元盤の固定幅・q点版の真の安定化長は未解決。
