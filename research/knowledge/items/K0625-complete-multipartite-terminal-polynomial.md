---
id: K0625
title: 完全多部グラフ型q点共円ゲームの部数無制限・極大終局長母関数多項式時間計数
kind: proposition
status: proved
topics: [geometry, maximal-safe, statistics, strategy-length, variants]
aliases: []
relations:
- type: depends_on
  target: K0602
  note: 任意グラフの整数共円実現と削除集合による極大配置母関数を使用
- type: generalizes
  target: K0604
  note: 完全二部グラフの母関数を任意部数の完全多部グラフへ拡張
artifacts:
- path: research/experiments/multipartite-terminal-20261102/proof.md
  role: proof
  note: 残存部の支持数による分類と残存点数・二乗和による多項式時間算法の全称証明
- path: research/experiments/multipartite-terminal-20261102/verify.py
  role: verifier
  note: 削除集合1506条件、禁止超辺47条件・483184部分集合、既知閉式186条件の独立照合
scope: 2部以上、各部正整数サイズの任意完全多部グラフG=K_(n1,...,nk)、任意q>=4のK0602整数平面共円・共線禁止構成。部数・部サイズは無制限。標準全格子盤は対象外。
evidence: 残存集合の必要十分分類と(A,Q,s)状態動的計画法による全称証明。有限完全列挙は独立の実装監査。
---

# 完全多部グラフなら部数が無制限でも終局長分布を多項式時間で厳密計数できる

K0602 のグラフ型 q 点共円・共線禁止構成で G=K_{n_1,...,n_k}、k>=2、n_i>=1、n=Σn_i、e=Σ_{i<j}n_i n_j、r=q−3、N=1+n+re とする。

各部の残存点数 a_i に対し A=Σa_i、E=Σ_{i<j}a_i a_j と置くと、全極大配置の石数別母関数は

\[
\boxed{P_G(u)=u^{N-1}+\sum_{j=1}^k u^{N-n+n_j}
+\sum_{|\{i:a_i>0\}|\ge2}
\left(\prod_i\binom{n_i}{a_i}\right)r^E u^{N-n+A-E}.}
\]

最後の和は各 0<=a_i<=n_i を走る。残存頂点が2部以上にまたがれば削除頂点はすべて残存隣接点を持ち、1部だけに残る場合はその部の全頂点が残る必要がある。K0602 の削除集合分類からこの場合分けは必要十分。

さらに E=(A²−Q)/2、Q=Σa_i² であるため、部を順に処理して (A,Q,残存非空部数を2で打ち切った値) を保持すれば、**O(n⁴) 回の整数演算**（係数ビット長は n と log q に関して多項式）で全係数を厳密に求められる。部数 k 自体が増大しても成立する。

特に q=4 での極大配置総数は

\[
\boxed{P_G(1)=2^n-\sum_i2^{n_i}+2k.}
\]

完全二部グラフの K0604、完全グラフの K0602 と一致する。例えば G=K_{m,m,m} は頂点被覆数・木幅がともに 2m と無界だが、今回の算法は m に関して多項式時間である。

[全称証明](../../experiments/multipartite-terminal-20261102/proof.md)と[独立検証器](../../experiments/multipartite-terminal-20261102/verify.py)を保存。削除集合1506条件、禁止超辺の全483184部分集合・47条件、既知閉式186条件を照合して不一致0。無界の結論は有限計算からの外挿ではない。

**限界**：完全多部グラフという構造を利用しており、任意グラフへの多項式時間計数、標準11×11盤の勝敗は主張しない。
