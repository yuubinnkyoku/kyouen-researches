---
id: K0621
title: 擬森グラフ型q点共円ゲームの極大配置石数母関数を多項式時間で厳密計数
kind: proposition
status: proved
topics: [geometry, maximal-safe, statistics, strategy-length, variants]
aliases: []
relations:
- type: depends_on
  target: K0602
  note: 任意グラフの整数共円実現と削除頂点集合による極大配置分類を使用
- type: generalizes
  target: K0611
  note: 森の三状態計数を、各連結成分が高々一閉路を持つ擬森に拡張
artifacts:
- path: research/experiments/pseudoforest-terminal-dp-20261102/proof.md
  role: proof
  note: 付属木の三状態計数と閉路の隣接二状態4状態遷移による全称証明
- path: research/experiments/pseudoforest-terminal-dp-20261102/verify.py
  role: verifier
  note: 4290グラフ条件の独立削除集合照合と90条件180624部分集合の禁止超辺直接列挙
scope: 各連結成分が高々一つの閉路を持ち、少なくとも1辺を持つ任意有限単純擬森Gと任意整数q>=4のK0602自由整数平面点配置。標準全格子盤は対象外。
evidence: K0602の極大配置分類とK0611の木三状態を用いた閉路4状態動的計画法の全称証明。4290条件のグラフ独立列挙と90条件の禁止超辺直接完全列挙による補助検証。
---

# 閉路が一つある成分でも極大石数分布を厳密に高速計算できる

K0602のグラフ型q点共円実現で、各連結成分が木または単一閉路付きの木（擬森）なら、全極大配置の石数別母関数を、頂点部分集合の指数的全列挙を使わず多項式時間で計算できる。q≥4、r=q−3、N=1+|V|+r|E| とする。

木成分にはK0611の三状態漸化式を用いる。単一閉路を持つ成分は、閉路外の枝を同じ三状態で集約し、閉路上の頂点の残存・削除を隣接二状態4種類の遷移で計算する。各閉路頂点が削除され、枝内に残存隣接点がない場合は、閉路上の左右いずれかが残存するときに限り許す。両端残存の閉路辺には重みr/uを掛ける。

木成分寄与をZ_T、単一閉路成分寄与をZ_Cとすれば、厳密に

\[
\boxed{P_G(u)=u^{N-1}+u^N\prod_T Z_T(u)\prod_C Z_C(u).}
\]

各Z_Cは4状態の閉路遷移で閉路長に線形回数の多項式演算に帰着する。孤立頂点も許す。例えば三角形に葉を一つ付けたグラフでは、q=4で **2u^5+6u^6+3u^7+u^8**、q=5で **24u^9+15u^{10}+4u^{11}+u^{12}** を得る。

[全称証明](../../experiments/pseudoforest-terminal-dp-20261102/proof.md)と[独立検証器](../../experiments/pseudoforest-terminal-dp-20261102/verify.py)を保存。4290条件のグラフ削除集合完全列挙と、90条件・180624部分集合の禁止超辺直接列挙が一致した。有限検証から一般定理を外挿したものではない。複数の閉路が同一成分にある一般グラフへの多項式時間拡張は本定理の対象外。
