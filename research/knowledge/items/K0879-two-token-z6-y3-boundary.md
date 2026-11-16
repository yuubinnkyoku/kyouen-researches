---
id: K0879
title: 2トークン残余ゲーム z=6・y=3境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z6 y3 full Grundy slice]
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームHの定義、A/B/C再帰、Theorem Tとtail定理を使用する
- type: depends_on
  target: K0873
  note: C子の評価にz=5の全Grundyスライスを使用する
- type: depends_on
  target: K0878
  note: B子の評価にz=6,y=2境界切片の全Grundy公式を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z6-y3-boundary-20261117/report.md
  role: proof
  note: 固定z=6,y=3・全x,RのGrundy値0/1/2をA/B/C選択肢署名表とR強帰納で分類する全称証明
- path: research/experiments/vertical-fiber-two-token-z6-y3-boundary-20261117/verify_z6_y3.py
  role: verifier
  note: 生のトークン再帰とz=5・z=6,y=2アンカーからのA/B/C再構成を分離した独立有限監査器
- path: research/experiments/vertical-fiber-two-token-z6-y3-boundary-20261117/output/audit.json
  role: data
  note: 4,120,238検査・不一致0・二回実行byte-identical
- path: research/log/2026-11-17-vertical-fiber-two-token-z6-y3-boundary.md
  role: log
  note: 最新main・未解決範囲との照合、z=6,y=3切片の証明・監査・限界
scope: >-
  κ=1残余ゲームH(R;(x,y);z)の2トークン族における固定高さz=6、境界y=3、全x≥3・全R≥0。Grundy値0/1/2を完全分類する。
evidence: >-
  Rに関する強帰納。x=3では2つのトークン減少手が同じ(x,2)子へ合流し、x≥4ではA子が帰納仮説、B子がK0878のz=6,y=2公式、C子がK0873のz=5全公式で評価される。K0832のTheorem Tにより奇数親の選択肢は{0,1}、偶数親の値は高々1。x=3..11の過渡域とx≥12の定常域に分けた全R署名表からmexを決定する。tail R≥x+10は既証明のH=(x+3) mod 2。独立有限監査は直接再帰4,515状態、アンカー11,817状態、署名・mex各2,040,957点、tail19,992点、固定seed2,000点を含む4,120,238検査で不一致0。有限監査は証明の代わりではなく、全称性は選択肢表とR強帰納による。


## 現在の未解決範囲

本項は \(z=6,y=3\) の切片を証明する。[K0880](K0880-two-token-z6-y4-boundary.md)により \(y=4\) も証明済み。\(z=6,y\ge5\)、\(z\ge7\) の全Grundy分類と、全高さを統合する3族値2位置一般式は未解決。標準二次元共円ゲームの固定幅安定化長へ直接転送しない。
