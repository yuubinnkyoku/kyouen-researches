---
id: K0987
title: 2トークン残余ゲーム z=8・y=4境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z8 y4 boundary slice]
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームの再帰、Theorem T、高さのみ縮約、高R tailを使用する
- type: depends_on
  target: K0986
  note: B子の評価にz=8,y=3境界切片を使用する
- type: depends_on
  target: K0980
  note: C子の評価にz=7,y=4境界切片を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z8-y4-boundary-20261119/report.md
  role: proof
  note: x外帰納と全xを覆うA/B/C署名帯表による全称証明
- path: research/experiments/vertical-fiber-two-token-z8-y4-boundary-20261119/verify_z8_y4.py
  role: verifier
  note: 順序付き・正準化直接mex再帰、K0986/K0980アンカー、署名帯・mex・tail・Theorem T・高さ縮約を独立監査する検証器
- path: research/experiments/vertical-fiber-two-token-z8-y4-boundary-20261119/output/audit.json
  role: data
  note: 8,175,427検査・不一致0・独立プロセス二回の監査JSON byte-identical
- path: research/log/2026-11-19-vertical-fiber-two-token-z8-y4-boundary.md
  role: log
  note: 最新mainとの照合、z=8,y=4切片の選定・外帰納証明・独立監査・限界
date: 2026-11-19
scope: >-
  κ=1残余ゲームH(R;(x,y);z)の2トークン族における固定高さz=8、境界y=4、全x>=4・全R>=0。Grundy値0/1/2を完全分類する。
evidence: >-
  x外帰納。x=4では二つのトークン減少手が同一の(4,3)子へ合流し、x>=5ではA子が帰納仮説、B子がK0986のz=8,y=3公式、C子がK0980のz=7,y=4公式で評価される。1<=R<=x+12を全て覆う署名帯表とK0832 Theorem Tのmex制約で分類し、R>=x+13は一般高R tailで閉じる。独立監査は8,175,427検査・不一致0・独立プロセス二回byte-identical。有限監査は証明の代わりではなく、全称性はx外帰納と署名帯表による。
---

## 定理

O[a,b]・E[a,b]は区間内の奇数・偶数、I[a,∞)はa以上の全整数とする。値2位置T、値1位置Pは対応するproof artifactに全式を記載した。全x>=4・R>=0で
\[
H(R;(x,4);8)=
\begin{cases}
2,&R\in T_8^{(4)}(x),\\
1,&R\in P_8^{(4)}(x),\\
0,&\text{otherwise}.
\end{cases}
\]
が成立する。

tailは
\[
R\ge x+13\implies H(R;(x,4);8)=(x+4)\bmod2.
\]

## 現在の根拠と限界

全称性はx外帰納と、1<=R<=x+12を過不足なく覆うA/B/C署名帯表による。x=4ではA/Bが同一の(4,3)子へ合流する。x>=5ではAを帰納仮説、BをK0986、CをK0980で評価する。高R tailはK0832から従う。有限監査は二つの直接再帰と署名表の独立照合であり、全称証明そのものとは区別する。

本項は抽象残余ゲームの固定切片である。z=8,y>=5、z=9,y>=2、z>=10の全Grundy分類、全高さ統一式、標準二次元盤の固定幅・q点安定化長は未解決。
