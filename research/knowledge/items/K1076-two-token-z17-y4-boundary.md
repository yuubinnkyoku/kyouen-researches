---
id: K1076
title: 2トークン残余ゲーム z=17・y=4境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z17 y4 boundary slice]
relations:
- type: depends_on
  target: K0832
  note: 高さのみ縮約と一般tailを使用する
- type: depends_on
  target: K1067
  note: B子の評価とx=4基底の多重集合合流にz=17・y=3切片を使用する
- type: depends_on
  target: K1064
  note: C子の評価に1 xor (z=16・y=4切片)を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z17-y4-boundary-20261120/report.md
  role: proof
  note: x外帰納と全Rを覆うA/B/C署名帯表による全称証明
- path: research/experiments/vertical-fiber-two-token-z17-y4-boundary-20261120/verify_z17_y4.py
  role: verifier
  note: 二方式の親再帰、署名帯、帰納ステップ閉包、深域帯端点、tailの独立監査
- path: research/experiments/vertical-fiber-two-token-z17-y4-boundary-20261120/output/audit.json
  role: data
  note: 12,693,293照合・不一致0の決定論的監査結果（二作業ディレクトリでbyte-identical）
- path: research/log/2026-11-20-vertical-fiber-two-token-z17-y4-boundary.md
  role: log
  note: 最新main・既存依存定理・未解決範囲の確認、証明・監査・次の着手候補
scope: >-
  κ=1残余ゲームH(R;(x,y);z)の2トークン族における固定高さz=17、y=4、
  全x>=4・全R>=0。Grundy値0/1/2を完全分類する。
evidence: >-
  xに関する外帰納。x=4では二つのトークン減少手が同じ多重集合(3,4)に合流し、
  B子はK1067のx=4行、C子は1 xor K1064のx=4行で閉じる。x>=5では
  A子を帰納仮説、B子をK1067、C子を1 xor K1064で評価する。
  全1<=R<=x+21はreport.mdの静的行x=4..22、例外行x=23、偶奇別一般行
  x>=24のA/B/C署名帯表が互いに素に被覆し、mex表からT/Pが得られる。
  R>=x+22はK0832の一般tailで親値(x+4) mod 2に閉じる。R<=18の高さのみ
  縮約もK0832から従う。独立監査は署名帯6486点、memo直接再帰2961点、
  別の下からの行構成8694点、x<=5000の帰納ステップ閉包掃引12607431点、
  x<=200000の決定論的散点57727点、tail端点9994点、合計12693293照合で
  不一致0。二作業ディレクトリでaudit.jsonがbyte-identical。
---

## 命題・範囲

全ての \(x\ge4\)、\(R\ge0\) について、\(H(R;(x,4);17)\) のGrundy値0/1/2を
report.mdの \(T(x),P(x)\) で完全分類する。低残容量は \(R\le18\) で単一トークン
\(x+4\) へ縮約し、高残容量は \(R\ge x+22\) で \((x+4)\bmod2\) となる。

値2は初期ラダー \(O[1,2\lfloor(x+1)/2\rfloor+3]\)（x=4..12）から
z=17ラダー \(O[1,17]\) へ移る。x=13は \(x+y=z\) 行で \(O[1,21]\)、
x=17に前倒し点23、x=21にpin 25、x=22に掃引帯 \(O[25,43]\) が現れ、
x>=23で \(O[1,17]\cup\{25\}\) に定着する。

値1の基底点はx>=20で
\(\{18,20,22,24\}=\{z+1,z+3,z+5,z+7\}\) のちょうどy点に定着する。
pinは \(25=2y+z\)、掃引行は \(x=z+y+1=22\) である。

## 現在の根拠と限界

全称性はx外帰納と、全Rを互いに素に覆うA/B/C署名帯表による。B子はK1067、
C子はK1064の全称定理であり、低R縮約・一般tailはK0832から従う。
有限監査は証明そのものではない。前倒し格子 \(2y+(d+z)/2\) はx=17で
23を与えるが、同じ合同条件の早い候補x=9・19は値2に現れず、出現条件は未解決。
z=17・y=5は本項とK1074を両子として持つ次の候補。z=16・y>=6一様族は
別レーンの単一オーナー宣言があるため対象外。標準二次元盤の固定幅・q点版
安定化長、値1基底点y点仮説の全z一般証明、前倒し格子の一般証明も未解決。
