---
id: K0605
title: グラフ星型共円ゲームの支配集合恒等式と次数非依存の最短配置非集中境界
kind: proposition
status: proved
topics: [geometry, maximal-safe, statistics, strategy-length, variants]
aliases: []
relations:
- type: depends_on
  target: K0602
  note: グラフ星型整数共円実現、極小横断集合分類、最短極大配置数を使用
- type: generalizes
  target: K0603
  note: 最大次数Δの非集中境界を全域森二色分割で強化
artifacts:
- path: research/experiments/graph-star-domination-bound-20261101/proof.md
  role: proof
  note: 支配集合恒等式、全域森二色分割による全称上界とq=4の無条件指数的非集中
- path: research/experiments/graph-star-domination-bound-20261101/verify.py
  role: verifier
  note: 792グラフ・重み条件の独立列挙と12条件の禁止超辺全部分集合列挙
scope: K0602の整数平面グラフ星型構成、任意q>=4、孤立頂点なし・最小次数2以上の有限単純グラフ。標準全格子盤は対象外。
evidence: K0602の横断集合分類と全域森二色分割の全称数学的証明。792条件の厳密有理数照合、12条件の超辺直接完全列挙。
---

# 最短極大配置の非集中を、最大次数が増えるグラフにも拡張

禁止点数q>=4、r=q-3、有限単純グラフG=(V,E)の頂点数t、辺数e、最小次数δ>=2、最大次数Δとする。K0602の整数共円構成では最短極大配置数M=r^e、全極大配置数Tは

\[
\boxed{T=1+\sum_{U\text{ が }G\text{ の支配集合}}r^{e(U)}}.
\]

さらに全域森の二色分割を使うと、**全グラフに対して**

\[
\boxed{\frac MT\le\left[r^{-e}-1+
(1+r^{-\Delta})^{\lceil t/2\rceil}+
(1+r^{-\Delta})^{\lfloor t/2\rfloor}\right]^{-1}}.
\]

K0603の最大次数上界で現れた指数\(\lceil t/(\Delta+1)\rceil\)を、次数に依存しない約t/2へ改善した。

**q=4では** \(T=1+d(G)\)（d(G)は支配集合数）、\(M=1\)なので

\[
\boxed{\frac MT\le\frac1{2^{\lceil t/2\rceil}+2^{\lfloor t/2\rfloor}}\to0.}
\]

これはΔが無制限に増大するグラフ族でも成立する。固定q>=5では \(t r^{-\Delta}\to\infty\) が最短割合0への十分条件であり、特に\(\Delta\le(1-\varepsilon)\log_r t\) なら非集中。

数学的証明と独立検証はartifacts参照。全称結論を有限列挙から推測したものではない。整数点を自由に配置するK0602の構成に限り、標準11×11全盤の勝敗やs_11は導かない。
