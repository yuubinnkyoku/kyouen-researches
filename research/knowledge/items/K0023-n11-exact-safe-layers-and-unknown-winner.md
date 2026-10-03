---
id: K0023
title: 11×11は勝敗未確定、層0〜5の安全局面数は厳密
kind: computation
status: computed
topics:
- square-outcomes
- verification
aliases: []
relations:
- type: depends_on
  target: K0001
  note: ''
artifacts:
- path: research/verification/N11-RESULT.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/data/n11_d4_final.json
  role: data
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/scripts/n11_d4.cpp
  role: solver
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: README.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
solution:
  board: 11×11
  level: unsolved
  outcome: unknown
  classification:
  - safe-layers
  coverage: 厳密列挙は層0〜5のみ
  conditions: 標準q=4・完全指摘・通常プレイ
  verification:
  - exhaustive-enumeration
  certificate: 空盤勝敗証明書なし
  independent_check: 禁止四点独立再計数・小盤回帰
  note: 打切りP/Nは真の勝敗ではない
---

# 11×11は勝敗未確定、層0〜5の安全局面数は厳密

禁止四点組は95,670個。層0〜5の厳密列挙結果は次のとおり。局面には128-bit表現が必要。

| 石数の層 | 安全集合数 | D4軌道数 |
|---|---:|---:|
| 0 | 1 | 1 |
| 1 | 121 | 21 |
| 2 | 7,260 | 970 |
| 3 | 287,980 | 36,390 |
| 4 | 8,399,740 | 1,051,657 |
| 5 | 187,879,156 | 23,489,377 |

層5から未計算の合法辺2,439,393,194本が残り、層5をg=0とするDPは打切りゲームの値である。
真の空盤勝敗について結果ファイルは `g_empty=null`、`winner=UNKNOWN`、`complete=false` と記録する。
初版の「先手必勝」は証拠不足で撤回され、先手負けを証明したわけではない。後日のDFPN作業も空盤の証明を閉じたとは確認されていない。
