---
id: K0300
title: 効く極小三点辺の最小接続木は三葉上のK1,3
kind: proposition
status: proved
topics:
- residual-games
relations: []
aliases: []
artifacts:
- path: research/experiments/original-claims/reports/round44-three-stone-cliques-and-tree-minima.md
  role: proof
  note: 最小接続木K1,3の一般証明と格子実現
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round44_tree_clique_verified.json
  role: data
  note: 明示証人と有限照合結果
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/scripts/round44_tree_and_clique.py
  role: verifier
  note: 証人の独立検算
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 効く極小三点辺の最小接続木は三葉上のK1,3

木の二点競合構造に極小三点辺 (e) を追加してGrundy値が変わる場合を考える。三点辺の三頂点は二点競合では互いに独立なので、この三点を含む最小接続部分木は少なくとも4頂点を必要とする。

4頂点で独立な三葉を接続できる木は中心1点と三葉からなる (K_{1,3}) だけであり、4×4の共円ゲーム残局にこの型を実現して実際にGrundy値が変わる明示例がある。従って「効く三点制約」の最小接続型はK1,3で確定する。

これは最小型の定理であり、K0193に残る「より大きな木で距離・共有パスから効果を分類できるか」という一般分類を解いたものではない。
