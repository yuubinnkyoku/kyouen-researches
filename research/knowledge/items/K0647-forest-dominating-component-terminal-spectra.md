---
id: K0647
title: 森の極大終局長は支配誘導成分数で決まり、星森では任意の部分和スペクトルを実現できる
kind: proposition
status: proved
topics: [geometry, maximal-safe, statistics, strategy-length, variants]
aliases: []
relations:
- type: depends_on
  target: K0602
  note: グラフ星型共円構成の極大配置の支配集合母関数
artifacts:
- path: research/experiments/forest-terminal-spectrum-20261103/proof.md
  role: proof
  note: 森の誘導辺数恒等式、星森の積公式、道の連続終局長の全称証明
- path: research/experiments/forest-terminal-spectrum-20261103/verify.py
  role: verifier
  note: 1441木・4323支配集合照合、56星森照合、24禁止超辺完全列挙、24道照合
scope: 少なくとも一辺を持つ任意有限単純森G、任意整数q>=4のK0602整数共円・共線禁止構成。標準全格子盤は対象外。
evidence: 森の誘導辺数=頂点数-成分数の全称恒等式、星ごとの支配集合分類、道の明示支配集合構成。有限監査は独立照合。
---

# 森の終局長を支配集合の連結成分数だけで特徴付ける

n=|V|、e=|E|≥1、r=q−3≥1、N=1+n+re とする。森 G の支配集合 R の誘導成分数を c(R) とすると、K0602の極大安全配置母関数は

\[
\boxed{P_{G,q}(u)=u^{N-1}+\sum_{R\text{ 支配集合}}r^{e_G(R)}u^{N-n+c(R)}}.
\]

従って中心点を含む終局長の種類は N−n+c(R) に一致する。森の連結成分数を k、最大独立集合の大きさを α(G) とすると、k≤c(R)≤α(G) であり両端は必ず達成される。途中は必ずしも埋まらない。

特に G=⊔_i K_{1,d_i}（d_i≥1）では s=N−e として

\[
\boxed{P_{G,q}(u)=u^{N-1}+u^s\prod_i((q-2)^{d_i}+u^{d_i-1})}.
\]

中心点を含む終局長差は正確に d_i−1 の**部分和全体**である。任意の正整数列 a_i に対し d_i=a_i+1 とすれば、その部分和集合を終局長差として実現できる。k 個の K_{1,3} なら差は 0,2,...,2k のみで、内部に任意個数の欠番が生じる。

対照的に、道 P_n（n≥2）では中心点を含む終局長は **s から s+⌈n/2⌉−1 まで連続**する。各値を実現する支配集合を明示構成できる。これらは全 q≥4 の数学的定理であり、標準全格子盤や最適戦略の終局長に関する主張ではない。

[全称証明](../../experiments/forest-terminal-spectrum-20261103/proof.md)と[独立検証器](../../experiments/forest-terminal-spectrum-20261103/verify.py)を保存。全1,441木、星森56条件、禁止超辺からの直接完全列挙24条件、道24条件で不一致0。有限検証と全称証明は区別する。
