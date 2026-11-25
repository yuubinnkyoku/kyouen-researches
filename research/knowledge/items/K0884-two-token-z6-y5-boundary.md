---
id: K0884
title: 2トークン残余ゲーム z=6・y=5切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z6 y5 full Grundy slice]
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームHのA/B/C再帰、Theorem T、完了予算・tail定理を使用する
- type: depends_on
  target: K0873
  note: C子の評価にz=5の全Grundyスライスを使用する
- type: depends_on
  target: K0880
  note: B子の評価にz=6,y=4の全Grundy切片を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z6-y5-boundary-20261117/report.md
  role: proof
  note: 固定z=6,y=5・全x,RのGrundy値0/1/2をA/B/C選択肢署名表とR強帰納で分類する全称証明
- path: research/experiments/vertical-fiber-two-token-z6-y5-boundary-20261117/verify_z6_y5.py
  role: verifier
  note: z=5・z=6,y=4アンカーと二方式再帰から署名表・mex・tailを独立監査する検証器
- path: research/experiments/vertical-fiber-two-token-z6-y5-boundary-20261117/output/audit.json
  role: data
  note: 6,205,577検査・不一致0・二回実行byte-identical
- path: research/log/2026-11-17-vertical-fiber-two-token-z6-y5-boundary.md
  role: log
  note: 最新main・未解決事項との照合、z=6,y=5切片の証明・監査・限界
scope: >-
  κ=1残余ゲームH(R;X;z)の2トークン族X=(x,5)、全x≥5・全R≥0、固定高さz=6。Grundy値0/1/2を完全分類する。
evidence: >-
  Rに関する強帰納。x=5では二つのトークン減少手が同じ(5,4)子へ合流し、x≥6ではA子が帰納仮説、B子がK0880のz=6,y=4公式、C子がK0873のz=5全公式で評価できる。K0832のTheorem Tにより奇数親の選択肢は{0,1}、偶数親の値は高々1。x=5..13の過渡域とx≥14偶数・x≥15奇数の定常域に分けた全R署名表からmexを決定する。tail R≥x+12ではH=(x+5) mod 2。独立有限監査は二方式直接再帰3,003件、選択肢署名・mex各2,022,946点、tail129,740点、固定seed遠方tail2,000点など計6,205,577検査で不一致0。有限監査は証明の代わりではなく、全称性は選択肢表・Theorem T・tail定理とR強帰納による。
---

## 定理

偶数区間 \(E[a,b]\) とtail \(I[a,\infty)=\{R\in\mathbb Z:R\ge a\}\) を用いる。値2位置 \(T_6^{(5)}(x)\) は
\[
T_6^{(5)}(x)=
\begin{cases}
\{1,3,5,13\},&x=5,\\
\{1,3,5\},&x\in\{6,7,8\},\\
\{1,3,5,15\},&x=9,\\
\{1,3,5\},&x\in\{10,11\},\\
\{1,3,5,17,19,21,23\},&x=12,\\
\{1,3,5,17\},&x\ge13.
\end{cases}
\]
値1位置 \(P_6^{(5)}(x)\) は
\[
P_6^{(5)}(x)=
\begin{cases}
\{7,9,11\},&x=5,\\
\{7,9,11,13\}\cup I[14,\infty),&x=6,\\
\{7,9,11,13\},&x=7,\\
\{7,9,11,13\}\cup I[15,\infty),&x\in\{8,10\},\\
\{7,9,11,13\},&x=9,\\
\{7,9,11,13,15\},&x=11,\\
\{7,9,11,13,15\}\cup E[18,x+10]\cup I[x+12,\infty),
  &x\ge12\text{ 偶数},\\
\{7,9,11,13,15\}\cup E[18,x+11],
  &x\ge13\text{ 奇数}.
\end{cases}
\]
全 \(x\ge5,R\ge0\) で
\[
H(R;(x,5);6)=
\begin{cases}
2,&R\in T_6^{(5)}(x),\\
1,&R\in P_6^{(5)}(x),\\
0,&\text{それ以外}
\end{cases}
\]
が成立する。

## 証明と限界

\(R\ge1,x\ge6\) の選択肢は
\[
\left\{
H(R-1;(x-1,5);6),\
H(R-1;(x,4);6),\
1\oplus H(R-1;(x,5);5)
\right\}.
\]
A子は \(R\) 強帰納仮説、B子はK0880、C子はK0873で評価する。\(x=5\) ではA/Bが同一の \((5,4)\) 子となる。

Theorem Tにより奇数親の選択肢値は0/1に限られ、偶数親の値は高々1。報告書の全パラメータ署名表は \(1\le R<x+12\) を覆い、奇数親では署名のmex、偶数親では0の出現だけから閉形式を得る。tail定理は \(R\ge x+12\) で \(H=(x+5)\bmod2\) を与えるため、強帰納が閉じる。

値2位置はK0832の3族予想の \(z=6,y=5\) 特殊化とも一致する（EXTが13,15、\(d=7\) のランが17,19,21,23、\(d\ge8\) の定常点が17）。これは当該切片の証明であり、一般予想全体の証明ではない。

本項は抽象残余ゲームの \(z=6,y=5\) のみを証明する。\(z=6,y\ge6\)、\(z\ge7\)、全高さを統合する3族値2位置一般式は未解決。標準二次元共円ゲームの固定幅安定化長へ直接転送しない。