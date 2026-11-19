---
id: K1061
title: 2トークン残余ゲーム z=13・y>=6一様全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z13 uniform y-ge6 full grundy]
relations:
- type: depends_on
  target: K0832
  note: A/B/C再帰、Theorem T、高さのみ縮約、一般tailを使用する
- type: depends_on
  target: K1045
  note: y=6基底行のB子をz=13,y=5全x定理で閉じる
- type: depends_on
  target: K1056
  note: 全y>=6行のC子をz=12一様全Grundy定理で閉じる
artifacts:
- path: research/experiments/vertical-fiber-two-token-z13-y-ge6-proof-20261120/report.md
  role: proof
  note: y強帰納・行内x外帰納と全R A/B/C署名帯表による全称証明
- path: research/experiments/vertical-fiber-two-token-z13-y-ge6-proof-20261120/candidate.py
  role: verifier
  note: T/P閉形式、K1045/K1056子アンカー転写、二つの直接mex再帰、single_token
- path: research/experiments/vertical-fiber-two-token-z13-y-ge6-proof-20261120/bands.py
  role: verifier
  note: (y,d)クラス別の奇偶署名帯表の正本実装
- path: research/experiments/vertical-fiber-two-token-z13-y-ge6-proof-20261120/band_derive.py
  role: verifier
  note: K1045/K1056と帰納候補からA/B/C子署名を独立導出
- path: research/experiments/vertical-fiber-two-token-z13-y-ge6-proof-20261120/verify_z13_y_ge6_proof.py
  role: verifier
  note: 二直接再帰、子アンカー、署名帯・mex、低R縮約、tailの独立監査
- path: research/experiments/vertical-fiber-two-token-z13-y-ge6-proof-20261120/output/audit.json
  role: data
  note: 1,835,629検査・不一致0・2回および別cwd byte-identical
- path: research/log/2026-11-20-vertical-fiber-two-token-z13-y-ge6-proof.md
  role: log
  note: 重複確認、式の導出、縮退セル4つ、監査と次の未解決範囲
scope: >-
  κ=1残余ゲームH(R;(x,y);13)の2トークン族における固定高さz=13、
  全x>=y>=6・全R>=0。Grundy値0/1/2を本文と証明報告のT/P式で完全分類する。
evidence: >-
  yに関する強帰納と、各y行内のx外帰納。y=6のB子はK1045、全行のC子は
  1 xor K1056、y>=7のB子はy帰納仮定、A子はx帰納仮定で評価する。
  1<=R<=S+13（S=x+y）の全域をd=x-y別・parity別のA/B/C署名帯表で一意被覆し
  （coverage smoke 573,319行・bad=0）、mexを取る。R=0は終局、
  R>=S+14はK0832一般tailで閉じる。独立監査は1,835,629検査・不一致0・
  2回実行および別cwdでbyte-identical。有限監査は証明そのものではなく、
  全称性は二段帰納と記号的署名帯表による。
---

## 命題・範囲

全ての \(x\ge y\ge6\)、\(R\ge0\) について、\(H(R;(x,y);13)\) のGrundy値0/1/2を
実験報告の \(T(x,y),P(x,y)\) で完全分類する。低残容量は \(R\le19\) で高さのみ
縮約で単一トークン \(S=x+y\) に一致し、高残容量は \(R\ge S+14\) で \(S\bmod2\)
となる。

## 現在の根拠と限界

全称性はy強帰納・各行内x外帰納と、全Rを覆うA/B/C署名帯表による。
y=6のB子はK1045、C子はK1056で、y>=7のB子は強帰納仮定、A子はx外帰納仮定。
署名帯のmexは本文のT/Pと一致し、K0832のTheorem Tの偶奇上界も満たす。
縮退セルは(y,d)=(6,0),(6,1),(6,2),(7,0)の4つで、y=5基底行K1045の過渡が
署名レベルで残る。

有限監査は二直接再帰・子アンカー・署名帯・mex・縮約・tailの転写照合であり、
証明の代わりではない。z=13のy=1..5は個別切片定理（y=5はK1045）の範囲である。
z=14以上のy>=6一様族、全高さを統合する2トークン一般式、値1基底点y点仮説の
全z一般証明、標準二次元盤の固定幅・q点版の真の安定化長は未解決。
