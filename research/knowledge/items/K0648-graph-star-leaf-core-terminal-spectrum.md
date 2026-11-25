---
id: K0648
title: グラフ星型共円ゲームの全終局長は葉と高次数核で計数でき、最短直上の欠番は次数2で決まる
kind: proposition
status: proved
topics: [geometry, maximal-safe, statistics, strategy-length, variants, search-methods]
aliases: []
relations:
- type: depends_on
  target: K0602
  note: グラフ星型共円構成と極大配置の支配集合による分類
- type: generalizes
  target: K0647
  note: 森に限らず任意グラフの終局長係数を葉と高次数核で分類する。ただし森の成分数表示や星森の部分和公式は別の系として維持する
artifacts:
- path: research/experiments/graph-star-leaf-core-spectrum-20261103/proof.md
  role: proof
  note: 葉と高次数核の全終局長母関数、固定欠損の小核定理、次数2による最短直上欠番判定の全称証明
- path: research/experiments/graph-star-leaf-core-spectrum-20261103/verify.py
  role: verifier
  note: 5937条件の全分布直接照合、直上欠番条件と108条件の禁止超辺完全列挙
- path: research/experiments/graph-star-connected-kernel-20261103/proof.md
  role: proof
  note: 許容核の連結成分を次数制限付きで列挙し固定欠損係数を O(f(d)n^d(n+e)) に改善する全称証明
- path: research/experiments/graph-star-connected-kernel-20261103/verify.py
  role: verifier
  note: 連結核列挙と支配集合直接列挙の16720係数独立照合
- path: research/experiments/graph-star-fixed-defect-fpt-20261103/proof.md
  role: proof
  note: 競合グラフの有界次数と独立集合多項式の連結支持対数展開による f(d)(n+e) 算術演算の全称証明
- path: research/experiments/graph-star-fixed-defect-fpt-20261103/verify.py
  role: verifier
  note: 支配集合直接列挙との13047係数独立照合
- path: research/experiments/graph-star-fixed-defect-bit-fpt-20261103/proof.md
  role: proof
  note: 固定欠損計数の有理数除去と二進ビット計算量 O(f(d)L^5) の全称証明
- path: research/experiments/graph-star-fixed-defect-bit-fpt-20261103/verify.py
  role: verifier
  note: 16510係数の独立した整数置換・直接列挙照合
scope: 辺を持つ任意有限単純グラフGと任意固定または可変q>=4のK0602整数平面共円・共線禁止構成。標準全格子盤は対象外。
evidence: 葉・高次数核への一意分解、次数上界と連結核の分解列挙による全称証明。有限照合は独立監査。
---

# 全終局長の葉・高次数核公式と最短直上の欠番

G の辺数を e≥1、r=q−3、全点数を N=1+|V|+re、最短極大石数を s=N−e とする。L は次数2以上の頂点に隣接する葉の数、h は孤立辺 K₂ の成分数、C=e−L−h とする。

次数2以上の頂点集合 H の部分集合 B で、各 v∈B が B の外に隣接点を持つものを**許容核**と呼ぶ。a(B) は B に隣接する次数1頂点数、d(B)=Σ_{v∈B}(deg(v)−1)−e_G(B) とする。

**全称定理：** 全極大安全配置の石数別母関数は

\[
\boxed{P_{G,q}(u)=u^{N-1}
+u^s(r+2)^h\sum_{B\text{ 許容核}}
r^{C+a(B)-|B|-d(B)}(r+1)^{L-a(B)}u^{d(B)}.}
\]

各 r の指数は非負整数。さらに **|B|≤2d(B)** が常に成立する。連結成分分解と次数上界 **deg(v)≤d+1（v∈B、d(B)=d）** を併用すると、最短から d 石だけ長い終局の個数は、固定 d に対し **O(f(d)n^d(n+e))** 回の整数演算で厳密に計数できる（n=|V|、e=|E|、f(d) は d のみに依存）。旧上界 O(n^{2d}(n+e)) を改善する。全分布を同じ計算量で求められるという主張ではない。

特に **e≥3 のとき、s+1 石の極大配置が存在する必要十分条件は G に次数2の頂点があること**。e=2 では中心なしの極大配置が必ず s+1 を実現し、e=1 では s+1 は不可能。すべての q≥4 で成立する。

例えば三角形 K₃ の s+1 石配置数は 3r+3、3葉星 K_{1,3} では0、4頂点道 P₄ では2r+3、互いに素な孤立辺2本では1である。

[全称証明](../../experiments/graph-star-leaf-core-spectrum-20261103/proof.md)と[独立検証器](../../experiments/graph-star-leaf-core-spectrum-20261103/verify.py)を保存。全分布5,937条件、直上係数7,836条件、禁止超辺からの直接完全列挙108条件で不一致0。数学的証明と有限照合は区別する。K0647 の森における成分数公式とは異なる、任意グラフの**係数ごとの局所構造分類**である。標準全格子盤や11×11空盤勝敗は対象外。


## 固定欠損係数の改善（2026-11-03）

許容核 B の誘導連結成分はそれぞれ正の欠損を持ち、欠損 d の核は高々 d 成分からなる。また、各核頂点の次数は d+1 以下、核の大きさは 2d 以下である。したがって次数制限付きの連結候補は O(f(d)n) 個しかなく、そのうち高々 d 個を非隣接に選ぶことで係数を計数できる。全称証明は[連結核列挙の証明](../../experiments/graph-star-connected-kernel-20261103/proof.md)、独立検証は[連結核検証器](../../experiments/graph-star-connected-kernel-20261103/verify.py)に保存。全16,720係数で支配集合直接列挙と一致（不一致0）。固定パラメータ容易性は未証明。

## 固定欠損係数は固定パラメータ容易（2026-11-03）

連結核を頂点とし、重複または隣接する核を競合させるグラフは、欠損上限 d に対して頂点数 O(f(d)n)、最大次数 f(d) 以下となる。重み付き独立集合多項式の対数を連結支持に分解すると、d 次までの係数は大きさ d 以下の連結支持だけから厳密に復元できる。従って **s+d 石の極大配置数は f(d)(n+e) 回の有理数・整数演算で計数できる**。従来の O(f(d)n^d(n+e)) を改善し、パラメータ d に関する固定パラメータ容易性を証明した（ビット演算量の主張ではない）。[全称証明](../../experiments/graph-star-fixed-defect-fpt-20261103/proof.md)と[独立検証器](../../experiments/graph-star-fixed-defect-fpt-20261103/verify.py)を保存。13,047係数で直接列挙と一致、不一致0。

## 二進ビット計算量でも固定パラメータ容易（2026-11-03）

算術 FPT の候補重みの分母を、欠損次数に応じた整数置換で消去できる。各連結核の欠損を t、重みを w とすると、D=r^T(r+1)^T、T=2d(d+1)+3d により D^t w は整数となる。整数多項式 Q(x)=Z_J(Dx) を連結支持の対数展開で計算し、H=lcm(1,…,d) 倍の整数対数係数から、割り切れる漸化式で係数を復元する。従って、入力長の上界 L=n+e+⌈log₂(q+1)⌉ に対して **O(f(d)L⁵) ビット演算**の厳密計数が成立する。有理数演算は不要。組合せ入力 G,q,d に対する結果であり、標準格子盤は対象外。[全称証明](../../experiments/graph-star-fixed-defect-bit-fpt-20261103/proof.md)と[独立検証器](../../experiments/graph-star-fixed-defect-bit-fpt-20261103/verify.py)を保存。16,510係数で不一致0。
