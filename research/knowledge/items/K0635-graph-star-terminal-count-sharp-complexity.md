---
id: K0635
title: グラフ星型4点共円ゲームの極大終局総数計数は組合せ入力で#P完全
kind: proposition
status: proved
topics: [geometry, maximal-safe, statistics, variants, search-methods]
aliases: []
relations:
- type: depends_on
  target: K0602
  note: グラフ星型禁止4点組と極大配置総数1+支配集合数の恒等式
artifacts:
- path: research/experiments/graph-star-count-complexity-20261102/proof.md
  role: proof
  note: #VertexCoverから分割グラフへの単一照会・B進最高位抽出還元の全称証明
- path: research/experiments/graph-star-count-complexity-20261102/verify.py
  role: verifier
  note: 814グラフの桁抽出、1255条件の支配集合直接列挙、10条件の禁止超辺直接列挙
scope: q=4のK0602グラフ星型ゲーム。入力は有限単純グラフまたは明示的4一様禁止超辺。整数平面での実現可能性はK0602を使用するが座標の多項式ビット長は主張しない。
evidence: #VertexCoverからの単一照会・多項式時間後処理による還元と、候補極大性の多項式時間検査による#P所属の数学的証明。有限列挙は独立監査。
---

# 一般グラフ星型の極大終局総数は#P完全

K0602の4点禁止ゲームをグラフHの組合せ表現で入力する。全極大安全配置の数T(H)=1+d(H)（d(H)は支配集合数）を求める問題は**#Pに属し、単一照会・多項式時間後処理で#P困難**である。従って多項式時間チューリング還元の意味で#P完全。

証明は#VertexCoverからの明示的還元。元グラフGの孤立頂点を除き、n頂点m辺とする。Gの全頂点をクリークにし、各辺の両端にだけ隣接するt=n+1個の独立な複製頂点を加えた分割グラフHを作る。B=2^t、Sが覆うGの辺数をc(S)とすると

\[
T(H)=2+\sum_{\varnothing\ne S\subseteq V(G)}B^{c(S)},\qquad
\boxed{\#VC(G)=\left\lfloor\frac{T(H)-2}{B^m}\right\rfloor}.
\]

各桁の係数和が2^n−1<Bなので繰上がりはなく、最高位の係数が頂点被覆数になる。孤立頂点があれば元の回答にその数の2冪を掛ける。Hはn+tm頂点、n(n−1)/2+2tm辺で多項式サイズ。極大性は多項式時間で検査できる。

[全称証明](../../experiments/graph-star-count-complexity-20261102/proof.md)と[独立検証器](../../experiments/graph-star-count-complexity-20261102/verify.py)を参照。814グラフで最高位抽出、1,255条件でHの支配集合を直接列挙、10条件で禁止4点組から極大集合を直接列挙し、不一致0。

**範囲の注意**：整数平面上で同じ禁止組を実現できることはK0602が証明しているが、その整数座標のビット長が入力サイズに対して多項式であるとは本稿では示していない。従って**整数座標を明示入力する幾何ゲームの#P完全性は主張しない**。標準全格子盤の勝敗・Grundy値やq≥5の計数困難性も対象外。K0621〜K0632の高速計数法とは、一般入力に構造制限を課すことで整合する。
