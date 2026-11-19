---
id: K1005
title: 2トークン残余ゲーム z=10・y=3境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z10 y3 boundary slice]
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームHの再帰、Theorem T、単一トークン全z公式、tail定理、高さのみ縮約を使用する
- type: depends_on
  target: K1004
  note: B子の評価にz=10,y=2境界切片を使用する
- type: depends_on
  target: K0989
  note: C子の評価にz=9,y=3境界切片を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z10-y3-boundary-20261119/report.md
  role: proof
  note: 固定z=10・y=3・全x>=3,R>=0のGrundy値0/1/2をx外帰納とA/B/C署名帯表で分類する全称証明
- path: research/experiments/vertical-fiber-two-token-z10-y3-boundary-20261119/verify_z10_y3.py
  role: verifier
  note: 独立実装の直接mex再帰、降順正準化第2実装、アンカー照合、全x署名帯表とTheorem Tと高さのみ縮約を監査する検証器
- path: research/experiments/vertical-fiber-two-token-z10-y3-boundary-20261119/output/audit.json
  role: data
  note: 8,182,142照合・不一致0・二回実行byte-identical
- path: research/log/2026-11-19-vertical-fiber-two-token-z10-y3-boundary.md
  role: log
  note: K1004/K0989を用いたz=10,y=3切片の発見・外帰納証明・独立監査・限界
scope: >-
  κ=1残余ゲームH(R;(x,y);z)の2トークン族における固定高さz=10、y=3、全x>=3・全R>=0。
  Grundy値0/1/2を完全分類する。
evidence: >-
  xに関する外帰納。x>=4ではA子を帰納仮説、B子をK1004のz=10,y=2公式、C子をK0989の
  z=9,y=3公式で評価する。x=3では2つのトークン減少手が同一の(2,3);10子に合流する。
  x=3..15の個別署名帯とx>=16偶/x>=17奇の定常署名帯で全Rを被覆し、Theorem Tのmex規則で
  閉じる。R<=11は高さのみ縮約でv_single(x+3,10,R)に一致し並走レーンの低残余帯と接続、
  tailはR>=x+14でH=(x+3) mod 2。独立有限監査は8,182,142照合・不一致0であり、
  全称性の根拠は外帰納と署名表である。
---

## 定理

値2位置を \(T_{10}^{(3)}(x)\)、値1位置を \(P_{10}^{(3)}(x)\) とする。\(O[a,b]\) は区間内の奇数、\(E[a,b]\) は偶数、\(I[a,\infty)\) は \(a\) 以上の全整数である。

\[
T_{10}^{(3)}(x)=
\begin{cases}
\{1,3,5\},&x=3,\\
\{1,3,5,7\},&x\in\{4,5\},\\
\{1,3,5,7,9\},&x=6,\\
\{1,3,5,7,9,11,13\},&x=7,\\
\{1,3,5,7,9\},&x\in\{8,9,10,12,13\},\\
\{1,3,5,7,9,15\},&x=11,\\
\{1,3,5,7,9\}\cup O[17,27],&x=14,\\
\{1,3,5,7,9,17\},&x\ge15.
\end{cases}
\]

\[
P_{10}^{(3)}(x)=
\begin{cases}
\varnothing,&x\in\{3,5,7\},\\
I[8,\infty),&x=4,\\
I[10,\infty),&x=6,\\
\{11,13\},&x\in\{9,11\},\\
\{11,13\}\cup I[14,\infty),&x=8,\\
\{11,13\}\cup I[15,\infty),&x\in\{10,12\},\\
\{11,13,15\},&x=13,\\
\{11,13,15\}\cup E[18,26]\cup I[28,\infty),&x=14,\\
\{11,13,15\}\cup E[18,x+12]\cup I[x+14,\infty),&x\ge16\text{ 偶数},\\
\{11,13,15\}\cup E[18,x+13],&x\ge15\text{ 奇数}.
\end{cases}
\]

全 \(x\ge3,R\ge0\) について

\[
H(R;(x,3);10)=
\begin{cases}
2,&R\in T_{10}^{(3)}(x),\\
1,&R\in P_{10}^{(3)}(x),\\
0,&\text{それ以外}.
\end{cases}
\]

一般tailは

\[
R\ge x+14\implies H(R;(x,3);10)=(x+3)\bmod2.
\]

## 証明の要点

\(R\ge1,x\ge4\) の選択肢は

\[
A=H(R-1;(x-1,3);10),\quad
B=H(R-1;(x,2);10),\quad
C=1\oplus H(R-1;(x,3);9).
\]

Aはx外帰納、BはK1004、CはK0989で与えられる。x=3ではA手とB手が同一の(2,3);10子に合流する。

全xのA/B/C署名帯は証明報告に列挙した。mex対応は 01→2, 23→0, 03→1, 02→1, 023→1, 123→0, 12→0, 0→1, 1→0。Theorem Tにより奇数Rの親は値2以下、偶数Rの親は値1以下であり、署名表のmexが上記のT/Pを与える。

x=7（高さh=x+y=10=z）はz+1=11に加えてz+3=13も値2となる2点前倒しの新形（y=1,2のh=z行は1点）、x=11は前倒し生存点（x=y+8、R=2y+9=15）、x=14（=z+y+1）は掃引行（掃引帯O[17,27]=O[pin,x+y+z]、pin=2y+z+[z偶]=17）、x=15はA子が掃引行を横切る移行行（偶帯E[18,28]全体の署名02）、x≥16偶/x≥17奇では帯境界がxの一次式で一様に成立する。値1の基底点は{11,13,15}={z+1,z+3,z+5}の3点（基底点y個仮説）、帯開始はz+2y+2=18で偶奇はzの偶奇（E帯）で決まり、I帯はx偶数行のみ（tail値(x+y) mod 2が1の行）。R≤11の列は高さのみ縮約v_single(x+3,10,R)に一致し並走レーン出版のz=10低残余帯と完全一致する。tailはR>=x+14でH=(x+3) mod 2。従って外帰納が閉じる。

## 限界

本項は抽象残余ゲームのz=10,y=3切片のみ。z=10のy=4..5は未証明（y=4はA=x外帰納・B子=本項・C子=1 xor K0990で着手可能）、y>=6はK1002の候補のまま。z>=11・全高さを統合する2トークン値2位置の一般式、標準二次元盤の固定幅・q点安定化長は未解決。
