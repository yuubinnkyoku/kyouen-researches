---
id: K0482
title: 二点禁止残局の木でGrundy値0〜8を実現する最小頂点数
kind: proposition
status: proved
topics:
- grundy
- residual-games
aliases: []
relations:
- type: depends_on
  target: K0108
  note: 実格子残局では二点残余禁止集合だけの場合に限って木モデルを使用できる
artifacts:
- path: research/experiments/game-structure/tree-grundy-minima-20261020/README.md
  role: proof
  note: 全非同型木列挙の完全性論証と計算結果・適用限界
- path: research/experiments/game-structure/tree-grundy-minima-20261020/verify_tree_minima.py
  role: verifier
  note: 葉付加とAHU正規形による列挙器
- path: research/experiments/game-structure/tree-grundy-minima-20261020/tree_occupied_mex.cpp
  role: verifier
  note: C++占有点集合mex再帰
- path: research/experiments/game-structure/tree-grundy-minima-20261020/verify_tree_minima_networkx.py
  role: verifier
  note: 独立NetworkX木列挙とPython残存誘導グラフmex
- path: research/experiments/game-structure/tree-grundy-minima-20261020/output/tree_minima_independent.json
  role: data
  note: 全木Grundy分布と達成例
- path: research/experiments/game-structure/tree-grundy-minima-20261020/output/tree_minima_networkx.json
  role: data
  note: 独立列挙・独立再帰の全分布
- path: research/experiments/knowledge-audit-20261021/README.md
  role: log
  note: 証明の論理監査・再実行範囲・判定
scope: 任意の非空の有限単純木の独立集合を一点ずつ増やす通常プレイゲーム。Grundy値0〜8の最小頂点数。共円ゲームの実際の格子残局としての実現性は含まない。
evidence: '2026-10-21監査。葉追加とAHU正規形の完全性を確認。全15頂点以下の木をC++占有mexとNetworkX+Python残存mexで再検査し全分布一致。 監査記録: research/experiments/knowledge-audit-20261021/README.md。'
---


# 木の二点禁止残局のGrundy最小頂点数

非空の木Tの独立集合を一点ずつ増やす通常プレイのGrundy値g(T)について、各k=0,...,8を実現する最小頂点数は

| k | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 最小頂点数 | 4 | 1 | 3 | 5 | 8 | 10 | 11 | 13 | 15 |

全15頂点以下の非同型木の分布を二つの異なる列挙・Grundy再帰で一致させた。特にg=8を実現する15頂点木は非同型で6種類。達成例の辺集合・全初手の子Grundy値はexperimentのREADMEとJSONに記載。

任意のn頂点木から葉を一つ除去すれば(n−1)頂点木になる。葉付加列挙は帰納的に漏れがなく、中心を根にしたAHU正規形で重複を除ける。n≤15を完全に検査したため、各達成値kに対してそれより小さい頂点数の非存在も証明対象内に収まる。

**限界**：実際の整数格子上の共円ゲーム残局でこれらの木を実現できるかは未解決。一般の三点・四点禁止集合を含む残局には適用できない。g=9の最小木頂点数は未確定。形式検証や11×11探索器での実速度評価は未実施。
