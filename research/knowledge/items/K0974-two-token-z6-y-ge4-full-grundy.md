---
id: K0974
title: 2トークン残余ゲーム z=6・全y≥4の全Grundy閉形式
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z6 all y>=4 full Grundy classification]
relations:
- type: depends_on
  target: K0832
  note: A/B/C残余再帰、Theorem T、一般tail定理を使用する
- type: depends_on
  target: K0873
  note: C子の評価にz=5の全Grundy公式を使う
- type: depends_on
  target: K0880
  note: y=4の全x・全R基底を使う
- type: generalizes
  target: K0973
  note: y=36の個別切片を含む全y>=4の一般定理
artifacts:
- path: research/experiments/vertical-fiber-two-token-z6-y-ge4-20261119/report.md
  role: proof
  note: y=4基底とx+y強帰納による全y>=4の全Grundy分類証明、全差のA/B/C署名表
- path: research/experiments/vertical-fiber-two-token-z6-y-ge4-20261119/verify_z6_y_ge4.py
  role: verifier
  note: y=4基底、y>=5の帰納署名・mex、tail、順序付き/正準化直接再帰を照合する独立有限監査器
- path: research/experiments/vertical-fiber-two-token-z6-y-ge4-20261119/output/audit.json
  role: data
  note: 4,754,888検査・不一致0・二回実行byte-identical。有限監査であり全称証明とは区別する
- path: research/log/2026-11-19-vertical-fiber-two-token-z6-y-ge4.md
  role: log
  note: 最新main・未解決事項との照合、y方向一般化の発見・証明・監査・限界
date: 2026-11-19
scope: >-
  κ=1残余ゲームH(R;(x,y);6)の2トークン族、全x>=y>=4・全R>=0。Grundy値0/1/2を全て閉形式で分類する。
evidence: >-
  y=4はK0880の全称定理。y>=5はS=x+yに関する強帰納。A子(x-1,y)とB子(x,y-1)は正準化後も最小トークン4以上・和S-1、対角d=0ではA/Bが同一子へ合流する。C子はK0873のz=5全公式。K0832のTheorem Tで奇数親の子値は{0,1}、偶数親の親値は高々1。d=0..8とd>=9のA/B/C署名表で全1<=R<=S+6を覆い、R>=S+7はtail H=S mod 2で閉じる。独立監査はy=4基底2,152,766点、署名・mex各2,120,596点、直接再帰1,170呼び出し、tail480,356点で不一致0、二回実行byte-identical。有限監査は証明の代わりではなく、全称性はy=4基底・S強帰納・署名表・既証明アンカーによる。
---

## 定理

\(S=x+y\)、\(d=x-y\) とし、\(O[a,b]\)・\(E[a,b]\) をそれぞれ区間内の奇数・偶数集合とする。全 \(x\ge y\ge4,R\ge0\) で
\[
H(R;(x,y);6)=
\begin{cases}
2,&R\in T_y(x),\\
1,&R\in P_y(x),\\
0,&\text{それ以外},
\end{cases}
\]
ただし
\[
T_y(x)=\{1,3,5\}\cup
\begin{cases}
\{2y+3\}&d=0,\\
\{2y+5\}&d=4,\\
\{2y+7,2y+9,2y+11,2y+13\}&d=7,\\
\{2y+7\}&d\ge8,\\
\varnothing&\text{その他},
\end{cases}
\]
\[
P_y(x)=
\begin{cases}
O[7,2y+1]&d=0,\\
O[7,\infty)\cup E[2y+4,\infty)&d=1,\\
O[7,2y+3]&d=2,\\
O[7,\infty)\cup E[2y+6,\infty)&d=3,\\
O[7,2y+3]&d=4,\\
O[7,\infty)\cup E[2y+6,\infty)&d=5,\\
O[7,2y+5]&d=6,\\
O[7,2y+5]\cup E[2y+8,\infty)\cup O[S+8,\infty)&d\ge7\text{ odd},\\
O[7,2y+5]\cup E[2y+8,S+6]&d\ge8\text{ even}.
\end{cases}
\]
tailは
\[
R\ge S+7\implies H(R;(x,y);6)=S\bmod2.
\]

## 証明の要点

K0880のy=4全切片を基底とし、y≥5ではS=x+yに関する強帰納を行う。A/B子はSを1減らしてy≥4に留まり、C子はK0873のz=5公式で評価できる。d=0ではA/B子が正準化後に一致する。K0832のTheorem Tにより、奇数親では子値が{0,1}、偶数親では親値が高々1となるため、全差dの署名表からmexが一意に決まる。tailはK0832の一般式で閉じる。完全な署名表は証明報告を参照。

## 現在の根拠と限界

本定理はy=4を含む全y≥4を一括分類する。K0877・K0878・K0879のy=1,2,3切片と合わせると、z=6の2トークン族は全y≥1で全Grundy値が証明済みであり、K0832の3族値2位置予想のz=6特殊化も全域で証明済みとなる。y=3の対角切片にはR=7の追加値2位置があるため、本定理の一様式の適用下限y=4は鋭い。z≥7の全Grundy分類、全高さを統合する値2位置一般式、標準二次元共円ゲームの固定幅・q点版の真の安定化長は未解決。
