---
id: K0462
title: 残余禁止集合が3個以下かつ各4点以下ならGrundy値は3以下
kind: proposition
status: proved
topics:
- grundy
- residual-games
- search-methods
- variants
aliases: []
relations:
- type: depends_on
  target: K0002
  note: 通常プレイのGrundy再帰と直和定理
artifacts:
- path: research/experiments/game-structure/reports/residual_three_edges_q4_20261018.md
  role: proof
  note: 有限型への数学的帰着、全称命題の計算機支援証明、反例、適用限界
- path: research/experiments/game-structure/scripts/residual_three_edges_q4_20261018.py
  role: verifier
  note: 残点数ベクトルによる全型・全安全状態の再帰
- path: research/experiments/game-structure/scripts/residual_three_edges_q4_independent.cpp
  role: verifier
  note: 独立したビット集合による全安全部分集合mex検証
- path: research/experiments/game-structure/output/residual_three_edges_q4_20261018.json
  role: data
  note: 全分類の機械可読結果
- path: research/experiments/game-structure/output/residual_three_edges_q4_independent.txt
  role: data
  note: C++独立照合結果と反例
- path: research/experiments/game-structure/scripts/residual_three_foursets_minimum_20261018.py
  role: verifier
  note: 全て4点の禁止集合で空盤値3の最小点数と度数を独立確認
- path: research/experiments/knowledge-audit-20261021/README.md
  role: log
  note: 証明の論理監査・再実行範囲・判定
evidence: '2026-10-21監査。7所属型への全称帰着と4/30/641型の完全性を確認。型再帰Pythonとビット再帰C++の全分布を再実行。 監査記録: research/experiments/knowledge-audit-20261021/README.md。'
---


# 3個以下・各4点以下の残余禁止集合のGrundy値上界

任意の有限点集合上の通常プレイの禁止集合ゲームで、安全局面に残る極小禁止集合が高々3個で、各集合の残点数が1〜4なら、局面のGrundy値は必ず0,1,2,3のいずれかである。禁止集合に現れない自由点は偶奇のXORとして分離できる。これは標準q=4の共円・共線ゲームの残余局面に適用できる。

証明は、禁止集合への所属を最大7種類の型に分ける全称帰着と、極小禁止集合が1,2,3個の場合の4、30、641型についての全安全状態の完全mex計算からなる。Pythonの型別残数再帰と、C++の独立したビット集合全数再帰が全分布で一致した。これは有限分類による計算機支援証明であり、形式証明器内の証明ではない。

上限3は鋭い。3個の禁止4点組 `{0,2,3,7}, {1,2,3,7}, {4,5,6,7}` の空盤はGrundy値3。各集合サイズを5まで許すと、7点の3集合で空盤値4が実現し、サイズ6まで許すと8点で値5が実現する。反例が幾何学的に実現できるとは主張しない。

11×11などの探索で残余の極小禁止集合が高々3個なら、最大12点・4096状態以下の完全再帰で厳密評価できる。ただし実測の高速化は未確認。証明・検証器・結果はartifactを参照。
