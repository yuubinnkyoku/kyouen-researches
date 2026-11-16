---
id: K0868
title: "S6→S7 sweep候補規約の確定 — own_candidates・edge costは6石の任意の3つ組と共円にも共線にも乗らない空セル（survival moves）であり、det4整数演算で石配置から独立再導出できる"
kind: definition
status: active
computed: 2026-11-16
topics: [bookkeeping, certificates, verification]
aliases: [s6-s7 sweep candidate convention, own_candidates convention, survival move convention]
relations:
- type: depends_on
  target: K0001
  note: 生残条件は共円禁止規則（q=4・完全指摘）の勝利条件の否定（退化円=直線を含む）
- type: depends_on
  target: K0783
  note: worklist・receipt・foldの簿記規約（own_candidates列・edge cost・bits）
artifacts:
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost65f-win2-structural-audit-20261116.json
  role: primary output
  note: 候補規約確定の正本記録。42/42 cost階層・17/17 receipts bits・65f child再導出・円のみ規約の9行不一致リスト
- path: research/experiments/n11-class2-lane-closability-ranking-20261116/output/class-frontier-remaining-s6-worklist-1410-20261116.csv
  role: input data
  note: worklist-1410全6,438行のown_candidates・edge cost列の正本
- path: research/log/2026-11-16-n11-class2-lane-cost65f-win2-structural-audit.md
  role: report
  note: 規約確定とbits 20/21構造監査のログ
scope: "n11 class-lane head-1410のS6行（6石の自分の石配置）からS7へのsweep候補の法定義と、worklist-1410のedge cost列・65j fold v2の17 receipts bits・65f childのpublished値との一致"
evidence: "第三実装（TypeScript・BigInt・D4正準化・整数のみdet3/det4）による独立再導出: (a) 65f child 00000000000000809102000080000000 で completing 50・survival 65・published edge cost 65と完全一致、(b) 65j fold v2の17/17 receipts bitsが全てsurvival合法、(c) worklist-1410の6,438行からcost階層ごとに42層サンプリングして42/42完全一致、(d) 共線を除外した円のみ規約は9/42階層で不一致（常にderived≧published、cost-57行で63・cost-78行で90）。不一致9行のリストはaudit JSONに記録"
---

## 主張

S6行 R（自分の石6個の配置）に対する legal S6→S7 sweep 候補集合（worklist-1410 の own_candidates 列・edge cost の意味するもの）は次で定義される。

own_candidates(R) = { 空セル d : 任意の3つ組 {a,b,c} ⊆ stones(R) について det4(a,b,c,d) ≠ 0 }

ただし

det4(a,b,c,d) = det3(a,b,c) − det3(a,b,d) + det3(a,c,d) − det3(b,c,d)

det3(p,q,r) = 行 [x²+y², x, y] の3×3行列式。

つまり候補セルは「既存6石のどの3つ組とも共円にも共線（退化円）にも乗らない」セルである。sweep は完成手（ある3つ組と共円になるセル = その手番の勝ち）ではなく生き残り手（survival moves）を列挙し、edge cost = |own_candidates(R)| である。3つ組は退化（共線）しているものも除外せずそのまま含める。det4 = 0 は「共円または共線」の条件そのものであり、共線3つ組についても4点目がその直線上にあるセルが候補から除外される。

系として、worklist 全6,438行の own_candidates 列は石配置だけから厳密整数演算で独立再導出可能であり、edge cost 列は sweep の mobility の測度であってゲーム理論的な量ではない。

## 検証

- 65f child 00000000000000809102000080000000: completing 50・survival 65。survival 65 が published edge cost 65 と完全一致（50+65 = 115 = 121−6 で全空セルの完全分割とも一致）。
- 65j fold v2 receipts 17/17 の bits はすべてこの規約で survival 合法（bits 20/21 を含む）。
- worklist-1410（6,438行）から edge cost 階層ごとに42層をサンプリングし、own_candidates を再導出して 42/42 完全一致。
- 共線を除外した「円のみ」規約では 9/42 階層で不一致（常に derived ≧ published、例: hex 00000000000000003800001001800000 は published 57 に対し円のみ規約で63、hex 00000000000000003800000000000025 は published 78 に対し90）。不一致9行の完全なリストは audit JSON に記録。このため共線を含む規約が正しい規約として確定した。

## 境界

- worklist-1410 の検証は42階層サンプリングによる（6,438行全行の単独再導出ではない）。65f child と17 receipts は全数検証。
- 本項目は sweep 候補・edge cost の規約確定であり、いかなる勝敗判定でもない。verdict 規約（raw batch loss:true = WIN7-D10、loss:false = REFUTED-D10、capped:true = 未解決）は本項目と独立で、REFUTED-D10 は LOSS 証明ではない。
- 初期の「円完成側が合法」という誤読（65f bits 20/21 を illegal と誤判定した原因）は訂正済み。bits 20/21 は両方とも cost-64 の win_receipt_scheduled 行を cover する receipts であり、fold v2 適用監査の C3（commit 72d18d2c）と交差検証済み。
- 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。
