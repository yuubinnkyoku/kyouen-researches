---
id: K1006
title: 2トークン残余ゲーム z=10・y=4境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z10 y4 boundary slice]
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームHの再帰、Theorem T、単一トークン全z公式、tail定理、高さのみ縮約を使用する
- type: depends_on
  target: K1005
  note: B子の評価にz=10,y=3境界切片を使用する
- type: depends_on
  target: K0990
  note: C子の評価にz=9,y=4境界切片を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z10-y4-boundary-20261119/report.md
  role: proof
  note: 固定z=10・y=4・全x>=4,R>=0のGrundy値0/1/2をx外帰納とA/B/C署名帯表で分類する全称証明
- path: research/experiments/vertical-fiber-two-token-z10-y4-boundary-20261119/verify_z10_y4.py
  role: verifier
  note: 独立実装の直接mex再帰、降順正準化第2実装、アンカー照合、全x署名帯表とTheorem Tと高さのみ縮約を監査する検証器
- path: research/experiments/vertical-fiber-two-token-z10-y4-boundary-20261119/output/audit.json
  role: data
  note: 8,187,862照合・不一致0・二回実行byte-identical
- path: research/log/2026-11-19-vertical-fiber-two-token-z10-y4-boundary.md
  role: log
  note: K1005/K0990を用いたz=10,y=4切片の発見・外帰納証明・独立監査・限界
scope: >-
  κ=1残余ゲームH(R;(x,y);z)の2トークン族における固定高さz=10、y=4、全x>=4・全R>=0。
  Grundy値0/1/2を完全分類する。
evidence: >-
  xに関する外帰納。x>=5ではA子を帰納仮説、B子をK1005のz=10,y=3公式、C子をK0990の
  z=9,y=4公式で評価する。x=4では2つのトークン減少手が同一の(3,4);10子に合流する。
  x=4..16の個別署名帯とx>=18偶/x>=17奇の定常署名帯で全Rを被覆し、Theorem Tのmex規則で
  閉じる。R<=11は高さのみ縮約でv_single(x+4,10,R)に一致し並走レーンの低残余帯と接続、
  tailはR>=x+15でH=(x+4) mod 2。独立有限監査は8,187,862照合・不一致0であり、
  全称性の根拠は外帰納と署名表である。
---

## 定理

値2位置を \(T_{10}^{(4)}(x)\)、値1位置を \(P_{10}^{(4)}(x)\) とする。\(O[a,b]\) は区間内の奇数、\(E[a,b]\) は偶数、\(I[a,\infty)\) は \(a\) 以上の全整数である。

\[
T_{10}^{(4)}(x)=
\begin{cases}
\{1,3,5,7\},&x=4,\\
\{1,3,5,7,9\},&x=5,\\
\{1,3,5,7,9,11,13\},&x=6,\\
\{1,3,5,7,9\},&x\in\{7,9,10,11,13,14\},\\
\{1,3,5,7,9,15\},&x=8,\\
\{1,3,5,7,9,17\},&x=12,\\
\{1,3,5,7,9\}\cup O[19,29],&x=15,\\
\{1,3,5,7,9,19\},&x\ge16.
\end{cases}
\]

\[
P_{10}^{(4)}(x)=
\begin{cases}
\varnothing,&x\in\{4,6\},\\
I[10,\infty),&x=5,\\
\{11,13,15\}\cup I[16,\infty),&x\in\{7,9\},\\
\{11,13\},&x=8,\\
\{11,13,15\},&x\in\{10,12\},\\
\{11,13,15,17\}\cup I[18,\infty),&x\in\{11,13\},\\
\{11,13,15,17\},&x=14,\\
\{11,13,15,17\}\cup E[20,30]\cup I[31,\infty),&x=15,\\
\{11,13,15,17\}\cup E[20,x+14],&x\ge16\text{ 偶数},\\
\{11,13,15,17\}\cup E[20,x+15]\cup I[x+16,\infty),&x\ge17\text{ 奇数}.
\end{cases}
\]

全 \(x\ge4,R\ge0\) について

\[
H(R;(x,4);10)=
\begin{cases}
2,&R\in T_{10}^{(4)}(x),\\
1,&R\in P_{10}^{(4)}(x),\\
0,&\text{それ以外}.
\end{cases}
\]

一般tailは

\[
R\ge x+15\implies H(R;(x,4);10)=(x+4)\bmod2.
\]

## 証明の要点

\(R\ge1,x\ge5\) の選択肢は

\[
A=H(R-1;(x-1,4);10),\quad
B=H(R-1;(x,3);10),\quad
C=1\oplus H(R-1;(x,4);9).
\]

Aはx外帰納、BはK1005、CはK0990で与えられる。x=4ではA手とB手が同一の(3,4);10子に合流する。

全xのA/B/C署名帯は証明報告に列挙した。mex対応は 01→2, 23→0, 03→1, 02→1, 023→1, 123→0, 12→0, 0→1, 1→0。Theorem Tにより奇数Rの親は値2以下、偶数Rの親は値1以下であり、署名表のmexが上記のT/Pを与える。

x=6（高さh=x+y=10=z）は{11,13}の2点前倒し（y=3 と同じく2点）、x=12は前倒し生存点（x=y+8、R=2y+9=17）、x=8は点15=2y+7の追加行、x=15（=z+y+1）は掃引行（掃引帯O[19,29]=O[pin,x+y+z]、pin=2y+z+[z偶]=19）、x=16はA子が掃引帯を横切る移行行（偶帯E[20,30]全幅の署名02だが値表は偶行定常と同一）、x≥18偶/x≥17奇では帯境界がxの一次式で一様に成立する。値1の基底点は{11,13,15,17}={z+1,z+3,z+5,z+7}の4点（基底点y個仮説）、帯開始はz+2y+2=20で偶奇はzの偶奇（E帯）で決まり、I帯はx奇数行のみ（tail値(x+y) mod 2が1の行）。R≤11の列は高さのみ縮約v_single(x+4,10,R)に一致し並走レーン出版のz=10低残余帯と完全一致する。tailはR>=x+15でH=(x+4) mod 2。従って外帰納が閉じる。

## 限界

本項は抽象残余ゲームのz=10,y=4切片のみ。z=10のy=5はK1007で、y=6はK1008で全称証明済み、y>=7はK1002の候補のまま（y=7行の三子B子=K1008・C子=1 xor K0997〔z=9,y=7切片・全称証明済み〕で着手可能）。z>=11・全高さを統合する2トークン値2位置の一般式、標準二次元盤の固定幅・q点安定化長は未解決。
