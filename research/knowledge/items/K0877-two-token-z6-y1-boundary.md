---
id: K0877
title: 2トークン残余ゲーム z=6・y=1境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z6 y1 boundary slice]
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームHの再帰、Theorem T、単一トークン全z公式とtail定理を使用する
- type: depends_on
  target: K0873
  note: C子の評価にz=5全Grundy定理のy=1切片を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z6-y1-boundary-20261117/report.md
  role: proof
  note: 固定z=6・y=1・全x,RのGrundy値0/1/2をR強帰納とA/B/C選択肢署名表で分類する全称証明
- path: research/experiments/vertical-fiber-two-token-z6-y1-boundary-20261117/verify_z6_y1.py
  role: verifier
  note: 単一トークンz=7・二トークンz=5境界公式からA/B/C選択肢を再構成し、候補式と署名表を照合する独立監査器
- path: research/experiments/vertical-fiber-two-token-z6-y1-boundary-20261117/output/audit.json
  role: data
  note: 2,096,420照合・不一致0・二回実行byte-identical
- path: research/log/2026-11-17-vertical-fiber-two-token-z6-y1-boundary.md
  role: log
  note: 最新main・未解決範囲との照合、z=6境界切片の選定・証明・監査・限界
scope: >-
  κ=1残余ゲームH(R;(x,y);z)の2トークン族における固定高さz=6、境界y=1、全x≥1・全R≥0。Grundy値0/1/2を完全分類する。
evidence: >-
  Rに関する強帰納。x≥2ではA子を帰納仮説、B子をK0832の単一トークンz=7閉形式、C子をK0873のz=5,y=1境界公式で評価する。x=1では二つのB手が同じ単一トークン子を与える。Theorem Tにより奇数親の選択肢は{0,1}、偶数親の値は高々1。全xを覆う選択肢署名表のmexから閉形式を得る。独立有限監査は2,096,420照合・不一致0であり、全称性の根拠は強帰納証明である。
---

## 定理

\(E[a,b]\) を区間内の偶数、\(O[a,b]\) を奇数、\(I[a,\infty)\) を \(a\) 以上の全整数とする。値2位置 \(T_6^{(1)}(x)\) は

\[
T_6^{(1)}(x)=
\begin{cases}
\{1\},&x=1,\\
\{1,3\},&x\in\{2,3\},\\
\{1,3,5\},&x=4,\\
\{1,3,5,7\},&x=5,\\
\{1,3,5\},&x\in\{6,7\},\\
\{1,3,5\}\cup O[9,15],&x=8,\\
\{1,3,5,9\},&x\ge9.
\end{cases}
\]

値1位置 \(P_6^{(1)}(x)\) は

\[
P_6^{(1)}(x)=
\begin{cases}
\varnothing,&x\in\{1,3,5\},\\
I[4,\infty),&x=2,\\
I[6,\infty),&x=4,\\
I[7,\infty),&x=6,\\
\{7\},&x=7,\\
\{7\}\cup E[10,14]\cup I[16,\infty),&x=8,\\
\{7\}\cup E[10,x+7],&x\ge9\text{ odd},\\
\{7\}\cup E[10,x+6]\cup I[x+8,\infty),&x\ge10\text{ even}.
\end{cases}
\]

任意の \(x\ge1,R\ge0\) について

\[
H(R;(x,1);6)=
\begin{cases}
2,&R\in T_6^{(1)}(x),\\
1,&R\in P_6^{(1)}(x),\\
0,&\text{otherwise}.
\end{cases}
\]

## 証明

\(R=0\) は終局で値0。\(R\ge1,x\ge2\) では選択肢は

\[
\left\{
H(R-1;(x-1,1);6),\
H(R-1;(x);7),\
1\oplus H(R-1;(x,1);5)
\right\}.
\]

\(x=1\) ではA手がなく、二つのB手は同じ単一トークン子である。A子は帰納仮説、B子はK0832の単一トークン公式、C子はK0873のz=5,y=1公式で評価できる。

Theorem Tにより、奇数Rの親では子の残容量が偶数なので選択肢値は0/1だけである。選択肢集合が \(\{0,1\}\)、\(\{0\}\)、\(\{1\}\) または空のどれかに応じてmexは2、1、0、0となる。偶数Rの親は値が高々1なので、選択肢に0があるかだけを見ればよい。

これらをA/B/Cに代入した全 \(x\) の選択肢署名表は[証明報告](../experiments/vertical-fiber-two-token-z6-y1-boundary-20261117/report.md)に記載した。特に \(x=7,8,9\) の過渡例外と \(x\ge10\) の偶奇定常域を分けると、全てのRが被覆され、mexは上記の \(T_6^{(1)},P_6^{(1)}\) と一致する。従ってR強帰納が閉じる。∎

独立監査は2,096,420照合・不一致0。有限監査は全称性の根拠ではなく、全称性は上記の強帰納証明による。詳細は[報告](../experiments/vertical-fiber-two-token-z6-y1-boundary-20261117/report.md)と[検証器](../experiments/vertical-fiber-two-token-z6-y1-boundary-20261117/verify_z6_y1.py)を参照。

## 限界

本項は \(z=6,y=1\) の境界切片だけを証明する。\(z=6,y\ge2\)、\(z\ge7\) の全Grundy分類、全高さを統合する3族の値2位置一般式は未解決である。標準二次元共円ゲームの固定幅安定化長へ直接転送しない。
