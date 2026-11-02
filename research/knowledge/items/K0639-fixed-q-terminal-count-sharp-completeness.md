---
id: K0639
title: 任意固定q>=5の整数共円ゲーム極大配置計数は#P完全
kind: proposition
status: proved
topics: [geometry, maximal-safe, statistics, variants, search-methods]
aliases: []
relations:
- type: depends_on
  target: K0602
  note: グラフ星型q点構成と誘導辺重み付き支配集合の極大配置総数公式
- type: depends_on
  target: K0636
  note: 任意固定q>=4で多項式ビット長の整数座標を決定的に構成できること
- type: generalizes
  target: K0635
  note: q=4の組合せ入力の計数困難性を任意固定q>=5にも拡張
artifacts:
- path: research/experiments/graph-star-fixed-q-count-complexity-20261102/proof.md
  role: proof
  note: 辺ごとの接続複製と相異なる指数底のVandermonde補間による全称的な#VertexCover還元
- path: research/experiments/graph-star-fixed-q-count-complexity-20261102/verify.py
  role: verifier
  note: 重み付き支配集合直接列挙・厳密有理補間・q点禁止超辺の極大配置直接列挙の独立照合
scope: 任意の固定整数q>=5、整数平面上の有限点集合を明示入力し、共円または共線のq点を禁止するゲームの全極大安全配置総数。#P完全性は多項式時間チューリング還元の意味。3点共線のない入力にも#P困難性。標準全格子盤は対象外。
evidence: '#VertexCoverからO(m²)回の計数照会による多項式時間還元の数学的証明。q>=5の重みr=q−3に対する相異なる指数底のVandermonde補間とK0636の多項式ビット長整数座標構成。有限独立照合は補助的監査。'
---

# 任意の固定q>=5でも極大配置総数の計数は#P完全

K0635・K0636で未解決だった**q>=5の計数困難性**を解決した。任意の固定整数q>=5について、整数座標を明示入力する有限点集合の「q点共円または共線禁止」ゲームの全極大安全配置総数を求める問題は、**多項式時間チューリング還元の意味で#P完全**である。3点共線のない入力に制限しても#P困難性は残る。K0636のq=4と合わせ、任意の固定q>=4を覆う。

鍵は、K0602の極大配置総数

\[
T_q(H)=1+\sum_{R\text{ dominating}}(q-3)^{e_H(R)}
\]

を使うこと。元グラフGの各辺に、その両端だけと隣接する次数2の独立頂点をt個ずつ追加したH_tを考える。r=q−3>=2、S⊆V(G)、a(S)=SとV\\Sを横切る辺数、b(S)=G[S]の辺数とすれば

\[
T_q(H_t)-1=\sum_{S\subseteq V(G)}r^{b(S)}(1+r)^{t a(S)}(1+r^2)^{t b(S)}.
\]

\((1+r)^a(1+r^2)^b\) は異なる(a,b)で相異なる正整数となるため、\(t=1,\ldots,(m+1)(m+2)/2\) の値から有理数上のVandermonde補間で、各(a,b)を持つ部分集合の個数を厳密復元できる。特にa+b=mならSは頂点被覆なので、#VertexCoverが多項式回の照会で求まる。K0636により、各H_tを多項式ビット長の整数座標に変換できる。

[全称証明](../../experiments/graph-star-fixed-q-count-complexity-20261102/proof.md)・[独立検証器](../../experiments/graph-star-fixed-q-count-complexity-20261102/verify.py)を保存。72条件の厳密補間、144条件の支配集合直接列挙、7条件のq点禁止超辺直接極大列挙を独立照合し、不一致0。有限検査と無界の数学的証明は区別する。

**限界**：主張は多項式時間チューリング還元の意味であり、単一照会・計数保存還元は未証明。標準n×n全格子盤の計数困難性、空盤勝敗・Grundy値の困難性も示さない。
