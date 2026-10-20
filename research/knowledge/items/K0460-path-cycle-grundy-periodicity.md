---
id: K0460
title: 二点禁止の道Grundyは52以降最小周期34、最大次数2の鋭い上界は15
kind: proposition
status: needs-review
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
evidence: 2026-10-20添付統合。元資料では proved または computed と報告（個別の元statusは保存ZIPを参照）。本項目の全量化範囲に対する証明・計算の再監査は未完了。有限検証の実行範囲は統合実験のVALIDATION.mdを参照。
---


> 統合監査: 以下は取込元の主張・報告。全称証明・完全列挙の監査が未完了のため、現在の採用状態は needs-review。本文中の「証明」「一致」は元資料での報告を表す。


# 道・閉路の二点禁止残局Grundyと次数2上界

二点禁止集合のみからなる抽象通常プレイにおいて、n頂点の道のGrundy値a_nはn≥52でa_(n+34)=a_nを満たす。最小最終周期は34、周期34の最小開始点は52。全nでa_n≤9、n≥52でa_n=0 iff n mod34∈{4,8,20,24,28}。

最大次数2の任意有限単純グラフは道と閉路の直和で、各閉路のGrundy値は0または1。従って**全局面のGrundy値は15以下**。P_68⊔P_13⊔P_3⊔P_1が値15を達成し、値15に必要な最小頂点数は85。

証明は道の分割mex再帰、有限周期延長補題（52..139の88等式で全nに拡張）、16状態の厳密最短路による。Pythonと独立C++で有限基底・小さい全局面を照合した。標準正方形盤の残局でこの達成グラフが幾何的に実現可能かは未証明であり、二点以外の禁止集合がある残局には適用しない。
