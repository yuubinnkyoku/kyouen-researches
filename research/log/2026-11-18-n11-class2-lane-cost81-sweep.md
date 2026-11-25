# 2026-11-18 n11 class2-lane cost81: fresh v17 sweep完了・全81 bit反証 (2026-11-18)

## 背景

cost81 claim v1（`class2-lane-cost81-inflight-20261118.json`・blob `3e852931`・
census v17は`22078142`・census v17 script `382c375b`・driver commit `dc2e0b34`、
初回からlane dir `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/`に直接着地・
誤配置なし）は、census v17 rank-1行
`00000000020000003800000080008000`（S6・石bits [15,31,59,60,61,89]・edge cost 81・
open 66 + confirmation 15・demand {c1:0, c2:0, c4:3}・法候補81 == edge cost）の
fresh 81-bit depth-10 sweepを計画し、長期レーンの同じセッションがdriver
`ev81_batches_20261118.sh`で実行して完走した。80f（6つ目の完全反証）に続き、
**本行も全81 bitがREFUTED-D10**に確定し、74i・75f・79d・79e・80e・80fに次ぐ
**7つ目の完全反証行**となった。band名cost81は**最初のcost-81台バンド**
（repo全検索でcost81[a-z]一切なし）。80f行のswept化でcensus v17の20番目の
verdict mapが本行のbits 45/75をcanon被覆し（**初のcost80f由来転移**）、
confirmationは15 bit構成となった行でもある。

## 実行: fresh v17 depth-10 sweep

- 66 open bits（7×9 + 1×3）+ 15 confirmation bitsの9バッチ。engine v17
  （blob `c132cc64`）・depth 10・cap 1e9/bit・andclose 1・pilot_d6管理。
- 81/81 verdicts確定: **0 WIN7-D10 / 81 REFUTED-D10 / 0 capped**。
  candidate nodes **86,480,711** + pilot 9×3,402。実行環境: node v22.20.0・
  sandbox（約300k nodes/s、単一runnerプロセス、foreground実行・計約4.5分）。
  80f行（51,125,648 nodes）より約69%多い計算量。per-batch:
  b1 14,998,423 / b2 6,929,098 / b3 11,124,602 / b4 9,114,068 / b5 8,409,582 /
  b6 6,564,368 / b7 8,339,804 / b8 3,108,481 / b9-conf 17,892,285 nodes。
- 9/9バッチがpilot_d6管理 loss=false・ちょうど3,402 nodesで開始（v17管理・全合格）。
- 確認batch 9（bits [27,30,32,35,41,45,46,74,75,79,85,88,90,93,115]）はcensus v17
  overlay予測と**15/15完全一致**（全REFUTED-D10・衝突0）。転移元は
  pre-64h harvest×3・cost74i行×2・cost80e行×2・cost79e行×2・cost75f行×2・
  cost79d行×2・cost80f行×2（bits 45/75・初のcost80f由来転移）。
- 決定性: det1/det8再実行はmsのみ差でfield同一
  （`class2-lane-cost81-det-batch1-20261118.jsonl` blob `bb3f35d6`・
  `class2-lane-cost81-det-batch8-20261118.jsonl` blob `18e71d31`）。
- v15 cross-engine: 独立v15 runner（blob `8744fc65`）で確認15 bitを再チェック、
  **15/15 REFUTED-D10一致**（pilot_d6 5,949・blob `f42e202a`）・衝突0。
- 生バッチ監査（`audit_cost81_raw_batches_20261118.py`・blob `bddb9d20`・
  出力 `class2-lane-cost81-raw-batches-1-9-audit-20261118.json`・blob `f90bdccd`）:
  全batchのpilot 3402・bit列計画一致・andclose全true・capped 0・terminal石数範囲[13,17]・
  verdict意味論の適用・**per-bit D4 root canonの独立再計算**（確認15 bitのroot canonは
  census v17転移canonと一致）・v15 crosscheck 15/15・node合計86,480,711・
  12 rawファイルのsha1 pin。80f監査からの機械変換に伴うunknown_status文中の
  「80 seven-stone roots」を「81」に修正してから出版した（二重実行byte-identical）。

## 出版

- 12 raw JSONL（9 batch + det2 + v15 crosscheck）+ audit JSON + audit scriptの
  14ファイル、claim v2（`class2-lane-cost81-inflight-20261118.json`・blob `5dc33107`）、
  本logの16ファイルを1コミットで出版。全ファイルのgit blob SHAをclaim v2にpin。
- claim v1・driverは初回からlane dirに正しく着地しており、80f時のような
  再配置・削除は不要だった。

## 制限

- 本sweepが証明するのは「このchildの81個の7石rootのそれぞれについてdepth 10以内に
  先手勝ちが存在しない（REFUTED-D10）」のみ。**REFUTED-D10はLOSS証明ではない**。
  行のreceipt foldは不要（win bit 0のため、74i/75f/79d/79e/80e/80fと同様）。
- 11x11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4はいずれも
  **UNKNOWN** のまま。

## 次の一手

- census v18で本行をswept（81 REFUTED-D10・完全反証・証明書なし・fold不要）として
  記録し、census v17 ranking_top10のrunner-up `00000000020000003800000080000800`
  （cost 82・open 67）を次ターゲット候補として選定する。
- 並走管轄のまま手を出さないもの: 66i receipt fold残り、66j/69j/71e/72d/73i/73j/73k/73l
  fold、K09xx系、cost73k測定系。
