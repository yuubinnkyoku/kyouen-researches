---
id: K0674
title: 修復後46証人は全員手番WINだった：LOSS証人計画は中央領域で不成立（方向性崩壊）
kind: computation
status: computed
topics: [square-outcomes, certificates, verification]
aliases: []
relations:
- type: depends_on
  target: K0673
  note: 修復済み46証人集合（最良2,140類）の全子確定検証
- type: depends_on
  target: K0003
  note: 条件付き証明義務と確定勝敗の区別
- type: refutes
  target: K0673
  note: 修復後も全46証人が手番WINであり、修復計画のLOSS前提も崩壊する
artifacts:
- path: research/experiments/n11-central-19-cover-20261031/output/frontier2140/aggregation.json
  role: data
  note: 修復後46証人の勝敗集計（46/46手番WIN、missing 0）
- path: research/experiments/n11-central-19-cover-20261031/output/frontier2140/verified.json
  role: data
  note: フロンティア2,401類の独立監査結果（loss 1,777 / win 624 / fails 0）
- path: research/experiments/n11-central-19-cover-20261031/output/frontier2140/classify_frontier.sh
  role: source
  note: 2091フロンティア分類ドライバ（focus62 除外、8並列）
- path: research/experiments/n11-central-19-cover-20261031/output/frontier2140/verify_classify.py
  role: verifier
  note: 独立4x4 Bareiss監査器による分類結果の監査ドライバ（8並列）
- path: research/experiments/n11-central-19-cover-20261031/output/frontier2140/aggregate_repair.py
  role: source
  note: 修復後46証人の勝敗集計スクリプト（基準集合=2091 derivation）
- path: research/log/2026-11-06-n11-frontier2140-all-first-win.md
  role: log
  note: 全2,140類確定の経緯
scope: 標準11x11完全指摘・通常プレイの修復後46六石証人集合の全7手目子2,140類（全類確定済み）。
evidence: >-
  修復後46証人の全7手目子2,140類を確定戦略生成器（generate_five_terminal_loss7.cpp）で全探索し、独立の 4x4 Bareiss 監査器（verify_five_terminal_loss7.py）で全件検証した（focus62 の62類を含め合計2,463類を検証し、fails 0; フロンティア自身は1,777 LOSS7・624 WIN7・タイムアウト0）。集計結果、46証人全員が手番（先手）WINであり、LOSSは0件であった。すなわち、K0673の修復計画の前提（46証人がLOSS候補であること）も崩壊し、中央領域における第二手WINの条件付き計画は方向性ごと不成立となった。六石LOSS・二石root・空盤勝敗は従来どおりUNKNOWN。
---

# 46証人の全員手番WIN

K0673 の修復済み46証人集合について、その全7手目子 **2,140 類** を確定戦略生成器で
全探索し、独立の 4x4 Bareiss 監査器で全件検証した（合計 2,463 類を検証、fails 0）。

結果は **46証人全員が手番（先手）WIN、LOSS は 0 件** であった。

## 含意：条件付き計画の方向性崩壊

K0673 の修復計画の前提（46証人が LOSS 候補であること）は崩壊した。
中央領域における「第二手が六石 LOSS 証人で先手に勝つ」という条件付き計画の
方向性は不成立となった。六石 LOSS・二石 root・空盤勝敗は従来どおり UNKNOWN であり、
次段は先手 WIN の証人構造（S6 全集合の WIN-for-mover スイープ）への転換である。

各証人の内訳（子数・LOSS7 数・WIN7 数）は `aggregation.json` に収録した。
