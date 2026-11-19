---
id: K1004
title: 2トークン残余ゲーム z=10・y=2境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z10 y2 boundary slice]
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームHの再帰、Theorem T、単一トークン全z公式、tail定理、高さのみ縮約を使用する
- type: depends_on
  target: K1003
  note: B子の評価にz=10,y=1境界切片を使用する
- type: depends_on
  target: K0988
  note: C子の評価にz=9,y=2境界切片を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z10-y2-boundary-20261119/report.md
  role: proof
  note: 固定z=10・y=2・全x>=2,R>=0のGrundy値0/1/2をx外帰納とA/B/C署名帯表で分類する全称証明
- path: research/experiments/vertical-fiber-two-token-z10-y2-boundary-20261119/verify_z10_y2.py
  role: verifier
  note: 独立実装の直接mex再帰、反復DP第2実装、アンカー照合、全x署名帯表とTheorem Tと高さのみ縮約を監査する検証器
- path: research/experiments/vertical-fiber-two-token-z10-y2-boundary-20261119/output/audit.json
  role: data
  note: 4,175,318照合・不一致0・二回実行byte-identical
- path: research/log/2026-11-19-vertical-fiber-two-token-z10-y2-boundary.md
  role: log
  note: K1003/K0988を用いたz=10,y=2切片の発見・外帰納証明・独立監査・限界
scope: >-
  κ=1残余ゲームH(R;(x,y);z)の2トークン族における固定高さz=10、y=2、全x>=2・全R>=0。
  Grundy値0/1/2を完全分類する。
evidence: >-
  xに関する外帰納。x>=3ではA子を帰納仮説、B子をK1003のz=10,y=1公式、C子をK0988の
  z=9,y=2公式で評価する。x=2では2つのトークン減少手が同一の(1,2);10子に合流する。
  x=2..14の個別署名帯とx>=16偶/x>=15奇の定常署名帯で全Rを被覆し、Theorem Tのmex規則で
  閉じる。R<=11は高さのみ縮約でv_single(x+2,10,R)に一致し並走レーンの低残余帯と接続、
  tailはR>=x+13でH=(x+2) mod 2。独立有限監査は4,175,318照合・不一致0であり、
  全称性の根拠は外帰納と署名表である。
---

## 定理

値2位置を \(T_{10}^{(2)}(x)\)、値1位置を \(P_{10}^{(2)}(x)\) とする。\(O[a,b]\) は区間内の奇数、\(E[a,b]\) は偶数、\(I[a,\infty)\) は \(a\) 以上の全整数である。

\[
T_{10}^{(2)}(x)=
\begin{cases}
\{1,3\},&x=2,\\
\{1,3,5\},&x\in\{3,4\},\\
\{1,3,5,7\},&x\in\{5,6\},\\
\{1,3,5,7,9\},&x=7,\\
\{1,3,5,7,9,11\},&x=8,\\
\{1,3,5,7,9\},&x=9,\\
\{1,3,5,7,9,13\},&x=10,\\
\{1,3,5,7,9\},&x\in\{11,12\},\\
\{1,3,5,7,9\}\cup O[15,25],&x=13,\\
\{1,3,5,7,9,15\},&x\ge14.
\end{cases}
\]

\[
P_{10}^{(2)}(x)=
\begin{cases}
\varnothing,&x\in\{2,4,6,8\},\\
I[6,\infty),&x=3,\\
I[8,\infty),&x=5,\\
I[10,\infty),&x=7,\\
\{11,13\}\cup I[14,\infty),&x\in\{9,11\},\\
\{11\},&x=10,\\
\{11,13\},&x=12,\\
\{11,13\}\cup E[16,x+11]\cup I[x+13,\infty),&x\ge13\text{ 奇数},\\
\{11,13\}\cup E[16,x+12],&x\ge14\text{ 偶数}.
\end{cases}
\]

全 \(x\ge2,R\ge0\) について

\[
H(R;(x,2);10)=
\begin{cases}
2,&R\in T_{10}^{(2)}(x),\\
1,&R\in P_{10}^{(2)}(x),\\
0,&\text{それ以外}.
\end{cases}
\]

一般tailは

\[
R\ge x+13\implies H(R;(x,2);10)=(x+2)\bmod2.
\]

## 証明の要点

\(R\ge1,x\ge3\) の選択肢は

\[
A=H(R-1;(x-1,2);10),\quad
B=H(R-1;(x,1);10),\quad
C=1\oplus H(R-1;(x,2);9).
\]

Aはx外帰納、BはK1003、CはK0988で与えられる。x=2ではA手とB手が同一の(1,2);10子に合流する。

全xのA/B/C署名帯は証明報告に列挙した。mex対応は 01→2, 23→0, 03→1, 02→1, 023→1, 123→0, 12→0, 0→1, 1→0。Theorem Tにより奇数Rの親は値2以下、偶数Rの親は値1以下であり、署名表のmexが上記のT/Pを与える。

x=8（高さx+y=z）は高さのみ縮約のz=h枠による追加点11、x=10は前倒し格子d=8（x=y+8）の点13、x=13（=z+y+1）は掃引行（掃引帯O[15,25]=O[pin,x+y+z]、pin=2y+z+1=15）、x=14はA子が掃引行を横切る移行行（署名のみ異なる）、x≥16偶/x≥15奇では帯境界がxの一次式で一様に成立する。値1の基底点は{z+1,z+3}={11,13}の2点、帯開始は z+2y+2=16 で偶奇はzの偶奇（E帯）で決まる。R≤11の列は高さのみ縮約v_single(x+2,10,R)に一致し、並走レーン出版のz=10低残余帯（R=0..11・tail）と完全一致する。tailはR>=x+13でH=(x+2) mod 2。従って外帰納が閉じる。

## 限界

本項は抽象残余ゲームのz=10,y=2切片のみ。z=10のy=3はK1005で証明済み、y=4..5は未証明（y=4はA=x外帰納・B子=K1005・C子=1 xor K0990で着手可能）、y>=6はK1002の候補のまま。z>=11・全高さを統合する2トークン値2位置の一般式、標準二次元盤の固定幅・q点安定化長は未解決。
