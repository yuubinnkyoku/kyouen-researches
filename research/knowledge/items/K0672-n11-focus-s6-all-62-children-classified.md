---
id: K0672
title: 11x11中央49条件付き計画のfocus六石局面の全62子局面を確定（35 LOSS7・27 WIN7）
kind: computation
status: computed
topics: [square-outcomes, certificates, verification]
aliases: []
relations:
- type: depends_on
  target: K0670
  note: 2091条件付き計画のfocus六石局面 00000000000000203808000000000040
- type: depends_on
  target: K0003
  note: 条件付き証明義務と確定勝敗の区別
artifacts:
- path: research/experiments/n11-central-19-cover-20261031/output/focus2154_62certs/verified.json
  role: data
  note: 62件の独立監査結果（loss 35 / win 27 / fails 0、各証明書sha256を収録したmanifest）
- path: research/experiments/n11-central-19-cover-20261031/output/focus2154_62certs/results.json
  role: data
  note: 生成器の実行結果（states/reachable等の内訳）
- path: research/experiments/n11-central-19-cover-20261031/output/focus2154_62certs/run_focus62.sh
  role: source
  note: 並列生成スクリプト。62件のcert本体はマシンローカルの /mnt/d/kyouen-focus-certs/ に保存し、生成器＋根から再生成可能
- path: research/experiments/n11-central-19-cover-20261031/output/focus2154_62certs/verify_focus62.py
  role: verifier
  note: 独立4x4 Bareiss監査器による62件の監査ドライバ（fails 0）
- path: research/log/2026-11-06-n11-focus62-classified.md
  role: log
  note: 本確定の経緯
scope: 標準11x11完全指摘・通常プレイの六石局面 00000000000000203808000000000040 の全7手目子62件。
evidence: >-
  focus2154_plan.json の unverified_s7 62件すべてに確定戦略生成器（generate_five_terminal_loss7.cpp）で終局まで全探索した結果、LOSS7 35件・WIN7 27件を得た。生成器と独立の 4x4 Bareiss 監査器（verify_five_terminal_loss7.py）で62件すべて PASS（fails 0）。WIN7 子が27件存在するため、focus_s6 の手番（先手）に勝ち手があり、focus_s6 は terminal 戦略レベルで先手勝ちと確定する。これは K0670 等の条件付き計画の outcomes を変更するものではない（従来どおり UNKNOWN）。
---

# 62子局面の確定

2091条件付き計画（K0670）のfocus六石局面 `00000000000000203808000000000040` の
未検証 S7 子 62 件（focus2154_plan.json の unverified_s7）を全探索した。
結果は LOSS7 35 件・WIN7 27 件で、独立の 4x4 Bareiss 監査器により
62 件すべて PASS（fails 0）を確認した。

WIN7 子が 27 件存在するため、この六石局面は手番（先手）にとって
先手勝ちと確定する。これは条件付き計画（K0670 等）の outcomes を
変更するものではない（従来どおり UNKNOWN）。

証明書本体（62件、合計約24M）はマシンローカルの
`/mnt/d/kyouen-focus-certs/` に保存し、生成器と監査器の再実行で
再生成可能。各certの sha256 は `verified.json` に収録した。
