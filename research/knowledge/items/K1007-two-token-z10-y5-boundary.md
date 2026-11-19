---
id: K1007
title: 2トークン残余ゲーム z=10・y=5境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z10 y5 boundary slice]
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームHの再帰、Theorem T、単一トークン全z公式、tail定理、高さのみ縮約を使用する
- type: depends_on
  target: K1006
  note: B子の評価にz=10,y=4境界切片を使用する
- type: depends_on
  target: K0992
  note: C子の評価にz=9,y=5境界切片を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z10-y5-boundary-20261119/report.md
  role: proof
  note: 固定z=10・y=5・全x>=5,R>=0のGrundy値0/1/2をx外帰納とA/B/C署名帯表で分類する全称証明
- path: research/experiments/vertical-fiber-two-token-z10-y5-boundary-20261119/verify_z10_y5.py
  role: verifier
  note: 独立実装の直接mex再帰、降順正準化第2実装、B(K1006)/C(K0992)アンカー照合、全x署名帯表とTheorem Tと高さのみ縮約を監査する検証器
- path: research/experiments/vertical-fiber-two-token-z10-y5-boundary-20261119/output/audit.json
  role: data
  note: 8,193,568照合・不一致0・二回実行byte-identical
- path: research/experiments/vertical-fiber-two-token-z10-y5-boundary-20261119/agree_k1002_y5.py
  role: verifier
  note: 本項の全称式とK1002一様候補のy=5スライス整合監査。2,073,342照合・グリッド不一致はちょうど対角線2点(5,11),(5,13)（候補1・実測2）
- path: research/experiments/vertical-fiber-two-token-z10-y5-boundary-20261119/output/agree_audit.json
  role: data
  note: 整合監査の結果JSON・二回実行byte-identical
- path: research/log/2026-11-19-vertical-fiber-two-token-z10-y5-boundary.md
  role: log
  note: K1006/K0992を用いたz=10,y=5切片の発見・外帰納証明・独立監査・K1002候補との整合・限界
scope: >-
  κ=1残余ゲームH(R;(x,y);z)の2トークン族における固定高さz=10、y=5、全x>=5・全R>=0。
  Grundy値0/1/2を完全分類する。
evidence: >-
  xに関する外帰納。x>=6ではA子を帰納仮説、B子をK1006のz=10,y=4公式、C子をK0992の
  z=9,y=5公式で評価する。x=5では2つのトークン減少手が同一の(5,4);10子に合流する。
  x=5..17の個別署名帯とx>=18偶/x>=19奇の定常署名帯で全Rを被覆し、Theorem Tのmex規則で
  閉じる。R<=11は高さのみ縮約でv_single(x+5,10,R)に一致し並走レーンの低残余帯と接続、
  tailはR>=x+16でH=(x+5) mod 2。独立有限監査は8,193,568照合・不一致0であり、
  全称性の根拠は外帰納と署名表である。
---

## 定理

値2位置を \(T_{10}^{(5)}(x)\)、値1位置を \(P_{10}^{(5)}(x)\) とする。\(O[a,b]\) は区間内の奇数、\(E[a,b]\) は偶数、\(I[a,\infty)\) は \(a\) 以上の全整数である。

\[
T_{10}^{(5)}(x)=
\begin{cases}
\{1,3,5,7,9,11,13,15\},&x=5,\\
\{1,3,5,7,9\},&x\in\{6,7,8,10,11,12,14,15\},\\
\{1,3,5,7,9,17\},&x=9,\\
\{1,3,5,7,9,19\},&x=13,\\
\{1,3,5,7,9\}\cup O[21,31],&x=16,\\
\{1,3,5,7,9,21\},&x\ge17.
\end{cases}
\]

\[
P_{10}^{(5)}(x)=
\begin{cases}
\varnothing,&x=5,\\
\{11,13,15\}\cup I[16,\infty),&x=6,\\
\{11,13,15\},&x\in\{7,9,13\},\\
\{11,13,15,17\}\cup I[18,\infty),&x\in\{8,10\},\\
\{11,13,15,17\},&x\in\{11,13\},\\
\{11,13,15,17,19\}\cup I[20,\infty),&x\in\{12,14\},\\
\{11,13,15,17,19\},&x=15,\\
\{11,13,15,17,19\}\cup E[22,x+16]\cup I[x+17,\infty),&x\ge16\text{ 偶数},\\
\{11,13,15,17,19\}\cup E[22,x+15],&x\ge17\text{ 奇数}.
\end{cases}
\]

