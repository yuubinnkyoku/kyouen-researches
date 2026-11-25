---
id: K0918
title: 2トークン残余ゲーム z=6・y=24切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z6 y24 full Grundy slice]
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームHのA/B/C再帰、Theorem T、一般tail定理を使用する
- type: depends_on
  target: K0873
  note: C子の評価にz=5の全Grundy公式を使用する
- type: depends_on
  target: K0917
  note: B子とx=24境界の合流子をz=6,y=23全Grundy切片で評価する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z6-y24-boundary-20261117/report.md
  role: proof
  note: z=6,y=24切片の全x,R分類をA/B/C選択肢署名表とR強帰納で証明
- path: research/experiments/vertical-fiber-two-token-z6-y24-boundary-20261117/verify_z6_y24.py
  role: verifier
  note: 二方式直接再帰、z=5/z=6,y=23アンカー、全署名・mex・tailを独立監査
- path: research/experiments/vertical-fiber-two-token-z6-y24-boundary-20261117/output/audit.json
  role: data
  note: 6,324,884検査・不一致0・二回実行byte-identical。有限監査であり全称証明とは区別する
- path: research/log/2026-11-17-vertical-fiber-two-token-z6-y24-boundary.md
  role: log
  note: 最新main・未解決事項との照合、z=6,y=24切片の証明・監査・限界
scope: >-
  κ=1残余ゲームH(R;(x,24);6)の2トークン族、固定高さz=6、y=24、全x≥24・全R≥0。Grundy値0/1/2を完全分類する。
evidence: >-
  Rに関する強帰納。x=24ではA/B子が正準化後に同じ(24,23)状態へ合流する。x≥25ではA子が同じy=24切片の帰納仮説、B子がK0917、C子がK0873で評価できる。K0832のTheorem Tにより奇数親の選択肢は{0,1}、偶数親の親値は高々1。x=24..32の過渡署名表、x≥33の偶奇別定常署名を併合してmexを決定する。一般tail定理はR≥x+31でH=(x+24) mod 2を与える。独立有限監査は二方式直接再帰・公式アンカー10,323件、選択肢署名・mex各2,060,034点、tail128,505点など計6,324,884検査で不一致0。有限監査は証明の代わりではなく、全称性は署名表・Theorem T・tail定理と強帰納による。
---

## 定理

全x≥24,R≥0に対してH(R;(x,24);6)のGrundy値0/1/2をreport.mdのT₂₄(x),P₂₄(x)で完全分類する。tailはR≥x+31で(x+24) mod 2。

## 現在の根拠と限界

全称性はK0917/K0873をアンカーとするA/B/C選択肢署名表、K0832のTheorem T、一般tail定理、残容量Rに関する強帰納による。独立有限監査6,324,884件は不一致0だが、有限監査そのものを全称証明とは扱わない。値2位置はK0832の3族値2位置予想のz=6,y=24特殊化と一致するが、3族予想全体は未証明。対象は抽象残余ゲームのz=6,y=24切片に限り、z=6,y≥35、z≥7、標準二次元共円ゲームの固定幅安定化長は未解決である。
