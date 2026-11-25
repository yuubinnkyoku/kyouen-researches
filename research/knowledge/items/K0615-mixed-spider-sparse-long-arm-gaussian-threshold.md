---
id: K0615
title: 混合枝長2・3の蜘蛛木で疎な長枝が二峰混合を正規極限へ変える鋭い条件
kind: proposition
status: proved
topics: [geometry, maximal-safe, statistics, strategy-length, variants]
aliases: []
relations:
- type: depends_on
  target: K0602
  note: 任意グラフの整数平面q点共円実現と極大配置母関数
- type: generalizes
  target: K0612
  note: 長さ2のみの場合の禁止4点版二峰混合を含む
- type: generalizes
  target: K0613
  note: 長さ3のみの場合の禁止4点版正規極限を含む
- type: depends_on
  target: K0614
  note: 中心残存・削除の枝別母関数を異長枝に拡張
artifacts:
- path: research/experiments/mixed-spider-critical-20261102/proof.md
  role: proof
  note: 異長枝の厳密母関数、有限誤差、正規極限の必要十分条件、固定長枝数の二点混合の証明
- path: research/experiments/mixed-spider-critical-20261102/verify.py
  role: verifier
  note: グラフ削除24条件・禁止超辺9条件628032部分集合・総数49条件の独立照合
scope: K0602の整数平面実現による長さ2の枝n本・長さ3の枝k本を持つ蜘蛛木、禁止4点版q=4、n+k>=1。漸近はn→∞でk=k(n)任意の非負整数、極大配置一様分布。標準全格子盤と無作為着手順は対象外。
evidence: 中心状態で分解した母関数の全称組合せ証明、独立Bernoulli和への全変動距離評価、Lindebergの中心極限定理、二点混合の厳密漸近。有限独立完全列挙。
---

# 禁止4点版の二峰混合は、長さ3の枝が無界個あるだけで消える

中心から長さ2の枝をn本、長さ3の枝をk本伸ばす木をK0602の自由な整数点集合として実現する。全点数N=2+4n+6k、最短極大石数s=2+2n+3kとする。極大安全配置の石数別母関数は、全n,k>=0、n+k>=1について

\[
\boxed{P_{n,k}(u)=u^s(2+u)^n(2+4u)^k
+u^{s+n+k-1}\{3^n(4+u)^k-2^k\}
+u^{s+2n+3k-1}.}
\]

極大配置を一様に選んだ石数をHとし、独立なX~Bin(n,1/3)、Y~Bin(k,2/3)を置くと、**任意の有限n,k**について

\[
\boxed{d_{TV}(\mathcal L(H-s),\mathcal L(X+Y))\le(5/6)^k.}
\]

特にn→∞、k=k(n)のとき、次の必要十分条件が成立する。

\[
\boxed{\frac{H-s-(n+2k)/3}{\sqrt{2(n+k)/9}}\Rightarrow N(0,1)
\quad\Longleftrightarrow\quad k\to\infty.}
\]

対照的に、kを固定してn→∞とすると、終局石数の巨視的分布は

\[
\boxed{\frac{H-s}{n}\Rightarrow
\frac{6^k}{6^k+5^k}\delta_{1/3}
+\frac{5^k}{6^k+5^k}\delta_1.}
\]

k=0はK0612の等重み二峰混合に一致する。**kがnに比べてどれほど少なくても、k→∞だけで正規極限に変わる**（例えばk=⌈log log(n+3)⌉）。一方、kが有限個にとどまるなら二峰混合が残る。これは固定枝長ごとの分類K0614には含まれない、混合枝長の鋭い相転移である。

[全称証明](../../experiments/mixed-spider-critical-20261102/proof.md)・[独立検証器](../../experiments/mixed-spider-critical-20261102/verify.py)。グラフ削除24条件、禁止超辺直接列挙9条件・628,032部分集合、総数49条件で不一致0。無限族の結論は数学的証明であり有限列挙の外挿ではない。標準11×11盤の勝敗や無作為な着手順の終局分布は述べない。
