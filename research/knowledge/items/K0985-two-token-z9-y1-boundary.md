---
id: K0985
title: 2トークン残余ゲーム z=9・y=1境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z9 y1 boundary slice]
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームHの再帰、Theorem T、単一トークン全z公式、tail定理、高さのみ縮約を使用する
- type: depends_on
  target: K0983
  note: C子の評価にz=8,y=1境界切片を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z9-y1-boundary-20261119/report.md
  role: proof
  note: 固定z=9・y=1・全x>=1,R>=0のGrundy値0/1/2をx外帰納とA/B/C署名帯表で分類する全称証明
- path: research/experiments/vertical-fiber-two-token-z9-y1-boundary-20261119/verify_z9_y1.py
  role: verifier
  note: 独立実装の直接mex再帰、アンカー照合、全x署名帯表とTheorem Tを監査する検証器
- path: research/experiments/vertical-fiber-two-token-z9-y1-boundary-20261119/output/audit.json
  role: data
  note: 4,165,460照合・不一致0・二回実行byte-identical
- path: research/log/2026-11-19-vertical-fiber-two-token-z9-y1-boundary.md
  role: log
  note: K0983を用いたz=9,y=1切片の発見・外帰納証明・独立監査・限界
date: 2026-11-19
scope: >-
  κ=1残余ゲームH(R;(x,y);z)の2トークン族における固定高さz=9、y=1、全x>=1・全R>=0。Grundy値0/1/2を完全分類する。
evidence: >-
  xに関する外帰納。x>=2ではA子を帰納仮説、B子をK0832の単一トークンz=10公式、C子をK0983のz=8,y=1公式で評価する。x=1では二つの除去手が同一の(1);10子に合流する。x=1..12の個別署名帯とx>=13奇/x>=14偶の定常署名帯で全Rを被覆し、Theorem Tのmex規則で閉じる。tailはR>=x+11でH=(x+1) mod 2。独立有限監査は4,165,460照合・不一致0であり、全称性の根拠は外帰納と署名表である。
---

## 定理

値2位置を \(T_9^{(1)}(x)\)、値1位置を \(P_9^{(1)}(x)\) とする。\(O[a,b]\) は区間内の奇数、\(E[a,b]\) は偶数、\(I[a,\infty)\) は \(a\) 以上の全整数である。

\[
T_9^{(1)}(x)=
\begin{cases}
\{1\},&x=1,\\
\{1,3\},&x\in\{2,3\},\\
\{1,3,5\},&x\in\{4,5\},\\
\{1,3,5,7\},&x\in\{6,7\},\\
\{1,3,5,7,9\},&x\in\{8,9\},\\
\{1,3,5,7,9,11\}\cup O[13,21],&x=11,\\
\{1,3,5,7,9,11\},&x=10\text{ または }x\ge12.
\end{cases}
\]

\[
P_9^{(1)}(x)=
\begin{cases}
\varnothing,&x\in\{1,3,5,7\},\\
I[4,\infty),&x=2,\\
I[6,\infty),&x=4,\\
I[8,\infty),&x=6,\\
I[10,\infty),&x=8,\\
\{10\},&x\in\{9,11\},\\
\{10,12\}\cup I[13,\infty),&x=10,\\
\{10\}\cup O[13,x+10],&x\ge13\text{ 奇数},\\
\{10\}\cup O[13,x+11]\cup I[x+12,\infty),&x\ge12\text{ 偶数}.
\end{cases}
\]

全 \(x\ge1,R\ge0\) について

\[
H(R;(x,1);9)=
\begin{cases}
2,&R\in T_9^{(1)}(x),\\
1,&R\in P_9^{(1)}(x),\\
0,&\text{それ以外}.
\end{cases}
\]

一般tailは

\[
R\ge x+11\implies H(R;(x,1);9)=(x+1)\bmod2.
\]

## 証明の要点

\(R\ge1,x\ge2\) の選択肢は

\[
A=H(R-1;(x-1,1);9),\quad
B=H(R-1;(x);10),\quad
C=1\oplus H(R-1;(x,1);8).
\]

Aはx外帰納、BはK0832の単一トークンz=10公式、CはK0983で与えられる。x=1ではA手が存在せず、2本の除去手は同一の(1);10子に合流する。

全xのA/B/C署名帯は証明報告に列挙した。mex対応は 01→2, 23→0, 03→1, 02→1, 13→0, 12→0, 0→1, 1→0, 023→1, 123→0。Theorem Tにより奇数Rの親は値2以下、偶数Rの親は値1以下であり、署名表のmexが上記のT/Pを与える。

x=12はA子がx=11行の掃引帯を署名（{1,2}）に引き継ぐが、mex後の値はx>=14偶数の定常式に合流する。x>=13奇数・x>=14偶数では帯境界がxの一次式で一様に成立する。値1の基底点はz+1=10、帯開始はz+4=13で偶奇はzとともに反転する。従って外帰納が閉じる。

## 限界

本項は抽象残余ゲームのz=9,y=1切片のみ。z=9のy>=2、z>=10、全高さを統合する2トークン値2位置の一般式、標準二次元盤の固定幅・q点安定化長は未解決。
