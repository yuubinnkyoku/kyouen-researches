---
id: K0443
title: 残余禁止辺4本以下・rank4の通常Grundy値は5以下で、孤立点なしの達成型は2種類
kind: proposition
status: proved
topics:
- residual-games
- grundy
- search-methods
aliases: []
relations:
- type: depends_on
  target: K0108
  note: 極小残余辺による継続ゲームの表現
- type: depends_on
  target: K0002
  note: mexと孤立点のxor
artifacts:
- path: research/experiments/fastlane-four-edge-20261019/reports/four-edge-rank-four.md
  role: proof
  note: 92,550候補の完全性と37,592種類の有限完全列挙、適用範囲
- path: research/experiments/fastlane-four-edge-20261019/scripts/enumerate.py
  role: verifier
  note: 所属個数mexと辺改名軌道の全列挙
- path: research/experiments/fastlane-four-edge-20261019/scripts/independent.cpp
  role: verifier
  note: 独立した全占有集合mexによる全37,592種類の照合
- path: research/experiments/fastlane-four-edge-20261019/output/results.json
  role: data
  note: 全分布・達成例・軌道数
- path: research/experiments/four-q4-residual-grundy-20261018/proof.md
  role: proof
  note: 15所属型への全称帰着、4,079型の完全列挙、最小点数と具体証人
- path: research/experiments/four-q4-residual-grundy-20261018/verify.py
  role: verifier
  note: Pythonの点集合ビットマスクによる完全再帰
- path: research/experiments/four-q4-residual-grundy-20261018/independent.cpp
  role: verifier
  note: C++の未占有所属型数による独立再帰
- path: research/experiments/four-q4-residual-grundy-20261018/results.json
  role: data
  note: 全4,079型のGrundy値分布と証人
- path: research/experiments/knowledge-audit-20261021/README.md
  role: log
  note: 証明の論理監査・再実行範囲・判定
scope: 通常プレイの任意有限禁止集合ゲーム。現在合法な点上の包含極小残余禁止辺が4本以下、各辺サイズ2〜4。孤立点を許す。達成型の一意性は孤立点を除いた核に限り、幾何実現性は主張しない。
evidence: '2026-10-21監査。所属型の完全性・辺極小性と2軌道分類、自由点xorを確認。PythonとC++の37592族を再実行。 監査記録: research/experiments/knowledge-audit-20261021/README.md。'
---


# 4本以下の残余禁止辺・rank4のGrundy上界5

包含極小残余辺が4本以下で、各辺サイズが2〜4なら、任意の安全局面の通常Grundy値は5以下。孤立点を除いた核でg=5を実現する超グラフは、辺と頂点の改名を除いて9頂点・辺サイズ(2,3,3,4)と11頂点・4辺すべてサイズ4の2種類のみ。

4辺の場合、2^4−1=15種類の所属個数を各辺サイズ4以下で全列挙すると92,550個。各辺サイズ2以上・包含極小を満たす37,592個のg分布は(0..5)=(13508,13427,5111,5270,240,36)。g≥6は0。g=5の36個は辺改名で24個と12個の2軌道に分かれる。3辺以下は最大3。孤立点は独立な1点成分でxor偶奇を与えるので上界5を変えない。

9頂点達成例の辺は{0,2}, {1,2,8}, {3,4,8}, {5,6,7,8}。11頂点で4辺すべてサイズ4の達成例は{0,6,9,10}, {1,2,5,6}, {3,4,5,6}, {7,8,9,10}。いずれも空局面g=5。

これは抽象残余ゲームの上界・分類であり、共円・共線な4点組による幾何実現性は未証明。計算機援用証明の全詳細・再現コード・独立検証は対応するexperimentを参照。

追加の同一命題資料: `K0439-four-q4-forbidden-grundy-bound.md`。詳細と独立証人・検算範囲は追加artifactを参照。原文は取込元ZIPに保存。
