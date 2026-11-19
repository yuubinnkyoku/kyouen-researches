---
id: K1010
title: 2トークン残余ゲーム z=10・y=8境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z10 y8 boundary slice]
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームHの再帰、Theorem T、単一トークン全z公式、高さのみ縮約、一般tailを使用する
- type: depends_on
  target: K1009
  note: B子の評価にz=10,y=7境界切片を使用する
- type: depends_on
  target: K0998
  note: C子の評価にz=9,y=8境界切片を使用する
- type: supports
  target: K1002
  note: z=10,y>=6一様候補のy=8切片を全称証明する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z10-y8-boundary-20261119/report.md
  role: proof
  note: 全x>=8・全R>=0のGrundy値0/1/2をx外帰納とA/B/C署名帯表で分類する証明
- path: research/experiments/vertical-fiber-two-token-z10-y8-boundary-20261119/verify_z10_y8.py
  role: verifier
  note: 二方式の直接mex再帰、K1009/K0998アンカー、署名帯・mex・tail・Theorem T・K1002整合を監査する検証器
- path: research/experiments/vertical-fiber-two-token-z10-y8-boundary-20261119/output/audit.json
  role: data
  note: 10,261,399検査・不一致0・二回実行byte-identical
- path: research/log/2026-11-19-vertical-fiber-two-token-z10-y8-boundary.md
  role: log
  note: y=8三子の接続、x外帰納証明、独立監査、K1002の残る範囲
scope: >-
  κ=1残余ゲームH(R;(x,y);z)の2トークン族における固定高さz=10、y=8、
  全x>=8・全R>=0。Grundy値0/1/2を完全分類する。
evidence: >-
  xに関する外帰納。x=8では二つのトークン減少手が同一の(8,7);10子に合流する。
  x>=9ではA子を帰納仮説、B子をK1009のz=10,y=7公式、C子をK0998のz=9,y=8公式
  で評価する。x=8..20の移行行とx>=21の定常署名帯で1<=R<=x+18を完全被覆し、
  各署名のmexが本文のT/P式を与える。R>=x+19はK0832の一般tail
  H=(x+8) mod 2で閉じる。独立監査は10,261,399検査・不一致0・二回実行byte-identical。
  有限監査は証明の代替ではなく、全称性はx外帰納と署名帯表による。
---

## 定理

d=x-8、S=x+8 とする。O[a,b] は区間内の奇数、E[a,b] は偶数である。

\[
T_{10}^{(8)}(x)=\{1,3,5,7,9\}\cup
\begin{cases}
\{21+d/2\},&d\in\{0,4,8\},\\
O[27,S+10],&d=11,\\
\{27\},&d\ge12,\\
\varnothing,&\text{otherwise}.
\end{cases}
\]

値1位置Pは次の4区分である。

- d偶数・0<=d<=10: O[11,19+2 ceil(d/4)]
- d偶数・d>=12: O[11,25] ∪ E[28,S+10]
- d奇数・1<=d<=9: O[11,S+10] ∪ E[22+2 floor((d+1)/4),S+9]
- d奇数・d>=11: O[11,25] ∪ E[28,S+9]

tailはR>=S+11=x+19でH=S mod 2。R=0は0、それ以外はTなら2、Pなら1、残りは0。

## 現在の根拠と限界

A/B/Cのx外帰納と全域署名帯表による全称証明である。K1002のy=8候補と一致するが、y>=9の一様中間帯は未証明なのでK1002全体をprovedへ変更しない。標準二次元盤の固定幅安定化長への転送も未証明。
