---
id: K0424
title: 11盤のS5九局面を終局DAGで独立証明し、共同計画を層別13・上界31,774・下界6,585へ更新
kind: proposition
status: proved
topics: [square-outcomes, certificates, verification, search-methods, provenance]
aliases: []
relations:
- type: depends_on
  target: K0371
  note: 元先手固定のAND/OR極性と終局payoff
- type: depends_on
  target: K0422
  note: 九局面の現行パイロット選択と完全合法境界
- type: supports
  target: K0417
  note: 層別13の確定 verdict をLOSS共同計画の修復に供給
- type: supports
  target: K0420
  note: WIN 6件をWIN証人側の確定に供給、LOSS 3件を証人候補から除外
artifacts:
- path: research/experiments/n11-adaptive-verify-20261013/output/adaptive10m-manifest.json
  role: manifest
  note: 126899 LOSS・144095 WINの10M探索記録
- path: research/experiments/n11-adaptive-probe-20261013/output/adaptive10m-manifest.json
  role: manifest
  note: 121263 LOSS・145001 LOSSの10M探索記録
- path: research/experiments/n11-night-batch1-20261014/output/nightb10m-manifest.json
  role: manifest
  note: 126017 WINの10M探索記録
- path: research/experiments/n11-night-batch2-20261014/output/nighta25m-manifest.json
  role: manifest
  note: 197665 WINの25M予算拡張探索記録
- path: research/experiments/n11-night-batch3-20261014/output/nighta25m-manifest.json
  role: manifest
  note: 206386 WINの25M予算拡張探索記録
- path: research/experiments/n11-night-batch4-20261014/output/nighta25m-manifest.json
  role: manifest
  note: 131631 WINの25M予算拡張探索記録
- path: research/experiments/n11-night-batch5-20261014/output/nighta25m-manifest.json
  role: manifest
  note: 162106 WINの25M予算拡張探索記録
- path: research/experiments/n11-night-plan-update7-20261015/output/repaired-joint-plan-update7.json
  role: data
  note: 162106 WINとS6由来LOSS 3件を反映した第7次計画（上界31,771・層別17）
- path: research/experiments/n11-night-plan-update8-20261016/output/repaired-joint-plan-update8.json
  role: data
  note: 層別外3件＋S6未反映2件＋新規LOSS 150871を反映した第8次計画（上界31,859・層別18）
- path: research/experiments/n11-night-plan-update8-20261016/output/update8probe10m-manifest.json
  role: manifest
  note: 150871 LOSS（SOLVED verdict 2）・144774 NODE_LIMITの10M探索記録
- path: research/experiments/n11-night-plan-update8-20261016/output/receipt-150871.json
  role: certificate
  note: 150871 LOSSの終局DAG独立検査receipt（trusted葉0・644,490節点/971,480辺/83,851終局）
- path: research/experiments/n11-night-plan-update6-20261014/output/repaired-joint-plan-update6.json
  role: data
  note: 層別13反映のLOSS共同計画（上界31,774・完全境界再検算済み）
- path: research/experiments/n11-night-plan-update6-20261014/output/updated-element-dual-update6.json
  role: certificate
  note: 厳密双対の整数下界6,585（--verify通過）
- path: research/experiments/n11-night-plan-update6-20261014/output/win-side-reanalysis6.json
  role: data
  note: WIN側再被覆（pool 1,933・未閉鎖1,746・AND幅6,812）
scope: 標準11×11・q=4・通常プレイ。点番号y*11+x、元先手固定視点。安全S5九局面のみ。
evidence: 下表の九局面はいずれも全ての葉が幾何終局のDAGを保存し、solver/cacheを読まない共通検査器で完全検査。trusted葉0。九局面の分類で空盤勝敗は未確定。本項目の夜間時点の計画は上界31,774・下界6,585・層別13（6W+7L）。162106は検証済みで、第7次計画更新（2026-10-16・update7）により層別17（WIN 7＋LOSS 10）の凍結計画へ反映された。K0426のS6 LOSS終局証明の独立検証により、選択S4固定のまま要求S5和集合は31,771へ縮小（K0417参照）。
---

