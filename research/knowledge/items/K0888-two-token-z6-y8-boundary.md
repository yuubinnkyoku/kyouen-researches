---
id: K0888
title: 2トークン残余ゲーム z=6・y=8切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z6 y8 full Grundy slice]
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームHのA/B/C再帰、Theorem T、一般tail定理と3族位置予想を使用する
- type: depends_on
  target: K0873
  note: C子の評価にz=5の全Grundy公式を使用する
- type: depends_on
  target: K0887
  note: B子の評価にz=6,y=7全Grundy切片を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z6-y8-boundary-20261117/report.md
  role: proof
  note: z=6,y=8切片の全x,R分類をA/B/C選択肢署名表とR強帰納で証明
- path: research/experiments/vertical-fiber-two-token-z6-y8-boundary-20261117/verify_z6_y8.py
  role: verifier
  note: K0887の二方式再帰とz=5/z=6,y=7アンカーを使い、新切片の式・署名・mex・tailを独立監査
- path: research/experiments/vertical-fiber-two-token-z6-y8-boundary-20261117/output/audit.json
  role: data
  note: 6,229,190検査・不一致0・二回実行byte-identical
- path: research/log/2026-11-17-vertical-fiber-two-token-z6-y8-boundary.md
  role: log
  note: 最新main・未解決範囲との照合、z=6,y=8切片の証明・独立監査・限界
scope: >-
  κ=1残余ゲームH(R;(x,y);z)の2トークン族、固定高さz=6、y=8、全x≥8・全R≥0。Grundy値0/1/2を完全分類する。
evidence: >-
  Rに関する強帰納。x=8では2つのトークン減少手が同じ(8,7)子へ合流し、x≥9ではA子が帰納仮説、B子がK0887のz=6,y=7公式、C子がK0873のz=5公式で評価できる。K0832のTheorem Tにより奇数親の選択肢は{0,1}、偶数親の値は高々1。x=8..16の過渡域とx≥17の偶奇別定常域に分けた全R署名表からmexを決定する。tail R≥x+15ではH=(x+8) mod 2。独立有限監査は二方式直接再帰9,030件、選択肢署名・mex各2,028,874点、tail129,545点、固定seed遠方tail2,000点など計6,229,190検査で不一致0。有限監査は証明の代わりではなく、全称性は選択肢表・Theorem T・tail定理とR強帰納による。
---

## 命題・範囲

全 \(x\ge8,R\ge0\) に対して、\(H(R;(x,8);6)\) のGrundy値0/1/2をreport.mdの \(T_8(x),P_8(x)\) で完全分類する。値2位置の追加点は、\(d=x-8\) に応じて \(d=0\) で19、\(d=4\) で21、\(d=7\) で23,25,27,29、\(d\ge8\) で23となり、基本ラダーは{1,3,5}である。

## 現在の根拠と限界

全称性はK0873/K0887をアンカーとするA/B/C選択肢署名表、K0832のTheorem T、一般tail定理、残容量Rに関する強帰納による。独立有限監査6,229,190件は不一致0だが、有限監査そのものを全称証明とは扱わない。対象は抽象残余ゲームのz=6,y=8切片に限り、z=6,y>=9、z>=7、3族位置予想全体、標準二次元共円ゲームの固定幅安定化長は未解決である。
