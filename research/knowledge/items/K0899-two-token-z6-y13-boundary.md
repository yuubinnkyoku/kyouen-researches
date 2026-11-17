---
id: K0899
title: 2トークン残余ゲーム z=6・y=13切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z6 y13 full Grundy slice]
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームHの定義、A/B/C再帰、Theorem Tと一般tail定理を使用する
- type: depends_on
  target: K0873
  note: C子の評価にz=5の全Grundy公式を使用する
- type: depends_on
  target: K0896
  note: B子の評価にz=6,y=12全Grundy切片を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z6-y13-boundary-20261117/report.md
  role: proof
  note: z=6,y=13切片の全x,R分類をA/B/C選択肢署名表とR強帰納で証明
- path: research/experiments/vertical-fiber-two-token-z6-y13-boundary-20261117/verify_z6_y13.py
  role: verifier
  note: 二方式直接再帰、z=5/z=6,y=12アンカー、全署名・mex・tailを独立監査
- path: research/experiments/vertical-fiber-two-token-z6-y13-boundary-20261117/output/audit.json
  role: data
  note: 6,254,540検査・不一致0・二回実行byte-identical。有限監査であり全称証明とは区別する
- path: research/log/2026-11-17-vertical-fiber-two-token-z6-y13-boundary.md
  role: log
  note: 最新main・未解決事項との照合、z=6,y=13切片の証明・監査・限界
scope: >-
  κ=1残余ゲームH(R;(x,y);z)の2トークン族、固定高さz=6、y=13、全x≥13・全R≥0。Grundy値0/1/2を完全分類する。
evidence: >-
  Rに関する強帰納。x=13ではA/B子が同じ(13,12)状態に合流する。x≥14ではA子が帰納仮説、B子がK0896、C子がK0873で評価できる。K0832のTheorem Tにより奇数親の選択肢は{0,1}、偶数親の値は高々1。x=13..21の過渡署名表とx≥22の偶奇別A/B/C閉形式を併合してmexを決定する。一般tail定理はR≥x+20でH=(x+13) mod 2を与える。有限独立監査は二方式直接再帰5,250件、選択肢署名・mex各2,038,694点、tail129,220点、固定seed遠方tail2,000点など計6,254,540検査で不一致0。有限監査は証明の代わりではなく、全称性は署名表・Theorem T・tail定理とR強帰納による。
---

## 命題・範囲

全 \(x\ge13,R\ge0\) に対して \(H(R;(x,13);6)\) のGrundy値0/1/2をreport.mdの \(T_{13}(x),P_{13}(x)\) で完全分類する。tailは \(R\ge x+20\) で \((x+13)\bmod2\)。

## 現在の根拠と限界

全称性はK0896/K0873をアンカーとするA/B/C選択肢署名表、K0832のTheorem T、一般tail定理、残容量Rに関する強帰納による。独立有限監査6,254,540件は不一致0だが、有限監査そのものを全称証明とは扱わない。対象は抽象残余ゲームのz=6,y=13切片に限り、z=6,y≥14、z≥7、3族値2位置予想全体、標準二次元共円ゲームの固定幅安定化長は未解決である。
