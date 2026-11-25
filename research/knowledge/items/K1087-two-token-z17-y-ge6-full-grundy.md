---
id: K1087
title: 2トークン残余ゲーム z=17・y>=6一様全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z17 uniform y-ge6 full grundy]
relations:
- type: depends_on
  target: K0832
  note: A/B/C再帰、単一トークン閉形式、一般tailを使用する
- type: depends_on
  target: K1080
  note: y=6基底行のB子をz=17,y=5全x定理で閉じる
- type: depends_on
  target: K1077
  note: 全y>=6行のC子を1 xor (z=16,y>=6一様全Grundy定理)で閉じる
artifacts:
- path: research/experiments/vertical-fiber-two-token-z17-y-ge6-proof-20261120/report.md
  role: proof
  note: y強帰納・行内d外帰納と全R A/B/C署名帯表による全称証明
- path: research/experiments/vertical-fiber-two-token-z17-y-ge6-proof-20261120/verify_z17_y_ge6.py
  role: verifier
  note: 二直接再帰、K1080/K1077子アンカー、署名帯・mex、直接クロージャ掃引、低R縮約、tailの独立監査
- path: research/experiments/vertical-fiber-two-token-z17-y-ge6-proof-20261120/output/audit.json
  role: data
  note: 6,641,445検査・不一致0・二回実行と別cwdでbyte-identical
- path: research/log/2026-11-20-vertical-fiber-two-token-z17-y-ge6-proof.md
  role: log
  note: 最新mainと単一オーナー宣言の確認、帯表導出の誤り訂正履歴、監査と次の未解決範囲
scope: >-
  κ=1残余ゲームH(R;(x,y);17)の2トークン族における固定高さz=17、
  全x>=y>=6・全R>=0。Grundy値0/1/2を本文と証明報告のT/P式で完全分類する。
evidence: >-
  yに関する強帰納と、各y行内のd=x-y外帰納。y=6のB子はK1080、全行のC子は
  1 xor K1077、y>=7のB子はy帰納仮定、A子はd外帰納仮定で評価する。
  1<=R<=S+17（S=x+y）の全域を縮退セル12行・S=17の3対角行込みの偶奇別記号的
  A/B/C署名帯表で一意被覆し、mexを取る。R=0は終局、R>=S+18はK0832一般tailで閉じる。
  独立監査は6,641,445検査・不一致0・二回実行および別cwdでbyte-identical。
  有限監査は証明そのものではなく、全称性は二段帰納と記号的署名帯表による。
---

## 命題・範囲

全ての \(x\ge y\ge6\)、\(R\ge0\) について、\(H(R;(x,y);17)\) のGrundy値0/1/2を
report.mdの \(T(x,y),P(x,y)\) で完全分類する。低残容量は \(R\le23\) で単一トークン
\(S=x+y\) に一致し、高残容量は \(R\ge S+18\) で \(S\bmod2\) となる。

## 現在の根拠と限界

全称性はy強帰納・各行内d外帰納と、全Rを覆うA/B/C署名帯表による。
y=6のB子はK1080、C子はK1077、y>=7のB子は強帰納仮定、A子はd外帰納仮定。
低Rの \(R\le23=z+6\) 単一トークン一致は閉形式からの族固有の系であり、K0832の一般条件
\(R\le z+1=18\) を一般定理として拡張する主張ではない。z=14（K1062）の20、
z=15（K1065）の21、z=16（K1077）の22に続き、境界 \(R\le z+6\) が4例連続で観測されたが、
一般z版は未証明の観察として区別する。tailはK0832から従う。

奇数z=17の族構造: 値2ラダーの上端は \(z\)（偶数z=16では \(z-1\)）。
値2は常に奇数Rの出現で、\(d+z\equiv2\pmod4\) の前倒し格子点は
\(d\in\{1,5,9,13\}\) の \(r=2y+(d+z)/2=2y+9,2y+11,2y+13,2y+15\)
（z=16では \(d\in\{2,6,10,14\}\) に同じr集合）。格子式を d=17 まで延長すると
\(r=2y+17\) となり、奇数zのpin位置 \(2y+z\) に一致する。pinは d=17 と
d>=19 の両クラスに現れる。掃引行は \(d=z+1=18\)、掃引帯は
\(O[2y+z,S+z]\)（z=16では \(O[2y+z+1,S+z]\)）。値1基底帯は
\(E[18,2y+16]=\{z+1,z+2,\ldots,2y+z-1\}\) のちょうどy点で、d=18 と d>=19 の
両クラス（z=16では奇ラダー O[17,Y+15] が該当）に現れる。d>=19 ではさらに奇ラダー
\(O[2y+19,S+17]\) が上に乗り、値1は偶奇両方のRに出る。過渡セルは
\((6,0),(6,1),(6,2),(6,3),(6,4),(6,5),(7,0),(7,1),(7,2),(7,3),(8,0),(8,1)\) の12行で
z=16と同一の (y,d) 集合（しきい値 2y+d<=17 がzに依らない）。うち S 偶数の
\((6,0),(6,2),(6,4),(7,0),(7,2),(8,0)\) の6行は値1が一度も出現しない。
S=17 の3対角行 \((6,5),(7,3),(8,1)\) では値2ラダーが 23/23/25 まで伸びる。
署名帯表上、d>=19 のE終帯は d=19 のみ '12'（子集合 \{1,2\}）、他は '1'、
mexはいずれも0で子値集合の相違として記録される。

これにより \(z=17\) は y=3（K1067）、y=4（K1076・K1079）、y=5（K1080）、
y>=6（本項）がすべて閉じ、y>=1（K1023 全y>=1）と併せ全yで分類済みになった。

z=18・y=5境界切片（B=K1083・C=1 xor K1080で全子が出版済み、即着手可）、
z=18・y>=6一様族（B=z18-y5切片・C=1 xor K1087）、全高さを統合する2トークン一般式、
値1基底点y点仮説と前倒し格子の全z一般証明、\(R\le z+6\) 低R縮約の全z一般証明、
標準二次元盤の固定幅・q点版の真の安定化長は未解決。
