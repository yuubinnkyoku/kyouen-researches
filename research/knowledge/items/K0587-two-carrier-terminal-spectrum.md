---
id: K0587
title: 二担い手q点禁止ゲームの全極大配置数・終局長分布・最小最大石数は閉形式で決定できる
kind: proposition
status: proved
topics: [geometry, variants, residual-games, maximal-safe, maximum-safe, strategy-length]
aliases: []
relations:
- type: depends_on
  target: K0586
  note: 同じ二担い手容量制約モデルを対象とする
- type: generalizes
  target: K0582
  note: N=2qの七型に限られた極大配置計数を任意の二担い手盤に拡張
- type: generalizes
  target: K0584
  note: N=2q+1の十二型に限られた極大配置計数を任意の二担い手盤に拡張
artifacts:
- path: research/experiments/two-carrier-terminal-20261031/proof.md
  role: proof
  note: 全極大集合の飽和場合分けによる全称証明、終局長・人数別履歴数
- path: research/experiments/two-carrier-terminal-20261031/verify.py
  role: verifier
  note: 156構成1296960部分集合の点別極大判定と24構成の順序付き履歴独立照合
scope: q≥4、|A|=q+a、|B|=q+b、|A∩B|=c≤2、外部自由点z≥0、A/B以外の禁止集合なし。極大配置と順序付き完了履歴の全称分類。
evidence: 飽和/非飽和の排反分類による数学的証明。156構成の全部分集合および24構成の全着手列で独立検証。
---

# 二担い手の極大配置と終局長の全称閉公式

q≥4、|A|=q+a、|B|=q+b、a,b≥0、c=|A∩B|≤2、外部点数z、x=q+a−c、y=q+b−c とする。安全集合はA/Bのそれぞれに高々q−1点を含む。

極大安全集合の石数kごとの個数M_kの母関数は

\[
\begin{aligned}
\sum_kM_kX^k={}&\sum_{t=0}^c\binom ct\binom{x}{q-1-t}\binom{y}{q-1-t}X^{2q-2-t+z}\\
&+\mathbf1_{c=2,b=0,a\ge1}\binom{x}{q-1}X^{2q-3+z}\\
&+\mathbf1_{c=2,a=0,b\ge1}\binom{y}{q-1}X^{2q-3+z}.
\end{aligned}
\]

極大石数の支持は、c=0で1長、c=1で連続2長、c=2で連続2長（a=0またはb=0）または連続3長（a,b≥1）に**厳密に**限られる。したがって(s,K)は順に(2q−2+z,2q−2+z)、(2q−3+z,2q−2+z)、(2q−4+z,2q−3+z)、(2q−4+z,2q−2+z)。

長さkの合法完了履歴数はM_k k!。r人巡回の場合、j番目が最後の石を置く履歴数はk≡j (mod r) の履歴数を合計すればよい。これは履歴の計数であり、r人対戦の最適戦略の解決を意味しない。

**根拠**：少なくとも片方の担い手は飽和する。両方飽和の場合は共有点数tで分類でき、片方のみ飽和する例外はc=2かつ非飽和側がちょうどq点、共有点を0個選ぶ場合に限られる。数学的な全称証明と独立列挙の詳細は proof.md を参照。

**限界**：平面の共円・共線盤に適用するには、q点以上を含む担い手がこの二本だけであることが必要。大盤の任意残局や第三担い手のある盤には適用しない。
