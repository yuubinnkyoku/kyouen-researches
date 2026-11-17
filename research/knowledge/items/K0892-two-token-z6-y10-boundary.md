---
id: K0892
title: 2トークン残余ゲーム z=6・y=10切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z6 y10 full Grundy slice]
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームHの定義、A/B/C再帰、Theorem Tと一般tail定理を使用する
- type: depends_on
  target: K0873
  note: C子の評価にz=5の全Grundy公式を使用する
- type: depends_on
  target: K0890
  note: B子の評価にz=6,y=9全Grundy切片を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z6-y10-boundary-20261117/report.md
  role: proof
  note: z=6,y=10切片の全x,R分類をA/B/C選択肢署名表とR強帰納で証明
- path: research/experiments/vertical-fiber-two-token-z6-y10-boundary-20261117/verify_z6_y10.py
  role: verifier
  note: 二方式直接再帰、z=5/z=6,y=9アンカー、全署名・mex・tailを独立監査
- path: research/experiments/vertical-fiber-two-token-z6-y10-boundary-20261117/output/audit.json
  role: data
  note: 6,242,702検査・不一致0。有限監査であり全称証明とは区別する
- path: research/log/2026-11-17-vertical-fiber-two-token-z6-y10-boundary.md
  role: log
  note: 最新main・未解決範囲との照合、z=6,y=10切片の証明・監査・限界
scope: >-
  κ=1残余ゲームH(R;(x,y);z)の2トークン族、固定高さz=6、y=10、全x≥10・全R≥0。Grundy値0/1/2を完全分類する。
evidence: >-
  Rに関する強帰納。x=10ではA/B子が同じ(10,9)状態に正準化される。x≥11ではA子が帰納仮説、B子がK0890、C子がK0873で評価できる。K0832のTheorem Tにより奇数親の選択肢は{0,1}、偶数親の値は高々1。x=10..18の過渡署名表とx≥19の偶奇別A/B/C閉形式を併合してmexを決定する。一般tail定理はR≥x+17でH=(x+10) mod 2を与える。有限独立監査は二方式直接再帰10,863件、選択肢署名・mex各2,032,811点、tail129,415点、固定seed遠方tail2,000点など計6,242,702検査で不一致0。有限監査は証明の代わりではなく、全称性は署名表・Theorem T・tail定理とR強帰納による。
---

## 定理

\(E[a,b]\)を区間内の偶数、\(O[a,b]\)を奇数、\(I[a,\infty)\)を \(a\) 以上の全整数とする。全 \(x\ge10,R\ge0\) で
\[
H(R;(x,10);6)=
\begin{cases}
2,&R\in T_{10}(x),\\
1,&R\in P_{10}(x),\\
0,&\text{それ以外},
\end{cases}
\]
ただし \(T_{10}\) と \(P_{10}\) は証明artifactのreport.mdに記した閉形式である。tailは \(R\ge x+17\) で \((x+10)\bmod2\)。

## 限界

これは抽象残余ゲームの固定切片だけを解決する。z=6,y≥11、z≥7の全スライス、全高さを統合する3族予想、標準二次元共円ゲームの固定幅安定化長には直接の結論を与えない。
