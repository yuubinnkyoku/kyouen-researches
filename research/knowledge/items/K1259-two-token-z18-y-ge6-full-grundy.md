---
id: K1259
title: 2トークン残余ゲーム z=18・y>=6一様全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z18 uniform y-ge6 full grundy]
relations:
- type: depends_on
  target: K0832
  note: A/B/C再帰、単一トークン閉形式、一般tailを使用する
- type: depends_on
  target: K1092
  note: y=6基底行のB子をz=18,y=5全x定理で閉じる
- type: depends_on
  target: K1087
  note: 全y>=6行のC子を1 xor (z=17,y>=6一様全Grundy定理)で閉じる
- type: related
  target: K1127
  note: z=18,y=6行はK1127のy=6族allz全称証明が先行到達済み
- type: related
  target: K1131
  note: z=18,y=7行はK1131のy=7族allz全称証明が先行到達済み
- type: related
  target: K1135
  note: z=18,y=8行はK1135のy=8族allz全称証明が先行到達済み
- type: related
  target: K1138
  note: z=18,y=9行はK1138のy=9族allz全称証明が先行到達済み
- type: related
  target: K1141
  note: z=18,y=10行はK1141のy=10族allz全称証明が先行到達済み
- type: related
  target: K1257
  note: z=18,y=6..22行のy族allz全称証明（K1127..K1257）が先行到達済み。本項の新規内容はy>=23無限行とz=18列の統一パラメトリック閉形式
artifacts:
- path: research/experiments/vertical-fiber-two-token-z18-y-ge6-proof-20261123/report.md
  role: proof
  note: y強帰納・行内d外帰納と全R A/B/C署名帯表（過渡16行込み）による全称証明
- path: research/experiments/vertical-fiber-two-token-z18-y-ge6-proof-20261123/verify_z18_y_ge6.py
  role: verifier
  note: 二直接再帰、K1092/K1087子アンカー、署名帯・mex、直接クロージャ掃引、低R縮約、tailの独立監査
- path: research/experiments/vertical-fiber-two-token-z18-y-ge6-proof-20261123/output/audit.json
  role: data
  note: 6,676,142検査・不一致0・4回実行（別cwd・別HOME隔離込み）でbyte-identical
- path: research/log/2026-11-23-vertical-fiber-two-token-z18-y-ge6-proof.md
  role: log
  note: 単一オーナー宣言、帯表導出の誤り訂正履歴、環境リセット再build、4回監査と次の未解決範囲
scope: >-
  κ=1残余ゲームH(R;(x,y);18)の2トークン族における固定高さz=18、
  全x>=y>=6・全R>=0。Grundy値0/1/2を本文と証明報告のT/P式で完全分類する。
evidence: >-
  yに関する強帰納と、各y行内のd=x-y外帰納。y=6のB子はK1092、全行のC子は
  1 xor K1087、y>=7のB子はy帰納仮定、A子はd外帰納仮定で評価する。
  1<=R<=S+18（S=x+y）の全域を過渡16行・S=18の4対角行込みの偶奇別記号的
  A/B/C署名帯表で一意被覆し、mexを取る。R=0は終局、R>=S+19はK0832一般tailで閉じる。
  独立監査は6,676,142検査・不一致0・同一cwd2回＋別cwd隔離＋別HOME隔離の4回でbyte-identical。
  有限監査は証明そのものではなく、全称性は二段帰納と記号的署名帯表による。
---

## 命題・範囲

全ての \(x\ge y\ge6\)、\(R\ge0\) について、\(H(R;(x,y);18)\) のGrundy値0/1/2を
report.mdの \(T(x,y),P(x,y)\) で完全分類する。低残容量は \(R\le24\) で単一トークン
\(S=x+y\) に一致し、高残容量は \(R\ge S+19=S+z+1\) で \(S\bmod2\) となる。

## 現在の根拠と限界

全称性はy強帰納・各行内d外帰納と、全Rを覆うA/B/C署名帯表による。
y=6のB子はK1092、C子はK1087、y>=7のB子は強帰納仮定、A子はd外帰納仮定。
低Rの \(R\le24=z+6\) 単一トークン一致は閉形式からの族固有の系であり、K0832の一般条件
\(R\le z+1=19\) を一般定理として拡張する主張ではない。z=14（K1062）の20、
z=15（K1065）の21、z=16（K1077）の22、z=17（K1087）の23に続き、境界
\(R\le z+6\) が5例連続で観測されたが、一般z版は未証明の観察として区別する。
witnessは \((12,6)\)、破壊高さ \(R=z+7\) でz=17の \((12,6)\)@24と同型。
tailはK0832から従う。

偶数z=18の族構造: 値2ラダーの上端は \(z-1=17\)（z=16と同じ偶数z型）。
値2は常に奇数Rの出現で、\(d+z\equiv2\pmod4\) の前倒し格子点は
\(d\in\{0,4,8,12,16\}\) の \(r=2y+(d+z)/2=2y+9,2y+11,2y+13,2y+15,2y+17\)
（z=16では \(d\in\{2,6,10,14\}\)。d=0行が新規に加わる）。pinは
\(2y+z+1\) でd>=20の全行に \(T=\{Y+19\}\) として現れる。掃引行は
\(d=z+1=19\)、掃引帯は \(O[2y+z+1,S+z]\)（下端がちょうどpin位置）。
値1基底帯は奇ラダー \(O[19,A_1]\)、\(A_1=Y+7+2\lfloor(d+2)/4\rfloor\)（d<=18）
で、z=16/z=17の偶数E基底帯から反転する（C子 \(1\oplus\)z=17値 の伝播）。
奇数d<=17行のPは \(O[19,A_1]\cup I[A_1+2,\infty)\) の単一ギャップ型で、
行高域がほぼ稠密に値1になる（z=16/17にない新構造）。過渡セルは
2y+d<=18 の16行（ \(S<z+1\) しきい値はzに依らない。S=18の4対角行
\((6,6),(7,4),(8,2),(9,0)\) では値2ラダーが23/25/25/27まで伸び、
値1は全Rで出現しない。S=19の4行は初期帯コード '12' の例外クラス）。

これにより \(z=18\) は y=1（K1023）、y=2（K1051）、y=3（K1078）、y=4（K1083）、
y=5（K1092）、y>=6（本項）がすべて閉じ、z=17に続き2本目の全y完結zとなった。
y=6..22行はy族allz全称証明（K1127..K1257）が先行到達済みであり、本項の新規内容は
y>=23の無限行の分類と、z=18列を単一のパラメトリック閉形式で束ねた点である。

z=19,y=5境界切片（B=K1100・C=1 xor K1092で全子が出版済み、即着手可・着手前に
単一オーナー宣言）、z=19・y>=6一様族（B=z19y5切片・C=1 xor 本項）、
全高さを統合する2トークン一般式、値1基底点y点仮説と前倒し格子の全z一般証明、
\(R\le z+6\) 低R縮約の全z一般証明、標準二次元盤の固定幅・q点版の真の安定化長は
未解決。
