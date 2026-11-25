---
id: K0645
title: グラフ星型共円ゲームの最長直下の終局欠番は最小頂点被覆数で決まる
kind: proposition
status: proved
topics: [geometry, maximal-safe, statistics, strategy-length, variants, search-methods]
aliases: []
relations:
- type: depends_on
  target: K0602
  note: 任意q点グラフ星型構成と極大配置の支配集合母関数
- type: depends_on
  target: K0636
  note: 頂点被覆からのNP困難性を整数座標入力に移す多項式ビット長構成
artifacts:
- path: research/experiments/graph-star-vertex-cover-terminal-gap-20261103/proof.md
  role: proof
  note: 最小頂点被覆と中心を含む最大終局石数の等式、上端欠番、NP完全性の全称証明
- path: research/experiments/graph-star-vertex-cover-terminal-gap-20261103/verify.py
  role: verifier
  note: 2094グラフ・6282条件の被覆数照合と1927条件・2112168部分集合の禁止超辺直接完全列挙
scope: 辺を持つ任意有限単純グラフGと任意q>=4のK0602整数平面グラフ星型構成。計算量帰結は任意の固定q>=4の明示整数座標入力。標準全格子盤は対象外。
evidence: 最小頂点被覆と支配集合の欠損費用の全称的な必要十分等式、K0636の多項式座標構成、6282条件の独立有限監査。
---

# 最長終局石数のすぐ下に何石分の欠番があるか

グラフGの頂点数をn、辺数をe>=1、最小頂点被覆数をτ(G)、禁止点数をq>=4とする。K0602の整数共円・共線禁止構成の全点数は N=1+n+(q−3)e で、すべての禁止組は中心点Oを含む。

**全称定理：** Oを含む極大安全配置の最大石数は正確に

\[
\boxed{L_O=N-\tau(G)}.
\]

Oを含まない極大配置は、O以外のN−1点をすべて選ぶ一通りだけ。従って **τ(G)>=2なら** 終局長の最大値N−1と、二番目に大きい異なる値N−τの間に、**ちょうどτ−2個の連続欠番**がある。τ=1ではOを含む極大配置もN−1石になり、この二番目の値の公式は適用しない。

Oを含む最大石数の極大配置数はr=q−3の非負整数係数多項式で、その定数項はGの最小頂点被覆の個数に等しい。係数は支配集合Rについて |V\R|+e_G(R)=τ を満たすものを誘導辺数別に数えた値である。全称証明は

\[
\boxed{\tau(G)=\min_{R\text{ 支配集合}}\bigl(|V\setminus R|+e_G(R)\bigr)}
\]

による。任意のRでは、V\RにG[R]の各辺の一端を加えれば頂点被覆ができる。逆向きは最小頂点被覆の補集合が極大独立集合、すなわち支配集合になることから従う。

**計算量の帰結：** 任意の固定q>=4で、整数平面点集合と指定点O、閾値Lを入力として「Oを含むL石以上の極大安全配置があるか」を判定する問題はNP完全。さらに、指定点なしで「L石以上N−2石以下の極大安全配置があるか」もNP完全である。後者は還元前のグラフに孤立辺K₂を追加してτ>=2とし、唯一のN−1石配置を除外する。K0636の多項式ビット長整数座標実現により、三点共線のない点集合に制限してもNP困難性は残る。標準n×n全格子盤の計算量は主張しない。

[全称証明](../../experiments/graph-star-vertex-cover-terminal-gap-20261103/proof.md)と[独立検証器](../../experiments/graph-star-vertex-cover-terminal-gap-20261103/verify.py)を保存。n<=5の全1,094グラフとn=6の1,000グラフ、q=4,5,6の計6,282条件を検査し、さらに1,927条件で禁止超辺から2,112,168個の中心含有部分集合を直接列挙して全係数を照合。不一致0。有限監査と全称証明は区別する。
