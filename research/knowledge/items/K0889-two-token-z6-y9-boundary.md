---
id: K0889
title: 2トークン残余ゲーム z=6・y=9切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z6 y9 full Grundy slice]
relations:
- type: depends_on
  target: K0832
  note: A/B/C再帰、Theorem T、一般tail定理、および3族値2位置予想を使用する
- type: depends_on
  target: K0873
  note: C子の評価にz=5の全Grundy公式を使用する
- type: depends_on
  target: K0888
  note: B子の評価にz=6,y=8全Grundy切片を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z6-y9-boundary-20261117/report.md
  role: proof
  note: z=6,y=9切片の全x,R分類をA/B/C選択肢署名表とR強帰納で証明
- path: research/experiments/vertical-fiber-two-token-z6-y9-boundary-20261117/verify_z6_y9.py
  role: verifier
  note: 二方式の直接再帰、z=5/z=6,y=8アンカー、全署名・mex・tailを独立監査
- path: research/experiments/vertical-fiber-two-token-z6-y9-boundary-20261117/output/audit.json
  role: data
  note: 6,232,997検査・不一致0。有限監査であり全称証明とは区別する
- path: research/log/2026-11-17-vertical-fiber-two-token-z6-y9-boundary.md
  role: log
  note: 最新main・未解決範囲との照合、z=6,y=9切片の証明・監査・限界
scope: >-
  κ=1残余ゲームH(R;(x,y);z)の2トークン族、固定高さz=6、y=9、全x≥9・全R≥0。Grundy値0/1/2を完全分類する。
evidence: >-
  Rに関する強帰納。x=9ではA/B子が同一の(9,8)状態に合流し、x≥10ではA子が帰納仮説、B子がK0888のz=6,y=8公式、C子がK0873のz=5公式で評価できる。K0832のTheorem Tにより奇数親の選択肢は{0,1}、偶数親の値は高々1。x=9..17の過渡域とx≥18の偶奇別定常域に分けた全R署名表からmexを決定する。tail R≥x+16ではH=(x+9) mod 2。独立有限監査は二方式直接再帰6,993件、選択肢署名・mex各2,030,844点、tail129,480点、固定seed遠方tail2,000点など計6,232,997検査で不一致0。有限監査は証明の代わりではなく、全称性は選択肢表・Theorem T・tail定理とR強帰納による。
---

全 \(x\ge9,\ R\ge0\) に対して、\(H(R;(x,9);6)\) のGrundy値0/1/2を以下で完全分類する。\(E[a,b]\) は区間内の偶数、\(O[a,b]\) は奇数、\(I[a,\infty)\) は \(a\) 以上の全整数。

値2位置:
\[
T_9(x)=\{1,3,5\}\cup
\begin{cases}
\{21\},&x=9,\\
\{23\},&x=13,\\
\{25,27,29,31\},&x=16,\\
\{25\},&x\ge17,\\
\varnothing,&x\in\{10,11,12,14,15\}.
\end{cases}
\]

値1位置:
\[
P_9(x)=
\begin{cases}
O[7,19],&x=9,\\
O[7,25]\cup I[22,\infty),&x=10,\\
O[7,21],&x=11,\\
O[7,27]\cup I[24,\infty),&x=12,\\
O[7,21],&x=13,\\
O[7,29]\cup I[24,\infty),&x=14,\\
O[7,23],&x=15,\\
O[7,23]\cup E[26,30]\cup I[32,\infty),&x=16,\\
O[7,23]\cup E[26,32],&x=17,\\
O[7,23]\cup E[26,x+14]\cup I[x+16,\infty),&x\ge18\text{ 偶数},\\
O[7,23]\cup E[26,x+15],&x\ge19\text{ 奇数}.
\end{cases}
\]
それ以外の位置の値は0である。全称性の証明はartifactのreport.mdを参照。
