---
id: K0940
title: 2トークン残余ゲーム z=6・y=27切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z6 y27 full Grundy slice]
relations:
- type: depends_on
  target: K0832
  note: A/B/C残余再帰、Theorem T、一般tail定理を使用する
- type: depends_on
  target: K0873
  note: C子の評価にz=5の全Grundy公式を使用する
- type: depends_on
  target: K0938
  note: B子とx=27境界のA子をz=6,y=26全Grundy公式で評価する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z6-y27-boundary-20261118/report.md
  role: proof
  note: z=6,y=27切片の全x,R分類、全選択肢署名表、R強帰納証明
- path: research/experiments/vertical-fiber-two-token-z6-y27-boundary-20261118/verify_z6_y27.py
  role: verifier
  note: 順序付き・降順正準化の二方式直接再帰、y=26/z=5アンカー、全署名・mex・tailを独立監査
- path: research/experiments/vertical-fiber-two-token-z6-y27-boundary-20261118/output/audit.json
  role: data
  note: 6,389,417検査・不一致0・二回実行byte-identical。有限監査であり全称証明とは区別する
- path: research/log/2026-11-18-vertical-fiber-two-token-z6-y27-boundary.md
  role: log
  note: 最新main・未解決事項との照合、z=6,y=27切片の証明・監査・限界
scope: >-
  κ=1残余ゲームH(R;(x,27);6)の2トークン族、固定高さz=6、y=27、全x≥27・全R≥0。Grundy値0/1/2を完全分類する。
evidence: >-
  Rに関する強帰納。x=27のA子は正準化後に(27,26)となるためK0938、x≥28のA子は同じy=27切片の帰納仮説、B子はK0938、C子はK0873で評価する。K0832のTheorem Tにより奇数親の子値は{0,1}、偶数親の親値は高々1。x=27..35の過渡署名表とx≥36 even/x≥37 oddの定常署名表から全署名を決定し、R≥x+34は一般tail定理H=(x+27) mod 2で閉じる。独立有限監査は6,389,417検査で不一致0、二回実行byte-identical。有限監査は証明の代わりではなく、全称性は署名表・Theorem T・tail定理・R強帰納による。
---

## 命題・範囲

\(O[a,b]\) をa以上b以下の奇数、\(E[a,b]\) を同範囲の偶数、\([a,\infty)\) を整数の無限区間とする。全ての \(x\ge27,R\ge0\) について

\[
H(R;(x,27);6)=
\begin{cases}
2,&R\in T_{27}(x),\\
1,&R\in P_{27}(x),\\
0,&\text{otherwise},
\end{cases}
\]

ただし

\[
T_{27}(x)=\{1,3,5\}\cup
\begin{cases}
\{57\}&x=27,\\
\{59\}&x=31,\\
\{61,63,65,67\}&x=34,\\
\{61\}&x\ge35,\\
\varnothing&x\in\{28,29,30,32,33\},
\end{cases}
\]

\[
P_{27}(x)=
\begin{cases}
O[7,55],&x=27,\\
O[7,55]\cup[57,\infty),&x=28,\\
O[7,57],&x=29,\\
O[7,57]\cup[59,\infty),&x=30,\\
O[7,57],&x=31,\\
O[7,59]\cup[60,\infty),&x=32,\\
O[7,59],&x=33,\\
O[7,59]\cup E[62,\infty)\cup O[69,\infty),&x=34,\\
O[7,59]\cup E[62,x+33],&x\ge35\text{ odd},\\
O[7,59]\cup E[62,\infty)\cup O[x+35,\infty),&x\ge36\text{ even}.
\end{cases}
\]

一般tailは

\[
R\ge x+34\implies H(R;(x,27);6)=(x+27)\bmod2.
\]

## 証明

\[
\begin{aligned}
A&=H(R-1;(x-1,27);6),\\
B&=H(R-1;(x,26);6),\\
C&=1\oplus H(R-1;(x,27);5),\\
H(R;(x,27);6)&=\operatorname{mex}\{A,B,C\}.
\end{aligned}
\]

x=27ではAの(26,27)を正準化すると(27,26)となりA=B=K0938。x≥28ではAは残容量R−1の帰納仮説、BはK0938、CはK0873で評価する。K0832のTheorem Tにより奇数Rの子値は{0,1}、偶数Rの親値は高々1。証明報告の全選択肢署名表はx=27..35の過渡域とx≥36 even/x≥37 oddの定常域で全正整数Rを覆う。奇数Rは署名01/0/1からmex 2/1/0、偶数Rは署名23・1・12・123/023・02・0からmex 0/1となり、上記のT27/P27を得る。

K0832の一般tail定理をX=(x,27), z=6へ適用すると閾値はx+34。Rに関する強帰納により全x≥27・全R≥0で成立する。有限範囲の外挿ではない。

## 独立監査と限界

順序付き直接再帰と降順正準化直接再帰を別実装し、y=27本体・y=26/z=5アンカーを照合。x=27..100の直接再帰50,838検査、x=27..2000の署名/mex 2,067,765点、tail128,310点、遠方tail5,000標本など合計6,389,417検査で不一致0。完全実行2回の監査内容はbyte-identical。有限監査は全称証明の代わりではなく、全称性は選択肢署名表・Theorem T・一般tail定理・R強帰納による。

証明対象は抽象κ=1残余ゲームの固定切片z=6,y=27のみ。z=6,y≥28、z≥7の全Grundy分類、全高さを統合する値2位置一般式、標準二次元共円ゲームの固定幅・q点安定化長は未解決。