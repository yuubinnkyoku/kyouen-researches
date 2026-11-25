---
id: K0460
title: 二点禁止の道Grundyは52以降最小周期34、最大次数2の鋭い上界は15
kind: proposition
status: proved
topics:
- grundy
- residual-games
- search-methods
- strategy-length
aliases: []
relations:
- type: depends_on
  target: K0002
  note: Grundyのmexと非干渉成分のxorを用いる
- type: depends_on
  target: K0108
  note: 二点禁止残局をグラフゲームとして扱う
artifacts:
- path: research/experiments/game-structure/path-periodicity-20261019/proof.md
  role: proof
  note: 無限周期延長補題と最大次数2の鋭い上界・最小達成頂点数
- path: research/experiments/game-structure/path-periodicity-20261019/verify_path_period.py
  role: verifier
  note: 周期延長補題の88個の有限基底、全マスク再帰、最短路
- path: research/experiments/game-structure/path-periodicity-20261019/verify_path_period_independent.cpp
  role: verifier
  note: 別方式の道・閉路再帰とBellman–Ford型最短路
- path: research/experiments/game-structure/path-periodicity-20261019/path_period_results.json
  role: data
  note: 再生成可能な周期基底とGrundy値・最小頂点数
- path: research/experiments/knowledge-audit-20261021/README.md
  role: log
  note: 証明の論理監査・再実行範囲・判定
evidence: '2026-10-21監査。無限周期延長補題・88基底等式・周期最小性・16状態最短路を確認。Pythonと独立C++を再実行。 監査記録: research/experiments/knowledge-audit-20261021/README.md。'
---


# 道・閉路の二点禁止残局Grundyと次数2上界

二点禁止集合のみからなる抽象通常プレイにおいて、n頂点の道のGrundy値a_nはn≥52でa_(n+34)=a_nを満たす。最小最終周期は34、周期34の最小開始点は52。全nでa_n≤9、n≥52でa_n=0 iff n mod34∈{4,8,20,24,28}。

最大次数2の任意有限単純グラフは道と閉路の直和で、各閉路のGrundy値は0または1。従って**全局面のGrundy値は15以下**。P_68⊔P_13⊔P_3⊔P_1が値15を達成し、値15に必要な最小頂点数は85。

証明は道の分割mex再帰、有限周期延長補題（52..139の88等式で全nに拡張）、16状態の厳密最短路による。Pythonと独立C++で有限基底・小さい全局面を照合した。標準正方形盤の残局でこの達成グラフが幾何的に実現可能かは未証明であり、二点以外の禁止集合がある残局には適用しない。
