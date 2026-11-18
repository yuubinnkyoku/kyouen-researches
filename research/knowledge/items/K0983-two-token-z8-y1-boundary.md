---
id: K0983
title: 2トークン残余ゲーム z=8・y=1境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z8 y1 boundary slice]
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームHの再帰、Theorem T、単一トークン全z公式、tail定理、高さのみ縮約を使用する
- type: depends_on
  target: K0977
  note: C子の評価にz=7,y=1境界公式を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z8-y1-boundary-20261119/report.md
  role: proof
  note: 固定z=8・y=1・全x,RのGrundy値0/1/2をx外帰納とA/B/C選択肢署名帯表で分類する全称証明
- path: research/experiments/vertical-fiber-two-token-z8-y1-boundary-20261119/verify_z8_y1.py
  role: verifier
  note: 独立多重集合直接再帰で候補式・署名帯表・単一トークンz=9・K0977転写・tail・高さ縮約・Theorem Tを照合する監査器
- path: research/experiments/vertical-fiber-two-token-z8-y1-boundary-20261119/output/audit.json
  role: data
  note: 4,164,960照合・不一致0・二回実行byte-identical
- path: research/log/2026-11-19-vertical-fiber-two-token-z8-y1-boundary.md
  role: log
  note: 最新main・K0977〜K0982との対照、z=8,y=1境界切片の選定・証明・監査・限界
date: 2026-11-19
scope: >-
  κ=1残余ゲームH(R;(x,y);z)の2トークン族における固定高さz=8、境界y=1、全x>=1・全R>=0。Grundy値0/1/2を完全分類する。z>=8の2トークン族として最初の全称証明済み切片である。
evidence: >-
  xに関する外帰納。x>=2ではA子を帰納仮定、B子をK0832の単一トークンz=9閉形式、C子をK0977のz=7,y=1境界公式で評価し、R帰納を不要にする。x=1..11は個別行（x=11は値は定常だが署名が一部異なる）、x>=12偶/x>=13奇は2行の定常署名帯表で全Rを被覆し、Theorem Tのmex規則で閉形式が閉じる。tailはR>=x+10でH=(x+1) mod 2。R<=9は高さのみ縮約で全x一意。独立有限監査は4,164,960照合・不一致0であり、全称性の根拠は外帰納証明である。
---

## 定理

\(E[a,b]\) を区間内の偶数、\(O[a,b]\) を奇数、\(I[a,\infty)\) を \(a\) 以上の全整数とする。値2位置 \(T_8^{(1)}(x)\) は

\[
T_8^{(1)}(x)=
\begin{cases}
\{1\},&x=1,\\
\{1,3\},&x\in\{2,3\},\\
\{1,3,5\},&x\in\{4,5\},\\
\{1,3,5,7\},&x=6,\\
\{1,3,5,7,9\},&x=7,\\
\{1,3,5,7\},&x\in\{8,9\},\\
\{1,3,5,7\}\cup O[11,19],&x=10,\\
\{1,3,5,7,11\},&x\ge11.
\end{cases}
\]

値1位置 \(P_8^{(1)}(x)\) は

\[
P_8^{(1)}(x)=
\begin{cases}
\varnothing,&x\in\{1,3,5,7\},\\
I[4,\infty),&x=2,\\
I[6,\infty),&x=4,\\
I[8,\infty),&x=6,\\
I[9,\infty),&x=8,\\
\{9\},&x=9,\\
\{9\}\cup E[12,18]\cup I[20,\infty),&x=10,\\
\{9\}\cup E[12,x+9],&x\ge11\text{ odd},\\
\{9\}\cup E[12,x+8]\cup I[x+10,\infty),&x\ge12\text{ even}.
\end{cases}
\]

任意の \(x\ge1,R\ge0\) について

\[
H(R;(x,1);8)=
\begin{cases}
2,&R\in T_8^{(1)}(x),\\
1,&R\in P_8^{(1)}(x),\\
0,&\text{otherwise}.
\end{cases}
\]

特に tail は \(R\ge x+10\) で \(H=(x+1)\bmod 2\) であり、K0832の一般tail定理の2トークン・z=8場合と一致する。値2位置の定常形は \(\{1,3,5,7,11\}\) で、z=7の \(\{1,3,5,7,9\}\) と違い第5点が9でなく11になる。

## 証明

\(R=0\) は終局で値0。\(R\ge1,x\ge2\) では選択肢は

\[
\left\{
H(R-1;(x-1,1);8),\
H(R-1;(x);9),\
1\oplus H(R-1;(x,1);7)
\right\}.
\]

\(x=1\) ではA手がなく、2本のB手は同じ単一トークン子 \((1);9\) に帰着する。A子はスライス \(x-1\) の値（x外帰納の仮定）、B子はK0832の単一トークンz=9公式、C子はK0977のz=7,y=1公式で評価でき、R帰納を要しない。
Theorem Tにより偶数親の値は高々1、奇数親の値は高々2で、署名 \(\{0,1\},\{2,3\},\{0,3\},\{0,2\},\{1\},\{0\},\{1,3\},\{1,2\},\{0,2,3\},\{1,2,3\}\) のmexはそれぞれ \(2,0,1,1,0,1,0,0,1,0\) に一意対応する。A/B/Cを代入した全 \(x\) の選択肢署名帯表（x=1..11の個別行と \(x\ge12\) 偶数・\(x\ge13\) 奇数の定常2行）は[証明報告](../../experiments/vertical-fiber-two-token-z8-y1-boundary-20261119/report.md)に記載した。全てのRが帯表で過不足なく被覆され、mexは上記の \(T_8^{(1)},P_8^{(1)}\) と一致する。定常行では子公式の帯境界が全てxの1次式で、x>=12 even / x>=13 oddについて一様に閉じることを代入で確認した。x=11は値は奇数定常行と同一だが、A子がスライスx=10の例外T帯 \(O[11,19]\) を映して \(R\in E[14,20]\) の署名が \{0,2\} になるため個別行とした（mexは不変）。従ってx外帰納が閉じる。∎

R<=9は高さのみ縮約定理（K0832）で全x一意に \(H=v(x+1,8,R)\) であり、上表のR<=9部分と一致する。x=10の例外 \(T_{10}=\{1,3,5,7\}\cup O[11,19]\) はB子 \(v(10,9,\cdot)\) の中間帯 \(9<r<19\) がr偶で1を供給しC子のP₇(10)がr偶数≥10で不在となる機構による（z=7のx=9例外がA子の無限P帯起因だったのとは異なる）。

独立監査は4,164,960照合・不一致0、二回実行byte-identical。有限監査は全称性の根拠ではなく、全称性は上記の外帰納証明による。詳細は[報告](../../experiments/vertical-fiber-two-token-z8-y1-boundary-20261119/report.md)と[検証器](../../experiments/vertical-fiber-two-token-z8-y1-boundary-20261119/verify_z8_y1.py)を参照。

## 限界

本項は \(z=8,y=1\) の境界切片を証明する。z=8のy=2はK0984、y=3はK0986で全称証明済みであり、z=8のy>=4、z=9のy>=2、z>=10は未解決である。2トークン族の全高さ\(z\)を統合する値2位置一般式は未解決である。標準二次元共円ゲームの固定幅安定化長へ直接転送しない。
