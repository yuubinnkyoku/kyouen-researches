---
id: K0005
title: 7×7の全安全局面Grundy・P/N分類と独立監査
kind: computation
status: computed
topics:
- grundy
- square-outcomes
- verification
aliases: []
relations:
- type: depends_on
  target: K0002
  note: ''
artifacts:
- path: research/experiments/original-claims/reports/round28-seven-board-original-verdicts.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round28_n7_audited.json
  role: data
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round28_n7_independent.json
  role: data
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/scripts/round28_recursive_verify.cpp
  role: verifier
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
solution:
  board: 7×7
  level: strong
  outcome: second-player-win
  classification:
  - root
  - all-safe-win-loss
  - all-safe-grundy
  coverage: 179,810,350/179,810,350安全局面
  conditions: 標準q=4・完全指摘・通常プレイ
  verification:
  - exhaustive-enumeration
  - independent-enumeration
  certificate: 空盤証明書あり。強解決単独証明書は未整理
  independent_check: 全層独立再帰照合
  note: README旧説明に全Grundy結果を補完
---

# 7×7の全安全局面Grundy・P/N分類と独立監査

全179,810,350安全集合、1,499,354,401合法辺を監査済み。Round28では真のmex、T*、WFTを層別DPで計算し、幾何を再生成・逆順再帰する第二方式と全層分布・最大Grundy・状態数・0〜3石19,650局面のg/T*/WFTが一致した。

READMEの「P/Nのみ」という記述より後の結果で、全Grundyも計算済み。巨大層ファイルはGit非管理で、全ソースと監査JSONが根拠。単独配布の強解決証明書は未整理。
