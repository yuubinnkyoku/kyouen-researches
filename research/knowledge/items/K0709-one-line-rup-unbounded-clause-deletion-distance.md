---
id: K0709
title: 一行RUP証明を持つCNFでもSAT化に必要な節削除数は任意に大きい
kind: proposition
status: proved
topics: [search-methods, verification, provenance]
aliases: []
relations: []
artifacts:
- path: research/experiments/proof-length-versus-deletion-distance-20261109/README.md
  role: proof
  note: 全m,kの明示構成、節削除数の上下界、一行RUP証明と適用範囲
- path: research/experiments/proof-length-versus-deletion-distance-20261109/verify.py
  role: verifier
  note: 15個のCNFで最少節削除数を全数列挙し、共通証明を修正版チェッカーで検査する
- path: research/experiments/proof-length-versus-deletion-distance-20261109/results.json
  role: data
  note: m<=5の有限検査と入力・検証器ソースhash。全称証明の代替ではない
scope: 一般のCNFの重みなし最少節削除数δ。特定の剰余放物線NAE族内の経験的相関については断定しない。
evidence: 任意の1<=k<=mで、変数m個・異なる節2m個・同語反復なし・δ=k・共通一行RUP証明のCNFを明示構成する。
---

## 命題と証明

F_(m,k)を、全正単位節(x_i)、先頭k個の負単位節(¬x_i)、残るj>kについての
正二項節(x_1∨x_j)からなるCNFとする（1<=k<=m）。変数数はm、節数は2mで、重複も同語反復もない。

SAT化には、k組の相反する単位節対のそれぞれから少なくとも一節を削除する必要がある。
負単位節k個を全て削除すれば全変数を真としてSATになるので、最少節削除数は厳密にk。
他方、相反する最初の単位節対だけで矛盾するため、全m,kで空節を追加する一行 `0` がRUP証明となる。

固定したmでも、同じ変数数・節数と一行証明のままで削除数は1..mの全値を取る。
m=kを大きくすれば、一行証明のまま削除数は無界である。
従って証明行数単独から削除数の値や大小順序は決まらず、その行数だけに依存する有限上界もない。
さらに節(x_1)の冗長なRUP追加を繰り返せば、同じCNF・同じ削除数の証明を任意の長さにできる。
実行で生成された証明の行数と、必要最小の証明長も区別する。

## 現在の根拠と限界

上の全称構成が証明であり、m<=5の15例の全数検査は支持確認である。
節長分布・全リテラル数を固定した族、剰余放物線の幾何的な違反数や点削除数の命題ではない。
節長4・連結・有界次数を保つ別の構成は [K0710](K0710-nae4-constant-rup-unbounded-deletion-distance.md) を参照。

剰余放物線の証明行数の中央値を、そのまま「不達成の頑健さ」やSAT化距離の順位へ読み替える根拠はない。
特定の幾何CNF族で相関があるかは、距離を定義し直接測定する別の問題として残る。
