---
id: K0685
title: 11x11空盤勝敗は領域機械の壁で留まる（S2 120件全て未証明、最良S3でも遠方ブロッカー60+）
kind: question
status: open
topics: [square-outcomes, certificates, verification]
aliases: []
relations:
- type: depends_on
  target: K0676
  note: 四石領域の先手勝ちは確定したが「遠方応手の全称」はoracle外
- type: depends_on
  target: K0003
  note: 条件付き証明義務と確定勝敗の区別
artifacts:
- path: research/experiments/n11-central-19-cover-20261031/output/s6sweep/s2_audit.json
  role: data
  note: S2 120件の証明済み先手勝ち数（0）・未証明数（120）の監査結果
- path: research/experiments/n11-central-19-cover-20261031/output/s6sweep/blockers.json
  role: data
  note: 各S2の最良S3に対するブロッカー数分布（最小60〜最大115）
- path: research/experiments/n11-central-19-cover-20261031/output/s6sweep/chain_audit.py
  role: source
  note: oracle限定鎖監査（W4述語のS3/S2/S1伝播）
- path: research/experiments/n11-central-19-cover-20261031/output/s6sweep/chain_blockers.py
  role: source
  note: 最良S3のブロッカー分布計測
- path: research/log/2026-11-07-n11-chain-audit.md
  role: log
  note: 鎖監査の記録
scope: 標準11x11完全指摘・通常プレイの空盤勝敗（中央初手60経路）に対する確定範囲。領域機械で閉じる部分と残る遠方ゲームの境界。
evidence: >-
  領域機械で閉じる確定範囲は五石まで（78先手勝ち・16第二手勝ち）であり、四石領域位置S4-A/Bは先手勝ちと確定した。しかし中央初手60の120応手S2のうち、領域機械（78先手勝ち五石子をoracleとするW4述語）のみでは1件も先手勝ちを証明できなかった（最良S3でも遠方ブロッカー60〜115）。「遠方応手の全称」という壁は、直接の大規模探索（4.39B visited級）と同じ種類の困難であり、11x11空盤勝敗の判定は依然としてUNKNOWNである。
---

# 領域機械の壁：空盤勝敗の残開

領域機械（K0672〜K0676）で閉じる確定範囲は五石までである：
78 先手勝ち五石子を oracle とした W4 述語（S4 の合法子に先手勝ち五石子がある）を
S3/S2/S1 へ伝播させた鎖監査では、120 S2 のうち証明済み先手勝ちは **0 件** であり、
各 S2 の最良 S3 でも遠方ブロッカー（W4 を満たさない第二手の四石応手）は **60〜115 件** 残る。

すなわち、第二手が第三手・第四手で遠方に逃げ始めると、領域機械は何も言えなくなる。
この「遠方応手の全称」という壁は、直接の大規模探索と同じ種類の困難であり、
11x11 空盤勝敗の判定は依然として **UNKNOWN** である。

残る方向は、11x11 の層別 DP プログラム（K0105 の方向）、別ソルバの開発、または資源の抜本的拡大である。
