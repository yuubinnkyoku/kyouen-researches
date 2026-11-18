---
id: K0984
title: 2トークン残余ゲーム z=8・y=2境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z8 y2 boundary slice]
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームHの再帰、Theorem T、一般tail定理を使用する
- type: depends_on
  target: K0983
  note: B子の評価にz=8,y=1境界切片を使用する
- type: depends_on
  target: K0978
  note: C子の評価にz=7,y=2境界切片を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z8-y2-boundary-20261119/report.md
  role: proof
  note: 固定z=8・y=2・全x>=2,R>=0のGrundy値0/1/2をx外帰納とA/B/C署名帯表で分類する全称証明
- path: research/experiments/vertical-fiber-two-token-z8-y2-boundary-20261119/verify_z8_y2.py
  role: verifier
  note: 独立した順序付き・正準化直接mex再帰、アンカー照合、全x署名帯表とTheorem Tを監査する検証器
- path: research/experiments/vertical-fiber-two-token-z8-y2-boundary-20261119/output/audit.json
  role: data
  note: 6,134,940照合・不一致0・二回実行byte-identical
- path: research/log/2026-11-19-vertical-fiber-two-token-z8-y2-boundary.md
  role: log
  note: K0983/K0978を用いたz=8,y=2切片の発見・外帰納証明・独立監査・限界
date: 2026-11-19
scope: >-
  κ=1残余ゲームH(R;(x,y);z)の2トークン族における固定高さz=8、y=2、全x>=2・全R>=0。Grundy値0/1/2を完全分類する。
evidence: >-
  xに関する外帰納。x>=3ではA子を帰納仮説、B子をK0983のz=8,y=1公式、C子をK0978のz=7,y=2公式で評価する。x=2では二つの減少手が同一の(2,1)子に合流する。x=2..12の個別署名帯とx>=13奇/x>=14偶の定常署名帯で全Rを被覆し、Theorem Tのmex規則で閉じる。tailはR>=x+11でH=(x+2) mod 2。独立有限監査は6,134,940照合・不一致0であり、全称性の根拠は外帰納と署名表である。
---

## 定理

値2位置を \(T_8^{(2)}(x)\)、値1位置を \(P_8^{(2)}(x)\) とする。\(O[a,b]\) は区間内の奇数、\(E[a,b]\) は偶数、\(I[a,\infty)\) は \(a\) 以上の全整数である。

\[
T_8^{(2)}(x)=
\begin{cases}
\{1,3\},&x=2,\\
\{1,3,5\},&x\in\{3,4\},\\
\{1,3,5,7\},&x=5,\\
\{1,3,5,7,9\},&x=6,\\
\{1,3,5,7\},&x=7,\\
\{1,3,5,7,11\},&x=8,\\
\{1,3,5,7\},&x\in\{9,10\},\\
\{1,3,5,7\}\cup O[13,21],&x=11,\\
\{1,3,5,7,13\},&x\ge12.
\end{cases}
\]

\[
P_8^{(2)}(x)=
\begin{cases}
\varnothing,&x\in\{2,4,6\},\\
I[6,\infty),&x=3,\\
I[8,\infty),&x=5,\\
\{9\}\cup I[11,\infty),&x\in\{7,9\},\\
\{9\},&x=8,\\
\{9,11\},&x=10,\\
\{9,11\}\cup E[14,20]\cup I[22,\infty),&x=11,\\
\{9,11\}\cup E[14,x+10],&x\ge12\text{ 偶数},\\
\{9,11\}\cup E[14,x+9]\cup I[x+11,\infty),&x\ge13\text{ 奇数}.
\end{cases}
\]

全 \(x\ge2,R\ge0\) について

\[
H(R;(x,2);8)=
\begin{cases}
2,&R\in T_8^{(2)}(x),\\
1,&R\in P_8^{(2)}(x),\\
0,&\text{それ以外}.
\end{cases}
\]

一般tailは

\[
R\ge x+11\implies H(R;(x,2);8)=(x+2)\bmod2.
\]

## 証明の要点

\(R\ge1,x\ge3\) の選択肢は

\[
A=H(R-1;(x-1,2);8),\quad
B=H(R-1;(x,1);8),\quad
C=1\oplus H(R-1;(x,2);7).
\]

Aはx外帰納、BはK0983、CはK0978で与えられる。x=2では二つの減少手が同じ(2,1)子に合流し、A=B=K0983の値となる。

全xのA/B/C署名帯は証明報告に列挙した。mex対応は 01→2, 23→0, 03→1, 0→1, 1→0, 12→0, 023→1, 123→0, 02→1。Theorem Tにより奇数Rの親は値2以下、偶数Rの親は値1以下であり、署名表のmexが上記のT/Pを与える。

x=12はA子がK0983のx=11例外帯を引き継ぐため署名だけが独立行になるが、値の閉形式はx>=12の定常式に合流する。x>=13奇数・x>=14偶数では帯境界がxの一次式で一様に成立する。従って外帰納が閉じる。

## 限界

本項は抽象残余ゲームのz=8,y=2切片のみ。z=8,y>=3、z>=9、全高さを統合する2トークン値2位置の一般式、標準二次元盤の固定幅・q点安定化長は未解決。
