---
id: K0598
title: 任意本数の禁止集合で全2^(r-1)種類の終局長集合を同一総点数・同一禁止点数で実現
kind: proposition
status: proved
topics: [maximal-safe, residual-games, variants, strategy-length]
aliases: []
relations:
- type: generalizes
  target: K0597
  note: 五禁止集合の16種類実現を任意rへ拡張し、q点一様性と総点数の共通化も与える
- type: depends_on
  target: K0596
  note: 極大安全集合と包含極小横断集合の対応、私有証人辺
artifacts:
- path: research/experiments/arbitrary-r-terminal-spectra-20261101/proof.md
  role: proof
  note: 入れ子型所属署名による全称構成、極大配置数の閉公式、同一N=rqへの均一化
- path: research/experiments/arbitrary-r-terminal-spectra-20261101/verify.py
  role: verifier
  note: 165構成・638340部分集合の点別独立完全検算、q点一様化版の極小横断集合列挙
scope: 任意r>=2、q>=rの抽象q点禁止集合ゲーム。各禁止集合に私有点あり、総点数N=rqを共通に固定。整数平面上の共円・共線実現や標準11×11全盤は対象外。
evidence: 入れ子型所属署名と極小横断集合の完全分類による全称数学的証明。165構成の独立点別列挙で不一致0。
---

# 任意の終局長集合を指定できる

任意のr>=2、q>=r、D⊆{1,...,r-1}について、**ちょうどr本の相異なるq点禁止集合・総点数N=rq・各辺に私有点あり**の抽象一点追加ゲームで、極大安全集合の石数が正確に

    {N-r} ∪ {N-k : k∈D}

となるものが存在する。したがってN-rを含む{N-r,...,N-1}の2^(r-1)種類の終局長集合が、同一r,q,Nのもとですべて実現する。

構成は、各k∈Dに最初のr-k+1辺に属する特殊点v_kを置き、各辺iにm_i=q-#{k∈D:i<=r-k+1}個の私有点を追加し、さらにz=Σ_{k∈D}(r-k)個の自由点を置く。m_i>=1、全辺サイズq、総点数rq。特殊点の所属署名は入れ子なので極小横断集合は特殊点を高々一つしか含まない。極大安全集合の母関数は

    P(u)=(∏_i m_i)u^(N-r) + Σ_{k∈D}(∏_{i=r-k+2}^r m_i)u^(N-k).

例としてr=q=6、D={1,3,5}ではP(u)=3600u^30+400u^31+25u^33+u^35、終局長32・34が欠番となる。

**証拠と限界**：無界のr,qに対する結論は数学的全称証明。独立検証器は165構成と638,340部分集合を含む点別列挙を照合し不一致0。禁止集合は抽象的であり、二円の交点高々2という幾何制約を満たすとは限らない。標準11×11格子の勝敗を決定しない。
