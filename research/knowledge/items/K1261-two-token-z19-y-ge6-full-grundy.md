---
id: K1261
title: 2トークン残余ゲーム z=19・y>=6 一様族の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z19 y>=6 uniform family full grundy]
relations:
- type: depends_on
  target: K0832
  note: A/B/C再帰、単一トークン閉形式、一般tailを使用する
- type: depends_on
  target: K1260
  note: B子（z=19,y=5）を出版アンカーとして閉じる
- type: depends_on
  target: K1259
  note: C子（z=18,y>=6一様族）を1 xor 出版アンカーとして閉じる
- type: related
  target: K1087
  note: 構造原形（z=17,y>=6一様族）。z=19はそのz+2シフト+偶行U+1一点修正
- type: related
  target: K1098
  note: z=19列のy=3先行項。前倒し活性d=15,19の観測源
artifacts:
- path: research/experiments/vertical-fiber-two-token-z19-y-ge6-proof-20261123/report.md
  role: proof
  note: y強帰納とd外帰納、全R A/B/C署名帯表（TRANSIENT 16行＋S=19対角式＋S>=20の7クラス）による全称証明
- path: research/experiments/vertical-fiber-two-token-z19-y-ge6-proof-20261123/verify_z19_y_ge6.py
  role: verifier
  note: 二直接再帰、K1260/K1259出版子アンカー、署名帯・mex、closure sweep、低R縮約、tail、set-vs-predicate、固定seed散点の独立監査（SMOKE対応）
- path: research/experiments/vertical-fiber-two-token-z19-y-ge6-proof-20261123/output/audit.json
  role: data
  note: 6,712,509検査・不一致0・4回実行（別cwd・別HOME隔離込み）でbyte-identical
- path: research/log/2026-11-23-vertical-fiber-two-token-z19-y-ge6-proof.md
  role: log
  note: 単一オーナー宣言、cand1の41点bad→U+1一点修正の確定、帯表d=0特異の誤り訂正、fail-closed検証、4回監査と次の未解決範囲
scope: >-
  κ=1残余ゲームH(R;(x,y);19)の2トークン族における固定z=19、全x>=y>=6・全R>=0。
  Grundy値0/1/2をreport.mdのT/P閉形式で完全分類する。
evidence: >-
  yに関する外帰納（y=6基底行はB子K1260と(6,6)合流、y>=7のB子はy帰納仮定、
  A子は同一行内のd外帰納仮定、d=0はA==B多重集合合流）。B子はK1260、
  C子は1⊕K1259で評価する。1<=R<=x+y+19の全域をTRANSIENT16行＋対角行式＋
  一般7クラスの記号的署名帯表で一意被覆し、mexを取る。R=0は終局、
  R>=x+y+20=S+z+1はK0832一般tailで閉じる。
  独立監査は6,712,509検査・不一致0・同一cwd2回＋隔離cwd＋別HOMEの4回で
  byte-identical、fail-closedはpin/anchor/sweep/band/lattice/lowRの6変異で
  rc=1を確認。有限監査は証明そのものではなく、全称性は外帰納と記号的署名帯表による。
---

## 命題・範囲

全ての \\(x\\ge y\\ge6\\)、\\(R\\ge0\\) について、\\(H(R;(x,y);19)\\) のGrundy値0/1/2を
report.mdの \\(T,P\\) 閉形式で完全分類する。低残容量 \\(R\\le25=z+6\\) は
単一トークン \\(S=x+y\\) に一致し、高残容量は \\(R\\ge x+y+20=S+z+1\\) で
\\(S\\bmod2\\) となる。

## 現在の根拠と限界

全称性はy外帰納・行内d外帰納と、全Rを覆うA/B/C署名帯表による。B子はK1260、
C子は1⊕K1259の出版検証器をアンカー照合。y=6では二つのトークン減少手が
多重集合 \\((y-1,y)\\) に合流してA=B=K1260の該当行となる。

構造観察: \\(z=19\\) は奇数zで \\(z=17\\) 型（ラダー \\(O[1,z]\\)、pin \\(2y+z\\)、
掃引帯 \\(O[2y+z,S+z]\\)、値1基底 \\(E[z+1,\\cdot]\\)）の \\(z+2\\) シフトだが、
**d≡2 (mod 4) 偶行に一点追加 \\(U+1\\)**（\\(U=2y+9+2\\lfloor d/4\\rfloor\\)、
奇数R、値1）が唯一の構造修正として必要。活性格子点は
\\(d\\equiv3\\pmod4\\)、\\(r=2y+(d+19)/2\\) は全z規則 \\(d+z\\equiv2\\pmod4\\) の
実現で、\\(d=19=d=z\\) 行では格子点がpin \\(2y+z\\) と重合（z=17のd=17と同型）。
対角行 \\(S=19\\) の4行 \\((6,7),(7,5),(8,3),(9,1)\\) の値2上端
25/25/27/27=\\(2y+q_o(z-y)\\) は10実例目の交差一致（K1260のx=14上端23に続き）。
低R縮約 \\(R\\le z+6\\) はz=14..19で6例連続、witness \\((14,6)@R=26\\)
（親0 vs 単一トークン1）はz=17/z=18の\\((12,6)\\) と同じy=6行で破壊高さ
\\(R=z+7\\) は全系共通。tailはK0832から従う。これら交叉観察は一般証明ではなく
観察として区別する。

本項により **\\(z=19\\) 列は全yで確定**（y=1特例、y=2 K1052、y=3 K1098、
y=4 K1100、y=5 K1260、y>=6 本項）し、z=17（K1087）、z=18（K1259）に続き
**3本目の全y完結z** となる。次候補は z>=20 レーン（着手前に単一オーナー宣言必須）。
\\(R\\le z+6\\) 低R縮約の全z一般証明、値1基底点y点仮説と前倒し格子・対角行格子の
全z一般証明、偶行 \\(U+1\\) 追加点の一般z起源、2トークンz横断一般式、
標準二次元盤の固定幅・q点版の真の安定化長（11×11空盤・二石root・S2・
class 1/2/4 は常にUNKNOWN）は未解決のまま。
