---
id: K0679
title: 有界次数グラフ星型の終局長は単点・隣接対の複合ポアソンで近似でき、正則族の臨界尺度は普遍的
kind: proposition
status: proved
topics: [geometry, maximal-safe, statistics, strategy-length, variants]
aliases: []
relations:
- type: depends_on
  target: K0602
  note: グラフ星型整数共円実現と極大配置の削除集合・重み公式
- type: depends_on
  target: K0603
  note: 閾値の低q側に用いる既存の独立集合による非集中評価を証明内で再掲
artifacts:
- path: research/experiments/graph-star-bounded-degree-poisson-20261107/proof.md
  role: proof
  note: 成分除去単射・連結成分重み評価・独立候補への条件付けによる全称証明
- path: research/experiments/graph-star-bounded-degree-poisson-20261107/verify.py
  role: verifier
  note: 全12332グラフの削除集合直接列挙、単点と隣接対の有理数監査、禁止超辺独立列挙
- path: research/experiments/graph-star-bounded-degree-poisson-20261107/output/audit.json
  role: data
  note: 厳密有限監査の集計と、大きいサイクル・K4直和の非厳密な診断表
- path: research/log/2026-11-07-bounded-degree-terminal-poisson.md
  role: log
  note: 既知の特殊族からグラフ形状によらない臨界則と隣接対補正へ至る経緯
scope: K0602の整数平面有限点構成、最小次数δ>=2・最大次数Δの任意有限単純グラフ、q>=4。有限誤差評価はr=q-3>Δ²。正則族の極限ではδ固定、n→∞。極大配置の一様分布。
evidence: 成分除去単射と連結集合の歩道計数による全称証明。全12332グラフ・36996有理数分布照合、22禁止超辺完全列挙、30整数転送行列照合は有限独立監査。
---

## 命題と対象

K0602 の構成で、グラフ G は n 頂点、e 辺、最小次数 δ≥2、最大次数 Δ、
r=q−3、N=1+n+re、最短極大石数 s=N−e とする。
**全極大安全配置から一様に選んだ**石数を H とする。

任意の r>Δ² について、全て相互に独立な

\[
 Z_v\sim\operatorname{Pois}\bigl((1+r^{\deg v})^{-1}\bigr),\quad
 Z_{ab}\sim\operatorname{Pois}\bigl((1+r^{\deg a+\deg b-1})^{-1}\bigr)
\]

を用いると、超過 H−s は

\[
 \widehat D=\sum_v(\deg v-1)Z_v+
 \sum_{ab\in E}(\deg a+\deg b-3)Z_{ab}
\]

で、次の**全変動距離の明示上界**以内に近似できる：

\[
 \boxed{
 d_{TV}(\mathcal L(H-s),\mathcal L(\widehat D))\le
 {n\Delta^4\over r^{2\delta}(1-\Delta^2/r)}+
 {(n+e)((\Delta+1)^2+1)\over r^{2\delta}}+r^{-e}.}
\]

単点項だけの近似にも、
nΔ²/[r^{2δ−1}(1−Δ²/r)]+(n+e)/r^{2δ}+r^{−e} という全称上界がある。

## 正則グラフの普遍的な閾値と補正

固定 δ≥2 の**どの δ 正則グラフ列**でも、e=δn/2、

\[
 A_n\sim\operatorname{Pois}\left({n\over1+r^\delta}\right),\quad
 B_n\sim\operatorname{Pois}\left({\delta n/2\over1+r^{2\delta-1}}\right)
\]

を独立とすれば、臨界域 r/n^{1/δ}→c∈(0,∞) で

\[
 \boxed{d_{TV}\bigl(\mathcal L(H-s),
 \mathcal L((\delta-1)A_n+(2\delta-3)B_n)\bigr)=O(1/n).}
\]

従って H−s は全変動距離で (δ−1)Poisson(c^{−δ}) に収束し、最短終局割合は

\[
 \boxed{
 \Pr(H=s)\longrightarrow
 \begin{cases}
 0,&r/n^{1/\delta}\to0,\\
 e^{-c^{-\delta}},&r/n^{1/\delta}\to c\in(0,\infty),\\
 1,&r/n^{1/\delta}\to\infty.
 \end{cases}}
\]

臨界域では最短割合の一次補正も
exp(−n/(1+r^δ)−(δn/2)/(1+r^{2δ−1})) に O(1/n) 以内で一致する。
連結性、二部性、三角形の有無などを仮定せず、隣接対補正の先頭項まで普遍的である。
δ=2 なら一つのポアソン分布で近似でき、δ=3 なら跳躍幅2と3の二成分になる。

## 根拠と限界

削除集合を連結成分に分解すると、ある成分 B が出現する確率はその重み r^{−L(B)} 以下。
全ての許容な連結 B（|B|≥2）について L(B)≥2δ+|B|−3 を証明し、
大きさ3以上の成分の総重みを一様に抑える。残る単点・辺を独立に選び、
競合確率を評価して、独立ポアソン変数へ置き換える。
[全称証明](../../experiments/graph-star-bounded-degree-poisson-20261107/proof.md)を参照。

全12332ラベル付きグラフ（n=3..6、最小次数≥2）で単点24664条件・隣接対12332条件の
有理数不等式を照合。禁止超辺からの独立全列挙22条件・363136局面と整数転送行列30条件でも一致。
有理数で直接監査するのは Poisson への置換前の独立 Bernoulli 近似であり、
Poisson への追加誤差は全称的な距離不等式で保証する。
大きい族の浮動小数点表は診断だけに使う。

O(1/n) は n 依存平均を使った二成分近似の誤差率。固定極限分布への収束速度は別である。
K0607 の固定q・増大次数を持つ特殊族とは量化が異なり、その項目の置換ではない。
標準 n×n 全格子盤の勝敗・最適戦略・ランダム着手順の分布には適用しない。
