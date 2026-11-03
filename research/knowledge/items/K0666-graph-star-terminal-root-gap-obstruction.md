---
id: K0666
title: グラフ星型の中心付き終局長多項式は次数2のない非自明グラフで実根性を失う
kind: proposition
status: proved
topics: [geometry, maximal-safe, statistics, strategy-length, variants]
aliases: []
relations:
- type: depends_on
  target: K0648
  note: 中心付き終局長母関数の非負係数と正の定数項
- type: depends_on
  target: K0655
  note: 最初の正の終局長差は最小非葉次数から決まる
- type: generalizes
  target: K0665
  note: 星型反例を次数2のない任意グラフへ拡張する
artifacts:
- path: research/experiments/graph-star-root-gap-obstruction-20261103/proof.md
  role: proof
  note: 正係数多項式の欠番障害とK0655による全称証明
scope: K0602の有限単純グラフGで辺数e>=2、次数2以上の頂点が存在し、次数2の頂点が存在しない場合。q>=4。中心点を含む極大配置の終局長差のみ。標準全格子盤は対象外。
evidence: K0648・K0655と実根多項式の係数の正値性からの全称証明。追加の有限計算には依存しない。
---

# 次数2を持たないグラフでは中心付き終局長多項式は実根的でない

辺数 e>=2、H={v:deg(v)>=2} が空でなく、G に次数2の頂点がないとする。q>=4 とし、中心点を含む極大配置の最短終局長差の母関数を F(u) とする。

**全称定理：F(u) は非実根を持つ。**

K0655 により最初の正の終局長差は min_{v∈H}(deg(v)-1)>=2。K0648 により定数項は正で、以後の係数は非負、かつ上側の正係数が存在する。したがって [u]F=0 だが deg F>=2。全根が実数ならすべて負となり、根の積表示から [u]F>0 が必要なので矛盾する。

**帰結：** 非葉頂点の次数がすべて3以上の任意の木で、中心付き終局長多項式は実根性を失う。星型 K1,d（d>=3）の K0665 を一般化する。次数2を含む枝分かれ木については、この方法では決着しない。

[全称証明](../../experiments/graph-star-root-gap-obstruction-20261103/proof.md)。
