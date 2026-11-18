---
id: K0979
title: 2トークン残余ゲーム z=7・y=3境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z7 y3 full Grundy slice]
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームHの定義、A/B/C再帰、Theorem T、単一トークン閉形式、高さだけの縮約（R<=z+1）、高R tail（R>=S+|X|+z-1=x+11）を使用する
- type: depends_on
  target: K0978
  note: B子の評価にz=7,y=2境界切片の全Grundy公式を使用する
- type: depends_on
  target: K0879
  note: C子の評価にz=6,y=3境界切片の全Grundy公式を使用する
- type: supports
  target: K0976
  note: z=7のy>=4候補式の全称証明に必要なy=1..3基底切片のうちy=3を供給し、y=1,2基底（K0977・K0978）と揃う
artifacts:
- path: research/experiments/vertical-fiber-two-token-z7-y3-boundary-20261118/report.md
  role: proof
  note: 固定z=7,y=3・全x,RのGrundy値0/1/2をA/B/C選択肢署名表とR強帰納で分類する全称証明
- path: research/experiments/vertical-fiber-two-token-z7-y3-boundary-20261118/verify_z7_y3.py
  role: verifier
  note: 生のトークン再帰とK0978・K0879アンカーからのA/B/C再構成を分離した独立有限監査器
- path: research/experiments/vertical-fiber-two-token-z7-y3-boundary-20261118/output/audit.json
  role: data
  note: 4,143,233検査・不一致0・二回実行byte-identical
- path: research/log/2026-11-18-vertical-fiber-two-token-z7-y3-boundary.md
  role: log
  note: 最新main・未解決範囲との照合、z=7,y=3切片の証明・監査・限界
scope: >-
  κ=1残余ゲームH(R;(x,y);z)の2トークン族における固定高さz=7、境界y=3、全x>=3・全R>=0。Grundy値0/1/2を完全分類する。
evidence: >-
  Rに関する強帰納。x=3では2つのトークン減少手が同じ(x,2)子へ合流し、x>=4ではA子が帰納仮説、B子がK0978のz=7,y=2公式、C子がK0879のz=6,y=3公式で評価される。K0832のTheorem Tにより奇数親の選択肢は{0,1}、偶数親の値は高々1。x=3..12の過渡域とx>=13の定常域に分けた全R署名表からmexを決定する。tail R>=x+11はK0832の高R縮約tail定理（R>=S+|X|+z-1）によるH=(x+3) mod 2。独立有限監査は直接再帰4,205状態、アンカー再構成4,205点、署名・mex各2,020,977点、tail帯27,972点、tail点19,992点、高さ縮約4,482点、固定seed2,000点、Theorem T 2,050,947点を含む4,143,233検査で不一致0。有限監査は証明の代わりではなく、全称性は選択肢表とR強帰納による。
---

## 現在の未解決範囲

本項は \(z=7,y=3\) の境界切片を証明する。\(y=1,2\) は[K0977](K0977-two-token-z7-y1-boundary.md)・[K0978](K0978-two-token-z7-y2-boundary.md)、\(y\ge4\) は[K0976](K0976-two-token-z7-y-ge4-conjecture.md)で全称証明済みとなり、2トークン族の \(z=7\) は全 \(y\ge1,x\ge y,R\ge0\) で完全分類された。z=8はy=1..3（K0983/K0984/K0986）が証明済みで、y>=4は未解決。z=9はy=1（K0985）が証明済みで、y>=2は未解決。z>=10、全高さを統合する値2位置一般式、標準二次元共円ゲームの固定幅安定化長も未解決である。
