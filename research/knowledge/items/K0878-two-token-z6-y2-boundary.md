---
id: K0878
title: 2トークン残余ゲーム z=6・y=2境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z6 y2 boundary slice]
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームHの定義、A/B/C再帰、Theorem T、tail定理を使用する
- type: depends_on
  target: K0873
  note: C子の評価にz=5の全Grundy定理を使用する
- type: depends_on
  target: K0877
  note: B子の評価にz=6,y=1境界切片の全Grundy定理を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z6-y2-boundary-20261117/report.md
  role: proof
  note: 固定z=6・y=2・全x≥2,R≥0のGrundy値0/1/2をA/B/C選択肢署名表とR強帰納で分類する全称証明
- path: research/experiments/vertical-fiber-two-token-z6-y2-boundary-20261117/verify_z6_y2.py
  role: verifier
  note: z=5全式とz=6,y=1全式からA/B/C子を再構成し、直接再帰・mex・署名表を独立監査する標準ライブラリ検証器
- path: research/experiments/vertical-fiber-two-token-z6-y2-boundary-20261117/output/audit.json
  role: data
  note: 4,165,275検査・不一致0・二回実行byte-identical
- path: research/log/2026-11-17-vertical-fiber-two-token-z6-y2-boundary.md
  role: log
  note: 最新main・未解決範囲との照合、z=6,y=2切片の証明・監査・限界
scope: >-
  κ=1残余ゲームH(R;X;z)の2トークン族X=(x,2)、全x≥2・全R≥0、固定高さz=6。Grundy値0/1/2を完全分類する。
evidence: >-
  Rに関する強帰納。x=2では2つのトークン減少手が同じ(x,1)子へ合流し、x≥3ではA子が帰納仮説、B子がK0877のz=6,y=1公式、C子がK0873のz=5全公式で評価される。K0832のTheorem Tにより奇数親の選択肢は{0,1}、偶数親の値は高々1。x=2..9の過渡域とx≥10の偶奇定常域に分けた全R署名表からmexを決定する。独立有限監査は直接再帰17,343状態、署名・mex各2,062,968点、tail19,996点、固定seed2,000点を含む4,165,275検査で不一致0。有限監査は証明の代わりではなく、全称性は選択肢表とR強帰納による。
---

## 定理

\(E[a,b]\) を区間内の偶数、\(O[a,b]\) を奇数、\(I[a,\infty)\) を \(a\) 以上の全整数とする。\(x\ge2\) に対し、値2位置 \(T_6^{(2)}(x)\) は

\[
T_6^{(2)}(x)=
\begin{cases}
\{1,3\},&x=2,\\
\{1,3,5\},&x\in\{3,5,7,8\},\\
\{1,3,5,7\},&x=4,\\
\{1,3,5,9\},&x=6,\\
\{1,3,5\}\cup O[11,17],&x=9,\\
\{1,3,5,11\},&x\ge10.
\end{cases}
\]

値1位置 \(P_6^{(2)}(x)\) は

\[
P_6^{(2)}(x)=
\begin{cases}
\varnothing,&x\in\{2,4\},\\
I[6,\infty),&x=3,\\
\{7\}\cup I[9,\infty),&x\in\{5,7\},\\
\{7\},&x=6,\\
\{7,9\},&x=8,\\
\{7,9\}\cup E[12,16]\cup I[18,\infty),&x=9,\\
\{7,9\}\cup E[12,x+8],&x\ge10\text{ even},\\
\{7,9\}\cup E[12,x+7]\cup I[x+9,\infty),&x\ge11\text{ odd}.
\end{cases}
\]

任意の \(x\ge2,R\ge0\) について

\[
H(R;(x,2);6)=
\begin{cases}
2,&R\in T_6^{(2)}(x),\\
1,&R\in P_6^{(2)}(x),\\
0,&\text{otherwise}
\end{cases}
\]

が成立する。

## 証明

\(R=0\) は終局で値0。\(R\ge1,x\ge3\) の選択肢は

\[
V_x(R)=\left\{
H(R-1;(x-1,2);6),
H(R-1;(x,1);6),
1\oplus H(R-1;(x,2);5)
\right\}.
\]

A子は \(R\) 強帰納仮説、B子はK0877、C子はK0873で評価する。\(x=2\) では2つのトークン減少手が同じ \((2,1)\) 子になるため、A/Bを一つにまとめる。

K0832のTheorem Tより、全残余値は2以下であり、偶数残容量の親の値は1以下である。従って奇数親では子の値が全て0/1に限られ、選択肢署名01, 0, 1のmexはそれぞれ2,1,0。偶数親では選択肢に0が含まれるかだけで値1/0が決まる。

A/B/Cの既知公式を代入した全 \(x,R\) の署名表、過渡域 \(x=2,\ldots,9\) と定常域 \(x\ge10\) の分割、mexの各セルへの適用は証明報告に記した。表は奇数R・偶数Rをそれぞれ全て分割するので、任意のRで帰納段階が閉じる。∎

## 独立監査と限界

検証器は直接再帰、z=5,y=2アンカー、z=6,y=1アンカー、A/B/C署名、mex、tailを4,165,275件検査し、不一致0。二回実行の監査JSONはバイト単位で一致した。有限監査は全称性の根拠ではなく、全称性は上記のR強帰納証明による。

本項は \(z=6,y=2\) のみを証明する。\(z=6,y=3\) は[K0879](K0879-two-token-z6-y3-boundary.md)で証明済みであり、\(z=6,y=4\) は[K0880](K0880-two-token-z6-y4-boundary.md)で証明済みであり、\(z=6,y\ge5\)、\(z\ge7\) の全Grundy分類と、全高さを統合する3族値2位置一般式は未解決である。標準二次元共円ゲームの固定幅安定化長へ直接転送しない。
