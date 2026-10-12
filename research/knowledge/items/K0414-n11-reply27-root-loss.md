---
id: K0414
title: 11×11二石局面{60,27}は元先手固定視点でLOSS
kind: proposition
status: computed
topics: [square-outcomes, certificates, verification, provenance]
aliases: []
relations:
- type: depends_on
  target: K0001
  note: 標準共円ゲームの合法手・終局規則
- type: depends_on
  target: K0002
  note: 元の先手に固定した勝敗と偶数OR・奇数AND
- type: depends_on
  target: K0355
  note: 保存exact S5 frontierと既存117第三手被覆の系譜
- type: depends_on
  target: K0372
  note: solver-trusted exact値とterminal-only独立証明の信頼区分
- type: depends_on
  target: K0373
  note: 第三手100・108の反射同値性
artifacts:
- path: research/experiments/n11-s4-boundary-direct-20261012/README.md
  role: source
  note: 探索選定、全結果、費用、信頼範囲、再現手順
- path: research/experiments/n11-s4-boundary-direct-20261012/output/s6-fourteenth-batch-audit.json
  role: verifier
  note: 15M S6 LOSS rawを独立幾何・極性・AND伝播で監査したreceipt
- path: research/experiments/n11-s4-boundary-direct-20261012/output/raw/s6-211.csv
  role: solver
  note: S6 LOSS witnessの完全solver replay raw
- path: research/experiments/n11-s4-boundary-direct-20261012/output/s5-s6-derived-cache-merge-receipt.json
  role: manifest
  note: S5 LOSSのexact-only safe atomic mergeと最終cache SHA-256
- path: research/experiments/n11-s4-boundary-direct-20261012/output/frontier-after-s6-parent-loss.json
  role: certificate
  note: 独立整数幾何で再生成した全3,384 S4境界と119/119被覆
- path: research/experiments/n11-s4-boundary-direct-20261012/output/root-60-27-loss-proof.json
  role: certificate
  note: 119個の合法root手それぞれにS4 LOSS応手を割り当てたAND/OR監査
- path: research/experiments/n11-s4-boundary-direct-20261012/output/cardinality-after-s6-parent-loss.json
  role: data
  note: 追加必要class数0と有理LP双対0の再計算
- path: research/experiments/n11-s4-boundary-direct-20261012/output/candidate-ranking-after-s6-parent-loss.json
  role: data
  note: 以前の残余100・108に関わる115 classの再分類・費用proxy順位
- path: research/experiments/n11-s4-boundary-direct-20261012/scripts/audit_raw_inventory.py
  role: verifier
  note: 全batch receiptのraw replay rowとSHA-256を再照合
- path: research/experiments/n11-s4-boundary-direct-20261012/output/raw-sha256-audit.json
  role: manifest
  note: 202参照・176個のunique raw全件のSHA、key、極性、費用を照合
- path: research/experiments/n11-s4-boundary-direct-20261012/input/saved-s6-raw-relocations.json
  role: manifest
  note: 保存S6 raw 2件の履歴由来、移動先、SHA-256を固定
scope: 11×11標準通常版の二石root {60,27} 一局面。固定元先手視点で119合法手を全て分類する。11×11空盤面の勝敗は含まない。
evidence: solver-trusted exact S5 evidenceを持つcacheから独立Boardが全3,384 S4 child境界を再生成した。対象S4 `(1297036692683752448,0)` はcanonical S5子106件すべてLOSS。最後のS5 `(1152921504607899649,536870912)` は、15M direct S5 UNKNOWN後、98 S6子のうち保存済み2 WINを再利用し、1Mで96子（77 WIN / 19 UNKNOWN）、そのUNKNOWNのうち15Mで12子（11 WIN / 1 LOSS）を解いた。S6 LOSS witness `(1152921504675009536,536870912)` は5,859,060 nodes。S5 odd ANDはこの一つの子によりLOSS、対象S4 even ORは全106 S5 LOSSによりLOSS。これにより全119 root moveにS4 LOSS応手を確認し、{60,27} even OR rootをLOSSとした。監査receipt23件が参照する202 raw記録を再読し、176 unique rawのSHA-256とreplay fieldsを照合、未追跡local raw参照は0件。unknownのまま残ったS6はroot verdictに不要。solver葉・保存cacheへの信頼は残り、terminal-only独立minimax DAGではない。
solution:
  board: "11×11"
  level: weak
  outcome: second-player-win
  classification: [root, first-moves]
  coverage: "119/119 legal moves from root {60,27}; 100 and 108 use S4 (1297036692683752448,0)"
  conditions: "標準q=4・完全指摘・通常プレイ・元先手固定視点"
  verification: [exact-search, csv-audit, independent-enumeration]
  certificate: "全119手に少なくとも一つS4 LOSS応手。新規S4の106 S5子は全てexact LOSS。solver-trusted leavesを使用。"
  independent_check: "独立Boardが全合法root手、S4応手、各S4の完全S5境界、AND/OR極性を再生成・照合。終局のみの独立DAGではない。"
  note: "二石局面{60,27}だけをLOSSと分類。11×11空盤面の勝者は未確定。"
---

# 二石root `{60,27}` のLOSS

二石root `{60,27}` からの119合法手すべてについて、次の三石位置が少なくとも一つの四石LOSS応手を持つ。三石は奇数石のAND位置なので各三石位置がLOSSとなり、二石rootは偶数石のOR位置なのでrootもLOSSとなる。独立整数幾何によるcoverageは119/119で、従来未被覆だった第三手100・108はS4 `(1297036692683752448,0)` がともに覆う。

このS4の完全canonical S5境界106件はすべてexact LOSS。最後の一件は直接S5探索では15M UNKNOWNだったが、保存済みS6 WINを再利用した後、層別探索でS6 LOSS witnessを得た。親S5のAND伝播とS4境界の全子LOSSを独立監査した。

勝敗葉はsolver-trusted exactであり、保存cacheに由来する従来の信頼依存も残る。root coverageと合法境界は独立再生成したが、全ゲーム木を終局まで展開したterminal-only独立minimax証明とは区別する。この結果は `{60,27}` のみで、11×11空盤面の勝敗は決めない。
