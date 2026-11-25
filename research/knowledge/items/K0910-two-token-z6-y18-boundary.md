---
id: K0910
title: 2トークン残余ゲーム z=6・y=18切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z6 y18 full Grundy slice]
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームHのA/B/C再帰、Theorem T、一般tail定理を使用する
- type: depends_on
  target: K0873
  note: C子の評価にz=5の全Grundy公式を使用する
- type: depends_on
  target: K0908
  note: B子とx=18境界の合流子をz=6,y=17全Grundy切片で評価する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z6-y18-boundary-20261117/report.md
  role: proof
  note: z=6,y=18切片の全x,R分類をA/B/C選択肢署名表とR強帰納で証明
- path: research/experiments/vertical-fiber-two-token-z6-y18-boundary-20261117/verify_z6_y18.py
  role: verifier
  note: 二方式直接再帰、z=5/z=6,y=17アンカー、全署名・mex・tailを独立監査
- path: research/experiments/vertical-fiber-two-token-z6-y18-boundary-20261117/output/audit.json
  role: data
  note: 6,299,078検査・不一致0・二回実行byte-identical。有限監査であり全称証明とは区別する
- path: research/log/2026-11-17-vertical-fiber-two-token-z6-y18-boundary.md
  role: log
  note: 最新main・未解決事項との照合、z=6,y=18切片の証明・監査・限界
scope: >-
  κ=1残余ゲームH(R;(x,18);6)の2トークン族、固定高さz=6、y=18、全x≥18・全R≥0。Grundy値0/1/2を完全分類する。
evidence: >-
  Rに関する強帰納。x=18ではA/B子が正準化後に同じ(18,17)状態へ合流する。x≥19ではA子が同じy=18切片の帰納仮説、B子がK0908、C子がK0873で評価できる。K0832のTheorem Tにより奇数親の選択肢は{0,1}、偶数親の値は高々1。x=18..25の過渡署名表、x=26の境界署名、x≥27の偶奇別定常署名を併合してmexを決定する。一般tail定理はR≥x+25でH=(x+18) mod 2を与える。独立有限監査は二方式直接再帰18,900件、選択肢署名・mex各2,048,439点、tail128,895点など計6,299,078検査で不一致0。有限監査は証明の代わりではなく、全称性は署名表・Theorem T・tail定理とR強帰納による。
---

## 定理

全 \(x\ge18,R\ge0\) に対して \(H(R;(x,18);6)\) のGrundy値0/1/2をreport.mdの \(T_{18}(x),P_{18}(x)\) で完全分類する。tailは \(R\ge x+25\) で \((x+18)\bmod2\)。

## 現在の根拠と限界

全称性はK0908/K0873をアンカーとするA/B/C選択肢署名表、K0832のTheorem T、一般tail定理、残容量Rに関する強帰納による。独立有限監査6,299,078件は不一致0だが、有限監査そのものを全称証明とは扱わない。値2位置はK0832の3族予想のz=6,y=18特殊化と一致するが、3族予想全体は未証明。対象は抽象残余ゲームのz=6,y=18切片に限り、z=6,y≥34、z≥7、標準二次元共円ゲームの固定幅安定化長は未解決である。
