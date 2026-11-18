---
id: K0978
title: 2トークン残余ゲーム z=7・y=2境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z7 y2 boundary slice]
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームHの再帰、Theorem T、tail定理、高さのみ縮約を使用する
- type: depends_on
  target: K0977
  note: B子の評価にz=7,y=1境界公式を使用する
- type: depends_on
  target: K0878
  note: C子の評価にz=6,y=2境界公式を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z7-y2-boundary-20261119/report.md
  role: proof
  note: 固定z=7・y=2・全x>=2,R>=0のGrundy値0/1/2をx外帰納とA/B/C選択肢署名帯表で分類する全称証明
- path: research/experiments/vertical-fiber-two-token-z7-y2-boundary-20261119/verify_z7_y2.py
  role: verifier
  note: 独立多重集合直接再帰で候補式・署名帯表・K0878転写・K0977公式・tail・高さ縮約を照合する監査器
- path: research/experiments/vertical-fiber-two-token-z7-y2-boundary-20261119/output/audit.json
  role: data
  note: 4,143,470照合・不一致0・二回実行byte-identical
- path: research/log/2026-11-19-vertical-fiber-two-token-z7-y2-boundary.md
  role: log
  note: 最新main・K0977/K0976との対照、z=7,y=2境界切片の選定・証明・監査・限界
date: 2026-11-19
scope: >-
  κ=1残余ゲームH(R;(x,y);z)の2トークン族における固定高さz=7、境界y=2、全x>=2・全R>=0。Grundy値0/1/2を完全分類する。K0976がz=7,y>=4有限予想の全称証明に必要とするy=1,2,3基底切片のうちy=2を供給する。
evidence: >-
  xに関する外帰納。x>=3ではA子をy=2族スライスx-1の帰納仮定、B子をK0977のz=7,y=1公式、C子をK0878のz=6,y=2公式で評価し、R帰納を不要にする。x=2は減少手2本が同一子(1,2)に合流。x=2..11は個別行、x>=12は奇偶2行の定常署名帯表で全Rを被覆し、Theorem Tのmex規則で閉形式が閉じる。tailはR>=x+10でH=(x+2) mod 2。R<=8は高さのみ縮約で全x一意。独立有限監査は4,143,470照合・不一致0であり、全称性の根拠は外帰納証明である。
---

## 定理

\(E[a,b]\) を区間内の偶数、\(O[a,b]\) を奇数、\(I[a,\infty)\) を \(a\) 以上の全整数とする。値2位置 \(T_7^{(2)}(x)\) は

\[
T_7^{(2)}(x)=
\begin{cases}
\{1,3\},&x=2,\\
\{1,3,5\},&x\in\{3,4\},\\
\{1,3,5,7,9\},&x=5,\\
\{1,3,5,7\},&x\in\{6,7,8\},\\
\{1,3,5,7,11\},&x=9,\\
\{1,3,5,7,11\}\cup O[13,19],&x=10,\\
\{1,3,5,7,11\},&x\ge11.
\end{cases}
\]

値1位置 \(P_7^{(2)}(x)\) は

\[
P_7^{(2)}(x)=
\begin{cases}
\varnothing,&x\in\{2,4\},\\
I[6,\infty),&x=3,\\
\{8\}\cup I[10,\infty),&x\in\{5,7\},\\
\{8\},&x=6,\\
\{8,10\},&x\in\{8,10\},\\
\{8,10\}\cup I[12,\infty),&x=9,\\
\{8,10\}\cup O[13,x+9]\cup I[x+10,\infty),&x\ge11\text{ odd},\\
\{8,10\}\cup O[13,x+9],&x\ge12\text{ even}.
\end{cases}
\]

任意の \(x\ge2,R\ge0\) について

\[
H(R;(x,2);7)=
\begin{cases}
2,&R\in T_7^{(2)}(x),\\
1,&R\in P_7^{(2)}(x),\\
0,&\text{otherwise}.
\end{cases}
\]

特に tail は \(R\ge x+10\) で \(H=(x+2)\bmod 2\) であり、K0832の一般tail定理（\(R\ge S+z+1=x+10\)、\(H=S\bmod 2\)）と一致する。\(R\le8\) は高さのみ縮約（K0832）で全x一意に \(H=v(x+2,7,R)\) である。

## 証明

\(R=0\) は終局で値0。\(R\ge1\) で \(x\ge3\) の選択肢は

\[
\left\{
H(R-1;(x-1,2);7),\\
H(R-1;(x,1);7),\\
1\oplus H(R-1;(x,2);6)
\right\}.
\]

\(x=2\) では \(X=(2,2)\) の減少手2本が同一の子 \((1,2)\) に合流し、選択肢は \(\{H(R-1;(1,2);7),\,1\oplus H(R-1;(2,2);6)\}\) である。A子はy=2族スライス \(x-1\) の値（x外帰納の仮定）、B子はK0977のz=7,y=1公式、C子はK0878のz=6,y=2公式で評価でき、R帰納を要しない。

Theorem Tにより偶数親の値は高々1、奇数親の値は高々2で、署名 \(\{0,1\},\{2,3\},\{0,3\},\{0,2\},\{1\},\{0\},\{1,3\},\{1,2\},\{0,2,3\},\{1,2,3\}\) のmexはそれぞれ \(2,0,1,1,0,1,0,0,1,0\) に一意対応する。A/B/Cを代入した全 \(x\) の選択肢署名帯表（x=2..11の個別行と \(x\ge12\) の奇偶2行の定常形）は[証明報告](../../experiments/vertical-fiber-two-token-z7-y2-boundary-20261119/report.md)に記載した。全てのRが帯表で過不足なく被覆され、mexは上記の \(T_7^{(2)},P_7^{(2)}\) と一致する。定常行では子公式の帯境界が全てxの1次式で、x>=12 even / x>=13 odd について一様に閉じることを代入で確認した（x=11行はE[14,20]帯の署名のみ12で値は定常行と同一）。従ってx外帰納が閉じる。∎

## 構造

定常値2位置はz=6,y=2（K0878）の \(\{1,3,5,11\}\) に対し \(\{1,3,5,7,11\}\)（zの増分7が加わる）。z=7,y=1の \(\{1,3,5,7,9\}\) に対しては9と11が入れ替わる。x=10の例外 \(T_{10}\supset O[13,19]\) はA子スライス9の無限値1帯 \(I[12,\infty)\) とB子の偶数ギャップが \(r\in\{10\}\cup E[12,18]\) で揃う機構で、x>=12偶ではA子のI帯が \(I[x+9,\infty)\) に後退してB子の \(I[x+10,\infty)\) とすれ違い消える。

## 限界

本項は \(z=7,y=2\) の境界切片だけを証明する。\(z=7\) の \(y=3\) は未証明であり、[K0976](K0976-two-token-z7-y-ge4-conjecture.md)のy>=4有限予想の全称証明にはy=3基底切片がなお必要である。y=3のC子はK0879（z=6,y=3）で既に全称証明済みであり、本項と同じ構造（A子=y=3族x外帰納、B子=K0977、C子=K0879）で取り組める。y=1,2が揃ったことでz=7の未証明境界はy=3のみ、統一式は別課題。\(z\ge8\) の全Grundy分類は未解決である。標準二次元共円ゲームの固定幅安定化長へ直接転送しない。
