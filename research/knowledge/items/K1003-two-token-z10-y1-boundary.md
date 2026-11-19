---
id: K1003
title: 2トークン残余ゲーム z=10・y=1境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z10 y1 boundary slice]
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームHの再帰、Theorem T、単一トークン全z公式、tail定理、高さのみ縮約を使用する
- type: depends_on
  target: K0985
  note: C子の評価にz=9,y=1境界切片を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z10-y1-boundary-20261119/report.md
  role: proof
  note: 固定z=10・y=1・全x>=1,R>=0のGrundy値0/1/2をx外帰納とA/B/C署名帯表で分類する全称証明
- path: research/experiments/vertical-fiber-two-token-z10-y1-boundary-20261119/verify_z10_y1.py
  role: verifier
  note: 独立実装の直接mex再帰、アンカー照合、全x署名帯表とTheorem Tを監査する検証器
- path: research/experiments/vertical-fiber-two-token-z10-y1-boundary-20261119/output/audit.json
  role: data
  note: 4,165,960照合・不一致0・二回実行byte-identical
- path: research/log/2026-11-19-vertical-fiber-two-token-z10-y1-boundary.md
  role: log
  note: K0985を用いたz=10,y=1切片の発見・外帰納証明・独立監査・限界
scope: >-
  κ=1残余ゲームH(R;(x,y);z)の2トークン族における固定高さz=10、y=1、全x>=1・全R>=0。
  Grundy値0/1/2を完全分類する。
evidence: >-
  xに関する外帰納。x>=2ではA子を帰納仮説、B子をK0832の単一トークンz=11公式、
  C子をK0985のz=9,y=1公式で評価する。x=1では二つの除去手が同一の(1);11子に合流する。
  x=1..13の個別署名帯とx>=14偶/x>=15奇の定常署名帯で全Rを被覆し、Theorem Tのmex規則で
  閉じる。tailはR>=x+12でH=(x+1) mod 2。独立有限監査は4,165,960照合・不一致0であり、
  全称性の根拠は外帰納と署名表である。
---

## 定理

値2位置を \(T_{10}^{(1)}(x)\)、値1位置を \(P_{10}^{(1)}(x)\) とする。\(O[a,b]\) は区間内の奇数、\(E[a,b]\) は偶数、\(I[a,\infty)\) は \(a\) 以上の全整数である。

\[
T_{10}^{(1)}(x)=
\begin{cases}
\{1\},&x=1,\\
\{1,3\},&x\in\{2,3\},\\
\{1,3,5\},&x\in\{4,5\},\\
\{1,3,5,7\},&x\in\{6,7\},\\
\{1,3,5,7,9\},&x=8,\\
\{1,3,5,7,9,11\},&x=9,\\
\{1,3,5,7,9\},&x\in\{10,11\},\\
\{1,3,5,7,9\}\cup O[13,23],&x=12,\\
\{1,3,5,7,9,13\},&x\ge13.
\end{cases}
\]

\[
P_{10}^{(1)}(x)=
\begin{cases}
\varnothing,&x\in\{1,3,5,7,9\},\\
I[4,\infty),&x=2,\\
I[6,\infty),&x=4,\\
I[8,\infty),&x=6,\\
I[10,\infty),&x=8,\\
I[11,\infty),&x=10,\\
\{11\},&x=11,\\
\{11\}\cup E[14,22]\cup I[24,\infty),&x=12,\\
\{11\}\cup E[14,x+11],&x\ge13\text{ 奇数},\\
\{11\}\cup E[14,x+10]\cup I[x+12,\infty),&x\ge14\text{ 偶数}.
\end{cases}
\]

全 \(x\ge1,R\ge0\) について

\[
H(R;(x,1);10)=
\begin{cases}
2,&R\in T_{10}^{(1)}(x),\\
1,&R\in P_{10}^{(1)}(x),\\
0,&\text{それ以外}.
\end{cases}
\]

一般tailは

\[
R\ge x+12\implies H(R;(x,1);10)=(x+1)\bmod2.
\]

## 証明の要点

\(R\ge1,x\ge2\) の選択肢は

\[
A=H(R-1;(x-1,1);10),\quad
B=H(R-1;(x);11),\quad
C=1\oplus H(R-1;(x,1);9).
\]

Aはx外帰納、BはK0832の単一トークンz=11公式、CはK0985で与えられる。x=1ではA手が存在せず、2本の除去手は同一の(1);11子に合流する。

全xのA/B/C署名帯は証明報告に列挙した。mex対応は 01→2, 23→0, 03→1, 02→1, 023→1, 123→0, 0→1, 1→0。Theorem Tにより奇数Rの親は値2以下、偶数Rの親は値1以下であり、署名表のmexが上記のT/Pを与える。

x=9の追加点11は高さのみ縮約のz=x枠（O[1,2x−1]型値2のR≤11制限）、x=10（=z）は冪ゼロ平坦化 P=I[11,∞)、x=11（=z+1）はP={11}有限、x=12（=z+2）は掃引行（掃引帯O[13,23]=O[pin,x+y+z]、pin=2y+z+1=13）、x=13はA子が掃引行を横切る移行行（署名のみ異なる）、x≥14偶/x≥15奇では帯境界がxの一次式で一様に成立する。値1の基底点はz+1=11、帯開始はz+4=14で偶奇はzとともに反転する。従って外帰納が閉じる。

## 限界

本項は抽象残余ゲームのz=10,y=1切片のみ。z=10のy=2..5は未証明、y≥6はK1002の候補のまま。z≥11・全高さを統合する2トークン値2位置の一般式、標準二次元盤の固定幅・q点安定化長は未解決。
