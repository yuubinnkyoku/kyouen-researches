---
id: K1262
title: 2トークン残余ゲーム z=20・y>=6 一様族の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z20 y>=6 uniform family full grundy]
relations:
- type: depends_on
  target: K0832
  note: A/B/C再帰、単一トークン閉形式、一般tailを使用する
- type: related
  target: K1259
  note: 構造原形（z=18,y>=6一様族）。z=20はそのz+2シフト（偶数z・非編集）
- type: depends_on
  target: K1126
  note: B子（y=5族・全zパラメトリック）のz=20行を出版アンカーとして閉じる
- type: depends_on
  target: K1261
  note: C子（z=19,y>=6一様族）を1 xor 出版アンカーとして閉じる
- type: related
  target: K1087
  note: 奇数z対照形（z=17）。偶数z型pin 2y+z+1と奇数z型pin 2y+zの対比
artifacts:
- path: research/experiments/vertical-fiber-two-token-z20-y-ge6-proof-20261123/report.md
  role: proof
  note: y強帰納とd外帰納、全R A/B/C署名帯表（TRANSIENT 25行＋S=20対角5行＋S>=21の7クラス）による全称証明
- path: research/experiments/vertical-fiber-two-token-z20-y-ge6-proof-20261123/verify_z20_y_ge6.py
  role: verifier
  note: 二直接再帰、K1126/K1261出版子アンカー、署名帯・mex、closure sweep、低R縮約、tail、set-vs-predicate、固定seed散点の独立監査（SMOKE対応）
- path: research/experiments/vertical-fiber-two-token-z20-y-ge6-proof-20261123/output/audit.json
  role: data
  note: 6,748,689検査・不一致0・4回実行（別cwd・別HOME隔離込み）でbyte-identical
- path: research/log/2026-11-23-vertical-fiber-two-token-z20-y-ge6-proof.md
  role: log
  note: 単一オーナー宣言、非編集z+2シフトの確定、S=21例外クラスとd=z特異形の分離、fail-closed検証、4回監査と次の未解決範囲
scope: >-
  κ=1残余ゲームH(R;(x,y);20)の2トークン族における固定z=20、全x>=y>=6・全R>=0。
  Grundy値0/1/2をreport.mdのT/P閉形式で完全分類する。
evidence: >-
  yに関する外帰納（y=6基底行はB子K1126 z=20行と(6,6)合流、y>=7のB子はy帰納仮定、
  A子は同一行内のd外帰納仮定、d=0はA==B多重集合合流）。B子はK1126、
  C子は1⊕K1261で評価する。1<=R<=x+y+20の全域をTRANSIENT25行＋対角行式＋
  一般7クラスの記号的署名帯表で一意被覆し、mexを取る。R=0は終局、
  R>=x+y+21=S+z+1はK0832一般tailで閉じる。
  独立監査は6,748,689検査・不一致0・同一cwd2回＋隔離cwd＋別HOMEの4回で
  byte-identical、fail-closedはpin/anchorB/sweep/band/lattice/lowr/a1/tailの8変異で
  rc=1を確認。有限監査は証明そのものではなく、全称性は外帰納と記号的署名帯表による。
---

## 命題・範囲

全ての \\(x\\ge y\\ge6\\)、\\(R\\ge0\\) について、\\(H(R;(x,y);20)\\) のGrundy値0/1/2を
report.mdの \\(T,P\\) 閉形式で完全分類する。低残容量 \\(R\\le26=z+6\\) は
単一トークン \\(S=x+y\\) に一致し、高残容量は \\(R\\ge x+y+21=S+z+1\\) で
\\(S\\bmod2\\) となる。

## 現在の根拠と限界

全称性はy外帰納・行内d外帰納と、全Rを覆うA/B/C署名帯表による。B子はK1126
（y=5族全zパラメトリック閉形式のz=20行）、C子は1⊕K1261の出版検証器を
アンカー照合。y=6では二つのトークン減少手が多重集合 \\((y-1,y)\\) に合流して
A=B=K1126の該当行となる。

構造観察: \\(z=20\\) は偶数zで \\(z=18\\) 型（ラダー \\(O[1,z-1]\\)、pin \\(2y+z+1\\)、
掃引帯 \\(O[2y+z+1,S+z]\\)、値1基底 \\(O[z+1,\\cdot]\\)）の **\\(z+2\\) シフトそのもので
追加編集不要**。活性格子点は \\(d\\equiv2\\pmod4\\)、\\(r=2y+(d+20)/2\\) は全z規則
\\(d+z\\equiv2\\pmod4\\) の実現で、偶数zでは偶行 \\(d\\equiv0\\pmod4\\) の候補位置が
偶数Rに落ち値1帯に吸収されるため、奇数z（z=19）で必要だった \\(U+1\\) 一点追加が
消える。これで偶数z型が \\(z=16,18,20\\) で3例連続し、偶数z非編集・奇数z一点追加の
構造則が確定した。\\(d=z=20\\) 行のE終帯 '123' 特異形はz=18の\\(d=18\\)・z=16の
\\(d=17\\) と同型、掃引行 \\(d=z+1=21\\) の帯下端はちょうどpin位置。
対角行 \\(S=20\\) の5行 \\((6,8),(7,6),(8,4),(9,2),(10,0)\\) の値2上端
25/27/27/29/29=\\(2y+q_o(z-y)\\) は交差一致の15実例目で、Pは全Rで空
（偶数z対角型、z=18と同型）。低R縮約 \\(R\\le z+6\\) はz=14..20で7例連続、
witness \\((16,6)@R=27\\)（親2 vs 単一トークン1）は値2側に破れる初例で、
破壊高さ \\(R=z+7\\) は全系共通。tailはK0832から従う。これら交叉観察は
一般証明ではなく観察として区別する。

本項により **\\(z=20\\) 列は全yで確定**（y=1..5 はK1126の全zパラメトリック閉形式の
z=20行、y>=6 本項）し、z=17（K1087）、z=18（K1259）、z=19（K1261）に続き
**4本目の全y完結z** となる。次候補は z=21 レーン（着手前に単一オーナー宣言必須）。
\\(R\\le z+6\\) 低R縮約の全z一般証明、偶数z/奇数zの非編集・一点追加則の全z一般証明、
値1基底点y点仮説と前倒し格子・対角行格子の全z一般証明、2トークンz横断一般式、
標準二次元盤の固定幅・q点版の真の安定化長（11×11空盤・二石root・S2・
class 1/2/4 は常にUNKNOWN）は未解決のまま。
