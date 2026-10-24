---
id: K0548
title: 無理数間隔比と有理数高さの三平行線q6は各線13候補で全終局15石となる
kind: proposition
status: proved
topics: [geometry, variants, rectangles, maximal-safe, grundy, first-moves]
aliases: []
relations: []
artifacts:
- path: research/experiments/irrational-three-lines-q6-20261024/proof.md
  role: proof
  note: 無理数係数の分離と非零同積弦のmatchingから一点二円上界・13候補十分性を証明
solution:
  board: 無理数間隔比・有理数高さの三平行線、各線13候補以上
  level: strong
  outcome: conditional
  classification: [root, first-moves, all-safe-win-loss, all-safe-grundy]
  coverage: 条件を満たす有限盤の全安全局面
  conditions: q=6共円または共線禁止、通常プレイ、全候補高さが共通座標で有理数
  verification: [mathematical-proof]
  certificate: 差の円方程式から弦積差一定、非零同積弦は高々二組、利用不能点は12以下
  independent_check: 数学的証明。特定二次無理数帯の直接二次体監査はK0549
  note: 全終局15石、g(S)=(15−|S|) mod2、空盤先手勝ち・全初手勝ち。13の最小性は未主張
scope: 三平行線の位置x0,x1,x2の比(x2−x0)/(x1−x0)が無理数、全候補高さが有理数、各線13候補以上。共通縦平行移動・等方拡大で有理数化できる場合も含む。
evidence: 無理数と有理数の線形独立性・非零同積弦の端点非共有による全称数学的証明。
---

# 有理高さ・無理数間隔比の13候補十分性

各線13候補以上なら全終局は各線5石、計15石。
全安全局面で `g(S)=(15−|S|) mod2`、空盤先手勝ち・全初手勝ち。

既存有理高さ点を通る二円の差の式から、無理数の相対間隔uの係数である弦積差δが等しくなる。
両外線で既存点を原点とした弦の積が一定となり、少なくとも一方の積は非零。
その線の高々5点では同積弦が互いに素となるため高々2円しか通れない。
不足線の占有点込み利用不能点は3a≤12なので13候補で常に延長できる。

全実数高さや有理間隔比へ条件を外さない。13が最小とは主張しない。
