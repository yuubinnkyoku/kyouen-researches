---
id: K1056
title: 2トークン残余ゲーム z=12・y>=6一様全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z12 uniform y-ge6 full grundy]
relations:
- type: depends_on
  target: K0832
  note: A/B/C再帰、Theorem T、高さのみ縮約、一般tailを使用する
- type: depends_on
  target: K1043
  note: y=6基底行のB子をz=12,y=5全x定理で閉じる
- type: depends_on
  target: K1055
  note: 全y>=6行のC子をz=11一様全Grundy定理で閉じる
artifacts:
- path: research/experiments/vertical-fiber-two-token-z12-y-ge6-proof-20261120/report.md
  role: proof
  note: y強帰納・行内x外帰納と全R A/B/C署名帯表による全称証明
- path: research/experiments/vertical-fiber-two-token-z12-y-ge6-proof-20261120/candidate.py
  role: verifier
  note: T/P閉形式、K1043/K1055子アンカー転写、二つの直接mex再帰
- path: research/experiments/vertical-fiber-two-token-z12-y-ge6-proof-20261120/bands.py
  role: verifier
  note: (y,d)クラス別の奇偶署名帯表の正本実装
- path: research/experiments/vertical-fiber-two-token-z12-y-ge6-proof-20261120/band_derive.py
  role: verifier
  note: K1043/K1055と帰納候補からA/B/C子署名を独立導出
- path: research/experiments/vertical-fiber-two-token-z12-y-ge6-proof-20261120/verify_z12_y_ge6_proof.py
  role: verifier
  note: 二直接再帰、子アンカー、署名帯・mex、低R縮約、tailの独立監査
- path: research/experiments/vertical-fiber-two-token-z12-y-ge6-proof-20261120/output/audit.json
  role: data
  note: 2,892,040検査・不一致0・2回および別cwd byte-identical
- path: research/log/2026-11-20-vertical-fiber-two-token-z12-y-ge6-proof.md
  role: log
  note: 重複確認、式の導出、例外セル、監査と次の未解決範囲
scope: >-
  κ=1残余ゲームH(R;(x,y);12)の2トークン族における固定高さz=12、
  全x>=y>=6・全R>=0。Grundy値0/1/2を本文と証明報告のT/P式で完全分類する。
evidence: >-
  yに関する強帰納と、各y行内のx外帰納。y=6のB子はK1043、全行のC子は
  1 xor K1055、y>=7のB子はy帰納仮定、A子はx帰納仮定で評価する。
  1<=R<=S+12（S=x+y）の全域をd=x-y別・parity別のA/B/C署名帯表で一意被覆し、
  mexを取る。R=0は終局、R>=S+13はK0832一般tailで閉じる。独立監査は
  2,892,040検査・不一致0・2回実行byte-identical。有限監査は証明そのものではなく、
  全称性は二段帰納と記号的署名帯表による。
---

## 命題・範囲

全ての \(x\ge y\ge6\)、\(R\ge0\) について、\(H(R;(x,y);12)\) のGrundy値0/1/2を
実験報告の \(T(x,y),P(x,y)\) で完全分類する。低残容量は \(R\le13\) で単一トークン
\(S=x+y\) へ縮約し、高残容量は \(R\ge S+13\) で \(S\bmod2\) となる。

## 現在の根拠と限界

全称性はy強帰納・各行内x外帰納と、全Rを覆うA/B/C署名帯表による。
y=6のB子はK1043、C子はK1055で、y>=7のB子は強帰納仮定、A子はx外帰納仮定。
署名帯のmexは本文のT/Pと一致し、K0832のTheorem Tの偶奇上界も満たす。

有限監査は二直接再帰・子アンカー・署名帯・mex・縮約・tailの転写照合であり、
証明の代わりではない。z=12のy=1..5は個別切片定理の範囲である。
z=13以上のy>=6一様族、全高さを統合する2トークン一般式、y点基底の全z一般証明、
標準二次元盤の固定幅・q点版の真の安定化長は未解決。