全 \(x\ge5,R\ge0\) について

\[
H(R;(x,5);10)=
\begin{cases}
2,&R\in T_{10}^{(5)}(x),\\
1,&R\in P_{10}^{(5)}(x),\\
0,&\text{それ以外}.
\end{cases}
\]

一般tailは

\[
R\ge x+16\implies H(R;(x,5);10)=(x+5)\bmod2.
\]

## 証明の要点

\(R\ge1,x\ge6\) の選択肢は

\[
A=H(R-1;(x-1,5);10),\quad
B=H(R-1;(x,4);10),\quad
C=1\oplus H(R-1;(x,5);9).
\]

Aはx外帰納、BはK1006、CはK0992で与えられる。x=5では2つのトークン減少手が同一の(5,4);10子に合流する。

全xのA/B/C署名帯は証明報告に列挙した。mex対応は 01→2, 23→0, 03→1, 02→1, 023→1, 123→0, 12→0, 0→1, 1→0。Theorem Tにより奇数Rの親は値2以下、偶数Rの親は値1以下であり、署名表のmexが上記のT/Pを与える。

x=5（高さh=x+y=10=z）は値2が{11,13,15}の3点前倒し（h=z行の追加点個数はy=1:1・y=2:1・y=3:2・y=4:2に対し3点で、仮説ceil(y/2)と整合）、x=9は点17=2y+7の追加行（d=4。y=4の点15=2y+7もd=4行で安定）、x=13は前倒し生存点（x=y+8、R=2y+9=19）、x=16（=z+y+1）は掃引行（掃引帯O[21,31]=O[pin,x+y+z]、pin=2y+z+[z偶]=21）、x=17はA子が掃引帯を横切る移行行（偶帯E[22,32]全幅の署名02だが値表は奇行定常と同一）、x≥18偶/x≥19奇では帯境界がxの一次式で一様に成立する。値1の基底点は{11,13,15,17,19}={z+1,z+3,z+5,z+7,z+9}の5点（基底点y個仮説{z+1,…,z+2y−1}をy=5でも満たす）、帯開始はz+2y+2=22で偶奇はzの偶奇（E帯）で決まり、I帯はx偶数行のみ（tail値(x+y) mod 2が1の行。y=1,3と同じ向き）。R≤11の列は高さのみ縮約v_single(x+5,10,R)に一致し並走レーン出版のz=10低残余帯と完全一致する。tailはR>=x+16でH=(x+5) mod 2。従って外帰納が閉じる。

## K1002 一様候補との整合

本項の全称式と K1002 の y>=6 一様候補（d=0,4,8の前倒し点2y+5,2y+7,2y+9・d=11掃引帯O[2y+11,S+10]・d>=12定常点2y+11・P・tail R>=S+11でS mod 2）を y=5 スライス上で機械照合すると（agree_k1002_y5.py、総照合2,073,342）、不一致は対角線 x=5 の \(R=11,13\) のちょうど2点である（K1002候補は1、実測は2）。対角線のh=z行は前倒し3点 \(\{11,13,15\}\) を持つが、うち \(15=2y+5\) は候補自身の d=0 格子点であり、掃引行・移行行・定常行・I帯行の全帯構造とtailは候補と一致する。h=z行は y>=6 では x+y>=12>10 で定義域 x>=y に現れないため、K1002のy>=6適用域限定の根拠が本項により全称的に確定した。

## 限界

本項は抽象残余ゲームのz=10,y=5切片のみ。y=6はK1008で（agree_k1002_y6.py総2,073,300照合・不一致0点）、y=7はK1009で全称証明済み（agree_k1002_y7.py総2,073,257照合・不一致0点）、y=8はK1010で全称証明済み（検証器統合監査のK1002整合グリッド2,050,797照合・不一致0点）、y>=9はK1002の一様式候補のまま（y=9行以降のC子=1 xor K1001〔z=9,y>=9一様式・全称証明済み〕で着手可能）。z>=11・全高さを統合する2トークン値2位置の一般式、標準二次元盤の固定幅・q点安定化長は未解決。