九局面はいずれも後手手番の5石安全局面である。LOSSは存在するS6子LOSS、WINは全S6子WIN（元先手固定視点・K0371）。

| 索引 | S | 極性 | 探索節点 | 終局DAG（節点/辺/終局） | trusted葉 |
|---:|---|---|---:|---|---:|
| 126899 | {2,5,8,49,60} | LOSS | 3,184,967 | 681,865/1,033,755/89,555 | 0 |
| 121263 | {1,5,9,49,60} | LOSS | 4,687,601 | 886,321/1,311,857/129,572 | 0 |
| 145001 | {23,60,61,65,89} | LOSS | 4,202,236 | 684,862/1,025,990/91,722 | 0 |
| 144095 | {5,45,49,53,60} | WIN | 4,152,553 | 895,968/1,312,454/135,795 | 0 |
| 126017 | {1,49,59,60,61} | WIN | 7,151,480 | 1,318,386/1,984,060/178,988 | 0 |
| 197665 | {37,49,59,60,61} | WIN | 10,294,083 | 1,624,418/2,433,495/227,142 | 0 |
| 206386 | {49,51,59,60,71} | WIN | 11,024,416 | 1,592,383/2,384,095/223,354 | 0 |
| 131631 | {2,49,59,60,61} | WIN | 22,709,147 | 2,815,975/4,139,862/429,845 | 0 |
| 162106 | {14,49,59,60,61} | WIN | 18,141,378 | 2,372,823/3,500,917/352,077 | 0 |

共通の独立検査器は整数幾何・合法追加・D4正準化・石数順位・全称節点の全具体合法手・存在節点の証人・終局payoffを全件再生成し、Python独立再検査とも一致した。Lean内の形式検査ではない。

あわせて既存solver結果の3件（137694 S={4,5,6,49,60}・143240 S={5,15,17,49,60}・220231 S={35,38,41,60,71、いずれもLOSS）をfrozen trace SHA一致のうえ同検査器で終局検証し独立証拠へ昇格した。独立receipt累積17件。

計画への反映は6段階で実施し、一括反映と段階反映の確定ラベル・合法候補・証明義務の一致を検査した（上界差分0）。LOSS側は除外S4 17件を代替選択で修復し上界31,774（K0423修復時の31,636から+138）。双対下界は6,585（+8、毎回厳密有理数で--verify再構成）。WIN側は保存pool 1,933・未閉鎖1,746・AND幅6,812、応手軌道[1,2,4,15,79,101]の6件が保存pool内で不能。新規証人の創作はなし。新規閉鎖の第三手・応手軌道は0。28候補中の内訳はWIN 7・LOSS 8・UNKNOWN 13。144019・144692は10MでNODE_LIMITのまま据え置いた。

11×11空盤勝敗、残り16候補（層別外3件を含む）、他のS5、全S6の求解は未完了。2026-10-15のK0426検証と2026-10-16の第7次計画更新による要求S5和集合31,771と下界6,585はK0417を参照。

## 第8次計画更新（2026-10-16・update8）

適応探索線の検証済みverdictに、focus10m由来の3件（115540 LOSS・144193 LOSS・144311 WIN、いずれも
共通検査器 `0f890cb4…`・trusted葉0）と、本ラウンドの新規10M探索150871 LOSS（SOLVED verdict 2・
3,744,513 nodes・終局DAG 644,490節点/971,480辺/83,851終局・trusted葉0、Python独立再導出一致）を加え、
凍結計画へ反映した。層別 **18（WIN 7＋LOSS 11）**・上界 **31,859**・下界 **6,587**・除外S4 **23件**。
144774は同一10MでNODE_LIMIT（UNKNOWN）につき証拠にせず、同条件再探索は禁止。詳細は
`research/experiments/n11-night-plan-update8-20261016/` と `research/log/2026-10-16-n11-plan-update8.md`。
空盤勝敗・残りの候補・他のS5・全S6の求解は引き続き未完了。
