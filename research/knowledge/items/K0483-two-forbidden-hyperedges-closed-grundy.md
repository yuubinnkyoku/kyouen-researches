---
id: K0483
title: 禁止集合が高々二つの有限配置ゲームは全安全局面のGrundy値に閉公式を持ち3以下
kind: proposition
status: needs-review
topics:
- grundy
- residual-games
- search-methods
- variants
aliases: []
relations:
- type: depends_on
  target: K0002
  note: mex再帰と独立ゲームのxor
- type: depends_on
  target: K0108
  note: 残余の包含極小禁止集合によるゲーム表現
artifacts:
- path: research/experiments/two-forbidden-hyperedges-20261018/proof.md
  role: proof
  note: 任意有限点集合の二つの禁止集合に対する全称mex帰納証明
- path: research/experiments/two-forbidden-hyperedges-20261018/verify.py
  role: verifier
  note: n<=7全組とn<=12固定乱数3000組のラベル付き全局面独立検査
- path: research/experiments/two-forbidden-hyperedges-20261018/results.json
  role: data
  note: 13795組・5260248安全局面の照合集計
- path: research/experiments/game-structure/reports/two-edge-exact-grundy-20261019.md
  role: proof
  note: 全称定理と帰納法による証明
- path: research/experiments/game-structure/scripts/verify_two_edges.py
  role: verifier
  note: 占有subsetによる独立した有限完全mex検査
- path: research/experiments/game-structure/scripts/verify_two_edges.cpp
  role: verifier
  note: 4領域の残数による独立した有限mex検査
- path: research/experiments/game-structure/output/two-edge-exact-grundy-20261019.json
  role: data
  note: 両検査の件数と範囲
scope: 任意有限点集合、包含極小禁止集合が0〜2個、完全指摘・二人通常プレイ、全安全局面
evidence: 2026-10-20添付統合。元資料では proved または computed と報告（個別の元statusは保存ZIPを参照）。本項目の全量化範囲に対する証明・計算の再監査は未完了。有限検証の実行範囲は統合実験のVALIDATION.mdを参照。
---


> 統合監査: 以下は取込元の主張・報告。全称証明・完全列挙の監査が未完了のため、現在の採用状態は needs-review。本文中の「証明」「一致」は元資料での報告を表す。


# 二禁止集合のGrundy閉公式

禁止集合E,Fの共通部、各固有部、外側の未占有点数をそれぞれc,u,v,zとする。安全局面でc=0ならu,v>=1。

- c=0: H=(u+v) mod2
- c>0かつmin(u,v)<c: H=(c-1+u+v) mod2
- c>0かつmin(u,v)=c: H=2+((max(u,v)-c) mod2)
- c>0かつmin(u,v)>c: H=(c+u+v) mod2

全安全局面でg=H xor(z mod2)。禁止集合が0個なら自由点数の偶奇、一つならE=Fとして適用する。従ってGrundy値は常に3以下。mex帰納法と独立成分のxorによる全称証明をproof.mdに記載。ラベル付き全局面の独立計算でn<=7全組およびn<=12の3000組を照合した。11×11の終盤で残余極小禁止集合が2個以下になれば直接評価可能だが、実探索速度の改善は未測定。

追加の同一命題資料: `K0454-two-edge-exact-grundy.md`。詳細と独立証人・検算範囲は追加artifactを参照。原文は取込元ZIPに保存。
