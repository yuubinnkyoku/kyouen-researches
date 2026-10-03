---
id: K0006
title: 8×8の全6,700,711,937安全局面をGrundy DPで完全計算
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
- path: research/verification/round5-batch-n8.md
  role: source
  note: 全安全局面列挙・streaming DP完走と集計
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round5_prand_n8.json
  role: data
  note: 層別状態数・P/N数・最大安全サイズを保存
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round5_n8_progress.md
  role: log
  note: 列挙再実行・交差検証・streaming solve完走の記録
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: README.md
  role: source
  note: 空盤勝敗と全局面計算の検証境界
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
solution:
  board: 8×8
  level: strong
  outcome: second-player-win
  classification:
  - root
  - all-safe-win-loss
  - all-safe-grundy
  coverage: 6,700,711,937/6,700,711,937安全局面
  conditions: 標準q=4・完全指摘・通常プレイ
  verification:
  - reported-streaming-dp
  certificate: 全局面証明書なし。空盤証明書は別項目
  independent_check: n=6で既知値と全一致、n=7で既知層サイズを照合。8×8全状態の独立再計算は未実施
  note: 全局面Grundy DP完走済み。独立全状態検査・強解決証明書は未整備
---

# 8×8の全6,700,711,937安全局面をGrundy DPで完全計算

Round5で全6,700,711,937安全集合を列挙し、streaming DPで全局面のGrundy値とp_randを計算した。集計はP=1,457,674,065、N=5,243,037,872、最大安全サイズK_8=15で、空盤はg=0となり既知の後手勝ちと一致する。

実装はn=6で既知の状態数・層別P/N・p_randと完全一致し、n=7でも既知の層サイズとの照合を行ってからn=8を実行した。古いREADME・考察文書にある「8×8以上は全局面未計算」という記述は、このRound5完走より前の状態を反映したものなので更新する。

これは計算内容として8×8の強解決に相当する。ただし8×8の67億状態を別実装で全再計算した独立監査や、全局面を覆う配布用の強解決証明書があるという意味ではない。「全局面計算済み」と「独立全件検査済み」は区別する。
