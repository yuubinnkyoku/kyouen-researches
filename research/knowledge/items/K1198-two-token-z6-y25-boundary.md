---
id: K1198
title: 2トークン残余ゲーム z=6・y=25切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z6 y25 full Grundy slice]
relations:
- type: depends_on
  target: K0832
  note: A/B/C残余再帰、Theorem T、一般tail定理を使用する
- type: depends_on
  target: K0873
  note: C子の評価にz=5の全Grundy公式を使用する
- type: depends_on
  target: K0918
  note: B子とx=25境界のA子をz=6,y=24全Grundy公式で評価する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z6-y25-boundary-20261118/report.md
  role: proof
  note: z=6,y=25切片の全x,R分類、過渡署名表、定常子式、R強帰納証明
- path: research/experiments/vertical-fiber-two-token-z6-y25-boundary-20261118/verify_z6_y25.py
  role: verifier
  note: 順序付き・降順正準化の二方式直接再帰、z=5/y=24アンカー、全署名・mex・tailを独立監査
- path: research/experiments/vertical-fiber-two-token-z6-y25-boundary-20261118/output/audit.json
  role: data
  note: 6,333,788検査・不一致0・二回実行byte-identical。有限監査であり全称証明とは区別する
- path: research/log/2026-11-18-vertical-fiber-two-token-z6-y25-boundary.md
  role: log
  note: 最新main・未解決事項との照合、z=6,y=25切片の証明・監査・限界
scope: >-
  κ=1残余ゲームH(R;(x,25);6)の2トークン族、固定高さz=6、y=25、全x≥25・全R≥0。Grundy値0/1/2を完全分類する。
evidence: >-
  Rに関する強帰納。x=25のA子は正準化後に(25,24)となるためK0918、x≥26のA子は同じy=25切片の帰納仮説、B子はK0918、C子はK0873で評価する。K0832のTheorem Tにより奇数親の子値は{0,1}、偶数親の親値は高々1。x=25..33の過渡A/B/C署名表とx≥34の偶奇別定常子式から全署名を決定し、R≥x+32は一般tail定理H=(x+25) mod 2で閉じる。独立有限監査は6,333,788検査で不一致0、二回実行byte-identical。有限監査は証明の代わりではなく、全称性は署名表・Theorem T・tail定理・R強帰納による。
---

## 命題・範囲

\(O[a,b]\) をa以上b以下の奇数、\(E[a,b]\) を同範囲の偶数、\([a,\infty)\) を整数の無限区間とする。全ての \(x\ge25,R\ge0\) について

\[
H(R;(x,25);6)=
\begin{cases}
2,&R\in T_{25}(x),\\
1,&R\in P_{25}(x),\\
0,&\text{otherwise},
\end{cases}
\]

ただし
\[
T_{25}(x)=\{1,3,5\}\cup
\begin{cases}
\{53\}&x=25,\\
\{55\}&x=29,\\
\{57,59,61,63\}&x=32,\\
\{57\}&x\ge33,\\
\varnothing&\text{otherwise},
\end{cases}
\]

\[
P_{25}(x)=
\begin{cases}
O[7,51],&x=25,\\
O[7,57]\cup E[54,56]\cup[58,\infty),&x=26,\\
O[7,53],&x=27,\\
O[7,59]\cup E[56,58]\cup[60,\infty),&x=28,\\
O[7,53],&x=29,\\
O[7,61]\cup E[56,60]\cup[62,\infty),&x=30,\\
O[7,55],&x=31,\\
O[7,55]\cup E[58,62]\cup[64,\infty),&x=32,\\
O[7,55]\cup E[58,64],&x=33,\\
O[7,55]\cup E[58,x+30]\cup[x+32,\infty),&x\ge34\text{ 偶数},\\
O[7,55]\cup E[58,x+31],&x\ge35\text{ 奇数}.
\end{cases}
\]
また一般tailは
\[
R\ge x+32\implies H(R;(x,25);6)=(x+25)\bmod2.
\]

## 現在の根拠と限界

A/B/C再帰は \(A=H(R-1;(x-1,25);6)\)、\(B=H(R-1;(x,24);6)\)、\(C=1\oplus H(R-1;(x,25);5)\)。K0918/K0873の既証明公式、K0832のTheorem T、一般tail定理を使う。過渡域x=25..33の全署名と定常域x≥34の偶奇別子式を明示し、残容量Rの強帰納で全称性を得る。値2位置はK0832の3族予想のz=6,y=25特殊化と一致するが、3族予想全体は未証明。

独立監査は6,333,788検査、不一致0、二回実行byte-identical。対象は抽象κ=1残余ゲームのz=6,y=25切片に限る。z=6,y≥35、z≥7の全Grundy分類、全高さの値2位置一般式、標準二次元共円ゲームの固定幅・q点版の真の安定化長は未解決。
