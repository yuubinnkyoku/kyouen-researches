---
id: K0105
title: 11×11の真の空盤勝敗は現在の主要未解決問題
kind: question
status: open
topics:
- square-outcomes
aliases: []
relations:
- type: depends_on
  target: K0023
  note: ''
- type: depends_on
  target: K0028
  note: ''
- type: depends_on
  target: K0312
  note: 最小極大サイズの境界は空盤勝敗と別の確定結果
- type: depends_on
  target: K0313
  note: 最大安全サイズの存在下界は空盤勝敗を決めない
artifacts:
- path: research/log/claim-audit/N11-DFPN-NIGHT-REPORT-2026-09-30.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/n11-search-methods/reports/N11-RESULT.md
  role: source
  note: 層0..5の厳密列挙と層6以降の資源下界
- path: research/experiments/saturation/reports/saturation-20261003.md
  role: source
  note: 8≤s_11≤10の有限完全排除と10石証人
- path: research/experiments/saturation/reports/saturation-20261003-extra.md
  role: source
  note: K_11≥21の独立検査済み安全配置
scope: 標準q=4・完全指摘・通常プレイの11×11空盤勝敗。層列挙・極大サイズ・misère勝敗とは別。
---

# 11×11の真の空盤勝敗は現在の主要未解決問題

標準通常版11×11の真の空盤勝敗はUNKNOWN。厳密な安全局面列挙は層0..5までで、層5には未計算の合法辺2,439,393,194本が残る。層5を終局にした旧DP勝敗は撤回済み。

層6の安全局面数は一般被覆評価でも3,194,106,864以上となり、既存環境での全状態DPは資源上困難。df-pn系探索の局所完了・途中統計は空盤全体の完了を意味しない。

周辺では8≤s_11≤10とK_11≥21が確定している。前者の8・9石極大の有無、後者の真の最大サイズは未確定であり、いずれも空盤勝敗とは別の問題である。

空盤の決着には真の終局まで閉じるAND/OR証明または正しい完了求解が必要。旧one-wordのK_11=11、打切りDP、proof numberを勝敗根拠にしない。
