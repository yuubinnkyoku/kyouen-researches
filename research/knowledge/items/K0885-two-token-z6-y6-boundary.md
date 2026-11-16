---
id: K0885
title: 2トークン残余ゲーム z=6・y=6切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z6 y6 full Grundy slice]
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームHのA/B/C再帰、Theorem T、完了予算・tail定理を使用する
- type: depends_on
  target: K0873
  note: C子の評価にz=5の全Grundyスライスを使用する
- type: depends_on
  target: K0884
  note: B子の評価にz=6,y=5の全Grundy切片を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z6-y6-boundary-20261117/report.md
  role: proof
  note: 固定z=6,y=6・全x,RのGrundy値0/1/2をA/B/C選択肢署名表とR強帰納で分類する全称証明
- path: research/experiments/vertical-fiber-two-token-z6-y6-boundary-20261117/verify_z6_y6.py
  role: verifier
  note: K0873/K0884の既証明公式を読み込み、二方式再帰・署名・mex・tailを独立監査
- path: research/experiments/vertical-fiber-two-token-z6-y6-boundary-20261117/output/audit.json
  role: data
  note: 6,216,410検査・不一致0・二回実行byte-identical
- path: research/log/2026-11-17-vertical-fiber-two-token-z6-y6-boundary.md
  role: log
  note: 最新main・未解決事項との照合、z=6,y=6切片の全称証明・独立監査・限界
scope: >-
  κ=1残余ゲームH(R;(x,6);6)の2トークン族、全x≥6・全R≥0。Grundy値0/1/2を完全分類する。
evidence: >-
  Rに関する強帰納。x=6では2つのトークン減少手が同じ(6,5)子に合流し、x≥7ではA子が帰納仮説、B子がK0884のz=6,y=5公式、C子がK0873のz=5全公式で評価できる。K0832のTheorem Tにより奇数親の選択肢は{0,1}、偶数親の値は高々1。x=6..14の過渡域とx≥15の偶奇別定常域に分けた全R署名表からmexを決定する。tail R≥x+13ではH=(x+6) mod 2。独立有限監査は二方式直接再帰7,965件、選択肢署名・mex各2,024,925点、tail129,675点、固定seed遠方tail2,000点など計6,216,410検査で不一致0。有限監査は証明の代わりではなく、全称性は選択肢表・Theorem T・tail定理とR強帰納による。
---