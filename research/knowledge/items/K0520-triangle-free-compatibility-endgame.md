---
id: K0520
title: 共存グラフに三角形がない遺伝的配置ゲームは高々2手で終局し孤立点の有無でP/Nが決まる
kind: proposition
status: proved
topics: [search-methods, verification, variants]
aliases: []
relations:
- type: supports
  target: K0505
  note: 7立方5点禁止版の終盤を正確に短縮する。空盤の勝敗証明ではない
artifacts:
- path: research/experiments/cube-q5-seven-hybrid-20261023/graph.md
  role: proof
  note: 全称補題の証明・実装・独立検査の範囲
- path: research/experiments/cube-q5-seven-hybrid-20261023/graph.cpp
  role: solver
  note: 候補数8以下で共存グラフを作り通常の全AND/OR証明書へ展開する探索器
- path: research/experiments/cube-q5-seven-hybrid-20261023/endgames-current-verified.json
  role: data
  note: 7立方24終盤の従来探索との一致と全証明書の独立Bareiss検査
- path: research/experiments/cube-q5-seven-hybrid-20261023/regression-graph.json
  role: data
  note: 既知3立方20根、tree置換、中断再開、不正checkpoint拒否の回帰
scope: 有限共有盤・遺伝的合法集合族・1手1点追加・通常プレイ、共存グラフが三角形を持たない局面
evidence: 3点の同時追加可能性は3対の共存を含意することと高々2手の完全な場合分け
---

合法局面Sと合法追加点集合Vに対し、異なるp,q間の辺の条件をS∪{p,q}が合法であること
とする。このグラフに三角形がなければ、3点を追加できない。もし追加できたなら、
合法性の遺伝性により各2点を追加でき、三角形になる。

孤立点がある場合、その点を置けば相手の合法手が0なのでN。
孤立点がない場合、どの手pの後にも隣接点qを置ける。3点目は置けないため各子局面は
Nで、元の局面はP。Vが空なら終端Pである。

5点共平面・共球面禁止ゲームにも適用できるが、三角形を持つ局面には適用しない。
7立方の空盤や全局面の分類を主張しない。
