---
id: K0977
title: 2トークン残余ゲーム z=7・y=1境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z7 y1 boundary slice]
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームHの再帰、Theorem T、単一トークン全z公式、tail定理、高さのみ縮約を使用する
- type: depends_on
  target: K0877
  note: C子の評価にz=6,y=1境界公式を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z7-y1-boundary-20261119/report.md
  role: proof
  note: 固定z=7・y=1・全x,RのGrundy値0/1/2をx外帰納とA/B/C選択肢署名帯表で分類する全称証明
- path: research/experiments/vertical-fiber-two-token-z7-y1-boundary-20261119/verify_z7_y1.py
  role: verifier
  note: 独立多重集合直接再帰で候補式・署名帯表・単一トークンz=8・K0877転写・tail・高さ縮約を照合する監査器
- path: research/experiments/vertical-fiber-two-token-z7-y1-boundary-20261119/output/audit.json
  role: data
  note: 4,147,450照合・不一致0・二回実行byte-identical
- path: research/log/2026-11-19-vertical-fiber-two-token-z7-y1-boundary.md
  role: log
  note: 最新main・K0976との対照、z=7,y=1境界切片の選定・証明・監査・限界
date: 2026-11-19
scope: >-
  κ=1残余ゲームH(R;(x,y);z)の2トークン族における固定高さz=7、境界y=1、全x>=1・全R>=0。Grundy値0/1/2を完全分類する。K0976がz=7,y>=4有限予想の全称証明に必要とするy=1基底切片を供給する。
evidence: >-
  xに関する外帰納。x>=2ではA子を帰納仮定、B子をK0832の単一トークンz=8閉形式、C子をK0877のz=6,y=1境界公式で評価し、R帰納を不要にする。x=1..10は個別行、x>=11は奇偶2行の定常署名帯表で全Rを被覆し、Theorem Tのmex規則で閉形式が閉じる。tailはR>=x+9でH=(x+1) mod 2。R<=8は高さのみ縮約で全x一意。独立有限監査は4,147,450照合・不一致0であり、全称性の根拠は外帰納証明である。
---

## 定理

\(E[a,b]\) を区間内の偶数、\(O[a,b]\) を奇数、\(I[a,\infty)\) を \(a\) 以上の全整数とする。値2位置 \(T_7^{(1)}(x)\) は

\[
T_7^{(1)}(x)=
\begin{cases}
\{1\},&x=1,\\
\{1,3\},&x\in\{2,3\},\\
\{1,3,5\},&x\in\{4,5\},\\
\{1,3,5,7\},&x\in\{6,7\},\\
O[1,17],&x=9,\\
\{1,3,5,7,9\},&x\ge8,\ x\ne9.
\end{cases}
\]

値1位置 \(P_7^{(1)}(x)\) は

\[
P_7^{(1)}(x)=
\begin{cases}
\varnothing,&x\in\{1,3,5\},\\
I[4,\infty),&x=2,\\
I[6,\infty),&x=4,\\
I[8,\infty),&x=6,\\
\{8\},&x\in\{7,9\},\\
\{8\}\cup I[10,\infty),&x=8,\\
\{8\}\cup O[11,x+8],&x\ge11\text{ odd},\\
\{8\}\cup O[11,x+9]\cup I[x+10,\infty),&x\ge10\text{ even}.
\end{cases}
\]

任意の \(x\ge1,R\ge0\) について

\[
H(R;(x,1);7)=
\begin{cases}
2,&R\in T_7^{(1)}(x),\\
1,&R\in P_7^{(1)}(x),\\
0,&\text{otherwise}.
\end{cases}
\]

特に tail は \(R\ge x+9\) で \(H=(x+1)\bmod 2\) であり、K0832の一般tail定理の2トークン・z=7場合と一致する。

## 証明

\(R=0\) は終局で値0。\(R\ge1,x\ge2\) では選択肢は

\[
\left\{
H(R-1;(x-1,1);7),\
H(R-1;(x);8),\
1\oplus H(R-1;(x,1);6)
\right\}.
\]

\(x=1\) ではA手がなく、2本のB手は同じ単一トークン子 \((1);8\) に帰着する。A子はスライス \(x-1\) の値（x外帰納の仮定）、B子はK0832の単一トークンz=8公式、C子はK0877のz=6,y=1公式で評価でき、R帰納を要しない。

Theorem Tにより偶数親の値は高々1、奇数親の値は高々2で、署名 \(\{0,1\},\{2,3\},\{0,3\},\{0,2\},\{1\},\{0\},\{1,3\},\{1,2\},\{0,2,3\},\{1,2,3\}\) のmexはそれぞれ \(2,0,1,1,0,1,0,0,1,0\) に一意対応する。A/B/Cを代入した全 \(x\) の選択肢署名帯表（x=1..10の個別行と \(x\ge11\) の奇偶2行の定常形）は[証明報告](../../experiments/vertical-fiber-two-token-z7-y1-boundary-20261119/report.md)に記載した。全てのRが帯表で過不足なく被覆され、mexは上記の \(T_7^{(1)},P_7^{(1)}\) と一致する。定常行では子公式の帯境界が全てxの1次式で、x>=11 odd / x>=12 evenについて一様に閉じることを代入で確認した。従ってx外帰納が閉じる。∎

R<=8は高さのみ縮約定理（K0832）で全x一意に \(H=v(x+1,7,R)\) であり、上表のR<=8部分と一致する。x=9の例外 \(T_9=O[1,17]\) はA子スライスx-1=8の無限値1帯とC子のz=6,y=1偶数帯が \(R-1\in E[10,16]\) で揃う機構による。

独立監査は4,147,450照合・不一致0、二回実行byte-identical。有限監査は全称性の根拠ではなく、全称性は上記の外帰納証明による。詳細は[報告](../../experiments/vertical-fiber-two-token-z7-y1-boundary-20261119/report.md)と[検証器](../../experiments/vertical-fiber-two-token-z7-y1-boundary-20261119/verify_z7_y1.py)を参照。

## 限界

本項は \(z=7,y=1\) の境界切片を証明する。\(y=2,3\) は[K0978](K0978-two-token-z7-y2-boundary.md)・[K0979](K0979-two-token-z7-y3-boundary.md)、\(y\ge4\) は[K0976](K0976-two-token-z7-y-ge4-conjecture.md)で全称証明済みであり、2トークン族の \(z=7\) は全 \(y\ge1\) でGrundy値0/1/2が分類された。\(z\ge8\) の全Grundy分類と全高さを統合する値2位置一般式は未解決である。標準二次元共円ゲームの固定幅安定化長へ直接転送しない。
