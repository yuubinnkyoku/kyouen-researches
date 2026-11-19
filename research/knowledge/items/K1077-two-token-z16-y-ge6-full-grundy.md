---
id: K1077
title: 2トークン残余ゲーム z=16・y>=6一様全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z16 uniform y-ge6 full grundy]
relations:
- type: depends_on
  target: K0832
  note: A/B/C再帰、単一トークン閉形式、一般tailを使用する
- type: depends_on
  target: K1074
  note: y=6基底行のB子をz=16,y=5全x定理で閉じる
- type: depends_on
  target: K1065
  note: 全y>=6行のC子を1 xor (z=15,y>=6一様全Grundy定理)で閉じる
artifacts:
- path: research/experiments/vertical-fiber-two-token-z16-y-ge6-proof-20261120/report.md
  role: proof
  note: y強帰納・行内d外帰納と全R A/B/C署名帯表による全称証明
- path: research/experiments/vertical-fiber-two-token-z16-y-ge6-proof-20261120/verify_z16_y_ge6.py
  role: verifier
  note: 二直接再帰、K1074/K1065子アンカー、署名帯・mex、低R縮約、tailの独立監査
- path: research/experiments/vertical-fiber-two-token-z16-y-ge6-proof-20261120/output/audit.json
  role: data
  note: 1,066,734検査・不一致0・二回実行と別cwdでbyte-identical
- path: research/log/2026-11-20-vertical-fiber-two-token-z16-y-ge6-proof.md
  role: log
  note: 最新mainと単一オーナー宣言の確認、帯表導出の誤り訂正履歴、監査と次の未解決範囲
scope: >-
  κ=1残余ゲームH(R;(x,y);16)の2トークン族における固定高さz=16、
  全x>=y>=6・全R>=0。Grundy値0/1/2を本文と証明報告のT/P式で完全分類する。
evidence: >-
  yに関する強帰納と、各y行内のd=x-y外帰納。y=6のB子はK1074、全行のC子は
  1 xor K1065、y>=7のB子はy帰納仮定、A子はd外帰納仮定で評価する。
  1<=R<=S+17（S=x+y）の全域を縮退セル12行・偶奇別の記号的A/B/C署名帯表で
  一意被覆し、mexを取る。R=0は終局、R>=S+17はK0832一般tailで閉じる。
  独立監査は1,066,734検査・不一致0・二回実行および別cwdでbyte-identical。
  有限監査は証明そのものではなく、全称性は二段帰納と記号的署名帯表による。
---

## 命題・範囲

全ての \(x\ge y\ge6\)、\(R\ge0\) について、\(H(R;(x,y);16)\) のGrundy値0/1/2を
report.mdの \(T(x,y),P(x,y)\) で完全分類する。低残容量は \(R\le22\) で単一トークン
\(S=x+y\) に一致し、高残容量は \(R\ge S+17\) で \(S\bmod2\) となる。

## 現在の根拠と限界

全称性はy強帰納・各行内d外帰納と、全Rを覆うA/B/C署名帯表による。
y=6のB子はK1074、C子はK1065、y>=7のB子は強帰納仮定、A子はd外帰納仮定。
低Rの \(R\le22=z+6\) 単一トークン一致は閉形式からの族固有の系であり、K0832の一般条件
\(R\le z+1=17\) を一般定理として拡張する主張ではない。z=14（K1062）の20、
z=15（K1065）の21と続き、境界 \(R\le z+6\) が3例連続で観測されているが、
一般z版は未証明の観察として区別する。tailはK0832から従う。

偶数zの族構造: 値2ラダーの上端は \(z-1=15\)（奇数zのK1065では上端 \(z\)）。
格子前倒し点は \(d+z\equiv2\pmod4\) の \(d\in\{2,6,10,14\}\) で
\(r=2y+(d+z)/2\)。掃引行は \(d=z+1=17\)、掃引帯 \(O[Y+17,S+16]\)。
定常pinは \(Y+17=2y+z+1\)（奇数zでは \(2y+z\)）。値1基底点は \(d=16\) で
\(O[17,Y+15]=\{z+1,z+3,\ldots,2y+15\}\) のちょうどy点となり、偶数zでは基底点は
奇数行に乗る（K1065の偶数行と対照）。値2は常に奇数Rに現れる。過渡セルは
\((6,0),(6,1),(6,2),(6,3),(6,4),(6,5),(7,0),(7,1),(7,2),(7,3),(8,0),(8,1)\) の12行で、
うち \((6,4),(7,2),(8,0)\) の3行はTのラダーが値1帯を全て覆い値1が出現しない。
署名帯表上、d=18（最初の偶数pin行）のE終帯のみ点でなく \([Y+18,S+16]\) 全域が02である。

z=17・y=5境界切片（z=17,y>=6一様族のB子）、z=18・y=3（B=K1051・C=1 xor K1067）、
全高さを統合する2トークン一般式、値1基底点y点仮説と前倒し格子の全z一般証明、
\(R\le z+6\) 低R縮約の全z一般証明、標準二次元盤の固定幅・q点版の真の安定化長は未解決。
