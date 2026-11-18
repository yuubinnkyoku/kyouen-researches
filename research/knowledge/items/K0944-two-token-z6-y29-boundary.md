---
id: K0944
title: 2トークン残余ゲーム z=6・y=29切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z6 y29 full Grundy slice]
relations:
- type: depends_on
  target: K0832
  note: Theorem Tと一般tail定理を使う
- type: depends_on
  target: K0873
  note: C子の評価にz=5の全Grundy公式を使う
- type: depends_on
  target: K0942
  note: B子とx=29境界のA子をz=6,y=28全Grundy公式で評価する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z6-y29-boundary-20261118/report.md
  role: proof
  note: z=6,y=29切片の全x,R分類、選択肢署名表、xに関する帰納証明
- path: research/experiments/vertical-fiber-two-token-z6-y29-boundary-20261118/verify_z6_y29.py
  role: verifier
  note: 順序付き・降順正準化の二方式直接再帰、y=28/z=5アンカー、全署名・mex・tailを独立監査
- path: research/experiments/vertical-fiber-two-token-z6-y29-boundary-20261118/output/audit.json
  role: data
  note: 6,376,910検査・不一致0・二回実行byte-identical。有限監査であり全称証明とは区別する
- path: research/log/2026-11-18-vertical-fiber-two-token-z6-y29-boundary.md
  role: log
  note: 最新main・未解決事項との照合、z=6,y=29切片の証明・監査・限界
scope: >-
  κ=1残余ゲームH(R;(x,29);6)の2トークン族、固定高さz=6、y=29、全x≥29・全R≥0。Grundy値0/1/2を完全分類する。
evidence: >-
  xに関する帰納。x=29ではA子の(28,29)が正準化後にK0942の(29,28)となりB子と一致する。x≥30ではA子をx-1の帰納仮説、B子をK0942、C子をK0873で評価する。1≤R<x+36の過渡署名表（x=29..37）と一般署名表（x≥38 even/x≥39 odd）で全選択肢を覆い、mexからT29/P29を得る。R≥x+36はK0832の一般tail定理H=(x+29) mod 2で閉じる。独立有限監査は6,376,910検査で不一致0、二回実行byte-identical。有限監査は証明の代わりではなく、全称性はx帰納・署名表・既証明アンカーによる。
---

## 命題・範囲

\(O[a,b]\) はa以上b以下の奇数、\(E[a,b]\) は同範囲の偶数とする。全ての \(x\ge29,R\ge0\) について

\[
H(R;(x,29);6)=
\begin{cases}
2,&R\in T_{29}(x),\\
1,&R\in P_{29}(x),\\
0,&\text{otherwise}.
\end{cases}
\]

\[
T_{29}(x)=\{1,3,5\}\cup
\begin{cases}
\{61\}&x=29,\\
\{63\}&x=33,\\
\{65,67,69,71\}&x=36,\\
\{65\}&x\ge37,\\
\varnothing&\text{otherwise}.
\end{cases}
\]

\[
P_{29}(x)=
\begin{cases}
O[7,59],&x=29,\\
O[7,\infty)\cup E[62,\infty),&x=30,\\
O[7,61],&x=31,\\
O[7,\infty)\cup E[64,\infty),&x=32,\\
O[7,61],&x=33,\\
O[7,\infty)\cup E[64,\infty),&x=34,\\
O[7,63],&x=35,\\
O[7,63]\cup E[66,\infty)\cup O[x+37,\infty),&x\ge36\text{ 偶数},\\
O[7,63]\cup E[66,x+35],&x\ge37\text{ 奇数}.
\end{cases}
\]

一般tailは

\[
R\ge x+36\implies H(R;(x,29);6)=(x+29)\bmod2.
\]

## 現在の根拠と限界

A/B/C再帰とxに関する強帰納。基底x=29はA=Bの正準化合流によりK0942へ接続する。帰納段のBはK0942、CはK0873。全署名表とmex、およびK0832のTheorem T・一般tail定理で全x・全Rを覆う。独立有限監査の詳細はartifactsの証明報告・検証器・監査JSONを参照。有限監査の範囲を全称性の根拠とはしない。

z=6,y≥32、z≥7、全高さを統合する値2位置の一般式、標準二次元共円ゲームの固定幅・q点安定化長は未解決。
