---
id: K0622
title: 任意多重閉路グラフの頂点被覆数による極大配置厳密計数とK2m相転移
kind: proposition
status: proved
topics: [geometry, maximal-safe, statistics, strategy-length, variants]
aliases: []
relations:
- type: depends_on
  target: K0602
  note: 任意有限単純グラフの整数共円実現と極大配置削除集合の分類を使用
artifacts:
- path: research/experiments/vertex-cover-terminal-dp-20261102/proof.md
  role: proof
  note: 3^k包除原理の全称証明、K2m明示式、q=4とq>=5の極限分布
- path: research/experiments/vertex-cover-terminal-dp-20261102/verify.py
  role: verifier
  note: 8067グラフ条件、996別被覆、100禁止超辺条件472592部分集合、K2m式80条件を照合
scope: 少なくとも1辺を持つ任意有限単純グラフG、任意q>=4、頂点被覆Cが与えられたK0602自由整数平面点配置。標準全格子盤は対象外。
evidence: 頂点被覆外の独立集合を用いる包除原理の全称証明とK2mの閉形式・確率極限の証明。有限完全列挙は独立の補助監査。
---

# 多重閉路があっても小さい頂点被覆があれば厳密計数できる

K0602 のグラフ型 q 点共円・共線禁止構成で、G=(V,E)、q>=4、r=q−3、N=1+|V|+r|E| とする。頂点被覆 C の大きさを k とすれば、全極大安全配置の石数別母関数は **O(3^k poly(N,log q))** 時間で厳密に求められる。閉路数に制限はない。C の外が独立集合になることを利用し、削除被覆頂点が残存隣接点を持つ条件を包除原理で処理する。

特に完全二部グラフ K_{2,m} (m>=1) では

\[
\boxed{P(u)=u^{N-1}+u^{N-2m}(r^2+u)^m+2((r+1)^m-1)u^{N-m-1}+u^{N-2},\quad N=3+m+2rm.}
\]

q=4 では一様極大配置の石数 H_m に対し

\[
\boxed{\frac{H_m-(N-2m)}m\Rightarrow\frac13\delta_{1/2}+\frac23\delta_1,}
\]

q>=5 では p=1/(r²+1) として

\[
\boxed{\frac{H_m-(N-2m)-mp}{\sqrt{mp(1-p)}}\Rightarrow N(0,1).}
\]

後者の二項分布との全変動距離は \(2(r+1)^m/((r^2+1)^m+2(r+1)^m)\) 以下。m>=3 で K_{2,m} は同一成分に複数の閉路を持つため、擬森に関する K0621 では扱えなかった族である。

[全称証明](../../experiments/vertex-cover-terminal-dp-20261102/proof.md)と[独立検証器](../../experiments/vertex-cover-terminal-dp-20261102/verify.py)を保存。8067グラフ条件、996別被覆、100禁止超辺条件・472592部分集合、K_{2,m}式80条件を照合し不一致0件。無界結論は有限検算からの外挿ではない。標準11×11全盤の勝敗は対象外。
