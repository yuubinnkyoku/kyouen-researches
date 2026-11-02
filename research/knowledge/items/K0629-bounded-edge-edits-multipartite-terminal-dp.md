---
id: K0629
title: 完全多部グラフの有限辺編集に対するq点共円極大終局長の固定パラメータ厳密計数
kind: proposition
status: proved
topics: [geometry, maximal-safe, statistics, strategy-length, variants]
aliases: []
relations:
- type: depends_on
  target: K0602
  note: 任意グラフの整数共円実現と削除頂点の隣接条件を使用
- type: generalizes
  target: K0625
  note: 完全多部グラフからの部内辺追加・部間辺削除を任意の有限数だけ許す
artifacts:
- path: research/experiments/multipartite-edge-edits-20261102/proof.md
  role: proof
  note: 例外端点を固定し残存部数2以上を(A,Q,s)動的計画法で計数する全称証明
- path: research/experiments/multipartite-edge-edits-20261102/verify.py
  role: verifier
  note: 削除集合10030条件と禁止超辺332条件・2117808点部分集合の独立完全照合
scope: 任意k>=2の完全多部グラフからt本の辺を追加または削除し、少なくとも1辺を残した任意有限単純グラフのK0602整数共円構成。q>=4、部割りと編集辺が入力。標準全格子盤は対象外。
evidence: 変更辺の全端点b個の残存選択と(A,Q,s)動的計画法によるO(2^b n^4)整数演算の全称証明。有限完全列挙は独立実装監査。
---

# 辺を少数変更しても完全多部グラフの厳密計数は効率的

完全多部グラフ G_0=K_(n_1,...,n_k)（k>=2）に対し、任意の t 本の辺を追加・削除して得た少なくとも1辺のグラフ G を考える。変更辺の全端点数を b<=2t、n=|V(G)|、q>=4 とすると、K0602 の整数平面上の q 点共円・共線禁止ゲームの全極大配置の石数別母関数は

\[
\boxed{O(2^b n^4)\subseteq O(4^t n^4)}
\]

回の整数演算で厳密に計算できる。係数のビット長は n と log q に関して多項式。部数、木幅、頂点被覆数に上限は不要である。

変更辺の端点集合 B の残存集合 T を固定すると、B 外の残存点が2部以上にまたがる場合、全削除点は必ず残存点に隣接する。この部分は (A,Q,s) の3情報による動的計画法で計数できる。B 外の残存が0部または1部の場合だけ、削除例外頂点の隣接関係と同じ部の削除点の救済条件を個別検査する。変更された誘導辺数の補正は T だけで決まる。

全称証明と実装は [proof.md](../../experiments/multipartite-edge-edits-20261102/proof.md)、[verify.py](../../experiments/multipartite-edge-edits-20261102/verify.py) に保存した。全順序付き部組成 n<=6 と変更辺数0〜2の9,530条件、追加500条件、禁止超辺の332条件・2,117,808部分集合で不一致0。有限検査を無界定理の証明に読み替えていない。

具体的には K_(2,2,2)、q=4 の極大配置総数58に対し、部間の1辺を削除すると56、同一部に1辺を追加すると60となる。分布は変わるが計算量の保証は残る。

**限界**：部割りと変更辺集合は入力として与える。一般グラフからその表現を発見する算法や、標準11×11盤の勝敗は対象外。変更辺数 t が無界のときの多項式時間計数は主張しない。
