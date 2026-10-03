---
id: K0006
title: 8×8全安全局面DPの完了報告と監査境界
kind: computation
status: needs-review
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
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round5_prand_n8.json
  role: data
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round5_n8_progress.md
  role: log
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: README.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
solution:
  board: 8×8（全局面報告）
  level: strong
  outcome: second-player-win
  classification:
  - root
  - all-safe-win-loss
  - all-safe-grundy
  coverage: 6,700,711,937安全局面のDP完了報告
  conditions: 標準q=4・完全指摘・通常プレイ
  verification:
  - reported-streaming-dp
  certificate: 全局面証明書なし。空盤証明書は別項目
  independent_check: 全状態独立検査は未確認
  note: needs-review：READMEとの差異あり、独立監査済みの強解決と区別
---

# 8×8全安全局面DPの完了報告と監査境界

Round5には全6,700,711,937安全集合の列挙とstreaming Grundy+p_rand DP完了が記録され、P=1,457,674,065、N=5,243,037,872、最大安全サイズ15。JSONの全層サイズ・P/N合計は検算可能。

READMEは8×8以上の全安全局面分類を未実施と記すため差異がある。報告は真の全局面計算を述べるが、この移行では巨大DPを再実行せず、全状態独立照合または強解決証明書も確認できていない。完了報告を消さず、独立監査済み強解決と断定しない。Grundyの全分布を正本に採用するには追加の既存資産監査が必要。
