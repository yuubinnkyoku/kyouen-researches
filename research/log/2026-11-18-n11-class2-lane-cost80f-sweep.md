# 2026-11-18 n11 class2-lane cost80f: fresh v17 sweep完了・全80 bit反証 (2026-11-18)

## 背景

cost80f claim v1（`class2-lane-cost80f-inflight-20261118.json`・blob `ce1acfdb`・
census v16は`972434a4`・census v16 script `871bc0d0`・driver commit `b3d13897`、
lane dirへの再配置 `4bc3def4`）は、census v16 rank-1行
`00000000020000003800200080000000`（S6・石bits [31,45,59,60,61,89]・edge cost 80・
open 67 + confirmation 13・demand {c1:0, c2:0, c4:1}・法候補80 == edge cost）の
fresh 80-bit depth-10 sweepを計画し、長期レーンの同じセッションがdriver
`ev80f_batches_20261118.sh`で実行して完走した。80e（5つ目の完全反証）に続き、
**本行も全80 bitがREFUTED-D10**に確定し、74i・75f・79d・79e・80eに次ぐ
**6つ目の完全反証行**となった。80e行のswept化でcensus v16の19番目のverdict mapが
本行のbit 88をcanon被覆し（初のcost80e由来転移）、open 68→67となった行でもある。

## 実行: fresh v17 depth-10 sweep

- 67 open bits（7×9 + 1×4）+ 13 confirmation bitsの9バッチ。engine v17
  （blob `c132cc64`）・depth 10・cap 1e9/bit・andclose 1・pilot_d6管理。
- 80/80 verdicts確定: **0 WIN7-D10 / 80 REFUTED-D10 / 0 capped**。
  candidate nodes **51,125,648** + pilot 9×3,402。実行環境: node v22.20.0・
  sandbox（約250k nodes/s、単一runnerプロセス、foreground実行）。
  80e行（87,301,907 nodes）より約41%少ない計算量で閉じた。
- 9/9バッチがpilot_d6管理 loss=false・ちょうど3,402 nodesで開始（v17管理・全合格）。
- 確認batch 9（bits [5,27,30,35,41,46,74,79,85,88,90,93,115]）はcensus v16 overlay
  予測と**13/13完全一致**（全REFUTED-D10・衝突0）。転移元は pre-64h harvest×4・
  cost74i行×2・cost79e行×2・cost75f行×2・cost79d行×2・cost80e行×1（bit 88）。
- 決定性: det1/det8再実行はmsのみ差でfield同一
  （`class2-lane-cost80f-det-batch1-20261118.jsonl` blob `978d4657`・
  `class2-lane-cost80f-det-batch8-20261118.jsonl` blob `d5f0e4f5`）。
- v15 cross-engine: 独立v15 runner（blob `8744fc65`）で確認13 bitを再チェック、
  **13/13 REFUTED-D10一致**（pilot_d6 5,949・blob `834d0d4a`）・衝突0。
- 生バッチ監査（`audit_cost80f_raw_batches_20261118.py`・blob `8717de7d`・
  出力 `class2-lane-cost80f-raw-batches-1-9-audit-20261118.json`・blob `52abb721`）:
  全batchのpilot 3402・bit列計画一致・andclose全true・capped 0・terminal石数範囲[13,17]・
  verdict意味論の適用・**per-bit D4 root canonの独立再計算**（確認13 bitのroot canonは
  census v16転移canonと一致）・v15 crosscheck 13/13・node合計51,125,648・
  12 rawファイルのsha1 pin。80e監査（ファイル名が`dit_`になっていた）とは異なり、
  正しい`audit_cost80f_`ファイル名で出版した。

## 出版

- 12 raw JSONL（9 batch + det2 + v15 crosscheck）+ audit JSON + audit scriptの14ファイル、
  claim v2（`class2-lane-cost80f-inflight-20261118.json`・blob `e54b24a2`）、
  本logを出版。全ファイルのgit blob SHAをclaim v2にpin。
- band名cost80fはhighest+1（class2-lane cost80eの次）で衝突なし。
- なおclaim v1とdriverは一度`research/output/`・`research/scripts/`に誤配置して出版
  したため、lane dir `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/`へ
  再配置（同一blob）し、誤配置分は削除した（commit `4bc3def4`・`cdef6805`・`cabeeb1a`）。

## 制限

- 本sweepが証明するのは「このchildの80個の7石rootのそれぞれについてdepth 10以内に
  先手勝ちが存在しない（REFUTED-D10）」のみ。**REFUTED-D10はLOSS証明ではない**。
  行のreceipt foldは不要（win bit 0のため、74i/75f/79d/79e/80eと同様）。
- 11x11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4はいずれも
  **UNKNOWN** のまま。

## 次の一手

- census v17で本行をswept（80 REFUTED-D10・完全反証・証明書なし・fold不要）として記録し、
  census v16 ranking_top10のrunner-up `00000000020000003800000080008000`
  （cost 81・open 68）を次ターゲット候補として選定する。
- 並走管轄のまま手を出さないもの: 66i receipt fold残り、66j/69j/71e/72d/73i/73j/73k/73l
  fold、K09xx系、cost73k測定系。
