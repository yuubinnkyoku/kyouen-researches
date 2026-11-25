---
id: K0623
title: 有界木幅グラフ型q点共円ゲームの極大終局長母関数の厳密計数
kind: proposition
status: proved
topics: [geometry, maximal-safe, statistics, strategy-length, variants]
aliases: []
relations:
- type: depends_on
  target: K0602
  note: 任意有限単純グラフの整数共円実現と削除頂点集合による極大配置分類を使用
- type: generalizes
  target: K0621
  note: 擬森に限らず任意の有界木幅グラフに適用可能
artifacts:
- path: research/experiments/treewidth-terminal-dp-20261102/proof.md
  role: proof
  note: 頂点の支配情報3状態と辺導入・合流を用いる木分解上の全称証明
- path: research/experiments/treewidth-terminal-dp-20261102/verify.py
  role: verifier
  note: 道分解6453条件、合流3735条件、禁止超辺80条件、K2mと梯子の照合
scope: 少なくとも1辺を持つ任意有限単純グラフG、任意q>=4、幅wの木分解が与えられたK0602自由整数平面点配置。標準全格子盤は対象外。
evidence: 木分解上の3状態動的計画法と合流規則の数学的帰納法による全称証明。有限完全列挙は独立の実装監査。
---

# 頂点被覆が大きくても木幅が小さければ厳密計数できる

K0602 のグラフ型 q 点共円・共線禁止構成で、G=(V,E)、q>=4、r=q−3、N=1+|V|+r|E| とする。**幅 w の木分解が与えられれば**、全極大安全配置の石数別母関数を

\[
\boxed{O(5^{w+1}\operatorname{poly}(N,\log q))}
\]

時間で厳密に計算できる。頂点被覆数は無制限であり、同一連結成分内の閉路数も無制限。木分解の構築時間は含めない。

袋内の頂点について「残存」「削除・未救済」「削除・救済済み」の3状態を持つ。辺を導入すると残存辺の重み r/u と救済状態を更新し、頂点を忘れるとき未救済の削除を棄却する。合流時は救済済みかどうかを論理和で統合する。袋サイズ w+1 の合流に許される状態対は頂点当たり5通りなので、5^{w+1} が得られる。これは K0602 の削除集合公式を全称的に計算する方法であり、有限実験からの外挿ではない。

特に **2×m 梯子グラフ**は最小頂点被覆数が m と無界になる一方、道幅は2に保たれる。K0622 の頂点被覆数に指数的な方法では効率が保証されなかったこの族を、m と q の多項式時間で扱える。

[全称証明](../../experiments/treewidth-terminal-dp-20261102/proof.md)と[独立検証器](../../experiments/treewidth-terminal-dp-20261102/verify.py)を保存。道分解と全削除集合の照合6,453条件、合流3,735条件、禁止超辺の直接列挙80条件・254,736部分集合、完全二部グラフの閉形式21条件、梯子14条件が一致した。

**限界**：一般グラフの多項式時間計数や、標準11×11格子盤の勝敗は主張しない。木分解は与えられるものとし、木幅の探索器は本項の対象外。
