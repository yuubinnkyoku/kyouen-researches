---
id: K0338
title: 標準正方形盤の安定化群位数4以上の安全集合は高々五石で正確にO(n²)個
kind: proposition
status: proved
topics: [geometry, grundy, search-methods]
aliases: []
relations:
- type: depends_on
  target: K0001
  note: 標準四点共円・共線禁止
artifacts:
- path: research/experiments/game-structure/reports/symmetry-scope-20261005.md
  role: proof
  note: D4部分群、禁止軌道、二軸配置の必要十分分類と個数公式
- path: research/experiments/game-structure/scripts/symmetry_scope_20261005.py
  role: verifier
  note: 部分群軌道の全選択と公式による生成を比較する
- path: research/experiments/game-structure/output/symmetry_scope_20261005.json
  role: data
  note: n=1..11の完全有限照合
scope: 標準q=4・円と直線を禁止する任意n×n盤、D4は八要素の抽象群
evidence: 全称数学的証明と独立した有限候補生成法の照合
---

# 高対称安全集合の全称分類

標準n×n盤の安全集合SでD4安定化群の位数が4以上なら、Sは中心一点以下、または中心を通る
水平・垂直二軸か二対角線上で各軸から高々一つの反対点対を選んだ集合である。
中心は存在すれば任意に追加でき、両軸の対を同時に使うときは中心距離が異なることが必要十分。
奇数盤では高々五石、偶数盤では高々四石。

該当安全集合の正確な個数は奇数nでn²+1、偶数nでn²/4+n/2+1。
空集合と存在する中心一点は安定化群位数8、他の該当集合は全て位数4。

従ってK0186の小軌道勝ち手問題で注意すべき候補は各nでO(n²)個に限られる。
これらの候補のg,hの計算や全nについての排除は完了しておらず、K0186は未解決のまま。
五石高対称集合は中心と両軸の対で三石ずつを持つため、合法手にはサイズ1/2の軌道が存在しない。
