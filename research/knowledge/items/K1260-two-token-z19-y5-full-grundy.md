---
id: K1260
title: 2トークン残余ゲーム z=19・y=5境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z19 y5 boundary slice full grundy]
relations:
- type: depends_on
  target: K0832
  note: A/B/C再帰、単一トークン閉形式、一般tailを使用する
- type: depends_on
  target: K1100
  note: B子（z=19,y=4）を出版アンカーとして閉じる
- type: depends_on
  target: K1092
  note: C子（z=18,y=5）を1 xor 出版アンカーとして閉じる
- type: related
  target: K1259
  note: C子の1段上の族（z=18,y>=6一様）。z=19,y>=6一様族では本項のB子が1 xor K1259のC子と対になる
- type: related
  target: K1098
  note: z=19列のy=3先行項。前倒し活性d=15,19の観測源
artifacts:
- path: research/experiments/vertical-fiber-two-token-z19-y5-proof-20261123/report.md
  role: proof
  note: x外帰納と全R A/C署名帯表（静的行x=5..25＋アフィン帯）による全称証明
- path: research/experiments/vertical-fiber-two-token-z19-y5-proof-20261123/verify_z19_y5.py
  role: verifier
  note: 二直接再帰、K1100/K1092出版子アンカー、署名帯・mex、closure sweep、低R縮約、tailの独立監査（SMOKE対応）
- path: research/experiments/vertical-fiber-two-token-z19-y5-proof-20261123/output/audit.json
  role: data
  note: 975,680検査・不一致0・4回実行（別cwd・別HOME隔離込み）でbyte-identical
- path: research/log/2026-11-23-vertical-fiber-two-token-z19-y5-proof.md
  role: log
  note: 単一オーナー宣言、転写等価確認、帯表導出の誤り訂正履歴、fail-closed検証、4回監査と次の未解決範囲
scope: >-
  κ=1残余ゲームH(R;(x,5);19)の2トークン族における固定z=19、全x>=5・全R>=0。
  Grundy値0/1/2をreport.mdのT/P閉形式で完全分類する。
evidence: >-
  xに関する外帰納（x=5基底行はB子K1100と(4,5)合流、x>=6のA子は帰納仮定）。
  B子はK1100、C子は1⊕K1092で評価する。1<=R<=x+24（S=x+5）の全域を
  静的行x=5..25偶奇別＋x>=26アフィン帯の記号的署名帯表で一意被覆し、mexを取る。
  R=0は終局、R>=x+25=S+z+1はK0832一般tailで閉じる。
  独立監査は975,680検査・不一致0・同一cwd2回＋隔離cwd＋別HOMEの4回でbyte-identical、
  fail-closedはpin/anchor/sweep/bandの4変異でrc=1を確認。
  有限監査は証明そのものではなく、全称性は外帰納と記号的署名帯表による。
---

## 命題・範囲

全ての \\(x\\ge5\\)、\\(R\\ge0\\) について、\\(H(R;(x,5);19)\\) のGrundy値0/1/2を
report.mdの \\(T_x,P_x\\) 閉形式で完全分類する。低残容量 \\(R\\le28\\)（x>=24行）は
単一トークンに一致し、高残容量は \\(R\\ge x+25=S+z+1\\) で \\(S\\bmod2\\) となる。

## 現在の根拠と限界

全称性はx外帰納と、全Rを覆うA/B/C署名帯表による。B子はK1100、C子は1⊕K1092の
出版検証器をアンカー照合。x=5では二つのトークン減少手が多重集合 \\((4,5)\\) に
合流してA=B=K1100のx=5行となる。

構造観察: 対角行 \\(x=14\\)（\\(S=19=z\\)）の値2上端は \\(2y+q_o(z-y)=23\\)
（9実例目の交差一致）。前倒し単点は \\(x=16,20,24\\)（点25・27・29、
\\(d\\in\\{11,15,19\\}\\)、\\(d+z\\equiv2\\pmod4\\)）で、\\(d=11=z-8\\) の活性化は
y=5で初観測（y=3,4では \\(d\\in\\{15,19\\}\\)）。\\(x=24\\) の前倒し点 \\(29=2y+z\\)
は \\(x=z+y\\) 行のpinそのもの。掃引行は \\(x=25=z+y+1\\)、掃引帯は
\\(O[29,49]=O[2y+z,S+z]\\)、定常pin 29は \\(x\\ge26\\)。値1基底点は
\\(\\{20,22,24,26,28\\}\\)ちょうどy=5点で、y点仮説が同一z=19で
\\(y=2,3,4,5\\) の4連続確認。\\(x\\le13\\)（\\(S<z\\)）は高さのみ縮約（4実例目）、
\\(x\\ge24=z+y\\) で最初の不一致は \\(R=29=2y+z\\)（5実例目・開始行 \\(x=z+y\\)）。
tailはK0832から従う。これら交叉観察は一般証明ではなく観察として区別する。

本項により \\(z=19\\) 列は y=2（K1052）、y=3（K1098）、y=4（K1100）、
y=5（本項）まで確定し、次候補は
z=19,y>=6 一様族（B子=本項・C子=1⊕K1259。着手前に単一オーナー宣言必須）である。
\\(R\\le z+6\\) 低R縮約の全z一般証明、値1基底点y点仮説と前倒し格子の全z一般証明、
2トークンz横断一般式、標準二次元盤の固定幅・q点版の真の安定化長（11×11空盤・
二石root・S2・class 1/2/4は常にUNKNOWN）は未解決のまま。
